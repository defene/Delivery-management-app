from dataclasses import dataclass
from datetime import datetime

@dataclass
class TokenRecordDto:
    user_id: int
    token: str
    expires_at: datetime