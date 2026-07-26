"""Runtime configuration sourced from explicit environment variables."""

from functools import cached_property
from typing import Self

from psycopg.conninfo import make_conninfo
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated process settings with libpq-compatible environment names."""

    model_config = SettingsConfigDict(
        env_file=None,
        extra="ignore",
        populate_by_name=True,
        validate_default=True,
    )

    pg_host: str = Field(default="postgres", alias="PGHOST", min_length=1)
    pg_port: int = Field(default=5432, alias="PGPORT", ge=1, le=65535)
    pg_database: str = Field(default="domaincatalog", alias="PGDATABASE", min_length=1)
    pg_user: str = Field(default="domaincatalog", alias="PGUSER", min_length=1)
    pg_password: SecretStr = Field(alias="PGPASSWORD", min_length=1)

    pool_min_size: int = Field(default=1, alias="DB_POOL_MIN_SIZE", ge=1)
    pool_max_size: int = Field(default=5, alias="DB_POOL_MAX_SIZE", ge=1)
    pool_timeout_seconds: float = Field(default=10.0, alias="DB_POOL_TIMEOUT_SECONDS", gt=0)
    pool_max_lifetime_seconds: float = Field(
        default=1800.0,
        alias="DB_POOL_MAX_LIFETIME_SECONDS",
        gt=0,
    )
    flyway_history_relation: str = Field(
        default="public.flyway_schema_history",
        alias="FLYWAY_HISTORY_RELATION",
        pattern=r"^[a-z_][a-z0-9_]*\.[a-z_][a-z0-9_]*$",
    )

    @classmethod
    def from_environment(cls) -> Self:
        """Load settings exclusively through the configured environment aliases."""

        return cls.model_validate({})

    @cached_property
    def database_conninfo(self) -> str:
        """Build an escaped libpq connection string without exposing it in logs."""

        return make_conninfo(
            host=self.pg_host,
            port=self.pg_port,
            dbname=self.pg_database,
            user=self.pg_user,
            password=self.pg_password.get_secret_value(),
        )
