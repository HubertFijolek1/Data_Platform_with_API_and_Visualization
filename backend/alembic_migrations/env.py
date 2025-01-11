import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from app.database import Base
from sqlalchemy import engine_from_config, pool

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

config = context.config
config.set_main_option("script_location", "alembic_migrations")

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
