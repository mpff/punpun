"""
Filename: server.py
"""


import os
import pickle
import pandas

from animerec import utils
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/predict', methods=['POST', 'GET'])
def apicall():
    """ API Call  """

    try:
        user = request.args.get('username')
    except Exception as e:
        raise e
    
    if user is None:
        return(bad_request())
    else:
        print("Loading item ids...")
        ids = None
        with open("./model/item-id.pickle", 'rb') as f:
            ids = pickle.load(f)

        print("Scraping MyAnimeList profile...")
        p = utils.get_user_anime_list(user)
        x = utils.get_score_vector_from_user_anime_list(p, ids)

        print("Loading pickled model...")
        model = None
        with open('./model/model.pickle', 'rb') as f:
            model = pickle.load(f)

        print("Predicting anime scores...")
        rhat = model.predict(x)

        print("Loading anime metadata...")
        meta = None
        with open("./model/meta.pickle", 'rb') as f:
            meta = pickle.load(f)
        meta.index = meta['anime_id']
        meta = meta[ ['title', 'type', 'premiered', 'genre'] ]

        print("Merging metadata and prediction...")
        prediction = utils.prediction_to_dataframe(rhat, p, ids, keep_all=False)
        prediction = pandas.DataFrame(prediction)
        prediction.columns = ['score']
        prediction = prediction.join(meta)
        prediction = prediction.sort_values(by='score',ascending=False).head(5)

        response = jsonify(predictions=prediction.to_json(orient='records'))
        response.status_code=200

        return(response)

