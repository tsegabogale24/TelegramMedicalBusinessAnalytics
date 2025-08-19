# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from .models import Message
from typing import List

def get_channel_activity(db: Session, channel_name: str):
    return (
        db.query(
            func.date_trunc('day', Message.message_date).label("date"),
            func.count()
        )
        .select_from(Message)
        .filter(Message.channel_name == channel_name)
        .group_by(func.date_trunc('day', Message.message_date))
        .order_by(func.date_trunc('day', Message.message_date))
        .all()
    )

def get_all_channels(db: Session):
    return [r[0] for r in db.query(Message.channel_name).distinct().order_by(Message.channel_name).all()]

def get_top_products(db: Session, limit: int = 10, strategy: str = "combined") -> List[str]:
    # Strategy options:
    # - 'whitelist': map text to canonical drug names via whitelist
    # - 'regex': regex-extract simple patterns (e.g., words ending with '-cin', '-mox', etc.)
    # - 'combined': union whitelist and regex results; fallback to frequent tokens if empty

    if strategy not in {"whitelist", "regex", "combined"}:
        strategy = "combined"

    stopwords_list = [
        'the','and','for','with','you','your','this','that','from','are','have','has','not','all','any','can','our','out','now','new','see','get','use','per','day','week','dose','qty','pack','pcs','buy','sale','offer','free','off','best','price','only','contact','call','pm','dm','tel','http','https','www','com'
    ]

    sql_whitelist = text(
        """
        SELECT w.canonical_name AS product_name, COUNT(*) AS count
        FROM raw_analytics.fct_messages f
        JOIN raw_analytics.dim_drug_whitelist w
          ON lower(f.message_text) LIKE ('%' || lower(w.synonym) || '%')
        WHERE f.message_text IS NOT NULL AND f.message_text <> ''
        GROUP BY w.canonical_name
        ORDER BY count DESC
        LIMIT :limit
        """
    )

    sql_regex = text(
        """
        WITH msgs AS (
            SELECT lower(message_text) AS message_text
            FROM raw_analytics.fct_messages
            WHERE message_text IS NOT NULL AND message_text <> ''
        ),
        matches AS (
            SELECT lower(m[1]) AS product_name
            FROM msgs, regexp_matches(message_text, '\\y([a-z0-9]{4,}cin)\\y', 'gi') AS m
            UNION ALL
            SELECT lower(m[1]) AS product_name
            FROM msgs, regexp_matches(message_text, '\\y([a-z0-9]{4,}mox)\\y', 'gi') AS m
            UNION ALL
            SELECT lower(m[1]) AS product_name
            FROM msgs, regexp_matches(message_text, '\\y([a-z0-9]{4,}zole)\\y', 'gi') AS m
        )
        SELECT product_name, COUNT(*) AS count
        FROM matches
        WHERE product_name IS NOT NULL AND product_name <> ''
        GROUP BY product_name
        ORDER BY count DESC
        LIMIT :limit
        """
    )

    sql_tokens = text(
        """
        WITH msgs AS (
            SELECT lower(message_text) AS message_text
            FROM raw_analytics.fct_messages
            WHERE message_text IS NOT NULL AND message_text <> ''
        ),
        tokens AS (
            SELECT regexp_split_to_table(message_text, '[^a-z0-9]+') AS token
            FROM msgs
        ),
        filtered AS (
            SELECT token AS product_name
            FROM tokens
            WHERE length(token) >= 3
              AND token ~ '[a-z]'
              AND NOT (token = ANY(:stopwords))
        )
        SELECT product_name, COUNT(*) AS count
        FROM filtered
        GROUP BY product_name
        ORDER BY count DESC
        LIMIT :limit
        """
    )

    results: List[tuple] = []

    if strategy in {"whitelist", "combined"}:
        results = db.execute(sql_whitelist, {"limit": limit}).fetchall()
    if (strategy == "whitelist" and not results) or strategy in {"regex", "combined"}:
        regs = db.execute(sql_regex, {"limit": limit}).fetchall()
        if strategy == "regex":
            results = regs
        else:
            # merge
            results = list(results) + list(regs)
    if not results:
        results = db.execute(sql_tokens, {"limit": limit, "stopwords": stopwords_list}).fetchall()

    # aggregate duplicates if combined
    agg = {}
    for name, count in results:
        if not name:
            continue
        agg[name] = agg.get(name, 0) + int(count)
    top = sorted(agg.items(), key=lambda x: x[1], reverse=True)[:limit]
    return [{"product_name": n, "count": c} for n, c in top]

def search_messages(db: Session, query: str):
    return (
        db.query(Message)
        .filter(Message.message_text.ilike(f"%{query}%"))
        .limit(100)
        .all()
    )
