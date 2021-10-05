import os
import time
import scipy
import ntpath
import datetime
import platform
import subprocess
import matplotlib
import numpy as np
import pandas as pd
import ipycytoscape
import seaborn as sns
from configobj import ConfigObj
import matplotlib.pyplot as plt
from pandarallel import pandarallel
from astropy.timeseries import LombScargle as ls


DATADIR = '../datasets'


############ Utility Functions ############

def view_data_toc():
    '''Print the Dataset Table of Contents file'''
    toc_df = pd.read_csv(os.path.join(DATADIR, 'dataset_TOC.csv'), index_col=0, comment='#', dtype=str)
    return toc_df


def load_dataset(dataset_name):
    '''
    Load a dataset into a dataframe
    
    dataset_name: the file name of the dataset, with or without the file extension
    '''
    if '.tsv' not in dataset_name:
        dataset_name = dataset_name + '.tsv'
    return pd.read_csv(os.path.join(DATADIR, dataset_name), index_col=0, sep='\t', comment='#')


def load_results(periodicity_results_name):
    '''
    Load periodicity results into a dataframe
    
    periodicity_results_name: the file name of the periodicity results file. Will be stored as the output of running the periodicity functions.
    '''
    if '.tsv' not in periodicity_results_name:
        periodicity_results_name = periodicity_results_name + '.tsv'
    return pd.read_csv(os.path.join(DATADIR, periodicity_results_name), index_col=0, sep='\t', comment='#')


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


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def uniques(lst1, lst2, intersection):

    uniq_lst1 = [value for value in lst1 if value not in intersection]
    uniq_lst2 = [value for value in lst2 if value not in intersection]

    return uniq_lst1, uniq_lst2


def get_genelist_from_top_n_genes(periodicity_result, filtering_column, top_genes):
    '''
    Return gene list consisting of top n genes based off of the periodicity inputs and a specified number of genes.
    periodicity_result is the output from run_periodicity, run_pyjtk, or run_pydl. Can consist of a path to a file or a dataframe.
    filtering_column is the name of a column in the periodicity result above. For example, for JTK specifying 'p-value' will allow for the top n genes ranked based off of the JTK p-value.
    top_genes is an integer that specifies the number of top genes to include
    '''
    
    if type(periodicity_result) == str:
        print('Loading periodicity results')
        periodicity_df = load_results(periodicity_result)
    elif type(periodicity_result)==pd.core.frame.DataFrame:
        periodicity_df = periodicity_result
    if filtering_column in periodicity_df.columns:
        periodicity_df=periodicity_df.sort_values(by=filtering_column)
        gene_list = list(periodicity_df.iloc[0:top_genes].index)
        return gene_list
    else:
        print('filtering column must be a numeric column in the periodicity result dataframe.')
        return None
    

def get_genelist_from_threshhold(periodicity_result, filtering_column, threshhold, threshhold_below=True):
    '''
    Return gene list consisting of top genes based off of the periodicity inputs and a specified numeric threshhold.
    periodicity_result is the output from run_periodicity, run_pyjtk, or run_pydl. Can consist of a path to a file or a dataframe.
    filtering_column is the name of a column in the periodicity result above. For example, for JTK specifying 'p-value' will allow for the top genes based off of the supplied p-value threshhold.
    threshhold is a numeric value corresponding to the threshhold for the filtering column
    threshhold below, when True will include genes with a periodicity score below the threshhold. When False will take genes with a periodicity score above the threshhold.
    '''
        
    if type(periodicity_result) == str:
        print('Loading periodicity results')
        periodicity_df = load_results(periodicity_result)
    elif type(periodicity_result)==pd.core.frame.DataFrame:
        periodicity_df = periodicity_result
    
    if threshhold_below:
        gene_list = list(periodicity_df.loc[periodicity_df[filtering_column]<threshhold].index)
    else:
        gene_list= list(periodicity_df.loc[periodicity_df[filtering_column]>threshhold].index)
    return gene_list


