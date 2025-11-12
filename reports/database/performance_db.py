"""
Performance Database - SQLite database for storing historical performance data
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PerformanceDatabase:
    """Manages performance data storage and retrieval"""

    def __init__(self, db_path: str = 'reports/data/performance.db'):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self._initialize_database()

    def _initialize_database(self):
        """Create database schema if it doesn't exist"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()

        # Create tables
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                config TEXT,
                status TEXT DEFAULT 'completed'
            );

            CREATE TABLE IF NOT EXISTS benchmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL,
                category TEXT NOT NULL,
                algorithm TEXT NOT NULL,
                language TEXT NOT NULL,
                avg_time_ms REAL NOT NULL,
                median_time_ms REAL,
                stdev_time_ms REAL,
                min_time_ms REAL,
                max_time_ms REAL,
                iterations INTEGER,
                input_size INTEGER,
                avg_memory_mb REAL,
                raw_data TEXT,
                FOREIGN KEY (run_id) REFERENCES runs(run_id)
            );

            CREATE TABLE IF NOT EXISTS trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                algorithm TEXT NOT NULL,
                language TEXT NOT NULL,
                category TEXT NOT NULL,
                trend_type TEXT,
                regression_percent REAL,
                detected_at TEXT
            );

            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                details TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (run_id) REFERENCES runs(run_id)
            );

            CREATE INDEX IF NOT EXISTS idx_benchmarks_algorithm
                ON benchmarks(algorithm, language);

            CREATE INDEX IF NOT EXISTS idx_benchmarks_run
                ON benchmarks(run_id);

            CREATE INDEX IF NOT EXISTS idx_trends_algorithm
                ON trends(algorithm, language);
        ''')

        self.conn.commit()
        logger.info(f"Database initialized: {self.db_path}")

    def store_results(self, results: Dict[str, Any]):
        """
        Store complete benchmark results

        Args:
            results: Analysis results dictionary
        """
        cursor = self.conn.cursor()

        # Store run metadata
        cursor.execute('''
            INSERT INTO runs (run_id, timestamp, config, status)
            VALUES (?, ?, ?, ?)
        ''', (
            results['run_id'],
            results['timestamp'],
            json.dumps(results['config']),
            'completed'
        ))

        # Store benchmark results
        for category, algorithms in results['benchmarks'].items():
            for algorithm, languages in algorithms.items():
                for language, data in languages.items():
                    if 'error' in data:
                        continue

                    cursor.execute('''
                        INSERT INTO benchmarks (
                            run_id, category, algorithm, language,
                            avg_time_ms, median_time_ms, stdev_time_ms,
                            min_time_ms, max_time_ms, iterations,
                            input_size, avg_memory_mb, raw_data
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        results['run_id'],
                        category,
                        algorithm,
                        language,
                        data['avg_time_ms'],
                        data['median_time_ms'],
                        data['stdev_time_ms'],
                        data['min_time_ms'],
                        data['max_time_ms'],
                        data['iterations'],
                        data.get('input_size'),
                        data.get('avg_memory_mb'),
                        json.dumps(data)
                    ))

        # Store trends/regressions
        if 'trends' in results and 'regressions' in results['trends']:
            for regression in results['trends']['regressions']:
                cursor.execute('''
                    INSERT INTO trends (
                        algorithm, language, category,
                        trend_type, regression_percent, detected_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    regression['algorithm'],
                    regression['language'],
                    regression.get('category', 'unknown'),
                    'regression',
                    regression['regression_percent'],
                    results['timestamp']
                ))

        self.conn.commit()
        logger.info(f"Stored results for run {results['run_id']}")

    def get_historical_data(
        self,
        algorithm: str,
        language: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get historical performance data for an algorithm/language combination

        Args:
            algorithm: Algorithm name
            language: Language name
            limit: Maximum number of records

        Returns:
            List of historical benchmark results
        """
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT
                r.run_id,
                r.timestamp,
                b.avg_time_ms,
                b.median_time_ms,
                b.stdev_time_ms,
                b.input_size
            FROM benchmarks b
            JOIN runs r ON b.run_id = r.run_id
            WHERE b.algorithm = ? AND b.language = ?
            ORDER BY r.timestamp DESC
            LIMIT ?
        ''', (algorithm, language, limit))

        results = []
        for row in cursor.fetchall():
            results.append(dict(row))

        return results

    def get_latest_benchmarks(self, run_id: Optional[str] = None) -> Dict[str, Any]:
        """Get benchmarks from latest or specified run"""
        cursor = self.conn.cursor()

        if run_id is None:
            # Get latest run_id
            cursor.execute('SELECT run_id FROM runs ORDER BY timestamp DESC LIMIT 1')
            row = cursor.fetchone()
            if not row:
                return {}
            run_id = row['run_id']

        cursor.execute('''
            SELECT *
            FROM benchmarks
            WHERE run_id = ?
        ''', (run_id,))

        results = {}
        for row in cursor.fetchall():
            category = row['category']
            algorithm = row['algorithm']
            language = row['language']

            if category not in results:
                results[category] = {}
            if algorithm not in results[category]:
                results[category][algorithm] = {}

            results[category][algorithm][language] = dict(row)

        return results

    def get_performance_trends(
        self,
        algorithm: str,
        language: str,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get performance trends over time"""
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT
                r.timestamp,
                b.avg_time_ms,
                b.input_size
            FROM benchmarks b
            JOIN runs r ON b.run_id = r.run_id
            WHERE b.algorithm = ? AND b.language = ?
                AND datetime(r.timestamp) >= datetime('now', '-' || ? || ' days')
            ORDER BY r.timestamp ASC
        ''', (algorithm, language, days))

        trends = []
        for row in cursor.fetchall():
            trends.append(dict(row))

        return trends

    def store_alert(
        self,
        run_id: str,
        alert_type: str,
        severity: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """Store an alert"""
        cursor = self.conn.cursor()

        cursor.execute('''
            INSERT INTO alerts (run_id, alert_type, severity, message, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            run_id,
            alert_type,
            severity,
            message,
            json.dumps(details) if details else None
        ))

        self.conn.commit()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
