# Live-Arduino-Sound-Data-Analysis
This repository deals with the live data coming from arduino. Feel free the tweak the code however you like!

**analysis.py**

1. The code uses an unlimited deque to store all data points received from the Arduino.
2. The time domain plot displays all data points received since the program started running.
3. The frequency domain plot and spectrogram are updated based on the complete set of data points.
4. The time domain plot can become cluttered over time as more data points are received.

**analysis-101.py**

1. The code uses a deque with a specified maximum length to store only the most recent data points.
2. The time domain plot displays only the data points from the last 10 seconds, providing a focused visualization.
3. The frequency domain plot and spectrogram are updated based on the latest data points within the 10-second timeframe.
4. The x-axis limits of the frequency domain plot are adjusted to show a specific range of frequencies, improving clarity.
5. The code dynamically calculates the number of samples for the Fourier transform, adapting to the length of the data.
