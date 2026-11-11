# NEXT GEN POWER

NEXT GEN POWER is a Django application for a Ghanaian electric vehicle dealership and charging infrastructure operator. The project includes server-rendered public pages, database-backed vehicle and charging records, staff operations, and payment/charger adapter integration points.

## Requirements

- Python 3.12 or newer (the project has been set up and checked with Python 3.14)
- Git (optional, for version control)
- PostgreSQL only when using a non-SQLite database

## Local setup on Windows PowerShell

From the project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Generate a local secret and place it in `.env` without committing that file:

```powershell
$secret = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
$content = (Get-Content .env -Raw) -replace '(?m)^DJANGO_SECRET_KEY=$', "DJANGO_SECRET_KEY=$secret"
[System.IO.File]::WriteAllText((Resolve-Path .env), $content, [System.Text.UTF8Encoding]::new($false))
```

Create the database tables and an administrative account:

```powershell
python manage.py migrate
python manage.py seed_demo_content
python manage.py createsuperuser
python manage.py runserver
```

Run the application test suite with:

```powershell
python manage.py test
```

Open http://127.0.0.1:8000/ for the website, http://127.0.0.1:8000/admin/ for Django administration, and http://127.0.0.1:8000/operations/ for the staff operations overview. Grant the staff account the `charging | charging session | Can view charging session` permission to use the operations overview.

`seed_demo_content` adds three clearly labeled BYD examples, five long-dwell host venues (Accra Mall, West Hills Mall, Atlantic Mall, Labadi Beach Hotel and One Airport Square) with 10 x 22 kW Type 2 AC chargers each, and five 88 kW CCS2 DC chargers split 3 near Suhum and 2 near Winneba. These are illustrative host-site locations and charger states, not deployment commitments or live availability. Vehicle prices/specifications/photos and station coordinates are demonstrations, not quotations or proof of inventory/equipment. Add confirmed vehicles, host agreements, station assets and charger records through Django admin before representing any site as operational. Only published records appear publicly. Live availability requires a selected and implemented charger-controller adapter.

## Database configuration

By default, the application uses `db.sqlite3` in the project directory. To use PostgreSQL, set `DATABASE_URL` in the untracked local `.env`, for example:

```text
DATABASE_URL=postgresql://db_user:db_password@localhost:5432/next_gen_power
```

The PostgreSQL driver is included in `requirements.txt`. Keep database credentials and `.env` out of source control.

## Payments and charging authorization

The QR route is `/charging/chargers/<charger-public-uuid>/`. It creates a pending charging session and payment record. The application does not mark a payment as successful from a browser request: a configured payment-provider adapter must verify the provider's signed webhook. Charger authorization is a separate adapter step. Until both provider and charger-controller adapters are selected, checkout shows that live payment is unavailable and no charging session is authorized.

Implement the provider adapter selected by `PAYMENT_PROVIDER_CLASS` with `create_checkout(payment, request)` and `verify_webhook(request)` methods. The verified webhook result must include `payment_id`, `status`, `amount`, `currency` and `reference`. Implement the charger adapter selected by `CHARGER_CONTROLLER_CLASS` with an `authorize(session)` method. Store credentials only in environment variables; never commit secrets or handle raw card data in this application.

## Routes and API

- `/vehicles/` and `/vehicles/<slug>/`: vehicle catalogue, specifications and purchase enquiries
- `/charging/` and `/charging/stations/<slug>/`: station locator and charger details
- `/charging/how-it-works/`: QR charging and payment explainer
- `/charging/chargers/<uuid>/`: QR-based charger landing and prepaid session start
- `/charging/chargers/<uuid>/qr.svg`: generated printable SVG QR label for a published charger
- `/charging/api/v1/stations/`: read-only station availability data
- `/charging/api/v1/chargers/<uuid>/`: read-only charger status
- `/accounts/login/`: Django authentication
- `/operations/`: staff dashboard (requires staff status and charging-session view permission)
- `/admin/`: Django admin, restricted to authenticated staff users

Static assets are in `static/`, Django templates are in `templates/` and uploaded vehicle images are stored under `media/` in development. The original static Aurelle pages and assets are retained intact in `legacy/static-prototype/` as migration reference; Django routes serve the active application.

## Production checklist

Set `DEBUG=False`, a unique secret, production `ALLOWED_HOSTS`, PostgreSQL credentials, HTTPS, email configuration and provider/controller adapters. Run `python manage.py check --deploy`, apply migrations and collect static files with `python manage.py collectstatic`. Configure durable media storage and backups before accepting real enquiries or operating charging sites.
