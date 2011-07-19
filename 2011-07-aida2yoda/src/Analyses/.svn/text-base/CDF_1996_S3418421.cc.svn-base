// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Tools/BinnedHistogram.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"

namespace Rivet {


  /// @brief CDF dijet angular distributions
  class CDF_1996_S3418421 : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    CDF_1996_S3418421()
      : Analysis("CDF_1996_S3418421")
    {
      setBeams(PROTON, ANTIPROTON);
    }

    //@}


  public:

    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {
      FinalState fs(-4.2, 4.2);
      addProjection(FastJets(fs, FastJets::CDFJETCLU, 0.7), "Jets");

      _h_chi.addHistogram(241.0, 300.0, bookHistogram1D(1, 1, 1));
      _h_chi.addHistogram(300.0, 400.0, bookHistogram1D(1, 1, 2));
      _h_chi.addHistogram(400.0, 517.0, bookHistogram1D(1, 1, 3));
      _h_chi.addHistogram(517.0, 625.0, bookHistogram1D(1, 1, 4));
      _h_chi.addHistogram(625.0, 1800.0, bookHistogram1D(1, 1, 5));

      _h_ratio = bookDataPointSet(2,1,1,"","","");
      _chi_above_25.resize(_h_ratio->size());
      _chi_below_25.resize(_h_ratio->size());
    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();

      Jets jets = applyProjection<FastJets>(event, "Jets").jetsByPt(50.0*GeV);
      if (jets.size()<2) {
        vetoEvent;
      }
      FourMomentum jet1 = jets[0].momentum();
      FourMomentum jet2 = jets[1].momentum();
      double eta1 = jet1.eta();
      double eta2 = jet2.eta();
      double chi = exp(fabs(eta1-eta2));
      if (fabs(eta2)>2.0 || fabs(eta1)>2.0 || chi>5.0) {
        vetoEvent;
      }

      double m = FourMomentum(jet1+jet2).mass();
      _h_chi.fill(m, chi, weight);

      // fill ratio counter
      if (m > _h_ratio->lowerExtent(0) && m < _h_ratio->upperExtent(0)) {
        int bin=-1;
        for (int i=0; i<_h_ratio->size(); ++i) {
          AIDA::IMeasurement* x = _h_ratio->point(i)->coordinate(0);
          if (m > x->value()-x->errorMinus() && m < x->value()+x->errorPlus()) {
            bin=i;
            break;
          }
        }
        if (bin>-1) {
          if (chi>2.5) _chi_above_25[bin] += weight;
          else _chi_below_25[bin] += weight;
        }
      }
    }


    /// Normalise histograms etc., after the run
    void finalize() {

      foreach (AIDA::IHistogram1D* hist, _h_chi.getHistograms()) {
        normalize(hist);
      }

      for (int bin=0; bin<_h_ratio->size(); ++bin) {
        _h_ratio->point(bin)->coordinate(1)->setValue(_chi_below_25[bin]/_chi_above_25[bin]);
        /// @todo calculate errors while analysing and fill them here as well
      }
    }

    //@}


  private:

    // Data members like post-cuts event weight counters go here
    std::vector<double> _chi_above_25;
    std::vector<double> _chi_below_25;

  private:

    /// @name Histograms
    //@{
    BinnedHistogram<double> _h_chi;
    AIDA::IDataPointSet* _h_ratio;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CDF_1996_S3418421> plugin_CDF_1996_S3418421;


}
