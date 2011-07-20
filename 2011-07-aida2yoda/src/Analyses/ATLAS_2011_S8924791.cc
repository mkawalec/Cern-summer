// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Projections/VisibleFinalState.hh"
#include "Rivet/Projections/JetShape.hh"

namespace Rivet {


  /// @brief ATLAS jet shape analysis
  /// @author Andy Buckley, Judith Katzy, Francesc Vives
  class ATLAS_2011_S8924791 : public Analysis {
  public:

    /// Constructor
    ATLAS_2011_S8924791()
      : Analysis("ATLAS_2011_S8924791")
    {
      setBeams(PROTON, PROTON);
    }


    /// @name Analysis methods
    //@{

    void init() {
      // Set up projections
      const FinalState fs(-5.0, 5.0);
      addProjection(fs, "FS");
      FastJets fj(fs, FastJets::ANTIKT, 0.6);
      fj.useInvisibles();
      addProjection(fj, "Jets");

      // Specify pT bins
      _ptedges += 30.0, 40.0, 60.0, 80.0, 110.0, 160.0, 210.0, 260.0, 310.0, 400.0, 500.0, 600.0;
      _yedges  += 0.0, 0.3, 0.8, 1.2, 2.1, 2.8;


      // Register a jet shape projection and histogram for each pT bin
      for (size_t i = 0; i < 11; ++i) {
        for (size_t j = 0; j < 6; ++j) {
          if (i==8 && j==4) continue;
          if (i==9 && j==4) continue;
          if (i==10 && j!=5) continue;
          stringstream ss; ss << "JetShape" << i << j;
          const string pname = ss.str();
          _jsnames_pT[i][j] = pname;

          if (j < 5) {
            const JetShape jsp(fj, 0.0, 0.7, 7, _ptedges[i], _ptedges[i+1], _yedges[j], _yedges[j+1], RAPIDITY);
            addProjection(jsp, pname);
          } else {
            const JetShape jsp(fj, 0.0, 0.7, 7, _ptedges[i], _ptedges[i+1], _yedges.front(), _yedges.back(), RAPIDITY);
            addProjection(jsp, pname);
          }
          _profhistRho_pT[i][j] = bookProfile1D(i+1, j+1, 1);
          _profhistPsi_pT[i][j] = bookProfile1D(i+1, j+1, 2);
        }
      }
    }



    /// Do the analysis
    void analyze(const Event& evt) {

      // Get jets and require at least one to pass pT and y cuts
      const Jets jets = applyProjection<FastJets>(evt, "Jets").jetsByPt(_ptedges.front()*GeV, _ptedges.back()*GeV,
                                                                        -2.8, 2.8, RAPIDITY);
      MSG_DEBUG("Jet multiplicity before cuts = " << jets.size());
      if (jets.size() == 0) {
        MSG_DEBUG("No jets found in required pT & rapidity range");
        vetoEvent;
      }
      // Calculate and histogram jet shapes
      const double weight = evt.weight();

      for (size_t ipt = 0; ipt < 11; ++ipt) {
        for (size_t jy = 0; jy < 6; ++jy) {
          if (ipt==8 && jy==4) continue;
          if (ipt==9 && jy==4) continue;
          if (ipt==10 && jy!=5) continue;
          const JetShape& jsipt = applyProjection<JetShape>(evt, _jsnames_pT[ipt][jy]);
          for (size_t ijet = 0; ijet < jsipt.numJets(); ++ijet) {
            for (size_t rbin = 0; rbin < jsipt.numBins(); ++rbin) {
              const double r_rho = jsipt.rBinMid(rbin);
              _profhistRho_pT[ipt][jy]->fill(r_rho, (1./0.1)*jsipt.diffJetShape(ijet, rbin), weight);
              const double r_Psi = jsipt.rBinMid(rbin);
              _profhistPsi_pT[ipt][jy]->fill(r_Psi, jsipt.intJetShape(ijet, rbin), weight);
            }
          }
        }
      }
    }


    // Finalize
    void finalize() {
    }

    //@}


  private:

    /// @name Analysis data
    //@{

    /// Jet \f$ p_\perp\f$ bins.
    vector<double> _ptedges; // This can't be a raw array if we want to initialise it non-painfully
    vector<double> _yedges;

    /// JetShape projection name for each \f$p_\perp\f$ bin.
    string _jsnames_pT[11][6];

    //@}

    /// @name Histograms
    //@{
    Profile1DPtr _profhistRho_pT[11][6];
    Profile1DPtr _profhistPsi_pT[11][6];
    //@}

  };


  // This global object acts as a hook for the plugin system
  AnalysisBuilder<ATLAS_2011_S8924791> plugin_ATLAS_2011_S8924791;

}
