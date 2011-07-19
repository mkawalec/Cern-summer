// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ZFinder.hh"
#include "Rivet/Projections/FastJets.hh"

namespace Rivet {


  /// @brief D0 Z+jets angular distributions
  class D0_2009_S8349509 : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    D0_2009_S8349509() : Analysis("D0_2009_S8349509"),
                         _inclusive_Z_sumofweights(0.0)
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

      _h_dphi_jet_Z25 = bookHistogram1D(1, 1, 1);
      _h_dphi_jet_Z45 = bookHistogram1D(2, 1, 1);

      _h_dy_jet_Z25 = bookHistogram1D(3, 1, 1);
      _h_dy_jet_Z45 = bookHistogram1D(4, 1, 1);

      _h_yboost_jet_Z25 = bookHistogram1D(5, 1, 1);
      _h_yboost_jet_Z45 = bookHistogram1D(6, 1, 1);

      _h_dphi_jet_Z25_xs = bookHistogram1D(1, 1, 2);
      _h_dphi_jet_Z45_xs = bookHistogram1D(2, 1, 2);

      _h_dy_jet_Z25_xs = bookHistogram1D(3, 1, 2);
      _h_dy_jet_Z45_xs = bookHistogram1D(4, 1, 2);

      _h_yboost_jet_Z25_xs = bookHistogram1D(5, 1, 2);
      _h_yboost_jet_Z45_xs = bookHistogram1D(6, 1, 2);

      _inclusive_Z_sumofweights = 0.0;
    }


    void analyze(const Event& event) {
      const double weight = event.weight();

      const ZFinder& zfinder = applyProjection<ZFinder>(event, "ZFinder");
      if (zfinder.particles().size()==1) {
        // count inclusive sum of weights for histogram normalisation
        _inclusive_Z_sumofweights += weight;

        const FourMomentum Zmom = zfinder.particles()[0].momentum();
        if (Zmom.pT()<25.0*GeV) {
          vetoEvent;
        }

        Jets jets;
        foreach (const Jet& j, applyProjection<JetAlg>(event, "ConeFinder").jetsByPt(20.0*GeV)) {
          if (fabs(j.momentum().pseudorapidity()) < 2.8) {
            jets.push_back(j);
            break;
          }
        }

        // Return if there are no jets:
        if (jets.size() < 1) {
          getLog() << Log::DEBUG << "Skipping event " << event.genEvent().event_number()
                   << " because no jets pass cuts " << endl;
          vetoEvent;
        }

        const FourMomentum jetmom = jets[0].momentum();
        double yZ = Zmom.rapidity();
        double yjet = jetmom.rapidity();
        double dphi = deltaPhi(Zmom.phi(), jetmom.phi());
        double dy = fabs(yZ-yjet);
        double yboost = fabs(yZ+yjet)/2.0;

        if (Zmom.pT() > 25.0*GeV) {
          _h_dphi_jet_Z25->fill(dphi,weight);
          _h_dy_jet_Z25->fill(dy, weight);
          _h_yboost_jet_Z25->fill(yboost, weight);
          _h_dphi_jet_Z25_xs->fill(dphi,weight);
          _h_dy_jet_Z25_xs->fill(dy, weight);
          _h_yboost_jet_Z25_xs->fill(yboost, weight);
        }
        if (Zmom.pT() > 45.0*GeV) {
          _h_dphi_jet_Z45->fill(dphi,weight);
          _h_dy_jet_Z45->fill(dy, weight);
          _h_yboost_jet_Z45->fill(yboost, weight);
          _h_dphi_jet_Z45_xs->fill(dphi,weight);
          _h_dy_jet_Z45_xs->fill(dy, weight);
          _h_yboost_jet_Z45_xs->fill(yboost, weight);
        }
      }

    }


    void finalize() {
      if (_inclusive_Z_sumofweights == 0.0) return;
      scale(_h_dphi_jet_Z25, 1.0/_inclusive_Z_sumofweights);
      scale(_h_dphi_jet_Z45, 1.0/_inclusive_Z_sumofweights);
      scale(_h_dy_jet_Z25, 1.0/_inclusive_Z_sumofweights);
      scale(_h_dy_jet_Z45, 1.0/_inclusive_Z_sumofweights);
      scale(_h_yboost_jet_Z25, 1.0/_inclusive_Z_sumofweights);
      scale(_h_yboost_jet_Z45, 1.0/_inclusive_Z_sumofweights);

      scale(_h_dphi_jet_Z25_xs, crossSectionPerEvent());
      scale(_h_dphi_jet_Z45_xs, crossSectionPerEvent());
      scale(_h_dy_jet_Z25_xs, crossSectionPerEvent());
      scale(_h_dy_jet_Z45_xs, crossSectionPerEvent());
      scale(_h_yboost_jet_Z25_xs, crossSectionPerEvent());
      scale(_h_yboost_jet_Z45_xs, crossSectionPerEvent());
    }

    //@}

  private:

    // Data members like post-cuts event weight counters go here

  private:

    /// @name Histograms (normalised)
    //@{
    AIDA::IHistogram1D *_h_dphi_jet_Z25;
    AIDA::IHistogram1D *_h_dphi_jet_Z45;

    AIDA::IHistogram1D *_h_dy_jet_Z25;
    AIDA::IHistogram1D *_h_dy_jet_Z45;

    AIDA::IHistogram1D *_h_yboost_jet_Z25;
    AIDA::IHistogram1D *_h_yboost_jet_Z45;
    //@}

    /// @name Histograms (absolute cross sections)
    //@{
    AIDA::IHistogram1D *_h_dphi_jet_Z25_xs;
    AIDA::IHistogram1D *_h_dphi_jet_Z45_xs;

    AIDA::IHistogram1D *_h_dy_jet_Z25_xs;
    AIDA::IHistogram1D *_h_dy_jet_Z45_xs;

    AIDA::IHistogram1D *_h_yboost_jet_Z25_xs;
    AIDA::IHistogram1D *_h_yboost_jet_Z45_xs;
    //@}

    double _inclusive_Z_sumofweights;

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<D0_2009_S8349509> plugin_D0_2009_S8349509;

}
