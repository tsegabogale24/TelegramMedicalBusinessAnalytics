import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


SQL = text(
    """
    UPDATE raw_analytics.fct_messages AS f
    SET product_name = w.canonical_name
    FROM raw_analytics.dim_drug_whitelist w
    WHERE f.product_name IS NULL OR f.product_name = ''
      AND f.message_text IS NOT NULL AND f.message_text <> ''
      AND lower(f.message_text) LIKE ('%' || lower(w.synonym) || '%')
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


