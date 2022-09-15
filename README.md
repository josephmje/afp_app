# AFP Web App

## Set up environment

### Python

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
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
django-admin startproject afp_app
```

Run web app:

```bash
python manage.py runserver
```

Creating an app within the project:

```bash
cd afp_app
mkdir -p afp_app/accounts
python manage.py startapp accounts afp_app/accounts

mkdir -p afp_app/claims
python manage.py startapp claims afp_app/claims
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
cd afp_app/static/css
npm init
npm install --save bootstrap
sass bootstrap.scss bootstrap.css
```

## External Libraries

-   Bootstrap
-   datatables
-   jquery
-   FontAwesome

## User Permissions

-   is_superuser: Michael
-   is_staff: can log into admin pages (AFP Committee)
-   is_physician: physician review
-   is_scientist: clinician scientist review

## Navbar

-   RH
    -   Admin: is_admin
    -   Help: all
    -   Profile: all
    -   Logout: all

## To Do

-   learn [flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/#flexbox-background) for site layout
-   upload file doesn't capture files yet
-   instructions stating to use either file upload or URL for verification
-   simple forms
    -   Award
    -   Promotion
        -   needs to update user profile as well
        -   selection list shouldn't include Lecturer
    -   GrantReview
        -   branching logic for `is_member`, `num_days`
    -   EditorialBoard
    -   CommitteeWork
    -   Lectures
-   inline formsets
    -   Grant
        -   external tables include GrantAgency, GrantLink
        -   tagging system for investigators and roles
    -   Publication
        -   branching logic depending on publication type
        -   query Journal table
        -   external tables include PublicationLink
        -   tagging system for authors
    -   Exam
        -   external tables include Student
    -   Supervision
        -   external tables include Student
        -   limit choices based on student type
