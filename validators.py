import re 
from dataclasses import dataclass 
from decimal import Decimal 
from typing import Optional 

@dataclass 
class OrderParams :
    symbol :str 
    side :str 
    order_type :str 
    quantity :Decimal 
    price :Optional [Decimal ]=None 

    def __post_init__ (self ):
        self .symbol =self .symbol .strip ().upper ()
        self .side =self .side .strip ().upper ()
        self .order_type =self .order_type .strip ().upper ()

        if not re .match (r'^[A-Z0-9]+USDT$',self .symbol ):
            raise ValueError ('Symbol must be uppercase and end with USDT (e.g., BTCUSDT)')

        if self .side not in {'BUY','SELL'}:
            raise ValueError ('Side must be BUY or SELL')

        if self .order_type not in {'MARKET','LIMIT'}:
            raise ValueError ('Order type must be MARKET or LIMIT')

        if self .quantity <=0 :
            raise ValueError ('Quantity must be positive')
        if len (str (self .quantity ))>12 :
            raise ValueError ('Quantity precision too high')

        if self .order_type =='LIMIT':
            if self .price is None :
                raise ValueError ('Price is required for LIMIT orders')
            if self .price <=0 :
                raise ValueError ('Price must be positive')
        elif self .price is not None and self .price <=0 :
            raise ValueError ('Price must be positive')

@dataclass 
class BinanceClientConfig :
    api_key :str 
    api_secret :str 

    def __post_init__ (self ):
        if not self .api_key or len (self .api_key .strip ())<20 :
            raise ValueError ('Invalid API key format')
        if not self .api_secret or len (self .api_secret .strip ())<30 :
            raise ValueError ('Invalid API secret format')
