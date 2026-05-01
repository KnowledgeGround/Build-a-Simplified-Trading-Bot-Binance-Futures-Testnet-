
import typer 
from rich .console import Console 
from rich .table import Table 
from rich .panel import Panel 
from decimal import Decimal 
from typing import Optional 
import logging 

from bot .client import BinanceFuturesClient 
from bot .orders import OrderManager 
from bot .validators import OrderParams 

console =Console ()
logger =logging .getLogger (__name__ )

app =typer .Typer (help ="Simplified Trading Bot for Binance Futures Testnet")

def create_order_manager ():
    """Create authenticated order manager."""
    client =BinanceFuturesClient (testnet =True )
    return OrderManager (client )

@app .command ()
def market (
symbol :str =typer .Argument (...,help ="Trading pair (e.g., BTCUSDT)"),
side :str =typer .Option ("BUY","--side","-s",help ="Order side: BUY/SELL"),
quantity :float =typer .Option (...,"--quantity","-q",help ="Order quantity"),
):
    """Place a MARKET order."""
    _place_order (symbol ,side ,"MARKET",quantity ,None )

@app .command ()
def limit (
symbol :str =typer .Argument (...,help ="Trading pair (e.g., BTCUSDT)"),
side :str =typer .Option ("BUY","--side","-s",help ="Order side: BUY/SELL"),
quantity :float =typer .Option (...,"--quantity","-q",help ="Order quantity"),
price :float =typer .Option (...,"--price","-p",help ="Limit price"),
):
    """Place a LIMIT order."""
    _place_order (symbol ,side ,"LIMIT",quantity ,price )

def _place_order (symbol :str ,side :str ,order_type :str ,quantity :float ,price :Optional [float ]):
    """Core order placement logic with rich UI."""

    try :

        params =OrderParams (
        symbol =symbol ,
        side =side ,
        order_type =order_type ,
        quantity =Decimal (str (quantity )),
        price =Decimal (str (price ))if price else None 
        )


        console .print (Panel (_format_order_summary (params ),title ="📊 Order Summary",border_style ="blue"))


        if not typer .confirm ("Confirm order placement?"):
            console .print ("❌ Order cancelled by user",style ="bold red")
            raise typer .Abort ()


        manager =create_order_manager ()
        order_result =manager .place_order (params )


        console .print (Panel (_format_order_result (order_result ),title ="✅ Order Executed",border_style ="green"))

        logger .info (f"CLI: Order completed successfully - {order_result }")

    except ValueError as e :
        console .print (f"❌ Validation Error: {e }",style ="bold red")
        logger .error (f"Validation failed: {e }")
        raise typer .Exit (code =1 )

    except Exception as e :
        console .print (f"❌ Execution Error: {e }",style ="bold red")
        logger .error (f"Order execution failed: {e }")
        raise typer .Exit (code =1 )

def _format_order_summary (params :OrderParams )->Table :
    """Format rich order summary table."""
    table =Table (show_header =False ,box =None )
    table .add_row ("Symbol",params .symbol )
    table .add_row ("Side",params .side )
    table .add_row ("Type",params .order_type )
    table .add_row ("Quantity",f"{params .quantity :.8f}")
    if params .price :
        table .add_row ("Price",f"${params .price :.2f}")
    return table 

def _format_order_result (order :dict )->Table :
    """Format rich order result table."""
    table =Table (show_header =False ,box =None )
    table .add_row ("Order ID",str (order .get ('orderId','N/A')))
    table .add_row ("Status",order .get ('status','UNKNOWN'))
    table .add_row ("Executed Qty",str (order .get ('executedQty','0')))
    table .add_row ("Avg Price",str (order .get ('avgPrice','N/A')))
    if 'cummulativeQuoteQty'in order :
        table .add_row ("Total Cost",f"${float (order ['cummulativeQuoteQty']):.2f}")
    return table 

if __name__ =="__main__":
    app ()