# databaes-backend 

## Development setup (Mac OS) 

0. Clone the repo and `cd` into `databaes-backend`
```Shell
git clone https://github.com/sardinachanx/326-final-project
cd 326-final project/databaes-backend
```

1. Set up a Python 3 virtual environment
```Shell
python3 -m venv .env
source .env/bin/activate
```

2. Install dependencies
```Shell
pip install -r requirements.txt
```

3. Install & start PostgreSQL
```Shell
brew install postgresql
brew services start postgresql
psql
```

4. Create new database and user, and grant all database privileges to user
```Shell
psql > CREATE DATABASE db_name;
psql > CREATE USER db_user WITH ENCRYPTED PASSWORD db_pass;
psql > GRANT ALL PRIVILEGES ON DATABASE db_name TO db_user;
```

5. Add the following to your `.bash_profile` or `.bashrc`:
- `DB_NAME`: Name of database created in Step 4 (`db_name`)
- `DB_USER`: Username of new user created in Step 4 (`db_user`)
- `DB_PASS`: Password of new user created in Step 4 (`db_pass`)

6. Run initial migration and launch server
```Shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
``` 

7. Navigate to http://localhost:8000/api/v1. You should see a list of all available API endpoints. 

To view the admin panel, first create a superuser:
```Shell
python manage.py createsuperuser
``` 

Now you should be able to log into and view the admin panel at http://localhost:8000/admin after starting the server. 

### API Spec
