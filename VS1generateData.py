import csv
import random
import time

while True:
    closed = True
    # Continuously check if the CSV file is currently being accessed by another file (client1.py)
    # Repeat this action until the file becomes available for modification
    while closed:
        try:
            with open('sensor_data1.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                # Generate random numbers for the data of the first client and put it in the csv file
                temperature = random.randint(50, 300)
                writer.writerow([str(temperature)])
                closed = False
        except IOError:
            pass

    time.sleep(10)
