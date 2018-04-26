import logging

# Set logger
logging.getLogger(__name__).addHandler(logging.NullHandler())
FORMAT = "[%(asctime)s;%(levelname)s;%(filename)s:%(lineno)s;%(funcName)20s()] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
