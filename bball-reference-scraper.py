import requests
from bs4 import BeautifulSoup
import json

# fetch link
page = requests.get(
    'https://www.basketball-reference.com/leagues/NBA_2021_per_game.html')
# Get HTML content
soup = BeautifulSoup(page.text, 'html.parser')

links_list = []
playersTable = soup.find(id='per_game_stats')
playerRows = playersTable.find_all('tr')

players = {}
for playerRow in playerRows:
    playerStats = playerRow.find_all('td')
    player = {}
    for playerStat in playerStats:
        statName = playerStat['data-stat']
        statData = playerStat.string
        player[statName] = statData

    if(player != {}):
        playerName = player['player']
        if(playerName in players):
            players[playerName]['team_id'] = player['team_id']
        else:
            players[playerName] = player

formattedPlayers = []

for player in players:
    formattedPlayers.append(players[player])

teams = {}

for player in formattedPlayers:
    teamName = player['team_id']
    if teamName not in teams:
        teams[teamName] = [player]
    else:
        teams[teamName].append(player)

for team in teams:
    file = open(f"{team}.json", "w")
    file.write(json.dumps(teams[team]))
