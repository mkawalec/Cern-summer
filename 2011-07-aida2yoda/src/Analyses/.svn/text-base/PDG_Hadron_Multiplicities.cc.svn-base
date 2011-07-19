// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/UnstableFinalState.hh"

namespace Rivet {


  /// @brief Implementation of PDG hadron multiplicities
  /// @author Hendrik Hoeth
  class PDG_HADRON_MULTIPLICITIES : public Analysis {
  public:

    /// Constructor
    PDG_HADRON_MULTIPLICITIES() : Analysis("PDG_HADRON_MULTIPLICITIES")
    {
      setBeams(ELECTRON, POSITRON);
    }


    /// @name Analysis methods
    //@{

    void analyze(const Event& e) {
      // First, veto on leptonic events by requiring at least 4 charged FS particles
      const FinalState& fs = applyProjection<FinalState>(e, "FS");
      const size_t numParticles = fs.particles().size();

      // Even if we only generate hadronic events, we still need a cut on numCharged >= 2.
      if (numParticles < 2) {
        MSG_DEBUG("Failed leptonic event cut");
        vetoEvent;
      }
      MSG_DEBUG("Passed leptonic event cut");

      // Get event weight for histo filling
      const double weight = e.weight();

      MSG_DEBUG("sqrt(s) = " << sqrtS()/GeV << " GeV");

      // Final state of unstable particles to get particle spectra
      const UnstableFinalState& ufs = applyProjection<UnstableFinalState>(e, "UFS");

      if (sqrtS()/GeV >= 9.5 && sqrtS()/GeV <= 10.5) {
        foreach (const Particle& p, ufs.particles()) {
          const PdgId id = abs(p.pdgId());
          switch (id) {
             case 211:
                _histMeanMultiPiPlus->fill(_histMeanMultiPiPlus->binMean(0), weight);
                break;
             case 111:
                _histMeanMultiPi0->fill(_histMeanMultiPi0->binMean(0), weight);
                break;
             case 321:
                _histMeanMultiKPlus->fill(_histMeanMultiKPlus->binMean(0), weight);
                break;
             case 130:
             case 310:
                _histMeanMultiK0->fill(_histMeanMultiK0->binMean(0), weight);
                break;
             case 221:
                _histMeanMultiEta->fill(_histMeanMultiEta->binMean(0), weight);
                break;
             case 331:
                _histMeanMultiEtaPrime->fill(_histMeanMultiEtaPrime->binMean(0), weight);
                break;
             case 411:
                _histMeanMultiDPlus->fill(_histMeanMultiDPlus->binMean(0), weight);
                break;
             case 421:
                _histMeanMultiD0->fill(_histMeanMultiD0->binMean(0), weight);
                break;
             case 431:
                _histMeanMultiDPlus_s->fill(_histMeanMultiDPlus_s->binMean(0), weight);
                break;
             case 9010221:
                _histMeanMultiF0_980->fill(_histMeanMultiF0_980->binMean(0), weight);
                break;
             case 113:
                _histMeanMultiRho770_0->fill(_histMeanMultiRho770_0->binMean(0), weight);
                break;
             case 223:
                _histMeanMultiOmega782->fill(_histMeanMultiOmega782->binMean(0), weight);
                break;
             case 323:
                _histMeanMultiKStar892Plus->fill(_histMeanMultiKStar892Plus->binMean(0), weight);
                break;
             case 313:
                _histMeanMultiKStar892_0->fill(_histMeanMultiKStar892_0->binMean(0), weight);
                break;
             case 333:
                _histMeanMultiPhi1020->fill(_histMeanMultiPhi1020->binMean(0), weight);
                break;
             case 413:
                _histMeanMultiDStar2010Plus->fill(_histMeanMultiDStar2010Plus->binMean(0), weight);
                break;
             case 423:
                _histMeanMultiDStar2007_0->fill(_histMeanMultiDStar2007_0->binMean(0), weight);
                break;
             case 433:
                _histMeanMultiDStar_s2112Plus->fill(_histMeanMultiDStar_s2112Plus->binMean(0), weight);
                break;
             case 443:
                _histMeanMultiJPsi1S->fill(_histMeanMultiJPsi1S->binMean(0), weight);
                break;
             case 225:
                _histMeanMultiF2_1270->fill(_histMeanMultiF2_1270->binMean(0), weight);
                break;
             case 2212:
                _histMeanMultiP->fill(_histMeanMultiP->binMean(0), weight);
                break;
             case 3122:
                _histMeanMultiLambda->fill(_histMeanMultiLambda->binMean(0), weight);
                break;
             case 3212:
                _histMeanMultiSigma0->fill(_histMeanMultiSigma0->binMean(0), weight);
                break;
             case 3312:
                _histMeanMultiXiMinus->fill(_histMeanMultiXiMinus->binMean(0), weight);
                break;
             case 2224:
                _histMeanMultiDelta1232PlusPlus->fill(_histMeanMultiDelta1232PlusPlus->binMean(0), weight);
                break;
             case 3114:
                _histMeanMultiSigma1385Minus->fill(_histMeanMultiSigma1385Minus->binMean(0), weight);
                _histMeanMultiSigma1385PlusMinus->fill(_histMeanMultiSigma1385PlusMinus->binMean(0), weight);
                break;
             case 3224:
                _histMeanMultiSigma1385Plus->fill(_histMeanMultiSigma1385Plus->binMean(0), weight);
                _histMeanMultiSigma1385PlusMinus->fill(_histMeanMultiSigma1385PlusMinus->binMean(0), weight);
                break;
             case 3324:
                _histMeanMultiXi1530_0->fill(_histMeanMultiXi1530_0->binMean(0), weight);
                break;
             case 3334:
                _histMeanMultiOmegaMinus->fill(_histMeanMultiOmegaMinus->binMean(0), weight);
                break;
             case 4122:
                _histMeanMultiLambda_c_Plus->fill(_histMeanMultiLambda_c_Plus->binMean(0), weight);
                break;
             case 4222:
             case 4112:
                _histMeanMultiSigma_c_PlusPlus_0->fill(_histMeanMultiSigma_c_PlusPlus_0->binMean(0), weight);
                break;
             case 3124:
                _histMeanMultiLambda1520->fill(_histMeanMultiLambda1520->binMean(0), weight);
                break;
          }
        }
      }

      if (sqrtS()/GeV >= 29 && sqrtS()/GeV <= 35) {
        foreach (const Particle& p, ufs.particles()) {
          const PdgId id = abs(p.pdgId());
          switch (id) {
             case 211:
                _histMeanMultiPiPlus->fill(_histMeanMultiPiPlus->binMean(0), weight);
                break;
             case 111:
                _histMeanMultiPi0->fill(_histMeanMultiPi0->binMean(0), weight);
                break;
             case 321:
                _histMeanMultiKPlus->fill(_histMeanMultiKPlus->binMean(0), weight);
                break;
             case 130:
             case 310:
                _histMeanMultiK0->fill(_histMeanMultiK0->binMean(0), weight);
                break;
             case 221:
                _histMeanMultiEta->fill(_histMeanMultiEta->binMean(0), weight);
                break;
             case 331:
                _histMeanMultiEtaPrime->fill(_histMeanMultiEtaPrime->binMean(0), weight);
                break;
             case 411:
                _histMeanMultiDPlus->fill(_histMeanMultiDPlus->binMean(0), weight);
                break;
             case 421:
                _histMeanMultiD0->fill(_histMeanMultiD0->binMean(0), weight);
                break;
             case 431:
                _histMeanMultiDPlus_s->fill(_histMeanMultiDPlus_s->binMean(0), weight);
                break;
             case 9010221:
                _histMeanMultiF0_980->fill(_histMeanMultiF0_980->binMean(0), weight);
                break;
             case 113:
                _histMeanMultiRho770_0->fill(_histMeanMultiRho770_0->binMean(0), weight);
                break;
             case 323:
                _histMeanMultiKStar892Plus->fill(_histMeanMultiKStar892Plus->binMean(0), weight);
                break;
             case 313:
                _histMeanMultiKStar892_0->fill(_histMeanMultiKStar892_0->binMean(0), weight);
                break;
             case 333:
                _histMeanMultiPhi1020->fill(_histMeanMultiPhi1020->binMean(0), weight);
                break;
             case 413:
                _histMeanMultiDStar2010Plus->fill(_histMeanMultiDStar2010Plus->binMean(0), weight);
                break;
             case 423:
                _histMeanMultiDStar2007_0->fill(_histMeanMultiDStar2007_0->binMean(0), weight);
                break;
             case 225:
                _histMeanMultiF2_1270->fill(_histMeanMultiF2_1270->binMean(0), weight);
                break;
             case 325:
                _histMeanMultiK2Star1430Plus->fill(_histMeanMultiK2Star1430Plus->binMean(0), weight);
                break;
             case 315:
                _histMeanMultiK2Star1430_0->fill(_histMeanMultiK2Star1430_0->binMean(0), weight);
                break;
             case 2212:
                _histMeanMultiP->fill(_histMeanMultiP->binMean(0), weight);
                break;
             case 3122:
                _histMeanMultiLambda->fill(_histMeanMultiLambda->binMean(0), weight);
                break;
             case 3312:
                _histMeanMultiXiMinus->fill(_histMeanMultiXiMinus->binMean(0), weight);
                break;
             case 3114:
                _histMeanMultiSigma1385Minus->fill(_histMeanMultiSigma1385Minus->binMean(0), weight);
                _histMeanMultiSigma1385PlusMinus->fill(_histMeanMultiSigma1385PlusMinus->binMean(0), weight);
                break;
             case 3224:
                _histMeanMultiSigma1385Plus->fill(_histMeanMultiSigma1385Plus->binMean(0), weight);
                _histMeanMultiSigma1385PlusMinus->fill(_histMeanMultiSigma1385PlusMinus->binMean(0), weight);
                break;
             case 3334:
                _histMeanMultiOmegaMinus->fill(_histMeanMultiOmegaMinus->binMean(0), weight);
                break;
             case 4122:
                _histMeanMultiLambda_c_Plus->fill(_histMeanMultiLambda_c_Plus->binMean(0), weight);
                break;
          }
        }
      }

      if (sqrtS()/GeV >= 89.5 && sqrtS()/GeV <= 91.8) {
        foreach (const Particle& p, ufs.particles()) {
          const PdgId id = abs(p.pdgId());
          switch (id) {
             case 211:
                _histMeanMultiPiPlus->fill(_histMeanMultiPiPlus->binMean(0), weight);
                break;
             case 111:
                _histMeanMultiPi0->fill(_histMeanMultiPi0->binMean(0), weight);
                break;
             case 321:
                _histMeanMultiKPlus->fill(_histMeanMultiKPlus->binMean(0), weight);
                break;
             case 130:
             case 310:
                _histMeanMultiK0->fill(_histMeanMultiK0->binMean(0), weight);
                break;
             case 221:
                _histMeanMultiEta->fill(_histMeanMultiEta->binMean(0), weight);
                break;
             case 331:
                _histMeanMultiEtaPrime->fill(_histMeanMultiEtaPrime->binMean(0), weight);
                break;
             case 411:
                _histMeanMultiDPlus->fill(_histMeanMultiDPlus->binMean(0), weight);
                break;
             case 421:
                _histMeanMultiD0->fill(_histMeanMultiD0->binMean(0), weight);
                break;
             case 431:
                _histMeanMultiDPlus_s->fill(_histMeanMultiDPlus_s->binMean(0), weight);
                break;
             case 511:
                _histMeanMultiBPlus_B0_d->fill(_histMeanMultiBPlus_B0_d->binMean(0), weight);
                break;
             case 521:
                _histMeanMultiBPlus_B0_d->fill(_histMeanMultiBPlus_B0_d->binMean(0), weight);
                _histMeanMultiBPlus_u->fill(_histMeanMultiBPlus_u->binMean(0), weight);
                break;
             case 531:
                _histMeanMultiB0_s->fill(_histMeanMultiB0_s->binMean(0), weight);
                break;
             case 9010221:
                _histMeanMultiF0_980->fill(_histMeanMultiF0_980->binMean(0), weight);
                break;
             case 9000211:
                _histMeanMultiA0_980Plus->fill(_histMeanMultiA0_980Plus->binMean(0), weight);
                break;
             case 113:
                _histMeanMultiRho770_0->fill(_histMeanMultiRho770_0->binMean(0), weight);
                break;
             case 213:
                _histMeanMultiRho770Plus->fill(_histMeanMultiRho770Plus->binMean(0), weight);
                break;
             case 223:
                _histMeanMultiOmega782->fill(_histMeanMultiOmega782->binMean(0), weight);
                break;
             case 323:
                _histMeanMultiKStar892Plus->fill(_histMeanMultiKStar892Plus->binMean(0), weight);
                break;
             case 313:
                _histMeanMultiKStar892_0->fill(_histMeanMultiKStar892_0->binMean(0), weight);
                break;
             case 333:
                _histMeanMultiPhi1020->fill(_histMeanMultiPhi1020->binMean(0), weight);
                break;
             case 413:
                _histMeanMultiDStar2010Plus->fill(_histMeanMultiDStar2010Plus->binMean(0), weight);
                break;
             case 433:
                _histMeanMultiDStar_s2112Plus->fill(_histMeanMultiDStar_s2112Plus->binMean(0), weight);
                break;
             case 513:
             case 523:
             case 533:
                _histMeanMultiBStar->fill(_histMeanMultiBStar->binMean(0), weight);
                break;
             case 443:
                _histMeanMultiJPsi1S->fill(_histMeanMultiJPsi1S->binMean(0), weight);
                break;
             case 100443:
                _histMeanMultiPsi2S->fill(_histMeanMultiPsi2S->binMean(0), weight);
                break;
             case 553:
                _histMeanMultiUpsilon1S->fill(_histMeanMultiUpsilon1S->binMean(0), weight);
                break;
             case 20223:
                _histMeanMultiF1_1285->fill(_histMeanMultiF1_1285->binMean(0), weight);
                break;
             case 20333:
                _histMeanMultiF1_1420->fill(_histMeanMultiF1_1420->binMean(0), weight);
                break;
             case 445:
                _histMeanMultiChi_c1_3510->fill(_histMeanMultiChi_c1_3510->binMean(0), weight);
                break;
             case 225:
                _histMeanMultiF2_1270->fill(_histMeanMultiF2_1270->binMean(0), weight);
                break;
             case 335:
                _histMeanMultiF2Prime1525->fill(_histMeanMultiF2Prime1525->binMean(0), weight);
                break;
             case 315:
                _histMeanMultiK2Star1430_0->fill(_histMeanMultiK2Star1430_0->binMean(0), weight);
                break;
             case 515:
             case 525:
             case 535:
                _histMeanMultiBStarStar->fill(_histMeanMultiBStarStar->binMean(0), weight);
                break;
             case 10433:
             case 20433:
                _histMeanMultiDs1Plus->fill(_histMeanMultiDs1Plus->binMean(0), weight);
                break;
             case 435:
                _histMeanMultiDs2Plus->fill(_histMeanMultiDs2Plus->binMean(0), weight);
                break;
             case 2212:
                _histMeanMultiP->fill(_histMeanMultiP->binMean(0), weight);
                break;
             case 3122:
                _histMeanMultiLambda->fill(_histMeanMultiLambda->binMean(0), weight);
                break;
             case 3212:
                _histMeanMultiSigma0->fill(_histMeanMultiSigma0->binMean(0), weight);
                break;
             case 3112:
                _histMeanMultiSigmaMinus->fill(_histMeanMultiSigmaMinus->binMean(0), weight);
                _histMeanMultiSigmaPlusMinus->fill(_histMeanMultiSigmaPlusMinus->binMean(0), weight);
                break;
             case 3222:
                _histMeanMultiSigmaPlus->fill(_histMeanMultiSigmaPlus->binMean(0), weight);
                _histMeanMultiSigmaPlusMinus->fill(_histMeanMultiSigmaPlusMinus->binMean(0), weight);
                break;
             case 3312:
                _histMeanMultiXiMinus->fill(_histMeanMultiXiMinus->binMean(0), weight);
                break;
             case 2224:
                _histMeanMultiDelta1232PlusPlus->fill(_histMeanMultiDelta1232PlusPlus->binMean(0), weight);
                break;
             case 3114:
                _histMeanMultiSigma1385Minus->fill(_histMeanMultiSigma1385Minus->binMean(0), weight);
                _histMeanMultiSigma1385PlusMinus->fill(_histMeanMultiSigma1385PlusMinus->binMean(0), weight);
                break;
             case 3224:
                _histMeanMultiSigma1385Plus->fill(_histMeanMultiSigma1385Plus->binMean(0), weight);
                _histMeanMultiSigma1385PlusMinus->fill(_histMeanMultiSigma1385PlusMinus->binMean(0), weight);
                break;
             case 3324:
                _histMeanMultiXi1530_0->fill(_histMeanMultiXi1530_0->binMean(0), weight);
                break;
             case 3334:
                _histMeanMultiOmegaMinus->fill(_histMeanMultiOmegaMinus->binMean(0), weight);
                break;
             case 4122:
                _histMeanMultiLambda_c_Plus->fill(_histMeanMultiLambda_c_Plus->binMean(0), weight);
                break;
             case 5122:
                _histMeanMultiLambda_b_0->fill(_histMeanMultiLambda_b_0->binMean(0), weight);
                break;
             case 3124:
                _histMeanMultiLambda1520->fill(_histMeanMultiLambda1520->binMean(0), weight);
                break;
          }
        }
      }

      if (sqrtS()/GeV >= 130 && sqrtS()/GeV <= 200) {
        foreach (const Particle& p, ufs.particles()) {
          const PdgId id = abs(p.pdgId());
          switch (id) {
             case 211:
                _histMeanMultiPiPlus->fill(_histMeanMultiPiPlus->binMean(0), weight);
                break;
             case 321:
                _histMeanMultiKPlus->fill(_histMeanMultiKPlus->binMean(0), weight);
                break;
             case 130:
             case 310:
                _histMeanMultiK0->fill(_histMeanMultiK0->binMean(0), weight);
                break;
             case 2212:
                _histMeanMultiP->fill(_histMeanMultiP->binMean(0), weight);
                break;
             case 3122:
                _histMeanMultiLambda->fill(_histMeanMultiLambda->binMean(0), weight);
                break;
          }
        }
      }

    }



