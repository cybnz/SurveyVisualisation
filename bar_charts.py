#%%
from matplotlib import pyplot as plt
from enum import Enum
import plotly.express as px
import pandas as pd

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

class Colours(Enum):
    FIVE = ["#FF0000", "#FF7F7F", "#7F7F7F", "#7F7FFF", "#0000FF"]
    SEVEN = ["#FF0000", "#FF5555", "#FFAAAA", "#7F7F7F", "#AAAAFF", "#5555FF", "#0000FF"]

import pandas as pd

def compute_age_weights(df, age_col='Q26 - Age: *'):
    # Filter out unwanted age responses.
    df_filtered = df[~df[age_col].isin(["Prefer not to say", "Under 16"])].copy()

    # Calculate sample counts and proportions for each age bracket.
    sample_counts = df_filtered[age_col].value_counts()
    total_sample = sample_counts.sum()
    sample_proportions = sample_counts / total_sample

    # Define the target population proportions.
    population_proportions = {
        '16-24': 0.1362463486,
        '25-34': 0.1661635833,
        '35-44': 0.1630233690,
        '45-54': 0.1511927945,
        '55-64': 0.1359785784,
        '65-74': 0.1206426485,
        '75-84': 0.0901411880,
        '85+':   0.0335199611
    }

    # Calculate weight for each age bracket: population proportion / sample proportion.
    age_weights = {}
    for age, pop_prop in population_proportions.items():
        sample_prop = sample_proportions.get(age, 0)
        if sample_prop > 0:
            age_weights[age] = pop_prop / sample_prop
        else:
            age_weights[age] = 0  # or handle appropriately if no respondents in the age bracket

    return age_weights

def stack_counts(df, columns, scale, pop_rep=True):
    if pop_rep is True:
        # Keep only the desired columns plus the age column.
        df_subset = df[columns + ['Q26 - Age: *']].copy()
        # Filter out rows with "Prefer not to say" or "Under 16"
        df_subset = df_subset[~df_subset["Q26 - Age: *"].isin(["Prefer not to say", "Under 16"])].copy()

        # Compute age weights using the helper function.
        age_weights = compute_age_weights(df_subset, age_col='Q26 - Age: *')

        # Melt the dataframe so each row is one response with its age.
        df_long = pd.melt(df_subset,
                          id_vars='Q26 - Age: *',
                          var_name='question',
                          value_name='response')

        # Map the weight for each row based on its age.
        df_long['weight'] = df_long['Q26 - Age: *'].map(age_weights)

        # Group by question and response to sum the weights.
        weighted_counts = df_long.groupby(['question', 'response'])['weight'].sum().unstack(fill_value=0)
        counts_df = weighted_counts
    else:
        # If not applying population representative weighting,
        # just count occurrences of each response for each question.
        df_subset = df[columns].copy()
        df_long = pd.melt(df_subset, var_name='question', value_name='response')
        counts_df = pd.crosstab(df_long['question'], df_long['response'], dropna=False)

    # Reorder columns according to the scale (assuming scale.value is an ordered list)
    counts_df = counts_df[scale.value]

    # Convert counts to percentages (each row sums to 1)
    counts_df = counts_df.div(counts_df.sum(axis=1), axis=0)

    return counts_df

def insert_line_break(text, char_num):
    result = []
    
    while len(text) > char_num:
        # Find the last space before or at the 40th character
        space_index = text.rfind(' ', 0, char_num)
        
        if space_index == -1:  # No space found, force break at 40
            space_index = char_num
        else:
            space_index += 1  # Include the space in the cut
        
        result.append(text[:space_index].rstrip())  # Add substring before the break
        text = text[space_index:].lstrip()  # Remove processed part and leading space
    
    result.append(text)  # Add remaining text
    return '<br>'.join(result)

