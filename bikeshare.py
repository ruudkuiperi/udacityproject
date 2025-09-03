import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
   
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
               city = str(input('Would you like information about Chicago, New York City or Washington?')).lower()
               if city in CITY_DATA:
                    break
               else:
                    print('That was not a valid input.') 
        except:
                print('That was not a valid input.') 
      
    # TO DO: get user input for month (all, january, february, ... , june)
    month = 'january'
    month_options = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        try:
               month = str(input('For which month would you like information? Choose from: all, january, february, march, april, may or june.')).lower()
               if month in month_options:
                    break
               else:
                    print('That was not a valid input.') 
        except:
                print('That was not a valid input.')
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = 'monday'
    day_options = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        try:
               day = str(input('For which week day would you like information? Choose from: all, monday, tuesday, wednesday, thursday, friday, saturday or sunday.')).lower()
               if day in day_options:
                    break
               else:
                    print('That was not a valid input.') 
        except:
                print('That was not a valid input.')
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':
        
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    # filter by day of week if applicable
    if day != 'all':
        
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[df['month'].mode()[0]-1]
    print('The most popular month is:', popular_month)
    
    # TO DO: display the most common day of week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    popular_day_of_week = days[df['day_of_week'].mode()[0]]
    print('The most popular day of the week is:', popular_day_of_week)

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour is:', popular_hour, ':00h', sep='')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular start station is:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular end station is:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['trips'] = "from " + df['Start Station'] + " to " + df['End Station'] 
    popular_trip = df['trips'].mode()[0]
    print('The most popular trip is:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    tt_total = df['Trip Duration'].sum()
    print('The total travel time in days, hours and minutes was:', pd.Timedelta(seconds=tt_total).round('min'))
    
    # TO DO: display mean travel time
    tt_mean = df['Trip Duration'].mean()
    print('The average travel time in minutes and secondes was:', pd.Timedelta(seconds=tt_mean).round('s'))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The amount of rentals per user type:', user_types, sep='\n')

    # TO DO: Display counts of gender
    if('Gender' in df.columns):
        gender = df['Gender'].value_counts()
        print('The amount of rentals per gender:', gender, sep='\n')        
    else:
        print('Gender information is not available for the selected city.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if('Birth Year' in df.columns):
        earliest_by = int(df['Birth Year'].min())
        recent_by = int(df['Birth Year'].max())
        common_by = int(df['Birth Year'].mode()[0])
        print('The earliest birth year is:', earliest_by)
        print('The most recent birth year is:', recent_by)
        print('The most common birth year is:', common_by)
    else:
        print('Birth year information is not available for the selected city.')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Allow the user to view raw data in the dataframe. Execute per 5 rows.""" 
    
    # set row index to zero
    n=0
    
    # get user input, handle errors and when user inputs 'yes' print raw data per 5 rows.
    while True:
        try:
            choice = str(input('Would you like to view five (more) rows of raw data for your selection? Enter yes or no.')).lower()
            if(choice == 'yes'):
                print(df.iloc[n:n+5])
                n+=5
            elif(choice == 'no'):
                break
            else:
                print('That was not a valid input.') 
        except:
                print('That was not a valid input.')    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter y or n.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
