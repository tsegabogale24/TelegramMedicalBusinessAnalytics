import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


SEED_DATA = {
    "paracetamol": ["paracetamol", "acetaminophen", "panadol"],
    "ibuprofen": ["ibuprofen", "advil", "nurofen"],
    "amoxicillin": ["amoxicillin", "amoxil"],
    "vitamin c": ["vitamin c", "ascorbic acid", "ascorbic"],
    "metformin": ["metformin", "glucophage"],
    "omeprazole": ["omeprazole", "prilosec"],
    "azithromycin": ["azithromycin", "zithromax"],
    "doxycycline": ["doxycycline"],
    "diclofenac": ["diclofenac", "voltaren"],
}


def main() -> None:
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL not set")
    engine = create_engine(url)

    ddl = text(
        """
        CREATE TABLE IF NOT EXISTS raw_analytics.dim_drug_whitelist (
            canonical_name TEXT NOT NULL,
            synonym TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS ix_drug_whitelist_syn ON raw_analytics.dim_drug_whitelist (synonym);
        """
    )

    with engine.begin() as conn:
        conn.execute(ddl)
        # upsert-like: delete existing rows for canonical to avoid duplicates, then insert
        for canonical, synonyms in SEED_DATA.items():
            conn.execute(text("DELETE FROM raw_analytics.dim_drug_whitelist WHERE canonical_name = :c"), {"c": canonical})
            for syn in synonyms:
                conn.execute(
                    text(
                        "INSERT INTO raw_analytics.dim_drug_whitelist (canonical_name, synonym) VALUES (:c, :s)"
                    ),
                    {"c": canonical, "s": syn},
                )

    print("Whitelist table ensured and seeded.")


if __name__ == "__main__":
    main()


