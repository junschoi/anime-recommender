from jikanpy import Jikan
import time
import random
import json
import math

"""
Add MyAnimeList club ids to club_list variable.

Note: This script may run for several hours or even days depending on the number of total users in club_list. 
"""

# Create Jikan object
jikan = Jikan()

# List of clubs to scrape usernames from
club_list = [20081, 70668, 67029]

def get_club_count(club_list):
    """
    Returns a list of club member counts for each club in club_list.

    Args:
    ---
    club_list : List of MyAnimeList club ids.
    """
    member_count_list = []
    for club_id in club_list:
        try:
            club = jikan.club(club_id)
            time.sleep(2 + 2*random.random())
            member_count_list.append(club['members_count'])
        except:
            pass
    return member_count_list

def get_user_list(club_list, members_count_list):
    """
    Returns list of usernames from each club in club_list.

    Args:
    ---
    club_list : List of MyAnimeList club ids

    members_count_list : List of club member counts for each club in club_list
    (output from get_club_count function)
    """
    members_lst = []
    for club_id, count in zip(club_list, members_count_list):
        for i in range(1, math.ceil(count/36)+1):
            try:
                club_members = jikan.club(club_id, extension='members', page=i)
                time.sleep(2 + 2*random.random())
                for member in club_members['members']:
                    members_lst.append(member['username'])
            except:
                pass
    return members_lst

def get_user_scores(members_lst):
    """
    Stores user information of all users in members_lst as a json file in data directory.

    Args:
    ---
    members_lst : List of usernames from clubs in club_list
    (output from get_user_list function)
    """
    scores_lst = []
    for i, member in enumerate(members_lst):
        try:
            user_score = jikan.user(member, request='animelist')
            time.sleep(2 + 2*random.random())
            if i%100 == 0:
                print(i, member)
            scores_lst.append(user_score)
        except:
            pass
    
    with open(f'../data/user_lst.json', 'w') as anime_file:
        json.dump(scores_lst, anime_file)

if __name__ == '__main__':
    members_count_list = get_club_count(club_list=club_list)
    members_lst = get_user_list(club_list=club_list, members_count_list=members_count_list)
    get_user_scores(members_lst)