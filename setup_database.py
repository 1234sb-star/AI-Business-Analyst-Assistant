from src.database import initialize_database, DB_PATH

initialize_database()
print(f"Database ready: {DB_PATH}")
