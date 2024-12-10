#!/usr/bin/env python
# coding: utf-8

# In[1]:


from word_cloud import visualise_column
from stacked_bars import display_bars, Scale

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
import pandas as pd

df = pd.read_csv('data/all-responses.csv')
# print(df.columns)

print("Existing technology aware of:")
visualise_column(df, "Q3 - We already have some council provided community technology in place. Which...")

print("Technology would you like to see more of, and how likely are you to use them:")
visualise_column(df, 'Q4 - What technology would you like to see more of in our community? *\n\nPlease t...')
columns = ["Q5 - If these types of technologies were made available to the community, how li..."]
display_bars(df, columns, Scale.LIKELY)

print("How important are the following outcomes:")
columns = ['Q7 - Technology should be accessible and help people feel included, safe, and co...',
       'Q8 - Technology should help preserve and protect our environment and make counci...',
       'Q9 - Technology should enable council to plan thriving town centres, resilient i...',
       'Q10 - Technology should make it easy to move around our city and use sustainable...',
       'Q11 - Technology should drive business growth and education opportunities, creati...']
display_bars(df, columns, Scale.IMPORTANT)

print("How important that technology improves the following:")
columns = ['Q13 - Traffic congestion. *', 'Q14 - A revitalised city centre. *',
       'Q15 - Reliable and timely public transport. *',
       'Q16 - Public safety. *', 'Q17 - Visibility of available parking. *',
       'Q18 - Staying informed and providing feedback on council decisions. *']
display_bars(df, columns, Scale.IMPORTANT)

# ranking

print("Preventing use of technology:")
visualise_column(df, "Q22 - Is there anything preventing you from using technology in our community’s o...")

# ideas and examples

# feedback about council or technology

print("Rate digital skills:")
columns = ["Q25 - How would you rate your digital skills when using community technology? *..."]
display_bars(df, columns, Scale.SKILL)


# In[ ]:




