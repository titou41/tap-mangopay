import time
from datetime import datetime, timedelta
import logging
from typing import Optional


class RateLimiter:
    def __init__(self, config: dict):
        self.max_calls = config.get("rate_limit_max_calls", 2300)
        self.time_window = config.get("rate_limit_time_window", 900)
        self.calls = []
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Rate limiter initialized with {self.max_calls} calls per {self.time_window} seconds")

    def wait_if_needed(self):
        """Attend si nécessaire pour respecter les limites."""
        now = datetime.now()
        # Nettoyer les appels plus vieux que la fenêtre de temps
        self.calls = [call_time for call_time in self.calls 
                     if now - call_time < timedelta(seconds=self.time_window)]
        
        if len(self.calls) >= self.max_calls:
            # Calculer le temps d'attente nécessaire
            oldest_call = min(self.calls)
            wait_time = (oldest_call + timedelta(seconds=self.time_window) - now).total_seconds()
            
            if wait_time > 0:
                self.logger.info(f"Rate limit atteint ({self.max_calls} appels en {self.time_window} secondes). "
                               f"Attente de {wait_time:.2f} secondes...")
                time.sleep(wait_time)
                # Vider la liste des appels après l'attente
                self.calls = []
        
        # Enregistrer le nouvel appel
        self.calls.append(now)