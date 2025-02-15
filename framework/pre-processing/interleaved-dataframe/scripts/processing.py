from toolz import interleave
import os
import pandas as pd
import json
import shutil 

# Porject main directory path
# main_path = os.getcwd()
main_path = '/TFG'

# Loads configuration file
cfg_filename = main_path + '/framework/pre-processing/config.json'
with open(cfg_filename) as f:
  full_config = json.load(f)
  cfg = full_config["in-dt"]

# Path to _output file
output_path = main_path + '/framework/pre-processing/interleaved-dataframe/_output/'
zippedoutput_path = main_path + '/framework/pre-processing/interleaved-dataframe/_output-zipped/'

##################################################################
# Methods                                                        #
##################################################################
def build_output_directory():
  #Clean output directory
  try:
    shutil.rmtree(output_path)
  except:
    print("No folder had to be removed")
  os.mkdir(output_path)

# Extracts orientation information for each line in csv
def extract_quat_columns(file, jointName):
    df = pd.read_csv(file, header=None)
    first_row = df.iloc[0].values
    df = df.iloc[1:]
    df.columns = first_row
    df = df.filter(regex=jointName)
    df = df[:].astype(float)
    df.insert(loc=0, column='quat', value=jointName)
    df.columns = ['quat', '0', '1', '2', '3']
    return df

# Extracts position information for each line in csv
def extract_position_columns(file, jointName):
    df = pd.read_csv(file, header=None)
    first_row = df.iloc[0].values
    df = df.iloc[1:]
    df.columns = first_row
    df = df.filter(regex=jointName)
    df = df[:].astype('float32')
    df.insert(loc=0, column='3D vector', value=jointName)
    df.columns = ['3D vecotr', '0', '1', '2']
    return df

# Builds composed datatable for all sensors and one movement
# Saves the new csv with the following data:
#   - Rows: original * number of sensors in the list.
#   - Columns: 4 in orientation sensors, 3 in position.
def build_dt(sample: str, subject: str, movement: str):
  subject_and_activity_file =  main_path + '/framework/pre-processing/dataset/' + subject + '-' + movement + '-' + sample + '.csv'
  orientation_df_list = list()
  position_df_list = list()

  # Check file exists
  try:
    f = open(subject_and_activity_file)
    f.close()
  except FileNotFoundError:
    print("      WARNING: File not accessible!")
    return
    
  if cfg["orientationSensors"]["enabled"]: 
    jointNamesListVicon = cfg["orientationSensors"]["list"]
    for sensor in jointNamesListVicon:
        df = extract_quat_columns(subject_and_activity_file, sensor)
        orientation_df_list.append(df.values)
    final_df = pd.DataFrame(interleave(orientation_df_list))
    subject_and_activity_file_output = output_path + subject + '-' + movement + '-Orientationjoints-' + sample + '.csv'
    final_df.to_csv(subject_and_activity_file_output, index=False)

  if cfg["positionSensors"]["enabled"]: 
    jointNamesListVicon = cfg["positionSensors"]["list"]
    for sensor in jointNamesListVicon:
        df = extract_position_columns(subject_and_activity_file, sensor)
        position_df_list.append(df.values)
    final_df = pd.DataFrame(interleave(position_df_list))
    subject_and_activity_file_output = output_path + subject + '-' + movement + '-Positionjoints-' + sample + '.csv'
    final_df.to_csv(subject_and_activity_file_output, index=False)

# Analyzes configured movements and samples
def  create_dt_by_movement(subject: str):
  print("Building interleaved dataframes for subject: " + subject)
  for movement in cfg["movements"]["list"]:
    for sample in cfg["movements"]["samples"]:
      print("   Movement " + movement + " & record sample " + sample)
      build_dt(sample, subject, movement)

#########################
# Main                  #
#########################
if cfg["enabled"]:
  build_output_directory()
  for subject in cfg["subjects"]["list"]:
    create_dt_by_movement(subject)
  print("\nINTERLEAVED DATAFRAMES BUILDING FINISHED")
else:
  print("\nnINTERLEAVED DATAFRAMES BUILDING DISABLED")