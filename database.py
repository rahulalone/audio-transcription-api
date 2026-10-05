import databases
import sqlalchemy

# PostgreSQL connection URL
DATABASE_URL = "postgresql+asyncpg://postgres:Roshan%40123@localhost:5432/postgres"

# Async database instance
database = databases.Database(DATABASE_URL)

# SQLAlchemy table definition
metadata = sqlalchemy.MetaData()

logs = sqlalchemy.Table(
    "transcription_logs",
    metadata,
    sqlalchemy.Column("id",                  sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("file_name",           sqlalchemy.String,  nullable=True),
    sqlalchemy.Column("file_size_kb",        sqlalchemy.Float,   nullable=True),
    sqlalchemy.Column("transcription",       sqlalchemy.Text,    nullable=True),
    sqlalchemy.Column("word_count",          sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("language",            sqlalchemy.String,  nullable=True),
    sqlalchemy.Column("audio_duration_sec",  sqlalchemy.Float,   nullable=True),
    sqlalchemy.Column("processing_time_sec", sqlalchemy.Float,   nullable=True),
    sqlalchemy.Column("client_ip",           sqlalchemy.String,  nullable=True),
    sqlalchemy.Column("status",              sqlalchemy.String,  nullable=True),
    sqlalchemy.Column("error_message",       sqlalchemy.Text,    nullable=True),
    sqlalchemy.Column("created_at",          sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
)

# Create engine (sync) to create tables on startup
engine = sqlalchemy.create_engine(
    "postgresql://postgres:Roshan%40123@localhost:5432/postgres"
)

def create_tables():
    metadata.create_all(engine)
