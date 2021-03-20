source_dir := $(CURDIR)/src
migrations_dir = $(CURDIR)/migrations
tests_dir := $(CURDIR)/tests

PYTHONPATH += $(source_dir)
ENV_NAME ?= env
make_venv = python -m venv $(ENV_NAME)
env_dir = $(CURDIR)/$(ENV_NAME)
bin_dir = $(env_dir)/bin
activate_env = . $(bin_dir)/activate

FLASK_ENV ?= development
CONFIG_VARIABLE_NAME = FLASK_BLOG_SETTINGS
CONFIG_FILENAME = $(CURDIR)/$(FLASK_ENV)-settings.cfg
TEST_CONFIG_FILENAME = $(CURDIR)/test-settings.cfg

pytest_temp_files := .coverage .pytest_cache
PYTEST_FILE_OR_DIR ?=

define create-venv
	@echo Creating $@...
	$(make_venv)
	$(bin_dir)/pip install --upgrade pip
	$(bin_dir)/pip install pip-tools
endef

define clear-python-cache
	@echo Clearing Python cache...
	rm -rf `find . -type d -name ".cache"`
	rm -rf `find . -type d -name "__pycache__"`
	rm -rf `find . -type f -name "*.py[co]"`
	rm -rf `find . -type d -name "*.egg-info"`
	rm -rf `find . -type d -name "pip-wheel-metadata"`
endef

default: dev_install test

env:
	$(create-venv)

.PHONY: install
install: env
	$(bin_dir)/pip-sync requirements.txt

.PHONY: dev_install
dev_install: env
	$(bin_dir)/pip-sync requirements.txt dev-requirements.txt

.PHONY: lint
lint:
	$(bin_dir)/flake8 $(source_dir) $(migrations_dir)

.PHONY: format
format:
	$(bin_dir)/black $(source_dir) $(migrations_dir)

.PHONY: test
test: lint
	PYTHONPATH=$(PYTHONPATH) 														\
	$(CONFIG_VARIABLE_NAME)="$(TEST_CONFIG_FILENAME)" 	\
	$(bin_dir)/pytest -vvs 															\
		--cov=$(source_dir) 															\
		--cov-report term-missing 												\
		--cov-fail-under 0 																\
		$(PYTEST_FILE_OR_DIR)

.PHONY: run
run:
	PYTHONPATH=$(PYTHONPATH)		\
	FLASK_ENV=$(FLASK_ENV)			\
	$(bin_dir)/flask run

.PHONY: db_migration
db_migration:
	PYTHONPATH=$(PYTHONPATH)		\
	$(bin_dir)/flask db migrate

.PHONY: db_upgrade
db_upgrade:
	PYTHONPATH=$(PYTHONPATH)		\
	$(bin_dir)/flask db upgrade

.PHONY: db_downgrade
db_downgrade:
	PYTHONPATH=$(PYTHONPATH)			\
	$(bin_dir)/flask db downgrade

.PHONY: shell
shell:
	PYTHONPATH=$(PYTHONPATH) \
	$(bin_dir)/flask shell

.PHONY: clean
clean:
	rm -rf $(env_dir) $(pytest_temp_files)
	$(clear-python-cache)
