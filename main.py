#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
import json
import datetime

src_path = os.path.join(os.getcwd(), 'src')

with open(os.path.join(src_path, 'teamsids.json')) as team_json:
    clubs = json.load(team_json)

with open(os.path.join(src_path, 'leagueids.json')) as league_json:
    leagues = json.load(league_json)

with open(os.path.join(src_path, 'api_key.txt')) as a_key:
    API_key = a_key.read().strip()

url = 'https://api.football-data.org/v2/'
header = {'X-Auth-Token': API_key}


def get_clubname_id(clubname):
    club_id, club_code = None, None
    for club in clubs['teams']:
        if club['name'] == clubname:
            club_id = club['id']
            club_code = club['code']
            break
    return club_id, clubname, club_code


def players_info(club_id, clubname):
    print(f'Club Name: {clubname}')
    response = requests.get(f'{url}teams/{club_id}', headers=header)
    content = response.json()
    print('Players:')
    for player_data in content["squad"]:
        if player_data["role"] != "COACH":
            if player_data['position'] == 'Goalkeeper':
                print(f'{player_data["name"]} (GK)')
            elif player_data['position'] == 'Defender':
                print(f'{player_data["name"]} (DF)')
            elif player_data['position'] == 'Midfielder':
                print(f'{player_data["name"]} (MF)')
            else:
                print(f'{player_data["name"]} (ST)')
        else:
            print(f'Coach:\n{player_data["name"]} (C)')
    return


def lstandings(leaguename):
    for league in leagues['LEAGUE_IDS']:
        if league['name'] == leaguename:
            league_id = league['id']
            break
    response = requests.get(f'{url}competitions/{league_id}/standings', headers=header)
    content = response.json()
    table_format = '{: ^25} || {: ^10} || {: ^10} || {: ^10} || {: ^10} || {: ^10} || {: ^10} || {: ^10} || {: ^10} ||'
    if league_id == 2001:
        for groups in content['standings']:
            print(f'{groups["group"]} {groups["type"]} matches:')
            print('=====================')
            print(table_format.format('Club Name', 'Played', 'Won', 'Draw', 'Lost', 'Points', 'For', 'Againts', 'Difference'))
            print('-------------------------------------------------------------------------------------------------------------------------------------------------')
            print(table_format.format(groups["table"][0]['team']["name"], *[groups['table'][0].get(key) for key in ['playedGames', 'won', 'draw', 'lost', 'points', 'goalsFor', 'goalsAgainst', 'goalDifference']]))
            print(table_format.format(groups["table"][1]['team']["name"], *[groups['table'][1].get(key) for key in ['playedGames', 'won', 'draw', 'lost', 'points', 'goalsFor', 'goalsAgainst', 'goalDifference']]))
            print(table_format.format(groups["table"][2]['team']["name"], *[groups['table'][2].get(key) for key in ['playedGames', 'won', 'draw', 'lost', 'points', 'goalsFor', 'goalsAgainst', 'goalDifference']]))
            print(table_format.format(groups["table"][3]['team']["name"], *[groups['table'][3].get(key) for key in ['playedGames', 'won', 'draw', 'lost', 'points', 'goalsFor', 'goalsAgainst', 'goalDifference']]))
            print()
        return

    print('Total Matches:')
    print('=============')
    print(table_format.format('Club Name', 'Played', 'Won', 'Draw', 'Lost', 'Points', 'For', 'Againts', 'Difference'))
    print('-------------------------------------------------------------------------------------------------------------------------------------------------')
    for teams in content['standings'][0]['table']:
        print(table_format.format(teams["team"]["name"], *[teams.get(key) for key in ['playedGames', 'won', 'draw', 'lost', 'points', 'goalsFor', 'goalsAgainst', 'goalDifference']]))
    print()

    print('Home Matches:')
    print('=============')
    print(table_format.format('Club Name', 'Played', 'Won', 'Draw', 'Lost', 'Points', 'For', 'Againts', 'Difference'))
    print('-------------------------------------------------------------------------------------------------------------------------------------------------')
    for teams in content['standings'][1]['table']:
        print(table_format.format(teams["team"]["name"], *[teams.get(key) for key in ['playedGames', 'won', 'draw', 'lost', 'points', 'goalsFor', 'goalsAgainst', 'goalDifference']]))
    print()

    print('Away Matches:')
    print('=============')
    print(table_format.format('Club Name', 'Played', 'Won', 'Draw', 'Lost', 'Points', 'For', 'Againts', 'Difference'))
    print('-------------------------------------------------------------------------------------------------------------------------------------------------')
    for teams in content['standings'][2]['table']:
        print(table_format.format(teams["team"]["name"], *[teams.get(key) for key in ['playedGames', 'won', 'draw', 'lost', 'points', 'goalsFor', 'goalsAgainst', 'goalDifference']]))
    return


