import os
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