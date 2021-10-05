#!/Library/Frameworks/Python.framework/Python
#
# _run_ls_params.py
# BY:	Anastasia Deckard anastasia<dot>deckard<at>duke<dot>edu
# DATE:	2011 01 14
# DESCRIPTION
#	for running algorithm; creates dir and file names, collects params,
#	makes dir in results folder for alg if necessary, makes dir in alg folder
#	for run, saves parameter file, and executes alg with params.
# INPUTS
#	FOR FILES & DIRECTORIES
#	1.	data_file: the data file to run through the alg
#	2.	results_dir: general results directory for repository.
#		will add alg abbr to the path for you.
#	FOR ALGORITHM (see _run_ls_params.R for detailed descriptions)
#	3.	per_min: the minimum period to examine
#	4.	per_max: the maximum period to examine
#	5.	test_freq:	number of test frequencies to scan,
#		test_freq * #timepoints, so this is multiplier.
# ACTIONS
#	1. makes a run name of the form <data_name>_ls_<params>
#	2. makes a directory <results_dir>/ls
#	3. makes a directory <results_dir>/ls/<run_name>
#	4. writes parameters to file <results_dir>/ls/<run_name>/<run_name>_params.txt
#	5. calls _run_ls_params.R with arguments
#	6. saves log to file <results_dir>/ls/<run_name>/<run_name>_log.txt


import os, sys, datetime


#THE ALGORITHM"S ABBR FOR NAMING FILES AND DIRECTORIES
alg = "ls"

#PARAMETERS FOR RUNNING ALGORITHM
#default params
test_freq = 4
unit_type = "minutes"

#user specified params
if (len(sys.argv) == 5):	#using default params
	data_file = sys.argv[1]
	results_dir = sys.argv[2]
	per_min = sys.argv[3]
	per_max = sys.argv[4]
	print("using arguments from command line:")
elif (len(sys.argv) == 7):	#using all speficied params
	data_file = sys.argv[1]
	results_dir = sys.argv[2]
	per_min = sys.argv[3]
	per_max = sys.argv[4]
	test_freq = sys.argv[5]
	unit_type = sys.argv[6]
	print("using arguments from command line:")
else:
	print("Please provide 4 arguments (defaults for other params will be used):")
	print("data_file results_dir per_min per_max")
	print("Please provide 6 arguments:")
	print("data_file results_dir per_min per_max test_freq unit_type")
	exit()

print(data_file, results_dir, per_min, per_max, test_freq, unit_type)



#SETUP NAMES FOR DIRECTORIES AND FILES
data_name = os.path.splitext(os.path.basename(data_file))[0]
run_name = "%s_%s_p%s-%sf%s" %(data_name, alg, per_min, per_max, test_freq)
resrun_dir = os.path.join(results_dir, run_name)
print("run name: ", run_name)
print("run results dir: ", resrun_dir)

# resalg_dir = results_dir #os.path.join(results_dir, alg)
# resrun_dir = os.path.join(resalg_dir, run_name)
# print("run name: ", run_name)
# print("alg results dir: ", resalg_dir)
# print("run results dir: ", resrun_dir)


#MAKE RESULTS DIRECTORY
if not os.path.exists(resrun_dir):
	os.mkdir(resrun_dir)
	print("made: ", resrun_dir)


#WRITE PARAMETERS FILE TO OUT DIRECTORY
param_path = resrun_dir + "/" + run_name + "_params.txt"
param_file = open(param_path,"w")
param_file.write("data_file:\t" + data_file + "\n")
param_file.write("per_min:\t" + str(per_min) + "\n")
param_file.write("per_max:\t" + str(per_max) + "\n")
param_file.write("test_freq:\t" + str(test_freq) + "\n")
param_file.write("unit:\t" + unit_type + "\n")
param_file.close()

#MAKE COMMAND & RUN ALGORITHM, TIME IT
consout_path = resrun_dir + "/" + run_name + "_consout.txt"

cmd1 = "Rscript ../src/ls/_run_ls_params.R %s %s %s %s %s %s %s | tee %s" %(os.path.abspath(data_file), os.path.abspath(resrun_dir), run_name, per_min, per_max, test_freq, unit_type, os.path.abspath(consout_path))
print(cmd1)

time_beg = datetime.datetime.now()

os.system(cmd1)

time_end = datetime.datetime.now()
diff = time_end - time_beg

print("finished, with time: ", str(diff))

#WRITE OUT LOG FILE WITH TIME INFO
log_path = resrun_dir + "/" + run_name + "_log.txt"
log_file = open(log_path,"w")
log_file.write(cmd1 + "\n\n")
log_file.write("start:\t" + time_beg.strftime("%Y-%m-%d %H:%M:%S") + "\n")
log_file.write("end:\t" + time_end.strftime("%Y-%m-%d %H:%M:%S") + "\n")
log_file.write("time:\t" + str(diff) + "\n")
log_file.write("time (S):\t" + str(diff.total_seconds()) + "\n")
log_file.write("time (M):\t" + str(diff.total_seconds()/60) + "\n")
log_file.write("time (H):\t" + str(diff.total_seconds()/(60*60)) + "\n")
log_file.close()
