import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s" )

def Logger(name: str):
    return logging.getLogger(name)


