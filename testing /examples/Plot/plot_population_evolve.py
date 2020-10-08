import csv

from matplotlib import pyplot as plt

csv_path = './data/progress.csv'

with open(csv_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    rewards = []
    iterations = []
    for (i, row) in enumerate(csv_reader):
        print(i)
        if i == 0:
            entry_dict = {}
            for index in range(len(row)):
                entry_dict[row[index]] = index
        else:
            rewards.append(max(0.0, float(row[entry_dict["MaxReturn"]])))
            iterations.append(int(row[entry_dict["Iteration"]]))

fig = plt.figure()
plt.scatter(iterations, rewards)
plt.xlabel('Iteration')
plt.ylabel('MaxReturn')
fig.savefig('Data/Plot/' + 'cartpole_gaInterPopulationEvolve.pdf')
plt.close(fig)
