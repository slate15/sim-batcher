import os
import subprocess
import time
import warnings

from ahk import AHK

from settings import *


# Global variables
# DSFL
DSFL_TEAMS = ("DAL", "KCC", "LDN", "MIN", "MBB", "NOR", "POR", "TIJ")

# Team list in exhibition game window
DSFL_TEAM_LIST = {
	"DAL": 0,
	"KCC": 1,
	"LDN": 2,
	"MIN": 3,
	"MBB": 4,
	"NOR": 5,
	"POR": 6,
	"TIJ": 7
}

# Team dropdown in "Teams" navigation menu
DSFL_TEAM_NAV = {
	"DAL": [1, 0],
	"MBB": [1, 1],
	"NOR": [1, 2],
	"TIJ": [1, 3],
	"KCC": [2, 0],
	"LDN": [2, 1],
	"MIN": [2, 2],
	"POR": [2, 3],
}

# ISFL
ISFL_TEAMS = ("ARI", "AUS", "BAL", "BER", "CHI", "COL", "HON", "NOL", "NYS", "OCO", "PHI", "SJS", "SAR", "YKW")

ISFL_TEAM_LIST = {
	"ARI": 0,
	"AUS": 1,
	"BAL": 2,
	"BER": 3,
	"CHI": 4,
	"COL": 5,
	"HON": 6,
	"NOL": 7,
	"NYS": 8,
	"OCO": 9,
	"PHI": 10,
	"SJS": 11,
	"SAR": 12,
	"YKW": 13
}

ISFL_TEAM_NAV = {
	"BAL": [1,0],
	"BER": [1,1],
	"CHI": [1,2],
	"COL": [1,3],
	"PHI": [1,4],
	"SAR": [1,5],
	"YKW": [1,6],
	"ARI": [2,0],
	"AUS": [2,1],
	"HON": [2,2],
	"NOR": [2,3],
	"NYS": [2,4],
	"OCO": [2,5],
	"SJS": [2,6],
}


# Starting in the DDSPF16 home screen (with league file loaded), change
# a specific team's strategy, save, and return to the DDSPF16 home screen
def changeTeamStrategy(ahk, team_code, command_list, save_strat=True):
	if not gameWindowExists(ahk):
		launchGame(ahk)

	ahk.run_script(createNavScript(team_code))

	time.sleep(0.2)

	ahk.click(STRATEGY_BUTTON_COORDINATES[0], STRATEGY_BUTTON_COORDINATES[1])

	pressedTabs = 0
	for command in command_list:
		numTabs = command[0]
		setting = command[1]
		title = command[2]
		if numTabs > pressedTabs:
			sendTabs = numTabs - pressedTabs
			for _ in range(sendTabs):
				ahk.send_input('{Tab}')

		if numTabs < pressedTabs:
			sendBackTabs = pressedTabs - numTabs
			for _ in range(sendBackTabs):
				ahk.send_input('+{Tab}')

		pressedTabs = numTabs

		if title.find("Playbook") > 0:
			ahk.send_input('{Up 7}')

			for _ in range(setting):
				ahk.key_press('Down')

		if title.find("Ratio") > 0:
			ahk.send_input('^a')
			ahk.send_input(str(setting))

	if gameWindowExists(ahk):
		time.sleep(0.5)
		ahk.click(SAVE_STRATEGY_COORDINATES[0], SAVE_STRATEGY_COORDINATES[1])
		time.sleep(1)
		ahk.send_input('!{F4}')
		time.sleep(0.2)
		if save_strat:
			ahk.send_input('^s')
			time.sleep(SAVE_BUFFER_DELAY)
		else:
			ahk.click(CLOSE_TEAM_COORDINATES[0], CLOSE_TEAM_COORDINATES[1])
			time.sleep(0.2)
			ahk.click(FOCUS_COORDINATES[0], FOCUS_COORDINATES[1])


# Force quit the DDSPF game window if things aren't working as expected
def closeGameWindow():
	os.system("taskkill /f /im \"Draft Day Sports - Pro Football 2016.exe\"")


# Create an autohotkey script that starts at the DDSPF main menu with league loaded
# and sets up an exhibition game between the specified home team and away team, then
# selects the "Sim Game" button
# In essence it takes you from home screen to ready to sim a game
def createExhibitionSetupScript(home_team_code, away_team_code):
	home_down_presses = -1
	away_down_presses = -1
	if home_team_code in DSFL_TEAMS and away_team_code in DSFL_TEAMS:
		home_down_presses = DSFL_TEAM_LIST[home_team_code]
		away_down_presses = DSFL_TEAM_LIST[away_team_code]
	elif home_team_code in ISFL_TEAMS and away_team_code in ISFL_TEAMS:
		home_down_presses = ISFL_TEAM_LIST[home_team_code]
		away_down_presses = ISFL_TEAM_LIST[away_team_code]
	else:
		raise ValueError("Both home and away team codes need to be valid for DSFL or ISFL together.")

	script = ""
	script += "Send !t\n" # Access Tasks menu
	script += "Send {Down 4}\n" # Navigate to Sim Exhibition Game
	script += "Send {Enter}\n" # Select Sim Exhibition Game
	script += "Send {Tab}\n" # Select home team

	if home_down_presses > 0:
		script += "Send {Down " + str(home_down_presses) + "}\n" # Navigate to home team within dropdown menu

	script += "Send {Tab}\n" # Select away team
	script += "Send {Up}\n" # Navigate to top of away team dropdown menu

	if away_down_presses > 0:
		script += "Send {Down " + str(away_down_presses) + "}\n" # Navigate to away team within dropdown menu

	script += "Send {Tab 2}" # Select "Sim Game"

	return script


