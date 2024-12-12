#!/usr/bin/env python
# coding: utf-8

# In[11]:


from IPython.core.display import Markdown
from language_processing import identify_themes
from word_cloud import visualise_column, visualise_ranked_columns
from bar_charts import stacked_bars, grouped_bars, Scale

import pandas as pd
import warnings

from bs4 import MarkupResemblesLocatorWarning
warnings.filterwarnings('ignore')

def visualise_responses(age_brackets, gender):
    df = pd.read_csv('data/all-responses.csv')
    # print(df.columns)

    df = df[df['Q26 - Age: *'].isin(age_brackets)]
    df = df[df['Q27 - Gender: *'].isin(gender)]

    def question_1():
        display(Markdown("## Existing technology aware of:"))
        visualise_column(df, "Q3 - We already have some council provided community technology in place. Which...")

    def question_2():
        display(Markdown("## Technology would you like to see more of, and how likely are you to use them:"))
        visualise_column(df, 'Q4 - What technology would you like to see more of in our community? *\n\nPlease t...')
        # identify_themes(df, 'Q4_11_TEXT - Other, please specify.')
        columns = ["Q5 - If these types of technologies were made available to the community, how li..."]
        stacked_bars(df, columns, Scale.LIKELY)

    def question_3():
        display(Markdown("## How important are the following outcomes:"))
        columns = ['Q7 - Technology should be accessible and help people feel included, safe, and co...',
           'Q8 - Technology should help preserve and protect our environment and make counci...',
           'Q9 - Technology should enable council to plan thriving town centres, resilient i...',
           'Q10 - Technology should make it easy to move around our city and use sustainable...',
           'Q11 - Technology should drive business growth and education opportunities, creati...']
        stacked_bars(df, columns, Scale.IMPORTANT)

    def question_4():
        display(Markdown("## How important that technology improves the following:"))
        columns = ['Q13 - Traffic congestion. *',
           'Q14 - A revitalised city centre. *',
           'Q15 - Reliable and timely public transport. *',
           'Q16 - Public safety. *',
           'Q17 - Visibility of available parking. *',
           'Q18 - Staying informed and providing feedback on council decisions. *']
        stacked_bars(df, columns, Scale.IMPORTANT)
        # identify_themes(df, 'Q19 - Other, please specify')

    def question_5():
        display(Markdown("## Ranking of preferred improvements with technology:"))
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
        # identify_themes(df, 'Q21_11_TEXT - Other, please specify')

    def question_6():
        display(Markdown("## Preventing use of technology:"))
        visualise_column(df, "Q22 - Is there anything preventing you from using technology in our community’s o...")
        # identify_themes(df, 'Q22_10_TEXT - Other, please specify.')

    def question_7():
        display(Markdown("## Ideas and examples from other cities:"))
        identify_themes(df, "Q23 - Do you have any ideas for new technology or examples you\'ve seen from other...")

    def question_8():
        display(Markdown("## Feedback about Council or technology:"))
        identify_themes(df, "Q24 - Do you have any other feedback or comments you would like to make about cou...")

    def question_9():
        display(Markdown("## Rate digital skills:"))
        columns = ["Q25 - How would you rate your digital skills when using community technology? *..."]
        stacked_bars(df, columns, Scale.SKILL)

    question_1()
    question_2()
    question_3()
    question_4()
    question_5()
    question_6()
    question_7()
    question_8()
    question_9()

# visualise_responses(['Under 16', '16-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75-84', '85+'], ['Male', 'Female', 'Prefer not to say', 'Other (please specify)', 'Non-binary'])


# In[12]:


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

