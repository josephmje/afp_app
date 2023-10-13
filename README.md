# AFP Web App

## Setting up environment

### Download code from GitHub

1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) the `afp_app` repository with your GitHub user.
This is now your own unique copy of the `afp_app` code. Changes here won't affect anyone else's work, so it's a safe space to explore edits to the code!
   
2. [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) your forked repository to your machine/computer.
While you can edit files [directly on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files), sometimes the changes you want to make will be complex and you will want to use a text editor that you have installed on your local machine/computer (one great text editor is [VSCode](https://code.visualstudio.com/)).
In order to work on the code locally, you must clone your forked repository.

### Database

Install [PostgreSQL](https://www.postgresql.org/download/) and create a new database called "afp".

A walkthrough can be found [here](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04).

### Python

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```



### Node, Sass, autoprefixer

```bash
npm install -g npm
npm install -g sass
npm install -g postcss-cli autoprefixer

# Add custom bootstrap
cd static/css
npm init
npm install --save bootstrap
sass bootstrap.scss bootstrap.css
```

## Basic Commands

The configuration files for running the web app can be found in `config/settings`.

To run the web app locally, use the settings found in the `local.py` file:

```bash
export DJANGO_SETTINGS_MODULE=config.settings.local
python manage.py runserver
```

Set up the database:

```bash
# Looks at the instructions found in afp/accounts/migrations and afp/claims/migrations
# Applies the changes to the database
python manage.py makemigrations
python manage.py migrate

# Creates database tables with standard fixed values
python manage.py loaddata afp/accounts/fixtures/*json
python manage.py loaddata afp/claims/fixtures/*json
```

Create admin user:

```bash
python manage.py createsuperuser
```

For a quick description of the files present in a Django web app, see the video [here](https://realpython.com/lessons/django-files/).

## Deployment

For a primer on how to deploy the web app using Google Cloud, see the following [video](https://www.youtube.com/watch?v=scdtpMBLT8A&ab_channel=GoogleCloudTech) and [example code](https://github.com/GoogleCloudPlatform/serverless-expeditions/tree/main/cloud-run-django-terraform).
