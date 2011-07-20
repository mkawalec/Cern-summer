// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Projections/LeadingParticlesFinalState.hh"
#include "Rivet/Projections/VetoedFinalState.hh"

namespace Rivet {


  /// @brief D0 Run I differential W/Z boson cross-section analysis
  /// @author Lars Sonnenschein
  class D0_2001_S4674421 : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor.
    D0_2001_S4674421() : Analysis("D0_2001_S4674421") {
      setBeams(PROTON, ANTIPROTON);
      setNeedsCrossSection(true);
    }
 
 
    /// @name Analysis methods
    //@{
 
    void init() {
      // Final state projection
      FinalState fs(-5.0, 5.0); // corrected for detector acceptance
      addProjection(fs, "FS");

      // Z -> e- e+
      LeadingParticlesFinalState eeFS(FinalState(-2.5, 2.5, 0.)); //20.);
      eeFS.addParticleIdPair(ELECTRON);
      addProjection(eeFS, "eeFS");
   
      // W- -> e- nu_e~
      LeadingParticlesFinalState enuFS(FinalState(-2.5, 2.5, 0.)); //25.);
      enuFS.addParticleId(ELECTRON).addParticleId(NU_EBAR);
      addProjection(enuFS, "enuFS");
   
      // W+ -> e+ nu_e
      LeadingParticlesFinalState enubFS(FinalState(-2.5, 2.5, 0.)); //25.);
      enubFS.addParticleId(POSITRON).addParticleId(NU_E);
      addProjection(enubFS, "enubFS");

      // Remove neutrinos for isolation of final state particles
      VetoedFinalState vfs(fs);
      vfs.vetoNeutrinos();
      addProjection(vfs, "VFS");

      // Counters
      _eventsFilledW = 0.0;
      _eventsFilledZ = 0.0;

      // Histograms
      _h_dsigdpt_w = bookHisto1D(1, 1, 1);
      _h_dsigdpt_z = bookHisto1D(1, 1, 2);
      _h_dsigdpt_scaled_z = bookScatter2D(2, 1, 1);
    }



    void analyze(const Event& event) {
      const double weight = event.weight();

      const LeadingParticlesFinalState& eeFS = applyProjection<LeadingParticlesFinalState>(event, "eeFS");
      if (eeFS.particles().size() == 2) {
        // If there is a Z candidate:
        static size_t Zcount = 0;
        // Fill Z pT distributions
        const ParticleVector& Zdaughters = eeFS.particles();
        const FourMomentum pmom = Zdaughters[0].momentum() + Zdaughters[1].momentum();
        double mass = sqrt(pmom.invariant());
        if (inRange(mass/GeV, 75.0, 105.0)) {
          ++Zcount;
          _eventsFilledZ += weight;
          //getLog() << Log::DEBUG << "Z #" << Zcount << " pmom.pT() = " << pmom.pT()/GeV << " GeV" << endl;
          _h_dsigdpt_z->fill(pmom.pT()/GeV, weight);
        }
      } else {
        // There is no Z -> ee candidate... so this must be a W event, right?
        const LeadingParticlesFinalState& enuFS = applyProjection<LeadingParticlesFinalState>(event, "enuFS");
        const LeadingParticlesFinalState& enubFS = applyProjection<LeadingParticlesFinalState>(event, "enubFS");
        static size_t Wcount = 0;

        // Fill W pT distributions
        ParticleVector Wdaughters;
        if (enuFS.particles().size() == 2 && enubFS.empty()) {
          Wdaughters = enuFS.particles();
        } else if (enuFS.empty() && enubFS.particles().size() == 2) {
          Wdaughters = enubFS.particles();
        }
        if (! Wdaughters.empty()) {
          assert(Wdaughters.size() == 2);
          const FourMomentum pmom = Wdaughters[0].momentum() + Wdaughters[1].momentum();
          ++Wcount;
          _eventsFilledW += weight;
          _h_dsigdpt_w->fill(pmom.pT()/GeV, weight);
        }
      }
    }



    void finalize() {
      // Get cross-section per event (i.e. per unit weight) from generator
      const double xSecPerEvent = crossSectionPerEvent()/picobarn;

      // Correct W pT distribution to W cross-section
      const double xSecW = xSecPerEvent * _eventsFilledW;

      // Correct Z pT distribution to Z cross-section
      const double xSecZ = xSecPerEvent * _eventsFilledZ;

      // Get W and Z pT integrals
      const double wpt_integral = integral(_h_dsigdpt_w);
      const double zpt_integral = integral(_h_dsigdpt_z);

      // Divide and scale ratio histos
      if (xSecW == 0 || wpt_integral == 0 || xSecZ == 0 || zpt_integral == 0) {
        getLog() << Log::WARN << "Not filling ratio plot because input histos are empty" << endl;
      } else {
        // Scale factor converts event counts to cross-sections, and inverts the
        // branching ratios since only one decay channel has been analysed for each boson.
        // Oh, and we put MW/MZ in, like they do in the paper.
        const double MW_MZ = 0.8820; // Ratio M_W/M_Z
        const double BRZEE_BRWENU = 0.033632 / 0.1073; // Ratio of branching fractions
        const double scalefactor = (xSecW / wpt_integral) / (xSecZ / zpt_integral) * MW_MZ * BRZEE_BRWENU;
        for (size_t ibin=0; ibin<_h_dsigdpt_scaled_z->numPoints(); ibin++) {
          if (_h_dsigdpt_w->bin(ibin).area() == 0 || _h_dsigdpt_z->bin(ibin).area() == 0) {
	    _h_dsigdpt_scaled_z->point(ibin) = Point2D(_h_dsigdpt_w->bin(ibin).midpoint(), 0.,
						       _h_dsigdpt_w->bin(ibin).width(), 0.);
          } else {
	    double yval = scalefactor * _h_dsigdpt_w->bin(ibin).area() / _h_dsigdpt_z->bin(ibin).area();
            double dy2 = 0.;
            // binWidth(ibin) is needed because binHeight is actually sumofweights. It's AIDA. Don't ask.  :-((((
            dy2 += pow(_h_dsigdpt_w->bin(ibin).areaError()/_h_dsigdpt_w->bin(ibin).height(),2);
            dy2 += pow(_h_dsigdpt_z->bin(ibin).areaError()/_h_dsigdpt_z->bin(ibin).height(),2);
            double dy = scalefactor * _h_dsigdpt_w->bin(ibin).area()/_h_dsigdpt_z->bin(ibin).area() * sqrt(dy2);

	    _h_dsigdpt_scaled_z->point(ibin) = Point2D(_h_dsigdpt_w->bin(ibin).midpoint(), yval,
						       _h_dsigdpt_w->bin(ibin).width(), dy);
          }
        }
      }

      // Normalize non-ratio histos
      normalize(_h_dsigdpt_w, xSecW);
      normalize(_h_dsigdpt_z, xSecZ);

    }


    //@}
 
  private:

    /// @name Event counters for cross section normalizations
    //@{
    double _eventsFilledW;
    double _eventsFilledZ;
    //@}

    //@{
    /// Histograms
    Histo1DPtr  _h_dsigdpt_w;
    Histo1DPtr  _h_dsigdpt_z;
    Scatter2DPtr _h_dsigdpt_scaled_z;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<D0_2001_S4674421> plugin_D0_2001_S4674421;

}
