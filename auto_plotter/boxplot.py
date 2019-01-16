import warnings

import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from auto_plotter.utils import DataLoader


COLOR_MAPS = {'Greys': 'from white to black',
              'rainbow': 'the colors of the rainbow',
              'cool': 'aesthetic feeling from light blue to light purple',
              'Spectral': 'from red to blue but simetric (zero is white)'}


def create_boxplot(data, xlabels, ylabels, boxlabels,
                   title=None,
                   box_width=0.2, spacing=0.5,
                   colors=None,
                   color_map='Greys',
                   patterns=None,
                   patterns_map=('----', '||||', '\\\\\\','xxxx', '..', '+++'),
                   median_color='k', alpha=1.0,
                   ):

    '''
    Creates a boxplot using the data provided

    args:
        - data (DataLoader/iterable): DataLoader object or iterable of DataLoader
            objects containing the data for each plot

        - xlabels (iterable): labels for each group of boxes

        - ylabels (iterable): labels for each plot

        - boxlabels (iterable): labels for each box (added to legend)

        - boxwidth (float): width of each box

        - spacing (float): space between box groups

        - colors (iterable): iterable of color names
            (optional and has precedence over color_map)

        - color_map (str): name of matplotlib color_map from matplotlib to use
            (if colors is provided, this is ignored)

        - patterns (iterable): iterable of patterns for the box hatches
            (optional and has precedence over patterns_map)

        - patterns_map (iterable): iterable of patterns to generate hatches for the boxes
            (if patterns is provided, this is ignored)

        - median_color (str): color of the median line for the boxes

        - alpha (float): transparency value of the boxes

    '''

    import collections

    if not isinstance(data, collections.Iterable) or isinstance(data, DataLoader):
        data = [data]

    n_plots = len(data)
    assert isinstance(data[0], (np.ndarray, DataLoader))
    n_groups = data[0].shape[1]
    boxes_per_group = data[0].shape[2]
    assert len(boxlabels) == boxes_per_group
    assert len(xlabels) == n_groups
    assert len(ylabels) == n_plots

    msg = None
    if colors is None:
        msg = ('Colors not provided defaulting to color map')
    elif len(colors) != boxes_per_group:
        msg = ('Number of colors and n_groups do not match, '
               'defaulting to color map')
    if msg:
        warnings.warn(msg, UserWarning)

        import matplotlib

        cmap = matplotlib.cm.get_cmap(color_map)
        # remove alpha from cmap
        colors = [cmap(i)[:-1] for i in np.linspace(0, 1, num=boxes_per_group)]


    msg = None
    if patterns is None:
        msg = ('Patterns not provided defaulting to color map')
    elif len(patterns) != boxes_per_group:
        msg = ('Number of patterns and n_groups do not match, '
               'defaulting to pattern map')
    if msg:
        warnings.warn(msg, UserWarning)

        import itertools

        hatches = ['']
        r = 1
        while len(hatches) < boxes_per_group:
            for i in itertools.combinations(patterns_map, r):
                hatches.append(''.join(i))
                if len(hatches) == boxes_per_group:
                    break
            r += 1

    fig, axes = plt.subplots(figsize=(9, n_plots*2.5), nrows=n_plots, ncols=1)
    if n_plots == 1:
        axes = [axes]

    start_positions = [spacing + box_width]
    for i in range(n_groups - 1):
        last = start_positions[-1]
        p = round(last + boxes_per_group * box_width + spacing, 2)
        start_positions.append(p)

    box_range = (box_width + 0.05) * boxes_per_group - 0.05 - (2 * box_width / 2)
    x_ticks_pos = [(p + box_range / 2) for p in start_positions]

    for ax, data_ax, ylabel in zip(axes, data, ylabels):
        positions = start_positions.copy()

        right_lim = 0
        for dim, color, hatch in zip(range(data_ax.shape[2]), colors, hatches):
            d = data_ax[:, :, dim]
            if dim != 0:
                positions = [round(p + box_width + 0.05, 2) for p in positions]

            bp = ax.boxplot(d, positions=positions, widths=[box_width]*n_groups,
                            patch_artist=True, sym='.')

            for box in bp['boxes']:
                box.set_color((*color,alpha))
                box.set_hatch(hatch)
                box.set_edgecolor((0, 0, 0, 1))

            for median in bp['medians']:
                median.set(color=median_color)

            right_lim = max(right_lim, max(positions))

        ax.set_xlim(left=0, right=right_lim+0.5)
        ax.set_xticks(x_ticks_pos)
        ax.set_ylabel(ylabel)
        plt.setp(ax.get_xticklabels(), visible=False)

    axes[-1].set_xticklabels(xlabels, rotation=0, fontsize=10)
    plt.setp(axes[-1].get_xticklabels(), visible=True)

    patches = []
    for color, hatch in zip(colors, hatches):
        patch = mpatches.Rectangle([0, 1], 3, 3, facecolor=color,
                                   edgecolor='k', lw=1, alpha=alpha,
                                   hatch=hatch)
        patches.append(patch)

    fig.legend(patches, boxlabels, loc='lower center', ncol=4, fancybox=True, fontsize=15)

    if title is not None:
        fig.tight_layout(rect=(0, 0.01, 1, 0.98))
        fig.suptitle(title, y=0.99)
    else:
        fig.tight_layout(rect=(0, 0.20, 1, 1))
    return fig
