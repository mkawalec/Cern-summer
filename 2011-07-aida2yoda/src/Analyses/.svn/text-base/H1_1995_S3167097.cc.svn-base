// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Projections/FinalStateHCM.hh"
#include "Rivet/Projections/CentralEtHCM.hh"

namespace Rivet {


  /// @brief H1 energy flow in DIS
  /// @todo Check this analysis!
  /// @author Leif Lonnblad
  class H1_1995_S3167097 : public Analysis {
  public:

    /// Constructor
    H1_1995_S3167097() : Analysis("H1_1995_S3167097")
    {
      setBeams(ELECTRON, PROTON);
    }


    /// @name Analysis methods
    //@{

    void init() {
      const DISKinematics& diskin = addProjection(DISKinematics(), "Kinematics");
      const FinalStateHCM& fshcm = addProjection(FinalStateHCM(diskin), "FS");
      addProjection(CentralEtHCM(fshcm), "Y1HCM");

      _hEtFlow = vector<Histo1DPtr>(_nbin);
      _hEtFlowStat = vector<Histo1DPtr>(_nbin);
      _nev = vector<double>(_nbin);
      /// @todo Automate this sort of thing so that the analysis code is more readable.
      for (size_t i = 0; i < _nbin; ++i) {
        string istr(1, char('1' + i));
        _hEtFlow[i] = bookHisto1D(istr, _nb, _xmin, _xmax);
        _hEtFlowStat[i] = bookHisto1D(istr, _nb, _xmin, _xmax);
      }
      _hAvEt = bookHisto1D("21tmp", _nbin, 1.0, 10.0);
      _hAvX  = bookHisto1D("22tmp", _nbin, 1.0, 10.0);
      _hAvQ2 = bookHisto1D("23tmp", _nbin, 1.0, 10.0);
      _hN    = bookHisto1D("24", _nbin, 1.0, 10.0);
    }


    /// Calculate the bin number from the DISKinematics projection
    int _getbin(const DISKinematics& dk) {
      if ( dk.Q2() > 5.0*GeV2 && dk.Q2() <= 10.0*GeV2 ) {
        if ( dk.x() > 0.0001 && dk.x() <= 0.0002 )
          return 0;
        else if ( dk.x() > 0.0002 && dk.x() <= 0.0005 && dk.Q2() > 6.0*GeV2 )
          return 1;
      }
      else if ( dk.Q2() > 10.0*GeV2 && dk.Q2() <= 20.0*GeV2 ){
        if ( dk.x() > 0.0002 && dk.x() <= 0.0005 )
          return 2;
        else if ( dk.x() > 0.0005 && dk.x() <= 0.0008 )
          return 3;
        else if ( dk.x() > 0.0008 && dk.x() <= 0.0015 )
          return 4;
        else if ( dk.x() > 0.0015 && dk.x() <= 0.0040 )
          return 5;
      }
      else if ( dk.Q2() > 20.0*GeV2 && dk.Q2() <= 50.0*GeV2 ){
        if ( dk.x() > 0.0005 && dk.x() <= 0.0014 )
          return 6;
        else if ( dk.x() > 0.0014 && dk.x() <= 0.0030 )
          return 7;
        else if ( dk.x() > 0.0030 && dk.x() <= 0.0100 )
          return 8;
      }
      return -1;
    }


    void analyze(const Event& event) {
      const FinalStateHCM& fs = applyProjection<FinalStateHCM>(event, "FS");
      const DISKinematics& dk = applyProjection<DISKinematics>(event, "Kinematics");
      const CentralEtHCM y1 = applyProjection<CentralEtHCM>(event, "Y1HCM");

      const int ibin = _getbin(dk);
      if (ibin < 0) vetoEvent;
      const double weight = event.weight();

      for (size_t i = 0, N = fs.particles().size(); i < N; ++i) {
        const double rap = fs.particles()[i].momentum().rapidity();
        const double et = fs.particles()[i].momentum().Et();
        _hEtFlow[ibin]->fill(rap, weight * et/GeV);
        _hEtFlowStat[ibin]->fill(rap, weight * et/GeV);
      }

      _nev[ibin] += weight;
      _hAvEt->fill(ibin + 1.5, weight * y1.sumEt()/GeV);
      _hAvX->fill(ibin + 1.5, weight * dk.x());
      _hAvQ2->fill(ibin + 1.5, weight * dk.Q2()/GeV2);
      _hN->fill(ibin + 1.5, weight);
    }


    void finalize() {
      for (size_t ibin = 0; ibin < _nbin; ++ibin) {
        scale( _hEtFlow[ibin], 1.0/(_nev[ibin]*double(_nb)/(_xmax-_xmin)));
        scale( _hEtFlowStat[ibin], 1.0/(_nev[ibin]*double(_nb)/(_xmax-_xmin)));
      }

      /// @todo Automate this sort of thing so that the analysis code is more readable.
      // \todo YODA divide
      // Scatter2DPtr h;
      // h = histogramFactory().divide("/H1_1995_S3167097/21", *_hAvEt, *_hN);
      // h->setTitle(_hAvEt->title());
      // histogramFactory().destroy(_hAvEt);

      // h = histogramFactory().divide("/H1_1995_S3167097/22", *_hAvX, *_hN);
      // h->setTitle(_hAvX->title());
      // histogramFactory().destroy(_hAvX);

      // h = histogramFactory().divide("/H1_1995_S3167097/23", *_hAvQ2, *_hN);
      // h->setTitle(_hAvQ2->title());
      // histogramFactory().destroy(_hAvQ2);
    }

    //@}


  private:

    /// Some integer constants used.
    /// @todo Remove statics!
    static const size_t _nb = 24, _nbin = 9;

    /// Some double constants used.
    /// @todo Remove statics!
    static const double _xmin, _xmax;

    /// Histograms for the \f$ E_T \f$ flows
    vector<Histo1DPtr> _hEtFlow, _hEtFlowStat;

    /// Histograms for averages in different kinematical bins.
    Histo1DPtr _hAvEt, _hAvX, _hAvQ2, _hN;

    /// Helper vector;
    vector<double> _nev;
  };


  // Init statics
  const double H1_1995_S3167097::_xmin = -6.0;
  const double H1_1995_S3167097::_xmax = 6.0;


  // This global object acts as a hook for the plugin system
  AnalysisBuilder<H1_1995_S3167097> plugin_H1_1995_S3167097;

}
