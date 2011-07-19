// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/MissingMomentum.hh"
#include "Rivet/Projections/FinalState.hh"

namespace Rivet {

  class ATLAS_2011_S9002537 : public Analysis {

  public:
    ATLAS_2011_S9002537(): Analysis("ATLAS_2011_S9002537")
    {
    }

  public:
    void init() {
      IdentifiedFinalState Muons(-2.4,2.4,20.*GeV);
      Muons.acceptIdPair(MUON);
      addProjection(Muons,"muons");

      ChargedFinalState CFS(-2.8,2.8,0.*GeV);
      addProjection(CFS,"tracks");

      MissingMomentum missmom(FinalState(-5.,5.,0.*GeV));
      addProjection(missmom,"MissingMomentum");

      _h_plus   = bookHistogram1D("_h_plus",  binEdges(1,1,1));
      _h_minus  = bookHistogram1D("_h_minus", binEdges(1,1,1));
      _h_asym   = bookDataPointSet(1,1,1);
    }

    void analyze(const Event& event) {
      const IdentifiedFinalState& muons =
        applyProjection<IdentifiedFinalState>(event, "muons");

      const ChargedFinalState& tracks =
        applyProjection<ChargedFinalState>(event, "tracks");

      if (muons.size()<1) vetoEvent;
      ParticleVector selected_muons;
      foreach (Particle muon, muons.particles()) {
        FourMomentum testmom = muon.momentum();
        double ptmu(testmom.pT()), ptsum(-ptmu), ratio(0.);
        foreach (Particle track,tracks.particles()) {
          FourMomentum trackmom = track.momentum();
          if (deltaR(testmom,trackmom)<0.4) {
            ptsum += trackmom.pT();
            ratio  = ptsum/ptmu;
            if (ratio>0.2)
              break;
          }
        }
        if (ratio<0.2)
          selected_muons.push_back(muon);
      }
      if (selected_muons.size()<1) vetoEvent;

      const FourMomentum muonmom = selected_muons[0].momentum();
      const MissingMomentum& missmom = applyProjection<MissingMomentum>(event, "MissingMomentum");
      FourMomentum missvec = -missmom.visibleMomentum();
      if (fabs(missvec.Et())<25) vetoEvent;

      double MTW = sqrt(2.*missvec.pT()*muonmom.pT()*(1.-cos(deltaPhi(missvec.phi(),muonmom.phi()))));
      if (MTW<40.*GeV) vetoEvent;

      if (selected_muons[0].pdgId()>0)
        _h_minus->fill(muonmom.eta(),event.weight());
      else
        _h_plus->fill(muonmom.eta(),event.weight());
    }


    /// Normalise histograms etc., after the run
    void finalize() {
      int Nbins = _h_plus->axis().bins();
      std::vector<double> asym, asym_err;
      for (int i=0; i<Nbins; i++) {
        double num   = _h_plus->binHeight(i) - _h_minus->binHeight(i);
        double denom = _h_plus->binHeight(i) + _h_minus->binHeight(i);
        double err   = _h_plus->binError(i)  + _h_minus->binError(i);

        if (num==0 || denom==0) {
          asym.push_back(0.);
          asym_err.push_back(0.);
        }
        else {
          asym.push_back(num/denom);
          asym_err.push_back(num/denom*((err/num)+(err/denom)));
        }
      }
      _h_asym->setCoordinate(1, asym, asym_err);

      histogramFactory().destroy(_h_plus);
      histogramFactory().destroy(_h_minus);
    }

  private:
    AIDA::IHistogram1D  *_h_plus, *_h_minus;
    AIDA::IDataPointSet *_h_asym;

  };

  AnalysisBuilder<ATLAS_2011_S9002537> plugin_ATLAS_2011_S9002537;
}
