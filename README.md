# OpenGroups

A small, self-hosted directory of groups. Feature it on any site, brand it with
environment variables, run it with Docker or plain Python.

- Browse, fuzzy-search and filter groups by tag
- Admin panel (password protected) to create, edit, pin and tag groups
- Optional "important links" section
- SQLite by default, PostgreSQL in production
- All branding comes from environment variables; no code changes needed

## Quick start

### Docker

```bash
docker compose up --build
# open http://localhost:8000
```

### Python

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

export DBWARDEN_CONFIG_MODULE=database PYTHONPATH=.
dbwarden migrate        # create the SQLite schema
uvicorn main:app --reload --port 8000
```

## Development

A `Makefile` wraps the common tasks:

```bash
make setup     # create venv + install dev dependencies
make dev       # run with autoreload on http://localhost:8000
make test      # pytest
make lint      # ruff check + format check
make format    # ruff --fix + ruff format
make migrate   # apply dbwarden migrations
make docker    # docker compose up --build
make clean     # remove venv, caches and groups.db
```

### Tests

The suite (`tests/`) spins up the real FastAPI app against a temporary SQLite
database and covers group CRUD, tags, fuzzy search, admin auth/lockout, URL
validation and important links.

```bash
make test      # or: pytest
```

### Linting and formatting

[Ruff](https://docs.astral.sh/ruff/) handles both, configured in
`pyproject.toml`:

```bash
make lint
make format
```

## Configuration

| Variable             | Default                   | Description                                        |
| -------------------- | ------------------------- | -------------------------------------------------- |
| `APP_NAME`           | `Groups`                  | Application title shown in the header/tab          |
| `APP_DESCRIPTION`    | `Directorio de grupos`    | Meta description                                   |
| `DISCLAIMER`         | _(empty)_                 | Optional text for the first-visit modal            |
| `ADMIN_PASSWORD`     | `admin123` (dev)          | Required in production                             |
| `SECRET_KEY`         | random (dev)              | Signs admin tokens; required in production         |
| `LOG_LEVEL`          | `INFO`                    | Python logging level                               |
| `PORT`               | `8080`                    | Port used by the container                         |
| `ROOT_PATH`          | _(empty)_                 | Set when serving under a subpath                   |
| `DATABASE_URL`       | `sqlite:///./groups.db`   | SQLite (plain or async URL) or PostgreSQL URL      |
| `ENVIRONMENT`        | `DEV`                     | Set to `PROD` to require production secrets        |
| `METRICS_API_KEY`    | _(empty)_                 | Enables optional usage metrics                     |
| `METRICS_EVENTS_URL` | `https://api.eclipselabs.com.uy/metrics/event` | Metrics events endpoint |
| `METRICS_VIEWS_URL`  | `https://api.eclipselabs.com.uy/metrics/views` | Metrics views endpoint  |

See `.env.example` for a copy-paste starting point.

## Database and migrations

The schema is generated from the SQLAlchemy models with
[dbwarden](https://docs.dbwarden.org/). The models live in `database.py`; the
base migration is `migrations/primary__0001_initial_schema.sql`. Tags ship
empty; they are created from the admin UI and saved to the database.

```bash
export DBWARDEN_CONFIG_MODULE=database PYTHONPATH=.
dbwarden make-migrations "describe your change"   # after editing models
dbwarden migrate                                   # apply pending migrations
```

## API

- `GET /healthz`: health probe
- `GET /api/groups`: list/search groups (`?q=`, `?tag=`)
- `POST /api/groups`: create (admin)
- `PUT /api/groups` / `DELETE /api/groups/{id}`: update/delete (admin)
- `GET /api/tags`, `POST /api/tags`, `DELETE /api/tags/{id}` (admin for writes)
- `POST /api/groups/{id}/tags`, `DELETE /api/groups/{id}/tags/{tag_id}` (admin)
- `GET /api/important-links`, `POST` / `PUT` / `DELETE` (admin)
- `POST /api/admin/login`, `GET /api/admin/status`
- `GET /api/config`: branding for the frontend

Interactive API docs are served at `/docs` outside of `PROD`.

## Project layout

```
main.py        FastAPI app: routes, auth, fuzzy search
database.py    SQLAlchemy models + dbwarden configuration
migrations/    dbwarden-generated SQL migrations
static/        Vue 3 (CDN) frontend: index.html (public) + admin.html
tests/         pytest suite
```

## License

MIT; see [LICENSE](LICENSE).
