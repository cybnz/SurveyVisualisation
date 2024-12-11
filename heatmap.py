#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('data/all-responses.csv')
df = df.loc[:, 'Q21_1 - Roads, footpaths, and cycle ways. ':'Q21_11 - Other, please specify']

# Plot heatmap
sns.heatmap(df, cmap='Blues_r', cbar_kws={'label': 'Ranking'})

# Customize plot labels and title
plt.xlabel('Issues')
plt.yticks(ticks=[], labels=[])

# Show plot
plt.show()

