# databaes-backend 

## Development setup 

0. Clone the repo and `cd` into `databaes-backend`
```
git clone https://github.com/sardinachanx/326-final-project
cd 326-final project/databaes-backend
```

1. Set up a Python 3 virtual environment
```
python3 -m venv .env
source .env/bin/activate
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Install PostgreSQL

4. Create new database and user, and grant all database privileges to user

5. Create environment variables (Windows) or add the following to `.bash_profile`:
- DB_NAME: Name of database created in Step 4
- DB_USER: Username of new user created in Step 4 (with database privileges)
- DB_PASS: Password of new user created in Step 4 (with database privileges) 

6. Run initial migration and launch server
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
``` 

7. Navigate to https://localhost:8000/api/v1. You should see a list of all available API endpoints. 

To view the admin panel, first create a superuser:
``` 
python manage.py createsuperuser
``` 

Now you should be able to log into and view the admin panel at https://localhost:8000/admin after starting the server. 

### API Spec
