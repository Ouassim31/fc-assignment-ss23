import time
import zmq
import logging
import random
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5554")

queued_data = []

while True:

    #  Wait for next request from client
    message = socket.recv_pyobj()
    print("Received (%s, %s, %s, %s)"
          % (message['pid'], message['time'], message['sensor'], message['sensor_temperature']))

    # Generate random maximum threshold based on the current weather
    time.sleep(1)
    current_weather = random.randint(-10, 30)
    if current_weather > 20:
        max_threshold = random.randint(150, 300)
    elif 10 < current_weather < 20:
        max_threshold = random.randint(100, 200)
    else:
        max_threshold = random.randint(20, 100)

    #  Send reply to client based on the engine temperature
    if (message['sensor_temperature']) > max_threshold:
        socket.send_pyobj({'max threshold': max_threshold, 'intensity': -10, 'time': time.time()})
    elif (message['sensor_temperature']) < max_threshold:
        socket.send_pyobj({'max threshold': max_threshold, 'intensity': +5, 'time': time.time()})
    else:
        socket.send_pyobj({'max threshold': max_threshold, 'intensity': 0, 'time': time.time()})
