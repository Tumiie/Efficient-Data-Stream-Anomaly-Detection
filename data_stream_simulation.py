import numpy as np
import rrcf
import matplotlib.pyplot as plt

def data_stream_generator(size=1000, seasonal=100, noise_level=1.0):

    """
    This function will generate a data stream with a seasonal pattern, noise, and random anomalies

    The parameters are:
        seasonal: this is the period of the seasonal pattern
        size: this is the number of data point in the stream
        noise_level: controls the randomness

    The function returns a numpy array with the generated data

    """
    #Define a trend to make the stream dynamic over time
    trend = np.linspace(0, 5, size)

    #Create a seasonal pattern to mimic the periodic variations
    seasonal = 10 * np.sin(np.linspace(0, 20 * np.pi, size) / seasonal)

    #Add the random noise to make the data less predictable
    noise = np.random.normal(0, noise_level, size)

    #Combine the trend, seasonality and noise to get the data stream
    data = trend + seasonal + noise

    return data

def forest_initialization(num_trees=40, tree_size=256):
    forest = []
    for _ in range(num_trees):
        tree = rrcf.RCTree()
        forest.append(tree)
    return forest
def update_forest(forest, point, tree_size):
    avg_codisp = 0  # Initialize average co-displacement score
    for tree in forest:
        if len(tree.leaves) > tree_size:
            # Forget the oldest point in the tree
            tree.forget_point(next(iter(tree.leaves.keys())))
        # Insert the new point into the tree
        tree.insert_point(point, index=point)
        # Calculate anomaly score
        avg_codisp += tree.codisp(point)
    
    avg_codisp /= len(forest)  # Average score across all trees
    return avg_codisp  

def visualize_data_stream(data, scores, threshold=10):
    """
    Displays a real-time plot of the data stream with anomalies marked.

    - `data`: The full data stream.
    - `scores`: Anomaly scores for each data point.
    - `threshold`: Score threshold above which points are flagged as anomalies.
    """
    window_size = 100  # Number of points displayed at a time in the window
    fig, ax = plt.subplots()
    
    # Initialize lists to hold the sliding window of data and anomaly flags
    stream_data = []
    anomaly_flags = []

    for i, (point, score) in enumerate(zip(data, scores)):
        # Update the sliding window data and flags lists
        stream_data.append(point)
        anomaly_flags.append(score > threshold)

        # Keep lists within the window size limit
        if len(stream_data) > window_size:
            stream_data.pop(0)
            anomaly_flags.pop(0)

        # Refresh plot
        ax.clear()
        ax.plot(range(len(stream_data)), stream_data, color='blue', label="Data")
        
        # Mark anomalies in red
        ax.scatter(
            [j for j, is_anomaly in enumerate(anomaly_flags) if is_anomaly],
            [stream_data[j] for j, is_anomaly in enumerate(anomaly_flags) if is_anomaly],
            color='red', label="Anomalies"
        )
        
        ax.set_title("Data Stream with Anomaly Detection")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        plt.pause(0.01)  # Pause for real-time effect
    
    plt.show()

def main():
    # Generate simulated data stream
    data = data_stream_generator(size=1000)
    
    # Initialize RRCF forest
    forest = forest_initialization(num_trees=40, tree_size=256)
    
    # List to store anomaly scores
    scores = []
    
    # Detect anomalies in the data stream
    for point in data:
        score = update_forest(forest, point, tree_size=256)
        scores.append(score)

    # Visualize results
    visualize_data_stream(data, scores, threshold=5)

if __name__ == "__main__":
    main()