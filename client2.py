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
SERVER_ENDPOINT = "tcp://34.141.3.45:5554"

logging.info("Connecting to server…")
client = context.socket(zmq.REQ)
client.connect(SERVER_ENDPOINT)

for sequence in itertools.count():
    closed = True
    # Retrieve the first tuple from the queue in the CSV data file and remove it from the file
    # Continuously check if the CSV file is currently being accessed by another file (VS1generateData.py)
    # Repeat this action until the file becomes available for modification

    while closed:
        try:
            with open('sensor_data2.csv', 'r') as file:
                # Create a CSV reader object
                reader = csv.reader(file)
                # Read the first line as an array
                data = next(reader)
                # Read the remaining lines
                remaining_lines = list(reader)

            # Write the remaining lines back to the file
            with open('sensor_data2.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(remaining_lines)
            # Success! The first value from the queue has been retrieved
            closed = False
        except IOError:
            # Ignore the IOError and continue the loop until the file becomes available
            pass

    pid = os.getpid()
    # Create a request
    request = {
        'pid': pid,
        'time': time.time(),
        'sensor': 2,
        'sensor_temperature': int(data[0]),
    }
    logging.info("Sending (%s, %s, %s, %s)"
                 % (request['pid'], request['time'], request['sensor'], request['sensor_temperature']))
    # Try to send the request.
    client.send_pyobj(request)
    retries_left = REQUEST_RETRIES
    # Retry 3 times
    while True:
        if (client.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
            reply = client.recv_pyobj()
            # If there is a valid server reply, the message was delivered
            if reply['max threshold']:
                logging.info("Received (%s,%s,%s)" % (reply['max threshold'], reply['intensity'], reply['time']))
                retries_left = REQUEST_RETRIES
            # Success! Go to the beginning and create another request with new data
            break
        retries_left -= 1

        logging.warning("No response from server")
        # Socket is confused. Close and remove it.
        client.setsockopt(zmq.LINGER, 0)
        client.close()
        if retries_left == 0:
            # If the client has attempted to connect to the server unsuccessfully three times,
            # pause the client for one minute and then retry.
            retries_left = REQUEST_RETRIES
            time.sleep(60)

        logging.info("Reconnecting to server…")
        # Create new connection
        client = context.socket(zmq.REQ)
        client.connect(SERVER_ENDPOINT)
        logging.info("Resending (%s)", request)
        client.send_pyobj(request)

    time.sleep(15)
