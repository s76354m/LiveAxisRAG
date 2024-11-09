
# Database Migrations
migrations-init:
	alembic init src/migrations

migrations-create:
	alembic revision --autogenerate -m "$(message)"

migrations-up:
	alembic upgrade head

migrations-down:
	alembic downgrade -1

migrations-history:
	alembic history --verbose

migrations-current:
	alembic current