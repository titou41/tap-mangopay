from __future__ import annotations
from typing import Optional, Any, Dict, List, Type
import requests
from singer_sdk import typing as th
from tap_mangopay.client import MangopayEventStream, MangopayPaginator
from .utils import BaseEventStream, BaseUserStream
from .schemas import (
        event_properties, payins_properties,refunds_properties, 
        transfers_properties,payouts_properties,users_properties,
        bankaccount_properties,kyc_properties,wallet_properties
)
import logging
from datetime import datetime, time
from typing import Optional, Iterable, Dict, Any
import logging
from singer_sdk.exceptions import RetriableAPIError



class EventsStream(MangopayEventStream):
    """Define custom stream for events."""

    name = "events"
    path = "/v2.01/{client_id}/events"
    primary_keys = ["ResourceId"]
    replication_key = "Date" 
    schema = event_properties.to_dict()
    records_jsonpath = "$[*]"


    def get_starting_replication_key_value(self, context: Optional[dict]) -> Any:
        """Get the starting value for the replication key.
        
        Returns:
            The last saved state value or None if no state exists.
        """
        state = self.get_context_state(context)
        if state:
            # Retourner la dernière date sauvegardée
            return state.get("replication_key_value")
        return None
        
    def get_replication_key_value(self, record: dict) -> Any:
        """Extract the replication key value from the record."""
        return record.get(self.replication_key)
    

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[Any]) -> Dict[str, Any]:
        """Return URL parameters for API request."""
        params = {
            "per_page": 100,
            "page": 1 if not next_page_token else next_page_token,
        }

        state = self.get_context_state(context)
        if state and state.get("replication_key_value"):
            params["AfterDate"] = int(state["replication_key_value"])

        return params

    def get_next_page_token(self, response: requests.Response, previous_token: Optional[Any]) -> Optional[Any]:
        """Return token for next page."""
        try:
            data = response.json()
            if not data:
                return None
                
            current_page = previous_token if previous_token else 1
            if len(data) == 100:
                return current_page + 1
            return None
        except Exception as e:
            self.logger.error(f"Error in pagination: {str(e)}")
            return None
    
    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return records."""
        try:
            data = response.json()
            self.logger.info(f"Received {len(data)} events")
            for record in data:
                yield record
        except Exception as e:
            self.logger.error(f"Error parsing response: {str(e)}")


class PayinStream(BaseEventStream):
    """Stream for Payin details."""

    name = "payin"
    path = "/v2.01/{client_id}/payins/{payin_id}"
    primary_keys = ["Id"]
    schema = payins_properties.to_dict()
    records_jsonpath = "$"
    
    EVENT_TYPES = [
        'PAYIN_NORMAL_CREATED',
        'PAYIN_NORMAL_FAILED',
        'PAYIN_NORMAL_SUCCEEDED'
    ]

        
class RefundStream(BaseEventStream):
    """Stream for Refund details."""

    name = "refund"
    path = "/v2.01/{client_id}/refunds/{refund_id}"
    primary_key = ["Id"]
    schema = refunds_properties.to_dict()
    records_jsonpath = "$"
    
    EVENT_TYPES = [
        'PAYIN_REFUND_CREATED', 
        'PAYIN_REFUND_FAILED', 
        'PAYIN_REFUND_SUCCEEDED'
    ]
   

class TransferStream(BaseEventStream):
    """Stream for Transfer details."""

    name = "transfer"
    path = "/v2.01/{client_id}/transfers/{transfer_id}"
    primary_key = ["Id"]
    schema = transfers_properties.to_dict()
    records_jsonpath = "$"
    
    EVENT_TYPES = [
        'TRANSFER_NORMAL_CREATED', 
        'TRANSFER_NORMAL_FAILED', 
        'TRANSFER_NORMAL_SUCCEEDED'
    ]

        
class PayoutStream(BaseEventStream):
    """Stream for Transfer details."""

    name = "payout"
    path = "/v2.01/{client_id}/payouts/{payout_id}"
    primary_key = ["Id"]
    schema = payouts_properties.to_dict()
    records_jsonpath = "$"
    
    EVENT_TYPES = [
        'PAYOUT_NORMAL_CREATED', 
        'PAYOUT_NORMAL_FAILED', 
        'PAYOUT_NORMAL_SUCCEEDED'
    ]

class UserStream(MangopayEventStream):   
    """Stream for Users details."""

    name = "users"
    path = "/v2.01/{client_id}/users"
    primary_keys = ["Id"]
    replication_key = "CreationDate"  # Désactive la réplication
    schema = users_properties.to_dict()
    records_jsonpath = "$[*]"


    def get_url_params(self, context: Optional[dict], next_page_token: Optional[Any]) -> Dict[str, Any]:
        """Return URL parameters for the request."""
        params = {
            "per_page": 100,
            "page": 1 if not next_page_token else next_page_token
        }
        self.logger.info(f"Requesting events with params: {params}")
        return params

    def get_next_page_token(self, response: requests.Response, previous_token: Optional[Any]) -> Optional[Any]:
        """Return token for next page."""
        try:
            data = response.json()
            if not data:
                return None
                
            current_page = previous_token if previous_token else 1
            if len(data) == 100:
                return current_page + 1
            return None
        except Exception as e:
            self.logger.error(f"Error in pagination: {str(e)}")
            return None
    
    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return records."""
        try:
            data = response.json()
            self.logger.info(f"Received {len(data)} events")
            for record in data:
                yield record
        except Exception as e:
            self.logger.error(f"Error parsing response: {str(e)}")


