import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def normalize(df, cols, invert=[]):
    scaler = MinMaxScaler()
    df_scaled = df.copy()
    df_scaled[cols] = scaler.fit_transform(df[cols].fillna(0))
    for col in invert:
        df_scaled[col] = 1 - df_scaled[col]
    return df_scaled

def rank_centres(df):
    players = df[df["position"] == "C"].copy()
    cols = ["goals_per_60", "assists_per_60", "xGFpct", "corsiPct",
            "ixG_per_60", "plusMinus", "takeaways", "giveaways",
            "hits", "faceoffPct"]
    scaled = normalize(players, cols, invert=["giveaways"])
    scaled["rank_score"] = (
        scaled["goals_per_60"]   * 0.20 +
        scaled["assists_per_60"] * 0.20 +
        scaled["xGFpct"]         * 0.15 +
        scaled["ixG_per_60"]     * 0.15 +
        scaled["corsiPct"]       * 0.10 +
        scaled["plusMinus"]      * 0.08 +
        scaled["takeaways"]      * 0.05 +
        scaled["giveaways"]      * 0.03 +
        scaled["hits"]           * 0.02 +
        scaled["faceoffPct"]     * 0.02
    )
    scaled["rank"] = scaled["rank_score"].rank(ascending=False).astype(int)
    return scaled

def rank_wingers(df):
    players = df[df["position"].isin(["L", "R"])].copy()
    cols = ["goals_per_60", "assists_per_60", "xGFpct", "corsiPct",
            "ixG_per_60", "plusMinus", "takeaways", "giveaways", "hits"]
    scaled = normalize(players, cols, invert=["giveaways"])
    scaled["rank_score"] = (
        scaled["goals_per_60"]   * 0.20 +
        scaled["assists_per_60"] * 0.20 +
        scaled["xGFpct"]         * 0.15 +
        scaled["ixG_per_60"]     * 0.15 +
        scaled["corsiPct"]       * 0.10 +
        scaled["plusMinus"]      * 0.08 +
        scaled["takeaways"]      * 0.05 +
        scaled["giveaways"]      * 0.03 +
        scaled["hits"]           * 0.04
    )
    scaled["rank"] = scaled["rank_score"].rank(ascending=False).astype(int)
    return scaled

def rank_defensemen(df):
    players = df[df["position"] == "D"].copy()
    cols = ["goals_per_60", "assists_per_60", "xGFpct", "corsiPct",
            "ixG_per_60", "plusMinus", "takeaways", "giveaways", "blocks"]
    scaled = normalize(players, cols, invert=["giveaways"])
    scaled["rank_score"] = (
        scaled["goals_per_60"]   * 0.10 +
        scaled["assists_per_60"] * 0.15 +
        scaled["xGFpct"]         * 0.20 +
        scaled["ixG_per_60"]     * 0.15 +
        scaled["corsiPct"]       * 0.15 +
        scaled["plusMinus"]      * 0.10 +
        scaled["takeaways"]      * 0.05 +
        scaled["giveaways"]      * 0.05 +
        scaled["blocks"]         * 0.05
    )
    scaled["rank"] = scaled["rank_score"].rank(ascending=False).astype(int)
    return scaled

def rank_players():
    df = pd.read_csv("players.csv")
    df["goals_per_60"]   = (df["goals"]   / df["toiSeconds"]) * 3600
    df["assists_per_60"] = (df["assists"] / df["toiSeconds"]) * 3600
    df["ixG_per_60"]     = (df["ixG"]     / df["toiSeconds"]) * 3600
    df["faceoffPct"]     = df["faceoffPct"].fillna(0)
    df["xGFpct"]         = df["xGFpct"].fillna(df["xGFpct"].median())
    df["corsiPct"]       = df["corsiPct"].fillna(df["corsiPct"].median())
    df["ixG_per_60"]     = df["ixG_per_60"].fillna(0)

    centres    = rank_centres(df)
    wingers    = rank_wingers(df)
    defensemen = rank_defensemen(df)
    return centres, wingers, defensemen

if __name__ == "__main__":
    centres, wingers, defensemen = rank_players()

    print("\n🏒 TOP 10 CENTRES")
    print(centres.sort_values("rank").head(10)[["rank", "name", "team", "rank_score"]].to_string())

    print("\n🏒 TOP 10 WINGERS")
    print(wingers.sort_values("rank").head(10)[["rank", "name", "team", "position", "rank_score"]].to_string())

    print("\n🛡️  TOP 10 DEFENSEMEN")
    print(defensemen.sort_values("rank").head(10)[["rank", "name", "team", "rank_score"]].to_string())
