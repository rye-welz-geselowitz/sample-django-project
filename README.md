Creat virtual enviornment: `python3 -m venv my-venv`

Activate virtua environment: `source my-venv/bin/activate`

Install requirements `pip install -r requirements.txt`

Create database: `createdb demodb` (assumes postgres is already installed)

Migrate database:`python manage.py migrate`

Run script: `python manage.py demo` OR `python manage.py optimize_me`



# Tips for efficient ORM usage
* Minimize trips to the database
* Use database indexes
* Use database aggregate functions
