#!/usr/bin/env python
# coding: utf-8

# In[1]:


from word_cloud import visualise_column, visualise_ranked_columns
from bar_charts import stacked_bars, grouped_bars, Scale

import pandas as pd

def visualise_responses(age_brackets, gender):
    df = pd.read_csv('data/all-responses.csv')
    # print(df.columns)

    df = df[df['Q26 - Age: *'].isin(age_brackets)]
    df = df[df['Q27 - Gender: *'].isin(gender)]

    print("Existing technology aware of:")
    visualise_column(df, "Q3 - We already have some council provided community technology in place. Which...")

    print("Technology would you like to see more of, and how likely are you to use them:")
    visualise_column(df, 'Q4 - What technology would you like to see more of in our community? *\n\nPlease t...')
    columns = ["Q5 - If these types of technologies were made available to the community, how li..."]
    stacked_bars(df, columns, Scale.LIKELY)

    print("How important are the following outcomes:")
    columns = ['Q7 - Technology should be accessible and help people feel included, safe, and co...',
       'Q8 - Technology should help preserve and protect our environment and make counci...',
       'Q9 - Technology should enable council to plan thriving town centres, resilient i...',
       'Q10 - Technology should make it easy to move around our city and use sustainable...',
       'Q11 - Technology should drive business growth and education opportunities, creati...']
    stacked_bars(df, columns, Scale.IMPORTANT)

    print("How important that technology improves the following:")
    columns = ['Q13 - Traffic congestion. *',
       'Q14 - A revitalised city centre. *',
       'Q15 - Reliable and timely public transport. *',
       'Q16 - Public safety. *',
       'Q17 - Visibility of available parking. *',
       'Q18 - Staying informed and providing feedback on council decisions. *']
    stacked_bars(df, columns, Scale.IMPORTANT)

    print("Ranking of preferred improvements with technology:")
    columns = ['Q21_1 - Roads, footpaths, and cycle ways. ',
       'Q21_4 - Rubbish and recycling services. ',
       'Q21_5 - Building and planning. ',
       'Q21_6 - Outdoor spaces, such as parks. ',
       'Q21_7 - Public facilities, such as community centres.  ',
       'Q21_8 - Drinking water, wastewater, and stormwater services. ',
       'Q21_9 - Business licensing and compliance. ',
       'Q21_10 - Community services, such as events. ']
    grouped_bars(df, columns)
    visualise_ranked_columns(df, columns)

    print("Preventing use of technology:")
    visualise_column(df, "Q22 - Is there anything preventing you from using technology in our community’s o...")


    # ideas and examples

    # feedback about council or technology

    print("Rate digital skills:")
    columns = ["Q25 - How would you rate your digital skills when using community technology? *..."]
    stacked_bars(df, columns, Scale.SKILL)


# In[2]:


import ipywidgets as widgets

# Create checkbox widgets for age brackets and gender
age_brackets_widget = widgets.SelectMultiple(
    options=['Under 16', '16-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75-84', '85+'],
    value=['Under 16', '16-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75-84', '85+'],
    description='Age Brackets:',
    disabled=False
)

gender_widget = widgets.SelectMultiple(
    options=['Male', 'Female', 'Prefer not to say', 'Other (please specify)', 'Non-binary'],
    value=['Male', 'Female', 'Prefer not to say', 'Other (please specify)', 'Non-binary'],
    description='Gender:',
    disabled=False
)

widgets.interactive(visualise_responses, age_brackets=age_brackets_widget, gender=gender_widget)

