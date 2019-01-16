from auto_plotter.boxplot import create_boxplot
from auto_plotter.utils import DataLoader

xlabels = ['dataset1', 'dataset2', 'dataset3', 'dataset4', 'dataset5']
ylabels = ['metric1', 'metric2', 'metric3']
boxlabels = ['algorithm1', 'algorithm2', 'algorithm3', 'algorithm4', 'algorithm5']

files = ['test_data/alg1.csv',
         'test_data/alg2.csv',
         'test_data/alg3.csv',
         'test_data/alg4.csv',
         'test_data/alg4.csv',]

dl = DataLoader(files, alg_names=boxlabels)

fig = create_boxplot([dl] * 3, xlabels, ylabels, title=None, color_map='cool')
fig.savefig('plots/test_boxplot5.png')

