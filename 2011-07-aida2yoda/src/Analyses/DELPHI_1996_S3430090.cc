// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Projections/Beam.hh"
#include "Rivet/Projections/Sphericity.hh"
#include "Rivet/Projections/Thrust.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/ParisiTensor.hh"
#include "Rivet/Projections/Hemispheres.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/UnstableFinalState.hh"

namespace Rivet {


  /**
   * @brief DELPHI event shapes and identified particle spectra
   * @author Andy Buckley
   * @author Hendrik Hoeth
   *
   * This is the paper which was used for the original PROFESSOR MC tuning
   * study. It studies a wide range of e+ e- event shape variables, differential
   * jet rates in the Durham and JADE schemes, and incorporates identified
   * particle spectra, from other LEP analyses.
   *
   * @par Run conditions
   *
   * @arg LEP1 beam energy: \f$ \sqrt{s} = \f$ 91.2 GeV
   * @arg Run with generic QCD events.
   * @arg No \f$ p_\perp^\text{min} \f$ cutoff is required
   */
  class DELPHI_1996_S3430090 : public Analysis {
  public:

    /// Constructor
    DELPHI_1996_S3430090()
      : Analysis("DELPHI_1996_S3430090")
    {
      setBeams(ELECTRON, POSITRON);
      _weightedTotalPartNum = 0.0;
      _passedCutWeightSum = 0.0;
      _passedCut3WeightSum = 0.0;
      _passedCut4WeightSum = 0.0;
      _passedCut5WeightSum = 0.0;
    }


    /// @name Analysis methods
    //@{

    void init() {
      addProjection(Beam(), "Beams");
      // Don't try to introduce a pT or eta cut here. It's all corrected
      // back. (See Section 2 of the paper.)
      const ChargedFinalState cfs;
      addProjection(cfs, "FS");
      addProjection(UnstableFinalState(), "UFS");
      addProjection(FastJets(cfs, FastJets::JADE, 0.7), "JadeJets");
      addProjection(FastJets(cfs, FastJets::DURHAM, 0.7), "DurhamJets");
      addProjection(Sphericity(cfs), "Sphericity");
      addProjection(ParisiTensor(cfs), "Parisi");
      const Thrust thrust(cfs);
      addProjection(thrust, "Thrust");
      addProjection(Hemispheres(thrust), "Hemispheres");

      _histPtTIn = bookHistogram1D(1, 1, 1);
      _histPtTOut = bookHistogram1D(2, 1, 1);
      _histPtSIn = bookHistogram1D(3, 1, 1);
      _histPtSOut = bookHistogram1D(4, 1, 1);

      _histRapidityT = bookHistogram1D(5, 1, 1);
      _histRapidityS = bookHistogram1D(6, 1, 1);
      _histScaledMom = bookHistogram1D(7, 1, 1);
      _histLogScaledMom = bookHistogram1D(8, 1, 1);

      _histPtTOutVsXp = bookProfile1D(9,  1, 1);
      _histPtVsXp = bookProfile1D(10, 1, 1);

      _hist1MinusT = bookHistogram1D(11, 1, 1);
      _histTMajor = bookHistogram1D(12, 1, 1);
      _histTMinor = bookHistogram1D(13, 1, 1);
      _histOblateness = bookHistogram1D(14, 1, 1);

      _histSphericity = bookHistogram1D(15, 1, 1);
      _histAplanarity = bookHistogram1D(16, 1, 1);
      _histPlanarity = bookHistogram1D(17, 1, 1);

      _histCParam = bookHistogram1D(18, 1, 1);
      _histDParam = bookHistogram1D(19, 1, 1);

      _histHemiMassH = bookHistogram1D(20, 1, 1);
      _histHemiMassL = bookHistogram1D(21, 1, 1);
      _histHemiMassD = bookHistogram1D(22, 1, 1);

      _histHemiBroadW = bookHistogram1D(23, 1, 1);
      _histHemiBroadN = bookHistogram1D(24, 1, 1);
      _histHemiBroadT = bookHistogram1D(25, 1, 1);
      _histHemiBroadD = bookHistogram1D(26, 1, 1);

      // Binned in y_cut
      _histDiffRate2Durham = bookHistogram1D(27, 1, 1);
      _histDiffRate2Jade = bookHistogram1D(28, 1, 1);
      _histDiffRate3Durham = bookHistogram1D(29, 1, 1);
      _histDiffRate3Jade = bookHistogram1D(30, 1, 1);
      _histDiffRate4Durham = bookHistogram1D(31, 1, 1);
      _histDiffRate4Jade = bookHistogram1D(32, 1, 1);

      // Binned in cos(chi)
      _histEEC = bookHistogram1D(33, 1, 1);
      _histAEEC = bookHistogram1D(34, 1, 1);

      _histMultiCharged = bookHistogram1D(35, 1, 1);

      _histMultiPiPlus = bookHistogram1D(36, 1, 1);
      _histMultiPi0 = bookHistogram1D(36, 1, 2);
      _histMultiKPlus = bookHistogram1D(36, 1, 3);
      _histMultiK0 = bookHistogram1D(36, 1, 4);
      _histMultiEta = bookHistogram1D(36, 1, 5);
      _histMultiEtaPrime = bookHistogram1D(36, 1, 6);
      _histMultiDPlus = bookHistogram1D(36, 1, 7);
      _histMultiD0 = bookHistogram1D(36, 1, 8);
      _histMultiBPlus0 = bookHistogram1D(36, 1, 9);

      _histMultiF0 = bookHistogram1D(37, 1, 1);

      _histMultiRho = bookHistogram1D(38, 1, 1);
      _histMultiKStar892Plus = bookHistogram1D(38, 1, 2);
      _histMultiKStar892_0 = bookHistogram1D(38, 1, 3);
      _histMultiPhi = bookHistogram1D(38, 1, 4);
      _histMultiDStar2010Plus = bookHistogram1D(38, 1, 5);

      _histMultiF2 = bookHistogram1D(39, 1, 1);
      _histMultiK2Star1430_0 = bookHistogram1D(39, 1, 2);

      _histMultiP = bookHistogram1D(40, 1, 1);
      _histMultiLambda0 = bookHistogram1D(40, 1, 2);
      _histMultiXiMinus = bookHistogram1D(40, 1, 3);
      _histMultiOmegaMinus = bookHistogram1D(40, 1, 4);
      _histMultiDeltaPlusPlus = bookHistogram1D(40, 1, 5);
      _histMultiSigma1385Plus = bookHistogram1D(40, 1, 6);
      _histMultiXi1530_0 = bookHistogram1D(40, 1, 7);
      _histMultiLambdaB0 = bookHistogram1D(40, 1, 8);
    }



