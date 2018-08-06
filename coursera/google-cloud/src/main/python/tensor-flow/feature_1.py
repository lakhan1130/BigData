%bash
git clone https://github.com/GoogleCloudPlatform/training-data-analyst
rm -rf training-data-analyst/.git

import math
import shutil
import numpy as np
import pandas as pd
import tensorflow as tf

print(tf.__version__)
tf.logging.set_verbosity(tf.logging.INFO)
pd.options.display.max_rows = 10
pd.options.display.float_format = '{:.1f}'.format

df = pd.read_csv("https://storage.googleapis.com/ml_universities/california_housing_train.csv", sep=",")


df.describe()


np.random.seed(seed=1) #makes result reproducible
msk = np.random.rand(len(df)) < 0.8
traindf = df[msk]
evaldf = df[~msk]

def add_more_features(df):
  df['avg_rooms_per_house'] = df['total_rooms'] / df['households'] #expect positive correlation
  df['avg_persons_per_room'] = df['population'] / df['total_rooms'] #expect negative correlation
  return df
  
  
  # Create pandas input function
def make_input_fn(df, num_epochs):
  return tf.estimator.inputs.pandas_input_fn(
    x = add_more_features(df),
    y = df['median_house_value'] / 100000, # will talk about why later in the course
    batch_size = 128,
    num_epochs = num_epochs,
    shuffle = True,
    queue_capacity = 1000,
    num_threads = 1
  )
  
  
  
  # Define your feature columns
def create_feature_cols():
  return [
    tf.feature_column.numeric_column('housing_median_age'),
    tf.feature_column.bucketized_column(tf.feature_column.numeric_column('latitude'), boundaries = np.arange(32.0, 42, 1).tolist()),
    tf.feature_column.numeric_column('avg_rooms_per_house'),
    tf.feature_column.numeric_column('avg_persons_per_room'),
    tf.feature_column.numeric_column('median_income')
  ]
  
  
  
# Define your feature columns
def create_feature_cols():
  return [
    tf.feature_column.numeric_column('housing_median_age'),
    tf.feature_column.bucketized_column(tf.feature_column.numeric_column('latitude'), boundaries = np.arange(32.0, 42, 1).tolist()),
    tf.feature_column.numeric_column('avg_rooms_per_house'),
    tf.feature_column.numeric_column('avg_persons_per_room'),
    tf.feature_column.numeric_column('median_income')
  ]
  
  
  
  # Launch tensorboard
from google.datalab.ml import TensorBoard

OUTDIR = './trained_model'
TensorBoard().start(OUTDIR)


# Run the model
shutil.rmtree(OUTDIR, ignore_errors = True)
train_and_evaluate(OUTDIR, 2000)