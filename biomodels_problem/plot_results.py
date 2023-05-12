import seaborn as sns
import matplotlib.pyplot as plt
import os, numpy, pandas
from matplotlib.colors import to_rgba

df = pandas.read_csv("results_no_copasi.csv")
labels = list(set(df['Tool'].to_list()))

# remove copasi data
labels = [i for i in labels if 'copasi' not in i.lower()]
# df = df[df['Tool'].isin(labels)]

colours = [to_rgba(i) for i in ["black", 'grey', 'white']*3]
# print(colours)
fig = plt.figure()
ax = sns.barplot(
    data=df, x="Tool", y='Time (sec)', units="Repeat",
    linewidth=1.0, edgecolor='black', hue='Mode',
    palette=colours
)
# plt.xticks( rotation=75)
sns.despine(fig=fig)
plt.legend(loc=(0.3, 0.6))
plt.xlabel("")
fname = os.path.join(os.path.dirname(__file__), "biomodels_problem_results.png")
plt.savefig(fname, dpi=250, bbox_inches='tight')
