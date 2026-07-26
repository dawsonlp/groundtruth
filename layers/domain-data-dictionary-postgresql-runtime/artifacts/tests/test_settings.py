"""Configuration validation and secret-handling tests."""

import pytest
from pydantic import ValidationError

from domaincatalog_api.settings import Settings


def test_password_is_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PGPASSWORD", raising=False)

    with pytest.raises(ValidationError):
        Settings.from_environment()


def test_password_is_redacted() -> None:
    settings = Settings.model_validate({"PGPASSWORD": "local-test-secret"})

    assert "local-test-secret" not in repr(settings)
    assert "local-test-secret" not in str(settings.model_dump())


def test_conninfo_escapes_values() -> None:
    settings = Settings.model_validate(
        {
            "PGHOST": "database host",
            "PGDATABASE": "catalog db",
            "PGUSER": "catalog user",
            "PGPASSWORD": "quotes ' and spaces",
        }
    )

    conninfo = settings.database_conninfo

    assert "host='database host'" in conninfo
    assert "dbname='catalog db'" in conninfo
    assert "password='quotes \\' and spaces'" in conninfo
