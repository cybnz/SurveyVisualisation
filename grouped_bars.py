#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/all-responses.csv')

def grouped_bars(df):

    df = df.loc[:, 'Q21_1 - Roads, footpaths, and cycle ways. ':'Q21_10 - Community services, such as events. ']
    # Create a DataFrame to store counts of rankings (1 through 9)
    ranking_counts = pd.DataFrame(index=df.columns, columns=range(1, 9))

    # Count how many times each ranking (1-9) occurs for each issue
    for col in df.columns:
        ranking_counts.loc[col] = [df[col].tolist().count(i) for i in range(1, 9)]

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 8))

    # Create grouped bar plot (issues grouped together on x-axis)
    ranking_counts.plot(kind='bar', ax=ax, width=0.8)

    # Adding labels and title
    ax.set_ylabel('Count of Rankings')
    ax.set_xlabel('Issues')

    # Rotate x-axis labels for clarity
    ax.set_xticklabels(ranking_counts.index, rotation=45, ha='right')

    # Adding legend
    ax.legend(title='Most important to least important', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.show()

grouped_bars(df)

