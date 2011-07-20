// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ZFinder.hh"

namespace Rivet {


  /// @brief CDF Z boson rapidity measurement
  class CDF_2009_S8383952 : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    CDF_2009_S8383952()
      : Analysis("CDF_2009_S8383952")
    {
      setBeams(PROTON, ANTIPROTON);
      setNeedsCrossSection(true);
    }

    //@}


  public:

    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {

      /// Initialise and register projections here
      // this seems to have been corrected completely for all selection cuts,
      // i.e. eta cuts and pT cuts on leptons.
      ZFinder zfinder(-MAXRAPIDITY, MAXRAPIDITY, 0.0*GeV, ELECTRON,
                      66.0*GeV, 116.0*GeV, 0.2, true, true);
      addProjection(zfinder, "ZFinder");


      /// Book histograms here
      _h_xs = bookHisto1D(1, 1, 1);
      _h_yZ = bookHisto1D(2, 1, 1);

    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();

      const ZFinder& zfinder = applyProjection<ZFinder>(event, "ZFinder");
      if (zfinder.particles().size() == 1) {
        double yZ = fabs(zfinder.particles()[0].momentum().rapidity());
        _h_yZ->fill(yZ, weight);
        _h_xs->fill(1960.0, weight);
      }
      else {
        getLog() << Log::DEBUG << "no unique lepton pair found." << endl;
      }

    }


    /// Normalise histograms etc., after the run
    void finalize() {
      scale(_h_xs, crossSection()/sumOfWeights());
      // Data seems to have been normalized for the avg of the two sides
      // (+ve & -ve rapidity) rather than the sum, hence the 0.5:
      scale(_h_yZ, 0.5*crossSection()/sumOfWeights());
    }

    //@}


  private:

    /// @name Histograms
    //@{
    Histo1DPtr _h_yZ;
    Histo1DPtr _h_xs;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CDF_2009_S8383952> plugin_CDF_2009_S8383952;


}
