// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/UnstableFinalState.hh"
#include "Rivet/Projections/MissingMomentum.hh"
#include "LWH/Histogram1D.h"

namespace Rivet {


  /// Generic analysis looking at various distributions of final state particles
  class MC_GENERIC : public Analysis {
  public:

    /// Constructor
    MC_GENERIC()
      : Analysis("MC_GENERIC")
    {    }


  public:

    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {

      // Projections
      const FinalState cnfs(-5.0, 5.0, 500*MeV);
      addProjection(cnfs, "FS");
      addProjection(ChargedFinalState(-5.0, 5.0, 500*MeV), "CFS");
      addProjection(UnstableFinalState(-5.0, 5.0, 500*MeV), "UFS");
      //addProjection(MissingMomentum(cnfs), "ETmiss");

      // Histograms
      // @todo Choose E/pT ranged based on input energies... can't do anything about kin. cuts, though
      _histMult   = bookHistogram1D("Mult", 100, -0.5, 199.5);
      _histMultCh = bookHistogram1D("MultCh", 100, -0.5, 199.5);

      _histStablePIDs  = bookHistogram1D("MultsStablePIDs", 3335, -0.5, 3334.5);
      _histDecayedPIDs = bookHistogram1D("MultsDecayedPIDs", 3335, -0.5, 3334.5);
      _histAllPIDs  = bookHistogram1D("MultsAllPIDs", 3335, -0.5, 3334.5);

      _histPt    = bookHistogram1D("Pt", 300, 0, 30);
      _histPtCh  = bookHistogram1D("PtCh", 300, 0, 30);

      _histE    = bookHistogram1D("E", 100, 0, 200);
      _histECh  = bookHistogram1D("ECh", 100, 0, 200);

      _histEta    = bookHistogram1D("Eta", 50, -5, 5);
      _histEtaCh  = bookHistogram1D("EtaCh", 50, -5, 5);
      _tmphistEtaPlus.reset(new LWH::Histogram1D(25, 0, 5));
      _tmphistEtaMinus.reset(new LWH::Histogram1D(25, 0, 5));
      _tmphistEtaChPlus.reset(new LWH::Histogram1D(25, 0, 5));
      _tmphistEtaChMinus.reset(new LWH::Histogram1D(25, 0, 5));

      _histEtaPi       = bookHistogram1D("EtaPi", 25, 0, 5);
      _histEtaK        = bookHistogram1D("EtaK", 25, 0, 5);
      _histEtaLambda   = bookHistogram1D("EtaLambda", 25, 0, 5);
      _histEtaSumEt    = bookProfile1D("EtaSumEt", 25, 0, 5);

      _histRapidity    = bookHistogram1D("Rapidity", 50, -5, 5);
      _histRapidityCh  = bookHistogram1D("RapidityCh", 50, -5, 5);
      _tmphistRapPlus.reset(new LWH::Histogram1D(25, 0, 5));
      _tmphistRapMinus.reset(new LWH::Histogram1D(25, 0, 5));
      _tmphistRapChPlus.reset(new LWH::Histogram1D(25, 0, 5));
      _tmphistRapChMinus.reset(new LWH::Histogram1D(25, 0, 5));

      _histPhi    = bookHistogram1D("Phi", 50, 0, TWOPI);
      _histPhiCh  = bookHistogram1D("PhiCh", 50, 0, TWOPI);
    }



    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();

      // Unphysical (debug) plotting of all PIDs in the event, physical or otherwise
      foreach (const GenParticle* gp, particles(event.genEvent())) {
        _histAllPIDs->fill(abs(gp->pdg_id()), weight);
      }

      // Charged + neutral final state
      const FinalState& cnfs = applyProjection<FinalState>(event, "FS");
      MSG_DEBUG("Total multiplicity = " << cnfs.size());
      _histMult->fill(cnfs.size(), weight);
      foreach (const Particle& p, cnfs.particles()) {
        _histStablePIDs->fill(abs(p.pdgId()), weight);
        const double eta = p.momentum().eta();
        _histEta->fill(eta, weight);
        _histEtaSumEt->fill(fabs(eta), p.momentum().Et(), weight);
        if (eta > 0) {
          _tmphistEtaPlus->fill(fabs(eta), weight);
        } else {
          _tmphistEtaMinus->fill(fabs(eta), weight);
        }
        const double rapidity = p.momentum().rapidity();
        _histRapidity->fill(rapidity, weight);
        if (rapidity > 0) {
          _tmphistRapPlus->fill(fabs(rapidity), weight);
        } else {
          _tmphistRapMinus->fill(fabs(rapidity), weight);
        }
        _histPt->fill(p.momentum().pT()/GeV, weight);
        _histE->fill(p.momentum().E()/GeV, weight);
        _histPhi->fill(p.momentum().phi(), weight);
      }

