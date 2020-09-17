from backend.strategyConstants import *


ALL_STRATEGIES = [
# The following is an example of 1 strategy that will be tested. It is a Python dictionary containing both the title (a string),
# and specifically formatted home/away strategies using a specific format and constants from backend/strategyConstants.py
{
	# Title must be provided for each strategy. If the titles are not unique they will be conflated in the statistical analysis.
	"Title": "All Power 30 & 3-4 50",
	# If you do not wish to specify a Home team strategy (i.e. leave it as-is in the league file), you can delete everything between the { and }
	# NOTE: Either all of the provided strategies need to have a home strategy specified, or none of them can have a home strategy specified. The same goes for away strategies.
	"Home": {
		FIRST_AND_TEN: (POWER_PLAYBOOK, 30, THREE_FOUR_PLAYBOOK, 50),
		FIRST_AND_SHORT: (POWER_PLAYBOOK, 30, THREE_FOUR_PLAYBOOK, 50),
		FIRST_AND_LONG: (POWER_PLAYBOOK, 30, THREE_FOUR_PLAYBOOK, 50),
		SECOND_AND_SHORT: (POWER_PLAYBOOK, 30, THREE_FOUR_PLAYBOOK, 50),
		SECOND_AND_LONG: (POWER_PLAYBOOK, 30, THREE_FOUR_PLAYBOOK, 50),
		THIRD_AND_SHORT: (POWER_PLAYBOOK, 30, THREE_FOUR_PLAYBOOK, 50),
		THIRD_AND_LONG: (POWER_PLAYBOOK, 30, THREE_FOUR_PLAYBOOK, 50),
		FOURTH_AND_SHORT: (POWER_PLAYBOOK, 30, THREE_FOUR_PLAYBOOK, 50),
		FOURTH_AND_LONG: (POWER_PLAYBOOK, 30, THREE_FOUR_PLAYBOOK, 50),
		GOAL_LINE: (POWER_PLAYBOOK, 30, THREE_FOUR_PLAYBOOK, 50),
		TWO_MIN_UP:  (POWER_PLAYBOOK, 30, THREE_FOUR_PLAYBOOK, 50),
		TWO_MIN_DOWN: (POWER_PLAYBOOK, 30, THREE_FOUR_PLAYBOOK, 50)
	},
	# If you do not wish to specify an Away team strategy (i.e. leave it as-is in the league file), you can delete everything between the { and }
	# As is done here
	"Away": {}
},
{
	"Title": "KCC vs MIN W13 Final",
	"Home": {
		FIRST_AND_TEN: (BALANCED_PLAYBOOK, 50, THREE_FOUR_PLAYBOOK, 50),
		FIRST_AND_SHORT: (POWER_PLAYBOOK, 30, NICKEL_PLAYBOOK, 35),
		FIRST_AND_LONG: (POWER_PLAYBOOK, 30, NICKEL_PLAYBOOK, 35),
		SECOND_AND_SHORT: (POWER_PLAYBOOK, 60, NICKEL_PLAYBOOK, 35),
		SECOND_AND_LONG: (WEST_COAST_PLAYBOOK, 40, NICKEL_PLAYBOOK, 35),
		THIRD_AND_SHORT: (POWER_PLAYBOOK, 30, THREE_FOUR_PLAYBOOK, 50),
		THIRD_AND_LONG: (VERTICAL_PLAYBOOK, 90, THREE_THREE_FIVE_PLAYBOOK, 50),
		FOURTH_AND_SHORT: (POWER_PLAYBOOK, 20, NICKEL_PLAYBOOK, 35),
		FOURTH_AND_LONG: (BALANCED_PLAYBOOK, 70, THREE_THREE_FIVE_PLAYBOOK, 50),
		GOAL_LINE: (WEST_COAST_PLAYBOOK, 30, NICKEL_PLAYBOOK, 35),
		TWO_MIN_UP:  (POWER_PLAYBOOK, 10, NICKEL_PLAYBOOK, 35),
		TWO_MIN_DOWN: (VERTICAL_PLAYBOOK, 100, THREE_FOUR_PLAYBOOK, 50),
	},
	"Away": {}
},
{
	"Title": "KCC vs MIN W13 1st&10 Spread 70",
	"Home": {
		FIRST_AND_TEN: (SPREAD_PLAYBOOK, 70, THREE_FOUR_PLAYBOOK, 50),
		FIRST_AND_SHORT: (POWER_PLAYBOOK, 30, NICKEL_PLAYBOOK, 35),
		FIRST_AND_LONG: (POWER_PLAYBOOK, 30, NICKEL_PLAYBOOK, 35),
		SECOND_AND_SHORT: (POWER_PLAYBOOK, 60, NICKEL_PLAYBOOK, 35),
		SECOND_AND_LONG: (WEST_COAST_PLAYBOOK, 40, NICKEL_PLAYBOOK, 35),
		THIRD_AND_SHORT: (POWER_PLAYBOOK, 30, THREE_FOUR_PLAYBOOK, 50),
		THIRD_AND_LONG: (VERTICAL_PLAYBOOK, 90, THREE_THREE_FIVE_PLAYBOOK, 50),
		FOURTH_AND_SHORT: (POWER_PLAYBOOK, 20, NICKEL_PLAYBOOK, 35),
		FOURTH_AND_LONG: (BALANCED_PLAYBOOK, 70, THREE_THREE_FIVE_PLAYBOOK, 50),
		GOAL_LINE: (WEST_COAST_PLAYBOOK, 30, NICKEL_PLAYBOOK, 35),
		TWO_MIN_UP:  (POWER_PLAYBOOK, 10, NICKEL_PLAYBOOK, 35),
		TWO_MIN_DOWN: (VERTICAL_PLAYBOOK, 100, THREE_FOUR_PLAYBOOK, 50),
	},
	"Away": {}
},
# Any number of other strategies can be added here by copy-pasting the above blocks & changing as needed
# Remember to include the comma between entries
]