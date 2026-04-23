import pandas as pd

data = {
    "playerId": [1, 2, 3, 4, 5],
    "name": ["Connor McDavid", "Nathan MacKinnon", "Leon Draisaitl", "Nikita Kucherov", "David Pastrnak"],
    "team": ["EDM", "COL", "EDM", "TBL", "BOS"],
    "position": ["C", "C", "C", "R", "R"],
    "icetime": [1500, 1450, 1400, 1350, 1300],
    "I_F_points": [100, 95, 90, 85, 80],
    "I_F_goals": [40, 35, 42, 30, 45],
    "I_F_assists": [60, 60, 48, 55, 35],
    "xGoalsPercentage": [58.5, 57.2, 56.8, 55.1, 54.9],
    "corsiPercentage": [57.0, 56.5, 55.9, 54.2, 53.8],
    "xGoalsFor": [120, 115, 110, 105, 100],
    "xGoalsAgainst": [85, 88, 84, 86, 87]
}

df = pd.DataFrame(data)
df["points_per_60"] = (df["I_F_points"] / df["icetime"]) * 3600
df["goals_per_60"]  = (df["I_F_goals"]  / df["icetime"]) * 3600

print(df.head())
df.to_csv("players.csv", index=False)
print("Done! players.csv saved.")
