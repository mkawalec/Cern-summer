// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/LeadingParticlesFinalState.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/RivetYODA.hh"

namespace Rivet {


  /// @brief Measurement of isolated gamma + jet + X differential cross-sections
  ///
  /// Inclusive isolated gamma + jet cross-sections, differential in pT(gamma), for
  /// various photon and jet rapidity bins.
  ///
  /// @author Andy Buckley
  /// @author Gavin Hesketh
  class D0_2008_S7719523 : public Analysis {

  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    D0_2008_S7719523()
      : Analysis("D0_2008_S7719523")
    {
      setBeams(PROTON, ANTIPROTON);
      setNeedsCrossSection(true);
    }

    //@}


    /// @name Analysis methods
    //@{

    /// Set up projections and book histograms
    void init() {
      // General FS
      FinalState fs;
      addProjection(fs, "FS");

      // Get leading photon
      LeadingParticlesFinalState photonfs(FinalState(-1.0, 1.0, 30.0*GeV));
      photonfs.addParticleId(PHOTON);
      addProjection(photonfs, "LeadingPhoton");

      // FS excluding the leading photon
      VetoedFinalState vfs(fs);
      vfs.addVetoOnThisFinalState(photonfs);
      addProjection(vfs, "JetFS");

      // Jets
      FastJets jetpro(vfs, FastJets::D0ILCONE, 0.7);
      addProjection(jetpro, "Jets");

      // Histograms
      _h_central_same_cross_section = bookHisto1D(1, 1, 1);
      _h_central_opp_cross_section  = bookHisto1D(2, 1, 1);
      _h_forward_same_cross_section = bookHisto1D(3, 1, 1);
      _h_forward_opp_cross_section  = bookHisto1D(4, 1, 1);
    }



    /// Do the analysis
    void analyze(const Event& event) {
      const double weight = event.weight();

      // Get the photon
      const FinalState& photonfs = applyProjection<FinalState>(event, "LeadingPhoton");
      if (photonfs.particles().size() != 1) {
        vetoEvent;
      }
      const FourMomentum photon = photonfs.particles().front().momentum();

      // Isolate photon by ensuring that a 0.4 cone around it contains less than 7% of the photon's energy
      double egamma = photon.E();
      double eta_P = photon.pseudorapidity();
      double phi_P = photon.azimuthalAngle();
      double econe = 0.0;
      foreach (const Particle& p, applyProjection<FinalState>(event, "JetFS").particles()) {
        if (deltaR(eta_P, phi_P,
                   p.momentum().pseudorapidity(), p.momentum().azimuthalAngle()) < 0.4) {
          econe += p.momentum().E();
          // Veto as soon as E_cone gets larger
          if (econe/egamma > 0.07) {
            getLog() << Log::DEBUG << "Vetoing event because photon is insufficiently isolated" << endl;
            vetoEvent;
          }
        }
      }

      Jets jets = applyProjection<FastJets>(event, "Jets").jetsByPt(15.0*GeV);
      if (jets.size()==0) {
        vetoEvent;
      }
      FourMomentum leadingJet = jets[0].momentum();
      if (deltaR(eta_P, phi_P, leadingJet.eta(), leadingJet.phi())<0.7) {
        vetoEvent;
      }

      int photon_jet_sign = sign( leadingJet.rapidity() * photon.rapidity() );

      // Veto if leading jet is outside plotted rapidity regions
      const double abs_y1 = fabs(leadingJet.rapidity());
      if (inRange(abs_y1, 0.8, 1.5) || abs_y1 > 2.5) {
        getLog() << Log::DEBUG << "Leading jet falls outside acceptance range; |y1| = "
                 << abs_y1 << endl;
        vetoEvent;
      }

      // Fill histos
      if (fabs(leadingJet.rapidity()) < 0.8) {
        if (photon_jet_sign >= 1) {
          _h_central_same_cross_section->fill(photon.pT(), weight);
        } else {
          _h_central_opp_cross_section->fill(photon.pT(), weight);
        }
      } else if (inRange( fabs(leadingJet.rapidity()), 1.5, 2.5)) {
        if (photon_jet_sign >= 1) {
          _h_forward_same_cross_section->fill(photon.pT(), weight);
        } else {
          _h_forward_opp_cross_section->fill(photon.pT(), weight);
        }
      }

    }



    /// Finalize
    void finalize() {
      const double lumi_gen = sumOfWeights()/crossSection();
      const double dy_photon = 2.0;
      const double dy_jet_central = 1.6;
      const double dy_jet_forward = 2.0;

      // \todo YODA divide
      // Cross-section ratios (6 plots)
      // Central/central and forward/forward ratios
      // AIDA::IHistogramFactory& hf = histogramFactory();
      // const string dir = histoDir();

      // hf.divide(dir + "/d05-x01-y01", *_h_central_opp_cross_section, *_h_central_same_cross_section);
      // hf.divide(dir + "/d08-x01-y01", *_h_forward_opp_cross_section, *_h_forward_same_cross_section);

      // // Central/forward ratio combinations
      // hf.divide(dir + "/d06-x01-y01", *_h_central_same_cross_section,
      //           *_h_forward_same_cross_section)->scale(dy_jet_forward/dy_jet_central, 1);
      // hf.divide(dir + "/d07-x01-y01", *_h_central_opp_cross_section,
      //           *_h_forward_same_cross_section)->scale(dy_jet_forward/dy_jet_central, 1);
      // hf.divide(dir + "/d09-x01-y01", *_h_central_same_cross_section,
      //           *_h_forward_opp_cross_section)->scale(dy_jet_forward/dy_jet_central, 1);
      // hf.divide(dir + "/d10-x01-y01", *_h_central_opp_cross_section,
      //           *_h_forward_opp_cross_section)->scale(dy_jet_forward/dy_jet_central, 1);

      // Use generator cross section for remaining histograms
      // Each of these needs the additional factor 2 because the
      // y_photon * y_jet requirement reduces the corresponding 2D "bin width"
      // by a factor 1/2.
      scale(_h_central_same_cross_section, 2.0/lumi_gen * 1.0/dy_photon * 1.0/dy_jet_central);
      scale(_h_central_opp_cross_section, 2.0/lumi_gen * 1.0/dy_photon * 1.0/dy_jet_central);
      scale(_h_forward_same_cross_section, 2.0/lumi_gen * 1.0/dy_photon * 1.0/dy_jet_forward);
      scale(_h_forward_opp_cross_section, 2.0/lumi_gen * 1.0/dy_photon * 1.0/dy_jet_forward);
    }

    //@}

  private:

    /// @name Histograms
    //@{
    Histo1DPtr _h_central_same_cross_section;
    Histo1DPtr _h_central_opp_cross_section;
    Histo1DPtr _h_forward_same_cross_section;
    Histo1DPtr _h_forward_opp_cross_section;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<D0_2008_S7719523> plugin_D0_2008_S7719523;

}
