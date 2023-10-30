from math import radians, cos, sin, atan2, sqrt

def get_direction_and_distance(start_lat, start_lon, end_lat, end_lon):
    # convert decimal degrees to radians
    start_lat, start_lon, end_lat, end_lon = map(radians, [start_lat, start_lon, end_lat, end_lon])

    # haversine formula
    dlat = end_lat - start_lat 
    dlon = end_lon - start_lon 
    a = sin(dlat/2)**2 + cos(start_lat) * cos(end_lat) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a)) 
    distance = 6371 * c # radius of earth in km

    # bearing formula
    y = sin(end_lon - start_lon) * cos(end_lat)
    x = cos(start_lat) * sin(end_lat) - sin(start_lat) * cos(end_lat) * cos(end_lon - start_lon)
    bearing = atan2(y, x) * 180 / pi

    return (bearing, distance)

