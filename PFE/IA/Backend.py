import os
import pandas as p
import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import TextVectorization
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Bidirectional, Dense, Embedding
from bottle import route, run, template, get, post, request, response, app
import json
MAX_FEATURES = 200000 # number of words in our tokenized vocab

model = tf.keras.models.load_model('toxic.keras')
data = p.read_csv('jigsaw-toxic-comment-train.csv') #p.read_csv('jigsaw-toxic-comment-train.csv')

#print(data[data.columns[2:]].iloc[6])

X = data['comment_text'].values # comments

for i in range(0, len(X)):
    X[i] = X[i].upper().lower()
Y = data[data.columns[2:]].values # toxicity evalution for each comment
MAX_FEATURES = 200000 # number of words in our tokenized vocab

vectorizer = TextVectorization(max_tokens=MAX_FEATURES, output_sequence_length=1800, output_mode='int') # sequence length : comment maximum length
vectorizer.adapt(X) # on construit notre vocab qui va être compris par le deep learning

# score_comment : is it toxic or not, we get as output a text report about different level of toxicity
def score_comment(comment):
    vectorized_comment = vectorizer([comment])
    result = model.predict(vectorized_comment)

    text = ''
    for idx, col in enumerate(["toxic","severe_toxic","obscene","threat","insult","identity_hate"]):
        text += '{}: {}\n'.format(col, result[0][idx] > 0.5)
    return text

# the API and point, we go through this URI via an URL for instance http://127.0.0.1/istoxic/moderate
# and we get as a response the toxicity detail.
@post('/istoxic/moderate')
def send():
    message = request.body.read().decode("utf-8")
    print("Message : ",message)
    return score_comment(message.upper().lower())
run(host='localhost', port=7777)