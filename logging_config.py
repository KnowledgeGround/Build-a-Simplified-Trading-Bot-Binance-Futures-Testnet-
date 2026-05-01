import logging 
from pathlib import Path 
from datetime import datetime 


def setup_logging (log_dir :str ="logs")->None :
    """Configure structured logging for the trading bot."""
    Path (log_dir ).mkdir (exist_ok =True )
    timestamp =datetime .now ().strftime ("%Y%m%d_%H%M%S")
    log_file =Path (log_dir )/f"trading_bot_{timestamp }.log"
    logging .root .setLevel (logging .INFO )
    file_handler =logging .FileHandler (log_file ,mode ='a',encoding ='utf-8')
    file_handler .setLevel (logging .DEBUG )
    console_handler =logging .StreamHandler ()
    console_handler .setLevel (logging .INFO )
    formatter =logging .Formatter ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler .setFormatter (formatter )
    console_handler .setFormatter (formatter )
    logging .root .addHandler (file_handler )
    logging .root .addHandler (console_handler )
    logging .root .propagate =False 
    logger =logging .getLogger (__name__ )
    logger .info (f"Logging initialized. Log file: {log_file }")
