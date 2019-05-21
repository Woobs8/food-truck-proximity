import pytest
from application.haversine import haversine


def test_haversine():
    """
    Test that the haversine function returns the correct distance.

    The test must account for tolerable inaccuracies in the calculation
    of the distance that occur as a result of several factors:
    - floating point approximations
    - approximation of earth radius

    Becaue of this, 1% deviation from the expected result is tolerated.

    1. Invoke haversine for coordinates with known distance
    2. Verify the returned distance
    """
    # Test for polar coordinates
    coord1 = (80.5025, -1.9076)
    coord2 = (79.59, 33.3556)
    known_dist_m = 674412
    calc_dist_m = haversine(coord1[0], coord1[1], coord2[0], coord2[1])

    # verify that result is within tolerance of expected result
    tolerance = known_dist_m*0.01
    assert calc_dist_m <= known_dist_m + tolerance and calc_dist_m >= known_dist_m - tolerance


    # test for equatorial coordinates
    coord1 = (0.034, -61.5828)
    coord2 = (-1.2814, -57.8707)
    known_dist_m = 437884
    calc_dist_m = haversine(coord1[0], coord1[1], coord2[0], coord2[1])

    # verify that result is within tolerance of expected result
    tolerance = known_dist_m*0.01
    assert calc_dist_m <= known_dist_m + tolerance and calc_dist_m >= known_dist_m - tolerance