    void analyze(const Event& e) {
      // First, veto on leptonic events by requiring at least 4 charged FS particles
      const FinalState& fs = applyProjection<FinalState>(e, "FS");
      const size_t numParticles = fs.particles().size();
      // Even if we only generate hadronic events, we still need a cut on numCharged >= 2.
      if (numParticles < 2) {
        getLog() << Log::DEBUG << "Failed leptonic event cut" << endl;
        vetoEvent;
      }
      getLog() << Log::DEBUG << "Passed leptonic event cut" << endl;
      const double weight = e.weight();
      _passedCutWeightSum += weight;
      _weightedTotalPartNum += numParticles * weight;

      // Get beams and average beam momentum
      const ParticlePair& beams = applyProjection<Beam>(e, "Beams").beams();
      const double meanBeamMom = ( beams.first.momentum().vector3().mod() +
                                   beams.second.momentum().vector3().mod() ) / 2.0;
      getLog() << Log::DEBUG << "Avg beam momentum = " << meanBeamMom << endl;

      // Thrusts
      getLog() << Log::DEBUG << "Calculating thrust" << endl;
      const Thrust& thrust = applyProjection<Thrust>(e, "Thrust");
      _hist1MinusT->fill(1 - thrust.thrust(), weight);
      _histTMajor->fill(thrust.thrustMajor(), weight);
      _histTMinor->fill(thrust.thrustMinor(), weight);
      _histOblateness->fill(thrust.oblateness(), weight);

      // Jets
      const FastJets& durjet = applyProjection<FastJets>(e, "DurhamJets");
      const FastJets& jadejet = applyProjection<FastJets>(e, "JadeJets");
      if (numParticles >= 3) {
        _passedCut3WeightSum += weight;
        if (durjet.clusterSeq()) _histDiffRate2Durham->fill(durjet.clusterSeq()->exclusive_ymerge_max(2), weight);
        if (jadejet.clusterSeq()) _histDiffRate2Jade->fill(jadejet.clusterSeq()->exclusive_ymerge_max(2), weight);
      }
      if (numParticles >= 4) {
        _passedCut4WeightSum += weight;
        if (durjet.clusterSeq()) _histDiffRate3Durham->fill(durjet.clusterSeq()->exclusive_ymerge_max(3), weight);
        if (jadejet.clusterSeq()) _histDiffRate3Jade->fill(jadejet.clusterSeq()->exclusive_ymerge_max(3), weight);
      }
      if (numParticles >= 5) {
        _passedCut5WeightSum += weight;
        if (durjet.clusterSeq()) _histDiffRate4Durham->fill(durjet.clusterSeq()->exclusive_ymerge_max(4), weight);
        if (jadejet.clusterSeq()) _histDiffRate4Jade->fill(jadejet.clusterSeq()->exclusive_ymerge_max(4), weight);
      }

      // Sphericities
      getLog() << Log::DEBUG << "Calculating sphericity" << endl;
      const Sphericity& sphericity = applyProjection<Sphericity>(e, "Sphericity");
      _histSphericity->fill(sphericity.sphericity(), weight);
      _histAplanarity->fill(sphericity.aplanarity(), weight);
      _histPlanarity->fill(sphericity.planarity(), weight);

      // C & D params
      getLog() << Log::DEBUG << "Calculating Parisi params" << endl;
      const ParisiTensor& parisi = applyProjection<ParisiTensor>(e, "Parisi");
      _histCParam->fill(parisi.C(), weight);
      _histDParam->fill(parisi.D(), weight);

      // Hemispheres
      getLog() << Log::DEBUG << "Calculating hemisphere variables" << endl;
      const Hemispheres& hemi = applyProjection<Hemispheres>(e, "Hemispheres");
      _histHemiMassH->fill(hemi.scaledM2high(), weight);
      _histHemiMassL->fill(hemi.scaledM2low(), weight);
      _histHemiMassD->fill(hemi.scaledM2diff(), weight);
      _histHemiBroadW->fill(hemi.Bmax(), weight);
      _histHemiBroadN->fill(hemi.Bmin(), weight);
      _histHemiBroadT->fill(hemi.Bsum(), weight);
      _histHemiBroadD->fill(hemi.Bdiff(), weight);

      // Iterate over all the charged final state particles.
      double Evis = 0.0;
      double Evis2 = 0.0;
      getLog() << Log::DEBUG << "About to iterate over charged FS particles" << endl;
      foreach (const Particle& p, fs.particles()) {
        // Get momentum and energy of each particle.
        const Vector3 mom3 = p.momentum().vector3();
        const double energy = p.momentum().E();
        Evis += energy;

        // Scaled momenta.
        const double mom = mom3.mod();
        const double scaledMom = mom/meanBeamMom;
        const double logInvScaledMom = -std::log(scaledMom);
        _histLogScaledMom->fill(logInvScaledMom, weight);
        _histScaledMom->fill(scaledMom, weight);

        // Get momenta components w.r.t. thrust and sphericity.
        const double momT = dot(thrust.thrustAxis(), mom3);
        const double momS = dot(sphericity.sphericityAxis(), mom3);
        const double pTinT = dot(mom3, thrust.thrustMajorAxis());
        const double pToutT = dot(mom3, thrust.thrustMinorAxis());
        const double pTinS = dot(mom3, sphericity.sphericityMajorAxis());
        const double pToutS = dot(mom3, sphericity.sphericityMinorAxis());
        const double pT = sqrt(pow(pTinT, 2) + pow(pToutT, 2));
        _histPtTIn->fill(fabs(pTinT/GeV), weight);
        _histPtTOut->fill(fabs(pToutT/GeV), weight);
        _histPtSIn->fill(fabs(pTinS/GeV), weight);
        _histPtSOut->fill(fabs(pToutS/GeV), weight);
        _histPtVsXp->fill(scaledMom, fabs(pT/GeV), weight);
        _histPtTOutVsXp->fill(scaledMom, fabs(pToutT/GeV), weight);

        // Calculate rapidities w.r.t. thrust and sphericity.
        const double rapidityT = 0.5 * std::log((energy + momT) / (energy - momT));
        const double rapidityS = 0.5 * std::log((energy + momS) / (energy - momS));
        _histRapidityT->fill(rapidityT, weight);
        _histRapidityS->fill(rapidityS, weight);
        //cerr << fabs(rapidityT) << " " << scaledMom/GeV << endl;
      }
      Evis2 = Evis*Evis;

      // (A)EEC
      // Need iterators since second loop starts at current outer loop iterator, i.e. no "foreach" here!
      for (ParticleVector::const_iterator p_i = fs.particles().begin(); p_i != fs.particles().end(); ++p_i) {
        for (ParticleVector::const_iterator p_j = p_i; p_j != fs.particles().end(); ++p_j) {
          if (p_i == p_j) continue;
          const Vector3 mom3_i = p_i->momentum().vector3();
          const Vector3 mom3_j = p_j->momentum().vector3();
          const double energy_i = p_i->momentum().E();
          const double energy_j = p_j->momentum().E();
          const double cosij = dot(mom3_i.unit(), mom3_j.unit());
          const double eec = (energy_i*energy_j) / Evis2;
          _histEEC->fill(cosij, eec*weight);
          _histAEEC->fill( cosij,  eec*weight);
          _histAEEC->fill(-cosij, -eec*weight);
        }
      }

      _histMultiCharged->fill(_histMultiCharged->binMean(0), numParticles*weight);


      // Final state of unstable particles to get particle spectra
      const UnstableFinalState& ufs = applyProjection<UnstableFinalState>(e, "UFS");

      foreach (const Particle& p, ufs.particles()) {
        int id = abs(p.pdgId());
        switch (id) {
        case 211:
          _histMultiPiPlus->fill(_histMultiPiPlus->binMean(0), weight);
          break;
        case 111:
          _histMultiPi0->fill(_histMultiPi0->binMean(0), weight);
          break;
        case 321:
          _histMultiKPlus->fill(_histMultiKPlus->binMean(0), weight);
          break;
        case 130:
        case 310:
          _histMultiK0->fill(_histMultiK0->binMean(0), weight);
          break;
        case 221:
          _histMultiEta->fill(_histMultiEta->binMean(0), weight);
          break;
        case 331:
          _histMultiEtaPrime->fill(_histMultiEtaPrime->binMean(0), weight);
          break;
        case 411:
          _histMultiDPlus->fill(_histMultiDPlus->binMean(0), weight);
          break;
        case 421:
          _histMultiD0->fill(_histMultiD0->binMean(0), weight);
          break;
        case 511:
        case 521:
        case 531:
          _histMultiBPlus0->fill(_histMultiBPlus0->binMean(0), weight);
          break;
        case 9010221:
          _histMultiF0->fill(_histMultiF0->binMean(0), weight);
          break;
        case 113:
          _histMultiRho->fill(_histMultiRho->binMean(0), weight);
          break;
        case 323:
          _histMultiKStar892Plus->fill(_histMultiKStar892Plus->binMean(0), weight);
          break;
        case 313:
          _histMultiKStar892_0->fill(_histMultiKStar892_0->binMean(0), weight);
          break;
        case 333:
          _histMultiPhi->fill(_histMultiPhi->binMean(0), weight);
          break;
        case 413:
          _histMultiDStar2010Plus->fill(_histMultiDStar2010Plus->binMean(0), weight);
          break;
        case 225:
          _histMultiF2->fill(_histMultiF2->binMean(0), weight);
          break;
        case 315:
          _histMultiK2Star1430_0->fill(_histMultiK2Star1430_0->binMean(0), weight);
          break;
        case 2212:
          _histMultiP->fill(_histMultiP->binMean(0), weight);
          break;
        case 3122:
          _histMultiLambda0->fill(_histMultiLambda0->binMean(0), weight);
          break;
        case 3312:
          _histMultiXiMinus->fill(_histMultiXiMinus->binMean(0), weight);
          break;
        case 3334:
          _histMultiOmegaMinus->fill(_histMultiOmegaMinus->binMean(0), weight);
          break;
        case 2224:
          _histMultiDeltaPlusPlus->fill(_histMultiDeltaPlusPlus->binMean(0), weight);
          break;
        case 3114:
          _histMultiSigma1385Plus->fill(_histMultiSigma1385Plus->binMean(0), weight);
          break;
        case 3324:
          _histMultiXi1530_0->fill(_histMultiXi1530_0->binMean(0), weight);
          break;
        case 5122:
          _histMultiLambdaB0->fill(_histMultiLambdaB0->binMean(0), weight);
          break;
        }
      }
    }