      const FinalState& cfs = applyProjection<FinalState>(event, "CFS");
      MSG_DEBUG("Total charged multiplicity = " << cfs.size());
      _histMultCh->fill(cfs.size(), weight);
      foreach (const Particle& p, cfs.particles()) {
        const double eta = p.momentum().eta();
        _histEtaCh->fill(eta, weight);
        if (eta > 0) {
          _tmphistEtaChPlus->fill(fabs(eta), weight);
        } else {
          _tmphistEtaChMinus->fill(fabs(eta), weight);
        }
        const double rapidity = p.momentum().rapidity();
        _histRapidityCh->fill(rapidity, weight);
        if (rapidity > 0) {
          _tmphistRapChPlus->fill(fabs(rapidity), weight);
        } else {
          _tmphistRapChMinus->fill(fabs(rapidity), weight);
        }
        _histPtCh->fill(p.momentum().pT()/GeV, weight);
        _histECh->fill(p.momentum().E()/GeV, weight);
        _histPhiCh->fill(p.momentum().phi(), weight);
      }


      // Histogram identified particle eta spectra
      const UnstableFinalState& ufs = applyProjection<UnstableFinalState>(event, "UFS");
      foreach (const Particle& p, ufs.particles()) {
        const double eta_abs = fabs(p.momentum().eta());
        _histDecayedPIDs->fill(p.pdgId(), weight);
        const PdgId pid = abs(p.pdgId());
        //if (PID::isMeson(pid) && PID::hasStrange()) {
        if (pid == 211 || pid == 111) _histEtaPi->fill(eta_abs, weight);
        else if (pid == 321 || pid == 130 || pid == 310) _histEtaK->fill(eta_abs, weight);
        else if (pid == 3122) _histEtaLambda->fill(eta_abs, weight);
        // const MissingMomentum& met = applyProjection<MissingMomentum>(event, "ETmiss");
      }

    }



    /// Finalize
    void finalize() {
      scale(_histMult, 1/sumOfWeights());
      scale(_histMultCh, 1/sumOfWeights());

      scale(_histStablePIDs, 1/sumOfWeights());
      scale(_histDecayedPIDs, 1/sumOfWeights());
      scale(_histAllPIDs, 1/sumOfWeights());

      scale(_histEta, 1/sumOfWeights());
      scale(_histEtaCh, 1/sumOfWeights());

      scale(_histEtaPi, 1/sumOfWeights());
      scale(_histEtaK, 1/sumOfWeights());
      scale(_histEtaLambda, 1/sumOfWeights());

      scale(_histRapidity, 1/sumOfWeights());
      scale(_histRapidityCh, 1/sumOfWeights());

      scale(_histPt, 1/sumOfWeights());
      scale(_histPtCh, 1/sumOfWeights());

      scale(_histE, 1/sumOfWeights());
      scale(_histECh, 1/sumOfWeights());

      scale(_histPhi, 1/sumOfWeights());
      scale(_histPhiCh, 1/sumOfWeights());

      histogramFactory().divide(histoPath("EtaPMRatio"), *_tmphistEtaPlus, *_tmphistEtaMinus);
      histogramFactory().divide(histoPath("EtaChPMRatio"), *_tmphistEtaChPlus, *_tmphistEtaChMinus);
      histogramFactory().divide(histoPath("RapidityPMRatio"), *_tmphistRapPlus, *_tmphistRapMinus);
      histogramFactory().divide(histoPath("RapidityChPMRatio"), *_tmphistRapChPlus, *_tmphistRapChMinus);
    }

    //@}


  private:

    /// Temporary histos used to calculate eta+/eta- ratio plot
    shared_ptr<LWH::Histogram1D> _tmphistEtaPlus, _tmphistEtaMinus;
    shared_ptr<LWH::Histogram1D> _tmphistEtaChPlus, _tmphistEtaChMinus;
    shared_ptr<LWH::Histogram1D> _tmphistRapPlus, _tmphistRapMinus;
    shared_ptr<LWH::Histogram1D> _tmphistRapChPlus, _tmphistRapChMinus;

    //@{
    /// Histograms
    AIDA::IHistogram1D *_histMult, *_histMultCh;
    AIDA::IHistogram1D *_histStablePIDs, *_histDecayedPIDs, *_histAllPIDs;
    AIDA::IHistogram1D *_histEtaPi, *_histEtaK, *_histEtaLambda;
    AIDA::IProfile1D   *_histEtaSumEt;
    AIDA::IHistogram1D *_histEta, *_histEtaCh;
    AIDA::IHistogram1D *_histRapidity, *_histRapidityCh;
    AIDA::IHistogram1D *_histPt, *_histPtCh;
    AIDA::IHistogram1D *_histE, *_histECh;
    AIDA::IHistogram1D *_histPhi, *_histPhiCh;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<MC_GENERIC> plugin_MC_GENERIC;

}
