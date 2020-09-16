import itertools

from backend.strategyConstants import *

# Utility function to check the format of a provided down&distance is valid and convert
# an integer index down-distance into a standard string format
def parse_down_distance(down_and_distance):
	if isinstance(down_and_distance, str):
		if down_and_distance in DOWN_DISTANCES:
			return down_and_distance
	elif isinstance(down_and_distance, int):
		if down_and_distance < len(DOWN_DISTANCES) and down_and_distance >= 0:
			return DOWN_DISTANCES[down_and_distance]

	raise ValueError("Down and distance must be specified as a string or integer")

# Utility function to check the format of a provided parameter value given the field
# for which it is intended.
# If field is OFF_PLAYBOOK or DEF_PLAYBOOK, the provided value can either be one of the
# possible options for that respective field or an integer index of those.
# If field is OFF_RATIO or DEF_RATIO, the provided value must be an integer between 1 and 100.
def parse_parameter_value(value, field):
	error_msg = None

	if field == OFF_PLAYBOOK:
		if isinstance(value, str):
			if value in OFF_PLAYBOOK_OPTIONS:
				return value
		elif isinstance(value, int):
			if value < len(OFF_PLAYBOOK_OPTIONS) and value >= 0:
				return OFF_PLAYBOOK_OPTIONS[value]
		error_msg = "Offense playbook parameter values must be a string or integer"

	elif field == DEF_PLAYBOOK:
		if isinstance(value, str):
			if value in DEF_PLAYBOOK_OPTIONS:
				return value
		elif isinstance(value ,int):
			if value < len(DEF_PLAYBOOK_OPTIONS) and value >= 0:
				return DEF_PLAYBOOK_OPTIONS[value]
		error_msg = "Defense playbook parameter values must be a string or integer"

	elif field == OFF_RATIO:
		if isinstance(value, int):
			if value >= 1 and value <= 100:
				return value
		error_msg = "Run/pass ratio parameter values must be an integer between 1 and 100"

	elif field == DEF_RATIO:
		if isinstance(value, int):
			if value >= 0 and value <= 100:
				return value
		error_msg = "Blitz ratio parameter values must be an integer between 1 and 100"

	raise ValueError(error_msg)


# An object to represent a Strategy as implemented in the Team's strategy tab in DDSPF 2016
class Strategy():
	# Initialize the Strategy object from a provided dictionary. The dictionary should be
	# in the format of:
	# {
	#  OFF_PLAYBOOK: {DOWN_DISTANCE: SETTING, ...},
	#  DEF_PLAYBOOK: {DOWN_DISTANCE: SETTING, ...},
	#  OFF_RATIO: {DOWN_DISTANCE: SETTING, ...},
	#  DEF_RATIO: {DOWN_DISTANCE: SETTING, ...}
	# }
	def __init__(self, strategy_dict=None):
		if strategy_dict is None:
			self.off_playbook = {}
			self.def_playbook = {}
			self.run_pass_ratio = {}
			self.blitz_ratio = {}
		else:
			assert len(strategy_dict.keys()) == 4
			for field in strategy_dict.keys():
				assert field in STRATEGY_FIELDS
				down_distance_dict = strategy_dict[field]

				parameter_dict = {}

				for dd_key in down_distance_dict:
					down_and_distance = parse_down_distance(dd_key)
					value = parse_parameter_value(down_distance_dict[dd_key], field)
					parameter_dict[down_and_distance] = value

				if field == OFF_PLAYBOOK:
					self.off_playbook = parameter_dict.copy()
				elif field == DEF_PLAYBOOK:
					self.def_playbook = parameter_dict.copy()
				elif field == OFF_RATIO:
					self.run_pass_ratio = parameter_dict.copy()
				elif field == DEF_RATIO:
					self.blitz_ratio = parameter_dict.copy()

	# Convert this Strategy into a list of tab commands to be
	# implemented, where each tab command contains the number
	# of tabs needed to reach the specified field, the setting
	# to be implemented at that field, and the type of field it is
	def getTabCommands(self):
		command_list = []

		for down_and_distance in self.off_playbook.keys():
			value = self.off_playbook[down_and_distance]

			tabs = OFF_PLAYBOOK_TABS[down_and_distance]
			setting = OFF_PLAYBOOK_DROPDOWN_TABS[value]
			command_list.append((tabs, setting, OFF_PLAYBOOK))

		for down_and_distance in self.def_playbook.keys():
			value = self.def_playbook[down_and_distance]

			tabs = DEF_PLAYBOOK_TABS[down_and_distance]
			setting = DEF_PLAYBOOK_DROPDOWN_TABS[value]
			command_list.append((tabs, setting, DEF_PLAYBOOK))

		for down_and_distance in self.run_pass_ratio.keys():
			setting = self.run_pass_ratio[down_and_distance]

			tabs = OFF_RATIO_TABS[down_and_distance]
			command_list.append((tabs, setting, OFF_RATIO))

		for down_and_distance in self.blitz_ratio.keys():
			setting = self.blitz_ratio[down_and_distance]

			tabs = DEF_RATIO_TABS[down_and_distance]
			command_list.append((tabs, setting, DEF_RATIO))

		# To speed up implementation, sort the tab commands
		# by the number of tabs needed rather than by the playbook
		command_list.sort(key=lambda x: x[0])

		return command_list

	# Check whether this strategy is valid given the ISFL rules
	def is_valid(self):
		valid = True
		for down_distance in DOWN_DISTANCES:
			if down_distance in self.def_playbook.keys() and down_distance in self.blitz_ratio.keys():
				def_pb = self.def_playbook[down_distance]
				def_rat = self.blitz_ratio[down_distance]

				if def_pb in (NICKEL_PLAYBOOK, FOUR_THREE_PLAYBOOK) and def_rat > 35:
					valid = False
				elif def_pb in (THREE_FOUR_PLAYBOOK, THREE_THREE_FIVE_PLAYBOOK) and def_rat > 50:
					valid = False
				elif def_pb == DIME_PLAYBOOK and def_rat > 20:
					valid = False
			
			if down_distance in self.off_playbook.keys() and down_distance in self.run_pass_ratio.keys():
				off_pb = self.off_playbook[down_distance]
				off_rat = self.run_pass_ratio[down_distance]

				if down_distance not in (THIRD_AND_LONG, FOURTH_AND_LONG, FOURTH_AND_SHORT, TWO_MIN_DOWN, TWO_MIN_UP) and \
					(off_rat > 70 or off_rat < 30):
					valid = False

		return valid

	# Return this playbook as a (large) string
	def __str__(self):
		output = ""
		for down_and_distance in DOWN_DISTANCES:
			output += down_and_distance
			if down_and_distance in self.off_playbook.keys():
				output += ":\t{}".format(self.off_playbook[down_and_distance])
			else:
				output += ":\tN/A"

			if down_and_distance in self.run_pass_ratio.keys():
				output += "\t{}".format(self.run_pass_ratio[down_and_distance])
			else:
				output += "\tN/A"

			if down_and_distance in self.def_playbook.keys():
				output += "\t|\t{}".format(self.def_playbook[down_and_distance])
			else:
				output += "\t|\tN/A"

			if down_and_distance in self.blitz_ratio.keys():
				output += "\t{}".format(self.blitz_ratio[down_and_distance])
			else:
				output += "\tN/A"

			output += "\n"

		return output