def closest_column(list_columns, n):
    '''
    Returns the column from a list of columns that is closest to the number n. List of columns must contain numbers.
    '''
      
    return list_columns[min(range(len(list_columns)), key = lambda i: abs(list_columns[i]-n))]


def get_closest_column_from_period(dataset_df, period):
    '''
    Returns the column from the supplied dataset that is closest to the supplied period.
    '''
    columns_in_df = list(dataset_df.columns)
    timepoints_numeric = [int(i) for i in columns_in_df]
    closest_column_int = closest_column(timepoints_numeric, period)
    return closest_column_int


def normalize_data(dataset):
    ''''
    Z-score normalize a time series dataframe.
    '''
    z_pyjtk = scipy.stats.zscore(dataset, axis=1)
    return pd.DataFrame(z_pyjtk, index=dataset.index, columns=dataset.columns)






############ Vizualization Functions ############

# For normalizing data and getting Haase Lab coloring in heatmaps 
norm = matplotlib.colors.Normalize(-1.5,1.5)
colors = [[norm(-1.5), "cyan"],
      [norm(0), "black"],
     [norm(1.5), "yellow"]]
haase = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)


def plot_heatmap(dataset, periodicity_result, period, filtering_column, top_genes=1000, threshhold=None, threshhold_below=True):
    '''
    Plot genes from a single dataset in a heatmap ordered by first period maximum. Genes included will depend on the top_genes or threshhold values. Top_genes defaults to 1000, so by default the top 1000 genes based off the
    supplied periodicity result will be plotted.
    
    dataset
    periodicity_result is the output from run_periodicity, run_pyjtk, or run_pydl. Can consist of a path to a file or a dataframe.
    period is the period used to create the periodicity result.
    filtering_column is the name of a column in the periodicity result above. For example, for JTK specifying 'p-value' will allow for the top n genes ranked based off of the JTK p-value.
    top_genes is an integer that specifies the number of top genes to include (default 1000, set to None if you want to filter the genes based off of a threshhold instead)
    threshhold is a numeric value corresponding to the threshhold for the filtering column (default None, set to a value (i.e. 0.5) and set top_genes to None to filter based off of a threshhold)
    threshhold below, when True will include genes with a periodicity score below the threshhold. When False will take genes with a periodicity score above the threshhold.
    handle_duplicates, when True will either drop or relabel duplicates, when True will leave duplicates as is.
    drop_duplicates, when True, will drop duplicates in the dataset based on drop_method. When False, duplicates are relabeled to prevent pyDL from failing.
    drop_method specifies the method to use for determining which duplicates to drop.
    '''
    
    if top_genes is not None and threshhold is None:
        gene_list = get_genelist_from_top_n_genes(periodicity_result, filtering_column, top_genes)
    elif top_genes is not None and threshhold is not None:
        gene_list = get_genelist_from_top_n_genes(periodicity_result, filtering_column, top_genes)
        print('Note: both threshhold and top genes were supplied with a value. Using top genes. To use threshhold, please set top genes to None.')
    else:
        if threshhold is not None:
            gene_list = get_genelist_from_threshhold(periodicity_result, filtering_column, threshhold, threshhold_below)
        else:
            print('Either top_genes or threshhold must be not None.')
    dataset = dataset.reindex(gene_list)
    data = dataset.loc[gene_list]
    if len(gene_list)>75:
        yticks = False
    else:
        yticks = True
    
    z_pyjtk_df = normalize_data(data)
    
    first_period = get_closest_column_from_period(data, period)
    first_period_index = data.columns.get_loc(str(first_period))
    
    z_pyjtk_1stperiod = z_pyjtk_df.iloc[:, 0:first_period_index]
    max_time = z_pyjtk_1stperiod.idxmax(axis=1)
    z_pyjtk_df["max"] = max_time
    z_pyjtk_df["max"] = pd.to_numeric(z_pyjtk_df["max"])
    z_pyjtk_df = z_pyjtk_df.sort_values(by="max", axis=0)
    z_pyjtk_df = z_pyjtk_df.drop(columns=['max'])

    fig = plt.figure(figsize = (8,8))
    
    if top_genes is not None:
        subtitle = "Filtered by " + filtering_column +": top " + str(top_genes) +" genes\n"
    elif threshhold is not None:
        subtitle = "Filtered by " + filtering_column +" with threshold = "+ str(threshhold) +"\n"
    title = 'Time Series Data'
    plt.title(subtitle, fontsize = 13, y = .96)
    plt.suptitle(title, fontsize=15, ha='center', x = 0.435, y = .96)    
    fig.subplots_adjust(top = 0.90)

    sns.heatmap(z_pyjtk_df, cmap=haase, vmin=-1.5, vmax=1.5, yticklabels = yticks, cbar = True)
    plt.show()


