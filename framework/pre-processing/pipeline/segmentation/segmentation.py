from toolz import interleave
import os, sys, json, progressbar
import pandas as pd
import segmentationUtils

# Current file path
current_path = os.path.dirname(os.path.abspath(__file__))
cfg_filename = current_path + '/../../config.json'

# Path to _output file
output_path = current_path + '/_output/'

# Path to input
input_path = current_path + '/../features-extraction/pre-segmentation_output/'

# Load file utils file
sys.path.append(current_path + '/../../utils')
import fileUtils

# Loads configuration file
with open(cfg_filename) as f:
  full_config = json.load(f)
  cfg = full_config["pipeline"]["segmentation"]

#########################
# Main                  #
#########################
files = fileUtils.load_files(input_path)

# Prepare output directory
fileUtils.build_output_directory(output_path)

print("\nStarting segmentation.")
pbar = fileUtils.initialize_progress_bar(len(files))

for idx, file in enumerate(files):
  pbar.update(idx)
  segmentationUtils.segmentate(file, input_path, output_path, cfg["window-size"], cfg["overlap"])

print("\nSegmentation completed.\n")
