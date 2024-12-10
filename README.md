Creat virtual enviornment: `python3 -m venv my-venv`

Activate virtua environment: `source venv my-venv/bin/activate`

Install requirements `pip install -r requirements.txt`

Create database: `createdb demodb` (assumes postgres is already installed)

Migrate database:`python manage.py migrate`

Run test script: `python manage.py demo`