def plot_heatmap_in_supplied_order(dataset, order):
    '''
    Plot genes from a single dataset in a heatmap ordered by the supplied order.
    
    order is a list containing the genes to plot in the heatmap in the desired order.
    handle_duplicates, when True will either drop or relabel duplicates, when True will leave duplicates as is.
    drop_duplicates, when True, will drop duplicates in the dataset based on drop_method. When False, duplicates are relabeled to prevent pyDL from failing.
    drop_method specifies the method to use for determining which duplicates to drop.
    '''
            
    if len(order)>100:
        yticks = False
    else:
        yticks = True

    dataset = dataset.reindex(order)
    data = dataset.loc[order]
    z_pyjtk_df = normalize_data(data)

    fig = plt.figure(figsize = (8,8))
    subtitle = "Ordered by supplied genelist"
    title = 'Time Series Data'
    plt.title(subtitle, fontsize = 13, y = .995)
    plt.suptitle(title, fontsize=15, ha='center', x = 0.435, y = .96)    
    fig.subplots_adjust(top = 0.90)

    sns.heatmap(z_pyjtk_df, cmap=haase, vmin=-1.5, vmax=1.5, yticklabels = yticks, cbar= True)
    plt.show()


def plot_linegraphs_from_gene_list(dataset, gene_list, norm_data=False):
    '''
    Plots supplied genes in the genelist from a single dataset in lineplots. Can only plot between 1 and 10 genes.

    '''
    
    if norm_data:
        dataset = normalize_data(dataset)

    if len(gene_list) <=5 and len(gene_list)>0:
        num_rows = 1
        num_columns = len(gene_list)
        length_size = 3
        width_size = len(gene_list)*4
        
    elif len(gene_list) > 5 and len(gene_list)<=10:
        num_rows = 2
        num_columns = 5
        length_size = 6
        width_size = 20
    else:
        print("Gene-list must be between 1 and 10 genes in length")
        
    
    fig = plt.figure(figsize = (width_size,length_size))
    
    if len(gene_list) <=5 and len(gene_list)>0:
        top_size = .8
    elif len(gene_list) > 5 and len(gene_list)<=10:
        top_size = 0.9
    
    fig.subplots_adjust(hspace=0.3, wspace=0.3, top = top_size)
    plt.suptitle('Time Series Data', fontsize=15, y = 0.99)    

    for i, genename in enumerate(gene_list):
        plt.subplot(num_rows, num_columns, i+1)
        sns.lineplot(x = dataset.columns, y = dataset.loc[genename,:]).set_title(genename)
    plt.show()
    