    // Finalize
    void finalize() {
      // Normalize inclusive single particle distributions to the average number
      // of charged particles per event.
      const double avgNumParts = _weightedTotalPartNum / _passedCutWeightSum;

      normalize(_histPtTIn, avgNumParts);
      normalize(_histPtTOut, avgNumParts);
      normalize(_histPtSIn, avgNumParts);
      normalize(_histPtSOut, avgNumParts);

      normalize(_histRapidityT, avgNumParts);
      normalize(_histRapidityS, avgNumParts);

      normalize(_histLogScaledMom, avgNumParts);
      normalize(_histScaledMom, avgNumParts);

      scale(_histEEC, 1.0/_passedCutWeightSum);
      scale(_histAEEC, 1.0/_passedCutWeightSum);
      scale(_histMultiCharged, 1.0/_passedCutWeightSum);

      scale(_histMultiPiPlus, 1.0/_passedCutWeightSum);
      scale(_histMultiPi0, 1.0/_passedCutWeightSum);
      scale(_histMultiKPlus, 1.0/_passedCutWeightSum);
      scale(_histMultiK0, 1.0/_passedCutWeightSum);
      scale(_histMultiEta, 1.0/_passedCutWeightSum);
      scale(_histMultiEtaPrime, 1.0/_passedCutWeightSum);
      scale(_histMultiDPlus, 1.0/_passedCutWeightSum);
      scale(_histMultiD0, 1.0/_passedCutWeightSum);
      scale(_histMultiBPlus0, 1.0/_passedCutWeightSum);

      scale(_histMultiF0, 1.0/_passedCutWeightSum);

      scale(_histMultiRho, 1.0/_passedCutWeightSum);
      scale(_histMultiKStar892Plus, 1.0/_passedCutWeightSum);
      scale(_histMultiKStar892_0, 1.0/_passedCutWeightSum);
      scale(_histMultiPhi, 1.0/_passedCutWeightSum);
      scale(_histMultiDStar2010Plus, 1.0/_passedCutWeightSum);

      scale(_histMultiF2, 1.0/_passedCutWeightSum);
      scale(_histMultiK2Star1430_0, 1.0/_passedCutWeightSum);

      scale(_histMultiP, 1.0/_passedCutWeightSum);
      scale(_histMultiLambda0, 1.0/_passedCutWeightSum);
      scale(_histMultiXiMinus, 1.0/_passedCutWeightSum);
      scale(_histMultiOmegaMinus, 1.0/_passedCutWeightSum);
      scale(_histMultiDeltaPlusPlus, 1.0/_passedCutWeightSum);
      scale(_histMultiSigma1385Plus, 1.0/_passedCutWeightSum);
      scale(_histMultiXi1530_0, 1.0/_passedCutWeightSum);
      scale(_histMultiLambdaB0, 1.0/_passedCutWeightSum);

      scale(_hist1MinusT, 1.0/_passedCutWeightSum);
      scale(_histTMajor, 1.0/_passedCutWeightSum);
      scale(_histTMinor, 1.0/_passedCutWeightSum);
      scale(_histOblateness, 1.0/_passedCutWeightSum);

      scale(_histSphericity, 1.0/_passedCutWeightSum);
      scale(_histAplanarity, 1.0/_passedCutWeightSum);
      scale(_histPlanarity, 1.0/_passedCutWeightSum);

      scale(_histHemiMassD, 1.0/_passedCutWeightSum);
      scale(_histHemiMassH, 1.0/_passedCutWeightSum);
      scale(_histHemiMassL, 1.0/_passedCutWeightSum);

      scale(_histHemiBroadW, 1.0/_passedCutWeightSum);
      scale(_histHemiBroadN, 1.0/_passedCutWeightSum);
      scale(_histHemiBroadT, 1.0/_passedCutWeightSum);
      scale(_histHemiBroadD, 1.0/_passedCutWeightSum);

      scale(_histCParam, 1.0/_passedCutWeightSum);
      scale(_histDParam, 1.0/_passedCutWeightSum);

      scale(_histDiffRate2Durham, 1.0/_passedCut3WeightSum);
      scale(_histDiffRate2Jade, 1.0/_passedCut3WeightSum);
      scale(_histDiffRate3Durham, 1.0/_passedCut4WeightSum);
      scale(_histDiffRate3Jade, 1.0/_passedCut4WeightSum);
      scale(_histDiffRate4Durham, 1.0/_passedCut5WeightSum);
      scale(_histDiffRate4Jade, 1.0/_passedCut5WeightSum);
    }

