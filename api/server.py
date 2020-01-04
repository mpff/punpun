"""
Filename: server.py
"""


import os
import pickle
import pandas
import numpy
from scipy.sparse import csc_matrix

from animerec import utils
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/predict', methods=['POST','GET'])
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

        print("Loading model...")
        model = None
        with open('./model/model.pickle', 'rb') as f:
            model = pickle.load(f)

        print("Predicting anime scores...")
        x = csc_matrix(numpy.nan_to_num(numpy.array([x])))
        rhat = model.predict(x)[0,:]

        print("Merging metadata and prediction...")
        prediction = [{'anime_id': i, 'score': s} for i,s in zip(ids,rhat)]
        animelist = [
            {'anime_id': a['id_ref'], 
             'status': a['status'], 
             'score': a['score']} for a in p]

        print("Packing json response...")
        response = jsonify(prediction=prediction, animelist=animelist)
        response.status_code=200

        print("Serve predictions.")
        return(response)

