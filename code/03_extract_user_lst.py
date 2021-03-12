import pandas as pd
import re
import ijson

"""
Run this script after running scrape_user.py which creates a json containing users' anime lists. 
Make sure the filepath variable directs to the correct user_lst.json file in the data directory.

Note: ijson library is used for extracting information from user_lst.json file because the file may be very large.
"""

filepath = "../data/user_lst.json"

def extract_user_lst(filepath):
    """
    Reads user_lst.json created from `scrape_user.py` script, extracts animelist information,
    and stores the extracted information as `user_cleaned.csv` file in the data directory. 

    Args:
    ---
    filepath : Path to user_lst_date.json file in the data directory
    """
    items = ijson.items(open(filepath), 'item')

    data = []
    userRegex = re.compile(r"\/user\/(.+)\/animelist")

    for item in items:
        for anime in item['anime']:
            data.append(
                (
                userRegex.search(item['jikan_url']).group(1),
                anime['mal_id'],
                anime['title'],
                anime['score'],
                anime['type']
                )
            )

    columns = ['username', 'mal_id', 'title', 'score', 'type']
    user_df = pd.DataFrame(data, columns=columns)
    user_df.to_csv("../data/user_cleaned.csv", index=False)

if __name__ == '__main__':
    extract_user_lst(filepath)