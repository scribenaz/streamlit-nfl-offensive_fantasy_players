import pandas as pd
import streamlit as st


def load_data():
    return pd.read_csv("top_players_2025.csv")


def calculate_points(df, scoring):
    df = df.copy()
    if scoring == "Standard":
        df["points"] = df["fantasy_points"]
    elif scoring == "Half PPR":
        df["points"] = (df["fantasy_points"] + df["fantasy_points_ppr"]) / 2
    else:
        df["points"] = df["fantasy_points_ppr"]
    df["points"] = df["points"].round(1)
    df["ppg"] = (df["points"] / df["games"]).round(1)
    return df.sort_values("points", ascending=False)


st.title("NFL Fantasy Draft Helper")
st.write("Top QB, RB, and WR from each NFL team based on the 2025 season.")

# User inputs
scoring = st.selectbox("Scoring format", ["Standard", "Half PPR", "Full PPR"], index=2)
positions = st.multiselect("Positions", ["QB", "RB", "WR"], default=["QB", "RB", "WR"])
min_games = st.slider("Minimum games played", 1, 17, 1)

# Load and filter data
data = calculate_points(load_data(), scoring)
data = data[data["position"].isin(positions) & (data["games"] >= min_games)]

if data.empty:
    st.warning("No players match these filters.")
    st.stop()

# Visualizations
st.subheader("Top 15 Players by Fantasy Points")
st.bar_chart(data.head(15).set_index("player")["points"])

st.subheader("Player Stats")
table = data[["player", "team", "position", "games", "points", "ppg"]]
st.dataframe(table, hide_index=True)

best = data.sort_values("ppg", ascending=False).iloc[0]
st.subheader("Best Points Per Game")
st.write(f"{best['player']} ({best['team']}, {best['position']}): {best['ppg']} PPG")

# Download button
st.download_button("Download Player Data CSV", table.to_csv(index=False), "players.csv")
