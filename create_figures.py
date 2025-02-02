#!/usr/bin/env python
# coding: utf-8

# In[1]:


from IPython.core.display import Markdown
from language_processing import identify_themes
from word_cloud import visualise_column, visualise_ranked_columns
from bar_charts import stacked_bars, grouped_bars, Scale

import pandas as pd
import warnings

from bs4 import MarkupResemblesLocatorWarning
warnings.filterwarnings('ignore')

def visualise_responses(age_brackets, gender):
    df = pd.read_csv('data/all-responses-CLEANED.csv')
    # print(df.columns)

    df = df[df['Q26 - Age: *'].isin(age_brackets)]
    df = df[df['Q27 - Gender: *'].isin(gender)]

    def question_1():
        display(Markdown("## We already have some council provided community technology in place. Which of the following are you aware of?"))
        visualise_column(df, "We already have some council provided community technology in place. Which of the following are you aware of?")

    def question_2():
        display(Markdown("## What technology would you like to see more of in our community?"))
        visualise_column(df, 'What technology would you like to see more of in our community?')
        # identify_themes(df, 'Q4_11_TEXT - Other, please specify.')
        display(Markdown("### If these types of technologies were made available to the community, how likely would you be to use them in your daily life?"))
        columns = ["If these types of technologies were made available to the community, how likely would you be to use them in your daily life?"]
        stacked_bars(df, columns, Scale.LIKELY)

    def question_3():
        display(Markdown("## How important is it to you that technology helps provide the following outcomes for our community?"))
        columns = ['Technology should be accessible and help people feel included, safe, and connected.',
           'Technology should help preserve and protect our environment and make council operations more sustainable.',
           'Technology should enable council to plan thriving town centres, resilient infrastructure, and suitable community facilities.',
           'Technology should make it easy to move around our city and use sustainable transport choices.',
           'Technology should drive business growth and education opportunities, creating jobs, and a skilled workforce in Tauranga.']
        stacked_bars(df, columns, Scale.IMPORTANT)

    def question_4():
        display(Markdown("## How important is it to you that technology helps improve the following?"))
        columns = ['Traffic congestion.',
           'A revitalised city centre.',
           'Reliable and timely public transport.',
           'Public safety.',
           'Visibility of available parking.',
           'Staying informed and providing feedback on council decisions.']
        stacked_bars(df, columns, Scale.IMPORTANT)
        # identify_themes(df, 'Q19 - Other, please specify')

    def question_5():
        display(Markdown("## Thinking about the following council services, in which order (from first to last) would you like to see them improved through the use of technology?"))
        columns = ['Roads, footpaths, and cycle ways.',
           'Rubbish and recycling services.',
           'Building and planning.',
           'Outdoor spaces, such as parks.',
           'Public facilities, such as community centres.',
           'Drinking water, wastewater, and stormwater services.',
           'Business licensing and compliance.',
           'Community services, such as events.']
        grouped_bars(df, columns)
        visualise_ranked_columns(df, columns)
        # identify_themes(df, 'Q21_11_TEXT - Other, please specify')

    def question_6():
        display(Markdown("## Is there anything preventing you from using technology in our community's outdoor spaces or public facilities?"))
        visualise_column(df, "Is there anything preventing you from using technology in our community’s outdoor spaces or public facilities?")
        # identify_themes(df, 'Q22_10_TEXT - Other, please specify.')

    def question_7():
        display(Markdown("## Do you have any ideas for new technology or examples you\'ve seen from other cities that could benefit our community?"))
        identify_themes(df, "Q23 - Do you have any ideas for new technology or examples you\'ve seen from other...")

    def question_8():
        display(Markdown("## Do you have any other feedback or comments you would like to make about council or community technology?"))
        identify_themes(df, "Q24 - Do you have any other feedback or comments you would like to make about cou...")

    def question_9():
        display(Markdown("## How would you rate your digital skills when using community technology?"))
        columns = ["How would you rate your digital skills when using community technology?"]
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

visualise_responses(['Under 16', '16-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75-84', '85+'], ['Male', 'Female', 'Prefer not to say', 'Other (please specify)', 'Non-binary'])


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

