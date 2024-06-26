from location.locationObj import Location
from datetime import datetime, timedelta
import re

# finds time in str
# matches 24 hour and 12 hour system
# returns datetime array of matches
def convertTime(str: str):
    pattern = r'\b((1[0-2]|0?[1-9]):([0-5][0-9]) ?([APap][Mm])|(2[0-3]|[01]?[0-9]):?[0-5][0-9])\b'
    matches = re.findall(pattern, str)
    
    result = []
    for match in matches:
        time_str = match[0]
        try:
            # Try parsing as 12-hour format with space before ampm
            result.append(datetime.strptime(time_str, "%I:%M %p"))
        except ValueError:
            try:
                # Try parsing as 12-hour format with no space before ampm
                result.append(datetime.strptime(time_str, "%I:%M%p"))
            except ValueError:
                try:
                    # Try parsing as 24-hour format with colon
                    result.append(datetime.strptime(time_str, "%H:%M"))
                except ValueError:
                    # Try parsing as 24-hour format without colon
                    result.append(datetime.strptime(time_str, "%H%M"))
    
    return result

# finds days in str, returns array of matches
def convertDay(str: str):
    pattern = r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b'
    matches = re.findall(pattern, str)
    
    result = [match for match in matches]
    
    return result

# function that filters locations based on their opening/closing time
# 'open': determine to filter based on opening or closing time
# 'early': determine to filter based on query mentioning "earliest" (true) or "latest" (false)
def findEarliestOrLatestStore(locations: list[Location], open: bool, early: bool):
    def adjust_closetime(opentime, closetime):
        if closetime <= opentime:
            closetime += timedelta(days=1)
        return closetime

    def get_relevant_time(times, open):
        opentime, closetime = times[0], times[1]
        closetime = adjust_closetime(opentime, closetime)
        return opentime if open else closetime

    curr = None
    filteredLocations = []

    for loc in locations:
        times = [convertTime(loc.getStandardTimes()), convertTime(loc.getSpecialTimes())]

        for time in times:
            if len(time) < 2:
                continue

            relevant_time = get_relevant_time(time, open)

            if curr is None:
                curr = relevant_time
                filteredLocations.append(loc.toJSON())
            else:
                if (early and relevant_time < curr) or (not early and relevant_time > curr):
                    curr = relevant_time
                    filteredLocations = [loc.toJSON()]
                    break
                elif relevant_time == curr:
                    filteredLocations.append(loc.toJSON())
                    break

    return filteredLocations

# function that filters locations based on their opening/closing time
# 'timestr': time to search for in operating hours
# 'open': determine to filter based on opening time or closing time
def findStoreSpecificTime(locations: list[Location], timestr: str, open: bool):
    curr = convertTime(timestr)[0]
    filteredLocations = []

    def get_relevant_time(times, open):
        return times[0] if open else times[1]

    for loc in locations:
        times = [convertTime(loc.getStandardTimes()), convertTime(loc.getSpecialTimes())]

        for time in times:
            if len(time) < 2:
                continue

            relevant_time = get_relevant_time(time, open)

            if relevant_time == curr:
                filteredLocations.append(loc.toJSON())
                break

    return filteredLocations

# function that filters locations based on the duration of their operating hours
# 'hours': specific duration in the query
# 'longshort': bool to determine if the query wants the longest/shortest operating hours instead of specific duration
# 'long': bool to determine if the query wants either the longest operating hours or shortest operating hours
def findStoreOperationalHours(locations: list[Location], hours: int, longshort=False, long=False):
    def adjust_closetime(opentime, closetime):
        if closetime <= opentime:
            closetime += timedelta(days=1)
        return closetime

    def calculate_operational_hours(times):
        opentime, closetime = times[0], times[1]
        closetime = adjust_closetime(opentime, closetime)
        return (closetime - opentime).total_seconds() / 3600

    curr = None
    filteredLocations = []

    for loc in locations:
        times = [convertTime(loc.getStandardTimes()), convertTime(loc.getSpecialTimes())]

        for time in times:
            if len(time) < 2:
                continue

            operational_hours = calculate_operational_hours(time)

            if not longshort:
                if operational_hours == hours:
                    filteredLocations.append(loc.toJSON())
                    break
            else:
                if curr is None:
                    curr = operational_hours
                    filteredLocations.append(loc.toJSON())
                else:
                    if (long and curr < operational_hours) or (not long and curr > operational_hours):
                        curr = operational_hours
                        filteredLocations = [loc.toJSON()]
                        break
                    elif curr == operational_hours:
                        filteredLocations.append(loc.toJSON())
                        break

    return filteredLocations

# function that filters locations based on whether or not they are open/closed on 'day'
# 'day': what day to look for
# 'open': determines if the query is asking for "open on day" (true) or "closed on day" (false)
def findOpenStoresOnDay(locations: list[Location], day: str, open: bool):
    def get_days_range(day):
        weekdays = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}
        weekends = {"Saturday", "Sunday"}
        if day.lower() == "weekdays":
            return weekdays
        elif day.lower() == "weekends":
            return weekends
        else:
            if day[-1] == 's':
                print(day[:-1].capitalize())
                return {day[:-1].capitalize()}
            return {day.capitalize()}

    def expand_day_range(first_day, last_day):
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        start_index = day_order.index(first_day)
        end_index = day_order.index(last_day)
        if start_index <= end_index:
            return set(day_order[start_index:end_index + 1])
        else:
            return set(day_order[start_index:] + day_order[:end_index + 1])

    def is_store_open_on_day(opendays, day_set):
        return any(day in opendays for day in day_set)

    day_set = get_days_range(day)
    filteredLocations = []

    for loc in locations:
        times = [convertDay(loc.getStandardTimes()), convertDay(loc.getSpecialTimes())]

        for days in times:
            if len(days) == 0:
                continue

            if len(days) == 2:
                firstDay, lastDay = days[0], days[1]
                opendays = expand_day_range(firstDay, lastDay)
            elif len(days) == 1:
                firstDay = days[0]
                opendays = expand_day_range(firstDay, firstDay)

            if open and is_store_open_on_day(opendays, day_set):
                filteredLocations.append(loc.toJSON())
                break
            elif not open and not is_store_open_on_day(opendays, day_set):
                filteredLocations.append(loc.toJSON())
            elif not open and is_store_open_on_day(opendays, day_set):
                try:
                    filteredLocations.remove(loc.toJSON())
                except ValueError:
                    pass
                finally:
                    break

    return filteredLocations