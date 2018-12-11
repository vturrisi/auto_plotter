from auto_plotter.boxplot import create_boxplot
from auto_plotter.utils import DataLoader

xlabels = ['dataset1', 'dataset2', 'dataset3', 'dataset4', 'dataset5']
boxlabels = ['alg1', 'alg2', 'alg3', 'alg4']

dl = DataLoader(['test_data/alg1.csv', 'test_data/alg2.csv',
                 'test_data/alg3.csv', 'test_data/alg4.csv'])

fig = create_boxplot([dl] * 3, xlabels, boxlabels, title=None)
fig.savefig('resulting_plots/test_boxplot.pdf')

