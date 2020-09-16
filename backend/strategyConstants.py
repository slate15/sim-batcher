# Strategy components
OFF_PLAYBOOK = "Offense Playbook"
DEF_PLAYBOOK = "Defense Playbook"
OFF_RATIO = "Run/Pass Ratio"
DEF_RATIO = "Blitz Ratio"

STRATEGY_FIELDS = (OFF_PLAYBOOK, DEF_PLAYBOOK, OFF_RATIO, DEF_RATIO)

# Offensive playbooks
DEFAULT_PLAYBOOK = "Default"
WEST_COAST_PLAYBOOK = "West Coast"
POWER_PLAYBOOK = "Power"
BALANCED_PLAYBOOK = "Balanced"
VERTICAL_PLAYBOOK = "Vertical"
SPREAD_PLAYBOOK = "Spread Offense"

OFF_PLAYBOOK_OPTIONS = (
	DEFAULT_PLAYBOOK,
	WEST_COAST_PLAYBOOK,
	POWER_PLAYBOOK,
	BALANCED_PLAYBOOK,
	VERTICAL_PLAYBOOK,
	SPREAD_PLAYBOOK
)

# Defensive playbooks
THREE_FOUR_PLAYBOOK = "3-4 Defense"
THREE_THREE_FIVE_PLAYBOOK = "3-3-5"
FOUR_THREE_PLAYBOOK = "4-3 Defense"
NICKEL_PLAYBOOK = "Nickel"
DIME_PLAYBOOK = "Dime"
TARGET_RUN_PLAYBOOK = "Target Run"
TARGET_MIXED_PLAYBOOK = "Target Mixed"
TARGET_PASS_PLAYBOOK = "Target Pass"

DEF_PLAYBOOK_OPTIONS = (
	THREE_FOUR_PLAYBOOK,
	THREE_THREE_FIVE_PLAYBOOK,
	FOUR_THREE_PLAYBOOK,
	NICKEL_PLAYBOOK,
	DIME_PLAYBOOK,
	TARGET_RUN_PLAYBOOK,
	TARGET_MIXED_PLAYBOOK,
	TARGET_PASS_PLAYBOOK
)

# Down and distances used for strategies
FIRST_AND_TEN = "1st & 10"
FIRST_AND_SHORT = "1st & short"
FIRST_AND_LONG = "1st & long"
SECOND_AND_SHORT = "2nd & short"
SECOND_AND_LONG = "2nd & long"
THIRD_AND_SHORT = "3rd & short"
THIRD_AND_LONG = "3rd & long"
FOURTH_AND_SHORT = "4th & short"
FOURTH_AND_LONG = "4th & long"
GOAL_LINE = "Goal line"
TWO_MIN_UP = "Last 2 min (ahead)"
TWO_MIN_DOWN = "Last 2 min (behind)"

DOWN_DISTANCES = (
	FIRST_AND_TEN,
	FIRST_AND_SHORT,
	FIRST_AND_LONG,
	SECOND_AND_SHORT,
	SECOND_AND_LONG,
	THIRD_AND_SHORT,
	THIRD_AND_LONG,
	FOURTH_AND_SHORT,
	FOURTH_AND_LONG,
	GOAL_LINE,
	TWO_MIN_UP,
	TWO_MIN_DOWN
)

# Number of tabs needed to access various fields from Strategy menu opening
OFF_PLAYBOOK_TABS = {
	"1st & 10": 2,
	"1st & short": 6,
	"1st & long": 10,
	"2nd & short": 13,
	"2nd & long": 18,
	"3rd & short": 22,
	"3rd & long": 25,
	"4th & short": 29,
	"4th & long": 33,
	"Goal line": 37,
	"Last 2 min (ahead)": 41,
	"Last 2 min (behind)": 45
}

OFF_PLAYBOOK_DROPDOWN_TABS = {
	DEFAULT_PLAYBOOK: 0,
	WEST_COAST_PLAYBOOK: 1,
	POWER_PLAYBOOK: 2,
	BALANCED_PLAYBOOK: 3,
	VERTICAL_PLAYBOOK: 4,
	SPREAD_PLAYBOOK: 5
}

DEF_PLAYBOOK_TABS = {
	"1st & 10": 1,
	"1st & short": 5,
	"1st & long": 9,
	"2nd & short": 14,
	"2nd & long": 17,
	"3rd & short": 21,
	"3rd & long": 26,
	"4th & short": 30,
	"4th & long": 34,
	"Goal line": 38,
	"Last 2 min (ahead)": 42,
	"Last 2 min (behind)": 46
}

DEF_PLAYBOOK_DROPDOWN_TABS = {
	THREE_FOUR_PLAYBOOK: 0,
	THREE_THREE_FIVE_PLAYBOOK: 1,
	FOUR_THREE_PLAYBOOK: 2,
	NICKEL_PLAYBOOK: 3,
	DIME_PLAYBOOK: 4,
	TARGET_RUN_PLAYBOOK: 5,
	TARGET_MIXED_PLAYBOOK: 6,
	TARGET_PASS_PLAYBOOK: 7
}

OFF_RATIO_TABS = {
	"1st & 10": 4,
	"1st & short": 8,
	"1st & long": 12,
	"2nd & short": 15,
	"2nd & long": 20,
	"3rd & short": 24,
	"3rd & long": 27,
	"4th & short": 31,
	"4th & long": 35,
	"Goal line": 39,
	"Last 2 min (ahead)": 43,
	"Last 2 min (behind)": 47
}

DEF_RATIO_TABS = {
	"1st & 10": 3,
	"1st & short": 7,
	"1st & long": 11,
	"2nd & short": 16,
	"2nd & long": 19,
	"3rd & short": 23,
	"3rd & long": 28,
	"4th & short": 32,
	"4th & long": 36,
	"Goal line": 40,
	"Last 2 min (ahead)": 44,
	"Last 2 min (behind)": 48
}
