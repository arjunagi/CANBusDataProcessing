#File to read the JSON file and process the CAN bus data in the following ways:
# 1. Read the file and retrieve the list of dictionaries.
# 2. Print the first 10 signal enteries of the file.  
# 3. Print all the different types of signals. Ask the user to select 1 and print the number of occurances and value range.
# 4. Calculate the vehicle trip time and trip distance.
# 5. Plot each signal type versus timestamp.
# 6. Compute the max and average vehicle speeds.
# 7. Trace the vehicle path on Google Map.
# 8. Calculate the mileage of the car using the given data in the file.

import os
import json
import pprint
import matplotlib.pyplot as pl
from pylab import *
import numpy as np
import pygmaps

#store the path of the JSON file
json_file = os.path.abspath("/Users/Karthik/Documents/ENTS_Courses/ENTS_749C/CANBusDataProcessing/alicedata.json")

# Creates a list of the dictionaries present in the JSON and returns this list.
#@input - the file path
#@return - list of dictionaries
def func1(json_file):
    list_of_dicts = [] #create an empty list
    with open(json_file) as fp:
        for each_dict in fp: #for each dictionay in the file
            list_of_dicts.append(json.loads(each_dict)) #append each dictionary to the list
    return list_of_dicts


# Pretty prints the the first 10 signal enteries
#@input - list of the dictionaries 
def func2(list_from_file):
    print("The first 10 signal entries:")
    pprint.pprint(list_from_file[:10],indent = 4, width = 105) #print the first 10 signal enteries with indent as 4 and the width of each line as 105
    print ("\n")


# Parses the list of dictionaries and prints the different signal names.
# It then asks the user to select 1 of these signals and prints the number 
# of occurances and value range of this signal.
#@input - list of the dictionaries
def func3(list_from_file):
    print("The different signal names are:")
    set_of_values = set()   #create an empty set. Use a set to avoid storing repeated values.
    for each_dict in list_from_file:
        if 'name' in each_dict: 
            set_of_values.add(each_dict['name']) # store the values of each key 'name' in a list
    for signals in set_of_values:
        print(signals)

    print ("\nEnter a signal name from the above list of signals:")
    signal_name = input() #Take input from the user for the dersired signal
    list_of_values = signal_values(list_from_file, signal_name) #Create a list of all the odometer values 
    print ("Number of occurances of the signal \"" + signal_name + "\": " + str(len(list_of_values)))
    print ("Range of values of the signal \"" + signal_name + "\": " + str(min(list_of_values)) + " to " + str(max(list_of_values))) # Print the range of the signal value by computing the min amd max value present in the list.


# Parses the list of dictionaries and retrieves the first and last timestamp and odometer values.
# Using these values, it calculates the trip time period and trip distance.
# @input - list of the dictionaries
# @return - trip distance and time period
def func4(list_from_file):
    list_of_odometer_values = signal_values(list_from_file, "odometer") #Create a list of all the odometer values 
    list_of_timestamp = []
    for each_dict in list_from_file:
        if each_dict.get('timestamp'):
            list_of_timestamp.append(each_dict.get('timestamp')) #Create a list of all timestamp values
    time_period = "{:.6f}".format(list_of_timestamp[len(list_of_timestamp)-1] - list_of_timestamp[0]) #Calculate the time period by subtracting the last and first timestamp.
    trip_distance = "{:.6f}".format(list_of_odometer_values[len(list_of_odometer_values)-1] - list_of_odometer_values[0]) #Calculate the trip distance by subtracting the last and first odometer value.
    print ("\nThe trip time period of vehicle is: "+ time_period + " seconds")
    print ("The trip distance is: " + trip_distance + " miles")
    return time_period,trip_distance


