# NSUPS-Banner
NSUPS-banner unlike the name suggests, is **not** a banner in the conventional sense of the word.

It is a basic selenium based web crawler created for NSUPS (North South University Problem Solvers) to track the participation of contestants in Bootcamp.

It takes in a url `(i.e: https://nsups.github.io/s17)` of the bootcamp shown below.



![image](https://github.com/salmandotexe/nsups-banner/assets/29581454/5157f3de-2add-46a4-b31d-8bc4c3ab3825)

It parses the `<table>` data and returns it as a `Pandas Dataframe` that can be used to perfrom data analysis on:



![image](https://github.com/salmandotexe/nsups-banner/assets/29581454/49b1387f-ed2b-4755-8afd-6df64ce0d5c8)

## Requirements
Python 3.9 is used. The `requirements.txt` file contains the dependencies for the following:
```
pandas==2.2.2
selenium==4.19.0
```

## Usage
Create a python virtual environment using

`python -m venv .venv`

Activate the virtual environment and run 

`pip install -r requirements.txt`

Specify url inside of main.py

`url = 'https://nsups.github.io/s17'`

Run `main.py`

## Example
If we want to return a list of participants with less than 90% solves in the **last four contests**:

```
THRESHOLD = 90
last_4_columns = df.columns[-4:]

for column in last_4_columns:
    filtered_df[column] = filtered_df[column].str.extract(r'(\d+\.\d+)').astype(float)

# Filtering participants with less than THRESHOLD % in any of the last 4 contests

filtered_participants = filtered_df[(filtered_df[last_4_columns] < THRESHOLD).any(axis=1)]['Participants'].tolist()
print(f"Participants with less than {THRESHOLD}% in any of the last 4 contests: {len(filtered_participants)} people\n")

for p in filtered_participants:
    print(p)
```

## Acknowledgements
Shout out to [Tahmid](https://github.com/withtahmid) and [Mahir](https://github.com/mahirshahriar1) for their amazing work in creating the solve tracker.

Thanks to North End Coffee Roasters for their great coffee.

And last but not least,
Thanks to Season 17 of the NSUPS Bootcamp for not only making this project possible, but necessary.
