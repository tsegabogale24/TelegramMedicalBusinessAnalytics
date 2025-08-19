import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


KEYWORDS = {
    'paracetamol': ['paracetamol', 'acetaminophen', 'panadol'],
    'ibuprofen': ['ibuprofen', 'advil', 'nurofen'],
    'amoxicillin': ['amoxicillin', 'amoxil'],
    'vitamin_c': ['vitamin c', 'ascorbic'],
}


def build_case_expression() -> str:
    branches = []
    for product, terms in KEYWORDS.items():
        ors_parts = []
        for t in terms:
            sanitized = t.replace("'", "''")
            ors_parts.append("message_text ILIKE '%{}%'".format(sanitized))
        ors = " OR ".join(ors_parts)
        branches.append(f"WHEN {ors} THEN '{product}'")
    return " CASE " + " ".join(branches) + " ELSE NULL END "


def main() -> None:
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL not set")
    engine = create_engine(url)

    case_expr = build_case_expression()
    sql = text(
        f"""
        UPDATE raw_analytics.fct_messages
        SET product_name = {case_expr}
        WHERE (product_name IS NULL OR product_name = '')
        """
    )

    with engine.begin() as conn:
        result = conn.execute(sql)
        try:
            print("rows updated:", result.rowcount)
        except Exception:
            print("rows updated: unknown")


if __name__ == "__main__":
    main()


