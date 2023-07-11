# Fog Computing Prototyping Project SS23

This repository contains the code for a prototyping project created as an assignment for the "Fog Computing" module at the Technical University Berlin. The project focuses on solving fog-specific challenges, such as reliable message delivery.

## Installation

To use this project, you need to have the following dependencies installed:

* Python 
* pip 
* ZeroMQ library

Please follow the steps below to install the necessary dependencies:

Python: If Python is not installed on your system, you can download it from the official [Python website:](https://www.python.org/downloads/). Follow the installation instructions specific to your operating system.

pip: pip usually comes pre-installed with Python. However, if it's not available or you need to upgrade it, you can follow the [instructions](https://pip.pypa.io/en/stable/installation/) to install or upgrade pip.

ZeroMQ library: ZeroMQ is a prerequisite for this project. You can install it using pip by running the following command:

```bash
pip install pyzmq
```

## Files
* VS1generateData.py and VS2generateData.py are two virtual sensors that generate realistic temperature data every 10seconds and save it to a .csv file
* client1.py and client2.py are used to send the generated data to the cloud component (server.py)
* server.py - receives information from the clients and sends separate responses to each
client

## Instructions
The server should run on a cloud component. Our server runs on GCE with the following configurations :
* Machine type : e2-medium
* CPU platform : Intel Broadwell
* Architecture :  x86/64
* Operation system :  Ubuntu 20.04.6 LTS
* Firewall requiered rule : allow tcp:5554
* External IP address : 34.141.3.45
  
If you run your own server on another cloud component you should change the _SERVER_ENDPOINT variable_ in the client1.py and client2.py files.

1. Start the data generation:
```bash
py VS1generateData.py
py VS2generateData.py
```

2. Start the clients:
```bash
py client1.py
py client2.py
```

3. Make test with the message delivery by stopping the clients/server
## License

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
