# Project Overview: Analysis of Flight Data for Traffic Analysis and Flight Planning

The goal of this project is to analyze flight data from five airports in the Los Angeles area to gain insights into traffic patterns from 2018. The project involves two main functions that leverage the flight data:



1.   Top 3 Early Flight Carriers (carriers_on_time()):

> This function determines the top three early flight carriers on a given day of the year and a desired destination. By analyzing historical flight data, it identifies the airlines that consistently operate early morning flights to the specified destination. This information can be valuable to see airlines that are puctual with regard to a desired destination.


2.   Minimum People Traffic Analysis (crowd_avoidance()):

> The second function focuses on identifying the best five days and corresponding time periods in a given month with minimal people traffic at an airport of destination. By analyzing historical flight data and passenger traffic patterns, it pinpoints the days and time periods when there is likely to be lower passenger volume at the specified airport. This information can be useful for airlines and passengers to plan travel during less crowded periods, ensuring a smoother and more comfortable experience.


Los Angeles Airports are:

* Los Angeles International Airport (LAX)
* Ontario International Airport (ONT)
* John Wayne Airport (SNA)
* Hollywood Burbank Airport (BUR)
* Long Beach Airport (LGB)

Dataset information:

* fl_datetime: flight date time
* tailnum: Plane tail number.
* carrier: Two letter carrier abbreviation.
* origin, dest: Origin and destination.
* dep_time, arr_time: Actual departure and arrival times (format HHMM or HMM), local tz.
* dep_delay, arr_delay: Departure and arrival delays, in minutes. Negative times represent early departures/arrivals.
* air_time: Amount of time spent in the air, in minutes.




