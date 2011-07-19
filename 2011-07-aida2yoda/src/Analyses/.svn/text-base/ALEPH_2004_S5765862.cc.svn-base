// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/Thrust.hh"
#include "Rivet/Projections/Sphericity.hh"
#include "Rivet/Projections/ParisiTensor.hh"
#include "Rivet/Projections/Hemispheres.hh"
#include "Rivet/Projections/Beam.hh"

namespace Rivet {


  /// @brief ALEPH jet rates and event shapes at LEP 1 and 2
  class ALEPH_2004_S5765862 : public Analysis {
  public:

    ALEPH_2004_S5765862()
      : Analysis("ALEPH_2004_S5765862") , _initialisedJets(false),
        _initialisedSpectra(false), _weightedTotalChargedPartNum(0)
    {
      setBeams(ELECTRON, POSITRON);
    }


  public:

    void init() {
      _initialisedJets    = true;
      _initialisedSpectra = true;
      // TODO: According to the paper they seem to discard neutral particles
      //       between 1 and 2 GeV. That correction is included in the systematic
      //       uncertainties and overly complicated to program, so we ignore it.
      const FinalState fs;
      addProjection(fs, "FS");
      FastJets durhamjets(fs, FastJets::DURHAM, 0.7);
      durhamjets.useInvisibles(true);
      addProjection(durhamjets, "DurhamJets");

      const Thrust thrust(fs);
      addProjection(thrust, "Thrust");
      addProjection(Sphericity(fs), "Sphericity");
      addProjection(ParisiTensor(fs), "Parisi");
      addProjection(Hemispheres(thrust), "Hemispheres");

      const ChargedFinalState cfs;
      addProjection(Beam(), "Beams");
      addProjection(cfs, "CFS");

      // Histos
      // offset for the event shapes and jets
      int offset = 0;
      switch (int(sqrtS()/GeV + 0.5)) {
      case 91: offset = 0; break;
      case 133: offset = 1; break;
      case 161: offset = 2; break;
      case 172: offset = 3; break;
      case 183: offset = 4; break;
      case 189: offset = 5; break;
      case 200: offset = 6; break;
      case 206: offset = 7; break;
      default:
        _initialisedJets = false;
      }
      // event shapes
      if(_initialisedJets) {
        _h_thrust = bookHistogram1D(offset+54, 1, 1);
        _h_heavyjetmass = bookHistogram1D(offset+62, 1, 1);
        _h_totaljetbroadening = bookHistogram1D(offset+70, 1, 1);
        _h_widejetbroadening = bookHistogram1D(offset+78, 1, 1);
        _h_cparameter = bookHistogram1D(offset+86, 1, 1);
        _h_thrustmajor = bookHistogram1D(offset+94, 1, 1);
        _h_thrustminor = bookHistogram1D(offset+102, 1, 1);
        _h_jetmassdifference = bookHistogram1D(offset+110, 1, 1);
        _h_aplanarity = bookHistogram1D(offset+118, 1, 1);
        _h_planarity  = offset==0 ? NULL : bookHistogram1D(offset+125, 1, 1);
        _h_oblateness = bookHistogram1D(offset+133, 1, 1);
        _h_sphericity = bookHistogram1D(offset+141, 1, 1);

        // Durham n->m jet resolutions
        _h_y_Durham[0] = bookHistogram1D(offset+149, 1, 1);   // y12 d149 ... d156
        _h_y_Durham[1] = bookHistogram1D(offset+157, 1, 1);   // y23 d157 ... d164
        if (offset<6) { // there is no y34, y45 and y56 for 200 gev
          _h_y_Durham[2] = bookHistogram1D(offset+165, 1, 1); // y34 d165 ... d172, but not 171
          _h_y_Durham[3] = bookHistogram1D(offset+173, 1, 1); // y45 d173 ... d179
          _h_y_Durham[4] = bookHistogram1D(offset+180, 1, 1); // y56 d180 ... d186
        }
        else if (offset==6) {
          _h_y_Durham[2] = NULL;
          _h_y_Durham[3] = NULL;
          _h_y_Durham[4] = NULL;
        }
        else if (offset==7) {
          _h_y_Durham[2] = bookHistogram1D(172, 1, 1);
          _h_y_Durham[3] = bookHistogram1D(179, 1, 1);
          _h_y_Durham[4] = bookHistogram1D(186, 1, 1);
        }

        // Durham n-jet fractions
        _h_R_Durham[0] = bookDataPointSet(offset+187, 1, 1); // R1 d187 ... d194
        _h_R_Durham[1] = bookDataPointSet(offset+195, 1, 1); // R2 d195 ... d202
        _h_R_Durham[2] = bookDataPointSet(offset+203, 1, 1); // R3 d203 ... d210
        _h_R_Durham[3] = bookDataPointSet(offset+211, 1, 1); // R4 d211 ... d218
        _h_R_Durham[4] = bookDataPointSet(offset+219, 1, 1); // R5 d219 ... d226
        _h_R_Durham[5] = bookDataPointSet(offset+227, 1, 1); // R>=6 d227 ... d234
      }
      // offset for the charged particle distributions
      offset = 0;
      switch (int(sqrtS()/GeV + 0.5)) {
      case 133: offset = 0; break;
      case 161: offset = 1; break;
      case 172: offset = 2; break;
      case 183: offset = 3; break;
      case 189: offset = 4; break;
      case 196: offset = 5; break;
      case 200: offset = 6; break;
      case 206: offset = 7; break;
      default:
        _initialisedSpectra=false;
      }
      if(_initialisedSpectra) {
        _h_xp = bookHistogram1D( 2+offset, 1, 1);
        _h_xi = bookHistogram1D(11+offset, 1, 1);
        _h_xe = bookHistogram1D(19+offset, 1, 1);
        _h_pTin  = bookHistogram1D(27+offset, 1, 1);
        _h_pTout = offset!=7 ? NULL : bookHistogram1D(35, 1, 1);
        _h_rapidityT = bookHistogram1D(36+offset, 1, 1);
        _h_rapidityS = bookHistogram1D(44+offset, 1, 1);
      }

      if(!_initialisedSpectra && !_initialisedJets) {
        getLog() << Log::WARNING
                 << "CMS energy of events sqrt(s) = " << sqrtS()/GeV
                 <<" doesn't match any available analysis energy ." << endl;
      }
    }