    //@}


  private:

    /// Store the weighted sums of numbers of charged / charged+neutral
    /// particles - used to calculate average number of particles for the
    /// inclusive single particle distributions' normalisations.
    double _weightedTotalPartNum;

    /// @name Sums of weights past various cuts
    //@{
    double _passedCutWeightSum;
    double _passedCut3WeightSum;
    double _passedCut4WeightSum;
    double _passedCut5WeightSum;
    //@}

    /// @name Histograms
    //@{
    AIDA::IHistogram1D *_histPtTIn;
    AIDA::IHistogram1D *_histPtTOut;
    AIDA::IHistogram1D *_histPtSIn;
    AIDA::IHistogram1D *_histPtSOut;

    AIDA::IHistogram1D *_histRapidityT;
    AIDA::IHistogram1D *_histRapidityS;

    AIDA::IHistogram1D *_histScaledMom, *_histLogScaledMom;

    AIDA::IProfile1D   *_histPtTOutVsXp, *_histPtVsXp;

    AIDA::IHistogram1D *_hist1MinusT;
    AIDA::IHistogram1D *_histTMajor;
    AIDA::IHistogram1D *_histTMinor;
    AIDA::IHistogram1D *_histOblateness;

    AIDA::IHistogram1D *_histSphericity;
    AIDA::IHistogram1D *_histAplanarity;
    AIDA::IHistogram1D *_histPlanarity;

