"""
AUTOLEADAI - Call Logging Module
Database management and call logging system
Author: Awais Ahmad
"""
import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import config

# Setup logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)


class CallLogger:
    """
    Manages call logs and database operations
    Stores call metadata, transcripts, and spam detection results
    """
    
    def __init__(self, db_path: str = config.DB_PATH):
        """
        Initialize call logger
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        try:
            # Ensure database directory exists
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create calls table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS calls (
                    call_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    audio_path TEXT NOT NULL,
                    duration REAL,
                    transcript TEXT,
                    is_spam BOOLEAN DEFAULT 0,
                    spam_confidence REAL DEFAULT 0.0,
                    spam_features TEXT,
                    status TEXT DEFAULT 'processed',
                    metadata TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create spam_calls table for filtered calls
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS spam_calls (
                    spam_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    call_id INTEGER,
                    audio_path TEXT,
                    transcript TEXT,
                    spam_confidence REAL,
                    spam_features TEXT,
                    blocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (call_id) REFERENCES calls (call_id)
                )
            ''')
            
            # Create transcripts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transcripts (
                    transcript_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    call_id INTEGER,
                    full_text TEXT,
                    language TEXT,
                    segments TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (call_id) REFERENCES calls (call_id)
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info(f"Database initialized: {self.db_path}")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def log_call(self, audio_path: str, transcript: Dict, spam_result: Dict,
                 duration: float = 0.0, metadata: Dict = None) -> int:
        """
        Log a processed call to database
        
        Args:
            audio_path: Path to audio file
            transcript: Transcript dictionary from STT
            spam_result: Spam detection result
            duration: Call duration in seconds
            metadata: Additional metadata
        
        Returns:
            call_id of logged call
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Extract spam features
            spam_features_json = json.dumps(spam_result.get('features', {}))
            
            # Insert into calls table
            cursor.execute('''
                INSERT INTO calls (
                    audio_path, duration, transcript, is_spam, 
                    spam_confidence, spam_features, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                audio_path,
                duration,
                transcript.get('text', ''),
                spam_result.get('is_spam', False),
                spam_result.get('confidence', 0.0),
                spam_features_json,
                json.dumps(metadata or {})
            ))
            
            call_id = cursor.lastrowid
            
            # Log transcript details
            cursor.execute('''
                INSERT INTO transcripts (call_id, full_text, language, segments)
                VALUES (?, ?, ?, ?)
            ''', (
                call_id,
                transcript.get('text', ''),
                transcript.get('language', 'en'),
                json.dumps(transcript.get('segments', []))
            ))
            
            # If spam, log to spam_calls table
            if spam_result.get('is_spam', False):
                cursor.execute('''
                    INSERT INTO spam_calls (
                        call_id, audio_path, transcript, 
                        spam_confidence, spam_features
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (
                    call_id,
                    audio_path,
                    transcript.get('text', ''),
                    spam_result.get('confidence', 0.0),
                    spam_features_json
                ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Call logged successfully: call_id={call_id}, spam={spam_result.get('is_spam')}")
            return call_id
            
        except Exception as e:
            logger.error(f"Failed to log call: {e}")
            raise
    
    def get_call(self, call_id: int) -> Optional[Dict]:
        """
        Retrieve call details by ID
        
        Args:
            call_id: Call ID
        
        Returns:
            Call details dictionary or None
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM calls WHERE call_id = ?', (call_id,))
            row = cursor.fetchone()
            
            if row:
                result = dict(row)
                result['metadata'] = json.loads(result.get('metadata', '{}'))
                result['spam_features'] = json.loads(result.get('spam_features', '{}'))
                conn.close()
                return result
            
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve call: {e}")
            return None
    
    def get_all_calls(self, limit: int = 100, spam_only: bool = False) -> List[Dict]:
        """
        Retrieve all calls
        
        Args:
            limit: Maximum number of calls to retrieve
            spam_only: If True, only return spam calls
        
        Returns:
            List of call dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if spam_only:
                query = 'SELECT * FROM calls WHERE is_spam = 1 ORDER BY timestamp DESC LIMIT ?'
            else:
                query = 'SELECT * FROM calls ORDER BY timestamp DESC LIMIT ?'
            
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                call_dict = dict(row)
                call_dict['metadata'] = json.loads(call_dict.get('metadata', '{}'))
                call_dict['spam_features'] = json.loads(call_dict.get('spam_features', '{}'))
                results.append(call_dict)
            
            conn.close()
            return results
            
        except Exception as e:
            logger.error(f"Failed to retrieve calls: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """
        Get call statistics
        
        Returns:
            Dictionary with statistics
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total calls
            cursor.execute('SELECT COUNT(*) FROM calls')
            total_calls = cursor.fetchone()[0]
            
            # Spam calls
            cursor.execute('SELECT COUNT(*) FROM calls WHERE is_spam = 1')
            spam_calls = cursor.fetchone()[0]
            
            # Legitimate calls
            legitimate_calls = total_calls - spam_calls
            
            # Average spam confidence
            cursor.execute('SELECT AVG(spam_confidence) FROM calls WHERE is_spam = 1')
            avg_spam_confidence = cursor.fetchone()[0] or 0.0
            
            conn.close()
            
            stats = {
                'total_calls': total_calls,
                'spam_calls': spam_calls,
                'legitimate_calls': legitimate_calls,
                'spam_rate': (spam_calls / total_calls * 100) if total_calls > 0 else 0,
                'avg_spam_confidence': round(avg_spam_confidence, 2)
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {}
    
    def export_to_csv(self, output_path: str, spam_only: bool = False):
        """
        Export calls to CSV file
        
        Args:
            output_path: Path to output CSV file
            spam_only: Export only spam calls
        """
        try:
            import csv
            
            calls = self.get_all_calls(limit=10000, spam_only=spam_only)
            
            if not calls:
                logger.warning("No calls to export")
                return
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=calls[0].keys())
                writer.writeheader()
                writer.writerows(calls)
            
            logger.info(f"Exported {len(calls)} calls to {output_path}")
            
        except Exception as e:
            logger.error(f"Export failed: {e}")


# Singleton instance
_logger_instance = None


def get_call_logger() -> CallLogger:
    """Get or create singleton instance of CallLogger"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = CallLogger()
    return _logger_instance

