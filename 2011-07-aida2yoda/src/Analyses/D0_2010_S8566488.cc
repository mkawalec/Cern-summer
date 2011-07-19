// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Tools/BinnedHistogram.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"

namespace Rivet {


  /// @brief D0 dijet invariant mass measurement
  class D0_2010_S8566488 : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    D0_2010_S8566488()
      : Analysis("D0_2010_S8566488")
    {
      setBeams(PROTON, ANTIPROTON);
      setNeedsCrossSection(true);
    }

    //@}


  public:

    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {

      FinalState fs;
      FastJets conefinder(fs, FastJets::D0ILCONE, 0.7);
      addProjection(conefinder, "ConeFinder");

      _h_m_dijet.addHistogram(0.0, 0.4, bookHistogram1D(1, 1, 1));
      _h_m_dijet.addHistogram(0.4, 0.8, bookHistogram1D(2, 1, 1));
      _h_m_dijet.addHistogram(0.8, 1.2, bookHistogram1D(3, 1, 1));
      _h_m_dijet.addHistogram(1.2, 1.6, bookHistogram1D(4, 1, 1));
      _h_m_dijet.addHistogram(1.6, 2.0, bookHistogram1D(5, 1, 1));
      _h_m_dijet.addHistogram(2.0, 2.4, bookHistogram1D(6, 1, 1));
    }


    /// Perform the per-event analysis
    void analyze(const Event& e) {
      const double weight = e.weight();

      const Jets& jets = applyProjection<JetAlg>(e, "ConeFinder").jetsByPt(40.0*GeV);
      if (jets.size() < 2) vetoEvent;

      FourMomentum j0(jets[0].momentum());
      FourMomentum j1(jets[1].momentum());
      double ymax = std::max(fabs(j0.rapidity()), fabs(j1.rapidity()));
      double mjj = FourMomentum(j0+j1).mass();

      _h_m_dijet.fill(ymax, mjj/TeV, weight);
    }


    /// Normalise histograms etc., after the run
    void finalize() {
      _h_m_dijet.scale(crossSection()/sumOfWeights(), this);
    }

    //@}


  private:

    // Data members like post-cuts event weight counters go here


  private:

    /// @name Histograms
    //@{
    BinnedHistogram<double> _h_m_dijet;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<D0_2010_S8566488> plugin_D0_2010_S8566488;


}
