# efg, Stowers Institute for Medical Research
# July 2004.  Updated 15 Sept 2005.
#
# Lomb-Scargle Normalized Periodogram
#
# from
#   "Fast Algorithm for Spectral Analysis of Unevenly Sampled Data"
#   Astrophysical Journal, 338:277-280, March 1989.
#   William H. Press and George B. Rybicki.
#
# Also appeared in Section 13.8, "Spectral Analysis of Unevenly
# Sampled Data" in Numerical Recipes in C (2nd Ed), William H. Press,
# et al, Cambridge University Press, 1992.
#
# Aug 2004:  For now use global variable "unit" to be replaced in
# an application with "second", "minute", "hour", etc.  Default
# unit is simply "unit".

source("../src/ls/R-Mnemonics.R")
#source("http://research.stowers-institute.org/efg/2005/LombScargle/R/R-Mnemonics.R")

unit <<- "unit"             # Global variable for now.  Should be singular.
                            # Replace with second, minute, hour, ...
MAXSPD <<- 25               # Default for now but can be changed.
SHOW.LOESS.PEAK    <<- TRUE # Default that can be changed
SHOW.TIME.INTERVAL <<- TRUE # Show histogram of time intervals

SHOW.PLOT          <<- TRUE # Save time on batch runs by blocking plots
                            # in ComputeAndPlotLombScargle

# "h" is vector of expression values for time points "t".
# SpectralPowerDensity will be evaluated at given TestFrequencies.
# Nindepedent of the TestFrequencies are assumed to be independent.
ComputeLombScargle <- function(t, h, TestFrequencies, Nindependent)
{
  stopifnot( length(t) == length(h) )

  if (length(t) > 0)
  {
    Nyquist <- 1 / (2 * ( (max(t) - min(t) )/ length(t) ) )

    hResidual    <- h - mean(h)

    SpectralPowerDensity <- rep(0, length(TestFrequencies))

	
    for (i in 1:length(TestFrequencies))
    {
	
      Omega       <- 2*pi*TestFrequencies[i]
      TwoOmegaT   <- 2*Omega*t
      Tau         <- atan2( sum(sin(TwoOmegaT)) , sum(cos(TwoOmegaT))) /
                     (2*Omega)
      
		
      OmegaTMinusTau <- Omega * (t - Tau)
      SpectralPowerDensity[i] <- (sum (hResidual * cos(OmegaTMinusTau))^2) /
                                  sum( cos(OmegaTMinusTau)^2 ) +
                                 (sum (hResidual * sin(OmegaTMinusTau))^2) /
                                  sum( sin(OmegaTMinusTau)^2 )
    }

    # The "normalized" spectral density refers to the variance term in the
    # denominator.  With this term the SpectralPowerDensity has an
    # exponential probability distribution with unit mean.
    SpectralPowerDensity <- SpectralPowerDensity / ( 2 * var(h) )

    Probability <- 1 - (1-exp(-SpectralPowerDensity))^Nindependent

    PeakIndex    <- match(max(SpectralPowerDensity), SpectralPowerDensity)

    # Note:  Might merit more investigation when PeakIndex is the first point.
    PeakPeriod <- 1 / TestFrequencies[PeakIndex]
    PeakPvalue <- Probability[PeakIndex]

  } else {

    # Time series has 0 points
    Nyquist     <- NA
    Probability <- 1.0
    PeakIndex   <- NA
    SpectralPowerDensity <- NA
    PeakPeriod  <- NA
    PeakPvalue  <- 1.0
  }

  return( list( t=t,
                h=h,
                Frequency=TestFrequencies,
                Nyquist=Nyquist,
                SpectralPowerDensity=SpectralPowerDensity,
                Probability=Probability,
                PeakIndex=PeakIndex,
                PeakSPD=SpectralPowerDensity[PeakIndex],
                PeakPeriod=PeakPeriod,
                PeakPvalue=PeakPvalue,
                N=length(h),
                Nindependent=Nindependent
              ) )
}


########################################################################

