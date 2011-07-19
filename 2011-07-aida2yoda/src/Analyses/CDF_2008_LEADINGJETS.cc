// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/FastJets.hh"

namespace Rivet {


  /// @brief CDF Run II underlying event in leading jet events
  /// @author Hendrik Hoeth
  ///
  /// Rick Field's measurement of the underlying event in "leading jet" events.
  /// The leading jet (CDF midpoint \f$ R = 0.7 \f$) must be within \f$|\eta| < 2 \f$
  /// and defines the "toward" phi direction. Particles are selected in
  /// \f$ |\eta| < 1 \f$. For the \f$ p_\perp \f$-related observables there
  /// is a \f$ p_\perp > 0.5 \f$ GeV cut. For \f$ \sum E_\perp \f$ there is no
  /// \f$ p_\perp \f$ cut.
  ///
  /* @par Run conditions
   *
   * @arg \f$ \sqrt{s} = \f$ 1960 GeV
   * @arg Run with generic QCD events.
   * @arg Set particles with c*tau > 10 mm stable
   * @arg Several \f$ p_\perp^\text{min} \f$ cutoffs are probably required to fill the profile histograms:
   *   @arg \f$ p_\perp^\text{min} = \f$ 0 (min bias), 10, 20, 50, 100, 150 GeV
   *   @arg The corresponding merging points are at \f$ p_T = \f$ 0, 30, 50, 80, 130, 180 GeV
   *
   */
  class CDF_2008_LEADINGJETS : public Analysis {
  public:

    /// Constructor
    CDF_2008_LEADINGJETS()
      : Analysis("CDF_2008_LEADINGJETS")
    {
      setBeams(PROTON, ANTIPROTON);
    }


    /// @name Analysis methods
    //@{

    void init() {
      // Final state for the jet finding
      const FinalState fsj(-4.0, 4.0, 0.0*GeV);
      addProjection(fsj, "FSJ");
      addProjection(FastJets(fsj, FastJets::CDFMIDPOINT, 0.7), "MidpointJets");

      // Final state for the sum(ET) distributions
      const FinalState fs(-1.0, 1.0, 0.0*GeV);
      addProjection(fs, "FS");

      // Charged final state for the distributions
      const ChargedFinalState cfs(-1.0, 1.0, 0.5*GeV);
      addProjection(cfs, "CFS");

      // Book histograms
      _hist_pnchg      = bookProfile1D( 1, 1, 1);
      _hist_pmaxnchg   = bookProfile1D( 2, 1, 1);
      _hist_pminnchg   = bookProfile1D( 3, 1, 1);
      _hist_pdifnchg   = bookProfile1D( 4, 1, 1);
      _hist_pcptsum    = bookProfile1D( 5, 1, 1);
      _hist_pmaxcptsum = bookProfile1D( 6, 1, 1);
      _hist_pmincptsum = bookProfile1D( 7, 1, 1);
      _hist_pdifcptsum = bookProfile1D( 8, 1, 1);
      _hist_pcptave    = bookProfile1D( 9, 1, 1);
      //_hist_onchg   = bookProfile1D( 1, 1, 1, "Overall number of charged particles");
      //_hist_ocptsum = bookProfile1D( 2, 1, 1, "Overall charged $p_\\perp$ sum");
      //_hist_oetsum  = bookProfile1D( 3, 1, 1, "Overall $E_\\perp$ sum");
    }


