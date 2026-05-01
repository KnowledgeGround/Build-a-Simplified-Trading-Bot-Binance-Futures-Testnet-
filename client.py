import os 
from typing import Optional ,Dict ,Any 
from binance .client import Client 
from binance .exceptions import BinanceAPIException ,BinanceOrderException 
from dotenv import load_dotenv 
from .validators import BinanceClientConfig 
from .logging_config import setup_logging 
import logging 

logger =logging .getLogger (__name__ )

class BinanceFuturesClient :
    def __init__ (self ,testnet :bool =True ):
        setup_logging ()
        load_dotenv ()

        api_key =os .getenv ('BINANCE_API_KEY')
        api_secret =os .getenv ('BINANCE_API_SECRET')

        if not api_key or not api_secret :
            raise ValueError ("Missing BINANCE_API_KEY or BINANCE_API_SECRET in .env")

        config =BinanceClientConfig (api_key =api_key ,api_secret =api_secret )


        self .client =Client (
        config .api_key ,
        config .api_secret ,
        testnet =testnet 
        )

        logger .info ("Binance Futures Testnet client initialized successfully")

    def get_account_balance (self ,symbol :str ="USDT")->Optional [Dict [str ,Any ]]:
        """Get account balance for specific asset."""
        try :
            balance =self .client .futures_account_balance ()
            for asset in balance :
                if asset ['asset']==symbol :
                    logger .info (f"Retrieved {symbol } balance: {asset }")
                    return asset 
            logger .warning (f"No {symbol } balance found")
            return None 
        except BinanceAPIException as e :
            logger .error (f"Failed to get balance: {e }")
            raise 

    def get_symbol_info (self ,symbol :str )->Optional [Dict [str ,Any ]]:
        """Get exchange info for specific symbol."""
        try :
            info =self .client .futures_exchange_info ()
            for sym in info ['symbols']:
                if sym ['symbol']==symbol :
                    logger .info (f"Retrieved symbol info for {symbol }")
                    return sym 
            logger .warning (f"Symbol {symbol } not found")
            return None 
        except BinanceAPIException as e :
            logger .error (f"Failed to get symbol info: {e }")
            raise 
