// -*- C++ -*-
#include <iostream>
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Projections/Beam.hh"
#include "Rivet/Projections/UnstableFinalState.hh"

namespace Rivet {


  /// @brief BELLE charmed mesons and baryons from fragmentation
  /// @author Eike von Seggern
  class BELLE_2006_S6265367 : public Analysis {
  public:

    BELLE_2006_S6265367(): Analysis("BELLE_2006_S6265367")
    {
      setBeams(ELECTRON, POSITRON);
      // setNeedsCrossSection(true);
    }


    void analyze(const Event& e) {
      //
      /// @todo Apply BELLE hadron selection cuts
      //

      const double weight = e.weight();

      // Loop through unstable FS particles and look for charmed mesons/baryons
      const UnstableFinalState& ufs = applyProjection<UnstableFinalState>(e, "UFS");

      /// @todo Implement sqrtS() for asymm. beams in beam projection
      const Beam beamproj = applyProjection<Beam>(e, "Beams");
      const ParticlePair& beams = beamproj.beams();
      FourMomentum mom_tot = beams.first.momentum() + beams.second.momentum();
      LorentzTransform cms_boost(-mom_tot.boostVector());
      const double s = sqr(beamproj.sqrtS());

      const bool onresonance = true;
      // const bool onresonance = fuzzyEquals(beamproj.sqrtS(), 10.58, 1E-4);

      // Particle masses from PDGlive (accessed online 16. Nov. 2009).
      foreach (const Particle& p, ufs.particles()) {
        // TODO: Data is not corrected for branching fractions.

        double xp = 0.0;
        double mH2 = 0.0;
        // 3-momentum in CMS frame
        const double mom = cms_boost.transform(p.momentum()).vector3().mod();

        const int PdgId = abs(p.pdgId());
        getLog() << Log::DEBUG << "pdgID = " << PdgId << "  mom = " << mom << endl;

        switch (PdgId) {

          case 421:
            getLog() << Log::DEBUG << "D0 found" << endl;
            mH2 = 3.47763; // 1.86484^2
            xp = mom/sqrt(s/4.0 - mH2);
            if (onresonance)
              _histXpD0_R->fill(xp, weight);
            else
              _histXpD0_C->fill(xp, weight);
            break;

          case 411:
            getLog() << Log::DEBUG << "D+ found" << endl;
            mH2 = 3.49547; // 1.86962^2
            xp = mom/sqrt(s/4.0 - mH2);
            if (onresonance)
              _histXpDplus_R->fill(xp, weight);
            else
              _histXpDplus_C->fill(xp, weight);
            break;

          case 431:
            getLog() << Log::DEBUG << "D+_s found" << endl;
            mH2 = 3.87495; // 1.96849^2
            xp = mom/sqrt(s/4.0 - mH2);
            if (onresonance)
              _histXpDplus_s_R->fill(xp, weight);
            else
              _histXpDplus_s_C->fill(xp, weight);
            break;

          case 4122:
            getLog() << Log::DEBUG << "Lambda_c found" << endl;
            mH2 = 5.22780; // 2.28646^2
            xp = mom/sqrt(s/4.0 - mH2);
            if (onresonance)
              _histXpLambda_c_R->fill(xp, weight);
            else
              _histXpLambda_c_C->fill(xp, weight);
            break;

          case 413: {
            getLog() << Log::DEBUG << "D*+ found" << endl;
            mH2 = 4.04119; // 2.01027^2
            xp = mom/sqrt(s/4.0 - mH2);

            const GenVertex* dv = p.genParticle().end_vertex();
            bool D0decay(false), Pi0decay(false), Piplusdecay(false), Dplusdecay(false);

            for (GenVertex::particles_out_const_iterator
                     pp = dv->particles_out_const_begin();
                 pp != dv->particles_out_const_end(); ++pp) {
              if (abs((*pp)->pdg_id()) == 421) {
                D0decay = true;
              } else if (abs((*pp)->pdg_id()) == 411) {
                Dplusdecay = true;
              } else if (abs((*pp)->pdg_id()) == 111) {
                Pi0decay = true;
              } else if (abs((*pp)->pdg_id()) == 211) {
                Piplusdecay = true;
              }
            }

            if (D0decay && Piplusdecay) {
              if (onresonance)
                _histXpDstarplus2D0_R->fill(xp, weight);
              else
                _histXpDstarplus2D0_C->fill(xp, weight);
            } else if (Dplusdecay && Pi0decay) {
              if (onresonance)
                _histXpDstarplus2Dplus_R->fill(xp, weight);
              else
                _histXpDstarplus2Dplus_C->fill(xp, weight);
            } else {
              getLog() << Log::WARN << "Unexpected D* decay!" << endl;
            }
            break;
            }

          case 423:
            getLog() << Log::DEBUG << "D*0 found" << endl;
            mH2 = 4.02793; // 2.00697**2
            xp = mom/sqrt(s/4.0 - mH2);
            getLog() << Log::DEBUG << "xp = " << xp << endl;
            if (onresonance)
              _histXpDstar0_R->fill(xp, weight);
            else
              _histXpDstar0_C->fill(xp, weight);
            break;
        }

      }
    } // analyze


