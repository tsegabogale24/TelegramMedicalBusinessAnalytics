## Development

### Requirements
- Python 3.11
- PostgreSQL

### Environment
Create `.env` with:
```
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/dbname
```

### Setup
```
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Prepare DB (dev)
alembic upgrade head
python database/alter_fct_messages_add_cols.py
python database/setup_drug_whitelist.py

# Run API
uvicorn api.main:app --reload
```

### Tests
```
pytest -q
```

## CI
GitHub Actions `.github/workflows/ci.yml` runs:
- Postgres service
- Alembic migrations + alter scripts
- Seed whitelist
- Ruff lint
- Pytest against live API


