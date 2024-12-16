from __future__ import annotations
import base64
import sys
from typing import Any, Callable, Iterable, Optional, Dict
import logging
import requests
from datetime import datetime
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator
from singer_sdk.streams import RESTStream
from .rate_limiter import RateLimiter

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def convert_to_int(value: Any) -> int:
    """Convert any date value to integer timestamp."""
    if value is None:
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            try:
                dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                return int(dt.timestamp())
            except ValueError:
                return 0
    return 0


class MangopayPaginator(BaseAPIPaginator):
    """Paginator for Mangopay API responses."""

    def __init__(self, start_value: int = 1):
        super().__init__(start_value)
        self._value = start_value
        self._total_pages = None
        self._current_page = start_value
        self.logger = logging.getLogger(__name__)

    def has_more(self, response: requests.Response) -> bool:
        """Determine if there are more pages to fetch."""
        try:
            data = response.json()
            items_count = len(data)
            self.logger.info(f"Pagination: Found {items_count} items")
            
            if items_count == 0:
                self.logger.info("No items found, stopping pagination")
                return False
                
            if items_count < 100:
                self.logger.info(f"Found {items_count} items (less than 100), stopping pagination")
                return False
                
            self.logger.info(f"Found {items_count} items, continuing to next page")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in pagination: {str(e)}")
            return False

    def get_next(self, response: requests.Response) -> Optional[int]:
        """Get the next page number."""
        if not self.has_more(response):
            return None
            
        self._current_page += 1
        self.logger.info(f"Moving to page {self._current_page}")
        return self._current_page

class MangopayEventStream(RESTStream):
    
    def __init__(self, tap=None):
        super().__init__(tap)
        self._access_token = None
        self.logger = logging.getLogger(__name__)
        self.rate_limiter = RateLimiter(self.config) 

    @property
    def url_base(self) -> str:
        """Return the API URL root, based on the environment."""
        environment = self.config.get("environment", "sandbox")
        return f"https://api.{'sandbox.' if environment == 'sandbox' else ''}mangopay.com"

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object."""
        if not self._access_token:
            self._access_token = self.get_access_token()
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self._access_token
        )

    def request_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Request records from REST endpoint(s)."""
        try:
            # Utiliser super().request_records au lieu de request_records_wrapper
            for record in super().request_records(context):
                self.rate_limiter.wait_if_needed()
                yield record
        except Exception as e:
            self.logger.error(f"Error in request_records: {str(e)}")
            raise

    def _request(self, prepared_request, context: Optional[dict] = None) -> requests.Response:
        """Execute a prepared API request and return the response."""
        # Attendre si nécessaire avant chaque appel API
        self.rate_limiter.wait_if_needed()
        return super()._request(prepared_request, context)

    def get_access_token(self) -> str:
        """Get OAuth2 access token."""
        auth_header = base64.b64encode(
            f"{self.config['client_id']}:{self.config['api_key']}".encode()
        ).decode()
        
        response = requests.post(
            f"{self.url_base}/v2.01/{self.config['client_id']}/oauth/token",
            headers={
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data={"grant_type": "client_credentials"}
        )
        
        if response.status_code != 200:
            raise Exception(f"Authentication failed: {response.text}")
            
        return response.json()["access_token"]

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[Any]) -> Dict[str, Any]:
        """Return URL parameters for the request."""
        params: dict = {
            "per_page": 100,
            "page": 1 if not next_page_token else next_page_token,
        }
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return records."""
        data = response.json()
        for record in data:
            # Convert any date fields to integers
            if 'Date' in record:
                record['Date'] = convert_to_int(record['Date'])
            if 'CreationDate' in record:
                record['CreationDate'] = convert_to_int(record['CreationDate'])
            yield record