# Create an autohotkey script that starts at the DDSPF main menu with league loaded
# and navigates to a team's home page from the "Teams" menu dropdown
def createNavScript(team_code):
	down_presses = [-1,-1]
	if team_code in DSFL_TEAMS:
		down_presses = DSFL_TEAM_NAV[team_code]
	elif team_code in ISFL_TEAMS:
		down_presses = ISFL_TEAM_NAV[team_code]
	else:
		raise ValueError("Team code specified was not a valid DSFL/ISFL team code.")

	script = ""
	script += "Send {LAlt down}\n" # Alt needs to be held down...
	script += "Send {t 2}\n" # so that pressing "t" twice navigates to Teams dropdown menu...
	script += "Send {LAlt up}\n" # and then can be released

	script += "Send {Down " + str(down_presses[0]) + "}\n" # Press down enough times to access the team's division
	script += "Send {Right}\n" # Press right to access the teams in that division
	if down_presses[1] > 0:
		script += "Send {Down " + str(down_presses[1]) + "}\n" # Press down to navigate to team within the division
	script += "Send {Enter}" # Select the team

	return script


# Starting in the DDSPF16 home screen (with league file loaded), navigate to
# configuration menu, enable personalities, and generate access/CSV files for simmed games
def exportSimFiles(ahk):
	script = """
	Send !o ; Access Configuration Menu
	Sleep 3000
	Click """ + "{}, {}".format(FOCUS_COORDINATES[0], FOCUS_COORDINATES[1]) + """ ; Activate window
	Send {Tab """ + "{}".format(ENABLE_PERSONALITIES_TABS) + """} ; Navigate to Enable Personalities
	Send {Space} ; Check Enable Personalities
	Send {Tab} ; Navigate to Save
	Send {Enter} ; Select Save
	Sleep 200
	Send {Enter} ; Dismiss MsgBox

	; Export sim files
	Send !f ; Access File Menu
	Send {Left """ + "{}".format(LEFT_PRESSES_TO_EXPORT) + """} ; Navigate to Export menu
	Send {Down} ; Navigate to Generate Access/CSV files
	Send {Enter} ; Select Generate Access/CSV files
	"""

	script += "\nSleep {}\n".format(EXPORT_BUFFER_DELAY*1000) # Autohotkey command "Sleep" takes millisecond argument
	script += "Send {Enter}"

	ahk.run_script(script)


# Finds the DDSPF window if it exists and brings it into focus
def focusGameWindow(ahk):
	win = ahk.find_window(title=b'Draft Day Sports: Pro Football 2016')
	win.activate()
	win.maximize()


# Checks whether there exists an open DDSPF game window
def gameWindowExists(ahk):
	win = ahk.find_window(title=b'Draft Day Sports: Pro Football 2016')
	return win is not None and win.exist


# Launches the game window if it does not currently exist, and loads the first league alphabetically
def launchGame(ahk, change_strategy=False, sim_games=False,
	strategy_args=None, sim_args=None):
	subprocess.Popen([GAME_APPLICATION_PATH,])
	time.sleep(LAUNCH_BUFFER_DELAY)

	focusGameWindow(ahk)
	reloadLeague(ahk)

	if change_strategy and strategy_args is not None:
		team_code = strategy_args[0]
		command_list = strategy_args[1]
		changeTeamStrategy(ahk, team_code, command_list)
	elif change_strategy:
		warnings.warn("No strategy arguments provided despite change_strategy=True on game relaunch", RuntimeWarning)

	if sim_games and sim_args is not None:
		home_team_code = sim_args[0]
		away_team_code = sim_args[1]
		N = sim_args[2]
		simExhibitionGames(ahk, home_team_code, away_team_code, N)
	elif sim_games:
		warnings.warn("No sim arguments provided despite sim_games=True on game relaunch", RuntimeWarning)


# Opens the first league listed alphabetically in the "File->Open" dropdown menu and waits for it to load
def reloadLeague(ahk):
	if gameWindowExists(ahk):
		script = """
		Send ^o ; Ctrl+O opens "Load League" menu
		Sleep 500
		Send {Tab 3} ; Navigate to league dropdown
		Send {Down} ; IMPORTANT: SIMMING LEAGUE MUST BE LISTED FIRST IN DROPDOWN
		Send {Tab 2} ; Navigate to continue
		Send {Enter} ; Press continue
		"""

		script += "\nSleep {}".format(LEAGUE_BUFFER_DELAY*1000) # Autohotkey command "sleep" takes millisecond arguments

		ahk.run_script(script)
	else:
		launchGame(ahk)


# Starting at the DDSPF home screen, with league loaded, runs the specified number of
# exhibition games between the home and away team provided, then closes the exhibition game window
def simExhibitionGames(ahk, home_team_code, away_team_code, N=100):
	ahk.run_script(createExhibitionSetupScript(home_team_code, away_team_code))

	for _ in range(N):
		ahk.send_input('{Space}') # Press "Sim Game"
		# print('.', end='', flush=True)
		time.sleep(SIM_BUFFER_DELAY)
		ahk.send_input('!{F4}') # Dismiss Game Detail window

	ahk.send_input('+{Tab}') # Select close
	ahk.send_input('{Enter}') # Press close