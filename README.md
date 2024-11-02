# Efficient-Data-Stream-Anomaly-Detection

<div align="justify"> 

**Algorithm Selection** 

For this project, I used the Isolation Forest algorithm, which is efficient and adaptable for anomaly detection in data streams. This algorithm isolates anomalies based on the principle that are rare and can be easily separated from normal data points. Isolation Forest builds binary trees using randomly selected features and split values. The anomalies are isolated in shorter paths within these trees due to their distinct characteristics, which makes them stand out from normal points. The algorithm assigns higher isolation scores to anomalies, facilitating quick and accurate identification.

Isolation Forest is particularly effective for high-dimensional data, as commonly found in financial transaction metrics and system monitoring. It can detect anomalies like unusual transaction amounts or irregular transaction patterns. Its adaptability is also invaluable. By periodically retraining with new data, the model remains responsive to evolving patterns in real-time, making it suitable for dynamic environments with changing user behaviour or systems loads.

The algorithm’s structure also allows it to accommodate seasonal variations in the data, such as predictable peaks during certain periods. This adaptability reduces false positives from expected fluctuations while still identifying true anomalies.

*Concept Drift & Seasonal Variations*: The Isolation Forest algorithm continuously updates its model based on recent data, allowing it to adapt to both concept drift and seasonal variations effectively.

*Real-time Detection*: The algorithm’s efficiency enables it to detect anomalies in real-time, as it does not require retraining on the entire dataset.

**Alternative Algorithms Considered**

While the Isolation Forest algorithm was ultimately selected for this project, it’s worth mentioning that several other algorithms could have been employed for anomaly detection. One notable alternative is Z-Score Analysis, a straightforward statistical method that calculates the Z-score of data points to identify anomalies based on how many standard deviations they deviate from the mean. This approach is simple to implement and works well for normally distributed data. However, its reliance on the assumption of a Gaussian distribution can limit its effectiveness when dealing with non-linear patterns or high-dimensional data.

Another contender is the Local Outlier Factor (LOF) algorithm. LOF operates by measuring the local density deviation of a data point compared to its neighbors, allowing it to identify points that significantly differ from their surroundings. This method is particularly good at detecting local anomalies in complex datasets. That said, it can be computationally intensive, especially with larger datasets, which may pose challenges in real-time applications.

The One-Class SVM is another algorithm that could have been considered. It functions by creating a hyperplane to separate normal data points from the origin, thus identifying those on the opposite side as anomalies. This approach is effective for high-dimensional data and can model complex boundaries, but it does require careful tuning of hyperparameters and can be slower when applied to large datasets.

Isolation Forest was chosen for this project due to its distinct advantages. One of its primary strengths is efficiency, it can handle large datasets without needing to retrain on the entire dataset, making it particularly well-suited for real-time applications. Furthermore, its adaptability allows for periodic retraining with new data, ensuring it remains effective in dynamic environments where user behavior and system loads can change rapidly. Isolation Forest also excels in high-dimensional spaces, which is crucial for analyzing financial transactions influenced by numerous variables. Its structure also accommodates the seasonal variations in data, helping to reduce false positives during expected fluctuations.

**Code Documentation**

**Data Stream Simulation**

The data_stream_generator(data_points) function generates a list of floating-point numbers that simulate a data stream with seasonal variations and random noise. 
random.random() < 0.02: This condition generates a random floating-point number between 0.0 and 1.0. If this number is less than 0.02 (which has a 2% chance), an anomaly is introduced. The 2% probability means that, on average, anomalies will occur in approximately 2% of the data points, reflecting a realistic scenario where anomalies are relatively rare.
value += random.randint(20, 50): If an anomaly is triggered, this line adds a random value between 20 and 50 to the current data point (value). This random spike simulates a significant deviation from the expected range of values, representing an anomaly.

**Anomaly Detection**

The anomaly_detector(data_stream) function employs the Isolation Forest algorithm to detect the anomalies based on a sliding window of recent data points.

