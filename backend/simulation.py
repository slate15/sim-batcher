import math
import time
import numpy as np
import pandas as pd

import settings
from backend.hotkeys import *
from backend.strategy import *
from backend.utils import *


# An object for interfacing between a single strategy setup to test (including both
# home & away strategies) and the simulation of that setup
class Simulation():
	# Initialize the Simulation object with the teams to simulate, their strategies,
	# and a flag to indicate whether a single strategy provided is for the home team
	#
	# team_codes: A string or tuple of length 1 or 2 giving the team codes to simulate
	#             (or the single team for which the strategy is provided)
	# strats: A single strategy.Strategy object or a tuple of length 1 or 2 containing
	#         strategy.Strategy objects, representing the strategies to implement for the
	#		  simulation test
	# title: A name for the strategy setup for this simulation test
	# home_team: If a single team code and strat is provided, this indicates whether those
	#            represent the home team code and strategy (True) or the away team (False)
	def __init__(self, team_codes, strats, title, home_team=True):
		# First check whether the team codes provided are a list or tuple
		iterable_team_codes = isinstance(team_codes, (list, tuple))

		# Assign team codes to the home and away team based on the parameters passed in
		self.home_team = None
		self.away_team = None
		if not iterable_team_codes or len(team_codes) == 1:
			# If only 1 team code is provided, assign it to the home team if the home_team
			# flag is True
			if home_team:
				# The team_codes could be a length 1 tuple/list
				self.home_team = team_codes if not iterable_team_codes else team_codes[0]
			else:
				self.away_team = team_codes if not iterable_team_codes else team_codes[0]
		else:
			# If two team codes are provided, the 1st is the home team and the 2nd is the
			# away team
			if len(strats) == 2:
				self.home_team = team_codes[0]
				self.away_team = team_codes[1]
			else:
				raise RuntimeError("More than 2 strategies provided to single simulation")

		# Next do the same for strategies
		iterable_strats = isinstance(strats, (list, tuple))

		self.home_strat = None
		self.away_strat = None
		if not iterable_strats or len(strats) == 1:
			if home_team:
				self.home_strat = strats if not iterable_strats else strats[0]
			else:
				self.away_strat = strats if not iterable_strats else strats[0]
		else:
			if len(strats) == 2:
				self.home_strat = strats[0]
				self.away_strat = strats[1]
			else:
				raise RuntimeError("More than 2 strategies provided to single simulation")

		self.title = title

	# Implement any strategies for the home and/or away teams in the game
	# Requires an autohotkey object to be passed in to implement the commands
	def initializeStrategies(self, ahk, save_file=True):
		if self.home_team is not None and self.home_strat is not None:
			changeTeamStrategy(ahk, self.home_team, self.home_strat.getTabCommands(), save_file)

		if self.away_team is not None and self.away_strat is not None:
			changeTeamStrategy(ahk, self.away_team, self.away_strat.getTabCommands(), save_file)

	# Simulate a specified number of games for this strategy
	#
	# ahk: An autohotkey object to implement the commands
	# N: the number of games to run, default 500
	# home_team: If no home team was specified when initializing the Simulation
	# 			 object, this argument can specify one. If a home team was specified,
	#			 this argument does nothing.
	# away_team: Likewise for the away team.
	def simulateGames(self, ahk, N=500, home_team=None, away_team=None):
		#
		if self.home_team is not None:
			home_team_code = self.home_team
		else:
			if home_team is not None:
				home_team_code = home_team
			else:
				raise RuntimeError("No home team provided in either Simulation __init__ " \
					"method or simulateGames arguments.")

		if self.away_team is not None:
			away_team_code = self.away_team
		else:
			if away_team is not None:
				away_team_code = away_team
			else:
				raise RuntimeError("No away team provided in either Simulation __init__ " \
					"method or simulateGames arguments.")

		# Check whether the game window exists before attempting to run games. If none is found,
		# first restart the game window, then re-initialize the strategies for this simulation
		# in case they were not saved before the game closed, then save the game file to include
		# these updated strategies.
		if not gameWindowExists(ahk):
			print("No game window was found to simulate games - attempting to restart game!")
			launchGame(ahk)

			print("Re-initializing strategies for simulating the games.")
			self.initializeStrategies(ahk)

			print("Done! Resuming sim tests.")

		simExhibitionGames(ahk, home_team_code, away_team_code, N)

