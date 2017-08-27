# CANBusDataProcessing

This project was done as part of the Vehicular Networks course during my Masters's degree.
This was assigned as part of introduction to Python.

The application parses CAN data from JSON file and 
1. identifies all of the different signal names in the data file, prints these signal names, then prompts the user to enter a signal name, 
and finally returns the number of occurrences and value range of the user-entered signal.
2. finds the vehicle trip time period and vehicle trip distance over which the data file was recorded
3. Plots each signal vs. trip time; such as vehicle speed, engine RPM, and other signal types versus time as the x-axis.
4. Computes maximum and average speeds of the vehicle.
5. Identifies where in the world the vehicle was driving and plot it’s position (latitude and longitude) trace on a Google Map.
Used pygmap module available at: https://code.google.com/p/pygmaps/

![Alt test](https://github.com/arjunagi/CANBusDataProcessing/blob/master/route_trace.png)
