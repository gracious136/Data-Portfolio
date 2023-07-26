import pandas as pd
import numpy as np

# load data
# This code is made to load our data stored on Google Drive
def gd_path(file_id):
    """Generate a shareable link from Google Drive file id."""
    return f"https://drive.google.com/uc?export=download&id={file_id}"

# Google Drive file ids
files_id = {
    "LAflights": "10kNZusetcMbSQetkC8rJLI4qtMFgbwmQ"
}

# Read data from Google Drive
LAflights = pd.read_csv(gd_path(files_id["LAflights"]), sep=",")


### Carriers on time: given a destination and a departure date, returns the three carriers with a lower departure delay in average.

def carriers_on_time():

  while True:
    look_date = input('Enter the date you are interested in. use this format (YYYY-MM-DD):\n')

    if len(look_date) == 10 and look_date[4] == look_date[7] == '-':
      look_year = look_date[:4]
      look_month = look_date[5:7]
      look_day = look_date[8:]

      if look_year.isdigit() and look_month.isdigit() and look_day.isdigit():
        pass
      else:
        print('\u26A0 Invalid Date Format. Please run the code again Enter Date (YYYY-MM-DD) \u26A0')
        break

    else:
      print('\u26A0 Invalid Date Format. Please run the code again and Enter Date (YYYY-MM-DD) \u26A0')
      break


    airports = np.sort(LAflights.dest.unique())
    print(f'\nThis is a list of the destination airports\n{airports}')
    destination = input('\nEnter your destination in three letters: ').upper()

    if destination in airports and len(destination)==3:
      pass
    else:
      print('\u26A0 Invalid Destination airport \u26A0')
      break

    results = LAflights.assign(flight_date = pd.to_datetime(LAflights['fl_datetime']).dt.date)\
    .loc[lambda record : (record['flight_date']==pd.to_datetime(look_date)) & (record['dest']== destination)]\
    .groupby(['flight_date', 'dest','op_carrier'])\
    .agg({'dep_delay':'mean'}).round({'dep_delay':0}).sort_values(by='dep_delay', ascending=True)\
    .rename(columns={'dep_delay':'average_departure_delay'})\
    .head(3)


    return results


carriers_on_time()


### Crowd avoidance: given a destination and a month, recommend which are the 5 best days and time range (morning, afternoon, evening and night) 
### where there is a low number of flights departing from the airport, so there will be less people on there. The time ranges will be:

# 1. Morning: 5 am to 12 pm (noon)
# 2. Afternoon: 12 pm to 5 pm
# 3. Evening: 5 pm to 9 pm
# 4. Night: 9 pm to 4 am

def crowd_avoidance():

  while True:
    valid_months =['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']


    travel_month = input('Enter your desired month in full (e.g January, March etc):\n').title()

    if travel_month.lower() in valid_months:
      pass
    else:
      print('\u26A0 Wrong Month Format. Please run the code again Enter month (e.g January, March etc) \u26A0')
      break

    airports = np.sort(LAflights.dest.unique())
    destination = input('Enter your destination in three letters: ').upper()

    if destination in airports and len(destination)==3:
      pass
    else:
      print('\u26A0 Invalid Destination airport \u26A0')
      break

    results = LAflights\
                    .assign(period = ['Morning' if 5 <= time <=12 else 'Afternoon'
                    if 12 <= time <=17 else 'Evening' if 17 <= time <= 21 else 'Night'
                    for time in pd.to_datetime(LAflights['fl_datetime']).dt.hour ])\
                    .assign(flight_date = pd.to_datetime(LAflights['fl_datetime']).dt.date)\
                    .assign(flight_month = pd.to_datetime(LAflights['fl_datetime']).dt.strftime('%B'))\
                    .loc[lambda record : (record['flight_month']== travel_month) & ((record['dest']== destination) | (record['origin']== destination))]\
                    .groupby(['flight_month', 'flight_date','period']).agg({'origin' : 'count'})\
                    .groupby(['flight_date', 'period']).agg({'origin':'sum'})\
                    .sort_values(by='origin', ascending=True)\
                    .rename(columns={'origin' : 'total_flights'})\
                    .head(5)

    return results


crowd_avoidance()













