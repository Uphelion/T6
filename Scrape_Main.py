import requests
from bs4 import BeautifulSoup
import pandas as pd

# Replace the URL with the appropriate source for the Premier League results
url = "https://www.flashscore.co.uk/football/england/premier-league/results/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

big_six = ["Arsenal", "Chelsea", "Liverpool", "Manchester United", "Manchester City", "Tottenham Hotspur"]
results = []

for game in soup.find_all("div", class_="game-result"):
    home_team = game.find("div", class_="home-team").text.strip()
    away_team = game.find("div", class_="away-team").text.strip()
    score = game.find("div", class_="score").text.strip().split("-")

    if home_team in big_six and away_team in big_six:
        home_goals, away_goals = int(score[0]), int(score[1])
        results.append((home_team, away_team, home_goals, away_goals))

print(results)

team_records = {team: {"Team": team, "Played": 0, "Won": 0, "Drawn": 0, "Lost": 0, "GF": 0, "GA": 0, "GD": 0, "Points": 0} for team in big_six}

for home, away, home_goals, away_goals in results:
    team_records[home]["Played"] += 1
    team_records[away]["Played"] += 1
    team_records[home]["GF"] += home_goals
    team_records[away]["GF"] += away_goals
    team_records[home]["GA"] += away_goals
    team_records[away]["GA"] += home_goals
    team_records[home]["GD"] += home_goals - away_goals
    team_records[away]["GD"] += away_goals - home_goals

    if home_goals > away_goals:
        team_records[home]["Won"] += 1
        team_records[away]["Lost"] += 1
        team_records[home]["Points"] += 3
    elif home_goals < away_goals:
        team_records[home]["Lost"] += 1
        team_records[away]["Won"] += 1
        team_records[away]["Points"] += 3
    else:
        team_records[home]["Drawn"] += 1
        team_records[away]["Drawn"] += 1
        team_records[home]["Points"] += 1
        team_records[away]["Points"] += 1

df = pd.DataFrame(team_records.values())
df = df.sort_values(by=["Points", "GD", "GF"], ascending=False)
df = df.reset_index(drop=True)
print(df)

