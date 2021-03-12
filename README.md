# Anime Recommender

## Table of Contents

- [Problem Statement](#Problem-Statement)
- [Executive Summary](#Executive-Summary)
- [Project Directory](#Project-Directory)
- [Data Collection](#Data-Collection)
- [EDA](#EDA)
- [Modeling](#Modeling)
- [Conclusion](#Conclusion)
- [References](#References)

---

# Problem Statement

[MyAnimeList](https://myanimelist.net/), often abbreviated as MAL, is an anime and manga social networking and social cataloging application website run by volunteers.<sup>[1]</sup> Although the website has a great amount of anime data, it lacks a data driven recommender system. The current recommendation section is just a list of user recommendation submissions (e.g. "If you like anime 'X', you will like anime 'Y'"), which are often very subjective and limited in the number of recommendations per anime title. So I decided to create a recommender system using the users' list of anime scores (collaborative filtering) and anime metadata (content-based recommender using NLP on genres and synopsis description). The goal is to provide better recommendations to MyAnimeList users via flask app.

# Executive Summary

I created a hybrid of content-based and collaborative item-item recommender using the data scraped from MyAnimeList. The content based recommender is created from a vectorized matrix using anime titles' genres and synopsis description. Cosine similarity scores are calculated from this vectorized matrix, and the recommendations are generated based on similarity scores. Similarly, the collaborative recommender is created from a pivot table of scores with anime title indices and username columns. Cosine similarity scores are calculated from this pivot table, and the collaborative recommendations are generated based on similarity scores. The flask app allows the user to choose the weight on the collaborative recommender, and the final recommendations are shown based on the weighted similarity scores.

# Project Directory

NOTE: `data` directory is not included in this repository because some data files exceed over 100 MB (github's maximum file size limit).

```
📜README.html
📜requirements.txt
📦app
┣ 📂templates
┃ ┣ 📜page.html
┃ ┗ 📜results.html
┗ 📜main.py
📦code
┣ 📜01_scrape_anime.py
┣ 📜02_scrape_user.py
┣ 📜03_extract_user_lst.py
┣ 📜notebook.ipynb
📦data
┣ 📜top_anime.json
┣ 📜user_cleaned.csv
┗ 📜user_lst.json
```

# Setup

1. Clone this repo
2. Run `01_scrape_anime.py` in `code` directory
3. Run `02_scrape_user.py` in `code` directory
4. Run `03_extract_user_lst.py` in `code` directory
5. Run `main.py` in `app` directory to host flask app

# Data Collection

I used a library called `jikanpy` which is a Python wrapper for [Jikan API](https://jikan.docs.apiary.io/#), an open-source PHP & REST API for MyAnimeList. Due to request limits in Jikan API, scraping scripts have 2-4 second delays between requests.

First, I created a script called `01_scrape_anime.py` which scrapes anime metadata from top 10,000 animes (by average review score). This script saves a json file called `top_anime.json` in the data directory, and this file is used for creating the content-based recommender. This script may run for several hours.

Then, I created a script called `02_scrape_user.py` which scrapes users' information including each specific user's anime review scores. **Important note:** Jikan API does not provide a complete list of usernames, but it allows you to get a list of usernames from specific "clubs" in MyAnimeList. The three clubs that I chose to get the list of usernames are:

- [Recommendation Club](https://myanimelist.net/clubs.php?cid=20081)
- [The Newbie Club](https://myanimelist.net/clubs.php?cid=20081)
- [Anime Paradise Club (A.P.C.)](https://myanimelist.net/clubs.php?cid=67029)

The main reason for choosing these clubs is that these clubs are very neutral in anime preference. However, I must acknowledge that anime preference of the users from these clubs may not be a good overall representation of anime preference of the total MyAnimeList userbase. Therefore, the collaborative recommender may be somewhat biased towards animes liked by users in the clubs mentioned above. If you wish to change the list of clubs to scrape usernames from, you can do so by editing `club_list` variable in `02_scrape_user.py` file in the code directory. The output of this script is `user_lst.json` file, and the file may be several gigabytes in size, and the script may run for several days depending on the total number of usernames for all the clubs in `club_list` variable.

Finally, I created a script called `03_extract_user_lst.py` which extracts core information from `user_lst.json` file created from `02_scrape_user.py`. Because `user_lst.json` file is very large (over 4.5 GB), it's not possible to load the json file using the standard `json` library with limited memory. Therefore, I had to use the `ijson` library which allows you to parse through the json file to collect certain information. The output of this script is `user_cleaned.csv` file which is used for creating the collaborative recommender.

# Exploratory Data Analysis

In progress

# Modeling

In progress

# Conclusion

In progress

# References

\[1\]: https://en.wikipedia.org/wiki/MyAnimeList
