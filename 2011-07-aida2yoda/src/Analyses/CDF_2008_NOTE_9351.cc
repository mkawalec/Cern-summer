// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/ChargedLeptons.hh"

namespace Rivet {


  /// @brief CDF Run II underlying event in Drell-Yan
  /// @author Hendrik Hoeth
  ///
  /// Measurement of the underlying event in Drell-Yan
  /// \f$ Z/\gamma^* \to e^+ e^- \f$ and
  /// \f$ Z/\gamma^* \to \mu^+ \mu^- \f$ events. The reconstructed
  /// Z defines the \f$ \phi \f$ orientation. A Z mass window cut is applied.
  ///
  /* @par Run conditions
   *
   * @arg \f$ \sqrt{s} = \f$ 1960 GeV
   * @arg produce Drell-Yan events
   * @arg Set particles with c*tau > 10 mm stable
   * @arg Z decay mode: Z -> e+e- and Z -> mu+mu-
   * @arg gamma decay mode: gamma -> e+e- and gamma -> mu+mu-
   * @arg minimum invariant mass of the fermion pair coming from the Z/gamma: 70 GeV
   *
   */
  class CDF_2008_NOTE_9351 : public Analysis {
  public:

    /// Constructor
    CDF_2008_NOTE_9351() : Analysis("CDF_2008_NOTE_9351")
    {
      setBeams(PROTON, ANTIPROTON);
    }


    /// @name Analysis methods
    //@{

    void init() {
      // Set up projections
      const ChargedFinalState cfs(-1.0, 1.0, 0.5*GeV);
      const ChargedFinalState clfs(-1.0, 1.0, 20*GeV);
      addProjection(cfs, "FS");
      addProjection(ChargedLeptons(clfs), "CL");

      // Book histograms
      _hist_tnchg      = bookProfile1D( 1, 1, 1);
      _hist_pnchg      = bookProfile1D( 2, 1, 1);
      _hist_pmaxnchg   = bookProfile1D( 3, 1, 1);
      _hist_pminnchg   = bookProfile1D( 4, 1, 1);
      _hist_pdifnchg   = bookProfile1D( 5, 1, 1);
      _hist_anchg      = bookProfile1D( 6, 1, 1);

      _hist_tcptsum    = bookProfile1D( 7, 1, 1);
      _hist_pcptsum    = bookProfile1D( 8, 1, 1);
      _hist_pmaxcptsum = bookProfile1D( 9, 1, 1);
      _hist_pmincptsum = bookProfile1D(10, 1, 1);
      _hist_pdifcptsum = bookProfile1D(11, 1, 1);
      _hist_acptsum    = bookProfile1D(12, 1, 1);

      _hist_tcptave    = bookProfile1D(13, 1, 1);
      _hist_pcptave    = bookProfile1D(14, 1, 1);
      _hist_acptave    = bookProfile1D(15, 1, 1);

      _hist_tcptmax    = bookProfile1D(16, 1, 1);
      _hist_pcptmax    = bookProfile1D(17, 1, 1);
      _hist_acptmax    = bookProfile1D(18, 1, 1);

      _hist_zptvsnchg  = bookProfile1D(19, 1, 1);
      _hist_cptavevsnchg = bookProfile1D(20, 1, 1);
      _hist_cptavevsnchgsmallzpt = bookProfile1D(21, 1, 1);
    }


