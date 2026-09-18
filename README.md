# Family Planning FastAPI + MySQL Project

A complete SQLAlchemy 2.x / FastAPI API for the `family_planning_fp` MySQL database.

## Included

- 20 SQLAlchemy model classes matching the MySQL schema
- Pydantic v2 Create / Update / Read schemas for every table
- Generic SQLAlchemy CRUD service layer
- REST CRUD routers for all 20 tables
- Pagination (`offset`, `limit`) on list endpoints
- Useful clinical aggregate endpoints
- MySQL health check
- `.env` configuration
- Dockerfile + Docker Compose
- Original MySQL database dump including synthetic data
- Basic mapper/schema tests

## Project structure

```text
family_planning_api/
├── app/
│   ├── main.py
│   ├── settings.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── exceptions.py
│   ├── crud/
│   │   ├── __init__.py
│   │   └── base.py
│   └── routers/
│       ├── __init__.py
│       ├── clinical.py
│       └── <one router per database table>.py
├── database/
│   └── family_planning_fp_mysql.sql
├── scripts/
│   ├── create_tables.py
│   └── import_db.sh
├── tests/
├── requirements.txt
├── .env.example
├── Dockerfile
└── docker-compose.yml
```

## Option 1: Run with your existing MySQL server

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
#link https://developers.facebook.com/apps/961273237022140/use_cases/customize/wa-settings/?use_case_enum=WHATSAPP_BUSINESS_MESSAGING&product_route=whatsapp-business&business_id=1608810040642467&selected_tab=wa-settings

### 2. Import the database (skip this if already imported)

```bash
mysql -u root -p < database/family_planning_fp_mysql.sql
```

or:

```bash
./scripts/import_db.sh
```

### 3. Configure credentials

```bash
cp .env .env
```

Edit `.env`:

```dotenv
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=family_planning_fp
```

### 4. Start FastAPI

```bash
uvicorn app.main:app --reload

python build_vector_db.py
```


```bash
## Expose the server to the public
ngrok http 8000
```

Open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health: http://127.0.0.1:8000/health

- https://developers.facebook.com/apps/961273237022140/use_cases/customize/wa-dev-console/?use_case_enum=WHATSAPP_BUSINESS_MESSAGING&product_route=whatsapp-business&business_id=1608810040642467&selected_tab=wa-dev-console
- https://developers.facebook.com/apps/1104039355981930/whatsapp-business/api-testing-v2/?business_id=2273437143196944

## Option 2: Run everything with Docker

```bash
docker compose up --build
```

Then open http://127.0.0.1:8000/docs.

> The SQL dump is mounted into MySQL's initialization directory. It is imported only when the Docker MySQL volume is first created. To rebuild the DB from scratch, use `docker compose down -v` before starting again.

## REST resources

All resource routes are under `/api/v1`

| Resource | Operations | Primary key |
|---|---|---|
| `counties` | GET list, GET one, POST, PATCH, DELETE | `county_id` |
| `education-levels` | GET list, GET one, POST, PATCH, DELETE | `education_level_id` |
| `marital-statuses` | GET list, GET one, POST, PATCH, DELETE | `marital_status_id` |
| `discontinuation-reasons` | GET list, GET one, POST, PATCH, DELETE | `discontinuation_reason_id` |
| `fp-methods` | GET list, GET one, POST, PATCH, DELETE | `method_id` |
| `database-metadata` | GET list, GET one, POST, PATCH, DELETE | `key` |
| `subcounties` | GET list, GET one, POST, PATCH, DELETE | `subcounty_id` |
| `facilities` | GET list, GET one, POST, PATCH, DELETE | `facility_id` |
| `clients` | GET list, GET one, POST, PATCH, DELETE | `client_id` |
| `encounters` | GET list, GET one, POST, PATCH, DELETE | `encounter_id` |
| `counselling-sessions` | GET list, GET one, POST, PATCH, DELETE | `counselling_session_id` |
| `reproductive-history` | GET list, GET one, POST, PATCH, DELETE | `reproductive_history_id` |
| `fp-method-advantages` | GET list, GET one, POST, PATCH, DELETE | `advantage_id` |
| `fp-method-cautions` | GET list, GET one, POST, PATCH, DELETE | `caution_id` |
| `fp-method-side-effects` | GET list, GET one, POST, PATCH, DELETE | `side_effect_id` |
| `fp-method-use-instructions` | GET list, GET one, POST, PATCH, DELETE | `instruction_id` |
| `fp-usage-episodes` | GET list, GET one, POST, PATCH, DELETE | `episode_id` |
| `fp-dispensing` | GET list, GET one, POST, PATCH, DELETE | `dispensing_id` |
| `followups` | GET list, GET one, POST, PATCH, DELETE | `followup_id` |
| `side-effect-reports` | GET list, GET one, POST, PATCH, DELETE | `report_id` |

Example:

```http
GET /api/v1/clients?offset=0&limit=100
GET /api/v1/clients/1
POST /api/v1/clients
PATCH /api/v1/clients/1
DELETE /api/v1/clients/1
```

## Additional useful endpoints

```http
GET /api/v1/clients/by-uid/FP000001
GET /api/v1/clients/1/timeline
GET /api/v1/fp-methods/5/details
```

The FP method detail endpoint returns the method together with its advantages, cautions, side effects and use instructions.

The client timeline endpoint returns the client plus reproductive history, encounters, method-use episodes, dispensing records, follow-ups and side-effect reports.

## Example create-client request

```json
{
  "client_uid": "FP-DEMO-1001",
  "facility_id": 1,
  "date_of_birth": "1995-05-12",
  "registration_date": "2026-08-31",
  "education_level_id": 3,
  "marital_status_id": 1,
  "residence_type": "Urban",
  "occupation_category": "Self-employed",
  "disability_status": "None reported",
  "consent_for_followup": true,
  "synthetic_record": true
}
```

## Database changes

This project assumes the provided MySQL dump is the source of truth. `scripts/create_tables.py` can create the tables from SQLAlchemy models in a blank database, but it does not load seed/synthetic data. For the complete dataset, import `database/family_planning_fp_mysql.sql`.

## Tests

```bash
pytest -q
```

## Important clinical note

The included dataset is synthetic/demo data. The FP clinical descriptions in the database should be validated against the current national clinical guidance before being used to support real-world clinical decisions.
