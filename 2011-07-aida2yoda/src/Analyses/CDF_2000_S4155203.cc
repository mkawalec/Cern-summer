// -*- C++ -*-
// CDF Z pT analysis

#include "Rivet/Analysis.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/ZFinder.hh"

namespace Rivet {


  /// @brief CDF Run I Z \f$ p_\perp \f$ in Drell-Yan events
  /// @author Hendrik Hoeth
  class CDF_2000_S4155203 : public Analysis {
  public:

    /// Constructor
    CDF_2000_S4155203()
      : Analysis("CDF_2000_S4155203")
    {
      setBeams(PROTON, ANTIPROTON);
      setNeedsCrossSection(true);
    }


    /// @name Analysis methods
    //@{

    void init() {
      // Set up projections
      ZFinder zfinder(-MAXRAPIDITY, MAXRAPIDITY, 0.0*GeV, ELECTRON,
                      66.0*GeV, 116.0*GeV, 0.0, false, false);
      addProjection(zfinder, "ZFinder");

      // Book histogram
      _hist_zpt = bookHisto1D(1, 1, 1);
    }


    /// Do the analysis
    void analyze(const Event& e) {
      const ZFinder& zfinder = applyProjection<ZFinder>(e, "ZFinder");
      if (zfinder.particles().size() != 1) {
        MSG_DEBUG("Num e+ e- pairs found = " << zfinder.particles().size());
        vetoEvent;
      }

      FourMomentum pZ = zfinder.particles()[0].momentum();
      if (pZ.mass2() < 0) {
        MSG_DEBUG("Negative Z mass**2 = " << pZ.mass2()/GeV2 << "!");
        vetoEvent;
      }

      MSG_DEBUG("Dilepton mass = " << pZ.mass()/GeV << " GeV");
      MSG_DEBUG("Dilepton pT   = " << pZ.pT()/GeV << " GeV");
      _hist_zpt->fill(pZ.pT()/GeV, e.weight());
    }


    void finalize() {
      scale(_hist_zpt, crossSection()/picobarn/sumOfWeights());
    }

    //@}


  private:

    Histo1DPtr _hist_zpt;

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CDF_2000_S4155203> plugin_CDF_2000_S4155203;

}
