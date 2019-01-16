from auto_plotter.boxplot import create_boxplot
from auto_plotter.utils import DataLoader

xlabels = ['dataset1', 'dataset2', 'dataset3', 'dataset4', 'dataset5']
ylabels = ['accuracy']
boxlabels = ['algorithm1', 'algorithm2', 'algorithm3', 'algorithm4', 'algorithm5',
             'algorithm6', 'algorithm7', 'algorithm8', 'algorithm9', 'algorithm10']

files = ['test_data/alg1.csv',
         'test_data/alg2.csv',
         'test_data/alg3.csv',
         'test_data/alg4.csv',
         'test_data/alg4.csv',
         'test_data/alg1.csv',
         'test_data/alg2.csv',
         'test_data/alg3.csv',
         'test_data/alg4.csv',
         'test_data/alg4.csv']

dl = DataLoader(files, alg_names=boxlabels)

fig = create_boxplot(dl, xlabels, ylabels, title=None)
fig.savefig('resulting_plots/test_boxplot.pdf')

