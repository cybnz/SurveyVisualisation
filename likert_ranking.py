#!/usr/bin/env python
# coding: utf-8

# In[41]:


import plot_likert
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum

class Scale(Enum):
    LIKELY = ['Very unlikely ',
             'Unlikely ',
             'Neutral ',
             'Likely ',
             'Very likely ']
    IMPORTANT = ['Not at all important',
                 'Not important',
                 'Neutral',
                 'Important',
                 'Very important']
    SKILL = ['Very low',
             'Low',
             'Somewhat low',
             'Neutral',
             'Somewhat high',
             'High',
             'Very high']

def setup_likert(df, start_column, end_column, scale):
    plot_likert.__internal__.BAR_LABEL_FORMAT = "%.0f"

    # Use .loc to slice the dataframe by column names
    ax = plot_likert.plot_likert(df.loc[:, start_column:end_column], scale.value, plot_percentage=True, bar_labels=True, bar_labels_color="snow", colors=plot_likert.colors.default_with_darker_neutral);

    return ax

def balanced_figure(df, start_column, end_column, scale):
    ax = setup_likert(df, start_column, end_column, scale)

    ax.set_xlim(left=-100, right=100)

    # Set custom x-ticks at specific intervals
    ticks = np.arange(-100, 101, 20)  # Example: ticks every 20 units
    ax.set_xticks(ticks)

    # Optional: Set custom tick labels (if you want to change the appearance of labels)
    tick_labels = [f'{tick}%' for tick in ticks]  # Label them as percentages
    ax.set_xticklabels(tick_labels)

    plt.show()

def unbalanced_figure(df, start_column, end_column, scale):
    setup_likert(df, start_column, end_column, scale)

    plt.show()

