# import the necessary packages
import os

# config
ORIG_BASE_PATH = '/content/drive/MyDrive/rcnn/INRIAPerson'
ORIG_TRAIN_ANNOT_PATH = os.path.sep.join([ORIG_BASE_PATH, "Train/annotations"])
ORIG_TEST_ANNOT_PATH = os.path.sep.join([ORIG_BASE_PATH, "Test/annotations"])
ORIG_TRAIN_POS_PATH = os.path.sep.join([ORIG_BASE_PATH, "Train/pos"])
ORIG_TEST_POS_PATH = os.path.sep.join([ORIG_BASE_PATH, "Test/pos"])
ORIG_TRAIN_NEG_PATH = os.path.sep.join([ORIG_BASE_PATH, "Train/neg"])
ORIG_TEST_NEG_PATH = os.path.sep.join([ORIG_BASE_PATH, "Test/neg"])

BASE_PATH = "/content/drive/MyDrive/rcnn/dataset"
TRAIN_PATH = os.path.sep.join([BASE_PATH, "Train"])
TRAIN_POS_PATH = os.path.sep.join([BASE_PATH, "Train/pos"])
TRAIN_NEG_PATH = os.path.sep.join([BASE_PATH, "Train/neg"])
TEST_PATH = os.path.sep.join([BASE_PATH, "Test"])
TEST_POS_PATH = os.path.sep.join([BASE_PATH, "Test/pos"])
TEST_NEG_PATH = os.path.sep.join([BASE_PATH, "Test/neg"])
TRAIN_ANNOT_DICT_PATH = os.path.sep.join([TRAIN_PATH, 
  "train_annot_dict.pickle"])
TEST_ANNOT_DICT_PATH = os.path.sep.join([TEST_PATH, "test_annot_dict.pickle"])


MAX_PROPOSALS = 2000
MAX_PROPOSALS_INFER = 200
INPUT_DIMS = (224, 224)

MAX_POSITIVE = 30
MAX_NEGATIVE = 10

MODEL_PATH = "/content/drive/MyDrive/rcnn/models"
ENCODER_PATH = "/content/drive/MyDrive/rcnn/label_encoder.pickle"
PLOT_PATH = "/content/drive/MyDrive/rcnn/plots"
MIN_PROBA = 0.99