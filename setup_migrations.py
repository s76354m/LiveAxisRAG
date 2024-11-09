import os
import sys

def create_migrations_setup():
    try:
        # Create migrations directory structure
        os.makedirs("src/migrations/versions", exist_ok=True)
        
        # Create alembic.ini
        alembic_ini = """[alembic]
script_location = src/migrations
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s
prepend_sys_path = .
timezone = UTC
truncate_slug_length = 40
revision_environment = false
sourceless = false
version_locations = %(here)s/versions
version_path_separator = os
output_encoding = utf-8
sqlalchemy.url = driver://user:pass@localhost/dbname"""

        # Create env.py
        env_py = """import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from api.models import Base
target_metadata = Base.metadata

def get_url():
    return os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost:5432/swarmrag")

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()"""

        # Create script.py.mako template
        script_mako = """\"\"\"${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
\"\"\"
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}

def upgrade() -> None:
    ${upgrades if upgrades else "pass"}

def downgrade() -> None:
    ${downgrades if downgrades else "pass"}"""

        # Create initial migration script
        initial_migration = """\"\"\"initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000
\"\"\"
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create documents table
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('documents')
    op.drop_table('users')"""

        # Write files
        with open("alembic.ini", "w") as f:
            f.write(alembic_ini)
            
        with open("src/migrations/env.py", "w") as f:
            f.write(env_py)
            
        with open("src/migrations/script.py.mako", "w") as f:
            f.write(script_mako)
            
        with open("src/migrations/versions/001_initial_migration.py", "w") as f:
            f.write(initial_migration)

        # Create requirements update
        requirements = """alembic>=1.13.0
asyncpg>=0.29.0
psycopg2-binary>=2.9.9
python-dotenv>=1.0.0"""

        with open("requirements.txt", "a") as f:
            f.write(requirements)
            
        # Create migration commands in Makefile
        makefile = """
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
	alembic current"""

        with open("Makefile", "a") as f:
            f.write(makefile)
            
        print("✅ Migration setup has been created successfully!")
        print("✅ Requirements.txt has been updated with Alembic dependencies")
        print("✅ Makefile has been updated with migration commands")
        print("\nTo run migrations:")
        print("1. Update DATABASE_URL in your .env file")
        print("2. Run 'make migrations-up' to apply migrations")
        print("3. Run 'make migrations-create message=\"your message\"' to create new migrations")
        return True
    except Exception as e:
        print(f"❌ Error setting up migrations: {str(e)}")
        return False

if __name__ == "__main__":
    response = input("Do you want to set up database migrations? (y/n): ")
    if response.lower() == 'y':
        create_migrations_setup()
    else:
        print("Operation cancelled.")