    void finalize() {
      // normalize(_histXpDstarplus2D0_R, crossSection());
      // normalize(_histXpD0_R, crossSection());
      // normalize(_histXpDplus_R, crossSection());
      // normalize(_histXpDplus_s_R, crossSection());
      // normalize(_histXpLambda_c_R, crossSection());
      // normalize(_histXpDstarplus2Dplus_R, crossSection());
      // normalize(_histXpDstar0_R, crossSection());

      // normalize(_histXpDstarplus2D0_C, crossSection());
      // normalize(_histXpD0_C, crossSection());
      // normalize(_histXpDplus_C, crossSection());
      // normalize(_histXpDplus_s_C, crossSection());
      // normalize(_histXpLambda_c_C, crossSection());
      // normalize(_histXpDstarplus2Dplus_C, crossSection());
      // normalize(_histXpDstar0_C, crossSection());
    } // finalize


    void init() {
      addProjection(Beam(), "Beams");
      addProjection(UnstableFinalState(-1.3170, 1.9008), "UFS");

      // histograms for continuum data (sqrt(s) = 10.52 GeV)
      _histXpDstarplus2D0_C = bookHistogram1D(2, 1, 1);
      _histXpD0_C = bookHistogram1D(3, 1, 1);
      _histXpDplus_C = bookHistogram1D(4, 1, 1);
      _histXpDplus_s_C = bookHistogram1D(5, 1, 1);
      _histXpLambda_c_C = bookHistogram1D(6, 1, 1);
      _histXpDstarplus2Dplus_C = bookHistogram1D(7, 1, 1);
      _histXpDstar0_C = bookHistogram1D(8, 1, 1);

      // histograms for on-resonance data (sqrt(s) = 10.58 GeV)
      _histXpDstarplus2D0_R = bookHistogram1D(9, 1, 1);
      _histXpD0_R = bookHistogram1D(10, 1, 1);
      _histXpDplus_R = bookHistogram1D(11, 1, 1);
      _histXpDplus_s_R = bookHistogram1D(12, 1, 1);
      _histXpLambda_c_R = bookHistogram1D(13, 1, 1);
      _histXpDstarplus2Dplus_R = bookHistogram1D(14, 1, 1);
      _histXpDstar0_R = bookHistogram1D(15, 1, 1);

    } // init

  private:

    //@{
    /// Histograms
    // histograms for continuum data (sqrt(s) = 10.52 GeV)
    AIDA::IHistogram1D* _histXpDstarplus2D0_C;
    AIDA::IHistogram1D* _histXpD0_C;
    AIDA::IHistogram1D* _histXpDplus_C;
    AIDA::IHistogram1D* _histXpDplus_s_C;
    AIDA::IHistogram1D* _histXpLambda_c_C;
    AIDA::IHistogram1D* _histXpDstarplus2Dplus_C;
    AIDA::IHistogram1D* _histXpDstar0_C;

    // histograms for on-resonance data (sqrt(s) = 10.58 GeV)
    AIDA::IHistogram1D* _histXpDstarplus2D0_R;
    AIDA::IHistogram1D* _histXpD0_R;
    AIDA::IHistogram1D* _histXpDplus_R;
    AIDA::IHistogram1D* _histXpDplus_s_R;
    AIDA::IHistogram1D* _histXpLambda_c_R;
    AIDA::IHistogram1D* _histXpDstarplus2Dplus_R;
    AIDA::IHistogram1D* _histXpDstar0_R;
    //@}
  };

  AnalysisBuilder<BELLE_2006_S6265367> plugin_BELLE_2006_S6265367;
}
