import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']



def _prompt_choice(prompt, valid_options):
    """
    Prompt helper to safely ask for a choice among valid options.

    Args:
        prompt (str): Message shown to the user.
        valid_options (list[str]): Accepted values (lowercase).

    Returns:
        str: The selected option (lowercase).
    """
    valid_set = set(valid_options)
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_set:
            return user_input
        print(f"Invalid input. Please choose one of: {', '.join(valid_options)}")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    print()

    city = _prompt_choice(
        "Please enter a city (chicago, new york city, washington):\n> ",
        list(CITY_DATA.keys()),
    )

    month = _prompt_choice(
        "Please enter a month (all, january, february, march, april, may, june):\n> ",
        MONTHS,
    )

    day = _prompt_choice(
        "Please enter a day of week (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday):\n> ",
        DAYS,
    )

    print("-" * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        city (str): name of the city to analyze
        month (str): name of the month to filter by, or "all"
        day (str): name of the day of week to filter by, or "all"

    Returns:
        pandas.DataFrame: city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # Create helpful columns for filtering/statistics
    df["month"] = df["Start Time"].dt.month              # 1-12
    df["day_of_week"] = df["Start Time"].dt.day_name()   # e.g., 'Monday'
    df["hour"] = df["Start Time"].dt.hour

    # Filter by month (if applicable)
    if month != "all":
        month_index = MONTHS.index(month)  # january -> 1, ..., june -> 6
        df = df[df["month"] == month_index]

    # Filter by day (if applicable)
    if day != "all":
        # Compare lowercased day names for safety
        df = df[df["day_of_week"].str.lower() == day]

    return df

        # safe mode helper to handle empty series when calculating mode

def _safe_mode(series):
    """
    Returns the most frequent value in a Series or None if empty.
    """
    if series.empty:
        return None
    return series.mode().iat[0]


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        print("-" * 40)
        return

    # Most common month
    common_month_num = _safe_mode(df["month"])
    common_month = MONTHS[common_month_num] if common_month_num is not None else None
    print(f"Most common month: {common_month}")

    # Most common day of week
    common_day = _safe_mode(df["day_of_week"])
    print(f"Most common day of week: {common_day}")

    # Most common start hour
    common_hour = _safe_mode(df["hour"])
    print(f"Most common start hour: {common_hour}:00")

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        print("-" * 40)
        return

    # Most commonly used start station
    common_start = _safe_mode(df["Start Station"])
    print(f"Most commonly used start station: {common_start}")

    # Most commonly used end station
    common_end = _safe_mode(df["End Station"])
    print(f"Most commonly used end station: {common_end}")

    # Most frequent combination of start station and end station trip
    combo = df.groupby(["Start Station", "End Station"]).size().sort_values(ascending=False)
    if combo.empty:
        print("Most frequent trip: Not available")
    else:
        most_common_trip = combo.index[0]
        trip_count = combo.iat[0]
        print(f"Most frequent trip: {most_common_trip[0]} -> {most_common_trip[1]} ({trip_count} trips)")

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        print("-" * 40)
        return

    # Total travel time
    total_duration = df["Trip Duration"].sum()
    print(f"Total travel time (seconds): {total_duration}")

    # Mean travel time
    mean_duration = df["Trip Duration"].mean()
    print(f"Mean travel time (seconds): {mean_duration:.2f}")

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")
    print("-" * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print("\nCalculating User Stats...\n")
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        print("-" * 40)
        return

    # Counts of user types
    if "User Type" in df.columns:
        print("Counts of user types:")
        print(df["User Type"].value_counts())
        print()
    else:
        print("User Type column not available.\n")

    # Counts of gender (not available for Washington in this dataset)
    if "Gender" in df.columns:
        print("Counts of gender:")
        print(df["Gender"].value_counts(dropna=False))
        print()
    else:
        print("Gender column not available for this city.\n")

    # Birth year stats (not available for Washington in this dataset)
    if "Birth Year" in df.columns:
        birth_years = df["Birth Year"].dropna()
        if birth_years.empty:
            print("Birth Year data is missing.\n")
        else:
            earliest = int(birth_years.min())
            most_recent = int(birth_years.max())
            most_common = int(birth_years.mode().iat[0])
            print(f"Earliest year of birth: {earliest}")
            print(f"Most recent year of birth: {most_recent}")
            print(f"Most common year of birth: {most_common}\n")
    else:
        print("Birth Year column not available for this city.\n")

    print(f"This took {time.time() - start_time:.4f} seconds.")
    print("-" * 40)


def display_raw_data(df):
    """
    Asks the user if they want to see raw data (5 rows at a time).
    """
    if df.empty:
        return

    start_loc = 0
    while True:
        show = input("\nWould you like to see 5 lines of raw data? Enter yes or no:\n> ").strip().lower()
        if show not in {"yes", "no"}:
            print("Please enter 'yes' or 'no'.")
            continue

        if show == "no":
            break

        end_loc = start_loc + 5
        print(df.iloc[start_loc:end_loc])
        start_loc = end_loc

        if start_loc >= len(df):
            print("\nNo more rows to display.")
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print("No trips match your filters. Try different filters.")
            print("-" * 40)
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n> ").strip().lower()
        if restart != "yes":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
