import datetime
import os
import win32api as win

from backend.strategy import *
from backend.strategyConstants import OFF_PLAYBOOK, DEF_PLAYBOOK, OFF_RATIO, DEF_RATIO

# Take a list of strategy dictionaries as formatted in ../testStrats.py and
# parse into a usable format for batch testing.
# Arguments:
# - test_strat_list: A list of strategy dictionaries formatted as {"Title": "X", "Home": {home_strat}, "Away": {away_strat}}
# Returns:
# - strategies: A list of strategy inputs for a SimulationManager, either tuples of (home_strat, away_strat) if both are provided or
#				just single strategies if only one is provided
# - titles: A list of titles for each strategy provided
# - home_strats: If only one of home/away strategies are provided, this indicates whether the single strategies returned are for the
#				 home team (True) or away team (False)
def parseStrategyInput(test_strat_list):
	strategies = list()

	titles = [spec["Title"] for spec in test_strat_list]

	home_strats = [spec["Home"] for spec in test_strat_list]
	away_strats = [spec["Away"] for spec in test_strat_list]

	has_home_strats = any([len(strat) > 0 for strat in home_strats])
	has_away_strats = any([len(strat) > 0 for strat in away_strats])

	if has_home_strats:
		try:
			assert all([len(strat)>0 for strat in home_strats])
		except AssertionError:
			raise ValueError("Either all or none of the strategies provided can have home strategies specified.")
	else:
		try:
			assert all([len(strat)==0 for strat in home_strats])
		except AssertionError:
			raise ValueError("Either all or none of the strategies provided can have home strategies specified.")

	if has_away_strats:
		try:
			assert all([len(strat)>0 for strat in away_strats])
		except AssertionError:
			raise ValueError("Either all or none of the strategies provided can have away strategies specified.")
	else:
		try:
			assert all([len(strat)==0 for strat in away_strats])
		except AssertionError:
			raise ValueError("Either all or none of the strategies provided can have away strategies specified.")

	if has_home_strats and has_away_strats:
		combined_strats = [(Strategy(transformStratDict(spec["Home"])), Strategy(transformStratDict(spec["Away"]))) for spec in test_strat_list]

		return combined_strats, titles, None

	elif has_home_strats:
		transformed_home_strats = [Strategy(transformStratDict(strat)) for strat in home_strats]

		return transformed_home_strats, titles, True

	else:
		transformed_away_strats = [Strategy(transformStratDict(strat)) for strat in away_strats]

		return transformed_away_strats, titles, False


# Transform a strategy dict from the format used in the game to the format used in Strategy objects
def transformStratDict(strategy_dict):
	transformed_strat_dict = {
		OFF_PLAYBOOK: {down_distance: strategy_dict[down_distance][0] for down_distance in strategy_dict.keys()},
		OFF_RATIO: {down_distance: strategy_dict[down_distance][1] for down_distance in strategy_dict.keys()},
		DEF_PLAYBOOK: {down_distance: strategy_dict[down_distance][2] for down_distance in strategy_dict.keys()},
		DEF_RATIO: {down_distance: strategy_dict[down_distance][3] for down_distance in strategy_dict.keys()},
	}

	return transformed_strat_dict

# Add a specified number of seconds to the current system time
def incrementSystemTime(secs):
	current = win.GetSystemTime()
	# win.getSystemTime() returns a tuple with day of week as the 3rd element of the tuple, which is extraneous
	# for the python datetime package
	T = datetime.datetime(*(current[:2] + current[3:]))

	delta = datetime.timedelta(0, secs)
	T_prime = T + delta
	day_of_week = T_prime.isocalendar()[2]
	T_tuple = tuple(T_prime.timetuple())
	# Create a new tuple to use to set windows time from the Python datetime objects
	future = T_tuple[:2] + (day_of_week,) + T_tuple[2:7]

	T_new = win.SetSystemTime(*future)

	return T_new


# Forces the command line to resync system time
def resyncSystemTime():
	os.system("w32tm /resync /force")