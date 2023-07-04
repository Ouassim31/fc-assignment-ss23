#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import os
import time
import logging
import itertools
import csv

context = zmq.Context()
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
#  Socket to talk to server
REQUEST_TIMEOUT = 2500
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://localhost:5554"
thermostat = 3

logging.info("Connecting to server…")
client = context.socket(zmq.REQ)
client.connect(SERVER_ENDPOINT)

for sequence in itertools.count():
    # Take the first tuple on the queue from the csv data file and delete it from the file
    closed = True

    # this loop checks if the csv file is already open from another file (VS1generateData.py)
    # repeats this action until the file is free to be modified
    while closed:
        try:
            with open('sensor_data1.csv', 'r') as file:
                # Create a CSV reader object
                reader = csv.reader(file)
                # Read the first line as an array
                data = next(reader)
                # Read the remaining lines
                remaining_lines = list(reader)

            # open the same CSV file in write mode to write the remaining lines back to the file
            with open('sensor_data1.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(remaining_lines)

            closed = False
        except IOError:
            pass

    pid = os.getpid()
    request = {
        'pid': pid,
        'time': time.time(),
        'sensor': 1,
        'sensor_temperature': int(data[0]),
    }
    logging.info("Sending (%s, %s, %s, %s)"
                 % (request['pid'], request['time'], request['sensor'], request['sensor_temperature']))
    # try to send the request
    client.send_pyobj(request)
    retries_left = REQUEST_RETRIES
    while True:
        if (client.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
            reply = client.recv_pyobj()
            # if there is a valid reply, the message was delivered

            if reply['max threshold']:
                logging.info("Received (%s,%s,%s)" % (reply['max threshold'], reply['intensity'], reply['time']))
                retries_left = REQUEST_RETRIES
            # go to the beginning and create another request with new data
            break
        retries_left -= 1

        logging.warning("No response from server")
        # Socket is confused. Close and remove it.
        client.setsockopt(zmq.LINGER, 0)
        client.close()

        # if the client tried 3 times to connect to the server
        # renew the retries variable value
        # sleep the client for one minute
        if retries_left == 0:
            retries_left = REQUEST_RETRIES
            time.sleep(60)

        # and try again to connect to the server with new socket
        logging.info("Reconnecting to server…")
        # Create new connection
        client = context.socket(zmq.REQ)
        client.connect(SERVER_ENDPOINT)
        logging.info("Resending (%s)", request)
        client.send_pyobj(request)

    time.sleep(15)
