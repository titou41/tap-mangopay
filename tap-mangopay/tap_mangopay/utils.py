from typing import Optional, Dict, Any, Iterable, List, Type
from tap_mangopay.client import MangopayEventStream
from datetime import datetime
import logging
from singer_sdk.exceptions import RetriableAPIError

logger = logging.getLogger(__name__)


class BaseEventStream(MangopayEventStream):
    """Base stream base on event with common functionality."""

    EVENT_TYPES: list = []

    def get_event_stream(self):
        """Get the events stream instance."""
        from tap_mangopay.streams import EventsStream
        return EventsStream(tap=self._tap)

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Get records based on events stream."""
        events = self.get_event_stream()
        
        for event in events.get_records(context):
            if event.get("EventType") in self.EVENT_TYPES:
                resource_id = event.get("ResourceId")
                if resource_id:
                    yield from self._get_resource_details(resource_id)

    def _get_resource_details(self, resource_id: str) -> Iterable[dict]:
        """Get detailed resource information."""
        url = self.path.format(
            client_id=self.config["client_id"],
            **{f"{self.name}_id": resource_id}
        )
        
        try:
            response = self.requests_session.get(
                url=self.url_base + url,
                headers=self.authenticator.auth_headers
            )
            
            if response.status_code == 200:
                yield response.json()
            else:
                logger.error(f"Failed to get {self.name} details for {resource_id}: {response.status_code}")
                logger.error(f"Response: {response.text}")
        
        except Exception as e:
            logger.error(f"Error fetching {self.name} {resource_id}: {str(e)}")

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        """Process the record after retrieval."""
        if not row:
            return None

        try:
            row["ProcessedAt"] = datetime.utcnow().isoformat()
            return row
        except Exception as e:
            self.logger.error(f"Error in post_process: {str(e)}")
            return Nones


class BaseUserStream(MangopayEventStream): 
    """Base stream base on user with common functionality."""

    def get_users_stream(self):
        """Get the events stream instance."""
        from tap_mangopay.streams import UserStream
        return UserStream(tap=self._tap)

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Get records for all users."""
        users = self.get_users_stream()
        
        for user in users.get_records(context):
            user_id = user.get("Id")
            if user_id:
                yield from self._get_user_resources(user_id)

    def _get_user_resources(self, user_id: str) -> Iterable[dict]:
        """Get resources for a specific user."""
        url = self.path.format(
            client_id=self.config["client_id"],
            user_id=user_id
        )
        
        try:
            response = self.requests_session.get(
                url=self.url_base + url,
                headers=self.authenticator.auth_headers
            )
            
            if response.status_code == 200:
                yield from response.json()
            else:
                logger.error(f"Failed to get {self.name} for user {user_id}: {response.status_code}")
                
        except RetriableAPIError as e:
            logger.error(f"API error for user {user_id}: {str(e)}")

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        """Process each record after parsing."""
        processed_row = super().post_process(row, context)
        if processed_row:
            if "CreationDate" in processed_row:
                try:
                    if isinstance(processed_row["CreationDate"], str):
                        dt = datetime.fromisoformat(processed_row["CreationDate"].replace('Z', '+00:00'))
                        processed_row["CreationDate"] = int(dt.timestamp())
                except Exception as e:
                    self.logger.error(f"Error converting date: {str(e)}")
        return processed_row