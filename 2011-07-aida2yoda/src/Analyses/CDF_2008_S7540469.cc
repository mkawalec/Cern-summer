// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Tools/Logging.hh"

namespace Rivet {


  /// @brief Measurement differential Z/\f$ \gamma^* \f$ + jet + \f$ X \f$ cross sections
  /// @author Frank Siegert
  class CDF_2008_S7540469 : public Analysis {

  public:

    /// Constructor
    CDF_2008_S7540469()
      : Analysis("CDF_2008_S7540469")
    {
      setBeams(PROTON, ANTIPROTON);
      setNeedsCrossSection(true);
    }


    /// @name Analysis methods
    //@{

    /// Book histograms
    void init() {
      // Full final state
      FinalState fs(-5.0, 5.0);
      addProjection(fs, "FS");

      // Leading electrons in tracking acceptance
      IdentifiedFinalState elfs(-5.0, 5.0, 25.0*GeV);
      elfs.acceptIdPair(ELECTRON);
      addProjection(elfs, "LeadingElectrons");

      _h_jet_multiplicity = bookHisto1D(1, 1, 1);
      _h_jet_pT_cross_section_incl_1jet = bookHisto1D(2, 1, 1);
      _h_jet_pT_cross_section_incl_2jet = bookHisto1D(3, 1, 1);
    }


    /// Do the analysis
    void analyze(const Event & event) {
      const double weight = event.weight();

      // Skip if the event is empty
      const FinalState& fs = applyProjection<FinalState>(event, "FS");
      if (fs.empty()) {
        getLog() << Log::DEBUG << "Skipping event " << event.genEvent().event_number()
                 << " because no final state pair found " << endl;
        vetoEvent;
      }

      // Find the Z candidates
      const FinalState & electronfs = applyProjection<FinalState>(event, "LeadingElectrons");
      std::vector<std::pair<Particle, Particle> > Z_candidates;
      ParticleVector all_els=electronfs.particles();
      for (size_t i=0; i<all_els.size(); ++i) {
        for (size_t j=i+1; j<all_els.size(); ++j) {
          bool candidate=true;
          double mZ=FourMomentum(all_els[i].momentum()+all_els[j].momentum()).mass()/GeV;
          if (mZ<66.0 || mZ>116.0) {
            candidate=false;
          }
          double abs_eta_0=fabs(all_els[i].momentum().pseudorapidity());
          double abs_eta_1=fabs(all_els[j].momentum().pseudorapidity());
          if (abs_eta_1<abs_eta_0) {
            double tmp=abs_eta_0;
            abs_eta_0=abs_eta_1;
            abs_eta_1=tmp;
          }
          if (abs_eta_0>1.0) {
            candidate=false;
          }
          if (!(abs_eta_1<1.0 || (abs_eta_1>1.2 && abs_eta_1<2.8))) {
            candidate=false;
          }
          if (candidate) {
            Z_candidates.push_back(make_pair(all_els[i], all_els[j]));
          }
        }
      }
      if (Z_candidates.size() != 1) {
        getLog() << Log::DEBUG << "Skipping event " << event.genEvent().event_number()
                 << " because no unique electron pair found " << endl;
        vetoEvent;
      }

      // Now build the jets on a FS without the electrons from the Z
      // (including their QED radiation)
      ParticleVector jetparts;
      foreach (const Particle& p, fs.particles()) {
        bool copy = true;
        if (p.pdgId() == PHOTON) {
          FourMomentum p_e0 = Z_candidates[0].first.momentum();
          FourMomentum p_e1 = Z_candidates[0].second.momentum();
          FourMomentum p_P = p.momentum();
          if (deltaR(p_e0.pseudorapidity(), p_e0.azimuthalAngle(),
                     p_P.pseudorapidity(), p_P.azimuthalAngle()) < 0.2) {
            copy = false;
          }
          if (deltaR(p_e1.pseudorapidity(), p_e1.azimuthalAngle(),
                     p_P.pseudorapidity(), p_P.azimuthalAngle()) < 0.2) {
            copy = false;
          }
        } else {
          if (p.genParticle().barcode()==Z_candidates[0].first.genParticle().barcode()) {
            copy = false;
          }
          if (p.genParticle().barcode()==Z_candidates[0].second.genParticle().barcode()) {
            copy = false;
          }
        }
        if (copy) jetparts.push_back(p);
      }
      /// @todo Allow proj creation w/o FS as ctor arg, so that calc can be used more easily.
      FastJets jetpro(fs, FastJets::CDFMIDPOINT, 0.7);
      jetpro.calc(jetparts);

      // Take jets with pt > 30, |eta| < 2.1:
      /// @todo Make this neater, using the JetAlg interface and the built-in sorting
      const Jets& jets = jetpro.jets();
      Jets jets_cut;
      foreach (const Jet& j, jets) {
        if (j.momentum().pT()/GeV > 30.0 && fabs(j.momentum().pseudorapidity()) < 2.1) {
          jets_cut.push_back(j);
        }
      }
      getLog() << Log::DEBUG << "Num jets above 30 GeV = " << jets_cut.size() << endl;

      // Return if there are no jets:
      if (jets_cut.empty()) {
        getLog() << Log::DEBUG << "No jets pass cuts " << endl;
        vetoEvent;
      }

      // Sort by pT:
      sort(jets_cut.begin(), jets_cut.end(), cmpJetsByPt);

      // cut on Delta R between jet and electrons
      foreach (const Jet& j, jets_cut) {
        Particle el = Z_candidates[0].first;
        if (deltaR(el.momentum().pseudorapidity(), el.momentum().azimuthalAngle(),
                   j.momentum().pseudorapidity(), j.momentum().azimuthalAngle()) < 0.7) {
          vetoEvent;
        }
        el = Z_candidates[0].second;
        if (deltaR(el.momentum().pseudorapidity(), el.momentum().azimuthalAngle(),
                   j.momentum().pseudorapidity(), j.momentum().azimuthalAngle()) < 0.7) {
          vetoEvent;
        }
      }

      for (size_t njet=1; njet<=jets_cut.size(); ++njet) {
        _h_jet_multiplicity->fill(njet, weight);
      }
      foreach (const Jet& j, jets_cut) {
        if (jets_cut.size()>0) {
          _h_jet_pT_cross_section_incl_1jet->fill(j.momentum().pT(), weight);
        }
        if (jets_cut.size()>1) {
          _h_jet_pT_cross_section_incl_2jet->fill(j.momentum().pT(), weight);
        }
      }
    }


    /// Rescale histos
    void finalize() {
      const double invlumi = crossSection()/femtobarn/sumOfWeights();
      scale(_h_jet_multiplicity, invlumi);
      scale(_h_jet_pT_cross_section_incl_1jet, invlumi);
      scale(_h_jet_pT_cross_section_incl_2jet, invlumi);
    }

    //@}

  private:

    /// @name Histograms
    //@{
    Histo1DPtr _h_jet_multiplicity;
    Histo1DPtr _h_jet_pT_cross_section_incl_1jet;
    Histo1DPtr _h_jet_pT_cross_section_incl_2jet;
    //@}

  };


  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CDF_2008_S7540469> plugin_CDF_2008_S7540469;

}
