import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt
import tensorflow as tf

from utils.train_utils import *

def main():

    tensor_train_features, tensor_train_labels, tensor_test_features, tensor_test_labels, tensor_valid_features, tensor_valid_labels = load_iotensor()

    # train the model with optimal hyperparameters
    tuner = tuning_dnn_model()
    best_hps = tuner.get_best_hyperparameters()[0]
    dnn_model = dnn_model_builder(best_hps)

    # retrain the best dnn model
    stop_early = EarlyStopping(monitor='val_loss', patience=10)
    history = dnn_model.fit(tensor_train_features, tensor_train_labels, epochs=100,  validation_data=(tensor_valid_features, tensor_valid_labels),callbacks=[stop_early])
    # save the loss/accuracy progress curves to assets/training_progress
    training_progress(history, 'dnn')

    # check test set
    test_loss, test_acc = dnn_model.evaluate(tensor_test_features,  tensor_test_labels, verbose=1)
    print('\nTest accuracy:', test_acc)
    print('Test loss:', test_loss)

    # predict the results for all data set
    train_predictions = dnn_model.predict(tensor_train_features)
    valid_predictions = dnn_model.predict(tensor_valid_features)
    test_predictions = dnn_model.predict(tensor_test_features)

    # save prediction results ro asset/prediction_results
    prediction_matrix(tensor_train_labels, train_predictions, 'dnn', 'train')
    prediction_matrix(tensor_valid_labels, valid_predictions, 'dnn', 'valid')
    prediction_matrix(tensor_test_labels, test_predictions,'dnn', 'test')
    

if __name__ == "__main__":
    main()