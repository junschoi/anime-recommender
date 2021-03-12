import pandas as pd
import json
import os
from flask import Flask, request, render_template
from sklearn.metrics.pairwise import cosine_similarity

path = os.getcwd()

app = Flask(__name__)

# Reading top anime data
# ----------------------
with open('../data/top_anime.json') as f:
    data = json.load(f)

columns = [
    'mal_id',
    'url',
    'image_url',
    'trailer_url',
    'title',
    'title_japanese',
    'type',
    'source',
    'episodes',
    'status',
    'rating',
    'score',
    'rank',
    'popularity',
    'members',
    'favorites',
    'synopsis',
    'premiered',
    'studios',
    'genres'
]

df = pd.DataFrame(columns=columns)

for col in columns:
    if not col in ['studios', 'genres']:
        df[col] = [ele[col] for ele in data]
    else:
        df[col] = [','.join([ele['name'] for ele in anime[col]]) for anime in data]

df = df.loc[df['type']=='TV']
df = df.drop_duplicates(subset='mal_id', keep='last')
df = df.loc[~df['score'].isnull()]
df['synopsis'] = df['synopsis'].fillna('')

# Collaborative recommender
# -------------------------
user_df = pd.read_csv("../data/user_cleaned.csv")
user_df = user_df.loc[user_df['type']=='TV'] # Excluding non-TV animes

# Creating pivot table
pivot = user_df.pivot_table(values='score', index='title', columns='username')
pivot = pivot.dropna(axis=0, how='all')
pivot = pivot.fillna(0)

include_anime = []
drop_anime = []
for title in user_df['title'].unique():
    if title in df['title'].unique():
        include_anime.append(title)
    else:
        drop_anime.append(title)
pivot = pivot.drop(drop_anime)

# Creating item_sim_df using cosine_similarity
item_sim_df = pd.DataFrame(cosine_similarity(pivot, pivot), index=pivot.index, columns=pivot.index)


@app.route('/')
def page():
    return render_template('page.html')

@app.route('/results', methods=['POST', 'GET'])
def recommend():
    if request.method == 'POST':
        inputs =  request.form
        anime = str(inputs['anime'])

        try:
            message = 'Top 20 Recommendations'
            ret = item_sim_df[anime].sort_values(ascending=False)[1:20].to_html()
        except:
            message = 'Please enter the exact anime title.'
            ret = ''
    
    return render_template(
        'results.html',
        ret=ret,
        message = message
        )

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = '4000'
    app.run(HOST, PORT, debug=True)