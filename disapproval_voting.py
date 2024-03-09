import random
import matplotlib.pyplot as plt

const = {"v_wing_sigma": 0.1, "voter": 1000, "candidate": 5, "popularity_weight_for_negative": 1}

num_voter = const["voter"]
num_candidate = const["candidate"]

c_popularity = [random.random() for x in range(num_candidate)] # 候補者それぞれの人気度を[0, 1]の乱数で決定
c_wing = [random.uniform(float(-1), float(1)) for x in range(num_candidate)] # 候補者それぞれの右翼左翼度を[-1, 1]の乱数で決定


# 各候補者ごとに右翼左翼度を設定
# 基準となる候補者を、候補者の人気度を重さとして振り分ける。その候補者の右翼左翼度を初期値とする
# 平均0、標準偏差を"v_wing_sigma"とした乱数をそれぞれ生成し初期値に足した値を最終的な投票者の右翼左翼度とする
v_wing = []
for v in range(num_voter):
    wing = c_wing[random.choices(population = range(num_candidate), weights = c_popularity, k = 1)[0]] + random.gauss(mu = 0, sigma = const["v_wing_sigma"])
    if wing < -1:
        wing = -1
    if wing > 1:
        wing = 1
    v_wing.append(wing)

v_distance = [] # 各投票者の右翼左翼度が各有権者のそれとどれくらい離れているかを表す、各投票者のリスト

v_support = [] # 各投票者の、各候補者ごとに算出した支持率のリスト
for v in range(num_voter):
    c_tmplist_d = []
    c_tmplist_s = []
    for c in range(num_candidate):
        distance = abs(v_wing[v] - c_wing[c])
        support = 2 - distance
        c_tmplist_d.append(distance)
        c_tmplist_s.append(support)
    v_distance.append(tuple(c_tmplist_d))
    v_support.append(tuple(c_tmplist_s))
v_positive = [v_support[v].index(max(v_support[v])) for v in range(num_voter)] # 各投票者の中で最も支持率が高い候補者をまとめたリスト

v_unsupport = [] # 各投票者の、各候補者ごとに算出した非支持率のリスト
for v in range(num_voter):
    c_tmpist_us = []
    for c in range(num_candidate):
        unsupport = v_distance[v][c] * (c_popularity[c] + const["popularity_weight_for_negative"]) # 各候補者への、人気度調整を含めた嫌い度
        c_tmpist_us.append(unsupport)
    v_unsupport.append(tuple(c_tmpist_us))
v_negative = [v_unsupport[v].index(max(v_unsupport[v])) for v in range(num_voter)] # 各投票者の中で最も非支持率が高い候補者をまとめたリスト

c_gotten_votes = [v_positive.count(c) for c in range(num_candidate)] # 各候補者が獲得したプラス票を集計
positive_winner = c_gotten_votes.index(max(c_gotten_votes)) # プラス票の最も多かった候補者
c_gotten_negative_votes = [v_negative.count(c) for c in range(num_candidate)] # 各候補者が獲得したマイナス票を集計
c_sum_votes = [v_positive.count(c) - v_negative.count(c) for c in range(num_candidate)] # マイナス票の最も多かった候補者
sum_winner = c_sum_votes.index(max(c_sum_votes))

print(f"popularity: {c_popularity}")
print(f"c_wing: {c_wing}")
print(f"v_wing: {v_wing}")
print(f"v_support: {v_support}")
print(f"positive: {v_positive}")
print(f"negative: {v_negative}")
print(f"positive_winner: {positive_winner}")
print(f"sum_winner: {sum_winner}")

fig = plt.figure()

ax1 = fig.add_subplot(3, 1, 1)
ax2 = fig.add_subplot(3, 1, 2)
ax3 = fig.add_subplot(3, 1, 3)

ax1.bar(range(num_candidate), c_gotten_votes)
ax2.bar(range(num_candidate), c_gotten_negative_votes)
ax3.bar(range(num_candidate), c_sum_votes)

plt.show()