# An object for managing a suite of simulation tests, including initializing the Simulation objects,
# running the simulations, and recording, reformatting, and outputting the combined data.
class SimulationManager():
	# Initialize the SimulationManager object.
	#
	# home_team: The team code for the home team in the tests.
	# away_team: The team code for the away team in the tests.
	# strats_list: A list of objects containing the Strategies to test. This can be a list of Strategy
	#			   objects, in which case the home_strats argument will inform whether they are strategies
	#			   for the home or away team (only the strategies for 1 team can be changed this way), or
	#			   it can be a list of tuples containing 2 strategies each, in which case it will be assumed
	#			   that the first strategy in the tuple is the home team's and the second is the away team's
	# title_list: A list of strings indicating the titles of the strategies to be tested. (In the case of both
	#			  home and away strategies being provided, still only 1 title is needed for each set of strategies.)
	# ahk: An autohotkey object to implement the commands
	# output_file: A filepath indicating where the combined output should be saved
	# num_iters: The number of games to simulate for each strategy, default 500
	# home_strats: If strats_list is a list of single Strategy objects to use for 1 team, this indicates whether
	#			   those objects represent strategies to be implemented for the home team (True) or away team (False)
	def __init__(self, home_team, away_team, strats_list, title_list, ahk,
		output_file, num_iters=500, home_strats=True):

		# Initialize a list to contain the Simulation objects to test
		self.simulations = list()

		# Iterate through the Strategy objects (or pairs of Strategy objects) and create
		# Simulation objects for each, using None to indicate there is no Strategy object
		# to implement in cases where only 1 is provided
		for idx, strat_spec in enumerate(strats_list):
			home_strat = None
			away_strat = None
			iterable_strats = isinstance(strat_spec, (list, tuple))
			if not iterable_strats:
				if home_strats:
					home_strat = strat_spec
				else:
					away_strat = strat_spec
			else:
				if len(strat_spec) == 2:
					home_strat = strat_spec[0]
					away_strat = strat_spec[1]
				else:
					raise RuntimeError("More than 2 strategies provided for single simulation " \
						"in strategy list passed to SimulationManager")

			sim = Simulation((home_team, away_team), (home_strat, away_strat), title_list[idx])

			# Append the Simulation object to the list of sims to test
			self.simulations.append(sim)

		self.ahk = ahk

		# More simmed games can be requested than the game can handle (as indicated
		# in the global variable MAX_ITERS). In this case, calculate how many times
		# the game will have to be reloaded to complete that many iterations, and
		# how many games to simulate on each reload
		if num_iters > settings.MAX_ITERS:
			self.reloads_per_strat = math.ceil(num_iters / settings.MAX_ITERS)
			self.iters_per_sim = round(num_iters / self.reloads_per_strat)
		else:
			self.reloads_per_strat = 1
			self.iters_per_sim = num_iters

		# Keep track of how many total games have been simmed, and how mnay have
		# been simmed since the last time the game was reloaded
		self.total_iters = 0
		self.iters_since_reload = 0

		self.output_file = output_file
		self.has_prev_output = False

		# Initialize the output file with an empty DataFrame so that it can be
		# loaded without issue
		dummy_game_data = pd.DataFrame()
		dummy_game_data.to_csv(self.output_file)


	# Create batches of simulations to test
	def generateSimBatches(self):
		batches = list()

		current_batch = list()
		current_batch_sims = 0
		for sim in self.simulations:
			remaining_sim_iters = self.iters_per_sim * self.reloads_per_strat

			while remaining_sim_iters > 0:
				current_batch.append(sim)
				remaining_sim_iters -= self.iters_per_sim
				current_batch_sims += self.iters_per_sim

				if current_batch_sims + self.iters_per_sim > settings.MAX_ITERS:
					batches.append(current_batch.copy())
					current_batch = list()
					current_batch_sims = 0

		if len(current_batch) > 0:
			batches.append(current_batch.copy())

		return batches


	# Conduct the simulations for all strategies to test
	def simulateAll(self):
		batches = self.generateSimBatches()
		prev_sim = None

		for batch in batches:
			batch_start_time = time.time()
			game_data_exists = False

			while not game_data_exists:
				for sim in batch:
					if prev_sim is None or sim.title != prev_sim.title:
						print("Initializing strategy: {}".format(sim.title))
						sim.initializeStrategies(self.ahk, self.iters_since_reload==0)
						# Since strategies have changed, the random seed being the same
						# as the previous batch is not a serious issue. So we can resync
						# the system time to the correct time to limit how far away it
						# drifts.
						resyncSystemTime()

					print("Simulating {} games for strategy {}".format(
						self.iters_per_sim, sim.title))
					sim.simulateGames(self.ahk, N=self.iters_per_sim)
					print("Complete!\n")

					self.total_iters += self.iters_per_sim
					self.iters_since_reload += self.iters_per_sim
					prev_sim = sim

					time.sleep(5)

				game_data_exists = self.reloadAndSave(batch, clear_cache=False)

			# If the next batch of sims starts within 214.75 seconds of the previous
			# batch, the random seed will be identical and duplicate results will
			# be obtained.
			# So we increment the system time in order to force a change in the
			# random seed and ensure no duplicate data is obtained.
			batch_end_time = time.time()
			time_skip = 220 - (batch_end_time - batch_start_time)
			assert np.isclose(batch_end_time - batch_start_time + time_skip, 220.0)
			print("Incrementing system time by {} seconds".format(time_skip))

			incrementSystemTime(time_skip)

		resyncSystemTime()


	# Export any data for games that have been run, then save that data into the output
	# file and reload the game window so that more sims can be run without crashing.
	# Returns True if the game data is successfully found and added to the output data.
	# Returns False otherwise.
	def reloadAndSave(self, sims_since_reset, clear_cache=True):
		print("\nExporting sim game data for the following sims:")
		for sim in sims_since_reset:
			print("  - {}".format(sim.title))

		exportSimFiles(self.ahk)
		print("Complete!\n")

		# Once the sim files have exported, add the data from those simmed games
		# into the complete output file.
		game_data_exists = self.updateGameData(sims_since_reset)

		# If no data was found from the game output, that means that exporting
		# failed somehow. In that case, unfortunately, the game will usually need
		# to be closed and restarted since the current state is hard to predict.
		if not game_data_exists:
			print("No game data found after export. Closing game window to reset from fresh state.")
			closeGameWindow()

		if gameWindowExists(self.ahk):
			focusGameWindow(self.ahk)

		print("\nReloading league file")

		reloadLeague(self.ahk)
		print("Complete!")

		if gameWindowExists(self.ahk):
			focusGameWindow(self.ahk)

		self.iters_since_reload = 0
		if clear_cache:
			sims_since_reset.clear()

		return game_data_exists

	# Handle the nitty-gritty of taking the output data from the simulated games and add
	# it to our consolidated output file.
	# Returns True if the process completes successfully, False otherwise.
	def updateGameData(self, sims_since_reset):
		try:
			all_game_data = pd.read_csv(settings.GAME_OUTPUT_FILE)
		except FileNotFoundError:
			return False
		simmed_game_data = all_game_data[all_game_data["GameType"] == "Exhibition"]
		simmed_game_data.reset_index(inplace=True)

		game_index = 0

		for sim in sims_since_reset:

			if "Strat" not in simmed_game_data.columns:
				simmed_game_data["Strat"] = pd.Series()

			simmed_game_data.loc[game_index:game_index+self.iters_per_sim, "Strat"] = sim.title

			title_components = sim.title.split(" ")
			if len(title_components) > 1:
				for idx, component in enumerate(title_components):
					subcomponents = component.split(".")
					if len(subcomponents) > 1:
						raise RuntimeError("Home/Away setting specification not yet supported")
					else:
						original_name = component.replace("_"," ").replace(" and ", " & ")
						colname = None
						if original_name in DOWN_DISTANCES:
							colname = "Down_Distance"
							value = component
						elif original_name in OFF_PLAYBOOK_OPTIONS:
							colname = "Off_Playbook"
							value = component
						elif original_name in DEF_PLAYBOOK_OPTIONS:
							colname = "Def_Playbook"
							value = component
						elif component.find("RP_") >= 0:
							colname = "Run_Pass_Ratio"
							value = component.replace("RP_","")
						elif component.find("Blitz_") >= 0:
							colname = "Blitz_Ratio"
							value = component.replace("Blitz_","")

						if colname is not None:
							if colname not in simmed_game_data.columns:
								simmed_game_data[colname] = pd.Series()

							simmed_game_data.loc[game_index:game_index+self.iters_per_sim, colname] = value

			game_index += self.iters_per_sim

		if not self.has_prev_output:
			simmed_game_data.to_csv(self.output_file, index=False)
			self.has_prev_output = True
		else:
			simmed_game_data.to_csv(self.output_file, mode='a', index=False, header=False)

		# game_data = pd.read_csv(self.output_file)
		# game_data = game_data.append(simmed_game_data, ignore_index=True, sort=False)
		# game_data.to_csv(self.output_file, index=False)

		print("Data output complete!")
		print("Data from {} games saved to {}".format(len(simmed_game_data), self.output_file))

		# Now that the data has been saved elsewhere, delete the game output file so that
		# a failure to simulate games can be identified in the future
		os.remove(settings.GAME_OUTPUT_FILE)

		return True