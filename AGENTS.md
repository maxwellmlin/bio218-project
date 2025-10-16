# Repository Guidelines

## Project Structure & Module Organization
- `src/` stores shared libraries: `lempy/` for Local Edge Machine inference, `pyjtk/` for rhythmicity statistics, `ls/` for Lomb-Scargle utilities (Python & R), `pydl/` for delay embedding, and `utilities.py` for cross-cutting helpers.
- `notebooks/` contains hands-on workflows; duplicate `data_to_network_demo.ipynb` when prototyping and clear notebook outputs before committing.
- `datasets/` holds raw time-series inputs; keep generated tables, plots, and logs inside `results/` using dataset-prefixed folders.
- `ODE_model_LEM/` bundles reference ODE runs and synthetic data; align new experiments under a similarly named subdirectory for traceability.

## Build, Test, and Development Commands
- `git submodule update --init --recursive` pulls the bundled analysis code expected by notebooks and scripts.
- `conda env create -f conda_req.yml` provisions the `BioClocksClass` environment; rerun with `--force` only when dependencies change.
- `conda activate BioClocksClass` selects the environment before opening notebooks or running scripts.
- `jupyter lab` launches the primary development interface; `bash start_jupyter.sh` does the same on managed workstations.
- `python src/ls/_run_ls_params.py --help` exposes the Lomb-Scargle batch CLI; adapt the example flags for new parameter sweeps.

## Coding Style & Naming Conventions
- Adhere to PEP 8 with 4-space indentation and grouped imports as shown in `src/lempy/lempy.py`; keep function docstrings concise but descriptive.
- Use snake_case for Python modules, lower-case hyphenated names for results folders, and sentence-case titles inside notebooks.
- When editing R scripts in `src/ls`, match existing tidyverse-style spacing and comment with `#` explaining non-obvious parameters.

## Testing Guidelines
- No automated test runner is bundled; validate changes by re-executing `notebooks/data_to_network_demo.ipynb` and any notebook tied to your edits.
- For `lempy` changes, run `mpiexec -n 4 python src/lempy/lempy.py src/lempy/exp/synnet_3_config.txt` and confirm posterior summaries match expectations.
- Capture before/after plots or metric tables under `results/` and describe deviations in your PR to document behavioral impact.

## Commit & Pull Request Guidelines
- Write concise, imperative commit subjects (e.g., `Add synthetic dataset loader`) and include a short body when touching datasets or submodules.
- In PRs, link related notebooks or datasets, summarize reproduction steps, and attach representative figures or tables as images or markdown.
- Ensure `git status --submodule` is clean, and call out any environment updates or new data requirements in the PR checklist.

## Data & Access Notes
- Keep large datasets out of Git; document acquisition steps in the main `README.md` or a dedicated note inside `datasets/` if new sources are required.
- Avoid hard-coded absolute paths; rely on `src/utilities.DATADIR` or relative paths so notebooks stay portable across student environments.

## Descriptions of Functions
Note: For more information on each function including the arguments that the function needs, 
read the associated doc string in the utilities.py file or type “help(function_name)” into a 
jupyter notebook cell and run it.    
Utility Functions:  
• view_data_toc  
Prints the Dataset Table of Contents file. Displays a table describing each available 
dataset. This is the same table on the main page of the Biological Clocks Class GitLab 
repository.  
• load_dataset  
Loads a dataset into a dataframe, using the name of the dataset found in the “Dataset” 
column of the Dataset Table of Contents.  
• load_results  
Loads results from periodicity algorithms or LEMpy into a dataframe, using the name of 
the results file (for pyJTK and pyDL) or directory (or Lomb-Scargle and LEMpy).  
• duplicate_check  
Checks for duplicates within a dataset dataframe and prints out tips for what to do with 
the duplicates.  
• remove_duplicates  
Removes duplicate gene names by one of two methods supplied to the function.  
Method 1: keep only the duplicate with the highest gene expression at any time point. 
Method 2: keep the duplicate with the highest average gene expression.  
• relabel_duplicates  
Relabels duplicate gene names by appending “dupN” to each duplicate name where N is 
an integer.  
• intersection  
Returns a list that consists of the intersection of two supplied lists.  
• uniques  
Returns the unique genes in each the two supplied lists. Unique genes are those are not 
in the intersection of the two lists.  
• get_genelist_from_top_n_genes  
Returns a gene list consisting of the top n genes based off a specified periodicity score 
and a specified number of genes.  
• get_genelist_from_threshold  
Returns gene list consisting of the top genes based off a specified periodicity score and a 
specified numeric threshold on the periodicity score.  
• normalize_data  
Z-score normalizes a time series dataframe.  
Visualization Functions:  
• plot_heatmap  
Plots gene expression in a heatmap. Genes to plot are based on a user supplied 
threshold on a periodicity score. Orders the heatmap on the peak gene expression from 
the first period.  
• plot_heatmap_in_supplied_order  
Plots genes from a dataset in a heatmap ordered by a supplied order of gene names.  
• plot_linegraphs_from_gene_list  
Plots genes from a dataset from the supplied gene list in line plots. Can only plot 
between 1 and 10 genes.  
• plot_linegraphs_from_top_periodicity  
Plots the top n genes from a dataset in line plots. Top genes are determined based on 
supplied gene number and the supplied periodicity results.  
• make_network_from_edge_list  
Makes an interactive network graph from a list of edges in LEM edge specification.  
• make_top_edge_network  
Makes an interactive network graph from the top n edges from the LEM all scores 
dataframe.   
Periodicity Functions:   
Note: For descriptions of individual tools, check the Tools section of the README.  
• run_pyjtk  
Uses pyJTK to analyze the periodicity of each gene in a time series dataset dataframe. • 
run_pydl  
Uses pyDL to analyze the periodicity of each gene in a time series dataset dataframe.  
• run_ls  
Uses Lomb-Scargle to analyze the periodicity of each gene in a time series dataset 
dataframe.  
• run_periodicity  
Uses pyJTK, pyDL, and Lomb-Scargle on a single dataset to analyze and rank the 
periodicity of a time series dataset. Returns individual results for each periodicity 
algorithm.  
LEM Functions:  
Note: For descriptions of individual tools, check the Tools section of the README.  
• run_lem  
Runs LEMpy on a time series dataset dataframe, specifying what genes are targets, 
transcriptional repressors, and transcriptional regulators.  
 
Stripey Functions: 
• interpolate_timepoints 
Interpolates specified timepoints of a timeseries dataframe to handle stripeys. 
• quantile_normalize 
Quantile normalizes a timeseries dataframe to handle stripeys. 