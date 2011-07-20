// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"
#include "Rivet/Projections/MissingMomentum.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/ClusteredPhotons.hh"
#include "Rivet/Projections/LeadingParticlesFinalState.hh"

namespace Rivet {


  class ATLAS_2010_S8919674 : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    ATLAS_2010_S8919674()
      : Analysis("ATLAS_2010_S8919674")
    {
      setNeedsCrossSection(true);
    }

    //@}


  public:

    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {

      /// Initialise and register projections (selections on the final state)
      // projection to find the electrons
      std::vector<std::pair<double, double> > eta_e;
      eta_e.push_back(make_pair(-2.47,-1.52));
      eta_e.push_back(make_pair(-1.37,1.37));
      eta_e.push_back(make_pair(1.52,2.47));
      IdentifiedFinalState elecs(eta_e, 20.0*GeV);
      elecs.acceptIdPair(ELECTRON);
      addProjection(elecs, "elecs");
      // projection for finding the photons which have to be clustered into
      // the lepton later
      ClusteredPhotons cphotons_e(FinalState(), elecs, 0.1);
      addProjection(cphotons_e, "cphotons_e");

      // projection to find the muons
      std::vector<std::pair<double, double> > eta_m;
      eta_m.push_back(make_pair(-2.4,2.4));
      IdentifiedFinalState muons(eta_m, 20.0*GeV);
      muons.acceptIdPair(MUON);
      addProjection(muons, "muons");
      // projection for finding the photons which have to be clustered into
      // the lepton later
      ClusteredPhotons cphotons_m(FinalState(), muons, 0.1);
      addProjection(cphotons_m, "cphotons_m");

      // Leading neutrinos for Etmiss
      FinalState fs;
      LeadingParticlesFinalState muon_neutrino(fs);
      muon_neutrino.addParticleIdPair(NU_MU);
      addProjection(muon_neutrino, "muon_neutrino");
      LeadingParticlesFinalState elec_neutrino(fs);
      elec_neutrino.addParticleIdPair(NU_E);
      addProjection(elec_neutrino, "elec_neutrino");

      // Input for the jets: No neutrinos, no muons, and no electron which
      // passed the electron cuts ("elecs" finalstate from above)
      VetoedFinalState veto;
      veto.addVetoOnThisFinalState(elecs);
      veto.addVetoPairId(MUON);
      veto.vetoNeutrinos();
      FastJets jets(veto, FastJets::ANTIKT, 0.4);
      addProjection(jets, "jets");



      /// book histograms
      _h_el_njet_inclusive = bookHisto1D(1,1,1);
      _h_mu_njet_inclusive = bookHisto1D(2,1,1);

      _h_el_pT_jet1 = bookHisto1D(5,1,1);
      _h_mu_pT_jet1 = bookHisto1D(6,1,1);

      _h_el_pT_jet2 = bookHisto1D(7,1,1);
      _h_mu_pT_jet2 = bookHisto1D(8,1,1);
    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();

      const FinalState& elecs = applyProjection<FinalState>(event, "elecs");
      ParticleVector elec_neutrino=applyProjection<FinalState>(event, "elec_neutrino").particles();
      if (elecs.size()==1 && elec_neutrino.size()>0) {
        FourMomentum lepton=elecs.particles()[0].momentum();
        foreach (const Particle& photon,
                 applyProjection<FinalState>(event, "cphotons_e").particles()) {
          lepton+=photon.momentum();
        }
        FourMomentum p_miss = elec_neutrino[0].momentum();
        double mT=sqrt(2.0*lepton.pT()*p_miss.Et()*(1.0-cos(lepton.phi()-p_miss.phi())));
        if (p_miss.Et()>25.0*GeV && mT>40.0*GeV) {
          Jets jets;
          foreach (const Jet& jet, applyProjection<FastJets>(event, "jets").jetsByPt(20.0*GeV)) {
            if (fabs(jet.eta())<2.8 && deltaR(lepton, jet.momentum())>0.5) {
              jets.push_back(jet);
            }
          }

          _h_el_njet_inclusive->fill(0, weight);
          if (jets.size()>=1) {
            _h_el_njet_inclusive->fill(1, weight);
            _h_el_pT_jet1->fill(jets[0].momentum().pT(), weight);
          }
          if (jets.size()>=2) {
            _h_el_njet_inclusive->fill(2, weight);
            _h_el_pT_jet2->fill(jets[1].momentum().pT(), weight);
          }
          if (jets.size()>=3) {
            _h_el_njet_inclusive->fill(3, weight);
          }
        }
      }

      const FinalState& muons = applyProjection<FinalState>(event, "muons");
      ParticleVector muon_neutrino=applyProjection<FinalState>(event, "muon_neutrino").particles();
      if (muons.size()==1 && muon_neutrino.size()>0) {
        FourMomentum lepton=muons.particles()[0].momentum();
        foreach (const Particle& photon,
                 applyProjection<FinalState>(event, "cphotons_m").particles()) {
          lepton+=photon.momentum();
        }
        FourMomentum p_miss = muon_neutrino[0].momentum();
        double mT=sqrt(2.0*lepton.pT()*p_miss.Et()*(1.0-cos(lepton.phi()-p_miss.phi())));
        if (p_miss.Et()>25.0*GeV && mT>40.0*GeV) {
          Jets jets;
          foreach (const Jet& jet, applyProjection<FastJets>(event, "jets").jetsByPt(20.0*GeV)) {
            if (fabs(jet.eta())<2.8 && deltaR(lepton, jet.momentum())>0.5) {
              jets.push_back(jet);
            }
          }

          _h_mu_njet_inclusive->fill(0, weight);
          if (jets.size()>=1) {
            _h_mu_njet_inclusive->fill(1, weight);
            _h_mu_pT_jet1->fill(jets[0].momentum().pT(), weight);
          }
          if (jets.size()>=2) {
            _h_mu_njet_inclusive->fill(2, weight);
            _h_mu_pT_jet2->fill(jets[1].momentum().pT(), weight);
          }
          if (jets.size()>=3) {
            _h_mu_njet_inclusive->fill(3, weight);
          }
          if (jets.size()>=4) {
            _h_mu_njet_inclusive->fill(4, weight);
          }
        }
      }

    }


    /// Normalise histograms etc., after the run
    void finalize() {
      double normfac=crossSection()/sumOfWeights();
      scale(_h_el_njet_inclusive, normfac);
      scale(_h_mu_njet_inclusive, normfac);
      scale(_h_el_pT_jet1, normfac);
      scale(_h_mu_pT_jet1, normfac);
      scale(_h_el_pT_jet2, normfac);
      scale(_h_mu_pT_jet2, normfac);
    }

    //@}


  private:

    /// @name Histograms
    //@{

    Histo1DPtr _h_el_njet_inclusive;
    Histo1DPtr _h_mu_njet_inclusive;
    Histo1DPtr _h_el_pT_jet1;
    Histo1DPtr _h_mu_pT_jet1;
    Histo1DPtr _h_el_pT_jet2;
    Histo1DPtr _h_mu_pT_jet2;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<ATLAS_2010_S8919674> plugin_ATLAS_2010_S8919674;


}
