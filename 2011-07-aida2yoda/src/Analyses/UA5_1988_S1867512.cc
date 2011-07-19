// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Math/MathUtils.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/Beam.hh"
#include "Rivet/Projections/TriggerUA5.hh"

namespace Rivet {


  /// @brief UA5 charged particle correlations at 200, 546 and 900 GeV
  class UA5_1988_S1867512 : public Analysis {
  public:

    UA5_1988_S1867512() : Analysis("UA5_1988_S1867512")
    {
      setBeams(PROTON, ANTIPROTON);
      _sumWPassed = 0;
    }


    /// @name Analysis methods
    //@{

    void init() {
      // Projections
      addProjection(TriggerUA5(), "Trigger");

      // Symmetric eta interval
      addProjection(ChargedFinalState(-0.5, 0.5), "CFS05");

      // Asymmetric intervals first
      // Forward eta intervals
      addProjection(ChargedFinalState(0.0, 1.0), "CFS10F");
      addProjection(ChargedFinalState(0.5, 1.5), "CFS15F");
      addProjection(ChargedFinalState(1.0, 2.0), "CFS20F");
      addProjection(ChargedFinalState(1.5, 2.5), "CFS25F");
      addProjection(ChargedFinalState(2.0, 3.0), "CFS30F");
      addProjection(ChargedFinalState(2.5, 3.5), "CFS35F");
      addProjection(ChargedFinalState(3.0, 4.0), "CFS40F");

      // Backward eta intervals
      addProjection(ChargedFinalState(-1.0,  0.0), "CFS10B");
      addProjection(ChargedFinalState(-1.5, -0.5), "CFS15B");
      addProjection(ChargedFinalState(-2.0, -1.0), "CFS20B");
      addProjection(ChargedFinalState(-2.5, -1.5), "CFS25B");
      addProjection(ChargedFinalState(-3.0, -2.0), "CFS30B");
      addProjection(ChargedFinalState(-3.5, -2.5), "CFS35B");
      addProjection(ChargedFinalState(-4.0, -3.0), "CFS40B");

      // Histogram booking, we have sqrt(s) = 200, 546 and 900 GeV
      // TODO use DataPointSet to be able to output errors
      if (fuzzyEquals(sqrtS()/GeV, 200.0, 1E-4)) {
        _hist_correl = bookDataPointSet(2, 1, 1);
        _hist_correl_asym = bookDataPointSet(3, 1, 1);
      } else if (fuzzyEquals(sqrtS()/GeV, 546.0, 1E-4)) {
        _hist_correl = bookDataPointSet(2, 1, 2);
        _hist_correl_asym = bookDataPointSet(3, 1, 2);
      } else if (fuzzyEquals(sqrtS()/GeV, 900.0, 1E-4)) {
        _hist_correl = bookDataPointSet(2, 1, 3);
        _hist_correl_asym = bookDataPointSet(3, 1, 3);
      }
    }


    void analyze(const Event& event) {
      // Trigger
      const bool trigger = applyProjection<TriggerUA5>(event, "Trigger").nsdDecision();
      if (!trigger) vetoEvent;
      _sumWPassed += event.weight();

      // Count forward/backward particles
      n_10f += applyProjection<ChargedFinalState>(event, "CFS10F").size();
      n_15f += applyProjection<ChargedFinalState>(event, "CFS15F").size();
      n_20f += applyProjection<ChargedFinalState>(event, "CFS20F").size();
      n_25f += applyProjection<ChargedFinalState>(event, "CFS25F").size();
      n_30f += applyProjection<ChargedFinalState>(event, "CFS30F").size();
      n_35f += applyProjection<ChargedFinalState>(event, "CFS35F").size();
      n_40f += applyProjection<ChargedFinalState>(event, "CFS40F").size();
      //
      n_10b += applyProjection<ChargedFinalState>(event, "CFS10B").size();
      n_15b += applyProjection<ChargedFinalState>(event, "CFS15B").size();
      n_20b += applyProjection<ChargedFinalState>(event, "CFS20B").size();
      n_25b += applyProjection<ChargedFinalState>(event, "CFS25B").size();
      n_30b += applyProjection<ChargedFinalState>(event, "CFS30B").size();
      n_35b += applyProjection<ChargedFinalState>(event, "CFS35B").size();
      n_40b += applyProjection<ChargedFinalState>(event, "CFS40B").size();
      //
      n_05 += applyProjection<ChargedFinalState>(event, "CFS05").size();
    }


