import os
import sys
import ntpath
import datetime
import subprocess
import pandas as pd

DATADIR = '../datasets'


def view_data_toc():
    '''Print the Dataset Table of Contents file'''
    toc_df = pd.read_csv(f'{DATADIR}/dataset_TOC.csv', index_col=0, comment='#', dtype=str)
    return toc_df


def load_dataset(dataset_name):
    '''
    Load a dataset into a dataframe
    
    dataset_name: the file name of the dataset, with or without the file extension
    '''
    if '.tsv' not in dataset_name:
        dataset_name = dataset_name + '.tsv'
    return pd.read_csv(f'{DATADIR}/{dataset_name}', index_col=0, sep='\t', comment='#')



def convert_periods_to_str(periods):
    '''
    Convert a list of strings or integers to a single string or convert an integer to a string.
    '''
    # convert periods to string
    if isinstance(periods, int):
        periods = str(periods)
    elif isinstance(periods, list):
        if len(periods) > 1:
            periods = [str(p) for p in periods]
            periods = ' '.join(periods)
        else:
            periods = str(periods[0])
            
    return periods


def run_pyjtk(dataset, periods, is_tmp=False):
    '''
    Use pyJTK to analyze a time series dataset.
    Periods is a list of periods to use in pyJTK.
    '''
    
    datetimestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    
    # convert periods to string
    periods = convert_periods_to_str(periods)

    pyjtk_path = '../src/pyjtk/pyjtk.py'
    
    if is_tmp:
        data_path = dataset
        dataset = ntpath.basename(dataset).split('tmp')[0][:-1]
    else:
        data_path = f'../datasets/{dataset}.tsv'
    
    outfile = f'{dataset}_pyjtk_{datetimestr}.tsv'
    outdir = f'../results/{outfile}'
    
    full_cmd = ['python', pyjtk_path, data_path, '-T', periods, '-o', outdir]
    
    print(f'-- Running pyJTK on dataset {dataset}, testing period(s) of {periods}')
    
    submit_cmd = subprocess.Popen(full_cmd, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
    
    print(f'-- Command used: {" ".join(full_cmd)}')
    
    output, error = submit_cmd.communicate()
    str_error = error.decode("utf-8").split('\n')
    str_output = output.decode("utf-8").split('\n')
    if len(str_error) > 1:
        print(f'-- Error:')
        [print(e) for e in str_error]

    print(f'-- Results saved as {outfile} in the results directory')
    
    return outdir


def run_pydl(dataset, period, numb_reg=1000000, numb_per=10000, log_trans=True, verbose=False, is_tmp=False):
    '''
    Use pyDL to analyze a time series dataset.
    Period is single period to use in pyDL.
    '''
    datetimestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    
    # convert periods to string
    if isinstance(period, list):
        print(f'** ERROR: pyDL can only take one period. You set <period> to {period}.\nSelect one, set it for period and run again  **')
        return
    else:
        period = str(period)
    
    pydl_path = '../src/pydl/pydl.py'
    
    if is_tmp:
        data_path = dataset
        dataset = ntpath.basename(dataset).split('tmp')[0][:-1]
    else:
        data_path = f'../datasets/{dataset}.tsv'
        
    outfile = f'{dataset}_pydl_{datetimestr}.tsv'
    outdir = f'../results/{outfile}'
    
    print(f'-- Running pyDL on dataset {dataset}, testing a period of {period}')
    
    full_cmd = ['mpiexec', '-n', '2', 'python', pydl_path, data_path, '-T', period, '-o', outdir, 
                '-r', str(numb_reg), 
                '-p', str(numb_per), 
                '-l', str(log_trans), 
                '-v', str(verbose)]    
    
    submit_cmd = subprocess.Popen(full_cmd, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
    
    print(f'-- Command used: {" ".join(full_cmd)}')
    
    output, error = submit_cmd.communicate()
    str_error = error.decode("utf-8").split('\n')
    str_output = output.decode("utf-8").split('\n')
    if len(str_error) > 1:
        print(f'-- Error:')
        [print(e) for e in str_error]

    print(f'-- Results saved as {outfile} in the results directory')
    
    return outdir


def duplicate_check(dataset):
    '''
    Checks for duplicates and prints out tips for what to do with the duplicates.
    '''
    
    if dataset.index.is_unique:
        print('This dataset has no duplicate gene names.')
        return True
    else:
        print('This dataset has duplicate gene names. This needs to be corrected.')
        print('You can either drop duplicates or relabel duplicates.')
        print('-- Use remove_duplicates() to only keep the duplicate with either the highest gene expression at any time point or highest average gene expression.')
        print('-- Use relabel_duplicates() to append "dupN" to each duplicate gene name, where N is an integer.')
        return False

    
def remove_duplicates(dataset, method):
    '''
    Removes duplicate gene names by two methods.
    Method 1 (max): keep only the duplicate with the highest gene expression at any time points.
    Method 2 (average): keep the duplicate with the hightest average gene expression.
    '''
    
    df = dataset.copy()
    df = df.reset_index()
    idx_drops = list()
    
    if method == 'average':
        df[method] = df.mean(numeric_only=True, axis=1)
    elif method == 'max':
        df[method] = df.max(numeric_only=True, axis=1)
    else:
        print(f'Error: Method must be either "max" or "average". You entered "{method}".')
        return
        
    for genename, expression in df.groupby('time_points'):
        if expression.shape[0] > 1:
            keep_idx = expression[method].idxmax()
            drop_idx_list = expression[expression.index != keep_idx].index.tolist()
            idx_drops += drop_idx_list

    df = df[~df.index.isin(idx_drops)]   
    df = df.set_index('time_points')
    df = df.drop(labels=[method], axis=1)
    
    return df


def relabel_duplicates(dataset):
    '''
    Relabel duplicates. 
    Append "dupN" to each duplicate name where N is an integer.
    '''
    
    df = dataset.copy()
    new_index = list()
    
    for genename, expression in df.groupby('time_points'):
        if expression.shape[0] > 1:
            index_list = expression.index.tolist()
            [new_index.append(f'{idx} dup{i+1}') for idx, i in zip(index_list, range(len(index_list)))]
        else:
            new_index.append(genename)

    df.index = new_index  
    df.index.name = 'time_points'
    
    return df


def run_periodicity(dataset, pyjtk_periods, pydl_periods, drop_duplicates=False, drop_method='max'):
    '''
    Run pyJTK and pyDL on a single dataset.
    pyjtk_periods is a list of periods to use in pyJTK
    pydl_periods is a single period to use in pyDL
    drop_duplicates, when True, will drop duplicates in the dataset based on drop_method. When False, duplicates are relabeled to prevent pyDL from failing.
    drop_method specifies the method to use for determining which duplicates to drop.
    '''
    
    print(f'Running periodicity algorithms on {dataset}')
    
    print('Loading data.')
    df = load_dataset(dataset)
    
    if drop_duplicates:
        print(f'Dropping duplicates by the {drop_method} method in remove_duplicates().')
        df = remove_duplicates(df, drop_method)
    else:
        print('Relabeling duplicates.')
        df = relabel_duplicates(df)
    
    tmp_file = f'../tmp/{dataset}_tmp.tsv'
    
    df.to_csv(tmp_file, sep='\t')
    
    print('Running pyJTK')
    pyjtk_results_path = run_pyjtk(tmp_file, pyjtk_periods, is_tmp=True)
    
    print('Running pyDL')
    pydl_results_path = run_pydl(tmp_file, pydl_periods, is_tmp=True)
    
    pjyk_results = pd.read_csv(pyjtk_results_path, sep='\t', index_col=0, comment='#')
    pydl_results = pd.read_csv(pydl_results_path, sep='\t', index_col=0, comment='#')
    
    os.remove(tmp_file)
    
    return pjyk_results, pydl_results