from typing import Optional

from .account import Account
from .plus import Plus

class Status:
    account: Account
    plus: Optional[Plus]
