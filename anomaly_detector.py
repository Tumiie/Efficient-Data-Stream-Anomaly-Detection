#Tumelo Matobo - Efficient Data Stream Anomaly Detection

import numpy as np
import matplotlib.pyplot as plt 
import random

#Setting the parameters
#The total number of data points to be simulated
N = 1000
#The size of the window for calculating the mean and the standard deviation
WINDOW_SIZE = 100
#The period for the seasonal variations
SEASONAL_PERIOD = 100
#The threshold for determining the anomalies in standard deviations
ANOMALY_THRESHOLD = 3

"""
    The anomaly detection algorithm uses a sliding window approach where the mean and standard deviation of
    the last WINDOW_SIZE data points are calculated. If a new data point deviates from the mena by more than a
    specified number of standard deviations, it is flagged as an anomaly. This method is effective for detecting 
    the outliers in data that shows seasonal patterns and is adaptable to concept drift since it relies on the most
    recent data
"""

#The function will generate a data stream with seasonal variations and random noise
def data_stream_generator(data_points):
    #List to store the data
    data = []
    for i in range(data_points):
        #The base value generating a seasonal pattern
        base_value = 10 + 5 * np.sin(2 * np.pi * i / SEASONAL_PERIOD)
        #Adding the random noise to the base value
        noise = np.random.normal(0, 1)
        #The value is generated as a combination of the base value and the noise
        value = base_value + noise
        #THe anomaly is introduced with a 2% chance
        if random.random() < 0.02:
            value += random.randint(20, 50)
        data.append(value)
    return data

#The function for the real-time anomaly detection. It will detect the anomalies using a sliding window approach
def anomaly_detector(data_stream):
    #List to store the anomaly predictions
    predictions = []

    #For loop to iterate over the indices for continuous monitoring
    for i in range(len(data_stream)):
        if i < WINDOW_SIZE: 
            #Checking if there are enough data points to make a prediction
            predictions.append(1)
        else:
            #Extract the recent window of the data points
            window = data_stream[i - WINDOW_SIZE:i]
            #Calculating the mean of the window
            mean = np.mean(window)
            #Calculating the standard deviation of the window
            std_dev = np.std(window)

            #Checking if the current value is an anomaly
            if std_dev > 0:
                if abs(data_stream[i] - mean) > ANOMALY_THRESHOLD * std_dev:
                    #Is an anomaly
                    predictions.append(-1)
                else:
                    #Is normal
                    predictions.append(1)
            else:
                #If the standard deviation is zero then the data is normal
                predictions.append(1)      
    return predictions

#The function visualizes the data stream and the detected anomalies
def data_visualizer(data_stream):
    #Enabling the interactive plotting mode which updates the plot dynamically
    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 6))
    #Setting the title and the labels for the plot
    ax.set_title('Data Stream Anomaly Detection')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    #Initializing the lists to store the complete data and detected anomaly indices
    data, anomalies = [], []
    #Iterating through each data point in the data stream
    for i in range(len(data_stream)):
        data.append(data_stream[i])

        if i >= WINDOW_SIZE:
            window = data[i - WINDOW_SIZE:i]
            mean = np.mean(window)
            std_dev = np.std(window)
            #Checking if the current point deviates significantly from the mean
            if std_dev > 0 and abs(data[i] - mean) > ANOMALY_THRESHOLD * std_dev:
                anomalies.append(i)

        if i % 5 ==0:
            ax.clear()
            ax.plot(data, label='Data Stream', color='purple', alpha=0.5)
            ax.scatter(anomalies, [data[j] for j in anomalies], color='red', label='Anomalies', marker='x')
            ax.legend()
            plt.draw()
            plt.pause(0.01)

    plt.ioff()
    plt.show()

#Main function to run the simulation
def main():
    try:
        #Simulating the data stream
        data_stream = data_stream_generator(N)

        #Visualizing the results
        data_visualizer(data_stream)
     
    except Exception as e:
        print(f"An error has occured: {e}")

if __name__ == "__main__":
    main()