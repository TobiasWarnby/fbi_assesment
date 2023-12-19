# Extract

# Importing the liberys i need to get api, and transfoming it.

import requests
from pprint import pprint
import pandas as pd

# get the most wanted file from fictional FBI.
res = requests.get("https://api.fbi.gov/wanted/v1/list")
#convert to json
data = res.json()


#Transforme.

# create a list than i later can append the transformed data.
data_filtered = []

# extract the keys and values i whant to have in the data_filtered 
for person in data['items']:
    person_data = {
        "Name": person.get('title'),
        "Date of Birth": person.get('dates_of_birth_used'),
        "Race": person.get('race'),
        "Sex": person.get('sex'),
        "Last seen": person.get('age_min'),
        "Nationality": person.get('nationality'),
        "Eyes": person.get('eyes')
    }
    data_filtered.append(person_data)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data_filtered)

# remove the ARMED CARJACKING and HATE CRIME, it had no walues.
df = df[~df["Name"].isin(["ARMED CARJACKING", "HATE CRIME"])]

# Convert the "Last seen" column to integers, and only have the year, the oringinal was in [april, 17, 1999] 
df["Date of Birth"] = df["Date of Birth"].apply(lambda x: int(x[0][-4:]) if x is not None else None)




#load to the db and i don't want a index
df.to_csv('db_fbi/fbi.csv', index=False)

#Save and run the pipline in the terminal - python fbi_pipline.py