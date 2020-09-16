import numpy as np
import pandas as pd


def analyzeSingleStrat(strat_data, home_team=True):
	strat_data["HomeWin"] = strat_data["HomeScore"] > strat_data["AwayScore"]

	home_win_pct = sum(strat_data["HomeWin"]) / len(strat_data)
	home_win_err = np.sqrt(home_win_pct * (1-home_win_pct) / len(strat_data))
	home_avg_top = np.mean(strat_data["HomeTOP"])
	away_avg_top = np.mean(strat_data["AwayTOP"])
	home_avg_pts = np.mean(strat_data["HomeScore"])
	away_avg_pts = np.mean(strat_data["AwayScore"])
	home_avg_ryd = np.mean(strat_data["HomeRushYds"])
	home_avg_pyd = np.mean(strat_data["HomePassYds"])
	away_avg_ryd = np.mean(strat_data["AwayRushYds"])
	away_avg_pyd = np.mean(strat_data["AwayPassYds"])
	home_avg_3dp = np.mean(strat_data["Home3rdDownComp"]) / np.mean(strat_data["Home3rdDownAtt"])
	home_tot_3da = int(np.sum(strat_data["Home3rdDownAtt"]))
	home_tot_3dc = int(np.sum(strat_data["Home3rdDownComp"]))
	away_avg_3dp = np.mean(strat_data["Away3rdDownComp"]) / np.mean(strat_data["Away3rdDownAtt"])
	away_tot_3da = int(np.sum(strat_data["Away3rdDownAtt"]))
	away_tot_3dc = int(np.sum(strat_data["Away3rdDownComp"]))
	home_avg_tos = np.mean(strat_data["AwayInt"]) + np.mean(strat_data["HomeFumblesLost"])
	away_avg_tos = np.mean(strat_data["HomeInt"]) + np.mean(strat_data["AwayFumblesLost"])
	home_avg_pen = np.mean(strat_data["HomePenalties"])
	away_avg_pen = np.mean(strat_data["AwayPenalties"])

	if home_team:

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


def analyzeBatchOutput(results_file, titles, home_team=True):
	batch_data = pd.read_csv(results_file)

	for i, title in enumerate(titles):
		strat_data = batch_data[batch_data["Strat"] == title]
		print("Strategy #{}".format(i+1))
		print(title)
		print("N = {}\n".format(len(strat_data)))

		analyzeSingleStrat(strat_data, home_team)

		print("-----------------------------------")
