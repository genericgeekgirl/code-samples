import logging
import datetime
import re
import collections
import pytz
from django.db import connections

_logger = logging.getLogger(__name__)

def get_airports():

    with connections['flightsayer'].cursor() as cursor:

        airport_list = "('ATL', 'BOS', 'BWI', 'CLE', 'CLT', 'CVG', 'DCA', 'DEN', 'DFW', 'DTW', 'EWR', 'FLL', " \
                       "'HNL', 'IAD', 'IAH', 'JFK', 'LAS', 'LAX', 'LGA', 'MCO', 'MDW', 'MEM', 'MIA', 'MSP', " \
                       "'ORD', 'PDX', 'PHL', 'PHX', 'PIT', 'SAN', 'SEA', 'SFO', 'SLC', 'STL', 'TPA')"

        search_string = "select apt_cd, latitude, longitude, common_name, tz_name from airinfo.airports " \
                        "where apt_cd in %s or airport_rank = 0 order by apt_cd" % airport_list

        cursor.execute(search_string)

        return cursor.fetchall()


def get_metro_airports():
    """

    Returns: metro_areas mapping from a metro area to a list of airports, such as:
    {'CHI': ['ORD', 'MDW', 'RFD'], 'QMI': ['MIA', 'FLL', 'PBI'], 'NYC': ['JFK', 'EWR', 'LGA']}

    """
    search_string = """
    select near_airports.apt_cd, array_to_string(array_agg(airports.apt_cd), ', ')
    from airinfo.airports join airinfo.near_airports on (airports.apt_cd = near_airports.near_apt_cd)
    where near_airports.apt_cd in (select apt_cd from airinfo.airports where airport_rank = 0)
    group by near_airports.apt_cd
    """
    results = None
    with connections['flightsayer'].cursor() as cursor:
        cursor.execute(search_string)
        results = cursor.fetchall()

    if not results:
        _logger.error('Error getting metro areas for map. Using defaults')
        return {'CHI': ['ORD', 'MDW', 'RFD'], 'QMI': ['MIA', 'FLL', 'PBI'],
                'NYC': ['JFK', 'EWR', 'LGA'], 'WAS': ['IAD', 'DCA', 'BWI']}

    return {row[0]: row[1].split(', ') for row in results}


def setup_airport_color(iata_code, timestamp, mean_prob_ontime, num_flights):
    """
    Convert the prob of on time arrival to a value to use in the map. Intead of using the raw mean prob of on time
    flights, we add in 3 fake on time flights and re-calculate the interval. This is motivated by the Agresti-Coull
    interval for proportions (aka probabilities) where two success and two failures are added to get a nice
    confidence interval for proportions that works even with very small n
    (See http://www.stat.ufl.edu/~aa/articles/agresti_caffo_2000.pdf)

    Instead of adding two successes and two failures, we add three successes (on time flights). This way, for time
    periods with heavy traffic, the actual mean p0 isn't skewed much, but when there are only 1-2 flights in an interval,
    it means the prob on time is propped up.

    Args:
        iata_code: string
        timestamp: datetime object
        mean_prob_ontime: decimal
        num_flights: decomal

    Returns: a map of iata code, timestamp as a string, and color.
    """
    new_prob_ontime = (mean_prob_ontime * num_flights + 3) / (num_flights + 3)
    return {'iata': iata_code, 'time': str(timestamp), 'color': prob_to_color(new_prob_ontime)}


def get_delay_details(timezone, airports):
    """
    Args:
        timezone: name of timezone such as 'America/New_York'
        airports: a list of Airport objects

    Returns: a list of  (iata, local hour, avg p0, num flights) and today's datetime

    """
    today = datetime.datetime.now(pytz.timezone(timezone))
    if today.minute >= 30:
        today += datetime.timedelta(hours=1)
    today = today.replace(minute=0, second=0, microsecond=0)
    tomorrow = today + datetime.timedelta(hours=24)

    airports_string = "('" + "' , '".join([airport.iata for airport in airports]) + "')"

    with connections['flightsayer'].cursor() as cursor:
        search_string = "select apt_cd, hr_local, avg_p0, num_flts from flightsayer.apt_delay_arr " \
                        "where apt_cd in %s and hr_local between '%s' and '%s' " \
                        "order by apt_cd, hr_local" % (airports_string, today, tomorrow)

        cursor.execute(search_string)
        return cursor.fetchall(), today


