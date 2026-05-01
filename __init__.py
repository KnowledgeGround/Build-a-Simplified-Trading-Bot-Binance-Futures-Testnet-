"""Trading Bot Core Package."""

from .client import BinanceFuturesClient 
from .orders import OrderManager 
from .validators import OrderParams 

__version__ ="1.0.0"
__all__ =["BinanceFuturesClient","OrderManager","OrderParams"]
