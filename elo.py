import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("./nbaallelo.csv")
df["date_game"] = pd.to_datetime(df["date_game"])

# df = df[df["date_game"] >= pd.Timestamp(2000, 1, 1)]

grouped = df.groupby("gameorder")
pts = grouped["pts"].sum()

home = df[df.game_location == "H"]
away = df[df.game_location == "A"]

# Think about how to deal with these later.
neutral = df.drop(home.index).drop(away.index)

home = home.set_index("gameorder")
away = away.set_index("gameorder")

elo_sum = home["elo_i"] + away["elo_i"]
elo_diff = abs(home["elo_i"] - away["elo_i"])
elo_df = pd.DataFrame({"pts": pts, "elo_sum": elo_sum, "elo_diff": elo_diff})

plt.style.use("seaborn")

# Even with low alpha, still pretty "full."
elo_df.plot.scatter(x="elo_diff", y="pts", alpha=0.6)

plt.xlabel("Elo difference", fontsize=16)
plt.ylabel("Total points", fontsize=16)
plt.title("Total points versus absolute Elo difference", fontsize=20)

# Block histograms.

step = 100
for base_elo in range(0, 500, step):
    block = elo_df[(base_elo <= elo_df["elo_diff"]) &
                    (elo_df["elo_diff"] < base_elo + step)]
    plt.figure()
    block["pts"].hist()
    plt.xlabel("Total points")
    plt.title("Total points (Elo {}-{})".format(base_elo, base_elo + step))

plt.show()
