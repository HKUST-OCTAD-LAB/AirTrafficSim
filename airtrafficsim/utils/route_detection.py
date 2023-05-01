import numpy as np
from airtrafficsim.utils.calculation import Cal
from airtrafficsim.core.navigation import Nav


def distance(a, b):
    """
    Helper function to calculate distance between two points

    Parameters
    ----------
    a : [float, float]
        Lat, Long of point a [deg, deg]
    b : [float, float]
        Lat, Long of point b [deg, deg]

    Returns
    -------
    float
        Distance between two point
    """
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def point_line_distance(point, start, end):
    """
    Helper function to calculate distance between a point and a line

    Parameters
    ----------
    point : [float, float]
        Lat, Long of point a [deg, deg]
    start : [float, float]
        Lat, Long of the start point of the line [deg, deg]
    end : [float, float]
        Lat, Long of the end point of the line [deg, deg]

    Returns
    -------
    float
        Minimum distance between the point and the line
    """
    if (start == end).all():
        return distance(point, start)
    else:
        n = abs(
            (end[0] - start[0]) * (start[1] - point[1]) -
            (start[0] - point[0]) * (end[1] - start[1])
        )
        d = np.sqrt(
            (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
        )
        return n / d


def rdp(points, epsilon):
    """
    Reduces a series of points to a simplified version that loses detail, but
    maintains the general shape of the series.

    Parameters
    ----------
    points : float[lat, long]
        Trajectory points
    epsilon : float
        Maximum distance between the original line and the simplified line
    """
    dmax = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        d = point_line_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d

    if dmax >= epsilon:
        results = rdp(points[:index+1], epsilon)[:-1] + \
            rdp(points[index:], epsilon)
    else:
        results = [points[0], points[-1]]

    return results


def detect_sid_star(simplified_trajectory, procedure_dict, waypoints_coord_dict):
    """
    Detect SID and STAR

    Parameters
    ----------
    simplified_trajectory : float[lat, long]
        Simplified trajectory
    procedure_dict : dict
        Procedure dictionary
    waypoints_coord_dict : dict
        SID/STAR waypoint coordinate dictionary

    Returns
    -------
    SID/STAR : string
        Identified SID/STAR
    """
    area_list = []
    ats_list = []
    wp_lat = np.array(list(waypoints_coord_dict.values()))[:, 0]
    wp_long = np.array(list(waypoints_coord_dict.values()))[:, 1]
    for ats, waypoints in procedure_dict.items():
        # All waypoints in one procedure
        wp_list = np.empty([0, 2])
        for wp in waypoints:
            wp_list = np.vstack((wp_list, waypoints_coord_dict[wp]))
        # Calculate total area between each segment and its cloest waypoint
        total_area = 0
        trajectory_in_area = np.empty([0, 2])
        for i in range(len(simplified_trajectory)-1):
            # If the segment is within the procedure region
            if (simplified_trajectory[i][0] >= np.min(wp_lat)) & (simplified_trajectory[i][0] <= np.max(wp_lat)) & (simplified_trajectory[i][1] >= np.min(wp_long)) & (simplified_trajectory[i][1] <= np.max(wp_long)):
                trajectory_in_area = np.vstack(
                    (trajectory_in_area, simplified_trajectory[i], simplified_trajectory[i+1]))
                cross_dist = Cal.cal_cross_track_dist(
                    simplified_trajectory[i][0], simplified_trajectory[i][1], simplified_trajectory[i + 1][0], simplified_trajectory[i + 1][1], wp_list[:, 0], wp_list[:, 1])
                area = np.abs(Cal.cal_great_circle_dist(
                    simplified_trajectory[i][0], simplified_trajectory[i][1], simplified_trajectory[i + 1][0], simplified_trajectory[i + 1][1]) * cross_dist / 2.0)
                total_area += np.min(area)

        area_list.append(total_area)
        ats_list.append(ats)
        # print(ats, total_area)

    return ats_list[np.argmin(area_list)], trajectory_in_area


def get_arrival_data(airport, runway):
    """
    Get arrival data

    Parameters
    ----------
    airport : string
        Airport ICAO code
    runway : string
        Runway name

    Returns
    -------
    arrivals_dict : dict
        Arrival dictionary
    arrival_waypoints_coord_dict : dict
        Arrival waypoint coordinate dictionary
    """
    lat, long, _ = Nav.get_runway_coord(airport, runway)
    arrival_procedures = Nav.get_airport_procedures(airport, "STAR")
    # Get all arrival route and related waypoints
    arrival_waypoints = []
    arrivals_dict = {}
    for star in arrival_procedures:
        wp = Nav.get_procedure(airport, "", star)[0]
        wp = [ele for ele in wp if ele.strip()]
        arrival_waypoints.extend(wp)
        arrivals_dict[star] = wp
    arrival_waypoints = np.unique(arrival_waypoints)
    # Get coordinate of all arrival waypoints
    arrival_waypoints_coord_dict = {}
    for wp in arrival_waypoints:
        coord = Nav.get_wp_coord(wp, lat, long)
        arrival_waypoints_coord_dict[wp] = list(coord)

    return arrivals_dict, arrival_waypoints_coord_dict


def get_approach_data(airport, runway):
    """
    Get approach data

    Parameters
    ----------
    airport : string
        Airport ICAO code
    runway : string
        Runway name

    Returns
    -------
    approach_dict : dict
        Approach procedures dictionary
    approach_waypoints_coord_dict : dict
        Approach waypoint coordinate dictionary
    """
    lat, long, _ = Nav.get_runway_coord(airport, runway)
    approach_procedures = Nav.get_airport_procedures(airport, "APPCH")
    ils = [str for str in approach_procedures if "I" in str]
    ils_runway = [str.replace('I', '')
                  for str in approach_procedures if "I" in str]
    # Runway without ils
    missed_procedure = []
    for procedure in approach_procedures:
        hv_runway = [runway for runway in ils_runway if runway in procedure]
        if len(hv_runway) == 0:
            missed_procedure.append(procedure)
    approach_procedures = ils + missed_procedure
    # Get all approach route and related waypoints
    approach_waypoints = []
    approach_dict = {}
    for approach in approach_procedures:
        wp = Nav.get_procedure("VHHH", "", approach)[0]
        wp = [ele for ele in wp if ele.strip() and "RW" not in ele]
        approach_waypoints.extend(wp)
        approach_dict[approach] = wp
    approach_waypoints = np.unique(approach_waypoints)
    # Get coordinate of all approach waypoints
    approach_waypoints_coord_dict = {}
    for wp in approach_waypoints:
        coord = Nav.get_wp_coord(wp, lat, long)
        approach_waypoints_coord_dict[wp] = list(coord)
    return approach_dict, approach_waypoints_coord_dict