for i in range(len(data_stream)): This loop goes through each data point in the data_stream. The approach allows for real-time monitoring, as each data point is evaluated immediately after it becomes available. 
if i < WINDOW_SIZE: For the first WINDOW_SIZE data points, there’s not enough data to apply a sliding window since fewer than WINDOW_SIZE points are available. predictions.append(1): Since an anomaly can’t be confidently detected with insufficient data, these initial points are labeled as "normal" (1). 
window = data_stream[i - WINDOW_SIZE:i]: Once WINDOW_SIZE or more data points are available, a "sliding window" of the last WINDOW_SIZE data points is taken. This allows us to focus only on recent data, which helps the detection adapt to trends or shifts in the data. 
mean = np.mean(window) and std_dev = np.std(window): Calculates the mean and standard deviation for the values in the sliding window. These act as dynamic thresholds to assess whether the current data point is significantly different from recent data trends. 
if std_dev > 0: A standard deviation of zero indicates no variation in the windowed data, so any deviation would likely not be meaningful. In this case, the point is labeled as normal. 
if abs(data_stream[i] - mean) > ANOMALY_THRESHOLD * std_dev: This checks if the current value is a set number of standard deviations away from the mean. If it is, it’s labeled as an anomaly (-1); if not, it’s labeled as normal (1). This approach adapts as the sliding window captures changes in data trends. When the standard deviation is zero, the point is assumed normal by default, which prevents false anomalies in data without recent variation.

**Visualization**

The data_visualizer(data_stream) function plots the data stream and highlights the detected anomalies in red. 
for i in range(len(data_stream)): Iterates over each data point in the data_stream. This allows each data point to be analyzed and visualized immediately, simulating a real-time data stream. 
data.append(data_stream[i]): Adds each point in the data stream to the data list, which keeps track of all data points for the ongoing visualization. 
if i >= WINDOW_SIZE: Starts anomaly detection once WINDOW_SIZE points are available, ensuring a minimum amount of data for statistical calculations. 
window = data[i - WINDOW_SIZE:i]: Creates a sliding window of the most recent WINDOW_SIZE points, allowing for localized calculations that adapt to recent trends. 
mean = np.mean(window) and std_dev = np.std(window): Calculates the mean and standard deviation for the sliding window, providing a dynamic baseline for anomaly detection. 
if std_dev > 0 and abs(data[i] - mean) > ANOMALY_THRESHOLD * std_dev: Checks if the current data point deviates significantly from the mean (by more than ANOMALY_THRESHOLD standard deviations). If it does, the point is labeled as an anomaly, and its index is added to the anomalies list. 
if i % 5 == 0: Updates the plot every fifth data point rather than with each point, reducing the computational load and making the plot more responsive. 
ax.clear(): Clears the previous plot, allowing the graph to refresh with updated data. ax.plot(...) and ax.scatter(...): Replots the data stream with anomalies indicated by red 'x' markers. plt.draw() and plt.pause(0.01): Redraws the plot and briefly pauses to simulate real-time plotting, keeping the visualization in sync with the data stream’s updates.

**Main Function**

try-except block for Error Handling: Wrapping the main code within a try block allows for robust error handling. This is essential in a data stream simulation, where unexpected issues (e.g., out-of-bound indices or invalid calculations) could disrupt the flow. Captures any error that occurs during execution, preventing the program from crashing unexpectedly and providing a user-friendly error message. 
data_stream = data_stream_generator(N): Generates a data stream with N data points, incorporating seasonal variations and noise. This simulated data mimics real-world conditions (such as financial data or system metrics), enabling realistic anomaly detection and visualization testing. 
data_visualizer(data_stream): This function takes the simulated data stream and visualizes it, displaying any detected anomalies. Visualizing the results is crucial for real-time anomaly detection since it allows users to see trends, patterns, and anomalies as they unfold in the data stream. </div>
