import sys
import os
from pathlib import Path
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 1. Add the "backend/" directory to Python path.
#    This ensures "app/models.py" can be imported as "from app.models import Base"
current_dir = Path(__file__).resolve()
backend_dir = current_dir.parents[
    1
]  # Move 2 levels up: [alembic/, env.py] => [backend/]
sys.path.append(str(backend_dir))

from app.database import Base

# 2. The Alembic Config object
config = context.config

# 3. Configure logging
fileConfig(config.config_file_name)

# 4. Metadata for 'autogenerate'
target_metadata = Base.metadata

# 5. Get the DB URL from environment variable "DATABASE_URL"
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
