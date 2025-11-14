# app/config.py
from __future__ import annotations
import sys
from pydantic import Field, AnyHttpUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Azure REST
    AZURE_ACCOUNT: str = Field(..., env="AZURE_ACCOUNT")
    AZURE_CONTAINER: str = Field("incoming", env="AZURE_CONTAINER")
    AZURE_BASE_URL: AnyHttpUrl | None = Field(None, env="AZURE_BASE_URL")
    AZURE_SAS_TOKEN: str | None = Field(None, env="AZURE_SAS_TOKEN")
    AZURE_BASIC_USER: str | None = Field(None, env="AZURE_BASIC_USER")
    AZURE_BASIC_PASS: str | None = Field(None, env="AZURE_BASIC_PASS")

    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # SOAP
    SOAP_WSDL_URL: AnyHttpUrl = Field(..., env="SOAP_WSDL_URL")
    SOAP_USER: str | None = Field(None, env="SOAP_USER")
    SOAP_PASS: str | None = Field(None, env="SOAP_PASS")

    # Orchestration
    SCHED_INTERVAL_SECONDS: int = Field(60, env="SCHED_INTERVAL_SECONDS")

    # Paths
    INCOMING_DIR: str = Field("./app/runtime/incoming", env="INCOMING_DIR")

    class Config:
        env_file = ".env"
        case_sensitive = False

# Instantiate and show a readable error message on failure
try:
    settings = Settings()
except Exception as exc:
    print("\nERROR: Failed to load configuration (check your .env).", file=sys.stderr)
    # If the exception has an errors() method (ValidationError), print details
    if hasattr(exc, "errors"):
        for e in exc.errors():
            loc = ".".join(map(str, e.get("loc", [])))
            print(f" - {loc}: {e.get('msg')} ({e.get('type')})", file=sys.stderr)
    else:
        print(str(exc), file=sys.stderr)
    sys.exit(2)

