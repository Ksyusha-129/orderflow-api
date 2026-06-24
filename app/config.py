import os

class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:secret@localhost:5432/orderflow"
    )

settings = Settings()