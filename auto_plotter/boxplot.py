import warnings

import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from auto_plotter.utils import DataLoader


def create_boxplot(data, xlabels, boxlabels,
                   title=None, colors=None, hatches=None,
                   box_width=0.2, spacing=0.5,
                   color_map='rainbow',
                   patterns=('----', '||||', '\\\\\\','xxxx', '..', '+++'),
                   median_color='k', alpha=1,
                   ):

    '''
    Data format:
    - list of np arrays of size number of observations x n_groups x boxes_per_group
    - The list size must be equal to the number of plots
    '''

    n_plots = len(data)
    assert isinstance(data[0], (np.ndarray, DataLoader))
    n_groups = data[0].shape[1]
    boxes_per_group = data[0].shape[2]
    assert len(xlabels) == n_groups

    if colors is None or boxes_per_group != len(colors):
        msg = ('Colors not provided or number of colors '
               'and n_groups do not match, defaulting to '
               'random colors')
        warnings.warn(msg, UserWarning)

        import matplotlib

        cmap = matplotlib.cm.get_cmap(color_map)
        # remove alpha from cmap
        colors = [cmap(i)[:-1] for i in np.linspace(0, 1, num=boxes_per_group)]

    if hatches is None or boxes_per_group != len(colors):
        msg = ('Hatches not provided or number of hatches '
               'and n_groups do not match, defaulting to '
               'random hatches')
        warnings.warn(msg, UserWarning)

        import itertools

        hatches = ['']
        r = 1
        while len(hatches) < boxes_per_group:
            for i in itertools.combinations(patterns, r):
                hatches.append(''.join(i))
                if len(hatches) == boxes_per_group:
                    break
            r += 1


    fig, axs = plt.subplots(figsize=(9, n_plots*2.5), nrows=n_plots, ncols=1)
    if n_plots == 1:
        axs = [axs]

    start_positions = [0.5 + box_width]
    for i in range(n_groups - 1):
        last = start_positions[-1]
        p = round(last + boxes_per_group * box_width + spacing, 2)
        start_positions.append(p)

    x_ticks_pos = [(p + box_width + 0.05) for p in start_positions]

    for ax, data_ax in zip(axs, data):
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
        ax.set_xticklabels(xlabels, rotation=0, fontsize=10)
        plt.setp(ax.get_xticklabels(), visible=False)


    plt.setp(axs[-1].get_xticklabels(), visible=True)

    patches = []
    for color, hatch in zip(colors, hatches):
        patch = mpatches.Rectangle([0, 1], 3, 3, facecolor=color,
                                   edgecolor='k', lw=1, alpha=alpha,
                                   hatch=hatch)
        patches.append(patch)

    axs[-1].legend(patches, boxlabels, loc='lower center',
                   bbox_to_anchor=(0.5, -0.4), ncol=4, fancybox=True, fontsize=15)
    if title is not None:
        fig.tight_layout(rect=(0, 0.01, 1, 0.98))
        t = fig.suptitle(title, y=0.99)
    else:
        fig.tight_layout(rect=(0, 0.01, 1, 1))
    return fig
