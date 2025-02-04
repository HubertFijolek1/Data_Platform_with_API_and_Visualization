import os
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool

# Add the 'api' directory to sys.path to allow imports from 'app'
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api"))
)

from app.database import Base
from app.models.models import Dataset, User

# Set target_metadata for autogenerate
target_metadata = Base.metadata

# Get the database URL from the environment variable
database_url = os.getenv("DATABASE_URL")
if database_url:
    context.config.set_main_option("sqlalchemy.url", database_url)
else:
    raise ValueError("DATABASE_URL environment variable not set")


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = context.config.get_main_option("sqlalchemy.url")
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
        context.config.get_section(context.config.config_ini_section),
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