    void init() {
      addProjection(ChargedFinalState(), "FS");
      addProjection(UnstableFinalState(), "UFS");

      if (sqrtS()/GeV >= 9.5 && sqrtS()/GeV <= 10.5) {
        _histMeanMultiPiPlus             = bookHistogram1D( 1, 1, 1);
        _histMeanMultiPi0                = bookHistogram1D( 2, 1, 1);
        _histMeanMultiKPlus              = bookHistogram1D( 3, 1, 1);
        _histMeanMultiK0                 = bookHistogram1D( 4, 1, 1);
        _histMeanMultiEta                = bookHistogram1D( 5, 1, 1);
        _histMeanMultiEtaPrime           = bookHistogram1D( 6, 1, 1);
        _histMeanMultiDPlus              = bookHistogram1D( 7, 1, 1);
        _histMeanMultiD0                 = bookHistogram1D( 8, 1, 1);
        _histMeanMultiDPlus_s            = bookHistogram1D( 9, 1, 1);
        _histMeanMultiF0_980             = bookHistogram1D(13, 1, 1);
        _histMeanMultiRho770_0           = bookHistogram1D(15, 1, 1);
        _histMeanMultiOmega782           = bookHistogram1D(17, 1, 1);
        _histMeanMultiKStar892Plus       = bookHistogram1D(18, 1, 1);
        _histMeanMultiKStar892_0         = bookHistogram1D(19, 1, 1);
        _histMeanMultiPhi1020            = bookHistogram1D(20, 1, 1);
        _histMeanMultiDStar2010Plus      = bookHistogram1D(21, 1, 1);
        _histMeanMultiDStar2007_0        = bookHistogram1D(22, 1, 1);
        _histMeanMultiDStar_s2112Plus    = bookHistogram1D(23, 1, 1);
        _histMeanMultiJPsi1S             = bookHistogram1D(25, 1, 1);
        _histMeanMultiF2_1270            = bookHistogram1D(31, 1, 1);
        _histMeanMultiP                  = bookHistogram1D(38, 1, 1);
        _histMeanMultiLambda             = bookHistogram1D(39, 1, 1);
        _histMeanMultiSigma0             = bookHistogram1D(40, 1, 1);
        _histMeanMultiXiMinus            = bookHistogram1D(44, 1, 1);
        _histMeanMultiDelta1232PlusPlus  = bookHistogram1D(45, 1, 1);
        _histMeanMultiSigma1385Minus     = bookHistogram1D(46, 1, 1);
        _histMeanMultiSigma1385Plus      = bookHistogram1D(47, 1, 1);
        _histMeanMultiSigma1385PlusMinus = bookHistogram1D(48, 1, 1);
        _histMeanMultiXi1530_0           = bookHistogram1D(49, 1, 1);
        _histMeanMultiOmegaMinus         = bookHistogram1D(50, 1, 1);
        _histMeanMultiLambda_c_Plus      = bookHistogram1D(51, 1, 1);
        _histMeanMultiSigma_c_PlusPlus_0 = bookHistogram1D(53, 1, 1);
        _histMeanMultiLambda1520         = bookHistogram1D(54, 1, 1);
      }

      if (sqrtS()/GeV >= 29 && sqrtS()/GeV <= 35) {
        _histMeanMultiPiPlus             = bookHistogram1D( 1, 1, 2);
        _histMeanMultiPi0                = bookHistogram1D( 2, 1, 2);
        _histMeanMultiKPlus              = bookHistogram1D( 3, 1, 2);
        _histMeanMultiK0                 = bookHistogram1D( 4, 1, 2);
        _histMeanMultiEta                = bookHistogram1D( 5, 1, 2);
        _histMeanMultiEtaPrime           = bookHistogram1D( 6, 1, 2);
        _histMeanMultiDPlus              = bookHistogram1D( 7, 1, 2);
        _histMeanMultiD0                 = bookHistogram1D( 8, 1, 2);
        _histMeanMultiDPlus_s            = bookHistogram1D( 9, 1, 2);
        _histMeanMultiF0_980             = bookHistogram1D(13, 1, 2);
        _histMeanMultiRho770_0           = bookHistogram1D(15, 1, 2);
        _histMeanMultiKStar892Plus       = bookHistogram1D(18, 1, 2);
        _histMeanMultiKStar892_0         = bookHistogram1D(19, 1, 2);
        _histMeanMultiPhi1020            = bookHistogram1D(20, 1, 2);
        _histMeanMultiDStar2010Plus      = bookHistogram1D(21, 1, 2);
        _histMeanMultiDStar2007_0        = bookHistogram1D(22, 1, 2);
        _histMeanMultiF2_1270            = bookHistogram1D(31, 1, 2);
        _histMeanMultiK2Star1430Plus     = bookHistogram1D(33, 1, 1);
        _histMeanMultiK2Star1430_0       = bookHistogram1D(34, 1, 1);
        _histMeanMultiP                  = bookHistogram1D(38, 1, 2);
        _histMeanMultiLambda             = bookHistogram1D(39, 1, 2);
        _histMeanMultiXiMinus            = bookHistogram1D(44, 1, 2);
        _histMeanMultiSigma1385Minus     = bookHistogram1D(46, 1, 2);
        _histMeanMultiSigma1385Plus      = bookHistogram1D(47, 1, 2);
        _histMeanMultiSigma1385PlusMinus = bookHistogram1D(48, 1, 2);
        _histMeanMultiOmegaMinus         = bookHistogram1D(50, 1, 2);
        _histMeanMultiLambda_c_Plus      = bookHistogram1D(51, 1, 2);
      }

      if (sqrtS()/GeV >= 89.5 && sqrtS()/GeV <= 91.8) {
        _histMeanMultiPiPlus             = bookHistogram1D( 1, 1, 3);
        _histMeanMultiPi0                = bookHistogram1D( 2, 1, 3);
        _histMeanMultiKPlus              = bookHistogram1D( 3, 1, 3);
        _histMeanMultiK0                 = bookHistogram1D( 4, 1, 3);
        _histMeanMultiEta                = bookHistogram1D( 5, 1, 3);
        _histMeanMultiEtaPrime           = bookHistogram1D( 6, 1, 3);
        _histMeanMultiDPlus              = bookHistogram1D( 7, 1, 3);
        _histMeanMultiD0                 = bookHistogram1D( 8, 1, 3);
        _histMeanMultiDPlus_s            = bookHistogram1D( 9, 1, 3);
        _histMeanMultiBPlus_B0_d         = bookHistogram1D(10, 1, 1);
        _histMeanMultiBPlus_u            = bookHistogram1D(11, 1, 1);
        _histMeanMultiB0_s               = bookHistogram1D(12, 1, 1);
        _histMeanMultiF0_980             = bookHistogram1D(13, 1, 3);
        _histMeanMultiA0_980Plus         = bookHistogram1D(14, 1, 1);
        _histMeanMultiRho770_0           = bookHistogram1D(15, 1, 3);
        _histMeanMultiRho770Plus         = bookHistogram1D(16, 1, 1);
        _histMeanMultiOmega782           = bookHistogram1D(17, 1, 2);
        _histMeanMultiKStar892Plus       = bookHistogram1D(18, 1, 3);
        _histMeanMultiKStar892_0         = bookHistogram1D(19, 1, 3);
        _histMeanMultiPhi1020            = bookHistogram1D(20, 1, 3);
        _histMeanMultiDStar2010Plus      = bookHistogram1D(21, 1, 3);
        _histMeanMultiDStar_s2112Plus    = bookHistogram1D(23, 1, 2);
        _histMeanMultiBStar              = bookHistogram1D(24, 1, 1);
        _histMeanMultiJPsi1S             = bookHistogram1D(25, 1, 2);
        _histMeanMultiPsi2S              = bookHistogram1D(26, 1, 1);
        _histMeanMultiUpsilon1S          = bookHistogram1D(27, 1, 1);
        _histMeanMultiF1_1285            = bookHistogram1D(28, 1, 1);
        _histMeanMultiF1_1420            = bookHistogram1D(29, 1, 1);
        _histMeanMultiChi_c1_3510        = bookHistogram1D(30, 1, 1);
        _histMeanMultiF2_1270            = bookHistogram1D(31, 1, 3);
        _histMeanMultiF2Prime1525        = bookHistogram1D(32, 1, 1);
        _histMeanMultiK2Star1430_0       = bookHistogram1D(34, 1, 2);
        _histMeanMultiBStarStar          = bookHistogram1D(35, 1, 1);
        _histMeanMultiDs1Plus            = bookHistogram1D(36, 1, 1);
        _histMeanMultiDs2Plus            = bookHistogram1D(37, 1, 1);
        _histMeanMultiP                  = bookHistogram1D(38, 1, 3);
        _histMeanMultiLambda             = bookHistogram1D(39, 1, 3);
        _histMeanMultiSigma0             = bookHistogram1D(40, 1, 2);
        _histMeanMultiSigmaMinus         = bookHistogram1D(41, 1, 1);
        _histMeanMultiSigmaPlus          = bookHistogram1D(42, 1, 1);
        _histMeanMultiSigmaPlusMinus     = bookHistogram1D(43, 1, 1);
        _histMeanMultiXiMinus            = bookHistogram1D(44, 1, 3);
        _histMeanMultiDelta1232PlusPlus  = bookHistogram1D(45, 1, 2);
        _histMeanMultiSigma1385Minus     = bookHistogram1D(46, 1, 3);
        _histMeanMultiSigma1385Plus      = bookHistogram1D(47, 1, 3);
        _histMeanMultiSigma1385PlusMinus = bookHistogram1D(48, 1, 3);
        _histMeanMultiXi1530_0           = bookHistogram1D(49, 1, 2);
        _histMeanMultiOmegaMinus         = bookHistogram1D(50, 1, 3);
        _histMeanMultiLambda_c_Plus      = bookHistogram1D(51, 1, 3);
        _histMeanMultiLambda_b_0         = bookHistogram1D(52, 1, 1);
        _histMeanMultiLambda1520         = bookHistogram1D(54, 1, 2);
      }

      if (sqrtS()/GeV >= 130 && sqrtS()/GeV <= 200) {
        _histMeanMultiPiPlus            = bookHistogram1D( 1, 1, 4);
        _histMeanMultiKPlus             = bookHistogram1D( 3, 1, 4);
        _histMeanMultiK0                = bookHistogram1D( 4, 1, 4);
        _histMeanMultiP                 = bookHistogram1D(38, 1, 4);
        _histMeanMultiLambda            = bookHistogram1D(39, 1, 4);
      }
    }



