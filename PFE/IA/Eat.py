# notation matrix :
# -nice  
# -severly toxic
# -threat
# -racism

# tokenization of comments, ex : you suck, I'm coming for you
# attributes : [42, 8, 56]

import os
import pandas as p
import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import TextVectorization
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Bidirectional, Dense, Embedding

# TRAINNIG ###########

data = p.read_csv('jigsaw-toxic-comment-train.csv') 

#print(data[data.columns[2:]].iloc[6])

X = data['comment_text'].values # comments
Y = data[data.columns[2:]].values # toxicity evalution for each comment
MAX_FEATURES = 200000 # number of words in our tokenized vocab

vectorizer = TextVectorization(max_tokens=MAX_FEATURES, output_sequence_length=1800, output_mode='int') # sequence length : comment maximum length
vectorizer.adapt(X) # on construit notre vocab qui va être compris par le deep learning

vectorized_text = vectorizer(X)
dataset = tf.data.Dataset.from_tensor_slices((vectorized_text, Y)) # on donne les données qui sont mappées par Y (les colonnes)
dataset = dataset.cache() #
dataset = dataset.shuffle(160000)
dataset = dataset.batch(16)
dataset = dataset.prefetch(8) # helps prevent bottlenecks

batch_X, batch_y = dataset.as_numpy_iterator().next()

train = dataset.take(int(len(dataset)*.8))
val = dataset.skip(int(len(dataset)*.8)).take(int(len(dataset)*.2))

train_generator = train.as_numpy_iterator()
train_generator.next() # on passe au prochain batch
# en soit, on apprend à l'IA les propriétés d'un mot, que lorsqu'il est utilisé de cette manière, dans ce contexte c'est pas bien.

# Building the IA
model = Sequential()
model.add(Embedding(MAX_FEATURES+1, 32))
model.add(Bidirectional(LSTM(32, activation='tanh')))
model.add(Dense(128, activation='relu'))
model.add(Dense(256, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(6, activation='sigmoid')) # on a 6 critère de toxicité combiné

model.compile(loss="BinaryCrossentropy", optimizer="Adam")
model.summary()

history = model.fit(train, epochs=1, validation_data=val) # recommanded 5-10 epochs

model.save("toxic.keras") # we saved the model