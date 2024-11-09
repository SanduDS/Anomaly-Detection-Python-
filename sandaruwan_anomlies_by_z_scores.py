####################################################################################################################################
# This Python script generates a real-time plot of random data points and identifies anomalies using z-scores.                     #
# The plot dynamically updates with new data points, and the x-axis limits adjust to show the most recent 100 data points.         #
# and consider total datapoint when calculating z-scores. Anomalies are highlighted with a '*' marker.                             #
#                                                                                                                                  #
# ********************************************* !!! Z-Score based Anomaly Detection !!! *******************************************# 
#                                                                                                                                  #                                                 
# Z-score anomaly detection is a statistical method used to identify outliers in a dataset.                                        #
# The z-score measures how many standard deviations a data point is from the mean of the dataset.                                  #
# A data point is considered an anomaly if its z-score is beyond a specified threshold (e.g., greater than 0.9 or less than -0.9). # 
# This method helps in detecting data points that significantly deviate from the normal distribution.                              #
#                                                                                                                                  #
# Steps to Calculate Z-Score:                                                                                                      #
# 1. Calculate the mean (average) of the dataset.                                                                                  #
# 2. Calculate the standard deviation of the dataset.                                                                              #
# 3. For each data point, subtract the mean and divide by the standard deviation.                                                  #
#    Formula: z = (x - μ) / σ                                                                                                      #
#    where:                                                                                                                        #
#       x = data point                                                                                                             #
#       μ = mean of the dataset                                                                                                    #
#       σ = standard deviation of the dataset                                                                                      #
# 4. Compare the z-score to the threshold to determine if the data point is an anomaly.                                            #
#                                                                                                                                  #
####################################################################################################################################
# Steps to Run the Script                                                                                                          #
# 1. Install Required Libraries: Ensure you have the necessary libraries installed. `pip install matplotlib numpy`                 #
# 2. You can install them using pip if they are not already installed.                                                             #
# 3. Save the Script                                                                                                               #
# 4. Run the script. `python3 test.py`                                                                                             #             
####################################################################################################################################
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Create a plot figure and axis
plot_figure, ax = plt.subplots()

# Set the size of the plot figure
plot_figure.set_size_inches(10, 6)

# Lists to store raw data 
row_x_data, raw_data = [], []

# Lists to store anomalies
anomaly_x_data, anomaly_data = [], []

# List to store all data points
data_stream = []

# Create plot objects
plot1, = plt.plot([], [], 'o', color='blue',  label='Normal Data',  linestyle = 'dotted')
plot2, = plt.plot([], [], 'o', color='red', label='Anomaly Data')

# List to store the iteration number of refreshing the plot
data_round = []

# Anomaly detection threshold of z-score
threshold = 0.9

# Set axis limits (x-axis will reset)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# Initialize function for plot
def init():
    plot1.set_data([], [])
    plot2.set_data([], [])
    return plot1,plot2

# Function to generate random data points
def generate_data():
    # Reset when it reaches a multiple of 100 (simulate a streaming effect)
    data_stream_length = len(data_round)
    if data_stream_length % 100 == 0 and data_stream_length != 0:
        row_x_data.clear()
        raw_data.clear()
        anomaly_x_data.clear()
        anomaly_data.clear()
        ax.set_xlim(data_stream_length, data_stream_length + 100)  # Reset x-axis
        plt.draw()

    # generate random data points between 0 and 100    
    rn_data_point =  np.random.uniform(0, 100)
    # print(f"Data Point: {rn_data_point}")
    data_stream.append(rn_data_point)
    return rn_data_point

# This function to calculate the z-score of a data point
def calculate_z_score(data_point):
    # Calculate the mean 
    mean = np.mean(data_stream)

    # Calculate the standard deviation
    std_dev = np.std(data_stream)
 
    # Calculate the z-scores
    # Avoiding  Error division by zero
    if std_dev == 0:
        return 0
    z_score = (data_point - mean) / std_dev
    return z_score

def check_anomaly(data_point):
    # Retrieve the z-score
    z_score = calculate_z_score(data_point)

    # Identify the anomalies
    is_anomaly = False
    if z_score > threshold or z_score < -threshold:
        # print(f"Anomaly Detected at point: {data_point}, Z-Score: {z_score}")
        is_anomaly = True
    return is_anomaly

# This function to update the plot with new data points
def updatePlot(frame):
    # Generate random data points
    new_data = generate_data()

    # Check if the data point is an anomaly
    # if an anomaly, add it to the anomaly list else add it to the raw data list
    is_anomaly = check_anomaly(new_data)
    if is_anomaly :
        anomaly_x_data.append(len(data_round))
        anomaly_data.append(new_data)
        plot2.set_data(anomaly_x_data, anomaly_data)
        # print(f"Anomaly Data: {new_data}")
    else:
        row_x_data.append(len(data_round))
        raw_data.append(new_data)
        plot1.set_data(row_x_data, raw_data)
        # print(f"Normal Data: {new_data}")

    data_round.append(len(data_round) + 1)
    return plot1,plot2

# Create the animation of the plot
ani = animation.FuncAnimation(plot_figure, updatePlot, init_func=init, blit=True, interval=300)

# The title of the plot
plt.title("Real-time Plot with Anomaly Detection using Z-scores")

# The x-axis label
plt.xlabel("Random Data Points - X")

# The y-axis label
plt.ylabel("Random Data Points - Y")

# Show the legend
plt.legend(loc="lower right")

# Show the grid
plt.grid()

# Show the plot
plt.show()
