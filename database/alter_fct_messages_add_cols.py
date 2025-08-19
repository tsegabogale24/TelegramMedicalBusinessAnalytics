import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def main() -> None:
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")

    engine = create_engine(database_url)

    alter_sql = [
        "ALTER TABLE raw_analytics.fct_messages ADD COLUMN IF NOT EXISTS message_text TEXT",
        "ALTER TABLE raw_analytics.fct_messages ADD COLUMN IF NOT EXISTS product_name VARCHAR",
    ]

    backfill_sql = text(
        """
        UPDATE raw_analytics.fct_messages AS fm
        SET message_text = src.message_text
        FROM (
            SELECT id::BIGINT AS message_id, (raw_json->>'text') AS message_text
            FROM raw.telegram_messages
        ) AS src
        WHERE fm.message_id = src.message_id
          AND fm.message_text IS NULL
        """
    )

    with engine.begin() as conn:
        for stmt in alter_sql:
            conn.execute(text(stmt))
        result = conn.execute(backfill_sql)
        try:
            updated = result.rowcount  # type: ignore[attr-defined]
        except Exception:
            updated = None

    print("Altered fct_messages (added columns if missing)")
    if updated is not None:
        print(f"Backfilled message_text rows: {updated}")
    else:
        print("Backfill completed (rowcount unavailable)")


if __name__ == "__main__":
    main()


