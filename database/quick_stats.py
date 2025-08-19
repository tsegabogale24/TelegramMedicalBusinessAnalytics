import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def main() -> None:
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    if not url:
        raise SystemExit("DATABASE_URL not set")
    engine = create_engine(url)
    with engine.connect() as conn:
        total = conn.execute(text("select count(*) from raw_analytics.fct_messages")).scalar()
        with_text = conn.execute(text("select count(*) from raw_analytics.fct_messages where message_text is not null and message_text <> ''")).scalar()
        like_med = conn.execute(text("select count(*) from raw_analytics.fct_messages where message_text ilike '%medicine%'")).scalar()
        print({"total": total, "with_text": with_text, "like_medicine": like_med})
        sample = conn.execute(text("select message_id, left(message_text, 120) as snippet from raw_analytics.fct_messages where message_text is not null and message_text <> '' order by message_id desc limit 5")).fetchall()
        print("sample:", sample)
        # top detections (if available)
        try:
            det = conn.execute(text("select detected_object_class, count(*) as c from raw.fct_image_detections group by 1 order by c desc limit 10")).fetchall()
            print("detections:", det)
        except Exception as e:
            print("detections error:", e)


if __name__ == "__main__":
    main()


