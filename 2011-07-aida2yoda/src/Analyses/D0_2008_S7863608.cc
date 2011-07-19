// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/ZFinder.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/RivetAIDA.hh"

namespace Rivet {


  /// @brief D0 differential Z/\f$ \gamma^* \f$ + jet + \f$ X \f$ cross sections
  /// @author Gavin Hesketh, Andy Buckley, Frank Siegert
  class D0_2008_S7863608 : public Analysis {
  public:

    /// @name Construction
    //@{
    /// Constructor
    D0_2008_S7863608() : Analysis("D0_2008_S7863608")
    {
      setBeams(PROTON, ANTIPROTON);
      setNeedsCrossSection(true);
    }

    //@}


    /// @name Analysis methods
    //@{

    /// Book histograms
    void init() {
      ZFinder zfinder(-1.7, 1.7, 15.0*GeV, MUON, 65.0*GeV, 115.0*GeV, 0.2, false, true);
      addProjection(zfinder, "ZFinder");

      FastJets conefinder(zfinder.remainingFinalState(), FastJets::D0ILCONE, 0.5);
      addProjection(conefinder, "ConeFinder");

      _sum_of_weights_inclusive=0.0;

      _h_jet_pT_cross_section = bookHistogram1D(1, 1, 1);
      _h_jet_pT_normalised = bookHistogram1D(1, 1, 2);
      _h_jet_y_cross_section = bookHistogram1D(2, 1, 1);
      _h_jet_y_normalised = bookHistogram1D(2, 1, 2);
      _h_Z_pT_cross_section = bookHistogram1D(3, 1, 1);
      _h_Z_pT_normalised = bookHistogram1D(3, 1, 2);
      _h_Z_y_cross_section = bookHistogram1D(4, 1, 1);
      _h_Z_y_normalised = bookHistogram1D(4, 1, 2);
      _h_total_cross_section = bookHistogram1D(5, 1, 1);
    }



    // Do the analysis
    void analyze(const Event& e) {
      const double weight = e.weight();

      const ZFinder& zfinder = applyProjection<ZFinder>(e, "ZFinder");
      if (zfinder.particles().size()==1) {
        _sum_of_weights_inclusive += weight;
        const JetAlg& jetpro = applyProjection<JetAlg>(e, "ConeFinder");
        const Jets& jets = jetpro.jetsByPt(20.0*GeV);
        Jets jets_cut;
        foreach (const Jet& j, jets) {
          if (fabs(j.momentum().pseudorapidity()) < 2.8) {
            jets_cut.push_back(j);
          }
        }

        // Return if there are no jets:
        if(jets_cut.size()<1) {
          getLog() << Log::DEBUG << "Skipping event " << e.genEvent().event_number()
                   << " because no jets pass cuts " << endl;
          vetoEvent;
        }

        const FourMomentum Zmom = zfinder.particles()[0].momentum();

        // In jet pT
        _h_jet_pT_cross_section->fill( jets_cut[0].momentum().pT(), weight);
        _h_jet_pT_normalised->fill( jets_cut[0].momentum().pT(), weight);
        _h_jet_y_cross_section->fill( fabs(jets_cut[0].momentum().rapidity()), weight);
        _h_jet_y_normalised->fill( fabs(jets_cut[0].momentum().rapidity()), weight);

        // In Z pT
        _h_Z_pT_cross_section->fill(Zmom.pT(), weight);
        _h_Z_pT_normalised->fill(Zmom.pT(), weight);
        _h_Z_y_cross_section->fill(fabs(Zmom.rapidity()), weight);
        _h_Z_y_normalised->fill(fabs(Zmom.rapidity()), weight);

        _h_total_cross_section->fill(1960.0, weight);
      }
    }



    /// Finalize
    void finalize() {
      const double invlumi = crossSection()/sumOfWeights();
      scale(_h_total_cross_section, invlumi);
      scale(_h_jet_pT_cross_section, invlumi);
      scale(_h_jet_y_cross_section, invlumi);
      scale(_h_Z_pT_cross_section, invlumi);
      scale(_h_Z_y_cross_section, invlumi);

      double factor=1.0/_sum_of_weights_inclusive;
      if (_sum_of_weights_inclusive==0.0) factor=0.0;
      scale(_h_jet_pT_normalised, factor);
      scale(_h_jet_y_normalised, factor);
      scale(_h_Z_pT_normalised, factor);
      scale(_h_Z_y_normalised, factor);
    }

    //@}


  private:

    /// @name Histograms
    //@{
    AIDA::IHistogram1D * _h_jet_pT_cross_section;
    AIDA::IHistogram1D * _h_jet_y_cross_section;
    AIDA::IHistogram1D * _h_Z_pT_cross_section;
    AIDA::IHistogram1D * _h_Z_y_cross_section;
    AIDA::IHistogram1D * _h_total_cross_section;
    AIDA::IHistogram1D * _h_jet_pT_normalised;
    AIDA::IHistogram1D * _h_jet_y_normalised;
    AIDA::IHistogram1D * _h_Z_pT_normalised;
    AIDA::IHistogram1D * _h_Z_y_normalised;
    //@}

    double _sum_of_weights_inclusive;

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<D0_2008_S7863608> plugin_D0_2008_S7863608;

}
