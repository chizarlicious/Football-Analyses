#!/usr/bin/env python3

from math import sqrt
from os.path import isfile
from scipy.optimize import curve_fit
from sys import argv
import json
import matplotlib.pyplot as plt
import numpy as np


def binomial_error(M, N):
    """ Return the uncertainty on the ratio M/N assuming that there are N
    independent trials drawing from a binomial distribution with with
    probability p = M/N.

    For more information, see:
    http://www.pp.rhul.ac.uk/~cowan/stat/notes/efferr.pdf

    Args:
        M (int): The number of successful trials.
        N (int): The total number of trials.

    Returns:
        float: The uncertainty on the ratio M/N.
    """
    return sqrt(M * (1 - (M/N))) / N


def return_eff_err(win_temps, all_temps):
    eff = []
    err = []
    # We assume binomial error except for N=0,1, in which case we assume
    # Poisson
    for i in range(len(win_temps)):
        n_wins = win_temps[i]
        n_all = all_temps[i]

        if n_all == 0:
            eff.append(0)
            err.append(1)
        elif n_all == 1:
            eff.append(n_wins)
            err.append(1)
        else:
            ratio = n_wins / n_all
            eff.append(ratio)
            err.append(binomial_error(n_wins, n_all))

    return (eff, err)


def constant(x, a):
    return a


# Get the file list from the command line
files = [f for f in argv[1:] if isfile(f)]

# Run over the data and separate it into our sets
domes_data = {"all": [], "wins": []}
greenbay_data = {"all": [], "wins": [], "road loss": [], "all road": []}
outside_data = {"all": [], "wins": []}

for reco_file in files:
    with open(reco_file, "r") as open_file:
        json_obj = json.load(open_file)

        # Get the teams
        home_team = json_obj.get("home team")
        away_team = json_obj.get("away team")
        if home_team is None or away_team is None:
            continue

        # Get the venue
        venue_dict = json_obj.get("venue")
        if venue_dict is None:
            continue

        # Check if the game is in a Dome, and check if it's being played at
        # Greenbay
        is_dome = venue_dict.get("dome")
        is_greenbay = (home_team == "GB"
                       and venue_dict.get("stadium") == "Lambeau Field")

        # Get the temperature
        weather_dict = json_obj.get("weather")
        if weather_dict is None:
            continue
        temperature = weather_dict.get("temperature")
        wind_speed = weather_dict.get("windspeed")
        humidity = weather_dict.get("relative humidity")

        # Some of our data has bad temperature information, which we can tell
        # by the fact that it is all 0.
        bad_data = (temperature == 0 and wind_speed == 0 and humidity == 0)
        if temperature is None or bad_data:
            continue

        # Check if the home team wins
        plays_dict = json_obj.get("plays")
        if plays_dict is None:
            continue
        try:
            home_score = plays_dict[-1]["score"]["home"]
            away_score = plays_dict[-1]["score"]["away"]
        except:
            continue

        is_win = (home_score > away_score)

        # Pick the right place to store our temperature data
        if is_dome:
            target_dict = domes_data
        elif is_greenbay:
            target_dict = greenbay_data
        else:
            target_dict = outside_data

        # Save the temperature
        target_dict["all"].append(temperature)
        if is_win:
            target_dict["wins"].append(temperature)

        # Save loss information
        if away_team == "GB":
            greenbay_data["all road"].append(temperature)
            if is_win:  # The home team wins, not Greenbay
                greenbay_data["road loss"].append(temperature)

# Make the Plot

# Set up the bins for our histogram
bin_size = 10
left_edge = -10
right_edge = 80
bins = list(range(left_edge, right_edge+bin_size, bin_size))

# Histogram the data
domes_wins, bin_edges = np.histogram(domes_data["wins"], bins)
domes_all, bin_edges = np.histogram(domes_data["all"], bins)
domes_eff, domes_err = return_eff_err(domes_wins, domes_all)

greenbay_wins, bin_edges = np.histogram(greenbay_data["wins"], bins)
greenbay_all, bin_edges = np.histogram(greenbay_data["all"], bins)
greenbay_eff, greenbay_err = return_eff_err(greenbay_wins, greenbay_all)

outside_wins, bin_edges = np.histogram(outside_data["wins"], bins)
outside_all, bin_edges = np.histogram(outside_data["all"], bins)
outside_eff, outside_err = return_eff_err(outside_wins, outside_all)

# Get the bin centers
bin_centers = np.array((bin_edges[:-1] + bin_edges[1:])/2.)

# Correct for the Packer's strength by adjusting their away percentage to match
# the league
league_wins = len(domes_data["wins"]) + len(outside_data["wins"])
league_all = len(domes_data["all"]) + len(outside_data["all"])

# The away loss percentage is the same as the home win percentage
loss_percent = (league_wins / league_all)
greenbay_loss_percent = len(greenbay_data["road loss"]) / len(greenbay_data["all road"])
correction_factor = greenbay_loss_percent / loss_percent

corrected_greenbay_eff = correction_factor * np.array(greenbay_eff)

# Fit a constant to the Outdoors data
fit_params, _ = curve_fit(constant, bin_centers, outside_eff, p0=[0.57], sigma=outside_err)
const = fit_params[0]

# Make the plot
#plt.errorbar(bin_centers, domes_eff, fmt="o", yerr=domes_err, color="red", label="Domes")
plt.errorbar(bin_centers, greenbay_eff, fmt="o", capsize=5, yerr=greenbay_err, color="green", label="Greenbay", markersize=8)
plt.plot([left_edge, right_edge], [const] * 2, color="blue", linestyle="dashed", label="Other Teams (Fit {:.0%})".format(const), linewidth=2)
plt.errorbar(bin_centers, outside_eff, fmt="^", yerr=outside_err, color="blue", alpha=0.40, markersize=7)
plt.axis((left_edge, right_edge, 0, 1))
plt.xlabel('Temperature (F)')
plt.ylabel('Home Team Win Percentage')
plt.legend(numpoints=1)
plt.show()
