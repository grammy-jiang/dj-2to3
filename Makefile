# Makefile For This Project In Development

# Variables
PYTHON := python
MANAGE := $(PYTHON) manage.py
DJANGO_SETTINGS_MODULE_DEV = config.settings
DJANGO_SETTINGS_MODULE_TEST = tests.settings

# Commands
.PHONY: makemigrations migrate createsuperuser runserver_plus shell_plus reset_db all clean test

optimizemigration:
	$(MANAGE) optimizemigration --settings $(DJANGO_SETTINGS_MODULE_DEV) $(APP_LABEL) $(MIGRATION_NAME)

makemigrations:
	$(MANAGE) makemigrations --settings $(DJANGO_SETTINGS_MODULE_DEV)

migrate:
	$(MANAGE) migrate --settings $(DJANGO_SETTINGS_MODULE_DEV)

createsuperuser:
	$(MANAGE) createsuperuser --no-input --settings $(DJANGO_SETTINGS_MODULE_DEV)

runserver_plus:
	$(MANAGE) runserver_plus --settings $(DJANGO_SETTINGS_MODULE_DEV)

shell_plus:
	$(MANAGE) shell_plus --settings $(DJANGO_SETTINGS_MODULE_DEV)

reset_db:
	$(MANAGE) reset_db --no-input --settings $(DJANGO_SETTINGS_MODULE_DEV)

all: makemigrations migrate createsuperuser runserver_plus

clean: reset_db

test:
	$(MANAGE) test --no-input --settings $(DJANGO_SETTINGS_MODULE_TEST)
