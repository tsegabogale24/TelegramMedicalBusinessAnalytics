import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


SQL = text(
    """
    UPDATE raw_analytics.fct_messages AS fm
    SET message_text = src.message_text
    FROM (
        SELECT
            id::BIGINT AS message_id,
            CASE
                WHEN jsonb_typeof(raw_json->'text') = 'string' THEN raw_json->>'text'
                WHEN jsonb_typeof(raw_json->'text') = 'array' THEN (
                    SELECT string_agg(
                        CASE
                            WHEN jsonb_typeof(elem) = 'string' THEN trim(both '"' from elem::text)
                            WHEN jsonb_typeof(elem) = 'object' THEN coalesce(elem->>'text', '')
                            ELSE ''
                        END,
                        ''
                    )
                    FROM jsonb_array_elements(raw_json->'text') AS elem
                )
                WHEN raw_json ? 'message' THEN raw_json->>'message'
                WHEN raw_json ? 'caption' THEN raw_json->>'caption'
                ELSE NULL
            END AS message_text
        FROM raw.telegram_messages
    ) AS src
    WHERE fm.message_id = src.message_id
      AND (fm.message_text IS NULL OR fm.message_text = '')
    """
)


def main() -> None:
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL not set")
    engine = create_engine(url)
    with engine.begin() as conn:
        result = conn.execute(SQL)
        try:
            print("rows updated:", result.rowcount)
        except Exception:
            print("rows updated: unknown")


if __name__ == "__main__":
    main()


