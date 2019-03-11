#!/usr/bin/python
# -*- coding: utf-8 -*-

import tensorflow as tf
import pickle
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from tensorflow.python.ops import rnn, rnn_cell
import pandas as pd
import math
import os
from flask import current_app
from flaskresponse.filter.utils import dump_data, retrieve_data, retrieve_results

lemmatizer = WordNetLemmatizer()
tf.reset_default_graph()
hm_epochs = 7
n_classes = 2
batch_size = 128
chunk_size = 51
n_chunks = 51
rnn_size = 128
total_batches = int(1600000 / batch_size)

x = tf.placeholder('float', [None, n_chunks, chunk_size])
y = tf.placeholder('float')


def neural_network_model(x):
    layer = {'weights': tf.Variable(tf.random_normal([rnn_size,
             n_classes])),
             'biases': tf.Variable(tf.random_normal([n_classes]))}

    x = tf.transpose(x, [1, 0, 2])
    x = tf.reshape(x, [-1, chunk_size])
    x = tf.split(x, n_chunks, 0)

    lstm_cell = rnn_cell.BasicLSTMCell(rnn_size, state_is_tuple=True)
    (outputs, states) = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

    output = tf.matmul(outputs[-1], layer['weights']) + layer['biases']

    return output


def use_neural_network(data):
    prediction = neural_network_model(x)
    path = os.path.join(current_app.root_path, 'static/pickles','lexicon-2500-2638.pickle')
    with open(path, 'rb') as f:
        lexicon = pickle.load(f)

    with tf.Session() as sess:
        polarity = []
        sess.run(tf.initialize_all_variables())
        saver = tf.train.Saver()
        path = os.path.join(current_app.root_path, 'static/models','model.ckpt')
        saver.restore(sess, path)
        for input_data in data:
            temp=[]
            if input_data == 'none':
                polarity.append(-1)
                continue
            for d in input_data:
                current_words = word_tokenize(d.lower())
                current_words = [lemmatizer.lemmatize(i) for i in
                             current_words]
                features = np.zeros(len(lexicon))

                # print(features.shape)

                for word in current_words:
                    if word.lower() in lexicon:
                        index_value = lexicon.index(word.lower())
                        features[index_value] += 1
                features = np.array(list(features))
                features = features.reshape((-1, n_chunks, chunk_size))
                result = sess.run(tf.argmax(prediction.eval(feed_dict={x: features.tolist()}),1))
                if result[0] == 1:
                    temp.append(1)
                elif result[0] == 0:
                    temp.append(0)
            polarity.append(temp)
    return polarity



def filter_level1():
    data = retrieve_data()
    polarity = use_neural_network(data[2]) 
    data.append(polarity)
    path = os.path.join(current_app.root_path, 'static/pickles','results.pickle')
    with open(path, "wb") as fp:
        pickle.dump(data,fp) 

    
    

filter_level1()



