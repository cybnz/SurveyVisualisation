#!/usr/bin/env python
# coding: utf-8

# In[52]:


import pandas as pd

# Load the dataset
df = pd.read_csv('data/dashboard-export-02-51-am-2024-11-30.csv')
df = df[df["Q28 - The University of Waikato and Tauranga City Council are undertakinga resear..."] == "Yes"]

# Define a mapping for age brackets to numeric values for easier processing
age_map = {
    'Under 16': 0,
    '16-24': 1,
    '25-34': 2,
    '35-44': 3,
    '45-54': 4,
    '55-64': 5,
    '65-74': 6,
    '75-84': 7,
    '85+': 8,
    'Prefer not to say': 9  # Handle 'Prefer not to say' category
}

age_brackets = ['16-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75-84', '85+']

# Apply the mapping to the 'Age' column
df['Age_Num'] = df['Q26 - Age: *'].map(age_map)

# Number of groups you want to create
num_groups = 4

# Number of people in each group
group_size = 5

df["Group_Num"] = "None"

# Create empty groups
groups = {i: [] for i in range(num_groups)}

current_group = 0
current_age = 1 # Skip under 16s
# For each group, add the youngest person until the groups are full
# Results in spread of ages in each group (16-24 is added to group 0, then group 1, etc)
for i in range(len(age_map)):
    for _, row in df.iterrows():
        if row['Age_Num'] == current_age and len(groups[current_group]) < group_size:
            row['Group_Num'] = current_group # Assign group number
            groups[current_group].append(row) # Add person to group
            current_group = (current_group + 1) % num_groups

    current_age = current_age + 1

# Print the people in each group
for group_num, group_members in groups.items():
    print(f"Group {group_num}:")
    for person in group_members:
        fname = person['Q29 - First name: *']
        lname = person['Q30 - Last name: *']
        age = person['Q26 - Age: *']
        gender = person['Q27 - Gender: *']

        print(f"  {fname} {lname}, {age}, {gender}")

    # Show demographics in group
    group_df = pd.concat(group_members) # Convert to Pandas series to perform calc
    print((group_df['Q27 - Gender: *'].value_counts(normalize=True) * 100).to_string(index=True))
    print((group_df['Q26 - Age: *'].value_counts(normalize=True).reindex(age_brackets, fill_value=0) * 100).to_string(index=True)) # Include missing ages
    print()  # Add a blank line between groups

unassigned = df[df['Group_Num'] == "None"]