    // Finalize
    void finalize() {
      if (sqrtS()/GeV >= 9.5 && sqrtS()/GeV <= 10.5) {
        scale(_histMeanMultiPiPlus            , 1.0/sumOfWeights());
        scale(_histMeanMultiPi0               , 1.0/sumOfWeights());
        scale(_histMeanMultiKPlus             , 1.0/sumOfWeights());
        scale(_histMeanMultiK0                , 1.0/sumOfWeights());
        scale(_histMeanMultiEta               , 1.0/sumOfWeights());
        scale(_histMeanMultiEtaPrime          , 1.0/sumOfWeights());
        scale(_histMeanMultiDPlus             , 1.0/sumOfWeights());
        scale(_histMeanMultiD0                , 1.0/sumOfWeights());
        scale(_histMeanMultiDPlus_s           , 1.0/sumOfWeights());
        scale(_histMeanMultiF0_980            , 1.0/sumOfWeights());
        scale(_histMeanMultiRho770_0          , 1.0/sumOfWeights());
        scale(_histMeanMultiOmega782          , 1.0/sumOfWeights());
        scale(_histMeanMultiKStar892Plus      , 1.0/sumOfWeights());
        scale(_histMeanMultiKStar892_0        , 1.0/sumOfWeights());
        scale(_histMeanMultiPhi1020           , 1.0/sumOfWeights());
        scale(_histMeanMultiDStar2010Plus     , 1.0/sumOfWeights());
        scale(_histMeanMultiDStar2007_0       , 1.0/sumOfWeights());
        scale(_histMeanMultiDStar_s2112Plus   , 1.0/sumOfWeights());
        scale(_histMeanMultiJPsi1S            , 1.0/sumOfWeights());
        scale(_histMeanMultiF2_1270           , 1.0/sumOfWeights());
        scale(_histMeanMultiP                 , 1.0/sumOfWeights());
        scale(_histMeanMultiLambda            , 1.0/sumOfWeights());
        scale(_histMeanMultiSigma0            , 1.0/sumOfWeights());
        scale(_histMeanMultiXiMinus           , 1.0/sumOfWeights());
        scale(_histMeanMultiDelta1232PlusPlus , 1.0/sumOfWeights());
        scale(_histMeanMultiSigma1385Minus    , 1.0/sumOfWeights());
        scale(_histMeanMultiSigma1385Plus     , 1.0/sumOfWeights());
        scale(_histMeanMultiSigma1385PlusMinus, 1.0/sumOfWeights());
        scale(_histMeanMultiXi1530_0          , 1.0/sumOfWeights());
        scale(_histMeanMultiOmegaMinus        , 1.0/sumOfWeights());
        scale(_histMeanMultiLambda_c_Plus     , 1.0/sumOfWeights());
        scale(_histMeanMultiSigma_c_PlusPlus_0, 1.0/sumOfWeights());
        scale(_histMeanMultiLambda1520        , 1.0/sumOfWeights());
      }

      if (sqrtS()/GeV >= 29 && sqrtS()/GeV <= 35) {
        scale(_histMeanMultiPiPlus            , 1.0/sumOfWeights());
        scale(_histMeanMultiPi0               , 1.0/sumOfWeights());
        scale(_histMeanMultiKPlus             , 1.0/sumOfWeights());
        scale(_histMeanMultiK0                , 1.0/sumOfWeights());
        scale(_histMeanMultiEta               , 1.0/sumOfWeights());
        scale(_histMeanMultiEtaPrime          , 1.0/sumOfWeights());
        scale(_histMeanMultiDPlus             , 1.0/sumOfWeights());
        scale(_histMeanMultiD0                , 1.0/sumOfWeights());
        scale(_histMeanMultiDPlus_s           , 1.0/sumOfWeights());
        scale(_histMeanMultiF0_980            , 1.0/sumOfWeights());
        scale(_histMeanMultiRho770_0          , 1.0/sumOfWeights());
        scale(_histMeanMultiKStar892Plus      , 1.0/sumOfWeights());
        scale(_histMeanMultiKStar892_0        , 1.0/sumOfWeights());
        scale(_histMeanMultiPhi1020           , 1.0/sumOfWeights());
        scale(_histMeanMultiDStar2010Plus     , 1.0/sumOfWeights());
        scale(_histMeanMultiDStar2007_0       , 1.0/sumOfWeights());
        scale(_histMeanMultiF2_1270           , 1.0/sumOfWeights());
        scale(_histMeanMultiK2Star1430Plus    , 1.0/sumOfWeights());
        scale(_histMeanMultiK2Star1430_0      , 1.0/sumOfWeights());
        scale(_histMeanMultiP                 , 1.0/sumOfWeights());
        scale(_histMeanMultiLambda            , 1.0/sumOfWeights());
        scale(_histMeanMultiXiMinus           , 1.0/sumOfWeights());
        scale(_histMeanMultiSigma1385Minus    , 1.0/sumOfWeights());
        scale(_histMeanMultiSigma1385Plus     , 1.0/sumOfWeights());
        scale(_histMeanMultiSigma1385PlusMinus, 1.0/sumOfWeights());
        scale(_histMeanMultiOmegaMinus        , 1.0/sumOfWeights());
        scale(_histMeanMultiLambda_c_Plus     , 1.0/sumOfWeights());
      }

      if (sqrtS()/GeV >= 89.5 && sqrtS()/GeV <= 91.8) {
        scale(_histMeanMultiPiPlus            , 1.0/sumOfWeights());
        scale(_histMeanMultiPi0               , 1.0/sumOfWeights());
        scale(_histMeanMultiKPlus             , 1.0/sumOfWeights());
        scale(_histMeanMultiK0                , 1.0/sumOfWeights());
        scale(_histMeanMultiEta               , 1.0/sumOfWeights());
        scale(_histMeanMultiEtaPrime          , 1.0/sumOfWeights());
        scale(_histMeanMultiDPlus             , 1.0/sumOfWeights());
        scale(_histMeanMultiD0                , 1.0/sumOfWeights());
        scale(_histMeanMultiDPlus_s           , 1.0/sumOfWeights());
        scale(_histMeanMultiBPlus_B0_d        , 1.0/sumOfWeights());
        scale(_histMeanMultiBPlus_u           , 1.0/sumOfWeights());
        scale(_histMeanMultiB0_s              , 1.0/sumOfWeights());
        scale(_histMeanMultiF0_980            , 1.0/sumOfWeights());
        scale(_histMeanMultiA0_980Plus        , 1.0/sumOfWeights());
        scale(_histMeanMultiRho770_0          , 1.0/sumOfWeights());
        scale(_histMeanMultiRho770Plus        , 1.0/sumOfWeights());
        scale(_histMeanMultiOmega782          , 1.0/sumOfWeights());
        scale(_histMeanMultiKStar892Plus      , 1.0/sumOfWeights());
        scale(_histMeanMultiKStar892_0        , 1.0/sumOfWeights());
        scale(_histMeanMultiPhi1020           , 1.0/sumOfWeights());
        scale(_histMeanMultiDStar2010Plus     , 1.0/sumOfWeights());
        scale(_histMeanMultiDStar_s2112Plus   , 1.0/sumOfWeights());
        scale(_histMeanMultiBStar             , 1.0/sumOfWeights());
        scale(_histMeanMultiJPsi1S            , 1.0/sumOfWeights());
        scale(_histMeanMultiPsi2S             , 1.0/sumOfWeights());
        scale(_histMeanMultiUpsilon1S         , 1.0/sumOfWeights());
        scale(_histMeanMultiF1_1285           , 1.0/sumOfWeights());
        scale(_histMeanMultiF1_1420           , 1.0/sumOfWeights());
        scale(_histMeanMultiChi_c1_3510       , 1.0/sumOfWeights());
        scale(_histMeanMultiF2_1270           , 1.0/sumOfWeights());
        scale(_histMeanMultiF2Prime1525       , 1.0/sumOfWeights());
        scale(_histMeanMultiK2Star1430_0      , 1.0/sumOfWeights());
        scale(_histMeanMultiBStarStar         , 1.0/sumOfWeights());
        scale(_histMeanMultiDs1Plus           , 1.0/sumOfWeights());
        scale(_histMeanMultiDs2Plus           , 1.0/sumOfWeights());
        scale(_histMeanMultiP                 , 1.0/sumOfWeights());
        scale(_histMeanMultiLambda            , 1.0/sumOfWeights());
        scale(_histMeanMultiSigma0            , 1.0/sumOfWeights());
        scale(_histMeanMultiSigmaMinus        , 1.0/sumOfWeights());
        scale(_histMeanMultiSigmaPlus         , 1.0/sumOfWeights());
        scale(_histMeanMultiSigmaPlusMinus    , 1.0/sumOfWeights());
        scale(_histMeanMultiXiMinus           , 1.0/sumOfWeights());
        scale(_histMeanMultiDelta1232PlusPlus , 1.0/sumOfWeights());
        scale(_histMeanMultiSigma1385Minus    , 1.0/sumOfWeights());
        scale(_histMeanMultiSigma1385Plus     , 1.0/sumOfWeights());
        scale(_histMeanMultiSigma1385PlusMinus, 1.0/sumOfWeights());
        scale(_histMeanMultiXi1530_0          , 1.0/sumOfWeights());
        scale(_histMeanMultiOmegaMinus        , 1.0/sumOfWeights());
        scale(_histMeanMultiLambda_c_Plus     , 1.0/sumOfWeights());
        scale(_histMeanMultiLambda_b_0        , 1.0/sumOfWeights());
        scale(_histMeanMultiLambda1520        , 1.0/sumOfWeights());
      }

      if (sqrtS()/GeV >= 130 && sqrtS()/GeV <= 200) {
        scale(_histMeanMultiPiPlus           , 1.0/sumOfWeights());
        scale(_histMeanMultiKPlus            , 1.0/sumOfWeights());
        scale(_histMeanMultiK0               , 1.0/sumOfWeights());
        scale(_histMeanMultiP                , 1.0/sumOfWeights());
        scale(_histMeanMultiLambda           , 1.0/sumOfWeights());
      }
    }

