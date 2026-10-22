.PHONY: setup dev test seed build lint
PY=backend/.venv/bin/python

setup:
	test -f .env || cp .env.example .env
	python3 -m venv backend/.venv
	$(PY) -m pip install -q -U pip
	$(PY) -m pip install -q -r backend/requirements.txt
	cd frontend && npm install --no-audit --no-fund

dev:
	bash scripts/dev.sh

seed:
	cd backend && .venv/bin/python -m app.db.seed

test:
	cd backend && .venv/bin/python -m pytest -q
	cd frontend && npm run test --silent

lint:
	cd backend && .venv/bin/ruff check app tests
	cd frontend && npm run lint --silent

build:
	cd frontend && npm run build