# Time points "t" must be in ascending order with corresponding expression
# values in "h".  LS$t and LS$h have missing values removed, but t and h
# here do not.
PlotLombScargle <- function(LS, title, FigureLabels,
                            ShowIntervalHistogram=TRUE, Grid22=TRUE)
{
  # Show results graphically as suggested by MatLab code found on the
  # Woods Hole Oceanographic Institution web site:
  # http://w3eos.whoi.edu/12.747/notes/lect07/l07s05.html

  if (Grid22)
  {
    oldpar <- par(mfrow=c(2,2))  # 2 rows by 2 column2 of graphics
  }

  #########################################################
  # 1A. Original data curve
  PlotTitle <- title
  if ( nchar(FigureLabels) > 0 )
  {
    PlotTitle <- paste("(", substr(FigureLabels,1,1), ") ", PlotTitle, sep="")
  }
  plot(LS$t.all, LS$h.all,
       "o", col="Blue", ylab="Expression",
       xlab=paste("Time [", unit, "s]", sep=""),
       main=PlotTitle)
  mtext(paste("N =",length(LS$t)), TEXT_BELOW, col="blue", cex=0.8)
  abline(h=0)

  # Plot loess curve and peak if present
  if (SHOW.LOESS.PEAK & (!is.null(LS$h.loess)))
  {
    lines(LS$t.all, LS$h.loess, col="black", lty=LTY_DOTTED, lwd=2)
    points(LS$h.peak$maximum,LS$h.peak$objective, pch=PCH_CIRCLE, col="black")
  }


  if (ShowIntervalHistogram)
  {
    #########################################################
    # 2. Measure of uneveness of intervals
    # suppress this plot if all the t-deltas are the same

    if (SHOW.TIME.INTERVAL)
    {
      tIntervalTest <- LS$t
      if ( all(diff(tIntervalTest) == diff(tIntervalTest)[1]) )
      {
        # Don't bother showing anything if time deltas contant
        plot(0,type="n", axes=F, xlab="", ylab="")
      } else {
          PlotTitle <- "Time Interval Variability"
          if ( nchar(FigureLabels) > 0 )
          {
            PlotTitle <- paste("(", substr(FigureLabels,2,2), ") ", PlotTitle, sep="")
          }

          hist(log10(diff(tIntervalTest)), xlim=c(-1,1),
               xlab="log10(delta T)",
               main="Time Interval Variability")
      }
    } else {
      # is there an easier way to skip this graphics "slot"?
      plot(0,type="n", axes=F, xlab="", ylab="")
    }
  } else {

    # check if figure is 2-by-2 matrix of plots
    if (all( par()$mfrow == c(2,2) ))
    {
     # skip position (1,2) and continue next plot at (2,1)
      par(mfg=c(2,1, 2,2))
    }

  }


  #########################################################
  # 3. Lomb-Scargle Periodogram
  PlotTitle <- "Lomb-Scargle Periodogram"
  if ( nchar(FigureLabels) > 0 )
  {
    PlotTitle <- paste("(", substr(FigureLabels,3,3), ") ", PlotTitle, sep="")
  }
  plot(LS$Frequency, LS$SpectralPowerDensity,
       "o", col="Red",
       ylab="Normalized Power Spectral Density",
       xlab=paste("Frequency [1/", unit, "]", sep=""),
       main=PlotTitle,
       ylim=c(0,MAXSPD))

  # show probability levels on periodogram
  p <- c(0.05, 0.01, 0.001, 1e-4, 1e-5, 1e-6)
  for (k in 1:length(p))
  {
    z <- -log( 1 - (1-p[k])^(1/LS$Nindependent) )
    abline(h=z, col="gray", lty=LTY_DOTTED)
    text(LS$Frequency[length(LS$Frequency)],z,
         paste("p = ", p[k], sep=""),
         cex=0.7, pos=TEXT_LEFT, col="gray")
  }

  points(LS$Frequency[LS$PeakIndex], LS$SpectralPowerDensity[LS$PeakIndex],
       pch=PCH_CIRCLE, col="Red")
  mtext(paste("Period at Peak = ", round(LS$PeakPeriod,1), " ", unit, "s", sep=""),
        TEXT_ABOVE)
  if ( (LS$Nyquist >= LS$Frequency[1])   &
       (LS$Nyquist <= LS$Frequency[length(LS$Frequency)]) )
  {
    abline(v=LS$Nyquist, col="green")
    text(LS$Nyquist, 12.5, "Nyquist", pos=TEXT_RIGHT, col="green")
  }


  #########################################################
  # 4. Probability (significance of peak)
  PlotTitle <- "Peak Significance"
  if ( nchar(FigureLabels) > 0 )
  {
    PlotTitle <- paste("(", substr(FigureLabels,4,4), ") ", PlotTitle, sep="")
  }
  plot(LS$Frequency, LS$Probability,
       "o", col="Red",
       ylab="Probability", xlab=paste("Frequency [1/", unit, "]", sep=""),
       main=PlotTitle,
       ylim=c(0,1))
  points(LS$Frequency[LS$PeakIndex], LS$Probability[LS$PeakIndex],
       pch=PCH_CIRCLE, col="Red")
  mtext(paste("p = ", sprintf("%.3g",LS$PeakPvalue), " at Peak"), TEXT_ABOVE)
  if ( (LS$Nyquist >= LS$Frequency[1])   &
       (LS$Nyquist <= LS$Frequency[length(LS$Frequency)]) )
  {
    abline(v=LS$Nyquist, col="green")
    text(LS$Nyquist, 0.5, "Nyquist", pos=TEXT_RIGHT, col="green")
  }

  if (Grid22)
  {
    par(oldpar)   # Reset to original settings
  }
}


