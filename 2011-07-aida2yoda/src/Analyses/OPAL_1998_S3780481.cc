// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Projections/Beam.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/InitialQuarks.hh"

namespace Rivet {


  /// @brief OPAL flavour-dependent fragmentation paper
  /// @author Hendrik Hoeth
  class OPAL_1998_S3780481 : public Analysis {
  public:

    /// Constructor
    OPAL_1998_S3780481() : Analysis("OPAL_1998_S3780481")
    {
      setBeams(ELECTRON, POSITRON);

      // Counters
      _weightedTotalPartNum = 0;
      _SumOfudsWeights = 0;
      _SumOfcWeights = 0;
      _SumOfbWeights = 0;
    }


    /// @name Analysis methods
    //@{

    void analyze(const Event& e) {
      // First, veto on leptonic events by requiring at least 4 charged FS particles
      const FinalState& fs = applyProjection<FinalState>(e, "FS");
      const size_t numParticles = fs.particles().size();

      // Even if we only generate hadronic events, we still need a cut on numCharged >= 2.
      if (numParticles < 2) {
        getLog() << Log::DEBUG << "Failed ncharged cut" << endl;
        vetoEvent;
      }
      getLog() << Log::DEBUG << "Passed ncharged cut" << endl;

      // Get event weight for histo filling
      const double weight = e.weight();
      _weightedTotalPartNum += numParticles * weight;

      // Get beams and average beam momentum
      const ParticlePair& beams = applyProjection<Beam>(e, "Beams").beams();
      const double meanBeamMom = ( beams.first.momentum().vector3().mod() +
                                   beams.second.momentum().vector3().mod() ) / 2.0;
      getLog() << Log::DEBUG << "Avg beam momentum = " << meanBeamMom << endl;

      int flavour = 0;
      const InitialQuarks& iqf = applyProjection<InitialQuarks>(e, "IQF");

      // If we only have two quarks (qqbar), just take the flavour.
      // If we have more than two quarks, look for the highest energetic q-qbar pair.
      if (iqf.particles().size() == 2) {
        flavour = abs( iqf.particles().front().pdgId() );
      }
      else {
        map<int, double> quarkmap;
        foreach (const Particle& p, iqf.particles()) {
          if (quarkmap[p.pdgId()] < p.momentum().E()) {
            quarkmap[p.pdgId()] = p.momentum().E();
          }
        }
        double maxenergy = 0.;
        for (int i = 1; i <= 5; ++i) {
          if (quarkmap[i]+quarkmap[-i] > maxenergy) {
            flavour = i;
          }
        }
      }

      switch (flavour) {
      case 1:
      case 2:
      case 3:
        _SumOfudsWeights += weight;
        break;
      case 4:
        _SumOfcWeights += weight;
        break;
      case 5:
        _SumOfbWeights += weight;
        break;
      }

      foreach (const Particle& p, fs.particles()) {
        const double xp = p.momentum().vector3().mod()/meanBeamMom;
        const double logxp = -std::log(xp);
        _histXpall->fill(xp, weight);
        _histLogXpall->fill(logxp, weight);
        _histMultiChargedall->fill(_histMultiChargedall->binMean(0), weight);
        switch (flavour) {
          /// @todo Use PDG code enums
        case DQUARK:
        case UQUARK:
        case SQUARK:
          _histXpuds->fill(xp, weight);
          _histLogXpuds->fill(logxp, weight);
          _histMultiChargeduds->fill(_histMultiChargeduds->binMean(0), weight);
          break;
        case CQUARK:
          _histXpc->fill(xp, weight);
          _histLogXpc->fill(logxp, weight);
          _histMultiChargedc->fill(_histMultiChargedc->binMean(0), weight);
          break;
        case BQUARK:
          _histXpb->fill(xp, weight);
          _histLogXpb->fill(logxp, weight);
          _histMultiChargedb->fill(_histMultiChargedb->binMean(0), weight);
          break;
        }
      }

    }


    void init() {
      // Projections
      addProjection(Beam(), "Beams");
      addProjection(ChargedFinalState(), "FS");
      addProjection(InitialQuarks(), "IQF");

      // Book histos
      _histXpuds           = bookHistogram1D(1, 1, 1);
      _histXpc             = bookHistogram1D(2, 1, 1);
      _histXpb             = bookHistogram1D(3, 1, 1);
      _histXpall           = bookHistogram1D(4, 1, 1);
      _histLogXpuds        = bookHistogram1D(5, 1, 1);
      _histLogXpc          = bookHistogram1D(6, 1, 1);
      _histLogXpb          = bookHistogram1D(7, 1, 1);
      _histLogXpall        = bookHistogram1D(8, 1, 1);
      _histMultiChargeduds = bookHistogram1D(9, 1, 1);
      _histMultiChargedc   = bookHistogram1D(9, 1, 2);
      _histMultiChargedb   = bookHistogram1D(9, 1, 3);
      _histMultiChargedall = bookHistogram1D(9, 1, 4);
    }


    /// Finalize
    void finalize() {
      const double avgNumParts = _weightedTotalPartNum / sumOfWeights();
      normalize(_histXpuds    , avgNumParts);
      normalize(_histXpc      , avgNumParts);
      normalize(_histXpb      , avgNumParts);
      normalize(_histXpall    , avgNumParts);
      normalize(_histLogXpuds , avgNumParts);
      normalize(_histLogXpc   , avgNumParts);
      normalize(_histLogXpb   , avgNumParts);
      normalize(_histLogXpall , avgNumParts);

      scale(_histMultiChargeduds, 1.0/_SumOfudsWeights);
      scale(_histMultiChargedc  , 1.0/_SumOfcWeights);
      scale(_histMultiChargedb  , 1.0/_SumOfbWeights);
      scale(_histMultiChargedall, 1.0/sumOfWeights());
    }

    //@}


  private:

    /// Store the weighted sums of numbers of charged / charged+neutral
    /// particles - used to calculate average number of particles for the
    /// inclusive single particle distributions' normalisations.
    double _weightedTotalPartNum;

    double _SumOfudsWeights;
    double _SumOfcWeights;
    double _SumOfbWeights;

    AIDA::IHistogram1D *_histXpuds;
    AIDA::IHistogram1D *_histXpc;
    AIDA::IHistogram1D *_histXpb;
    AIDA::IHistogram1D *_histXpall;
    AIDA::IHistogram1D *_histLogXpuds;
    AIDA::IHistogram1D *_histLogXpc;
    AIDA::IHistogram1D *_histLogXpb;
    AIDA::IHistogram1D *_histLogXpall;
    AIDA::IHistogram1D *_histMultiChargeduds;
    AIDA::IHistogram1D *_histMultiChargedc;
    AIDA::IHistogram1D *_histMultiChargedb;
    AIDA::IHistogram1D *_histMultiChargedall;

    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<OPAL_1998_S3780481> plugin_OPAL_1998_S3780481;

}
