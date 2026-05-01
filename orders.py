from decimal import Decimal 
from typing import Dict ,Any ,Optional 
from binance .client import Client 
from binance .exceptions import BinanceAPIException ,BinanceOrderException 
import logging 
from .validators import OrderParams 

logger =logging .getLogger (__name__ )

class OrderManager :
    def __init__ (self ,client :Client ):
        self .client =client 

    def place_order (self ,params :OrderParams )->Dict [str ,Any ]:
        """Place a futures order with comprehensive error handling."""

        order_params ={
        'symbol':params .symbol ,
        'side':params .side ,
        'type':params .order_type ,
        'quantity':str (params .quantity ),
        }

        if params .order_type =='LIMIT'and params .price :
            order_params ['price']=str (params .price )
            order_params ['timeInForce']='GTC'

        logger .info (f"Placing order: {order_params }")

        try :
            symbol_info =self .client .futures_exchange_info ()
            valid_symbols =[s ['symbol']for s in symbol_info ['symbols']]

            if params .symbol not in valid_symbols :
                raise ValueError (f"Symbol {params .symbol } not found on testnet")

            order =self .client .futures_create_order (**order_params )

            logger .info (f"Order placed successfully: {order ['orderId']}")

            if order ['status']=='FILLED':
                order =self ._get_order_status (order ['orderId'],params .symbol )

            return order 

        except BinanceOrderException as e :
            error_msg =f"Order rejected by Binance: {e .message }"
            logger .error (error_msg )
            raise ValueError (error_msg )from e 

        except BinanceAPIException as e :
            error_msg =f"Binance API error: {e .message }"
            logger .error (error_msg )
            raise ValueError (error_msg )from e 

        except Exception as e :
            logger .error (f"Unexpected error placing order: {str (e )}")
            raise 

    def _get_order_status (self ,order_id :str ,symbol :str )->Dict [str ,Any ]:
        """Get detailed order status."""
        try :
            order =self .client .futures_get_order (symbol =symbol ,orderId =order_id )
            logger .info (f"Order status retrieved: {order }")
            return order 
        except Exception as e :
            logger .error (f"Failed to get order status: {e }")
            return {'orderId':order_id ,'status':'UNKNOWN','error':str (e )}
