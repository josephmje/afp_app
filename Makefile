# Select Python version
PYTHON = venv/bin/python

# Run management tool
MANAGE = ${PYTHON} manage.py


all:
	commands

## commands     : show all commands.
commands: Makefile
	@sed -n 's/^## //p' $<

run:
	${MANAGE} runserver

migrate:
	${MANAGE} makemigrations
	${MANAGE} migrate

superuser:
	${MANAGE} createsuperuser

test :
	${MANAGE} test

dev_database:
	${MANAGE} makemigrations
	${MANAGE} migrate
	${MANAGE} loaddata afp/accounts/fixtures/*json
	${MANAGE} loaddata afp/claims/fixtures/*json
	${MANAGE} createsuperuser

clean:
	rm -rf \
		$$(find . -name '*~' -print) \
		$$(find . -name '*.pyc' -print) \
		$$(find . -name '__pycache__' -print) \
		$$(find . -name 'db.sqlite3' -print) \
		$$(find . -path './afp/*/migrations/*.py' ! -name '__init__.py' -print) \
		$$(find . -path './afp/*/migrations/*.pyc' -print) \
		htmlerror

