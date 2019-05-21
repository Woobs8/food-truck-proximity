import math

def haversine(lat1, long1, lat2, long2, math=math):
    """
    This function uses the haversine formula to calculate the great-circle distance 
    between two coordinates. The function includes an option for specifying the
    module used for math operations.

    Parameters:
        lat1 (float): latitude of first coordinate in decimal format
        lon1 (float): longitude of first coordinate in decimal format
        lat2 (float): latitude of second coordinate in decimal format
        lon2 (float): longitude of second coordinate in decimal format
        math (module): a module that implements the math functions 
        cos(), acos(), sin(), asin(), radians(), pow() and sqrt()

    Returns:
        float: distance between the two coordinates
    """
    # convert decimal degrees to radians 
    lat1, long1, lat2, long2 = map(math.radians, [lat1, long1, lat2, long2])

    # haversine formula 
    a = math.pow(math.sin((lat2 - lat1)/2), 2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin((long2 - long1)/2), 2)
    c = 2 * math.asin(math.sqrt(a))
    R = 6378*1000 # earth mean radius (m)
    return c * R