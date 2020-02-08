import requests
import pandas as pd
from bs4 import BeautifulSoup
import os.path as path

if not path.exists("./data_tmp/table.html"):
    print("download html file")
    r = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")
    with open("./data_tmp/table.html", "wb") as f:
        f.write(r.content)

soup = BeautifulSoup(open('./data_tmp/table.html'), 'lxml')
postcodes_table = soup.find("table", {"class": "wikitable sortable"})

postcodes = []
boroughs = []
neighbourhoods = []

for row in postcodes_table.find_all('tr')[1:]:
    postcode_cell = row.find_all('td')[0]
    borough_cell = row.find_all('td')[1]
    neighbourhood_cell = row.find_all('td')[2]

    postcodes.append(postcode_cell.text.strip())
    boroughs.append(borough_cell.text.strip())
    neighbourhoods.append(neighbourhood_cell.text.strip())

df = pd.DataFrame(
    {
        'PostalCode': postcodes,
        'Borough': boroughs,
        "Neighborhood": neighbourhoods
    }
)

# STEP 2 clean the dataframe

#  Only process the cells that have an assigned borough.
#  Ignore cells with a borough that is Not assigned.
df = df[df.Borough != "Not assigned"]


def map_not_assigned_neighborhoods(row):
    if row.Neighborhood == "Not assigned":
        row.Neighborhood = row.Borough

    return row


df = df.apply(lambda x: map_not_assigned_neighborhoods(x), axis=1)

# More than one neighborhood can exist in one postal code area.
# For example, in the table on the Wikipedia page, you will notice that
# M5A is listed twice and has two neighborhoods: Harbourfront and Regent Park.
# These two rows will be combined into one row with the neighborhoods separated
# with a comma as shown in row 11 in the above table.
df.set_index('PostalCode', drop=False, inplace=True)
df_post_codes = df.PostalCode.unique()

for code in df_post_codes:
    candidate_for_duplicate = df.loc[code]
    # size must be above 3 because its a series item
    if candidate_for_duplicate.size > 3:
        str_neighbourhood = ", ".join(candidate_for_duplicate['Neighborhood'])
        df.loc[code, "Neighborhood"] = str_neighbourhood

df.drop_duplicates('PostalCode', inplace=True)

print(df.shape)
########################
# PART 2
if not path.exists("./data_tmp/geo_data.csv"):
    print("download  csv file")
    r = requests.get("https://cocl.us/Geospatial_data")
    with open("./data_tmp/geo_data.csv", "wb") as f:
        f.write(r.content)

csv_data = pd.read_csv("./data_tmp/geo_data.csv")

# I will merge the Frames on the PostalCode Column
csv_data.rename(columns={"Postal Code": "PostalCode"}, inplace=True)
# Lets remove the PostalCode index - merge won't work else
df.reset_index(level="PostalCode", drop=True, inplace=True)
df = pd.merge(df, csv_data, on="PostalCode")

print(df)
