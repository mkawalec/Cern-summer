// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/LeadingParticlesFinalState.hh"

namespace Rivet {


  /// @brief CDF inclusive isolated prompt photon cross-section
  class CDF_2009_S8436959 : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    CDF_2009_S8436959()
      : Analysis("CDF_2009_S8436959")
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
      addProjection(fs, "FS");

      LeadingParticlesFinalState photonfs(FinalState(-1.0, 1.0, 30.0*GeV));
      photonfs.addParticleId(PHOTON);
      addProjection(photonfs, "LeadingPhoton");

      _h_Et_photon = bookHistogram1D(1, 1, 1);

    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();

      ParticleVector fs = applyProjection<FinalState>(event, "FS").particles();
      ParticleVector photons = applyProjection<LeadingParticlesFinalState>(event, "LeadingPhoton").particles();
      if (photons.size()!=1) {
        vetoEvent;
      }
      FourMomentum leadingPhoton = photons[0].momentum();
      double eta_P = leadingPhoton.eta();
      double phi_P = leadingPhoton.phi();
      FourMomentum mom_in_cone;
      foreach (const Particle& p, fs) {
        if (deltaR(eta_P, phi_P, p.momentum().eta(), p.momentum().phi()) < 0.4) {
            mom_in_cone += p.momentum();
        }
      }
      if (mom_in_cone.Et()-leadingPhoton.Et() > 2.0*GeV) {
        vetoEvent;
      }
      _h_Et_photon->fill(leadingPhoton.Et(), weight);
    }


    /// Normalise histograms etc., after the run
    void finalize() {
      scale(_h_Et_photon, crossSection()/sumOfWeights()/2.0);
    }

    //@}


  private:

    /// @name Histograms
    //@{
    AIDA::IHistogram1D *_h_Et_photon;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CDF_2009_S8436959> plugin_CDF_2009_S8436959;


}
