# Django Political System Prototype  
## Installation and Project Requirements

This document explains how to install, configure, and run the Django Political System Prototype.

The prototype presents a public-facing government portal before revealing the decision institutions, influence networks, implementation bodies, policies, and feedback relationships operating behind it.

---

# 1. System Requirements

Install the following software before running the project:

- Python 3.11 or later
- Git
- Visual Studio Code or another code editor
- A modern web browser
- `pip`, which is normally installed with Python

Check your Python installation:

```bash
python --version
```

On some macOS or Linux systems, use:

```bash
python3 --version
```

Check that Git is installed:

```bash
git --version
```

Check that `pip` is installed:

```bash
pip --version
```

On some systems, use:

```bash
python -m pip --version
```

---

# 2. Downloading the Project

## Option A: Clone the GitHub repository

Open Terminal, Command Prompt, PowerShell, or the Visual Studio Code terminal.

Run:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the actual repository address.

Example:

```bash
git clone https://github.com/your-username/django-political-system-prototype.git
```

Enter the project folder:

```bash
cd django-political-system-prototype
```

## Option B: Download the ZIP file

1. Open the GitHub repository.
2. Select **Code**.
3. Select **Download ZIP**.
4. Extract the downloaded ZIP file.
5. Open the extracted folder in Visual Studio Code.

The folder you open should contain:

```text
manage.py
country/
civilization/
requirements.txt
```

---

# 3. Opening the Project in Visual Studio Code

Open Visual Studio Code.

Select:

```text
File → Open Folder
```

Open the main project folder containing `manage.py`.

Do not open only the `country` folder. The complete Django project folder must be opened.

Open the Visual Studio Code terminal by selecting:

```text
Terminal → New Terminal
```

---

# 4. Creating a Virtual Environment

A virtual environment keeps the project dependencies separate from other Python projects.

Create a virtual environment:

```bash
python -m venv .venv
```

On systems that use `python3`, run:

```bash
python3 -m venv .venv
```

## Activate the virtual environment on macOS or Linux

```bash
source .venv/bin/activate
```

## Activate the virtual environment on Windows Command Prompt

```cmd
.venv\Scripts\activate
```

## Activate the virtual environment on Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

After activation, the terminal should display something similar to:

```text
(.venv)
```

To deactivate the virtual environment later, run:

```bash
deactivate
```

---

# 5. Installing Python Packages

The project dependencies are stored in:

```text
requirements.txt
```

Install them by running:

```bash
pip install -r requirements.txt
```

On some systems, use:

```bash
python -m pip install -r requirements.txt
```

The project requires packages including:

```text
Django
python-dotenv
```

A basic `requirements.txt` may contain:

```text
Django
python-dotenv
```

The actual file may include specific version numbers, such as:

```text
Django==5.2.5
python-dotenv==1.1.1
```

To create or update `requirements.txt` from the current virtual environment, run:

```bash
pip freeze > requirements.txt
```

Do not use `REQUIREMENTS.md` with `pip`. This Markdown file explains installation, while `requirements.txt` contains installable Python packages.

---

# 6. Configuring the Django Secret Key

Django requires a `SECRET_KEY` before the application can start.

The real secret key must not be written directly in `settings.py` or uploaded to GitHub.

## 6.1 Generate a new secret key

Run:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated value.

It will look similar to:

```text
example-only-secret-key-generated-by-django
```

Do not use the example value shown above.

## 6.2 Create the `.env` file

Create a file named:

```text
.env
```

Place it in the main project folder beside `manage.py`.

The structure should look like:

```text
django-political-system-prototype/
├── .env
├── manage.py
├── country/
└── civilization/
```

Inside `.env`, add:

```env
DJANGO_SECRET_KEY=paste-your-generated-secret-key-here
```

Example structure:

```env
DJANGO_SECRET_KEY=your-real-generated-key
DJANGO_DEBUG=True
```

Do not add spaces around the equals sign.

Correct:

```env
DJANGO_SECRET_KEY=your-secret-key
```

Incorrect:

```env
DJANGO_SECRET_KEY = your-secret-key
```

---

# 7. Environment Example File

The GitHub repository should include:

```text
.env.example
```

This file shows users which environment variables are required without exposing the real values.

Add the following to `.env.example`:

```env
DJANGO_SECRET_KEY=replace-with-your-own-generated-secret-key
DJANGO_DEBUG=True
```

A user downloading the project should copy `.env.example` to `.env` and replace the example secret key.

On macOS or Linux:

```bash
cp .env.example .env
```

