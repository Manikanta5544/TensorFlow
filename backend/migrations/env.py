from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Import every entity module so their tables register on Base.metadata.
# Alembic autogenerate requires all models to be imported before it can
# compare metadata against the database schema.
from src.ai.domain import entities as ai_entities  # noqa: F401
from src.applications.domain import entities as applications_entities  # noqa: F401
from src.auth.domain import entities as auth_entities  # noqa: F401
from src.jobs.domain import entities as jobs_entities  # noqa: F401

from src.shared.config.settings import get_settings
from src.shared.database.session import Base

# Alembic Config object
config = context.config

# Configure Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Load application settings.
settings = get_settings()

# Use the application's validated DATABASE_URL instead of hardcoding
# the connection string in alembic.ini.
config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL,
)

# Metadata used for autogeneration.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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
    run_migrations_online()