    AIDA::IHistogram1D *_histCParam;
    AIDA::IHistogram1D *_histDParam;

    AIDA::IHistogram1D *_histHemiMassD;
    AIDA::IHistogram1D *_histHemiMassH;
    AIDA::IHistogram1D *_histHemiMassL;

    AIDA::IHistogram1D *_histHemiBroadW;
    AIDA::IHistogram1D *_histHemiBroadN;
    AIDA::IHistogram1D *_histHemiBroadT;
    AIDA::IHistogram1D *_histHemiBroadD;

    AIDA::IHistogram1D *_histDiffRate2Durham;
    AIDA::IHistogram1D *_histDiffRate2Jade;
    AIDA::IHistogram1D *_histDiffRate3Durham;
    AIDA::IHistogram1D *_histDiffRate3Jade;
    AIDA::IHistogram1D *_histDiffRate4Durham;
    AIDA::IHistogram1D *_histDiffRate4Jade;

    AIDA::IHistogram1D *_histEEC, *_histAEEC;

    AIDA::IHistogram1D *_histMultiCharged;

    AIDA::IHistogram1D *_histMultiPiPlus;
    AIDA::IHistogram1D *_histMultiPi0;
    AIDA::IHistogram1D *_histMultiKPlus;
    AIDA::IHistogram1D *_histMultiK0;
    AIDA::IHistogram1D *_histMultiEta;
    AIDA::IHistogram1D *_histMultiEtaPrime;
    AIDA::IHistogram1D *_histMultiDPlus;
    AIDA::IHistogram1D *_histMultiD0;
    AIDA::IHistogram1D *_histMultiBPlus0;

    AIDA::IHistogram1D *_histMultiF0;

    AIDA::IHistogram1D *_histMultiRho;
    AIDA::IHistogram1D *_histMultiKStar892Plus;
    AIDA::IHistogram1D *_histMultiKStar892_0;
    AIDA::IHistogram1D *_histMultiPhi;
    AIDA::IHistogram1D *_histMultiDStar2010Plus;

    AIDA::IHistogram1D *_histMultiF2;
    AIDA::IHistogram1D *_histMultiK2Star1430_0;

    AIDA::IHistogram1D *_histMultiP;
    AIDA::IHistogram1D *_histMultiLambda0;
    AIDA::IHistogram1D *_histMultiXiMinus;
    AIDA::IHistogram1D *_histMultiOmegaMinus;
    AIDA::IHistogram1D *_histMultiDeltaPlusPlus;
    AIDA::IHistogram1D *_histMultiSigma1385Plus;
    AIDA::IHistogram1D *_histMultiXi1530_0;
    AIDA::IHistogram1D *_histMultiLambdaB0;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<DELPHI_1996_S3430090> plugin_DELPHI_1996_S3430090;

}