On Windows Command Prompt:

```cmd
copy .env.example .env
```

The user must then generate a real key and place it inside `.env`.

---

# 8. Loading Environment Variables in Django

The project uses `python-dotenv` to load values from `.env`.

The beginning of `civilization/settings.py` should contain:

```python
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
```

For the debug setting, use:

```python
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"
```

The complete section may look like:

```python
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = []
```

If the environment variable is missing, Django may display:

```text
KeyError: 'DJANGO_SECRET_KEY'
```

Check that:

- `.env` is beside `manage.py`;
- the variable is named exactly `DJANGO_SECRET_KEY`;
- `load_dotenv(BASE_DIR / ".env")` appears before `SECRET_KEY`;
- `python-dotenv` is installed;
- the virtual environment is activated.

---

# 9. Protecting the Secret Key

The `.gitignore` file must prevent `.env` from being uploaded to GitHub.

Create or update:

```text
.gitignore
```

Add:

```gitignore
# Environment variables and secrets
.env
.env.*
!.env.example

# Python cache
__pycache__/
*.py[cod]
*.pyo

# Virtual environments
.venv/
venv/
env/

# Django local files
db.sqlite3
staticfiles/
media/

# Operating system files
.DS_Store
Thumbs.db

# Visual Studio Code settings
.vscode/
```

The line:

```gitignore
!.env.example
```

allows `.env.example` to be uploaded while keeping the real `.env` private.

Do not upload:

- `.env`;
- real Django secret keys;
- API keys;
- access tokens;
- email passwords;
- database passwords.

If a real key is accidentally uploaded publicly, generate a new key and replace the exposed one.

---

# 10. Checking the Project Configuration

After creating `.env`, run:

```bash
python manage.py check
```

A successful result should resemble:

```text
System check identified no issues.
```

If the command reports an error, read the error message and check:

- the secret key;
- installed packages;
- database configuration;
- application names in `INSTALLED_APPS`;
- template paths;
- URL configuration.

---

# 11. Preparing the Database

The project uses Django migrations to create the required database tables.

Run:

```bash
python manage.py makemigrations
```

Then run:

```bash
python manage.py migrate
```

These commands create the tables for:

- countries;
- institutions;
- policies;
- influence relationships;
- Django administration;
- authentication;
- sessions.

Migration files inside the application should be uploaded to GitHub.

Do not add the migrations folder to `.gitignore`.

---

# 12. Loading the Comparative Political Data

The project includes a custom Django management command that creates the country cases, institutions, policies, and influence relationships.

Run:

```bash
python manage.py seed_political_data
```

This command should add or update data for:

- United States;
- United Kingdom;
- Singapore;
- China;
- Russia.

The command uses `update_or_create()`, allowing it to be run more than once without producing duplicate records.

A successful result may display messages such as:

```text
Added or updated United States
Added or updated United Kingdom
Added or updated Singapore
Added or updated China
Added or updated Russia
Political data seeded successfully.
```

If Django reports:

```text
Unknown command: 'seed_political_data'
```

check that the file is located at:

```text
country/
└── management/
    ├── __init__.py
    └── commands/
        ├── __init__.py
        └── seed_political_data.py
```

Both `__init__.py` files must exist.

---

# 13. Creating a Django Administrator Account

To access Django Admin, create a superuser:

```bash
python manage.py createsuperuser
```

Enter:

- username;
- email address;
- password.

The password will not appear while typing.

After starting the server, open:

```text
http://127.0.0.1:8000/admin/
```

Log in using the superuser account.

Django Admin can be used to inspect:

- countries;
- institutions;
- policies;
- influence connections.

---

# 14. Running the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The terminal should display an address similar to:

```text
http://127.0.0.1:8000/
```

Open the address in a web browser.

To stop the server, press:

```text
Control + C
```

The development server should only be used for local testing. It is not intended as a production web server.

---

# 15. Recommended First-Time Installation Sequence

Run the following commands from the main project folder.

## macOS or Linux

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd django-political-system-prototype

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated key into `.env`.

Then run:

```bash
python manage.py check
python manage.py migrate
python manage.py seed_political_data
python manage.py runserver
```

## Windows PowerShell

