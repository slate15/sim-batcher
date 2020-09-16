import argparse
import importlib
import warnings

import numpy as np
import pandas as pd

import settings
from backend.analysis import *
from backend.hotkeys import *
from backend.simulation import *
from backend.strategy import *
from backend.utils import *


def main():
	parser = argparse.ArgumentParser(description="Run a batch sim test.")
	parser.add_argument('strat_file', metavar="STRATEGY_FILEPATH", type=str,
						help="The filepath of the file containing the strategies to be used (Omit the .py extension).")
	parser.add_argument('-H', '--home', metavar="HOME_TEAM_CODE", type=str, required=True,
						help="The three-letter code for the home team")
	parser.add_argument('-A', '--away', metavar="AWAY_TEAM_CODE", type=str, required=True,
						help="The three-letter code for the away team")
	parser.add_argument("-N", metavar="SAMPLE_SIZE", type=int, default=500,
						help="The number of iterations to run for each strategy")
	parser.add_argument("-O", "--output", metavar="OUTPUT_FILEPATH", type=str,
						help="The file where the output data will be stored. Can also be set in settings.py")

	args = parser.parse_args()

	try:
		strat_module = importlib.import_module(args.strat_file)
		strats_to_test = strat_module.ALL_STRATEGIES
	except ModuleNotFoundError:
		raise FileNotFoundError("No file found containing strategies at {}.py".format(args.strat_file))
	except AttributeError:
		raise ValueError("Batch testing expected a dictionary named ALL_STRATEGIES in {}.py but none was found".format(args.strat_file))

	strat_list, title_list, home_strats = parseStrategyInput(strats_to_test)

	output_file = None
	if args.output is not None:
		output_file = args.output
	else:
		try:
			output_file = settings.RESULTS_FILE
		except AttributeError:
			raise ValueError("Results file must be specified with either -O/--output command line argument or as RESULTS_FILE in settings.py")

	ahk = AHK()

	print("Full list of strategies to test:\n - ", end = '')
	print("\n - ".join(title_list))
	print("\nTOTAL STRATS: {} strategies to test".format(len(title_list)))
	print("TOTAL SIMS: {} games".format(len(title_list) * args.N))
	print("\n-----------------\n")

	focusGameWindow(ahk)

	sim_manager = SimulationManager(args.home, args.away, strat_list, title_list,
		ahk, output_file, num_iters=args.N, home_strats=home_strats)

	sim_manager.simulateAll()

	analyzeBatchOutput(output_file, title_list, home_strats)

if __name__=="__main__":
	warnings.filterwarnings("ignore")
	main()