    void analyze(const Event& e) {
      const double weight = e.weight();

      const Thrust& thrust = applyProjection<Thrust>(e, "Thrust");
      const Sphericity& sphericity = applyProjection<Sphericity>(e, "Sphericity");

      if(_initialisedJets) {
        bool LEP1 = fuzzyEquals(sqrtS(),91.2*GeV,0.01);
        // event shapes
        double thr = LEP1 ? thrust.thrust() : 1.0 - thrust.thrust();
        _h_thrust->fill(thr,weight);
        _h_thrustmajor->fill(thrust.thrustMajor(),weight);
        if(LEP1)
          _h_thrustminor->fill(log(thrust.thrustMinor()),weight);
        else
          _h_thrustminor->fill(thrust.thrustMinor(),weight);
        _h_oblateness->fill(thrust.oblateness(),weight);

        const Hemispheres& hemi = applyProjection<Hemispheres>(e, "Hemispheres");
        _h_heavyjetmass->fill(hemi.scaledM2high(),weight);
        _h_jetmassdifference->fill(hemi.scaledM2diff(),weight);
        _h_totaljetbroadening->fill(hemi.Bsum(),weight);
        _h_widejetbroadening->fill(hemi.Bmax(),weight);

        const ParisiTensor& parisi = applyProjection<ParisiTensor>(e, "Parisi");
        _h_cparameter->fill(parisi.C(),weight);

        _h_aplanarity->fill(sphericity.aplanarity(),weight);
        if(_h_planarity)
          _h_planarity->fill(sphericity.planarity(),weight);
        _h_sphericity->fill(sphericity.sphericity(),weight);

        // Jet rates
        const FastJets& durjet = applyProjection<FastJets>(e, "DurhamJets");
        double log10e = log10(exp(1.));
        if (durjet.clusterSeq()) {
          double logynm1=0.;
          double logyn;
          for (size_t i=0; i<5; ++i) {
            logyn = -log(durjet.clusterSeq()->exclusive_ymerge_max(i+1));
            if (_h_y_Durham[i]) {
              _h_y_Durham[i]->fill(logyn, weight);
            }
            if(!LEP1) logyn *= log10e;
            for (int j = 0; j < _h_R_Durham[i]->size(); ++j) {
              IDataPoint* dp = _h_R_Durham[i]->point(j);
              double val = -dp->coordinate(0)->value()+dp->coordinate(0)->errorMinus();
              if(val<=logynm1) break;
              if(val<logyn) {
                dp->coordinate(1)->setValue(dp->coordinate(1)->value()+weight);
              }
            }
            logynm1 = logyn;
          }
          for (int j = 0; j < _h_R_Durham[5]->size(); ++j) {
            IDataPoint* dp = _h_R_Durham[5]->point(j);
            double val = -dp->coordinate(0)->value()+dp->coordinate(0)->errorMinus();
            if(val<=logynm1) break;
            dp->coordinate(1)->setValue(dp->coordinate(1)->value()+weight);
          }
        }
        if( !_initialisedSpectra) {
          const ChargedFinalState& cfs = applyProjection<ChargedFinalState>(e, "CFS");
          const size_t numParticles = cfs.particles().size();
          _weightedTotalChargedPartNum += numParticles * weight;
        }
      }

      // charged particle distributions
      if(_initialisedSpectra) {
        const ChargedFinalState& cfs = applyProjection<ChargedFinalState>(e, "CFS");
        const size_t numParticles = cfs.particles().size();
        _weightedTotalChargedPartNum += numParticles * weight;
        const ParticlePair& beams = applyProjection<Beam>(e, "Beams").beams();
        const double meanBeamMom = ( beams.first.momentum().vector3().mod() +
                                     beams.second.momentum().vector3().mod() ) / 2.0;
        foreach (const Particle& p, cfs.particles()) {
          const double xp = p.momentum().vector3().mod()/meanBeamMom;
          _h_xp->fill(xp   , weight);
          const double logxp = -std::log(xp);
          _h_xi->fill(logxp, weight);
          const double xe = p.momentum().E()/meanBeamMom;
          _h_xe->fill(xe   , weight);
          const double pTinT  = dot(p.momentum().vector3(), thrust.thrustMajorAxis());
          const double pToutT = dot(p.momentum().vector3(), thrust.thrustMinorAxis());
          _h_pTin->fill(fabs(pTinT/GeV), weight);
          if(_h_pTout) _h_pTout->fill(fabs(pToutT/GeV), weight);
          const double momT = dot(thrust.thrustAxis()        ,p.momentum().vector3());
          const double rapidityT = 0.5 * std::log((p.momentum().E() + momT) /
                                                  (p.momentum().E() - momT));
          _h_rapidityT->fill(rapidityT, weight);
          const double momS = dot(sphericity.sphericityAxis(),p.momentum().vector3());
          const double rapidityS = 0.5 * std::log((p.momentum().E() + momS) /
                                                  (p.momentum().E() - momS));
          _h_rapidityS->fill(rapidityS, weight);
        }
      }
    }

