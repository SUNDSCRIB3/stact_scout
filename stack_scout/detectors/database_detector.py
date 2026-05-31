"""Database detection module."""

from typing import List, Dict
from .base import Detector, DetectionResult


class DatabaseDetector(Detector):
    """Detects databases from dependency files and config."""

    DATABASE_PATTERNS = {
        "PostgreSQL": ["psycopg2", "psycopg", "asyncpg", "pg", "postgresql"],
        "MySQL": ["mysqlclient", "mysql-connector", "pymysql", "mysql2", "mysql"],
        "SQLite": ["sqlite3", "sqlite", "better-sqlite3"],
        "MongoDB": ["mongodb", "mongoose", "pymongo", "mongod", "mongo"],
        "Redis": ["redis", "ioredis", "redis-py", "redis-cli"],
        "Elasticsearch": ["elasticsearch", "elastic", "elasticsearch-py", "opensearch"],
        "Cassandra": ["cassandra-driver", "cassandra"],
        "MariaDB": ["mariadb", "mariadb-connector"],
        "Neo4j": ["neo4j", "neo4j-driver", "py2neo"],
        "Firebase": ["firebase-admin", "firebase", "firestore"],
        "DynamoDB": ["boto3", "dynamodb", "aws-sdk"],
        "CouchDB": ["couchdb", "nano", "pouchdb"],
        "InfluxDB": ["influxdb", "influx"],
        "ClickHouse": ["clickhouse-driver", "clickhouse"],
    }

    CONFIG_INDICATORS = {
        "DATABASE_URL": "PostgreSQL",
        "POSTGRES": "PostgreSQL",
        "MYSQL": "MySQL",
        "MONGO": "MongoDB",
        "REDIS_URL": "Redis",
        "ELASTICSEARCH": "Elasticsearch",
    }

    def detect(self, file_paths: List[str], file_contents: Dict[str, str]) -> List[DetectionResult]:
        results = []
        detected_databases = {}
        all_content = " ".join(file_contents.values()).lower()

        # Check dependency files
        for db_name, patterns in self.DATABASE_PATTERNS.items():
            for pattern in patterns:
                if pattern in all_content:
                    if db_name not in detected_databases:
                        detected_databases[db_name] = {"sources": [], "confidence": "medium"}
                    if "requirement" in all_content or "package.json" in all_content:
                        detected_databases[db_name]["sources"].append("dependency file")
                        detected_databases[db_name]["confidence"] = "high"

        # Check for database-related filenames
        for path in file_paths:
            lower = path.lower()
            if "migration" in lower or "schema" in lower:
                for db_name in detected_databases:
                    detected_databases[db_name]["sources"].append(path)
            if "model" in lower:
                for db_name in detected_databases:
                    detected_databases[db_name]["sources"].append(path)

        # Check config files for database URLs
        for path, content in file_contents.items():
            content_lower = content.lower()
            for indicator, db_name in self.CONFIG_INDICATORS.items():
                if indicator.lower() in content_lower and db_name not in detected_databases:
                    detected_databases[db_name] = {"sources": [path], "confidence": "high"}

        for db_name, info in detected_databases.items():
            results.append(DetectionResult(
                category="database",
                name=db_name,
                confidence=info["confidence"],
                source_files=list(set(info["sources"]))[:5],
            ))

        return results
