# This file has been modified to work with 
# our automated system for the biochronicity project.
# 2012 01 30
# INPUTS:
#	FOR FILES & DIRECTORIES	
#	1.	data_file: (string) the data file to run through the alg.
#		File should be tab delimited, no quotes. 
#		The first row contains time labels (float). 
#		The first column contains the IDs (string). 
#		Position 1,1 usually has some text (like "probe"). 
#		The cell values are numeric (float).
#	2.	results_dir: (string) path to directory where files will be saved.
#	3.	results_name: (string) first part of file name for all saved files.
#	FOR ALGORITHM
#	4.	per_min: (float|int) the minimum period for range of periods to examine.
#	5.	per_max: (float|int) the maximum period for range of periods to examine.
#	6.	test_freq:	(float) number of test frequencies to scan,
#		test_freq * #timepoints, so this is multiplier. Suggested 2 or 4.
#	7.	unit_type: (string) unit for timepoints, e.g. "min", "hr". etc.
#
# SAVES:
#	1.	<results_dir>/<results_name>_Dominant.tsv
#		for each record, lists the information for the "best" period.
#		tab delimited, no quotes.
#	2.	<results_dir>/<results_name>_pValues.tsv
#		for each record, reports the adjusted pval for each period tested.
#		tab delimited, no quotes.


# Example of processing time series set
# efg, Stowers Institute for Medical Research, July 2005

source("../src/ls/ProcessLombScargleDataset.R")


args = commandArgs(trailingOnly = TRUE)
data_file = args[1]
results_dir = args[2]
results_name = args[3] 
per_min = as.numeric(args[4])
per_max = as.numeric(args[5])
test_freq = as.numeric(args[6])
unit_type = args[7]


# ====================================================================
# 1. Read data into Data Frame called RawData
filename <- data_file

# (use as.is=TRUE if IDs in column 1 are NOT unique
RawData <- read.table(file=filename, header=FALSE, sep="\t", quote="", comment.char = "#", stringsAsFactors = FALSE)
#print("Sample of:")
#print(filename)
#print(RawData[1:10,])

# ====================================================================
# 2. Define data elements needed for Lomb-Scargle Analysis

# 2.1  First column has IDs
ID <- as.character(RawData[2:nrow(RawData),1])
#cat("FIRST ID: ", ID[1], "\n")
#cat("LAST ID:  ", ID[nrow(RawData)-1], "\n")

# 2.2  Define time points for time series (need not be uniform)
# (do not use t for time here since it is reserved in R for transpose)
Time <- as.numeric(RawData[1, 2:ncol(RawData)])
#cat("TIMEPOINTS: ", Time, "\n")

# 2.3  Remaining columns have expression time series
Expression <- data.matrix(RawData[2:nrow(RawData),2:ncol(RawData)])
#cat("FIRST DATA ROW: ", Expression[1,], "\n")
#cat("LAST DATA ROW:  ", Expression[nrow(RawData)-1,], "\n")


# Check for consistency between Expression and Time
N <- ncol(Expression)  # number of time points in series
stopifnot(length(Time) == N)

# Define global value used by Lomb-Scargle to label plots
unit <<- unit_type

# 2.4  Define number of test frequencies:  normally 2N or 4N
M <- N * test_freq
print(M)

# Frequencies usually easier to define in terms of 1/Period.
# In this case since "dominant" frequency is expected to correspond
# to 24-hour period, lets search frequencies corresponding to
# periods from 6 hours to 48 hours.
MinFrequency <- 1 / per_max
MaxFrequency <- 1 / per_min

# See if MaxFrequency is perhaps too high
if (MaxFrequency > 1/(2*mean(diff(Time))))
{
  cat("MaxFrequency may be above Nyquist limit.\n")
}

TestFrequencies <- MinFrequency +
                  (MaxFrequency - MinFrequency) * (0:(M-1) / (M-1))

# 2.5 Define relative path for results and make sure directories exist

SLASH <- .Platform$file.sep
if (! file.exists(results_dir) )
{
  dir.create(results_dir)

  # only needed if SavePlots=TRUE (see below)
  # The "chart" directory will contain PDFs of the Lomb-Scargle analysis
  dir.create(paste(results_dir, SLASH, "charts", sep=""))
}



# ====================================================================
# 3. Process the time series
ProcessExpressionDataset(results_dir, results_name,
                         Time, ID, Expression,
                         TestFrequencies,
                         SavePlots=FALSE)
