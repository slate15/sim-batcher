# FILEPATHS

# The path to the game application .exe
GAME_APPLICATION_PATH = "C:/Program Files (x86)/Wolverine Studios/Draft Day Sports - Pro Football 2016/Draft Day Sports - Pro Football 2016.exe"

# The path to the game output file for the simulated games for the league being tested
# IMPORTANT: The league must be the first alphabetically in the dropdown list that appears in File -> Open
GAME_OUTPUT_FILE = "C:/Users/<Username>/Documents/DDSPF/Leagues/<League Name>/Output/<League Name>_Games.csv"
# The path where you would like the combined output of all tests run to be saved to, can be overwritten with the -O command line flag
RESULTS_FILE = "output/Results.csv"

# GAME SETTINGS

MAX_ITERS = 701 # Maximum iterations your game can run without crashing between reloading the league file

ENABLE_PERSONALITIES_TABS = 16 # How many tabs are needed to get to the "Enable Personalities" box in the Configuration page. Sometimes 16, sometimes 17 apparently.
LEFT_PRESSES_TO_EXPORT = 3 # How many left button presses are needed to get to the "Export" menu from the "File" dropdown

# Below are the (x, y) coordinates for various buttons on the screen, needed to ensure that the program will click the right things.
# These can be found using the utils/MousePosWatch.ahk script (requires installing AutoHotkey)

# Focus coordinates are some points within the game window to click to ensure the window is focused.
# Best to make sure they are away from any buttons or anything in the Configuration menu screen.
FOCUS_COORDINATES = (8, 100)
# Strategy button coordinates are the coordinates of the "Strategy" button on the team page (that brings up the playbook settings, tempo, etc.)
STRATEGY_BUTTON_COORDINATES = (375, 120)
# Save strategy coordinates are the coordinates of the "Save" button in that strategy pop-up window
SAVE_STRATEGY_COORDINATES = (1200, 250)
# Close team coordinates are the coordinates of the "X" button that navigates from the Team homepage to the DDSPF home screen
CLOSE_TEAM_COORDINATES = (1900, 60)


# BUFFER_SETTINGS

# All times are in seconds

# Export buffer is the time that the program will wait for the game to finish generating the CSV files for the simulated games
# If this is set too short, the output Games.csv will not have enough time to be made before the program tries to read data from it
EXPORT_BUFFER_DELAY = 40
# Launch buffer is the time that the program will wait for the game to open if it needs to be relaunched after crashing
LAUNCH_BUFFER_DELAY = 15
# League buffer is the time that the program will wait for the game to load the league file
LEAGUE_BUFFER_DELAY = 18
# Save buffer is the time that the program will wait for the game to save any changes made to the league file (i.e. strategy settings)
SAVE_BUFFER_DELAY = 3
# Sim buffer is the time in between simulated games
SIM_BUFFER_DELAY = 0.02
