from jikanpy import Jikan
import time
import random
import json

# Creating Jikan object
jikan = Jikan()

def get_top_anime_ids(num_pages=200):
    """
    Returns a list of anime IDs from MyAnimeList's top anime pages.
    
    Args:
        num_pages: Number of top anime pages to scrape anime IDs for. 
    """
    jikan = Jikan()
    mal_ids = []
    for i in range(0, num_pages+1):
        try:
            results = jikan.top(type='anime', page=i)['top']
            time.sleep(2 + 2*random.random()) #Jikan requests limit: 2 requests/sec
            for result in results:
                mal_ids.append(result['mal_id'])
        except:
            pass
    return mal_ids

def get_anime_info(mal_ids):
    """
    Creates json file with a list of dictionaries containing anime metadata from Jikan API
    
    Args:
        mal_ids: List of anime IDs from MyAnimeList
    """
    lst = []
    
    for i, mal_id in enumerate(mal_ids):
        try:
            anime = jikan.anime(mal_id)
            time.sleep(2 + 2*random.random()) #Jikan requests limit: 2 requests/sec
            lst.append(anime)
        except:
            pass
    
    with open(f'../data/top_anime.json', 'w') as anime_file:
        json.dump(lst, anime_file)

if __name__ == '__main__':
    top_anime_ids = get_top_anime_ids()
    get_anime_info(top_anime_ids)