def plot_line_graphs_from_top_periodicity(dataset, periodicity_result, filtering_column, top_gene_number, norm_data=False):
    '''
    Plots top n genes from a dataset in lineplots. Top genes are determined based off of supplied top gene number and the supplied periodicity results. To
    
    periodicity_result is the output from run_periodicity, run_pyjtk, or run_pydl. Can consist of a path to a file or a dataframe.
    period is the period used to create the periodicity result.
    filtering_column is the name of a column in the periodicity result above. For example, for JTK specifying 'p-value' will allow for the top n genes ranked based off of the JTK p-value.
    top_gene_number is an integer that specifies the number of top genes to include. Must be between 1 and 10.
    '''
    
    if top_gene_number not in list(range(1,11)):
        print("top_gene_number must be between 1 and 10")
    else:
        
        if type(periodicity_result) == str:
            print('Loading periodicity results')
            periodicity_df = load_results(periodicity_result)
        elif type(periodicity_result)==pd.core.frame.DataFrame:
            periodicity_df = periodicity_result
        
        gene_list = get_genelist_from_top_n_genes(periodicity_df, filtering_column, top_gene_number)
        plot_linegraphs_from_gene_list(dataset, gene_list, norm_data=norm_data)


def df_edges_to_ipycytoscape(lem_edge_list):
    '''
    converts a list of edges in LEM specification into a cytoscape element which can then be used in ipycytoscape for vizualizing a network. Also returns a cytoscape style dictionary.

    lem_edge_list: a list of edges in LEM specification
    '''

    nodes = list()
    edges = list()
    cyto_elements = dict()
    for lem_edge in list(lem_edge_list):
            target = lem_edge.split("=")[0]
            source = lem_edge.split("=")[1].split("(")[1].split(")")[0]
            type_reg = lem_edge.split("=")[1].split("(")[0]

            nodes.append({'data': {'id': source, 'label': source}})
            nodes.append({'data': {'id': target, 'label': target}})
            if type_reg == "tf_rep":
                edges.append({'data': {'id': f'{source}-{target}', 'source': source, 'target': target}, 'classes': 'rep'})

            else:
                edges.append({'data': {'id': f'{source}-{target}', 'source': source, 'target': target}, 'classes': 'act'})

    nodes = [i for n, i in enumerate(nodes) if i not in nodes[n + 1:]]
    cyto_elements['nodes'] = nodes
    cyto_elements['edges'] = edges
    cyto_styles = [{'selector': 'node', 'style': {'content': 'data(label)'}},
        {'selector': 'edge', 'style': {'curve-style': 'bezier'}},
        {'selector': '.rep', 'style': {'target-arrow-color': 'red', 'line-color': 'red', 'target-arrow-shape': 'tee'}},
        {'selector': '.act', 'style': {'target-arrow-color': 'green', 'target-arrow-shape': 'triangle', 'line-color': 'green'}}]
    return cyto_elements, cyto_styles


def make_network_from_edge_list(lem_edge_list):
    '''
    Make an interactive graph from a list of edges in LEM edge specification.

    lem_edge_list: a list of LEM edges. Each item in the list is in the format 'target=tf_rep(source)'. This is how LEM specifies an edge.
    Example: If the gene YOX1 represses SWI4 transcription then 'SWI4=tf_rep(YOX1)', or if SWI4 activates YOX1 then 'YOX1=tf_act(SWI4)'.
    
    Returns an interactive network made from the list of LEM edges.
    '''

    elements, styles = df_edges_to_ipycytoscape(lem_edge_list)
    cytonet = ipycytoscape.CytoscapeWidget()
    # cytonet = ipycytoscape.CytoscapeWidget(user_zooming_enabled=False, panning_enabled=False)
    cytonet.graph.add_graph_from_json(elements, multiple_edges=True)
    cytonet.set_style(styles)
    return cytonet


def make_top_edge_network(lem_all_scores_df, top_n_edges, score='pld'):
    '''
    Make an interactive graph from the top N edges from the LEM all_scores dataframe.

    lem_all_scores_df: the dataframe containing the all_scores results returned from running LEMpy
    top_n_edges: the integer to threshold the all_scores dataframe on
    score: the column in the all_scores dataframe to rank on before thresholding. Options are 'pld', 'loss', and 'norm_loss'. Default is 'pld'.

    Returns an interactive network made from the LEM edges.
    '''

    if score == 'pld':
        lem_all_scores_df = lem_all_scores_df.sort_values(by=score, ascending=False)
    else:
        lem_all_scores_df = lem_all_scores_df.sort_values(by=score)
    lem_edge_list = lem_all_scores_df.index.tolist()[:int(top_n_edges)]
    return make_network_from_edge_list(lem_edge_list)




