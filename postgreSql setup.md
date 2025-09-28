

- - -

## **1️⃣ Install PostgreSQL**

*   Download and install PostgreSQL from: [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
    
*   During installation, **note the password** you set for the `postgres` user (superuser).
    
*   Add PostgreSQL’s `bin` directory to your **system PATH** so that you can run `psql` from the terminal. For example:
    

makefile

```
C:\Program Files\PostgreSQL\16\bin
```

- - -

## **2️⃣ Open Command Prompt / Terminal**

Open a terminal (CMD, PowerShell, Git Bash, or MINGW64) and run:

bash


```
psql -U postgres
```

*   `-U postgres` → login as the superuser.
    
*   It will prompt for your PostgreSQL password. Enter the one you set during installation.
    

✅ You should see:

makefile

```
postgres=#
```

This means you’re in the PostgreSQL shell.

- - -

## **3️⃣ Create the Database**

Create the database for the Django project (as per your `settings.py`):

sql

```
CREATE DATABASE jdmrfinal;
```

Optional: check it exists:

sql
```
\l
For Quit
\q
```

- - -

## **4️⃣ Test Connection from Command Line**

bash

```
psql -U postgres -d jdmrfinal
```

*   `-d jdmrfinal` → connect to the specific database.
    
*   If it connects successfully, the database is ready.
    

- - -

## **5️⃣ Configure Django `settings.py`**

In your project’s `settings.py`, set:

python

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jdmrfinal',
        'USER': 'postgres',       # or your custom user
        'PASSWORD': 'Yash@2000', # or your password
        'HOST': 'localhost',
        'PORT': '5432',
    },
}
```

- - -

## **6️⃣ Run Django Migrations**

From your project root:

bash

```
python manage.py makemigrations
python manage.py migrate
```

*   This will create all tables in the `jdmrfinal` database.
    
*   If you get “relation does not exist” errors, check the **order of migrations** (some apps depend on others, like `students` before `batches`).
    

- - -

## **7️⃣ Verify the Tables**

You can check the tables via psql:

bash

```
psql -U postgres -d jdmrfinal
\dt
```

*   This lists all tables in the database.
    
*   Make sure tables like `accounts_user`, `teacher_makeappointment`, `students_unconfirmedstudentinst` exist.
    

- - -

## **8️⃣ Run the Development Server**

bash

```
python manage.py runserver
```

Now the project should work without table errors.

- - -

💡 **Tip:** Run `python manage.py showmigrations` to see migration status and ensure all tables exist.

- - -

If you want, I can also make a **super short copy-paste command list** for a new cloner that does all this quickly in order. Do you want me to make that?
