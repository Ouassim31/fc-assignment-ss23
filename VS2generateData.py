import csv
import random
import time

while True:
    closed = True
    while closed:
        try:
            with open('sensor_data2.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                # generate random numbers for the data of the second client and put it in the csv file
                temperature = random.randint(50, 300)
                writer.writerow([str(temperature)])
                closed = False
        except IOError:
            pass

    time.sleep(10)
