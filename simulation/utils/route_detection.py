import os
import pandas as pd
import numpy as np
from utils.cal import Calculation

def distance(a, b):
    return  np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def point_line_distance(point, start, end):
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
    """Reduces a series of points to a simplified version that loses detail, but
    maintains the general shape of the series.
    """
    dmax = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        d = point_line_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d

    if dmax >= epsilon:
        results = rdp(points[:index+1], epsilon)[:-1] + rdp(points[index:], epsilon)
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
    wp_lat = np.array(list(waypoints_coord_dict.values()))[:,0]
    wp_long = np.array(list(waypoints_coord_dict.values()))[:,1]
    for ats, waypoints in procedure_dict.items():
        # All waypoints in one procedure
        wp_list = np.empty([0,2])
        for wp in waypoints:
            wp_list = np.vstack((wp_list, waypoints_coord_dict[wp]))
        # Calculate total area between each segment and its cloest waypoint
        total_area = 0
        trajectory_in_area = np.empty([0,2])
        for i in range(len(simplified_trajectory)-1):
            # If the segment is within the procedure region
            if (simplified_trajectory[i][0] >= np.min(wp_lat)) & (simplified_trajectory[i][0] <= np.max(wp_lat)) & (simplified_trajectory[i][1] >= np.min(wp_long)) & (simplified_trajectory[i][1] <= np.max(wp_long)):
                trajectory_in_area = np.vstack((trajectory_in_area, simplified_trajectory[i], simplified_trajectory[i+1]))
                cross_dist = Calculation.cal_cross_track_distance(simplified_trajectory[i][0], simplified_trajectory[i][1], simplified_trajectory[i+1][0], simplified_trajectory[i+1][1], wp_list[:,0], wp_list[:,1])
                area = np.abs(Calculation.cal_great_circle_distance(simplified_trajectory[i][0], simplified_trajectory[i][1], simplified_trajectory[i+1][0], simplified_trajectory[i+1][1]) * cross_dist / 2.0)
                total_area += np.min(area)

        area_list.append(total_area)
        ats_list.append(ats)
        # print(ats, total_area)
    
    return ats_list[np.argmin(area_list)], trajectory_in_area