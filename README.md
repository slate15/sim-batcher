# sim-batcher
 Python package used to automate large batch tests for DDSPF 2016

## Quick Setup Guide
Requires:
* Python 3
* DDSPF 2016
* AutoHotKey

1. Download this code as a .ZIP file and extract it to a directory
2. Open the Command Prompt (cmd.exe) **as administrator** and navigate to that directory ("cd \<directory\>")
3. Run `pip install -r requirements.txt --user`
4. Open up the settings.py file in the text editor / IDE of your choice and change the filepaths as needed
5. Open DDSPF and load the league you want to use (DSFL only at present)
6. Launch utils/MousePosWatch.ank.ahk script, press Ctrl-J to start it, and use it to identify the mouse coordinates needed for settings.py (Press Esc to exit the MousePosWatch script)
7. In the Command Prompt, run `python batchtest.py input/exampleStrats.py --home KCC --away MIN -N 50` (or you can use any other team codes you want for home/away)
8. Message me on Discord if you have any issues to this point. Otherwise start defining your own strategies and running your own sim tests!

## Introduction

sim-batcher is a Python 3 package that allows for large-scale batch testing of multiple strategies in DDSPF 2016. The general way that it works is through a combination of the Python [autohotkey package](https://github.com/spyoungtech/ahk) and custom Python code that allows for representations of strategies as Python objects and interfaces with the simulator.

To run a batch of tests, the main command that is used is:

`python batchtest.py [STRATEGY_FILEPATH] -H [HOME_TEAM_CODE] -A [AWAY_TEAM_CODE] -N [NUM_TESTS] -O [OUTPUT_FILEPATH]`

What this does is:

1. Read in the Strategies defined at STRATEGY_FILEPATH and convert them into Python objects
2. Simulate a number of games equal to NUM_TESTS between the specified teams
3. Record the data to OUTPUT_FILEPATH (this is done as tests are ongoing, so if the sim tests are interrupted for some reason the output for the completed tests will still be saved there)
4. Displays summary statistics for each strategy used upon completion of all the tests

Note: The -N and -O arguments are optional. The default number of tests per strategy is 500 and the default output filepath is "output/Results.csv".

## Configuration

This code is written for Python 3 and requires a copy of DDSPF 2016 to run (so it can simulate the games). This code requires the Python packages [ahk](https://github.com/spyoungtech/ahk), numpy, and pandas.

The settings.py file contains most of the parameters that should remain the same across runs. These include:

1. GAME_APPLICATION_PATH, the filepath of the DDSPF .exe application file.
2. GAME_OUTPUT_FILE, the filepath of the Games.csv file for the league **IMPORTANT: The league must be listed first alphabetically in the game's dropdown menu for it to be reloaded upon hitting the maximum games simulated for one batch of tests.**
3. RESULTS_FILE, the target .csv filepath to save the game output to. (Can optionally be specified here, but is overridden by the -O flag in the command line execution)
4. MAX_ITERS, an upper bound on the number of games that can be run on one league load without the game crashing
5. Some coordinates for specific buttons in the game window. Since not everything can be accessed via keyboard shortcuts, several mouse clicks are needed throughout the simulation loop.

These coordinates may change depending on screen size, resolution, etc. The provided autohotkey script "MousePosWatch.ank.ahk" in the utils/ folder can be used to find the x- and y- values for each button for your specific setup. With AutoHotkey installed, simply launch the script by double-clicking the file, press Ctrl-J to start the mouse tooltip, record the coordinates specified in the comments, and press Esc to exit the script once you're done.

6. Delay settings. Sometimes the DDSPF window is doing some stuff and needs time. These settings specify how long the code waits for those tasks to finish.
