import requests
import csv
from bs4 import BeautifulSoup

def get_fixtures():
    url = "https://www.flashscore.co.uk/football/england/premier-league/results/"  # Replace with the actual URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    fixtures = []

    for fixture in soup.find_all('div', class_='fixture'):  # Replace with the actual HTML element and class
        home_team = fixture.find('span', class_='home-team').text.strip()
        away_team = fixture.find('span', class_='away-team').text.strip()
        score = fixture.find('span', class_='score').text.strip()

        print(f"Home Team: {home_team}, Away Team: {away_team}, Score: {score}")  # Print the scraped data

        if home_team in big_six and away_team in big_six:
            fixtures.append({
                'home_team': home_team,
                'away_team': away_team,
                'score': score
            })

    return fixtures



def build_big_six_table(fixtures):
    table = {team: {'P': 0, 'W': 0, 'D': 0, 'L': 0, 'F': 0, 'A': 0, 'GD': 0, 'Pts': 0} for team in big_six}

    for fixture in fixtures:
        home_team, away_team = fixture['home_team'], fixture['away_team']
        home_goals, away_goals = map(int, fixture['score'].split('-'))

        table[home_team]['P'] += 1
        table[away_team]['P'] += 1
        table[home_team]['F'] += home_goals
        table[home_team]['A'] += away_goals
        table[away_team]['F'] += away_goals
        table[away_team]['A'] += home_goals

        if home_goals > away_goals:
            table[home_team]['W'] += 1
            table[away_team]['L'] += 1
            table[home_team]['Pts'] += 3
        elif home_goals < away_goals:
            table[home_team]['L'] += 1
            table[away_team]['W'] += 1
            table[away_team]['Pts'] += 3
        else:
            table[home_team]['D'] += 1
            table[away_team]['D'] += 1
            table[home_team]['Pts'] += 1
            table[away_team]['Pts'] += 1

    for team in table:
        table[team]['GD'] = table[team]['F'] - table[team]['A']

    return table
    print(table)

def write_csv(table):
    with open('big_six_table.csv', 'w', newline='') as csvfile:
        fieldnames = ['Team', 'P', 'W', 'D', 'L', 'F', 'A', 'GD', 'Pts']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for team, stats in table.items():
            writer.writerow({
                'Team': team,
                'P': stats['P'],
                'W': stats['W'],
                'D': stats['D'],
                'L': stats['L'],
                'F': stats['F'],
                'A': stats['A'],
                'GD': stats['GD'],
                'Pts': stats['Pts']
            })

if __name__ == "__main__":
    big_six = ['Arsenal', 'Chelsea', 'Liverpool', 'Manchester United', 'Manchester City', 'Spurs']
    fixtures = get_fixtures()
    print(fixtures)  # Print the fixtures list
    big_six_table = build_big_six_table(fixtures)
    write_csv(big_six_table)

