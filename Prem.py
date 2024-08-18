import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load the data
data = pd.read_csv('premier-league-matches.csv')

# Filter data for the last 5 seasons
last_5_seasons = data['Season_End_Year'].unique()[-5:]
data = data[data['Season_End_Year'].isin(last_5_seasons)]

# Calculate points for each match
def calculate_points(row):
    if row['FTR'] == 'H':
        return 3
    elif row['FTR'] == 'A':
        return 3
    else:
        return 1

data['HomePoints'] = data.apply(lambda row: 3 if row['FTR'] == 'H' else (1 if row['FTR'] == 'D' else 0), axis=1)
data['AwayPoints'] = data.apply(lambda row: 3 if row['FTR'] == 'A' else (1 if row['FTR'] == 'D' else 0), axis=1)

# Aggregate points for each team, considering home and away games separately
home_stats = data.groupby(['Season_End_Year', 'Home']).agg({'HomePoints': 'sum', 'HomeGoals': 'sum', 'AwayGoals': 'sum'}).reset_index()
away_stats = data.groupby(['Season_End_Year', 'Away']).agg({'AwayPoints': 'sum', 'AwayGoals': 'sum', 'HomeGoals': 'sum'}).reset_index()

# Rename columns for consistency
home_stats.columns = ['Season_End_Year', 'Team', 'Points', 'GoalsFor', 'GoalsAgainst']
away_stats.columns = ['Season_End_Year', 'Team', 'Points', 'GoalsFor', 'GoalsAgainst']

# Combine home and away stats
team_stats = pd.concat([home_stats, away_stats])

# Aggregate by team and season
team_stats = team_stats.groupby(['Season_End_Year', 'Team']).sum().reset_index()

# Calculate additional statistics
team_stats['GoalDifference'] = team_stats['GoalsFor'] - team_stats['GoalsAgainst']

# Feature Engineering: Use average points, goal difference, etc.
features = team_stats.groupby('Team').agg({
    'Points': 'mean',
    'GoalDifference': 'mean'
}).reset_index()

# Model training
X = features[['Points', 'GoalDifference']]
y = (features['Points'] > features['Points'].median()).astype(int)  # Label teams with above-median points as potential winners

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)

# Predicting
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: {accuracy}")

# Ranking teams based on prediction
features['Predicted'] = model.predict(X)
top_teams = features.nlargest(3, 'Points')  # Rank based on average points, assuming it correlates with likelihood of winning

print("Top 3 Predicted Teams:")
print(top_teams[['Team', 'Points']])
