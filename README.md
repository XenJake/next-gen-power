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
$secret = & .\.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
$content = (Get-Content .env -Raw) -replace '(?m)^DJANGO_SECRET_KEY=.*$', "DJANGO_SECRET_KEY=$secret"
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

Open http://127.0.0.1:8000/ for the website, http://127.0.0.1:8000/operations/ for the custom operations workspace, and http://127.0.0.1:8000/admin/ for the optional Django administration interface. The operations overview requires an active staff account with view permissions for charging stations, chargers, charging sessions and payments. Other sections appear when the account has the corresponding view permission; create and edit actions additionally require the model's add/change permission. Sessions and payments are read-only in the custom workspace for auditability.

`seed_demo_content` adds the six drop-shipped vehicle listings and seven Greater Accra charging venues: West Hills Mall, The Junction Mall, Accra Mall, Palace Mall Center, Community 25, Atlantic Mall and One Airport Square. It creates 10 illustrative 22 kW Type 2 AC charger records per venue. Each vehicle has a five-image gallery sourced from Wikimedia Commons; images are saved under `static/images/vehicles/` and gallery captions link to the source and applicable image license. Photos open in an in-page viewer. The charging locations and charger states are demonstrations, not deployment commitments or live availability; vehicle specifications and photos should be confirmed with the team. Listed vehicle prices are source prices in USD; the catalogue also displays indicative GHS estimates. Add confirmed host agreements, station assets and charger records through Django admin before representing any site as operational. Only published records appear publicly. Live availability requires a selected and implemented charger-controller adapter.

## Vehicle and home-charger orders

Vehicle detail pages let customers create a mock purchase order for a car alone or with a home charger. `/payments/chargers/` sells the Standard Home Charger (GHS 3,999) and Premium Home Charger (GHS 4,999) separately. Charger prices are hardware-only; installation is quoted separately. The labels do not imply a particular power rating or guaranteed compatibility. The vehicle-plus-charger package applies a 5% discount to the combined post-promotion total. Seasonal vehicle discounts are created and scheduled by staff in Django admin under **Seasonal deals**; no sale is active by default. Supplier-confirmed vehicle inclusions are maintained in each vehicle's **Included accessories** field and are not assumed when unconfirmed.

Vehicle GHS estimates use a fixed, configurable USD/GHS reference rate of 11.70343, sourced from the [ExchangeRate-API open USD endpoint](https://open.er-api.com/v6/latest/USD), last updated 11 November 2026 UTC. This is an indicative mid-market reference, not a Bank of Ghana rate or a customer quote. Set `USD_GHS_EXCHANGE_RATE` and `USD_GHS_RATE_AS_OF` in the environment to update the displayed reference; an order snapshots the converted amount and discount at creation. Recheck the rate and product prices before accepting real payments.

Vehicle and home-charger checkouts are mock-only: simulated success does not move money, reserve a vehicle, confirm supplier stock, create a delivery or installation booking, or mark charging equipment operational. The order record is available in Django admin under **Vehicle orders**. Do not treat it as a completed sale.

Each available charger has a QR code that opens its charger page. The customer enters a prepaid amount, then selects MTN Mobile Money, Telecel Cash, AT Money, Visa or Mastercard in the payment portal. Local development defaults to a mock provider: confirmation records a simulated success only, does not contact a payment network or charge money, and does not activate the charger. Replace the mock provider with a verified payment-provider adapter before accepting real payments; use `PAYMENT_PROVIDER_CLASS=disabled` to turn checkout off.

## Database configuration

By default, the application uses `db.sqlite3` in the project directory. To use PostgreSQL, set `DATABASE_URL` in the untracked local `.env`, for example:

```text
DATABASE_URL=postgresql://db_user:db_password@localhost:5432/next_gen_power
```

The PostgreSQL driver is included in `requirements.txt`. Keep database credentials and `.env` out of source control.

## Payments and charging authorization

The QR route is `/charging/chargers/<charger-public-uuid>/`. It creates a pending charging session and payment record. The application does not mark a charging payment as successful from a browser request: a configured payment-provider adapter must verify the provider's signed webhook. Charger authorization is a separate adapter step. Until both provider and charger-controller adapters are selected, checkout shows that live payment is unavailable and no charging session is authorized. Vehicle and home-charger orders currently use a separate mock-only flow; the charging QR and payment flow is unchanged.

Implement the provider adapter selected by `PAYMENT_PROVIDER_CLASS` with `create_checkout(payment, request)` and `verify_webhook(request)` methods. The verified webhook result must include `payment_id`, `status`, `amount`, `currency` and `reference`. Implement the charger adapter selected by `CHARGER_CONTROLLER_CLASS` with an `authorize(session)` method. Store credentials only in environment variables; never commit secrets or handle raw card data in this application. Mock payments are for local testing only and must not be used to accept real payments.

## Routes and API

- `/vehicles/` and `/vehicles/<slug>/`: vehicle catalogue, specifications and purchase enquiries
- `/payments/chargers/`: home charger catalogue and mock order form
- `/payments/orders/<uuid>/checkout/`: vehicle/home-charger mock order checkout
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