    void finalize() {
      // The correlation strength is defined in formulas
      // 4.1 and 4.2

      // Fill histos, gap width histo comes first
      //      * Set the errors as Delta b / sqrt(sumWPassed) with
      //      Delta b being the absolute uncertainty of b according to
      //      Gaussian error-propagation (linear limit) and assuming
      //      Poissonian uncertainties for the number of particles in
      //      the eta-intervals
      //
      
      // Define vectors to be able to fill DataPointSets

      vector<double> xvals;
      vector<double> xerrs;
      vector<double> yvals;
      vector<double> yerrs;


      // This defines the binning eventually
      for (int i=0; i<7; i++) {
        xvals.push_back(static_cast<double>(i));
        xerrs.push_back(0.5);
      }

      // Fill the y-value vector
      yvals.push_back(correlation(n_10f, n_10b));
      yvals.push_back(correlation(n_15f, n_15b));
      yvals.push_back(correlation(n_20f, n_20b));
      yvals.push_back(correlation(n_25f, n_25b));
      yvals.push_back(correlation(n_30f, n_30b));
      yvals.push_back(correlation(n_35f, n_35b));
      yvals.push_back(correlation(n_40f, n_40b));

      // Fill the y-error vector
      yerrs.push_back(correlation_err(n_10f, n_10b)/sqrt(_sumWPassed));
      yerrs.push_back(correlation_err(n_15f, n_15b)/sqrt(_sumWPassed));
      yerrs.push_back(correlation_err(n_20f, n_20b)/sqrt(_sumWPassed));
      yerrs.push_back(correlation_err(n_25f, n_25b)/sqrt(_sumWPassed));
      yerrs.push_back(correlation_err(n_30f, n_30b)/sqrt(_sumWPassed));
      yerrs.push_back(correlation_err(n_35f, n_35b)/sqrt(_sumWPassed));
      yerrs.push_back(correlation_err(n_40f, n_40b)/sqrt(_sumWPassed));

      // Fill the DPS
      _hist_correl->setCoordinate(0, xvals, xerrs);
      _hist_correl->setCoordinate(1, yvals, yerrs);

      // Now do the other histo -- clear already defined vectors first
      xvals.clear();
      xerrs.clear();
      yvals.clear();
      yerrs.clear();

      // Different binning for this one
      for (int i=0; i<6; i++) {
        xvals.push_back(0.5* static_cast<double>(i));
        xerrs.push_back(0.25);
      }

      // Fill gap-center histo (Fig 15)
      //
      // The first bin contains the c_str strengths of
      // the gap size histo that has ane eta gap of two
      //
      // Fill the y-value vector
      yvals.push_back(correlation(n_20f, n_20b));
      yvals.push_back(correlation(n_25f, n_15b));
      yvals.push_back(correlation(n_30f, n_10b));
      yvals.push_back(correlation(n_35f, n_05 ));
      yvals.push_back(correlation(n_40f, n_10f));

      // Fill the y-error vector
      yerrs.push_back(correlation_err(n_20f, n_20b)/sqrt(_sumWPassed));
      yerrs.push_back(correlation_err(n_25f, n_15b)/sqrt(_sumWPassed));
      yerrs.push_back(correlation_err(n_30f, n_10b)/sqrt(_sumWPassed));
      yerrs.push_back(correlation_err(n_35f, n_05 )/sqrt(_sumWPassed));
      yerrs.push_back(correlation_err(n_40f, n_10f)/sqrt(_sumWPassed));


      // Fill in correlation strength for assymetric intervals,
      // see Tab. 5
      // Fill the DPS
      _hist_correl_asym->setCoordinate(0, xvals, xerrs);
      _hist_correl_asym->setCoordinate(1, yvals, yerrs);
    }

    //@}


  private:

    /// @name Counters
    //@{
    double _sumWPassed;
    //@}


    /// @name Vectors for storing the number of particles in the different eta intervals per event.
    /// @todo Is there a better way?
    //@{
    std::vector<int> n_10f;
    std::vector<int> n_15f;
    std::vector<int> n_20f;
    std::vector<int> n_25f;
    std::vector<int> n_30f;
    std::vector<int> n_35f;
    std::vector<int> n_40f;
    //
    std::vector<int> n_10b;
    std::vector<int> n_15b;
    std::vector<int> n_20b;
    std::vector<int> n_25b;
    std::vector<int> n_30b;
    std::vector<int> n_35b;
    std::vector<int> n_40b;
    //
    std::vector<int> n_05;
    //@}


    /// @name Histograms
    //@{
    // Symmetric eta intervals
    AIDA::IDataPointSet *_hist_correl;
    // For asymmetric eta intervals
    AIDA::IDataPointSet *_hist_correl_asym;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<UA5_1988_S1867512> plugin_UA5_1988_S1867512;

}
