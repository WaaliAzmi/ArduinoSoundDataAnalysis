import serial
import matplotlib.pyplot as plt
import time

NUM_SENSORS = 5
DATA_RANGE_MIN = 0
DATA_RANGE_MAX = 1024
MAX_DISPLAY_TIME = 10  # Maximum display time in seconds

def initialize_serial(port, baud_rate):
    ser = serial.Serial(port, baud_rate)
    ser.timeout = 3
    ser.readline()
    return ser

def close_serial(ser):
    ser.close()

def read_data(ser):
    data = []
    for _ in range(NUM_SENSORS):
        line_data = ser.readline().decode().strip()
        sensor_value = int(line_data.split(":")[1].strip())
        # Scale the sensor value to the desired range
        scaled_value = (sensor_value / 1023) * (DATA_RANGE_MAX - DATA_RANGE_MIN) + DATA_RANGE_MIN
        data.append(scaled_value)
    return data

def update_plot(x_data, y_data, lines, data, timestamps, ax):
    current_time = time.time()
    x_data.append(current_time)
    timestamps.append(current_time)  # Append the current timestamp
    for i in range(NUM_SENSORS):
        y_data[i].append(data[i])
        lines[i].set_data(x_data, y_data[i])
    # Update x-axis limits based on the latest timestamp
    min_time = current_time - MAX_DISPLAY_TIME
    max_time = current_time
    ax.set_xlim(min_time, max_time)

def calculate_sampling_rate(timestamps):
    if len(timestamps) < 2:
        return None
    time_diff = timestamps[-1] - timestamps[-2]
    sampling_rate = 1 / time_diff
    return sampling_rate

def plot_live_data(port, baud_rate):
    ser = initialize_serial(port, baud_rate)

    plt.ion()
    fig, ax = plt.subplots()
    x_data = []
    y_data = [[] for _ in range(NUM_SENSORS)]
    lines = [ax.plot(x_data, y_data[i])[0] for i in range(NUM_SENSORS)]
    ax.set_xlabel('Time')
    ax.set_ylabel('Data')
    ax.set_title('Live Data Plot')
    ax.set_ylim(DATA_RANGE_MIN, DATA_RANGE_MAX)  # Set y-axis limits

    timestamps = []  # Initialize timestamps list

    try:
        while True:
            data = read_data(ser)
            update_plot(x_data, y_data, lines, data, timestamps, ax)
            ax.relim()
            ax.autoscale_view()
            plt.draw()
            plt.pause(0.01)

            # Calculate sampling rate for each sensor
            sampling_rates = [calculate_sampling_rate(timestamps) for _ in range(NUM_SENSORS)]
            print("Sampling Rates:", sampling_rates)
    except KeyboardInterrupt:
        pass

    close_serial(ser)
    plt.ioff()
    plt.show()

# Example usage
port_name = 'COM6'  # Replace 'COM6' with the appropriate port name for your Arduino
baud_rate = 9600

plot_live_data(port_name, baud_rate)
