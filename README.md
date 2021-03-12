# Anime Recommender

## Table of Contents

- [Problem Statement](#Problem-Statement)
- [Executive Summary](#Executive-Summary)
- [Project Directory](#Project-Directory)
- [Data Collection](#Data-Collection-and-Cleaning)
- [EDA](#EDA)
- [Modeling](#Modeling)
- [Conclusion](#Conclusion)
- [References](#References)

---

# Problem Statement

MyAnimeList, often abbreviated as MAL, is an anime and manga social networking and social cataloging application website run by volunteers. ^[1] Although the website has a great amount of anime data, it lacks a data driven recommender system. The current recommendation section is just a list of user recommendation submissions (e.g. "If you like anime 'X', you will like anime 'Y'"), which are often very subjective and limited in the number of recommendations per anime title. Therefore, I decided to create a recommender system using the users' list of anime scores (collaborative filtering) and anime metadata (content-based recommender using NLP on genres and synopsis description). The goal is to provide better recommendations to MyAnimeList users.

# Executive Summary

I created a hybrid of content-based and collaborative recommender using the data scraped from MyAnimeList. The content based recommender is created from a vectorized matrix using anime titles' genres and synopsis description. Cosine similarity scores are calculated from this vectorized matrix, and the recommendations are generated based on these vales.

# Project Directory

NOTE: `user_lst_03092021.json` file is not in this repository because it is a very large file (4.51 GB)

```
📜README.html
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
┗ 📜user_lst_03092021.json
```

# Data Dictionary

# Data Collection and Cleaning

# Exploratory Data Analysis

# Modeling

# Conclusion

# References
