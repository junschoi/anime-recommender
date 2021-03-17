import numpy as np
import pandas as pd
import json
import os
from flask import Flask, request, render_template
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

path = os.getcwd()

app = Flask(__name__)

# Main dataframe
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

# Content-based recommender
tf_synop = TfidfVectorizer(stop_words='english', ngram_range=(1,2), min_df=10)
tf_synop_matrix = tf_synop.fit_transform(df['synopsis'])
genre_matrix = df['genres'].str.get_dummies(sep=',').to_numpy()
matrix = np.concatenate((tf_synop_matrix.toarray(), genre_matrix), axis=1)
cosine_sim_content = pd.DataFrame(cosine_similarity(matrix, matrix), index=df['title'], columns=df['title'])

# Collaborative recommender
user_df = pd.read_csv("../data/user_cleaned.csv")
user_df = user_df.loc[user_df['type']=='TV']
user_df = user_df.drop_duplicates(subset=['username', 'title'], keep='first')
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
cosine_sim_collab = pd.DataFrame(cosine_similarity(pivot, pivot), index=pivot.index, columns=pivot.index)

# Flask app
@app.route('/')
def page():
    return render_template('index.html')

@app.route('/results', methods=['POST', 'GET'])
def recommend():
    if request.method == 'POST':
        inputs =  request.form
        anime = str(inputs['anime'])
        collab_level = float(inputs['slider'])

        try:
            message = 'Top Recommendations'
            weighted_df = pd.merge(left=cosine_sim_content[anime], right=cosine_sim_collab[anime], on='title')
            weighted_df['weighted_sim'] = weighted_df.iloc[:, 0] * (1-collab_level) + weighted_df.iloc[:, 1] * collab_level
            final_df = pd.merge(left=df, right=weighted_df['weighted_sim'], left_on='title', right_on=weighted_df['weighted_sim'].index)

            ret = final_df.sort_values(by='weighted_sim', ascending=False)[['image_url', 'url', 'title', 'score', 'rating', 'status', 'premiered', 'trailer_url', 'weighted_sim']][1:51]
            ret['weighted_sim'] = np.round(ret['weighted_sim'], 4)
            ret.columns = ['Image', 'URL', 'Title', 'Score', 'Rating', 'Status', 'Premiered', 'Trailer', 'Weighted Similarity']
        except:
            message = 'Please enter the exact anime title.'
            ret = pd.DataFrame()
    
    return render_template(
        'results.html',
        message = message,
        collab_level = collab_level,
        column_names = ret.columns.values,
        row_data = list(ret.values.tolist()),
        image_column = 'Image',
        trailer_column = 'Trailer',
        url_column = 'URL',
        zip=zip
        )

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = '4000'
    app.run(HOST, PORT)