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


  /// @brief ALEPH QCD study with event shapes and identified particles
  /// @author Holger Schulz
  class ALEPH_1996_S3486095 : public Analysis {

  public:

    /// Constructor
    ALEPH_1996_S3486095()
      : Analysis("ALEPH_1996_S3486095")
    {
      setBeams(ELECTRON, POSITRON);
      _numChParticles               = 0;
      _weightedTotalPartNum         = 0;
      _weightedTotalNumPiPlus       = 0;
      _weightedTotalNumKPlus        = 0;
      _weightedTotalNumP            = 0;
      _weightedTotalNumPhoton       = 0;
      _weightedTotalNumPi0          = 0;
      _weightedTotalNumEta          = 0;
      _weightedTotalNumEtaPrime     = 0;
      _weightedTotalNumK0           = 0;
      _weightedTotalNumLambda0      = 0;
      _weightedTotalNumXiMinus      = 0;
      _weightedTotalNumSigma1385Plus= 0;
      _weightedTotalNumXi1530_0     = 0;
      _weightedTotalNumRho          = 0;
      _weightedTotalNumOmega782     = 0;
      _weightedTotalNumKStar892_0   = 0;
      _weightedTotalNumPhi          = 0;
      _weightedTotalNumKStar892Plus = 0;
    }


    /// @name Analysis methods
    //@{

    void init() {
      // Set up projections
      addProjection(Beam(), "Beams");
      const ChargedFinalState cfs;
      addProjection(cfs, "FS");
      addProjection(UnstableFinalState(), "UFS");
      addProjection(FastJets(cfs, FastJets::DURHAM, 0.7), "DurhamJets");
      addProjection(Sphericity(cfs), "Sphericity");
      addProjection(ParisiTensor(cfs), "Parisi");
      const Thrust thrust(cfs);
      addProjection(thrust, "Thrust");
      addProjection(Hemispheres(thrust), "Hemispheres");

      // Book histograms
      _histSphericity   = bookHistogram1D(1, 1, 1);
      _histAplanarity   = bookHistogram1D(2, 1, 1);

      _hist1MinusT      = bookHistogram1D(3, 1, 1);
      _histTMinor       = bookHistogram1D(4, 1, 1);

      _histY3           = bookHistogram1D(5, 1, 1);
      _histHeavyJetMass = bookHistogram1D(6, 1, 1);
      _histCParam       = bookHistogram1D(7, 1, 1);
      _histOblateness   = bookHistogram1D(8, 1, 1);

      _histScaledMom    = bookHistogram1D(9, 1, 1);
      _histRapidityT    = bookHistogram1D(10, 1, 1);

      _histPtSIn        = bookHistogram1D(11, 1, 1);
      _histPtSOut       = bookHistogram1D(12, 1, 1);

      _histLogScaledMom = bookHistogram1D(17, 1, 1);

      _histChMult       = bookHistogram1D(18, 1, 1);
      _histMeanChMult   = bookHistogram1D(19, 1, 1);

      _histMeanChMultRapt05= bookHistogram1D(20, 1, 1);
      _histMeanChMultRapt10= bookHistogram1D(21, 1, 1);
      _histMeanChMultRapt15= bookHistogram1D(22, 1, 1);
      _histMeanChMultRapt20= bookHistogram1D(23, 1, 1);


      // Particle spectra
      _histMultiPiPlus        = bookHistogram1D(25, 1, 1);
      _histMultiKPlus         = bookHistogram1D(26, 1, 1);
      _histMultiP             = bookHistogram1D(27, 1, 1);
      _histMultiPhoton        = bookHistogram1D(28, 1, 1);
      _histMultiPi0           = bookHistogram1D(29, 1, 1);
      _histMultiEta           = bookHistogram1D(30, 1, 1);
      _histMultiEtaPrime      = bookHistogram1D(31, 1, 1);
      _histMultiK0            = bookHistogram1D(32, 1, 1);
      _histMultiLambda0       = bookHistogram1D(33, 1, 1);
      _histMultiXiMinus       = bookHistogram1D(34, 1, 1);
      _histMultiSigma1385Plus = bookHistogram1D(35, 1, 1);
      _histMultiXi1530_0      = bookHistogram1D(36, 1, 1);
      _histMultiRho           = bookHistogram1D(37, 1, 1);
      _histMultiOmega782      = bookHistogram1D(38, 1, 1);
      _histMultiKStar892_0    = bookHistogram1D(39, 1, 1);
      _histMultiPhi           = bookHistogram1D(40, 1, 1);

      _histMultiKStar892Plus  = bookHistogram1D(43, 1, 1);

      // Mean multiplicities
      _histMeanMultiPi0           = bookHistogram1D(44, 1,  2);
      _histMeanMultiEta           = bookHistogram1D(44, 1,  3);
      _histMeanMultiEtaPrime      = bookHistogram1D(44, 1,  4);
      _histMeanMultiK0            = bookHistogram1D(44, 1,  5);
      _histMeanMultiRho           = bookHistogram1D(44, 1,  6);
      _histMeanMultiOmega782      = bookHistogram1D(44, 1,  7);
      _histMeanMultiPhi           = bookHistogram1D(44, 1,  8);
      _histMeanMultiKStar892Plus  = bookHistogram1D(44, 1,  9);
      _histMeanMultiKStar892_0    = bookHistogram1D(44, 1, 10);
      _histMeanMultiLambda0       = bookHistogram1D(44, 1, 11);
      _histMeanMultiSigma0        = bookHistogram1D(44, 1, 12);
      _histMeanMultiXiMinus       = bookHistogram1D(44, 1, 13);
      _histMeanMultiSigma1385Plus = bookHistogram1D(44, 1, 14);
      _histMeanMultiXi1530_0      = bookHistogram1D(44, 1, 15);
      _histMeanMultiOmegaOmegaBar = bookHistogram1D(44, 1, 16);
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

      // Get event weight for histo filling
      const double weight = e.weight();
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
      _histTMinor->fill(thrust.thrustMinor(), weight);
      _histOblateness->fill(thrust.oblateness(), weight);

      // Jets
      getLog() << Log::DEBUG << "Calculating differential jet rate plots:" << endl;
      const FastJets& durjet = applyProjection<FastJets>(e, "DurhamJets");
      if (durjet.clusterSeq()) {
        double y3 = durjet.clusterSeq()->exclusive_ymerge_max(2);
        _histY3->fill(-1. * std::log(y3), weight);
      }

      // Sphericities
      getLog() << Log::DEBUG << "Calculating sphericity" << endl;
      const Sphericity& sphericity = applyProjection<Sphericity>(e, "Sphericity");
      _histSphericity->fill(sphericity.sphericity(), weight);
      _histAplanarity->fill(sphericity.aplanarity(), weight);

      // C param
      getLog() << Log::DEBUG << "Calculating Parisi params" << endl;
      const ParisiTensor& parisi = applyProjection<ParisiTensor>(e, "Parisi");
      _histCParam->fill(parisi.C(), weight);

      // Hemispheres
      getLog() << Log::DEBUG << "Calculating hemisphere variables" << endl;
      const Hemispheres& hemi = applyProjection<Hemispheres>(e, "Hemispheres");
      _histHeavyJetMass->fill(hemi.scaledM2high(), weight);

      // Iterate over all the charged final state particles.
      double Evis = 0.0;
      double rapt05 = 0.;
      double rapt10 = 0.;
      double rapt15 = 0.;
      double rapt20 = 0.;
      //int numChParticles = 0;
      getLog() << Log::DEBUG << "About to iterate over charged FS particles" << endl;
      foreach (const Particle& p, fs.particles()) {
        // Get momentum and energy of each particle.
        const Vector3 mom3 = p.momentum().vector3();
        const double energy = p.momentum().E();
        Evis += energy;
        _numChParticles += weight;

        // Scaled momenta.
        const double mom = mom3.mod();
        const double scaledMom = mom/meanBeamMom;
        const double logInvScaledMom = -std::log(scaledMom);
        _histLogScaledMom->fill(logInvScaledMom, weight);
        _histScaledMom->fill(scaledMom, weight);

        // Get momenta components w.r.t. thrust and sphericity.
        const double momT = dot(thrust.thrustAxis(), mom3);
        const double pTinS = dot(mom3, sphericity.sphericityMajorAxis());
        const double pToutS = dot(mom3, sphericity.sphericityMinorAxis());
        _histPtSIn->fill(fabs(pTinS/GeV), weight);
        _histPtSOut->fill(fabs(pToutS/GeV), weight);

        // Calculate rapidities w.r.t. thrust.
        const double rapidityT = 0.5 * std::log((energy + momT) / (energy - momT));
        _histRapidityT->fill(rapidityT, weight);
        if (std::fabs(rapidityT) <= 0.5)  {
            rapt05 += 1.0;
        }
        if (std::fabs(rapidityT) <= 1.0)  {
            rapt10 += 1.0;
        }
        if (std::fabs(rapidityT) <= 1.5) {
            rapt15 += 1.0;
        }
        if (std::fabs(rapidityT) <= 2.0)  {
            rapt20 += 1.0;
        }

      }

      _histChMult->fill(numParticles, weight);

      _histMeanChMultRapt05->fill(_histMeanChMultRapt05->binMean(0), rapt05 * weight);
      _histMeanChMultRapt10->fill(_histMeanChMultRapt10->binMean(0), rapt10 * weight);
      _histMeanChMultRapt15->fill(_histMeanChMultRapt15->binMean(0), rapt15 * weight);
      _histMeanChMultRapt20->fill(_histMeanChMultRapt20->binMean(0), rapt20 * weight);
      _histMeanChMult->fill(_histMeanChMult->binMean(0), numParticles*weight);


      //// Final state of unstable particles to get particle spectra
      const UnstableFinalState& ufs = applyProjection<UnstableFinalState>(e, "UFS");
      for (ParticleVector::const_iterator p = ufs.particles().begin(); p != ufs.particles().end(); ++p) {
        const Vector3 mom3 = p->momentum().vector3();
        int id = abs(p->pdgId());
        const double mom = mom3.mod();
        const double energy = p->momentum().E();
        const double scaledMom = mom/meanBeamMom;
        const double scaledEnergy = energy/meanBeamMom;  // meanBeamMom is approximately beam energy
        switch (id) {
           case 22:
              _histMultiPhoton->fill(-1.*std::log(scaledMom), weight);
              _weightedTotalNumPhoton += weight;
              break;
           case -321:
           case 321:
              _weightedTotalNumKPlus += weight;
              _histMultiKPlus->fill(scaledMom, weight);
              break;
           case 211:
           case -211:
              _histMultiPiPlus->fill(scaledMom, weight);
              _weightedTotalNumPiPlus += weight;
              break;
           case 2212:
           case -2212:
              _histMultiP->fill(scaledMom, weight);
              _weightedTotalNumP += weight;
              break;
           case 111:
              _histMultiPi0->fill(scaledMom, weight);
              _histMeanMultiPi0->fill(_histMeanMultiPi0->binMean(0), weight);
              _weightedTotalNumPi0 += weight;
              break;
           case 221:
              if (scaledMom >= 0.1) {
                _histMultiEta->fill(scaledEnergy, weight);
                _histMeanMultiEta->fill(_histMeanMultiEta->binMean(0), weight);
                _weightedTotalNumEta += weight;
              }
              break;
           case 331:
              if (scaledMom >= 0.1) {
                _histMultiEtaPrime->fill(scaledEnergy, weight);
                _histMeanMultiEtaPrime->fill(_histMeanMultiEtaPrime->binMean(0), weight);
                _weightedTotalNumEtaPrime += weight;
              }
              break;
           case 130: //klong
           case 310: //kshort
              _histMultiK0->fill(scaledMom, weight);
              _histMeanMultiK0->fill(_histMeanMultiK0->binMean(0), weight);
              _weightedTotalNumK0 += weight;
              break;
           case 113:
              _histMultiRho->fill(scaledMom, weight);
              _histMeanMultiRho->fill(_histMeanMultiRho->binMean(0), weight);
              _weightedTotalNumRho += weight;
              break;
           case 223:
              _histMultiOmega782->fill(scaledMom, weight);
              _histMeanMultiOmega782->fill(_histMeanMultiOmega782->binMean(0), weight);
              _weightedTotalNumOmega782 += weight;
              break;
           case 333:
              _histMultiPhi->fill(scaledMom, weight);
              _histMeanMultiPhi->fill(_histMeanMultiPhi->binMean(0), weight);
              _weightedTotalNumPhi += weight;
              break;
           case 313:
           case -313:
              _histMultiKStar892_0->fill(scaledMom, weight);
              _histMeanMultiKStar892_0->fill(_histMeanMultiKStar892_0->binMean(0), weight);
              _weightedTotalNumKStar892_0 += weight;
              break;
           case 323:
           case -323:
              _histMultiKStar892Plus->fill(scaledEnergy, weight);
              _histMeanMultiKStar892Plus->fill(_histMeanMultiKStar892Plus->binMean(0), weight);
              _weightedTotalNumKStar892Plus += weight;
              break;
           case 3122:
           case -3122:
              _histMultiLambda0->fill(scaledMom, weight);
              _histMeanMultiLambda0->fill(_histMeanMultiLambda0->binMean(0), weight);
              _weightedTotalNumLambda0 += weight;
              break;
           case 3212:
           case -3212:
              _histMeanMultiSigma0->fill(_histMeanMultiSigma0->binMean(0), weight);
              break;
           case 3312:
           case -3312:
              _histMultiXiMinus->fill(scaledEnergy, weight);
              _histMeanMultiXiMinus->fill(_histMeanMultiXiMinus->binMean(0), weight);
              _weightedTotalNumXiMinus += weight;
              break;
           case 3114:
           case -3114:
           case 3224:
           case -3224:
              _histMultiSigma1385Plus->fill(scaledEnergy, weight);
              _histMeanMultiSigma1385Plus->fill(_histMeanMultiSigma1385Plus->binMean(0), weight);
              _weightedTotalNumSigma1385Plus += weight;
              break;
           case 3324:
           case -3324:
              _histMultiXi1530_0->fill(scaledEnergy, weight);
              _histMeanMultiXi1530_0->fill(_histMeanMultiXi1530_0->binMean(0), weight);
              _weightedTotalNumXi1530_0 += weight;
              break;
           case 3334:
              _histMeanMultiOmegaOmegaBar->fill(_histMeanMultiOmegaOmegaBar->binMean(0), weight);
              break;
        }
      }

    }



    /// Finalize
    void finalize() {
      // Normalize inclusive single particle distributions to the average number
      // of charged particles per event.
      const double avgNumParts = _weightedTotalPartNum / sumOfWeights();

      normalize(_histPtSIn, avgNumParts);
      normalize(_histPtSOut, avgNumParts);

      normalize(_histRapidityT, avgNumParts);
      normalize(_histY3);

      normalize(_histLogScaledMom, avgNumParts);
      normalize(_histScaledMom, avgNumParts);

      // particle spectra
      scale(_histMultiPiPlus        ,1./sumOfWeights());
      scale(_histMultiKPlus         ,1./sumOfWeights());
      scale(_histMultiP             ,1./sumOfWeights());
      scale(_histMultiPhoton        ,1./sumOfWeights());
      scale(_histMultiPi0           ,1./sumOfWeights());
      scale(_histMultiEta           ,1./sumOfWeights());
      scale(_histMultiEtaPrime      ,1./sumOfWeights());
      scale(_histMultiK0            ,1./sumOfWeights());
      scale(_histMultiLambda0       ,1./sumOfWeights());
      scale(_histMultiXiMinus       ,1./sumOfWeights());
      scale(_histMultiSigma1385Plus ,1./sumOfWeights());
      scale(_histMultiXi1530_0      ,1./sumOfWeights());
      scale(_histMultiRho           ,1./sumOfWeights());
      scale(_histMultiOmega782      ,1./sumOfWeights());
      scale(_histMultiKStar892_0    ,1./sumOfWeights());
      scale(_histMultiPhi           ,1./sumOfWeights());

      scale(_histMultiKStar892Plus  ,1./sumOfWeights());

      //normalize(_histMultiPiPlus        ,_weightedTotalNumPiPlus / sumOfWeights());
      //normalize(_histMultiKPlus         ,_weightedTotalNumKPlus/sumOfWeights());
      //normalize(_histMultiP             ,_weightedTotalNumP/sumOfWeights());
      //normalize(_histMultiPhoton            ,_weightedTotalNumPhoton/sumOfWeights());
      //normalize(_histMultiPi0           ,_weightedTotalNumPi0/sumOfWeights());
      //normalize(_histMultiEta           ,_weightedTotalNumEta/sumOfWeights());
      //normalize(_histMultiEtaPrime      ,_weightedTotalNumEtaPrime/sumOfWeights());
      //normalize(_histMultiK0            ,_weightedTotalNumK0/sumOfWeights());
      //normalize(_histMultiLambda0       ,_weightedTotalNumLambda0/sumOfWeights());
      //normalize(_histMultiXiMinus       ,_weightedTotalNumXiMinus/sumOfWeights());
      //normalize(_histMultiSigma1385Plus ,_weightedTotalNumSigma1385Plus/sumOfWeights());
      //normalize(_histMultiXi1530_0      ,_weightedTotalNumXi1530_0 /sumOfWeights());
      //normalize(_histMultiRho           ,_weightedTotalNumRho/sumOfWeights());
      //normalize(_histMultiOmegaMinus    ,_weightedTotalNumOmegaMinus/sumOfWeights());
      //normalize(_histMultiKStar892_0    ,_weightedTotalNumKStar892_0/sumOfWeights());
      //normalize(_histMultiPhi           ,_weightedTotalNumPhi/sumOfWeights());

      //normalize(_histMultiKStar892Plus  ,_weightedTotalNumKStar892Plus/sumOfWeights());

      // event shape
      normalize(_hist1MinusT);
      normalize(_histTMinor);
      normalize(_histOblateness);

      normalize(_histSphericity);
      normalize(_histAplanarity);
      normalize(_histHeavyJetMass);
      normalize(_histCParam);


      // mean multiplicities
      scale(_histChMult              , 2.0/sumOfWeights()); // taking into account the binwidth of 2
      scale(_histMeanChMult          , 1.0/sumOfWeights());
      scale(_histMeanChMultRapt05    , 1.0/sumOfWeights());
      scale(_histMeanChMultRapt10    , 1.0/sumOfWeights());
      scale(_histMeanChMultRapt15    , 1.0/sumOfWeights());
      scale(_histMeanChMultRapt20    , 1.0/sumOfWeights());


      scale(_histMeanMultiPi0          , 1.0/sumOfWeights());
      scale(_histMeanMultiEta          , 1.0/sumOfWeights());
      scale(_histMeanMultiEtaPrime     , 1.0/sumOfWeights());
      scale(_histMeanMultiK0           , 1.0/sumOfWeights());
      scale(_histMeanMultiRho          , 1.0/sumOfWeights());
      scale(_histMeanMultiOmega782     , 1.0/sumOfWeights());
      scale(_histMeanMultiPhi          , 1.0/sumOfWeights());
      scale(_histMeanMultiKStar892Plus , 1.0/sumOfWeights());
      scale(_histMeanMultiKStar892_0   , 1.0/sumOfWeights());
      scale(_histMeanMultiLambda0      , 1.0/sumOfWeights());
      scale(_histMeanMultiSigma0       , 1.0/sumOfWeights());
      scale(_histMeanMultiXiMinus      , 1.0/sumOfWeights());
      scale(_histMeanMultiSigma1385Plus, 1.0/sumOfWeights());
      scale(_histMeanMultiXi1530_0     , 1.0/sumOfWeights());
      scale(_histMeanMultiOmegaOmegaBar, 1.0/sumOfWeights());
    }

    //@}


  private:
    /// Store the weighted sums of numbers of charged / charged+neutral
    /// particles - used to calculate average number of particles for the
    /// inclusive single particle distributions' normalisations.
    double _weightedTotalPartNum;
    double _weightedTotalNumPiPlus;
    double _weightedTotalNumKPlus;
    double _weightedTotalNumP;
    double _weightedTotalNumPhoton;
    double _weightedTotalNumPi0;
    double _weightedTotalNumEta;
    double _weightedTotalNumEtaPrime;
    double _weightedTotalNumK0;
    double _weightedTotalNumLambda0;
    double _weightedTotalNumXiMinus;
    double _weightedTotalNumSigma1385Plus;
    double _weightedTotalNumXi1530_0;
    double _weightedTotalNumRho;
    double _weightedTotalNumOmega782;
    double _weightedTotalNumKStar892_0;
    double _weightedTotalNumPhi;
    double _weightedTotalNumKStar892Plus;
    double _numChParticles;

    /// @name Histograms
    //@{
    AIDA::IHistogram1D *_histSphericity;
    AIDA::IHistogram1D *_histAplanarity;

    AIDA::IHistogram1D *_hist1MinusT;
    AIDA::IHistogram1D *_histTMinor;
 
    AIDA::IHistogram1D *_histY3;
    AIDA::IHistogram1D *_histHeavyJetMass;
    AIDA::IHistogram1D *_histCParam;
    AIDA::IHistogram1D *_histOblateness;
 
    AIDA::IHistogram1D *_histScaledMom;
    AIDA::IHistogram1D *_histRapidityT;

    AIDA::IHistogram1D *_histPtSIn;
    AIDA::IHistogram1D *_histPtSOut;
 
    AIDA::IHistogram1D *_histJetRate2Durham;
    AIDA::IHistogram1D *_histJetRate3Durham;
    AIDA::IHistogram1D *_histJetRate4Durham;
    AIDA::IHistogram1D *_histJetRate5Durham;

    AIDA::IHistogram1D *_histLogScaledMom;
 
 
    AIDA::IHistogram1D *_histChMult;
 

    AIDA::IHistogram1D *_histMultiPiPlus;
    AIDA::IHistogram1D *_histMultiKPlus;
    AIDA::IHistogram1D *_histMultiP;
    AIDA::IHistogram1D *_histMultiPhoton;
    AIDA::IHistogram1D *_histMultiPi0;
    AIDA::IHistogram1D *_histMultiEta;
    AIDA::IHistogram1D *_histMultiEtaPrime;
    AIDA::IHistogram1D *_histMultiK0;
    AIDA::IHistogram1D *_histMultiLambda0;
    AIDA::IHistogram1D *_histMultiXiMinus;
    AIDA::IHistogram1D *_histMultiSigma1385Plus;
    AIDA::IHistogram1D *_histMultiXi1530_0;
    AIDA::IHistogram1D *_histMultiRho;
    AIDA::IHistogram1D *_histMultiOmega782;
    AIDA::IHistogram1D *_histMultiKStar892_0;
    AIDA::IHistogram1D *_histMultiPhi;
    AIDA::IHistogram1D *_histMultiKStar892Plus;

    // mean multiplicities
    AIDA::IHistogram1D *_histMeanChMult;
    AIDA::IHistogram1D *_histMeanChMultRapt05;
    AIDA::IHistogram1D *_histMeanChMultRapt10;
    AIDA::IHistogram1D *_histMeanChMultRapt15;
    AIDA::IHistogram1D *_histMeanChMultRapt20;
 
    AIDA::IHistogram1D *_histMeanMultiPi0;
    AIDA::IHistogram1D *_histMeanMultiEta;
    AIDA::IHistogram1D *_histMeanMultiEtaPrime;
    AIDA::IHistogram1D *_histMeanMultiK0;
    AIDA::IHistogram1D *_histMeanMultiRho;
    AIDA::IHistogram1D *_histMeanMultiOmega782;
    AIDA::IHistogram1D *_histMeanMultiPhi;
    AIDA::IHistogram1D *_histMeanMultiKStar892Plus;
    AIDA::IHistogram1D *_histMeanMultiKStar892_0;
    AIDA::IHistogram1D *_histMeanMultiLambda0;
    AIDA::IHistogram1D *_histMeanMultiSigma0;
    AIDA::IHistogram1D *_histMeanMultiXiMinus;
    AIDA::IHistogram1D *_histMeanMultiSigma1385Plus;
    AIDA::IHistogram1D *_histMeanMultiXi1530_0;
    AIDA::IHistogram1D *_histMeanMultiOmegaOmegaBar;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<ALEPH_1996_S3486095> plugin_ALEPH_1996_S3486095;

}