# Use this regression equation for estimating the number of independent
# frequencies for calls to ComputeLombScargle or ComputeAndPlotLombScargle.
#
########################################################################

# Estimate of number of independent frequencies in Lomb-Scargle
# analysis based on sample size.  From Horne and Baliunas,
# "A Prescription for Period Analysis of Unevenly Sampled Time Series",
# The Astrophysical Journal, 392: 757-763, 1986.
# Could trunc or round result

NHorneBaliunas <- function(N)
{
  Nindependent <- trunc(-6.362 + 1.193*N + 0.00098*N^2)
  if (Nindependent < 1)
  {
    Nindependent <- 1   # Kludge for now
  }
  return(Nindependent)
}


########################################################################

# Remove missing (na) and not-a-number (NaN) expression values.
# All time points are assumed to be present, but not necessarily in order.
# This routine will order time points and expression values in ascending
# time order.  The plot is suppressed for an 0-length time series.
ComputeAndPlotLombScargle <- function(t, h, TestFrequencies,
                                      Nindependent, title,
                                      FigureLabels="",
                                      GridOption=TRUE,
                                      IntervalHistogramOption=TRUE)
{
  # re-order in case out of time order
  h <- h[ order(t) ]
  t <- t[ order(t) ]

  # only pass non-NA, non-NaN values.
  t2 <- t[!(is.na(h) | is.nan(h))]
  h2 <- h[!(is.na(h) | is.nan(h))]

  # Order by time
  h2 <- h2[ order(t2) ]
  t2 <- t2[ order(t2) ]

  N <- length(h2)

  LS <- ComputeLombScargle(t2, h2, TestFrequencies, Nindependent)
  LS$t.all     <- t
  LS$h.all     <- h

  if (SHOW.LOESS.PEAK & (N > 5))
  {
    # Compute loess smoothed curve and find peak (assume only one for now)
    loess.fit <- loess(h ~ t, data.frame(t=t, h=h))
    h.loess   <- predict(loess.fit, data.frame(t=t))
    h.peak    <- optimize(function(t, model)
                             predict(model, data.frame(t=t)),
                             c(min(t),max(t)),
                             maximum=TRUE,
                             model=loess.fit)

    LS$h.loess   <- h.loess
    LS$h.peak    <- h.peak
  }
  else
  {
    LS$h.loess <- NULL
    LS$h.peak  <- list(maximum=NaN,objective=NaN)
  }

# moved to main function, by anastasia, 2013 10 15
#  if (N > 0 & SHOW.PLOT)
#  {
#    PlotLombScargle(LS, title, FigureLabels,
#                    Grid22=GridOption,
#                    ShowIntervalHistogram=IntervalHistogramOption)
#   }

  return(LS)
}