    //@}


  private:

    AIDA::IHistogram1D *_histMeanMultiPiPlus;
    AIDA::IHistogram1D *_histMeanMultiPi0;
    AIDA::IHistogram1D *_histMeanMultiKPlus;
    AIDA::IHistogram1D *_histMeanMultiK0;
    AIDA::IHistogram1D *_histMeanMultiEta;
    AIDA::IHistogram1D *_histMeanMultiEtaPrime;
    AIDA::IHistogram1D *_histMeanMultiDPlus;
    AIDA::IHistogram1D *_histMeanMultiD0;
    AIDA::IHistogram1D *_histMeanMultiDPlus_s;
    AIDA::IHistogram1D *_histMeanMultiBPlus_B0_d;
    AIDA::IHistogram1D *_histMeanMultiBPlus_u;
    AIDA::IHistogram1D *_histMeanMultiB0_s;
    AIDA::IHistogram1D *_histMeanMultiF0_980;
    AIDA::IHistogram1D *_histMeanMultiA0_980Plus;
    AIDA::IHistogram1D *_histMeanMultiRho770_0;
    AIDA::IHistogram1D *_histMeanMultiRho770Plus;
    AIDA::IHistogram1D *_histMeanMultiOmega782;
    AIDA::IHistogram1D *_histMeanMultiKStar892Plus;
    AIDA::IHistogram1D *_histMeanMultiKStar892_0;
    AIDA::IHistogram1D *_histMeanMultiPhi1020;
    AIDA::IHistogram1D *_histMeanMultiDStar2010Plus;
    AIDA::IHistogram1D *_histMeanMultiDStar2007_0;
    AIDA::IHistogram1D *_histMeanMultiDStar_s2112Plus;
    AIDA::IHistogram1D *_histMeanMultiBStar;
    AIDA::IHistogram1D *_histMeanMultiJPsi1S;
    AIDA::IHistogram1D *_histMeanMultiPsi2S;
    AIDA::IHistogram1D *_histMeanMultiUpsilon1S;
    AIDA::IHistogram1D *_histMeanMultiF1_1285;
    AIDA::IHistogram1D *_histMeanMultiF1_1420;
    AIDA::IHistogram1D *_histMeanMultiChi_c1_3510;
    AIDA::IHistogram1D *_histMeanMultiF2_1270;
    AIDA::IHistogram1D *_histMeanMultiF2Prime1525;
    AIDA::IHistogram1D *_histMeanMultiK2Star1430Plus;
    AIDA::IHistogram1D *_histMeanMultiK2Star1430_0;
    AIDA::IHistogram1D *_histMeanMultiBStarStar;
    AIDA::IHistogram1D *_histMeanMultiDs1Plus;
    AIDA::IHistogram1D *_histMeanMultiDs2Plus;
    AIDA::IHistogram1D *_histMeanMultiP;
    AIDA::IHistogram1D *_histMeanMultiLambda;
    AIDA::IHistogram1D *_histMeanMultiSigma0;
    AIDA::IHistogram1D *_histMeanMultiSigmaMinus;
    AIDA::IHistogram1D *_histMeanMultiSigmaPlus;
    AIDA::IHistogram1D *_histMeanMultiSigmaPlusMinus;
    AIDA::IHistogram1D *_histMeanMultiXiMinus;
    AIDA::IHistogram1D *_histMeanMultiDelta1232PlusPlus;
    AIDA::IHistogram1D *_histMeanMultiSigma1385Minus;
    AIDA::IHistogram1D *_histMeanMultiSigma1385Plus;
    AIDA::IHistogram1D *_histMeanMultiSigma1385PlusMinus;
    AIDA::IHistogram1D *_histMeanMultiXi1530_0;
    AIDA::IHistogram1D *_histMeanMultiOmegaMinus;
    AIDA::IHistogram1D *_histMeanMultiLambda_c_Plus;
    AIDA::IHistogram1D *_histMeanMultiLambda_b_0;
    AIDA::IHistogram1D *_histMeanMultiSigma_c_PlusPlus_0;
    AIDA::IHistogram1D *_histMeanMultiLambda1520;

    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<PDG_HADRON_MULTIPLICITIES> plugin_PDG_HADRON_MULTIPLICITIES;

}
