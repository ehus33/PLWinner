import pandas as pd

# Load data
data = pd.read_csv('male_players.csv')

# Split player_positions and select the primary position
data['primary_position'] = data['player_positions'].apply(lambda x: x.split(',')[0])

# Filter by Premier League teams and latest FIFA version
latest_year = data['fifa_version'].max()
prem_teams = [
    'Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton & Hove Albion', 'Burnley', 
    'Chelsea', 'Crystal Palace', 'Everton', 'Fulham', 'Ipswich Town','Leicester City','Liverpool', 
    'Manchester City', 'Manchester United', 'Newcastle United', 'Nottingham Forest', 
    'Southampton', 'Tottenham Hotspur', 'West Ham United', 'Wolverhampton Wanderers'
]
data = data[(data['club_name'].isin(prem_teams)) & (data['fifa_version'] == latest_year)]

# Define performance score for each position
data['forward_score'] = (data['attacking_finishing'] * 0.3 +
                         data['attacking_heading_accuracy'] * 0.1 +
                         data['pace'] * 0.3 +
                         data['dribbling'] * 0.2 +
                         data['shooting'] * 0.1)

data['midfielder_score'] = (data['passing'] * 0.3 +
                            data['dribbling'] * 0.2 +
                            data['mentality_vision'] * 0.2 +
                            data['power_stamina'] * 0.3)

data['defender_score'] = (data['defending'] * 0.4 +
                          data['mentality_interceptions'] * 0.3 +
                          data['defending_marking_awareness'] * 0.2 +
                          data['physic'] * 0.1)

data['goalkeeper_score'] = (data['goalkeeping_diving'] * 0.3 +
                            data['goalkeeping_handling'] * 0.3 +
                            data['goalkeeping_reflexes'] * 0.2 +
                            data['goalkeeping_positioning'] * 0.2)

# Identify the top players by specific positions
top_cb = data[data['primary_position'] == 'CB'].nlargest(2, 'defender_score').drop_duplicates('short_name')
top_lb = data[data['primary_position'].isin(['LB', 'LWB'])].nlargest(1, 'defender_score').drop_duplicates('short_name')
top_rb = data[data['primary_position'].isin(['RB', 'RWB'])].nlargest(1, 'defender_score').drop_duplicates('short_name')

bench_cb = data[data['primary_position'] == 'CB'].nlargest(4, 'defender_score').drop_duplicates('short_name').iloc[2:]
bench_lb = data[data['primary_position'].isin(['LB', 'LWB'])].nlargest(2, 'defender_score').drop_duplicates('short_name').iloc[1:]
bench_rb = data[data['primary_position'].isin(['RB', 'RWB'])].nlargest(2, 'defender_score').drop_duplicates('short_name').iloc[1:]

# Combine the top defenders
top_defenders = pd.concat([top_cb, top_lb, top_rb])
bench_defenders = pd.concat([bench_cb, bench_lb, bench_rb])

# Repeat the process for forwards, midfielders, and goalkeepers as before
top_forwards = data[data['primary_position'].isin(['ST', 'CF', 'LW', 'RW'])].nlargest(10, 'forward_score').drop_duplicates('short_name').nlargest(3, 'forward_score')
bench_forwards = data[data['primary_position'].isin(['ST', 'CF', 'LW', 'RW'])].nlargest(10, 'forward_score').drop_duplicates('short_name').nlargest(6, 'forward_score').iloc[3:]

top_midfielders = data[data['primary_position'].isin(['CM', 'CAM', 'CDM'])].nlargest(10, 'midfielder_score').drop_duplicates('short_name').nlargest(3, 'midfielder_score')
bench_midfielders = data[data['primary_position'].isin(['CM', 'CAM', 'CDM'])].nlargest(10, 'midfielder_score').drop_duplicates('short_name').nlargest(6, 'midfielder_score').iloc[3:]

top_goalkeeper = data[data['primary_position'] == 'GK'].nlargest(10, 'goalkeeper_score').drop_duplicates('short_name').nlargest(1, 'goalkeeper_score')
bench_goalkeeper = data[data['primary_position'] == 'GK'].nlargest(10, 'goalkeeper_score').drop_duplicates('short_name').nlargest(2, 'goalkeeper_score').iloc[1:]

# Output the best players
print("Starting XI:")
print("Top 3 Forwards (including strikers and wingers):")
for index, player in top_forwards.iterrows():
    print(f"{player['short_name']} - Club: {player['club_name']} - Score: {player['forward_score']}")

print("\nTop 3 Midfielders:")
for index, player in top_midfielders.iterrows():
    print(f"{player['short_name']} - Club: {player['club_name']} - Score: {player['midfielder_score']}")

print("\nTop 4 Defenders:")
for index, player in top_defenders.iterrows():
    print(f"{player['short_name']} - Club: {player['club_name']} - Score: {player['defender_score']}")

print("\nBest Goalkeeper:")
for index, player in top_goalkeeper.iterrows():
    print(f"{player['short_name']} - Club: {player['club_name']} - Score: {player['goalkeeper_score']}")

print("\nBench:")
print("Bench Forwards:")
for index, player in bench_forwards.iterrows():
    print(f"{player['short_name']} - Club: {player['club_name']} - Score: {player['forward_score']}")

print("\nBench Midfielders:")
for index, player in bench_midfielders.iterrows():
    print(f"{player['short_name']} - Club: {player['club_name']} - Score: {player['midfielder_score']}")

print("\nBench Defenders:")
for index, player in bench_defenders.iterrows():
    print(f"{player['short_name']} - Club: {player['club_name']} - Score: {player['defender_score']}")

print("\nBench Goalkeeper:")
for index, player in bench_goalkeeper.iterrows():
    print(f"{player['short_name']} - Club: {player['club_name']} - Score: {player['goalkeeper_score']}")
