#  ProcessLombScargleDataset.R:
#  Common processing for datasets of expression profiles.
#
#  efg, Stowers Institute for Medical Research
#  July 2004.  Updated 18 July 2005.
#

source("../src/ls/R-Mnemonics.R")
#source("R-efg.R") #commented out anastasia 2013 10 15
source("../src/ls/LombScargle.R")

###############################################################################

ShowExpressionStatistics <- function(Expression)
{
  # Column Statistics
  Expression.Mean    <- apply(Expression, APPLY_TO_COLUMNS, mean, na.rm=TRUE)
  Expression.StDev   <- apply(Expression, APPLY_TO_COLUMNS, sd,   na.rm=TRUE)
  Expression.Max     <- apply(Expression, APPLY_TO_COLUMNS, max,  na.rm=TRUE)
  Expression.Min     <- apply(Expression, APPLY_TO_COLUMNS, min,  na.rm=TRUE)


  # Prepare matrix for matplot
  y <-  matrix( c(Expression.Min,
                  Expression.Mean-Expression.StDev,
                  Expression.Mean,
                  Expression.Mean+Expression.StDev,
                  Expression.Max),
                  nc=5, length(Expression.Mean) )

  matplot(1:ncol(Expression), y,
    ylim=c(-8,4), type='lloll',
    col=c("red", "blue", "black", "blue", "red"), pch=PCH_CIRCLE,
    lty=LTY_SOLID,
    ylab="Log2 Expression", xlab="Time[hours]",
    main="Expression vs. Time")
  mtext("(Mean, +/- 1 Standard Deviation, Range)", TEXT_ABOVE)
  abline(h=0)
}


###############################################################################

# List "d" structure is returned by routine LoadPlasmodiumData, but could be
# any list with elements:  Time, ID, Expression, TestFrequencies.
# Parameter "j" gives index of row to process
ShowSingleProbeProfile <- function(d, j, Title="")
{
  if (Title == "")
  {
    Title <- d$ID[j]
  }

  # Use number of non-missing values in regression formula
  Nindependent <- NHorneBaliunas(sum(!is.na(d$Expression[j,])))

  return (ComputeAndPlotLombScargle( d$Time, d$Expression[j,],
                                     d$TestFrequencies,
                                     Nindependent,
                                     Title) )
}


###############################################################################

ShowSingleProbeProfileByName <- function(d, probe, Title="")
{
  Lookup <- 1:length(d$ID)
  names(Lookup) <- d$ID

  if  (is.na( Lookup[probe] ) )
  {
    cat("probe '", probe, "' not found\n")
  }
  else
  {
    return( ShowSingleProbeProfile(d, Lookup[probe], Title))
  }
}


###############################################################################

# Write three files to disk for future analysis
# 1. Dominant.CSV     index, probe name, dominant period, p value
# 2. Periodogram.CSV  index, probe name, periodogram array
# 3. pValue.CSV       index, probe name, p-Value array
# MODIFIED to write tsv files, with name_type.tsv
# dominant changed to summary

ProcessExpressionDataset <- function(path, results_name, Time, ID, Expression, TestFrequencies, SavePlots=FALSE)
{
  stopifnot( length(ID)   == nrow(Expression) )
  stopifnot( length(Time) == ncol(Expression) )

  outDominant <- file(paste(path, .Platform$file.sep, results_name, "_summary.tsv", sep=""),     "w")
  cat("index\tprobe\tPhaseShift\tPhaseShiftHeight\tPeakIndex\tPeakSPD\tPeriod\tp-value\tN\tNindependent\tNyquist\n",
      file=outDominant)

  outPeriod   <- file(paste(path, .Platform$file.sep, results_name, "_periodogram.tsv", sep=""),  "w")
  cat("index\tprobe", file=outPeriod)
  for (j in 1:length(TestFrequencies) )
  {
    #cat(paste(",F", j, sep=""), file=outPeriod)
    cat(paste("\t", 1/TestFrequencies[j], sep=""), file=outPeriod)
  }
  cat(paste("\n"), file=outPeriod)

  outPvalue   <- file(paste(path, .Platform$file.sep, results_name, "_pvalues.tsv", sep=""),       "w")
  cat("index\tprobe", file=outPvalue)
  for (j in 1:length(TestFrequencies) )
  {
    #cat(paste(",F", j, sep=""), file=outPvalue)
    cat(paste("\t", 1/TestFrequencies[j], sep=""), file=outPvalue)
  }
  cat("\n", file=outPvalue)

  pdf(paste(path, .Platform$file.sep, results_name, "_plots.pdf", sep=""))
  
  for (j in 1:length(ID))
  {
    cat(j, ID[j],"\n")
    if (.Platform$OS.type == "windows")
    {
      flush.console() # display immediately in Windows
    }

    Nindependent <- NHorneBaliunas(sum(!is.na(Expression[j,])))

    LS <- ComputeAndPlotLombScargle(Time, Expression[j,],
                                    TestFrequencies,
                                    Nindependent,
                                    ID[j])
                               
#     if (SavePlots)
#     {
#       WriteStampedPDF(paste(path, .Platform$file.sep, "charts", .Platform$file.sep,
#                     ID[j], ".pdf", sep=""))
#     }
    
    
    # moved to main function, by anastasia, 2013 10 15
    FigureLabels=""
    GridOption=TRUE
    IntervalHistogramOption=TRUE
    title = ID[j]
    if (N > 0 & SHOW.PLOT)
    {
      PlotLombScargle(LS, title, FigureLabels,
                      Grid22=GridOption,
                      ShowIntervalHistogram=IntervalHistogramOption)
    }
    #end moved 
    
    
    cat(sprintf("%d\t%s\t%.2f\t%.2f\t%d\t%.3f\t%.3f\t%.3g\t%d\t%.0f\t%.3f\n",
                j, ID[j],
                LS$h.peak$maximum,
                LS$h.peak$objective,
                LS$PeakIndex,
                LS$PeakSPD,
                LS$PeakPeriod,
                LS$PeakPvalue,
                LS$N,
                LS$Nindependent,
                LS$Nyquist),
        file=outDominant)

    cat(paste(j, ID[j], sep="\t"), file=outPeriod)
    for (k in 1:length(LS$SpectralPowerDensity))
    {
      cat("\t", LS$SpectralPowerDensity[k], sep="", file=outPeriod)
    }
    cat("\n", file=outPeriod)

    cat(paste(j, ID[j], sep="\t"), file=outPvalue)
    for (k in 1:length(LS$Probability))
    {
      cat("\t", LS$Probability[k], sep="", file=outPvalue)
    }
    cat("\n", file=outPvalue)
  }
  
  dev.off()
  close(outDominant)
  close(outPeriod)
  close(outPvalue)
  

}