    // Do the analysis
    void analyze(const Event& e) {
      /// @todo Implement Run II min bias trigger cf. CDF_2009?

      const FinalState& fsj = applyProjection<FinalState>(e, "FSJ");
      if (fsj.particles().size() < 1) {
        getLog() << Log::DEBUG << "Failed multiplicity cut" << endl;
        vetoEvent;
      }

      const Jets& jets = applyProjection<FastJets>(e, "MidpointJets").jetsByPt();
      getLog() << Log::DEBUG << "Jet multiplicity = " << jets.size() << endl;

      // We require the leading jet to be within |eta|<2
      if (jets.size() < 1 || fabs(jets[0].momentum().eta()) >= 2) {
        getLog() << Log::DEBUG << "Failed leading jet cut" << endl;
        vetoEvent;
      }

      const double jetphi = jets[0].momentum().phi();
      const double jeteta = jets[0].momentum().eta();
      const double jetpT  = jets[0].momentum().pT();
      getLog() << Log::DEBUG << "Leading jet: pT = " << jetpT
               << ", eta = " << jeteta << ", phi = " << jetphi << endl;

      // Get the event weight
      const double weight = e.weight();

      // Get the final states to work with for filling the distributions
      const FinalState& cfs = applyProjection<ChargedFinalState>(e, "CFS");

      size_t numOverall(0),     numToward(0),      numAway(0)  ;
      long int    numTrans1(0),     numTrans2(0);
      double ptSumOverall(0.0), ptSumToward(0.0), ptSumTrans1(0.0), ptSumTrans2(0.0), ptSumAway(0.0);
      //double EtSumOverall(0.0), EtSumToward(0.0), EtSumTrans1(0.0), EtSumTrans2(0.0), EtSumAway(0.0);
      double ptMaxOverall(0.0), ptMaxToward(0.0), ptMaxTrans1(0.0), ptMaxTrans2(0.0), ptMaxAway(0.0);

      // Calculate all the charged stuff
      foreach (const Particle& p, cfs.particles()) {
        const double dPhi = deltaPhi(p.momentum().phi(), jetphi);
        const double pT = p.momentum().pT();
        const double phi = p.momentum().phi();
        double rotatedphi = phi - jetphi;
        while (rotatedphi < 0) rotatedphi += 2*PI;

        ptSumOverall += pT;
        ++numOverall;
        if (pT > ptMaxOverall) {
          ptMaxOverall = pT;
        }

        if (dPhi < PI/3.0) {
          ptSumToward += pT;
          ++numToward;
          if (pT > ptMaxToward) ptMaxToward = pT;
        }
        else if (dPhi < 2*PI/3.0) {
          if (rotatedphi <= PI) {
            ptSumTrans1 += pT;
            ++numTrans1;
            if (pT > ptMaxTrans1) ptMaxTrans1 = pT;
          } else {
            ptSumTrans2 += pT;
            ++numTrans2;
            if (pT > ptMaxTrans2) ptMaxTrans2 = pT;
          }
        }
        else {
          ptSumAway += pT;
          ++numAway;
          if (pT > ptMaxAway) ptMaxAway = pT;
        }
      } // end charged particle loop


      #if 0
      /// @todo Enable this part when we have the numbers from Rick Field

      // And now the same business for all particles (including neutrals)
      foreach (const Particle& p, fs.particles()) {
        const double dPhi = deltaPhi(p.momentum().phi(), jetphi);
        const double ET = p.momentum().Et();
        const double phi = p.momentum().phi();
        double rotatedphi = phi - jetphi;
        while (rotatedphi < 0) rotatedphi += 2*PI;

        EtSumOverall += ET;

        if (dPhi < PI/3.0) {
          EtSumToward += ET;
        }
        else if (dPhi < 2*PI/3.0) {
          if (rotatedphi <= PI) {
            EtSumTrans1 += ET;
          }
          else {
            EtSumTrans2 += ET;
          }
        }
        else {
          EtSumAway += ET;
        }
      } // end all particle loop
      #endif


      // Fill the histograms
      //_hist_tnchg->fill(jetpT/GeV, numToward/(4*PI/3), weight);
      _hist_pnchg->fill(jetpT/GeV, (numTrans1+numTrans2)/(4*PI/3), weight);
      _hist_pmaxnchg->fill(jetpT/GeV, (numTrans1>numTrans2 ? numTrans1 : numTrans2)/(2*PI/3), weight);
      _hist_pminnchg->fill(jetpT/GeV, (numTrans1<numTrans2 ? numTrans1 : numTrans2)/(2*PI/3), weight);
      _hist_pdifnchg->fill(jetpT/GeV, abs(numTrans1-numTrans2)/(2*PI/3), weight);
      //_hist_anchg->fill(jetpT/GeV, numAway/(4*PI/3), weight);

      //_hist_tcptsum->fill(jetpT/GeV, ptSumToward/GeV/(4*PI/3), weight);
      _hist_pcptsum->fill(jetpT/GeV, (ptSumTrans1+ptSumTrans2)/GeV/(4*PI/3), weight);
      _hist_pmaxcptsum->fill(jetpT/GeV, (ptSumTrans1>ptSumTrans2 ? ptSumTrans1 : ptSumTrans2)/GeV/(2*PI/3), weight);
      _hist_pmincptsum->fill(jetpT/GeV, (ptSumTrans1<ptSumTrans2 ? ptSumTrans1 : ptSumTrans2)/GeV/(2*PI/3), weight);
      _hist_pdifcptsum->fill(jetpT/GeV, fabs(ptSumTrans1-ptSumTrans2)/GeV/(2*PI/3), weight);
      //_hist_acptsum->fill(jetpT/GeV, ptSumAway/GeV/(4*PI/3), weight);

      //if (numToward > 0) {
      //  _hist_tcptave->fill(jetpT/GeV, ptSumToward/GeV/numToward, weight);
      //  _hist_tcptmax->fill(jetpT/GeV, ptMaxToward/GeV, weight);
      //}
      if ((numTrans1+numTrans2) > 0) {
        _hist_pcptave->fill(jetpT/GeV, (ptSumTrans1+ptSumTrans2)/GeV/(numTrans1+numTrans2), weight);
        //_hist_pcptmax->fill(jetpT/GeV, (ptMaxTrans1 > ptMaxTrans2 ? ptMaxTrans1 : ptMaxTrans2)/GeV, weight);
      }
      //if (numAway > 0) {
      //  _hist_acptave->fill(jetpT/GeV, ptSumAway/GeV/numAway, weight);
      //  _hist_acptmax->fill(jetpT/GeV, ptMaxAway/GeV, weight);
      //}
    }


    void finalize() {
      //
    }

    //@}


  private:

    AIDA::IProfile1D *_hist_pnchg;
    AIDA::IProfile1D *_hist_pmaxnchg;
    AIDA::IProfile1D *_hist_pminnchg;
    AIDA::IProfile1D *_hist_pdifnchg;
    AIDA::IProfile1D *_hist_pcptsum;
    AIDA::IProfile1D *_hist_pmaxcptsum;
    AIDA::IProfile1D *_hist_pmincptsum;
    AIDA::IProfile1D *_hist_pdifcptsum;
    AIDA::IProfile1D *_hist_pcptave;

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CDF_2008_LEADINGJETS> plugin_CDF_2008_LEADINGJETS;

}
