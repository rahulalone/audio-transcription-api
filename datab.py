import databases
import sqlalchemy
DATABASE_URL = "postgresql+asyncpg://postgres:Roshan%40123@localhost:5432/postgres"

database = databases.Database(DATABASE_URL)
print(database)