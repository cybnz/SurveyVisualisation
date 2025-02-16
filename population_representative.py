#%%
from IPython.core.display import Markdown
from word_cloud import visualise_column, visualise_ranked_columns
from bar_charts import stacked_bars, grouped_bars, Scale, average_bars, percent_bars

import pandas as pd
import warnings

from bs4 import MarkupResemblesLocatorWarning
warnings.filterwarnings('ignore')

def visualise_responses(age_brackets, gender):
    df = pd.read_csv('data/all-responses-CLEANED.csv')

    df = df[df['Q26 - Age: *'].isin(age_brackets)]
    df = df[df['Q27 - Gender: *'].isin(gender)]

    def question_1():
        display(Markdown("## We already have some council provided community technology in place. Which of the following are you aware of?"))
        percent_bars(df, "We already have some council provided community technology in place. Which of the following are you aware of?", pop_rep=True)

    def question_2():
        display(Markdown("## What technology would you like to see more of in our community?"))
        percent_bars(df, 'What technology would you like to see more of in our community?', pop_rep=True)
        display(Markdown("### If these types of technologies were made available to the community, how likely would you be to use them in your daily life?"))
        columns = ["If these types of technologies were made available to the community, how likely would you be to use them in your daily life?"]
        stacked_bars(df, columns, Scale.LIKELY, pop_rep=True)

    def question_3():
        display(Markdown("## How important is it to you that technology helps provide the following outcomes for our community?"))
        columns = ['Technology should be accessible and help people feel included, safe, and connected.',
           'Technology should help preserve and protect our environment and make council operations more sustainable.',
           'Technology should enable council to plan thriving town centres, resilient infrastructure, and suitable community facilities.',
           'Technology should make it easy to move around our city and use sustainable transport choices.',
           'Technology should drive business growth and education opportunities, creating jobs, and a skilled workforce in Tauranga.']
        stacked_bars(df, columns, Scale.IMPORTANT, pop_rep=True)

    def question_4():
        display(Markdown("## How important is it to you that technology helps improve the following?"))
        columns = ['Traffic congestion.',
           'A revitalised city centre.',
           'Reliable and timely public transport.',
           'Public safety.',
           'Visibility of available parking.',
           'Staying informed and providing feedback on council decisions.']
        stacked_bars(df, columns, Scale.IMPORTANT, pop_rep=True)

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
        average_bars(df, columns, pop_rep=True)

    def question_6():
        display(Markdown("## Is there anything preventing you from using technology in our community's outdoor spaces or public facilities?"))
        percent_bars(df, "Is there anything preventing you from using technology in our community’s outdoor spaces or public facilities?", pop_rep=True)

    def question_9():
        display(Markdown("## How would you rate your digital skills when using community technology?"))
        columns = ["How would you rate your digital skills when using community technology?"]
        stacked_bars(df, columns, Scale.SKILL, pop_rep=True)

    question_1()
    question_2()
    question_3()
    question_4()
    question_5()
    question_6()
    question_9()

visualise_responses(['Under 16', '16-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75-84', '85+'], ['Male', 'Female', 'Prefer not to say', 'Other (please specify)', 'Non-binary'])