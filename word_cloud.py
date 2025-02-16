#%%
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import circlify
import textwrap

def calculate_counts(df, column_name, pop_rep=False):
    global num_cols
    num_cols = df.shape[0]

    # Extract and clean the relevant column (removes "Other, please specify." if present)
    column = df[column_name].str.replace('Other, please specify.,', '', regex=False)

    # Split the column into individual entries (comma-separated values)
    column_split = column.str.split(r'\s,|(?<=[a-zA-Z.]),(?=[a-zA-Z])').explode().str.strip()

    # Simplify the text (you can add specific text-cleaning steps here if necessary)
    simplified_column = column_split.apply(simplify_text)

    # Count the occurrences of each unique entry
    column_counts = simplified_column.value_counts()

    if pop_rep is True:
        age_column_counts = count_categories_by_age(df, column_name, 'Q26 - Age: *')

        weighted_column_counts = weight_counts(age_column_counts, 'Q26 - Age: *')
        column_counts = weighted_column_counts.groupby(column_name).sum()['count'].sort_values(ascending=False)

    return column_counts

def visualise_column(df, column_name, pop_rep=False):
    """
    Visualises a single column (with comma-separated values) as bubbles based on the frequency of the entries.
    """
    column_counts = calculate_counts(df, column_name, pop_rep=pop_rep)

    # Generate the circles and plot
    circles, labels, column_counts, ax = setup_plot('Response Distribution (%)', column_counts)
    render_circles(circles, labels, column_counts, ax, 'percentage')

def count_categories_by_age(df, response_column, age_column):
    # Make a copy of the DataFrame
    df_clean = df.copy()
    df_clean = df_clean[[response_column, age_column]]
    df_clean = df_clean.loc[~df_clean[age_column].isin(['Under 16', 'Prefer not to say'])]

    # Remove the "Other, please specify.," text if present
    df_clean[response_column] = df_clean[response_column].str.replace('Other, please specify.,', '', regex=False)

    # Split the responses into a list; the regex accounts for comma separation with/without whitespace
    df_clean['response_list'] = df_clean[response_column].str.split(r'\s,|(?<=[a-zA-Z.]),(?=[a-zA-Z])')

    # Explode the list so that each response is its own row, keeping the corresponding age
    df_exploded = df_clean.explode('response_list')

    # Strip any extra whitespace and simplify the text (assuming simplify_text is defined)
    df_exploded[response_column] = df_exploded['response_list'].str.strip().apply(simplify_text)

    # Group by age and response, then count the occurrences
    grouped_counts = (
        df_exploded.groupby([age_column, response_column])
                  .size()
                  .reset_index(name='count')
    )

    return grouped_counts

def weight_counts(age_column_counts, age_column):
    population_proportions = {
        '16-24': 0.1362463486,
        '25-34': 0.1661635833,
        '35-44': 0.1630233690,
        '45-54': 0.1511927945,
        '55-64': 0.1359785784,
        '65-74': 0.1206426485,
        '75-84': 0.0901411880,
        '85+': 0.0335199611
    }

    # Calculate sample counts per age bracket
    sample_counts = age_column_counts.groupby(age_column)['count'].sum() / age_column_counts['count'].sum()

    # Compute weights
    weights = {age: population_proportions.get(age, 0) / sample_counts.get(age, 1)
               for age in population_proportions.keys()}

    # Apply weights to each row
    age_column_counts['count'] = age_column_counts.apply(lambda row: row['count'] * weights.get(row[age_column], 1), axis=1)

    return age_column_counts

# Function to process and simplify each technology entry
def simplify_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()

    # Process the text using spaCy
    # doc = nlp(text)
    #
    # Keep original words that are not stop words, not punctuation, and have more than 1 character
    # simplified_tokens = [token.text for token in doc if not token.is_stop and not token.is_punct and len(token.text) > 1]

    # Return the simplified sentence (joined back together)
    # return " ".join(simplified_tokens)
    return text

def setup_plot(column_name, column_counts):
    """
    Prepares the plot by calculating circle positions based on counts.
    """
    # Compute circle positions based on the counts
    circles = circlify.circlify(
        column_counts.tolist(),
        show_enclosure=False,
        target_enclosure=circlify.Circle(x=0, y=0, r=1)
    )

    # Reverse the circles to match the order of data
    circles = circles[::-1]

    # Create a figure and subplot
    fig, ax = plt.subplots(figsize=(10, 10))

    # Set the title
    ax.set_title(column_name)

    # Remove axes from the plot
    ax.axis('off')

    # Find axis boundaries
    lim = max(
        max(
            abs(circle.x) + circle.r,
            abs(circle.y) + circle.r,
        )
        for circle in circles
    )
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)

    # Labels for the circles (unique values in the column)
    labels = column_counts.index

    return circles, labels, column_counts, ax

def render_circles(circles, labels, column_counts, ax, format_type='percentage'):
    """
    Renders the circles (bubbles) with labels.
    """
    # Loop through each circle and label
    for circle, label, count in zip(circles, labels, column_counts):
        # Calculate the percentage of occurrences for the frequency-based visualization
        if format_type == 'percentage':
            percentage = count / num_cols * 100
            wrapped_label = textwrap.fill(f"{label}\n({percentage:.1f}%)", width=int(2 * circle.r * 50))
        elif format_type == 'ranking':
            # For rankings, display the actual average ranking value
            wrapped_label = textwrap.fill(f"{label}\n({1/count:.2f})", width=int(2 * circle.r * 50))

        # Get circle properties (x, y, radius)
        x, y, r = circle

        # Draw the circle
        ax.add_patch(plt.Circle((x, y), r, alpha=0.5, linewidth=2))

        # Annotate the circle with the wrapped label
        plt.annotate(
            wrapped_label,
            (x, y),
            va='center',
            ha='center',
            fontsize=10,  # Font size
            color='black'
        )

    # Display the plot
    plt.show()

def visualise_ranked_columns(df, columns):
    """
    Visualises bubbles based on **inverse** of average rankings for each category,
    while keeping the label as the **actual** average ranking.
    """
    global num_cols
    num_cols = df.shape[0]

    # Compute the average ranking for each category (column)
    average_rankings = [df[column_name].mean() for column_name in columns]

    # Take the inverse of the rankings for bubble size (lower rankings => bigger circles)
    inverse_rankings = [1 / avg for avg in average_rankings]

    # Create a Series with the inverse rankings and corresponding column labels
    column_counts = pd.Series(inverse_rankings, index=columns)

    # Generate the circles and plot
    circles, labels, column_counts, ax = setup_plot("Average Ranking", column_counts)
    render_circles(circles, labels, column_counts, ax, 'ranking')

# # Read the CSV file (replace with the correct path)
# df = pd.read_csv('data/all-responses.csv')
#
# # Visualise the single-column data (comma-separated values)
# visualise_column(df, 'Q4 - What technology would you like to see more of in our community? *\n\nPlease t...', True)
#
# # List of columns representing rankings
# columns = ['Q21_1 - Roads, footpaths, and cycle ways. ',
#        'Q21_4 - Rubbish and recycling services. ',
#        'Q21_5 - Building and planning. ',
#        'Q21_6 - Outdoor spaces, such as parks. ',
#        'Q21_7 - Public facilities, such as community centres.  ',
#        'Q21_8 - Drinking water, wastewater, and stormwater services. ',
#        'Q21_9 - Business licensing and compliance. ',
#        'Q21_10 - Community services, such as events. ']
# # Visualise the ranked data (inverse of average ranking for bubble size)
# visualise_ranked_columns(df, columns)
