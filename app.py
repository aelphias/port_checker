# port_checker - 
# An app to give available port in range of 2 numbers
#  TODO put test test2 with pytest

import socket
import logging
from pathlib import Path
import uvicorn
from fastapi import FastAPI

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

app = FastAPI()
@app.get("/")
async def root():
    lst = createList(START, END)
    for port in lst:
        if tryPort(port):
            return port
        

if __name__ == "__main__":
    uvicorn.run(app, host=LOCAL_HOST, port=49154)
