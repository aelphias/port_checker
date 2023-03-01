# port_checker - 
# An app to give available port in range of 2 numbers
# 
import socket
import logging
from fastapi import FastAPI
from pathlib import Path

#creating a new directory called pythondirectory
Path("./log").mkdir(parents=True, exist_ok=True)

LOCAL_HOST = "0.0.0.0"
# TODO add date to log filename
LOG_FILE_PATH = f'./log/port_checker.log'
START = 49152
# END = 65535
END = 49160

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=LOG_FILE_PATH,
                    encoding='utf-8', level=logging.DEBUG)

# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')
# logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

# Create list
# with integers within given range (49152 to 65535)

def createList(r1, r2):
	return [item for item in range(r1, r2+1)]


def tryPort(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        sock.bind((LOCAL_HOST, port))
        result = True
    except:
        logging.info(f"Port {port} is in use")
    sock.close()
    return result


if '__main__' == __name__:
    lst = createList(START, END)
    #  while True:
    for port in lst:
        if tryPort(port):
            print(port)
            exit()
# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
