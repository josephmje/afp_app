# AFP Web App

## Start project structure

```bash
mkdir afp_app
cd afp_app/

mkdir data docs media static templates
```

## Set up environment

### Python

```bash
python3 -m venv venv
source venv/bin/activate
```

### Database

### Node, Sass, autoprefixer

```bash
npm install -g npm
npm install -g sass
npm install -g postcss-cli autoprefixer
```

## Basic Commands

Creating a project:

```bash
django-admin startproject afp .
```

Run web app:

```bash
python manage.py runserver
```

Creating an app within the project:

```bash
cd afp
django-admin startapp accounts
django-admin startapp claims
```

Set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create admin user:

```bash
python manage.py createsuperuser
```

## Custom Bootstrap

```bash
cd static/css
npm init
npm install --save bootstrap
sass bootstrap.scss bootstrap.css
```