class KycStream(BaseEventStream):
    """Stream for KYC details."""

    name = "kyc"
    path = "/v2.01/{client_id}/kyc/documents/{kyc_id}"
    primary_keys = ["Id"]
    schema = kyc_properties.to_dict()
    records_jsonpath = "$"

    EVENT_TYPES = [
        'KYC_CREATED', 
        'KYC_SUCCEEDED', 
        'KYC_VALIDATION_ASKED',
        'KYC_OUTDATED'
    ]

    def get_resource_records(self, event: dict, resource_id_field: str, resource_types: List[str]) -> Iterable[dict]:
        """Override to use correct ID field."""
        return super().get_resource_records(
            event=event,
            resource_id_field="ResourceId",
            resource_types=self.EVENT_TYPES
        )



class BankAccountsStream(BaseUserStream):
    """Stream for bank accounts details."""

    name = "bankaccounts"
    path = "/v2.01/{client_id}/users/{user_id}/bankaccounts"
    primary_keys = ["Id"]
    records_jsonpath = "$[*]"
    schema = bankaccount_properties.to_dict()
    replication_key = "CreationDate"  # Désactive la réplication

    # Ajouter ces paramètres pour la gestion du rate limiting
    retry_after_wait_time = 60  # temps d'attente en secondes
    max_retries = 5  # nombre maximum de tentatives
    
    def request_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Request records from REST endpoint(s)."""
        retries = 0
        while retries < self.max_retries:
            try:
                yield from super().request_records(context)
                break  # Sort de la boucle si succès
            except RetriableAPIError as e:
                if e.response.status_code == 429:  # Too Many Requests
                    retries += 1
                    if retries >= self.max_retries:
                        raise Exception(f"Max retries ({self.max_retries}) exceeded")
                    
                    # Récupérer le temps d'attente depuis les headers si disponible
                    wait_time = int(e.response.headers.get('Retry-After', self.retry_after_wait_time))
                    
                    self.logger.info(f"Rate limit hit. Waiting {wait_time} seconds. Retry {retries}/{self.max_retries}")
                    time.sleep(wait_time)
                else:
                    raise e
                
class WalletStream(BaseUserStream):
    """Stream for Wallet details."""

    name = "wallet"
    path = "/v2.01/{client_id}/users/{user_id}/wallets"
    primary_keys = ["Id"]
    records_jsonpath = "$[*]"
    schema = wallet_properties.to_dict()
    