class Airport():
    def __init__(self, airport_data):
        self.iata, lat, lon, self.name, self.timezone = airport_data
        self.lat = float(lat)
        self.lon = float(lon)

    def __repr__(self):
        return 'Airport %s' % self.iata


def get_airport_data(airports):
    """

    Args:
        airports: list of airport data, as output from get_airports()

    Returns:

    """
    airport_details = {}
    iata_to_airport = {}
    airports_by_timezone = {}

    for airport_data in airports:
        airport = Airport(airport_data)
        iata_to_airport[airport.iata] = airport

        if airport.timezone not in airports_by_timezone:
            airports_by_timezone[airport.timezone] = []
        airports_by_timezone[airport.timezone].append(airport)

    for timezone, airports in airports_by_timezone.items():
        delay_details, today = get_delay_details(timezone, airports)

        details = [setup_airport_color(*result) for result in delay_details]

        for airport in airports:
            airport_details[airport.iata] = collections.OrderedDict()
        for row in details:
            airport_details[row['iata']][row['time']] = row['color']
            airport_details[row['iata']]['start_time'] = today

    metro_areas = get_metro_airports()
    clustered_airports = []
    for metro_area, airports in metro_areas.items():
        clustered_airports.extend(airports)

    for iata in airport_details:
        airport_details[iata] = fill_in_gaps(airport_details[iata])

    for iata in airport_details:
        if iata not in clustered_airports:
            details = {}
            if iata in metro_areas:
                for apt_cd in metro_areas[iata]:
                    if apt_cd in airport_details:
                        details[apt_cd] = airport_details[apt_cd]
            else:
                details[iata] = airport_details[iata]
            airport_details[iata] = {}
            airport_details[iata]['risk'] = get_bubble_color(details)
            airport_details[iata]['airports'] = details

    airports = [x for x in iata_to_airport.values() if x not in clustered_airports]

    airport_data = [{'iata': airport.iata, 'latitude': airport.lat,
                     'longitude': airport.lon,
                     'name': airport.name,
                     'fillKey': airport_details[airport.iata]['risk'],
                     'highlightFillColor': 'fillKey',
                     'airports': airport_details[airport.iata]['airports']}
                    for airport in airports if airport.iata not in clustered_airports]
    return airport_data


def prob_to_color(prob):

    if prob >= 0.75:
        return 'low'
    elif prob >= 0.5:
        return 'medium'
    else:
        return 'high'


def get_bubble_color(details):
    colors = []

    for airport in details:
        values = list(details[airport].values())
        for value in values:
            colors.append(value[1])

    if 'high' in colors:
        return 'high'
    elif 'medium' in colors:
        return 'medium'
    else:
        return 'low'


def fill_in_gaps(details):
    new_details = collections.OrderedDict()

    start_time = ""

    for time, color in list(details.items()):
        if time == 'p0':
            continue
        elif time == 'start_time':
            start_time = color.hour
        else:
            time = re.sub(r"^\d{4}-\d{2}-\d{2}\s0?(\d*):\d{2}:\d{2}$", r"\1", time)
            new_details[int(time)] = color

    count = 0

    while count < 24:
        if count not in new_details:
            new_details[count] = 'low'
        count += 1

    new_details = collections.OrderedDict(sorted(list(new_details.items()), key=lambda t: t))

    start_of_list = collections.OrderedDict()
    end_of_list = collections.OrderedDict()

    for time, color in list(new_details.items()):

        if isinstance(start_time, int):
            if (time < start_time):
                end_of_list[time] = color
            else:
                start_of_list[time] = color

    new_details = start_of_list.copy()
    new_details.update(end_of_list)

    # because javascript doesn't understand ordered dictionaries and automatically sorts by key
    javascript_details = {}

    count = 0

    if new_details:
        while count < 24:
            (time, color) = new_details.popitem(last=False)
            if int(time) > 12:
                time = int(time) - 12
                time = str(time) + "PM"
            elif int(time) == 0:
                time = "Midnight"
            elif int(time) == 12:
                time = "Noon"
            else:
                time = str(time) + "AM"
            javascript_details[count] = [time, color]
            count += 1

    return javascript_details