############ Periodicity Functions ############

def run_pyjtk(dataset, periods, filename, is_tmp=False):
    '''
    Use pyJTK to analyze a time series dataset.
    Periods is a list of periods to use in pyJTK.
    '''
    
    datetimestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    
    # convert periods to string
    periods = convert_periods_to_str(periods)

    pyjtk_path = '../src/pyjtk/pyjtk.py'
    
    if is_tmp:
        data_path = filename
        filename = ntpath.basename(data_path).split('__')[0]
    else:
        datetimestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        data_path = f'../tmp/{filename}__{datetimestr}.tsv'
        dataset.to_csv(data_path, sep='\t')
    
    outfile = f'{filename}_pyjtk_{datetimestr}.tsv'
    outdir = f'../results/{outfile}'
    
    full_cmd = ['python', pyjtk_path, data_path, '-T', periods, '-o', outdir]
    
    print(f'-- Running pyJTK on dataset, testing period(s) of {periods}')
    
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
    
    if not is_tmp:
        os.remove(data_path)

    return outdir


# def run_pydl(dataset, period, filename, numb_reg=1000000, numb_per=10000, log_trans=True, verbose=False, is_tmp=False, windows_issues = False):
def run_pydl(dataset, period, filename, numb_reg=1, numb_per=1, log_trans=True, verbose=False, is_tmp=False, windows_issues = False):
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
        data_path = filename
        filename = ntpath.basename(data_path).split('__')[0]
    else:
        datetimestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        data_path = f'../tmp/{filename}__{datetimestr}.tsv'
        dataset.to_csv(data_path, sep='\t')
        
    outfile = f'{filename}_pydl_{datetimestr}.tsv'
    outdir = f'../results/{outfile}'
    
    system = platform.system()
    if system == 'Windows' and windows_issues:
        print('** IMPORTANT: System was detected as Windows. ** There is currently an issue running pyDL on Windows through the Jupyter notebook. Two commands will be printed below. Go into the terminal and change into the biological_clocks_class folder as described in the README.Then copy and paste the following commands. ')
        print(f' -- Printing command for pyDL on dataset, testing period of {period}:')
        pydl_path_windows = pydl_path.replace("../", "")
        data_path_windows = data_path.replace("../", "")
        outdir_windows = outdir.replace("../", "")
        command0 ='Command 1: conda activate BioClocksClass'
        command = f'Command 2: mpiexec -n 2 python {pydl_path_windows} {data_path_windows} -T {period} -o {outdir_windows} -r {numb_reg} -p {numb_per} -l {log_trans} -v {verbose}'
        print (command0)
        print(command)
    else:
        print(f'-- Running pyDL on dataset, testing a period of {period}')

        full_cmd = ['mpiexec', '-n', '2', 'python', pydl_path, data_path, '-T', period, '-o', outdir, 
                    '-r', str(numb_reg), 
                    '-p', str(numb_per), 
                    '-l', str(log_trans), 
                    '-v', str(verbose)]    
        print(f'-- Command used: {" ".join(full_cmd)}')

        submit_cmd = subprocess.Popen(full_cmd, 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE)



        output, error = submit_cmd.communicate()
        str_error = error.decode("utf-8").split('\n')
        str_output = output.decode("utf-8").split('\n')
        # print(str_output)
        if len(str_error) > 1:
            print(f'-- Error:')
            [print(e) for e in str_error]

        print(f'-- Results saved as {outfile} in the results directory')
    
    if not is_tmp:
        os.remove(data_path)

    return outdir


def lomb_scargle(data_array, timepoint_array, period_array):

    frequencies = [(1/p) for p in period_array]
    ls_results = ls(timepoint_array, data_array, normalization='standard', center_data=True)
    power = ls_results.power(frequencies)
    false_alarm_prob = ls_results.false_alarm_probability(power.max(), method='bootstrap')
    best_period = period_array[np.argmax(power, axis=0)]
    return false_alarm_prob, best_period


