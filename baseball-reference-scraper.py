from os import stat
from typing import Text
import requests
from bs4 import BeautifulSoup
from bs4 import Comment
import json

# fetch link
page = requests.get(
    'https://www.baseball-reference.com/leagues/MLB/2021-standard-batting.shtml')
# Get HTML content
soup = BeautifulSoup(page.text, 'html.parser')

# file = open("test.html", "w") file.write(str(soup))

# playersTable = soup.find(id='div_players_standard_batting')

comments = soup.find_all(string=lambda text: isinstance(text, Comment))

batterTableHTML = ""

for c in comments:
    # print(c)
    find = c.find('div_players_standard_batting')

    if(find != -1):
        batterTableHTML = str(c)


soup = BeautifulSoup(batterTableHTML, 'lxml')

playersTable = soup.find(id='players_standard_batting')


playerRows = playersTable.find_all('tr')

players = {}
for playerRow in playerRows:
    playerStats = playerRow.find_all('td')
    player = {'show': False}
    for playerStat in playerStats:
        statName = playerStat['data-stat']

        linkText = playerStat.find('a')

        if(linkText):
            player[statName] = linkText.string
        else:
            player[statName] = playerStat.string

    if(player != {'show': False}):
        playerName = player['player']
        if(playerName in players):
            players[playerName]['team_ID'] = player['team_ID']
        else:
            players[playerName] = player

formattedPlayers = []

for player in players:
    formattedPlayers.append(players[player])

teams = {}

for player in formattedPlayers:
    teamName = player['team_ID']
    if teamName not in teams:
        teams[teamName] = [player]
    else:
        teams[teamName].append(player)

teamNames = []
for team in teams:
    if(team):
        teamNames.append(team)
        file = open(f"MLB/{team}.json", "w")
        file.write(json.dumps(teams[team]))

file = open(f"MLB/teamNames.json", "w")
file.write(json.dumps(teamNames))
