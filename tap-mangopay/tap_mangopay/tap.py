"""Tap class for tap-mangopay."""
from typing import List
from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON Schema typing helpers


# Import des flux personnalisés
from .streams import (
    EventsStream,
    PayinStream,
    RefundStream,
    TransferStream,
    PayoutStream,
    UserStream,
    BankAccountsStream,
    KycStream,
    WalletStream
)

# Liste des types de flux
STREAM_TYPES = [
    EventsStream,
    PayinStream,
    RefundStream,
    TransferStream,
    PayoutStream,
    UserStream,
    BankAccountsStream,
    KycStream,
    WalletStream
]


class TapMangopay(Tap):
    """Singer tap for the Mangopay API."""

    name = "tap-mangopay"

    # Schéma de configuration
    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_id",
            th.StringType,
            required=True,
            description="Client ID for Mangopay API authentication."
        ),
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            description="API Key for Mangopay API authentication."
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync."
        ),
        th.Property(
            "environment",
            th.StringType,
            required=True,
            default="sandbox",
            allowed_values=["sandbox", "production"],  # Limite les valeurs possibles
            description="Environment to use (sandbox or production)"
        ),
        th.Property(
            "rate_limit_max_calls",
            th.IntegerType,
            required=False,
            default=2300,
            description="Maximum number of API calls allowed in the time window"
        ),
        th.Property(
            "rate_limit_time_window",
            th.IntegerType,
            required=False,
            default=900,
            description="Time window in seconds for rate limiting (default: 900 seconds = 15 minutes)"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
    