```powershell
git clone YOUR_GITHUB_REPOSITORY_URL
cd django-political-system-prototype

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

copy .env.example .env

python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated key into `.env`.

Then run:

```powershell
python manage.py check
python manage.py migrate
python manage.py seed_political_data
python manage.py runserver
```

---

# 16. Updating the Project

After making changes, check the modified files:

```bash
git status
```

Stage the changes:

```bash
git add .
```

Create a commit:

```bash
git commit -m "Update Django political system prototype"
```

Upload the commit:

```bash
git push
```

Before committing, confirm that `.env` does not appear in:

```bash
git status
```

If `.env` has already been tracked, remove it from Git tracking without deleting the local file:

```bash
git rm --cached .env
```

Then commit the change:

```bash
git commit -m "Remove environment file from Git tracking"
git push
```

Generate a new secret key if the previous one was publicly exposed.

---

# 17. Updating the Python Dependencies

When a new package is installed, update `requirements.txt`.

Example:

```bash
pip install package-name
pip freeze > requirements.txt
```

Commit the updated file:

```bash
git add requirements.txt
git commit -m "Update Python dependencies"
git push
```

---

# 18. Expected Project Structure

The project should resemble:

```text
django-political-system-prototype/
├── .env
├── .env.example
├── .gitignore
├── README.md
├── REQUIREMENTS.md
├── requirements.txt
├── manage.py
│
├── country/
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── seed_political_data.py
│   │
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   │   └── country/
│   │       ├── index.html
│   │       ├── layout.html
│   │       ├── public_state.html
│   │       └── system_view.html
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── middleware.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
└── civilization/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

The real `.env` file remains on the local computer and should not appear in the GitHub repository.

---

# 19. Common Installation Problems

## `python: command not found`

Try:

```bash
python3 --version
```

Then use `python3` instead of `python`.

## `No module named django`

Activate the virtual environment and install the packages:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## `No module named dotenv`

Install `python-dotenv`:

```bash
pip install python-dotenv
```

Then update the dependency file:

```bash
pip freeze > requirements.txt
```

## `KeyError: 'DJANGO_SECRET_KEY'`

Check that `.env` contains:

```env
DJANGO_SECRET_KEY=your-generated-secret-key
```

Confirm that `.env` is in the same folder as `manage.py`.

## `You have unapplied migrations`

Run:

```bash
python manage.py migrate
```

## `Unknown command: seed_political_data`

Check the management-command folder structure and ensure both `__init__.py` files exist.

## Port 8000 is already in use

Run the server on another port:

```bash
python manage.py runserver 8001
```

Then open:

```text
http://127.0.0.1:8001/
```

## Static files do not appear

During development, confirm that:

```python
DEBUG = True
```

Also check the static-file configuration in `settings.py`.

## The announcement count displays `00`

Run:

```bash
python manage.py seed_political_data
```

The public view displays only policies with the status:

```text
authorized
implemented
```

Policies marked `proposed` or `processed` remain stored but do not appear publicly.

---

# 20. Running Tests

Run the Django test suite:

```bash
python manage.py test
```

Run only the tests for the `country` application:

```bash
python manage.py test country
```

The project should be tested for:

- successful loading of the country-selection page;
- successful loading of public country pages;
- successful loading of system-view pages;
- correct filtering of authorised and implemented policies;
- separation of decision, influence, and implementation layers;
- correct links between policies and institutions;
- missing-country responses;
- empty database states.

---

# 21. Installation Checklist

Before running the project, confirm that:

- [ ] Python is installed.
- [ ] Git is installed.
- [ ] The repository has been downloaded or cloned.
- [ ] The complete project folder is open in Visual Studio Code.
- [ ] A virtual environment has been created.
- [ ] The virtual environment is active.
- [ ] `requirements.txt` has been installed.
- [ ] `.env` has been created.
- [ ] A unique Django secret key has been added to `.env`.
- [ ] `.env` is ignored by Git.
- [ ] Database migrations have been applied.
- [ ] Comparative political data have been seeded.
- [ ] `python manage.py check` reports no errors.
- [ ] The development server starts successfully.

---

# 22. Security Notice

Never publish:

- the real Django `SECRET_KEY`;
- the `.env` file;
- API keys;
- database passwords;
- email passwords;
- access tokens;
- private authentication credentials.

The repository should contain `.env.example`, but it must not contain the real `.env`.

If a secret is accidentally uploaded publicly:

1. generate a new secret;
2. update the local `.env`;
3. remove the exposed value from the repository;
4. commit the correction;
5. push the updated repository.

---

# 23. Quick Start

After cloning the repository, the basic installation process is:

```bash
cd django-political-system-prototype

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

Create `.env`:

```env
DJANGO_SECRET_KEY=your-generated-secret-key
DJANGO_DEBUG=True
```

Then run:

```bash
python manage.py check
python manage.py migrate
python manage.py seed_political_data
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```
