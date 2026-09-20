# OpenGroups

A small, self-hosted directory for groups. Feature it on any site, brand it with
environment variables, run it with Docker or plain Python.

## What it does

- Browse, fuzzy-search and filter groups by tag
- Admin panel (password protected) to create, edit, pin and tag groups
- Optional "important links" section
- SQLite by default, PostgreSQL in production
- All branding comes from environment variables — no code changes needed

## Quick start

### Docker

```bash
docker-compose up --build
# open http://localhost:8000
```

### Python

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export DBWARDEN_CONFIG_MODULE=database
dbwarden migrate --verbose
uvicorn main:app --reload --port 8000
```

## Configuration

| Variable          | Default              | Description                                   |
| ----------------- | -------------------- | --------------------------------------------- |
| `APP_NAME`        | `Groups`             | Application title shown in the header/tab     |
| `APP_DESCRIPTION` | `Directorio de grupos`| Meta description                             |
| `DISCLAIMER`      | _(empty)_            | Optional text for the first-visit modal       |
| `ADMIN_PASSWORD`  | `admin123` (dev)     | Required in production                        |
| `SECRET_KEY`      | random (dev)         | Signs admin tokens; required in production    |
| `LOG_LEVEL`       | `INFO`               | Python logging level                          |
| `ROOT_PATH`       | _(empty)_            | Set when serving under a subpath              |
| `DATABASE_URL`    | `sqlite:///./groups.db` | SQLite or PostgreSQL URL                  |
| `ENVIRONMENT`     | `DEV`                | Set to `PROD` to require production secrets   |
| `METRICS_API_KEY` | _(empty)_            | Enables optional usage metrics                |

## API

- `GET /api/groups` — list/search groups (`?q=`, `?tag=`)
- `POST /api/groups` — create (admin)
- `PUT /api/groups` / `DELETE /api/groups/{id}` — update/delete (admin)
- `GET /api/tags`, `POST /api/tags`, `DELETE /api/tags/{id}`
- `GET /api/important-links`, `POST` / `PUT` / `DELETE` (admin)
- `POST /api/admin/login`, `GET /api/admin/status`
- `GET /api/config` — branding for the frontend

## License

MIT — see [LICENSE](LICENSE).
