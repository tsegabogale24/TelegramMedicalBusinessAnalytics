import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def main() -> None:
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL not set")
    engine = create_engine(url)
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_fct_messages_text_trgm ON raw_analytics.fct_messages USING gin (lower(message_text) gin_trgm_ops)"))
    print("pg_trgm index ensured")


if __name__ == "__main__":
    main()