# Plot all the signal types versus timestamp.
# This function creates 3 figures(windows) with 4 plots each.
# @input - list of the dictionaries
def func5(list_from_file):

    figure(0) #Create a new figure window (0)
    odometer = signal_values(list_from_file, "odometer") # Get the odometer values
    odometer_time = timestamp_values(list_from_file, "odometer") #Get the corresponding timestamp values
    pl.subplot(2,2,1) #Divide the figure to contain 4 subplots (2 rows, 2 colums, the postion of this subplot is 1).
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Odometer (miles)")
    pl.plot(np.array(odometer_time),np.array(odometer)) #plot the time on x axis and odometer values on y axis

    latitude = signal_values(list_from_file, "latitude")
    latitude_time = timestamp_values(list_from_file, "latitude") 
    pl.subplot(2,2,2) #position of this subplot is 2
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Latitude (degrees)")
    pl.plot(np.array(latitude_time),np.array(latitude))

    torque_at_transmission = signal_values(list_from_file, "torque_at_transmission")
    torque_at_transmission_time = timestamp_values(list_from_file, "torque_at_transmission")
    pl.subplot(2,2,3) #position of this subplot is 3
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Torque at Transmission (Nm)")
    pl.plot(np.array(torque_at_transmission_time),np.array(torque_at_transmission))

    engine_speed = signal_values(list_from_file, "engine_speed")
    engine_speed_time = timestamp_values(list_from_file, "engine_speed")
    pl.subplot(2,2,4) #position of this subplot is 4
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Engine Speed (rpm)")
    pl.plot(np.array(engine_speed_time),np.array(engine_speed))

    figure(1) #Create a new figure window (1)
    steering_wheel_angle = signal_values(list_from_file, "steering_wheel_angle")
    steering_wheel_angle_time = timestamp_values(list_from_file, "steering_wheel_angle")
    pl.subplot(2,2,1)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Steering Wheel Angle (degrees)")
    pl.plot(np.array(steering_wheel_angle_time),np.array(steering_wheel_angle))

    accelerator_pedal_position = signal_values(list_from_file, "accelerator_pedal_position")
    accelerator_pedal_position_time = timestamp_values(list_from_file, "accelerator_pedal_position")
    pl.subplot(2,2,2)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Accelerator Pedal Position")
    pl.plot(np.array(accelerator_pedal_position_time),np.array(accelerator_pedal_position))

    transmission_gear_position = signal_values(list_from_file, "transmission_gear_position")
    transmission_gear_position_time = timestamp_values(list_from_file, "transmission_gear_position")
    pl.subplot(2,2,3)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Transmission Gear Position")
    pl.plot(np.array(transmission_gear_position_time),np.array(transmission_gear_position))

    brake_pedal_status = signal_values(list_from_file, "brake_pedal_status")
    brake_pedal_status_time = timestamp_values(list_from_file, "brake_pedal_status")
    pl.subplot(2,2,4)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Brake Pedal Status (True/False)")
    pl.plot(np.array(brake_pedal_status_time),np.array(brake_pedal_status))

    figure(2) #Create a new figure window (2)
    vehicle_speed = signal_values(list_from_file, "vehicle_speed")
    vehicle_speed_time = timestamp_values(list_from_file, "vehicle_speed")
    pl.subplot(2,2,1)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Vehicle Speed (miles/hour)")
    pl.plot(np.array(vehicle_speed_time),np.array(vehicle_speed))

    fuel_consumed_since_restart = signal_values(list_from_file, "fuel_consumed_since_restart")
    fuel_consumed_since_restart_time = timestamp_values(list_from_file, "fuel_consumed_since_restart")
    pl.subplot(2,2,2)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Fuel Consumed Since Restart (gallons)")
    pl.plot(np.array(fuel_consumed_since_restart_time),np.array(fuel_consumed_since_restart))

    longitude = signal_values(list_from_file, "longitude")
    longitude_time = timestamp_values(list_from_file, "longitude")
    pl.subplot(2,2,3)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Longitude (degrees)")
    pl.plot(np.array(longitude_time),np.array(longitude))

    fuel_level = signal_values(list_from_file, "fuel_level")
    fuel_level_time = timestamp_values(list_from_file, "fuel_level")
    pl.subplot(2,2,4)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Fuel Level (gallons)")
    pl.plot(np.array(fuel_level_time),np.array(fuel_level))
    
    show() # Display all the above 3 figures.

    
