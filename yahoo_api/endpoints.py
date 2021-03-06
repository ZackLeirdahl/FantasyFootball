def format_ids_to_keys(ids):
    return ['nfl.p.' + str(id) for id in ids]

def league():
    return 'https://fantasysports.yahooapis.com/fantasy/v2/league/nfl.l.98349'

def league_settings():
    return league() + '//settings'

def league_standings():
    return league() + '//standings'

def league_scoreboard():
    return league() + '//scoreboard'

def league_players():
    return league() + '//players'

def team(team_id):
    return 'https://fantasysports.yahooapis.com/fantasy/v2/team/nfl.l.98349.t.' + str(team_id)

def team_season_stats(team_id):
    return team(team_id) + '//stats;type=season'

def team_matchups(team_id, week):
    return team(team_id) + '//matchups;weeks='+str(week)

def team_roster(team_id):
    return team(team_id) + '//roster'

def team_roster_players(team_id):
    return team(team_id) + '//roster//players'

def players_by_key(player_ids):
    return 'https://fantasysports.yahooapis.com/fantasy/v2/players;player_keys='+','.join(format_ids_to_keys(player_ids))

def players_stats_by_key(player_ids):
    return players_by_key(player_ids) +'/stats'