    void finalize() {
      if(!_initialisedJets && !_initialisedSpectra) return;

      if (_initialisedJets) {
        normalize(_h_thrust);
        normalize(_h_heavyjetmass);
        normalize(_h_totaljetbroadening);
        normalize(_h_widejetbroadening);
        normalize(_h_cparameter);
        normalize(_h_thrustmajor);
        normalize(_h_thrustminor);
        normalize(_h_jetmassdifference);
        normalize(_h_aplanarity);
        if(_h_planarity) normalize(_h_planarity);
        normalize(_h_oblateness);
        normalize(_h_sphericity);

        for (size_t N=1; N<7; ++N) {
          for (int i = 0; i < _h_R_Durham[N-1]->size(); ++i) {
            _h_R_Durham[N-1]->point(i)->coordinate(1)->
              setValue(_h_R_Durham[N-1]->point(i)->coordinate(1)->value()/sumOfWeights());
          }
        }

        for (size_t n = 0; n < 5; ++n) {
          if (_h_y_Durham[n]) {
            scale(_h_y_Durham[n], 1.0/sumOfWeights());
          }
        }
      }

      const double avgNumParts = _weightedTotalChargedPartNum / sumOfWeights();
      AIDA::IDataPointSet * mult = bookDataPointSet(1, 1, 1);
      for (int i = 0; i < mult->size(); ++i) {
        if (fuzzyEquals(sqrtS(), mult->point(i)->coordinate(0)->value(), 0.01)) {
          mult->point(i)->coordinate(1)->setValue(avgNumParts);
        }
      }

      if (_initialisedSpectra) {
        normalize(_h_xp, avgNumParts);
        normalize(_h_xi, avgNumParts);
        normalize(_h_xe, avgNumParts);
        normalize(_h_pTin , avgNumParts);
        if (_h_pTout) normalize(_h_pTout, avgNumParts);
        normalize(_h_rapidityT, avgNumParts);
        normalize(_h_rapidityS, avgNumParts);
      }
    }

  private:

    bool _initialisedJets;
    bool _initialisedSpectra;

    AIDA::IHistogram1D *_h_xp;
    AIDA::IHistogram1D *_h_xi;
    AIDA::IHistogram1D *_h_xe;
    AIDA::IHistogram1D *_h_pTin;
    AIDA::IHistogram1D *_h_pTout;
    AIDA::IHistogram1D *_h_rapidityT;
    AIDA::IHistogram1D *_h_rapidityS;
    AIDA::IHistogram1D *_h_thrust;
    AIDA::IHistogram1D *_h_heavyjetmass;
    AIDA::IHistogram1D *_h_totaljetbroadening;
    AIDA::IHistogram1D *_h_widejetbroadening;
    AIDA::IHistogram1D *_h_cparameter;
    AIDA::IHistogram1D *_h_thrustmajor;
    AIDA::IHistogram1D *_h_thrustminor;
    AIDA::IHistogram1D *_h_jetmassdifference;
    AIDA::IHistogram1D *_h_aplanarity;
    AIDA::IHistogram1D *_h_planarity;
    AIDA::IHistogram1D *_h_oblateness;
    AIDA::IHistogram1D *_h_sphericity;

    AIDA::IDataPointSet *_h_R_Durham[6];
    AIDA::IHistogram1D *_h_y_Durham[5];

    double _weightedTotalChargedPartNum;

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<ALEPH_2004_S5765862> plugin_ALEPH_2004_S5765862;


}