def stacked_bars(df, columns, scale, pop_rep=True):
    counts_df = stack_counts(df, columns, scale, pop_rep=pop_rep)
    
    # Break up long question labels
    counts_df.index = counts_df.index.map(lambda text: insert_line_break(text, 40))

    if len(scale.value) == 5:
        colours = Colours.FIVE.value
    elif len(scale.value) == 7:
        colours = Colours.SEVEN.value

    # Create figure
    fig = px.bar(counts_df, x=scale.value, color_discrete_sequence=colours)
    fig.update_xaxes(tickformat=",.2%", title_text="Response Distribution (%)")
    fig.update_yaxes(title_text="Issue")
    fig.update_layout(legend_title="Response Category")
    fig.show()

def ranking_counts(df, columns):
    df = df[columns]
    # Create a DataFrame to store counts of ranking positions
    rankings = pd.DataFrame(index=df.columns, columns=range(1, len(columns)))

    # Count how many times each ranking value occurs for each issue
    for col in df.columns:
        rankings.loc[col] = [df[col].tolist().count(i) for i in range(1, len(columns))]

    return rankings

def grouped_bars(df, columns):
    # Get the counts of rankings per issue using the provided function.
    rankings = ranking_counts(df, columns)
    rankings.index = rankings.index.map(lambda text: insert_line_break(text, 30))
    # rankings now has issues as its index and ranking positions (1, 2, …, len(columns)-1) as its columns.

    # Reset the index to convert the issue names into a column.
    rankings_reset = rankings.reset_index().rename(columns={'index': 'Service'})
    
    # Convert the data from wide to long format.
    # Each row will have an Issue, a Ranking, and the corresponding Count.
    rankings_long = rankings_reset.melt(
        id_vars='Service',
        var_name='Ranking',
        value_name='Count'
    )
    
    # Create the grouped bar chart using Plotly Express.
    fig = px.bar(
        rankings_long,
        x="Service",
        y="Count",
        color="Ranking",
        barmode="group",  # This places the ranking bars side-by-side for each issue.
        labels={
            "Service": "Service",
            "Count": "Count of ranking",
            "Ranking": "Ranking".format(len(columns)-1)
        }
    )
    
    # Rotate x-axis labels for clarity, especially if issue names are long.
    fig.update_layout(xaxis_tickangle=-45, height=600)
    
    fig.show()

def average_bars(df, columns):
    df = df[columns]

    # Calculate the average ranking for each category (mean of each column)
    average_rankings = df.mean()

    # Sort the rankings for better visualization
    average_rankings_sorted = average_rankings.sort_values()

    # Plotting
    plt.figure(figsize=(10, 6))
    average_rankings_sorted.plot(kind='bar')

    # Customize the chart
    plt.xlabel('Issue')
    plt.ylabel('Average Ranking')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Show the plot
    plt.show()

df = pd.read_csv('data/all-responses-CLEANED.csv')
stacked_bars(df, ['Traffic congestion.',
           'A revitalised city centre.',
           'Reliable and timely public transport.',
           'Public safety.',
           'Visibility of available parking.',
           'Staying informed and providing feedback on council decisions.'],
            Scale.IMPORTANT)
# columns = ['Roads, footpaths, and cycle ways.',
#            'Rubbish and recycling services.',
#            'Building and planning.',
#            'Outdoor spaces, such as parks.',
#            'Public facilities, such as community centres.',
#            'Drinking water, wastewater, and stormwater services.',
#            'Business licensing and compliance.',
#            'Community services, such as events.']
# grouped_bars(df, columns)
# average_bars(df, ['Q21_1 - Roads, footpaths, and cycle ways. ',
#        'Q21_4 - Rubbish and recycling services. ',
#        'Q21_5 - Building and planning. ',
#        'Q21_6 - Outdoor spaces, such as parks. ',
#        'Q21_7 - Public facilities, such as community centres.  ',
#        'Q21_8 - Drinking water, wastewater, and stormwater services. ',
#        'Q21_9 - Business licensing and compliance. ',
#        'Q21_10 - Community services, such as events. '])