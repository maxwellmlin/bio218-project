LOMB-SCARGLE V2
2013 10 15

Reference: Glynn EF, Chen J, Mushegian A. 2006. Detecting periodic patterns in unevenly spaced gene expression time series using Lomb–Scargle periodograms. Bioinformatics, 22: 310–316.
Code Source: http://research.stowers-institute.org/efg/2005/LombScargle/


RUNNING

This program can be run by executing _run_ls_params.R or _run_ls_param.py. The R script takes parameters, reads data files, runs the algorithm and prints results. The python script was designed to make life easier when running the program multiple times; it creates names for directories and files, creates directories, saves a file with the parameters, and saves a log file with times, and calls the algorithm and passes it parameters. 

To run using the python script from the command line:
python _run_ls_params.py data_file results_dir per_min per_max

It will handle creating a run name and necessary directories:
run_name: <data_name>_ls_<params>
run_dir: <results_dir>/ls/<run_name>
output files: <run_dir>/<run_name>_<alg_output>.tsv or .txt


To run using the R script from the command line:
Rscript _run_ls_params.R data_file run_dir run_name per_min per_max

It will write files to:
output files: <run_dir>/<run_name>_<alg_output>.tsv or .txt


Please see the python and R scripts for detailed descriptions of the inputs.



RESTRICTIONS ON RUNNING

Missing or uneven samples
LS can handle unevenly spaced samples.
e.g. times: 10 20 30 33 37 40 *can* be run.

Blanks
LS can handle blank in the data.
e.g. values: 30 27 "" 78 *can* be run.

Periods Lengths
Can search for period lengths that are greater than or smaller than the length of the time in the data. 
e.g. if data covers times 1-24, you can search for periods of length 8 or 24 or 36.
Note that if you search for period lengths greater than the length of time in the data (e.g. looking for period length of 24 hours in data that only covers 12 hours),
the results might be misleading.
There should be more than two data points in the smallest period length.
e.g. times: 0 2 4 6 8 ..., so the interval is 2, then the smallest period length to search for should be greater than 4. 



OUTPUT

<run_name>_summary.tsv
Shows the period that had the most significant p-value. 
The columns of interest are:
probe:  id of the profile.
p:  the p-value for that profile.
Period:    the period for that profile.


<run_name>_pvalues.tsv
Shows the p-values for each period that was tested (columns) for each profile (rows).