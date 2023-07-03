
#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import logging

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
max_threshhold = 0.8
min_threshhold = 0.5
while True:
    #  Wait for next request from client
    message = socket.recv_pyobj()
    print("Received temperature: %s" % message['value'])
    

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    if(message['value'] >= max_threshhold):
        socket.send_pyobj({"thermostat":"-1"})
    elif(message['value'] <= min_threshhold):
        socket.send_pyobj({"thermostat":"+1"})
    else:
        socket.send_pyobj({"thermostat":None})