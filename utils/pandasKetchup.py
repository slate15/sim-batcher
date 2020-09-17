import warnings

import numpy as np
import pandas as pd

# Parameters
file_path = "../output/Results.csv"
team_to_test = "Home"


warnings.filterwarnings("ignore")

# Load file
X = pd.read_csv(file_path)
X["HomeWin"] = X["HomeScore"] > X["AwayScore"]

# Build list of strats
strat_data = list()
strat_names = X["Strat"].unique()
for strat in strat_names:
	strat_data.append(X[X["Strat"] == strat].reset_index())

for i, df in enumerate(strat_data):
	home_win_pct = sum(df["HomeWin"]) / len(df)
	home_win_err = np.sqrt(home_win_pct * (1-home_win_pct) / len(df))
	home_avg_top = np.mean(df["HomeTOP"])
	away_avg_top = np.mean(df["AwayTOP"])
	home_avg_pts = np.mean(df["HomeScore"])
	away_avg_pts = np.mean(df["AwayScore"])
	home_avg_ryd = np.mean(df["HomeRushYds"])
	home_avg_pyd = np.mean(df["HomePassYds"])
	away_avg_ryd = np.mean(df["AwayRushYds"])
	away_avg_pyd = np.mean(df["AwayPassYds"])
	home_avg_3dp = np.mean(df["Home3rdDownComp"]) / np.mean(df["Home3rdDownAtt"])
	home_tot_3da = int(np.sum(df["Home3rdDownAtt"]))
	home_tot_3dc = int(np.sum(df["Home3rdDownComp"]))
	away_avg_3dp = np.mean(df["Away3rdDownComp"]) / np.mean(df["Away3rdDownAtt"])
	away_tot_3da = int(np.sum(df["Away3rdDownAtt"]))
	away_tot_3dc = int(np.sum(df["Away3rdDownComp"]))
	home_avg_tos = np.mean(df["AwayInt"]) + np.mean(df["HomeFumblesLost"])
	away_avg_tos = np.mean(df["HomeInt"]) + np.mean(df["AwayFumblesLost"])
	home_avg_pen = np.mean(df["HomePenalties"])
	away_avg_pen = np.mean(df["AwayPenalties"])

	#Output results of Strat
	print("\nStrategy #{}".format(i+1))
	print(df.loc[0, "Strat"])
	print("N = {}\n".format(len(df)))

	if team_to_test == "Home":

		print("Win Percentage: {:.2f}%".format(100*home_win_pct))
		print("    90% Confidence Interval: ({:.2f}%, {:.2f}%)".format(100*(home_win_pct - (1.645*home_win_err)), 100*(home_win_pct + (1.645 * home_win_err))))
		print("Points Scored: {:.2f}".format(home_avg_pts))		

		print("Points Against: {:.2f}".format(away_avg_pts))
		print("Rushing Yards: {:.2f}".format(home_avg_ryd))
		print("Passing Yards: {:.2f}".format(home_avg_pyd))

		top_min = int(np.floor(home_avg_top / 60))
		top_sec = int(np.around(home_avg_top - (top_min * 60)))
		if top_sec < 10:
			top_sec = "0" + str(top_sec)
		print("Time Of Possession: {}:{}".format(top_min, top_sec))

		print("Third Down Conversion Rate: {:.2f}% ({} / {})".format(100*home_avg_3dp, home_tot_3dc, home_tot_3da))

		print("Rushing Yards Against: {:.2f}".format(away_avg_ryd))
		print("Passing Yards Against: {:.2f}".format(away_avg_pyd))

		print("Penalties: {:.2f}".format(home_avg_pen))

	else:

		print("Win Percentage: {:.2f}%".format(100*(1-home_win_pct)))
		print("    90% Confidence Interval: ({:.2f}%, {:.2f}%)".format(100*((1-home_win_pct) - (1.645*home_win_err)), 100*((1-home_win_pct) + (1.645 * home_win_err))))
		print("Points Scored: {:.2f}".format(away_avg_pts))
		print("Points Against: {:.2f}".format(home_avg_pts))
		print("Rushing Yards: {:.2f}".format(away_avg_ryd))
		print("Passing Yards: {:.2f}".format(away_avg_pyd))

		top_min = int(np.floor(away_avg_top / 60))
		top_sec = int(np.around(away_avg_top - (top_min * 60)))
		if top_sec < 10:
			top_sec = "0" + str(top_sec)
		print("Time Of Possession: {}:{}".format(top_min, top_sec))

		print("Third Down Conversion Rate: {:.2f}% ({} / {})".format(100*away_avg_3dp, away_tot_3dc, away_tot_3da))

		print("Rushing Yards Against: {:.2f}".format(home_avg_ryd))
		print("Passing Yards Against: {:.2f}".format(home_avg_pyd))

		print("Penalties: {:.2f}".format(away_avg_pen))

	# print("-----------------------------------")
	print("\n\nPress <ENTER> for next results.")
	input()
	print("-----------------------------------")