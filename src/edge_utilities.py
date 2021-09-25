import os
import sys
import time
import ntpath
import datetime
import subprocess
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
import matplotlib
import platform

from configobj import ConfigObj

DATADIR = '../datasets'


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def uniques(lst1, lst2, intersection):

    uniq_lst1 = [value for value in lst1 if value not in intersection]
    uniq_lst2 = [value for value in lst2 if value not in intersection]

    return uniq_lst1, uniq_lst2


def default_arguments():

    seed = round(time.time())

    def_arg_dict = dict()

    def_arg_dict['output_dir'] = '../results'

    # default settings for LEMpy
    def_arg_dict['loss'] = 'euc_loss'
    def_arg_dict['param_bounds'] = 'tf_param_bounds'
    def_arg_dict['prior'] = 'uniform_prior'
    def_arg_dict['normalize'] = True
    def_arg_dict['inv_temp'] = 1
    def_arg_dict['seed'] = seed

    def_arg_dict['minimizer_params'] = dict()
    def_arg_dict['minimizer_params']['niter'] = 200
    def_arg_dict['minimizer_params']['T'] = 1
    def_arg_dict['minimizer_params']['stepsize'] = .5
    def_arg_dict['minimizer_params']['interval'] = 10
    def_arg_dict['minimizer_params']['disp'] = False
    def_arg_dict['minimizer_params']['seed'] = seed

    return def_arg_dict


def gen_lempy_config(co, dataset_name, target_list, repressor_list, activator_list, datetimestr):
    def_arg_dict = default_arguments()
    lempy_config = ConfigObj(def_arg_dict)

    # Walk the config file and reduce the subsections by one
    def reduce_subsections(section, key):
        if section.depth > 1:
            section.depth = section.depth - 1

    lempy_config.walk(reduce_subsections)

    # Pass in pipeline config arguments needed by LEMpy
    lempy_config['data_files'] = co['data_files']
    lempy_config['verbose'] = co['verbose']
    lempy_config['num_proc'] = co['num_proc']
    lempy_config['annotation_file'] = co['annotation_file']

    # Specify the default output location needed for the next step
    lempy_config['output_dir'] = os.path.join(lempy_config['output_dir'], f'lempy_{dataset_name.split(".")[0]}_{datetimestr}')

    # Populate LEMpy config file with targets and regulators sections based on DLxJTK output and gene annotations
    lempy_config['targets'] = dict()
    lempy_config['regulators'] = dict()

    # add targets
    for target in target_list:
        # Gene is an allowed target
        lempy_config['targets'][target] = ''

    # regulators and their mode of regulation
    for gene in list(set(repressor_list + activator_list)):
        lempy_config['regulators'][gene] = []

    for rep_reg in repressor_list:
        # Gene is allowed this model of regulation
        lempy_config['regulators'][rep_reg].append('tf_rep')
    for act_reg in activator_list:
        # Gene is allowed this model of regulation
        lempy_config['regulators'][act_reg].append('tf_act')

    lempy_config.filename = os.path.join(lempy_config['output_dir'], f'lempy_{datetimestr}_config.txt')

    return lempy_config


def run_lem(dataset_name, target_list, repressor_list, activator_list, annotation_file, num_proc=2, verbose=False):

    datetimestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    if '.tsv' not in dataset_name:
        dataset_name = dataset_name + '.tsv'

    user_dict = {'data_files':[os.path.join(DATADIR, dataset_name)],
                'annotation_file':annotation_file,
                'num_proc':num_proc,
                'verbose':verbose}

    user_config = ConfigObj(user_dict)
    full_lem_config = gen_lempy_config(user_config, dataset_name, target_list, repressor_list, activator_list, datetimestr)
    os.makedirs(os.path.split(full_lem_config.filename)[0])
    full_lem_config.write()

    lempy_path = '../src/lempy/lempy.py'
    full_cmd = ['mpiexec', '-n', str(num_proc), 'python', lempy_path, full_lem_config.filename]
    
    print(f'-- Running LEMpy on dataset {dataset_name}')

    submit_cmd = subprocess.Popen(full_cmd,
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
    
    print(f'-- Command used: {" ".join(full_cmd)}')

    output, error = submit_cmd.communicate()
    str_error = error.decode("utf-8").split('\n')
    str_output = output.decode("utf-8").split('\n')
    # print(str_output)
    if len(str_error) > 1:
        print(f'-- Error:')
        [print(e) for e in str_error]
    else:
        print(f'-- Results saved in {os.path.split(full_lem_config.filename)[0]}')

        all_scores_file = os.path.join('summaries', 'ts0', 'allscores_ts0.tsv')
        all_scores_df = pd.read_csv(os.path.join(os.path.split(full_lem_config.filename)[0],all_scores_file), sep='\t', index_col=0, comment='#')

        targets_dir = os.path.join(os.path.split(full_lem_config.filename)[0], 'targets', 'ts0')
        target_dfs = list()
        localmin_dfs = list()
        for file in os.listdir(targets_dir):
            if 'target' in file:
                tar_df = pd.read_csv(os.path.join(targets_dir, file), sep='\t', index_col=0, comment='#')
                genename = file.split('_')[1]
                tar_df['target'] = genename
                tar_col = tar_df.pop('target')
                tar_df.insert(0, 'target', tar_col)
                target_dfs.append(tar_df)
            if 'localmin' in file:
                localmin_dfs.append(pd.read_csv(os.path.join(targets_dir, file), sep='\t', index_col=0, comment='#'))

        all_target_df = pd.concat(target_dfs)
        all_localmin_df = pd.concat(localmin_dfs)

        return all_scores_df, all_target_df, all_localmin_df


# TODO: add network making and vix functions