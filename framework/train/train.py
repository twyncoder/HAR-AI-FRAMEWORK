import utils.utils as utils
import tensorflow as tf 
import re, os, json
import importlib

# main_path = os.getcwd()
main_path = '/TFG'
final_input_path = main_path + '/framework/final-dataset/orientation/'
_, _, files = next(os.walk(final_input_path))

#########################
#  Main train function  #
#########################
def train_main(cfg: json, outcome_path:str):

# Load configuration data
  rows, columns, channels, movements, batch_size, train_steps, validation_steps, test_steps, epochs = utils.extract_info_from_config(cfg)

# Create filenames lists for datasets
  train_set, validation_set, test_set = utils.split_dataset(files, cfg)

# # Balance datasets
#   train_set = utils.balance_data_set(train_set, cfg, "training")
#   validation_set = utils.balance_data_set(validation_set, cfg, "validation")
#   test_set = utils.balance_data_set(test_set, cfg, "test")

# Create datasets from tensorflow custom data generators
  if channels == 1:
    train_dataset, test_dataset, test_dataset_prediction, validation_dataset = \
    utils.load_one_dimension_datasets(final_input_path, train_set, test_set, validation_set, batch_size, movements, rows, columns, channels, outcome_path)
  elif channels == 4:
    train_dataset, test_dataset, test_dataset_prediction, validation_dataset = \
      utils.load_four_dimension_datasets(final_input_path, train_set, test_set, validation_set, batch_size, movements, rows, columns, channels, outcome_path)

# Load model
  nn = importlib.import_module('neuralNetworks.' + cfg["neural-network"])
  model = nn.load_model(rows, columns, channels, len(movements))

# Add callbacks to model
  callbacks = []
  bestWeightsPath = outcome_path + '/best_weights'
  if cfg["callbacks"]["enabled"]:
    callbackList, modelCheckPoint = utils.addCallbacks(cfg["callbacks"]["list"], callbacks, bestWeightsPath)

# Fit model
  history_callback = model.fit(train_dataset, validation_data = validation_dataset, steps_per_epoch = train_steps,
          validation_steps = validation_steps, epochs = epochs, callbacks = callbacks)

# Evaluation & prediction phases
  if modelCheckPoint:
    model.load_weights(bestWeightsPath)
    test_loss, test_accuracy = model.evaluate(test_dataset, steps = test_steps)
    prediction = model.predict(test_dataset_prediction, steps = test_steps)
  else:
    test_loss, test_accuracy = model.evaluate(test_dataset, steps = test_steps)
    prediction = model.predict(test_dataset_prediction, steps = test_steps)

  return model, test_loss, test_accuracy, prediction, history_callback