def _parse_matches(content):
    for match in content['matches']:
        if match["status"] == 'POSTPONED':
            print(f"Match scheduled on: {match['utcDate'][:10]}")
            print(f'Match status: {match["status"]}')
        else:
            print(f"Match scheduled on: {match['utcDate'][:10]}")
            print(f'Match status: {match["status"]}')
        print(f'Matchday: {match["season"]["currentMatchday"]}')
        if match['score']['winner'] == 'HOME_TEAM':
            print(f'Winner: {match["homeTeam"]["name"]}')
        elif match['score']['winner'] == 'AWAY_TEAM':
            print(f'Winner: {match["awayTeam"]["name"]}')
        else:
            print(match['score']['winner'])
        print(f'Home team: {match["homeTeam"]["name"]}: {match["score"]["fullTime"]["homeTeam"]}')
        print(f'Away team: {match["awayTeam"]["name"]}: {match["score"]["fullTime"]["awayTeam"]}')
        print('========================')
    return


def get_matchinfo_clubs(club_id, clubname, dateFrom=None, dateTo=None):
    if dateFrom is not None and dateTo is not None:
        print(f'Showing matches of {clubname} from {dateFrom} to {dateTo}:')
        response = requests.get(f'{url}teams/{club_id}/matches?dateFrom={dateFrom}&dateTo={dateTo}'.strip(), headers=header)
    elif dateFrom is not None and dateTo is None:
        dateTo = str(datetime.datetime.today())[:10]
        print(f'Showing matches of {clubname} from {dateFrom} to today:')
        response = requests.get(f'{url}teams/{club_id}/matches?dateFrom={dateFrom}&dateTo={dateTo}'.strip(), headers=header)
    elif dateFrom is None and dateTo is not None:
        print('Must provide start date if end date is mentioned')
    else:
        print(f'Showing all the matches of {clubname}:')
        response = requests.get(f'{url}teams/{club_id}/matches'.strip(), headers=header)
    _parse_matches(response.json())
    return


def get_top_scorer(leaguename):
    for league in leagues['LEAGUE_IDS']:
        if league['name'] == leaguename:
            league_id = league['id']
            break
    response = requests.get(f'{url}competitions/{league_id}/scorers', headers=header)
    content = response.json()
    r = 1
    for scorer in content['scorers']:
        print(f'{r}.{scorer["player"]["name"]} scored {scorer["numberOfGoals"]} goals')
        r += 1
    return


def get_matchinfo_comp(competition, dateFrom=None, dateTo=None):
    if dateFrom is not None and dateTo is not None:
        print(f'Showing matches of {competition} from {dateFrom} to {dateTo}:')
        response = requests.get(f'{url}competitions/{competition}/matches?dateFrom={dateFrom}&dateTo={dateTo}', headers=header)
    elif dateFrom is not None and dateTo is None:
        dateTo = str(datetime.datetime.today())[:10]
        print(f'Showing matches of {competition} from {dateFrom} to {dateTo}:')
        response = requests.get(f'{url}competitions/{competition}/matches?dateFrom={dateFrom}&dateTo={dateTo}', headers=header)
    elif dateFrom is None and dateTo is not None:
        print('Must provide start date if end date is mentioned')
    else:
        print(f'Showing all the matches of {competition}:')
        response = requests.get(f'{url}competitions/{competition}/matches', headers=header)
    _parse_matches(response.json())
    return


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('To see how to use the command line arguments please refer to the README.md at ')
    elif sys.argv[1] == 'club_code':
        club_id, clubname, club_code = get_clubname_id(' '.join(sys.argv[2:]))
        print(f'Club name: {clubname}\nClub id: {club_id}')
    elif sys.argv[1] == 'squad_info':
        club_id, clubname, club_code = get_clubname_id(' '.join(sys.argv[2:]))
        players_info(club_id, clubname)
    elif sys.argv[1] == 'league_table':
        lstandings(sys.argv[2])
    elif sys.argv[1] == 'club_match_info':
        club_id = sys.argv[2]
        for club in clubs['teams']:
            if club['id'] == club_id:
                clubname = club['name']
                break
        try:
            datefrom = sys.argv[3]
            dateto = sys.argv[4]
            get_matchinfo_clubs(club_id, clubname, datefrom, dateto)
        except Exception:
            try:
                datefrom = sys.argv[3]
                get_matchinfo_clubs(club_id, clubname, datefrom)
            except Exception:
                get_matchinfo_clubs(club_id, clubname)
    elif sys.argv[1] == 'comp_match_info':
        comp = sys.argv[2]
        try:
            datefrom = sys.argv[3]
            dateto = sys.argv[4]
            get_matchinfo_comp(comp, datefrom, dateto)
        except Exception:
            try:
                datefrom = sys.argv[3]
                get_matchinfo_comp(comp, datefrom)
            except Exception:
                get_matchinfo_comp(comp)
    else:
        print('Please check your syntax')
