import pandas as pd
import matplotlib.pyplot as plt 

times = list()
with open('results_analise.txt', 'r') as f:
    times.append(f.read().splitlines())

for i in times:
    for u in i:
        print(u)
    plt.plot(i)
    plt.ylabel('time ')
    plt.show()