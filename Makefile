# How to run Python.
PYTHON = python3

# How to run the management tool.
MANAGE = ${PYTHON} manage.py


all:
	commands

## commands     : show all commands.
commands:
	Makefile @sed -n 's/^## //p' $<

run:
	${MANAGE} runserver

migrate:
	${MANAGE} makemigrations
	${MANAGE} migrate

superuser:
	${MANAGE} createsuperuser

## test         : run all tests.
test :
	${MANAGE} test

## dev_database : re-make database using saved data
dev_database:
	${MANAGE} reset_db
	${MANAGE} makemigrations
	${MANAGE} migrate
	${MANAGE} loaddata afp_app/accounts/fixtures/*json
	${MANAGE} loaddata afp_app/claims/fixtures/*json
	${MANAGE} createsuperuser

## clean        : clean up.
clean:
	rm -rf \
		$$(find . -name '*~' -print) \
		$$(find . -name '*.pyc' -print) \
		$$(find . -name '__pycache__' -print) \
		htmlerror \
		$$(find . -name 'db.sqlite3' -print) \