def run_lomb_scargle(dataset, periods, filename, numb_jobs=2, return_path=False):
    
    pandarallel.initialize(nb_workers=numb_jobs)

    timepoints = np.asarray([int(t) for t in dataset.columns])

    print(f'-- Running Lomb-Scargle on dataset, testing period(s) of {periods}')
    start_time = end_time = datetime.datetime.now()
    lomb_scargle_results = dataset.parallel_apply(lomb_scargle, args=(timepoints, np.asarray(periods)), axis=1, result_type='expand')
    end_time = datetime.datetime.now()
    lomb_scargle_results.columns = ['False_alarm_probability', 'Period']

    datetimestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    datetimestr_out = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    outfile = f'{filename}_LS_{datetimestr}.tsv'
    outdir = f'../results/{outfile}'

    with open(outdir, 'w') as out_file:
        out_file.write('# Lomb-Scargle periodicity scores computed on %s\n' % datetimestr_out)
        out_file.write('# Calculation time:  %f seconds\n' % (end_time - start_time).total_seconds())
        out_file.write('# Period(s) of oscillation tested:  %s\n' % periods)
        lomb_scargle_results.to_csv(out_file, sep='\t')

    print(f'-- Results saved as {outfile} in the results directory')

    if return_path:
        return outdir
    else:
        return lomb_scargle_results


def run_periodicity(dataset, pyjtk_ls_periods, pydl_periods, filename, windows_issues = False):
    '''
    Run pyJTK and pyDL on a single dataset.
    pyjtk_ls_periods is a list of periods to use in pyJTK and in Lomb-Scargle
    pydl_periods is a single period to use in pyDL
    drop_duplicates, when True, will drop duplicates in the dataset based on drop_method. When False, duplicates are relabeled to prevent pyDL from failing.
    drop_method specifies the method to use for determining which duplicates to drop.
    '''
    
    print(f'Running periodicity algorithms')
    
    datetimestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data_path = f'../tmp/{filename}__{datetimestr}.tsv'
    dataset.to_csv(data_path, sep='\t')
    
    print('Running pyJTK')
    pyjtk_results_path = run_pyjtk(data_path, pyjtk_ls_periods, data_path, is_tmp=True)
    
    print('Running pyDL')
    pydl_results_path = run_pydl(data_path, pydl_periods, data_path, is_tmp=True, windows_issues=windows_issues)

    print('Running Lomb-Scargle')
    ls_results = run_lomb_scargle(dataset, pyjtk_ls_periods, filename)
    
    system = platform.system()
    if system == 'Windows' and windows_issues:
        pjyk_results = pd.read_csv(pyjtk_results_path, sep='\t', index_col=0, comment='#')
        pydl_results = pydl_results_path
        print('After pyDL has completed in the terminal, please run the following line in the next cell in the Jupyter notebook. You can also delete the temp file that was created in the tmp folder.')
        command = 'pydl_results = load_results(pydl_results)'
        print(f"Code for jupyter cell: {command}")
    else:
        pjyk_results = pd.read_csv(pyjtk_results_path, sep='\t', index_col=0, comment='#')
        pydl_results = pd.read_csv(pydl_results_path, sep='\t', index_col=0, comment='#')
        os.remove(data_path)
    
    return pjyk_results, pydl_results, ls_results


def dlxjtk_func(row):
    # computes DLxJTK score for one gene in df
    amp = row["dl_reg_pval_norm"]
    per = row["jtk_per_pval_norm"]
    return per * amp * (1 + ((per / 0.001) ** 2)) * (1 + ((amp / 0.001) ** 2))