    /// Do the analysis
    void analyze(const Event& e) {

      const FinalState& fs = applyProjection<FinalState>(e, "FS");
      const size_t numParticles = fs.particles().size();

      // Even if we only generate hadronic events, we still need a cut on numCharged >= 2.
      if (numParticles < 1) {
        getLog() << Log::DEBUG << "Failed multiplicity cut" << endl;
        vetoEvent;
      }

      // Get the event weight
      const double weight = e.weight();

      // Get the leptons
      const ParticleVector& leptons = applyProjection<ChargedLeptons>(e, "CL").chargedLeptons();

      // We want exactly two leptons of the same flavour.
      getLog() << Log::DEBUG << "lepton multiplicity = " << leptons.size() << endl;
      if (leptons.size() != 2 || leptons[0].pdgId() != -leptons[1].pdgId() ) vetoEvent;

      // Lepton pT > 20 GeV
      if (leptons[0].momentum().pT()/GeV <= 20 || leptons[1].momentum().pT()/GeV <= 20) vetoEvent;

      // Lepton pair should have an invariant mass between 70 and 110 and |eta| < 6
      const FourMomentum dilepton = leptons[0].momentum() + leptons[1].momentum();
      if (!inRange(dilepton.mass()/GeV, 70., 110.) || fabs(dilepton.eta()) >= 6) vetoEvent;
      getLog() << Log::DEBUG << "Dilepton mass = " << mass(dilepton)/GeV << " GeV" << endl;
      getLog() << Log::DEBUG << "Dilepton pT   = " << pT(dilepton)/GeV << " GeV" << endl;

      // Calculate the observables
      size_t   numToward(0),     numAway(0);
      long int numTrans1(0),     numTrans2(0);
      double ptSumToward(0.0), ptSumTrans1(0.0), ptSumTrans2(0.0), ptSumAway(0.0);
      double ptMaxToward(0.0), ptMaxTrans1(0.0), ptMaxTrans2(0.0), ptMaxAway(0.0);
      const double phiZ = azimuthalAngle(dilepton);
      const double pTZ  = pT(dilepton);
      /// @todo Replace with foreach
      for (ParticleVector::const_iterator p = fs.particles().begin(); p != fs.particles().end(); ++p) {
        // Don't use the leptons
        /// @todo Replace with PID::isLepton
        if (abs(p->pdgId()) < 20) continue;

        const double dPhi = deltaPhi(p->momentum().phi(), phiZ);
        const double pT = p->momentum().pT();
        double rotatedphi = p->momentum().phi() - phiZ;
        while (rotatedphi < 0) rotatedphi += 2*PI;

        if (dPhi < PI/3.0) {
          ptSumToward += pT;
          ++numToward;
          if (pT > ptMaxToward)
            ptMaxToward = pT;
        } else if (dPhi < 2*PI/3.0) {
          if (rotatedphi <= PI) {
            ptSumTrans1 += pT;
            ++numTrans1;
            if (pT > ptMaxTrans1)
              ptMaxTrans1 = pT;
          }
          else {
            ptSumTrans2 += pT;
            ++numTrans2;
            if (pT > ptMaxTrans2)
              ptMaxTrans2 = pT;
          }
        } else {
          ptSumAway += pT;
          ++numAway;
          if (pT > ptMaxAway)
            ptMaxAway = pT;
        }
        // We need to subtract the two leptons from the number of particles to get the correct multiplicity
        _hist_cptavevsnchg->fill(numParticles-2, pT, weight);
        if (pTZ < 10)
          _hist_cptavevsnchgsmallzpt->fill(numParticles-2, pT, weight);
      }

      // Fill the histograms
      _hist_tnchg->fill(pTZ, numToward/(4*PI/3), weight);
      _hist_pnchg->fill(pTZ, (numTrans1+numTrans2)/(4*PI/3), weight);
      _hist_pmaxnchg->fill(pTZ, (numTrans1>numTrans2 ? numTrans1 : numTrans2)/(2*PI/3), weight);
      _hist_pminnchg->fill(pTZ, (numTrans1<numTrans2 ? numTrans1 : numTrans2)/(2*PI/3), weight);
      _hist_pdifnchg->fill(pTZ, abs(numTrans1-numTrans2)/(2*PI/3), weight);
      _hist_anchg->fill(pTZ, numAway/(4*PI/3), weight);

      _hist_tcptsum->fill(pTZ, ptSumToward/(4*PI/3), weight);
      _hist_pcptsum->fill(pTZ, (ptSumTrans1+ptSumTrans2)/(4*PI/3), weight);
      _hist_pmaxcptsum->fill(pTZ, (ptSumTrans1>ptSumTrans2 ? ptSumTrans1 : ptSumTrans2)/(2*PI/3), weight);
      _hist_pmincptsum->fill(pTZ, (ptSumTrans1<ptSumTrans2 ? ptSumTrans1 : ptSumTrans2)/(2*PI/3), weight);
      _hist_pdifcptsum->fill(pTZ, fabs(ptSumTrans1-ptSumTrans2)/(2*PI/3), weight);
      _hist_acptsum->fill(pTZ, ptSumAway/(4*PI/3), weight);

      if (numToward > 0) {
        _hist_tcptave->fill(pTZ, ptSumToward/numToward, weight);
        _hist_tcptmax->fill(pTZ, ptMaxToward, weight);
      }
      if ((numTrans1+numTrans2) > 0) {
        _hist_pcptave->fill(pTZ, (ptSumTrans1+ptSumTrans2)/(numTrans1+numTrans2), weight);
        _hist_pcptmax->fill(pTZ, (ptMaxTrans1 > ptMaxTrans2 ? ptMaxTrans1 : ptMaxTrans2), weight);
      }
      if (numAway > 0) {
        _hist_acptave->fill(pTZ, ptSumAway/numAway, weight);
        _hist_acptmax->fill(pTZ, ptMaxAway, weight);
      }

      // We need to subtract the two leptons from the number of particles to get the correct multiplicity
      _hist_zptvsnchg->fill(numParticles-2, pTZ, weight);
    }


    void finalize() {
      //
    }

    //@}

  private:

    AIDA::IProfile1D *_hist_tnchg;
    AIDA::IProfile1D *_hist_pnchg;
    AIDA::IProfile1D *_hist_pmaxnchg;
    AIDA::IProfile1D *_hist_pminnchg;
    AIDA::IProfile1D *_hist_pdifnchg;
    AIDA::IProfile1D *_hist_anchg;
    AIDA::IProfile1D *_hist_tcptsum;
    AIDA::IProfile1D *_hist_pcptsum;
    AIDA::IProfile1D *_hist_pmaxcptsum;
    AIDA::IProfile1D *_hist_pmincptsum;
    AIDA::IProfile1D *_hist_pdifcptsum;
    AIDA::IProfile1D *_hist_acptsum;
    AIDA::IProfile1D *_hist_tcptave;
    AIDA::IProfile1D *_hist_pcptave;
    AIDA::IProfile1D *_hist_acptave;
    AIDA::IProfile1D *_hist_tcptmax;
    AIDA::IProfile1D *_hist_pcptmax;
    AIDA::IProfile1D *_hist_acptmax;
    AIDA::IProfile1D *_hist_zptvsnchg;
    AIDA::IProfile1D *_hist_cptavevsnchg;
    AIDA::IProfile1D *_hist_cptavevsnchgsmallzpt;

  };


  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CDF_2008_NOTE_9351> plugin_CDF_2008_NOTE_9351;

}
