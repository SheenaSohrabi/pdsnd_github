#Links used to get help
#https://stackoverflow.com/questions/35261055/method-object-is-not-subscriptable-dont-know-whats-wrong
#https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/03_subset_data.html
#https://www.tutorialspoint.com/python/string_title.htm
#https://www.shanelynn.ie/select-pandas-dataframe-rows-and-columns-using-iloc-loc-and-ix/

mport time
import pandas as pd
import numpy as np
import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all','january','february','march','april','may','june']

DAY_DATA = ['all', 'monday', 'tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_name =''
    while city_name.lower() not in CITY_DATA:
        city_name = input("Which City would you like the bike data to be analysed for? ")
        if city_name.lower() in CITY_DATA:
            city = CITY_DATA[city_name.lower()]

        else:
            print("Error! Please input chicago, new york city or washington. Try again.\n")

    month_name =''
    while month_name.lower() not in MONTH_DATA:
        # get user input for month (all, january, february, ... , june)
        month_name = input("Which month do you want the data to be analysed for? ")

        if month_name.lower() in MONTH_DATA:
           month = month_name.lower()

        else:
            print("Error! Please input all, or january, february, ... Try again.\n")

    day_name =''
    while day_name.lower() not in DAY_DATA:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day_name = input("Which day of week would you like the bike data to be analysed for? ")
        if day_name.lower() in DAY_DATA:
           day = day_name.lower()

        else:
            print("Error! Please input all, or monday, tuesday, ... Try again.\n")

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

    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month

    # extract day from the Start Time column to create a day column
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    #filter by given month
    if month != 'all':
        month = MONTH_DATA.index(month)

        df = df.loc[df['month'] == month]

    #filter by given day
    if day != 'all':

        df = df.loc[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("The most common month is: " + MONTH_DATA[common_month].title())

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("The most common day of week is: " + common_day)

    # display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print("The most common start hour is: " + str(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most common start station is: " + common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most common end station is: " + common_end_station)

    # display most frequent combination of start station and end station trip
    most_frequent_combination = (df['Start Station'] + "||" + df['End Station']).mode()[0]
     print("The most frequent combination of start station and end station is : " + str(most_frequent_combination.split("||")))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is: " + str(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is: " + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The count of user types is: \n" + str(user_types))

    # Display counts of gender
    if city == 'chicago.csv' or city == 'new_york_city.csv':
         gender = df['Gender'].value_counts()
        print("The count of user gender is: \n" + str(gender))

        # Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]
        print('Earliest birth is: {}\n'.format(earliest_birth))
        print('Most recent birth is: {}\n'.format(most_recent_birth))
        print('Most common birth is: {}\n'.format(most_common_birth) )


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays raw data when requested.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print(df.head())
    next = 0
    while True:
        raw_data = input('\nWould you like to view next five row? Enter yes or no.\n')
        if display_data.lower() != 'yes':
        break
    print(tabulate(df_default.iloc[np.arange(0+i,5+i)], headers ="keys"))
    i+=5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        while True:
            raw_data = input('\nWould you like to see the 1st five raws? Yes, No \n')
            if raw_data.lower() != 'yes':
                break
            pd.set_option('display.max_columns',200)
            display_raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
