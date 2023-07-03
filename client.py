#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import random
import os
import sys
import time
import logging
import itertools

context = zmq.Context()
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
#  Socket to talk to server
REQUEST_TIMEOUT = 2500
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://localhost:5555"
thermostat = 3
context = zmq.Context()

logging.info("Connecting to server…")
client = context.socket(zmq.REQ)
client.connect(SERVER_ENDPOINT)

for sequence in itertools.count():
    
    temperature = round(random.random(),2)+thermostat*0.1
    logging.info("Sending (%s)", temperature)
    pid = os.getpid()
    request = {
       'pid' : pid,
       'time': time.time(),
       'value':temperature
     }
    client.send_pyobj(request)
    retries_left = REQUEST_RETRIES
    while True:
        if (client.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
            reply = client.recv_pyobj()
            
            if reply['thermostat']:
                logging.info("recieving command : thermostat (%s)", reply['thermostat'])
                thermostat = eval('thermostat'+reply['thermostat'])
                retries_left = REQUEST_RETRIES
            break
            
            
        retries_left -= 1
        logging.warning("No response from server")
        # Socket is confused. Close and remove it.
        client.setsockopt(zmq.LINGER, 0)
        client.close()
        if retries_left == 0:
            logging.error("Server seems to be offline, abandoning")
            sys.exit()

        logging.info("Reconnecting to server…")
        # Create new connection
        client = context.socket(zmq.REQ)
        client.connect(SERVER_ENDPOINT)
        logging.info("Resending (%s)", request)
        client.send_pyobj(request)
    logging.info("thermostat at "+str(thermostat))
#  Do 10 requests, waiting each time for a response

    
    