def run_dlxjtk(pyjtk_results, pydl_results):
    '''
    Computes the DLxJTK score using results from pyJTK and pyDL. The pyJTK and pyDL results must be from the same time series.

    pyjtk_results: results from running pyJTK on a time series file as pyDL was run on
    pydl_results: results from running pyDL on the same time series file as pyJTK was run on

    Returns a pandas dataframe
    '''

    if type(pyjtk_results) == str:
        print('Loading periodicity results')
        jtk_df = load_results(pyjtk_results)
    elif type(pyjtk_results)==pd.core.frame.DataFrame:
        jtk_df = pyjtk_results
    if type(pydl_results) == str:
        print('Loading periodicity results')
        dl_df = load_results(pydl_results)
    elif type(pydl_results)==pd.core.frame.DataFrame:
        dl_df = pydl_results
    
    dl_df.rename(columns={'p_reg': 'dl_reg_pval', 'p_reg_norm': 'dl_reg_pval_norm'}, inplace=True)
    jtk_df.rename(columns={'p-value': 'jtk_per_pval'}, inplace=True)

    # normalize jtk p-values for use in dlxjtk score
    jtk_df['jtk_per_pval_norm'] = jtk_df['jtk_per_pval'] / np.median(jtk_df['jtk_per_pval'])

    # merge dl and jtk dataframes
    dlxjtk_df = pd.merge(dl_df, jtk_df, left_index=True, right_index=True)
    dlxjtk_df = dlxjtk_df[['dl_reg_pval', 'dl_reg_pval_norm', 'jtk_per_pval', 'jtk_per_pval_norm']]

    # compute dlxjtk score and sort genes by the score
    dlxjtk_df['dlxjtk_score'] = dlxjtk_df.apply(dlxjtk_func, axis=1)
    dlxjtk_df.sort_values(by='dlxjtk_score', axis=0, ascending=True, inplace=True)

    return dlxjtk_df





############ LEM functions ############

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


def run_lem(dataset, target_list, repressor_list, activator_list, num_proc=2, verbose=False):
    '''
    Run LEMpy on a time series dataset, specifying what genes are targets, transcriptional repressors and transcription activators.
    ** Gene names must be in the time series dataset. **

    dataset: The time series dataset as a dataframe. This dataframe must be the same as was used in the periodicity algorithms. 
    target_list: a list of gene names which LEM will treat as targets
    repressor_list: a list of gene names which LEM will treat as transcriptional repressors
    activator_list: a list of gene names which LEM will treat as transcription activators
    num_proc: the number of processors to use. Default: 2
    verbose: a boolean which tells LEMpy to print out statements from the code. Default: False

    ** NOTE: A gene can be both a target and a regulator, additionally, a gene that is a regulator can be a repressor and an activator. **
    ** Therefore, depending on the role of the gene, it can be in any combination of the three lists, inlcuding all of them. **

    '''

    datetimestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    tmp_data_file = f'../tmp/tmp_{datetimestr}.tsv'
    dataset.to_csv(tmp_data_file, sep='\t')

    user_dict = {'data_files':[tmp_data_file],
                'num_proc':num_proc,
                'verbose':verbose}

    user_config = ConfigObj(user_dict)
    full_lem_config = gen_lempy_config(user_config, tmp_data_file, target_list, repressor_list, activator_list, datetimestr)
    os.makedirs(os.path.split(full_lem_config.filename)[0])
    full_lem_config.write()

    lempy_path = '../src/lempy/lempy.py'
    full_cmd = ['mpiexec', '-n', str(num_proc), 'python', lempy_path, full_lem_config.filename]
    
    print(f'-- Running LEMpy on dataset {tmp_data_file}')

    submit_cmd = subprocess.Popen(full_cmd,
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
    
    print(f'-- Command used: {" ".join(full_cmd)}')

    output, error = submit_cmd.communicate()
    str_error = error.decode("utf-8").split('\n')
    str_output = output.decode("utf-8").split('\n')
    # print(str_output)
    if len(str_error) > 1:
        os.remove(tmp_data_file)
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

        os.remove(tmp_data_file)
        return all_scores_df, all_target_df, all_localmin_df