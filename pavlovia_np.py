#!/usr/bin/env python
import pandas as pd
import os
import glob
import re

# define generic task path/file names
tasks = [
    {'name': 'pgngs',
    'path': 'pgngs_color_600ms_v11_eng',
    'file_name': '_PGNGS_colors_600ms_v11r4_english_'},
    {'name': 'fept',
    'path': 'fept_mr_v8r12_cow_video',
    'file_name': '_FEPT_MR_v8r12_pavlovia_'},
    {'name': 'fam',
    'path': 'familiarity_condition_feptv8r11',
    'file_name': '_fam_cond_'},
    {'name': 'syn',
    'path': 'synonyms-task',
    'file_name': '_Synonyms_'}
    ]

def print_files(participant_files):
    # prints the names of the files in participant_files
    print("\nNP files found:\n")
    for file in participant_files:
        print(os.path.split(file)[1])

def find_files(participant):
    # finds all files related to the participant and returns a list of file paths
    participant_files = []
    for task in tasks:
        file_name = str(participant) + task['file_name'] + "*"
        participant_files.extend(glob.glob(os.path.join('..', task['path'], 'data', file_name)))
    print_files(participant_files)
    return participant_files

def pgngs_validation(participant_files):
    # validates PGNGS data
    csv_files = []
    # get a list of all PGNGS csv files
    for file in participant_files:
        if re.search(tasks[0]['file_name'] + ".*.csv", file):
            csv_files.append(file)
    # grab the first csv file (if more than one)
    try:        
        pgngs_data_path = csv_files[0]  #TODO: method for choosing the most recent/most complete file
        print(f"\nChecking PGNGS file: {os.path.split(pgngs_data_path)[1]} ...")
        pgngs_df = pd.read_csv(pgngs_data_path)
        # check that the file has the expected number of rows
        if len(pgngs_df) == 1375:
            print("PGNGS: Task was finished.")
        else:
            print("PGNGS: Task not finished. Check data file.")
        # check that all blocks have responses
        blocks = [False, False, False, False, False, False]
        for i, block in enumerate(blocks):
            if not all(pd.isna(pgngs_df[f'block{i+1}_resp.keys'])):
                blocks[i] = True
        if all(blocks):
            print("PGNGS: All blocks have responses.")
        else:
            print("PGNGS: One or more block is empty. Check data file.")
    except:
        print("\nPGNGS file not found or is empty.")

def fept_validation(participant_files):
    # validates FEPT data
    csv_files = []
    # get a list of all FEPT csv files
    for file in participant_files:
        if re.search(tasks[1]['file_name'] + ".*.csv", file):
            csv_files.append(file)
    # grab the first csv file (if more than one)
    try:    
        fept_data_path = csv_files[0]
        print(f"\nChecking FEPT file: {os.path.split(fept_data_path)[1]} ...")
        fept_df = pd.read_csv(fept_data_path)
        # check that the file has the expected number of rows
        if len(fept_df) == 127:
            print("FEPT: Task was finished.")
        else:
            print("FEPT: Task not finished. Check data file.")
        # check that there are a sufficient number of correct responses
        if fept_df['key_resp_face.corr'].sum() >= 29:
            print(f"FEPT: Sufficient number of FACES correct: {fept_df['key_resp_face.corr'].sum():.0f}.")
        else:
            print("FEPT: Insufficient number of FACES correct. Check data file.")
        if fept_df['key_resp_animal2.corr'].sum() >= 40:
            print(f"FEPT: Sufficient number of ANIMALS correct: {fept_df['key_resp_animal2.corr'].sum():.0f}.")
        else:
            print("FEPT: Insufficient number of ANIMALS correct. Check data file.")
    except:
        print("\nFEPT file not found or is empty.")

def familiarity_validation(participant_files):
    # validates familiarity data
    csv_files = []
    # get a list of all familiarity csv files
    for file in participant_files:
        if re.search(tasks[2]['file_name'] + ".*.csv", file):
            csv_files.append(file)
    # grab first csv file
    try:    
        fam_data_path = csv_files[0]  #TODO: method for choosing the most recent/most complete file
        print(f"\nChecking FAMILIARITY file: {os.path.split(fam_data_path)[1]} ...")
        fam_df = pd.read_csv(fam_data_path)
        # check that the file has the expected number of rows
        if len(fam_df) == 24:
            print("FAMILIARITY: Task was finished.")
        else:
            print("FAMILIARITY: Task not finished. Check data file.")
        # check that there was more than just one key pressed
        if fam_df['key_resp.keys'].nunique() > 1:
            print("FAMILIARITY: Responses are varied.")
        else:
            print("FAMILIARITY: Same letter pressed for every response. Check data file.")
        #TODO: check if fam was done on the same day as fept
    except:
        print("\nFAMILIARITY file not found or is empty")

def synonyms_validation(participant_files):
    # validates synonyms data
    csv_files = []
    # get a list of all synonyms csv files
    for file in participant_files:
        if re.search(tasks[3]['file_name'] + ".*.csv", file):
            csv_files.append(file)
    # grab first csv file
    try:    
        syn_data_path = csv_files[0]  #TODO: method for choosing the most recent/most complete file
        print(f"\nChecking SYNONYMS file: {os.path.split(syn_data_path)[1]} ...")
        syn_df = pd.read_csv(syn_data_path)
        # check that the file has the expected number of rows
        if len(syn_df) == 43:
            print("SYNONYMS: Task was finished.")
        else:
            print("SYNONYMS: Task not finished. Check data file.")

        # grab responses and correct columns
        responses = syn_df['key_resp_2.keys'].dropna().reset_index(drop=True)
        correct = syn_df['correct'].dropna().reset_index(drop=True)

        # convert 'comma' to ',' and 'period' to '.', then increase score if correct
        score = 0
        for i, response in enumerate(responses):
            if response == 'comma':
                responses[i] = ','
            elif response == 'period':
                responses[i] = '.'
            if responses[i] == correct[i]:
                score += 1

        if score > 15 and score <= 40:
            print(f"SYNONYMS: Sufficient score: {score}.")
        else:
            print(f"SYNONYMS: Insufficient score: {score}. Check data file.")
    except:
        print("\nSYNONYMS file not found or is empty.")
    print('\n')

def find_validate_files(record):
    participant_files = find_files(record)
    pgngs_validation(participant_files)
    fept_validation(participant_files)
    familiarity_validation(participant_files)
    synonyms_validation(participant_files)