# Calculates the Maximum and Average speed of the vehicle.
#@input - list of dictionaries, trip period and trip distance.
def func6(list_from_file, trip_period, trip_distance):
    list_of_vehicle_speed_values = signal_values(list_from_file, "vehicle_speed") #get the list of vehicle speed values. Required to get the maximum speed.
    average_speed = "{:.6f}".format(float(trip_distance)/float(trip_period)) # Calculate the average speed = (total distance)/(total time)
    print ("\nThe maximum speed of the vehicle is: " + str(max(list_of_vehicle_speed_values)) + " miles per hour")
    print ("The averge speed of the vehicle is: " + str(average_speed) + " miles per second")


# Traces the path of the vehicle in Google Map. It uses the latitude and longitude values.
# @input - list of the dictionaries
def func7(list_from_file):
    list_of_latitude = signal_values(list_from_file, "latitude") #Get the list of latitude values 
    list_of_longitude = signal_values(list_from_file, "longitude") #Get the list of longitude values 
    trace_map = pygmaps.maps(list_of_latitude[0], list_of_longitude[0], 16) #Initialize the pygmap variable with the first latitude and longitude values from corresponding lists
    path = list(zip(list_of_latitude, list_of_longitude)) # Create the path using the list of latitude and longitude values
    trace_map.addpath(path) # Add the path in the map
    trace_map.draw('./trace_map.html') # Create the html file to display the path on Google Map.


# Calculate the mileage of the vehicle using the trip distance and fuel consumed since restart.
# @input - list of the dictionaries, total trip distance
def func8(list_from_file, trip_distance):
    fuel_consumed_since_restart = signal_values(list_from_file, "fuel_consumed_since_restart") #Get the list of fuel_consumed_from_restart values
    fuel = fuel_consumed_since_restart[len(fuel_consumed_since_restart)-1] - fuel_consumed_since_restart[0] #Get the fuel used.
    mileage = "{:.6f}".format(float(trip_distance)/ float(fuel)) #mileage = (trip_distance)/(fuel consumed)
    print ("\nThe mileage of the car is: " + mileage + " miles/gallon")


# Get the list of values and corresponding timestamps for the required signal.
#@input - list of dictionaries, signal name
#@return - lists of values of signal and corresponding timestamp
def signal_values(list_from_file, signal_name):
    signal = [] 
    for each_dict in list_from_file: 
        if each_dict.get('name') == signal_name:
            if signal_name == "transmission_gear_position": # Convert the transmission gear position from string to integer
                if each_dict.get('value') == "neutral":
                    signal.append(0)
                elif each_dict.get('value') == "first":
                    signal.append(1)
                elif each_dict.get('value') == "second":
                    signal.append(2)
                elif each_dict.get('value') == "third":
                    signal.append(3)
                elif each_dict.get('value') == "fourth":
                    signal.append(4)
            elif each_dict.get('name') == signal_name: 
                signal.append(each_dict.get('value')) # get the list of values for the required signal name.
    return signal


# Get the list of timestamps for the required signal.
#@input - list of dictionaries, signal name
#@return - lists of timestamps
def timestamp_values(ist_from_file, signal_name):
    timestamp = []
    for each_dict in list_from_file: 
        if each_dict.get('name') == signal_name:
            timestamp.append(each_dict.get('timestamp')) # get the timestamp for the required signal name.
    return timestamp


## Calling all the above functions in the required sequence
list_from_file = func1(json_file) # Get the list of dictionaries
func2(list_from_file) # Print the first 10 enteries
func3(list_from_file) # Print all the signal names, take an input from the user and print the number of occurances and value range
trip_period, trip_distance = func4(list_from_file) # Store the trip period and trip distance
func6(list_from_file, trip_period, trip_distance) # Compute the max and average speed of the vehicle
func7(list_from_file) # Plot the vehicle path on Google Maps
func8(list_from_file, trip_distance) # Calculate the mileage of the vehicle using the trip distance and fule used since restart.
func5(list_from_file) # Plot each signal versus timestamp
