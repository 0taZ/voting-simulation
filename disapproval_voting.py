import random
import matplotlib.pyplot as plt

const = {"v_wing_sigma": 0.1, "voter": 1000, "candidate": 5, "popularity_weight_for_negative": 1}

num_voter = const["voter"]
num_candidate = const["candidate"]

c_popularity = [random.random() for x in range(num_candidate)]
c_wing = [random.uniform(float(-1), float(1)) for x in range(num_candidate)]

v_wing = []
for v in range(num_voter):
    wing = c_wing[random.choices(population = range(num_candidate), weights = c_popularity, k = 1)[0]] + random.gauss(mu = 0, sigma = const["v_wing_sigma"])
    if wing < -1:
        wing = -1
    if wing > 1:
        wing = 1
    v_wing.append(wing)

v_distance = []

v_support = []
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
v_positive = [v_support[v].index(max(v_support[v])) for v in range(num_voter)]

v_unsupport = []
for v in range(num_voter):
    c_tmpist_us = []
    for c in range(num_candidate):
        unsupport = v_distance[v][c] * (c_popularity[c] + const["popularity_weight_for_negative"]) # 各候補者への、人気度調整を含めた嫌い度
        c_tmpist_us.append(unsupport)
    v_unsupport.append(tuple(c_tmpist_us))
v_negative = [v_unsupport[v].index(max(v_unsupport[v])) for v in range(num_voter)]

c_gotten_votes = [v_positive.count(c) for c in range(num_candidate)]
positive_winner = c_gotten_votes.index(max(c_gotten_votes))
c_gotten_negative_votes = [v_negative.count(c) for c in range(num_candidate)]
c_sum_votes = [v_positive.count(c) - v_negative.count(c) for c in range(num_candidate)]
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