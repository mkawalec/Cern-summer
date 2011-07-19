// -*- C++ -*-
#ifndef RIVET_FastJets_HH
#define RIVET_FastJets_HH

#include "Rivet/Projection.hh"
#include "Rivet/Projections/JetAlg.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Particle.hh"
#include "Rivet/Jet.hh"

#include "fastjet/JetDefinition.hh"
#include "fastjet/AreaDefinition.hh"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/ClusterSequenceArea.hh"
#include "fastjet/PseudoJet.hh"

#include "fastjet/SISConePlugin.hh"
#include "fastjet/ATLASConePlugin.hh"
#include "fastjet/CMSIterativeConePlugin.hh"
#include "fastjet/CDFJetCluPlugin.hh"
#include "fastjet/CDFMidPointPlugin.hh"
#include "fastjet/D0RunIIConePlugin.hh"
#include "fastjet/TrackJetPlugin.hh"
#include "fastjet/JadePlugin.hh"
//#include "fastjet/PxConePlugin.hh"

namespace Rivet {


  /// Make a 3-momentum vector from a FastJet pseudo-jet
  inline Vector3 momentum3(const fastjet::PseudoJet& pj) {
    return Vector3(pj.px(), pj.py(), pj.pz());
  }

  /// Make a 4-momentum vector from a FastJet pseudo-jet
  inline FourMomentum momentum(const fastjet::PseudoJet& pj) {
    return FourMomentum(pj.E(), pj.px(), pj.py(), pj.pz());
  }


  /// Typedef for a collection of PseudoJets.
  typedef vector<fastjet::PseudoJet> PseudoJets;



  /////////////////////////



  /// Project out jets found using the FastJet package jet algorithms.
  class FastJets : public JetAlg {

  public:
    /// Wrapper enum for selected Fastjet jet algorithms.
    enum JetAlgName { KT, CAM, SISCONE, ANTIKT,
                      PXCONE,
                      ATLASCONE, CMSCONE,
                      CDFJETCLU, CDFMIDPOINT, D0ILCONE,
                      JADE, DURHAM, TRACKJET };


    /// @name Constructors etc.
    //@{

    /// "Wrapped" argument constructor using Rivet enums for most common
    /// jet alg choices (including some plugins). For the built-in algs,
    /// E-scheme recombination is used. For full control of
    /// FastJet built-in jet algs, use the native arg constructor.
    FastJets(const FinalState& fsp, JetAlgName alg,
             double rparameter, double seed_threshold=1.0);

    /// Native argument constructor, using FastJet alg/scheme enums.
    FastJets(const FinalState& fsp, fastjet::JetAlgorithm type,
             fastjet::RecombinationScheme recom, double rparameter);

    /// Explicitly pass in an externally-constructed plugin
    FastJets(const FinalState& fsp, fastjet::JetDefinition::Plugin& plugin);

    /// Same thing as above, but we want to pass the particles directly to the calc method
    FastJets(JetAlgName alg, double rparameter, double seed_threshold=1.0);
    FastJets(fastjet::JetAlgorithm type, fastjet::RecombinationScheme recom, double rparameter);
    FastJets(fastjet::JetDefinition::Plugin& plugin);

    // /// Explicit copy constructor.
    // FastJets(const FastJets& other);

    /// Clone on the heap.
    virtual const Projection* clone() const {
      return new FastJets(*this);
    }

    //@}


  public:

    /// Reset the projection. Jet def, etc. are unchanged.
    void reset();

    /// @brief Use provided jet area definition
    /// @warning adef is NOT copied, the user must ensure that it remains valid!
    /// Provide an adef null pointer to re-disable jet area calculation
    void useJetArea(fastjet::AreaDefinition* adef) {
      _adef = adef;
    }

    /// Number of jets above the \f$ p_\perp \f$ cut.
    size_t numJets(double ptmin = 0.0) const;

    /// Number of jets.
    size_t size() const {
      return numJets();
    }

    /// Get the jets (unordered).
    Jets _jets(double ptmin = 0.0) const;

    /// Get the pseudo jets (unordered).
    PseudoJets pseudoJets(double ptmin = 0.0) const;

    /// Get the pseudo jets, ordered by \f$ p_T \f$.
    PseudoJets pseudoJetsByPt(double ptmin = 0.0) const {
      return sorted_by_pt(pseudoJets(ptmin));
    }

    /// Get the pseudo jets, ordered by \f$ E \f$.
    PseudoJets pseudoJetsByE(double ptmin = 0.0) const {
      return sorted_by_E(pseudoJets(ptmin));
    }

    /// Get the pseudo jets, ordered by rapidity.
    PseudoJets pseudoJetsByRapidity(double ptmin = 0.0) const {
      return sorted_by_rapidity(pseudoJets(ptmin));
    }

    /// Return the cluster sequence (FastJet-specific).
    const fastjet::ClusterSequence* clusterSeq() const {
      return _cseq.get();
    }

    /// Return the cluster sequence (FastJet-specific).
    const fastjet::ClusterSequenceArea* clusterSeqArea() const {
      /// @todo Throw error if no area def? Or just blindly call dynamic_cast?
      if (_adef == 0) return (fastjet::ClusterSequenceArea*) 0;
      return dynamic_cast<fastjet::ClusterSequenceArea*>(_cseq.get());
    }

    /// Return the jet definition (FastJet-specific).
    const fastjet::JetDefinition& jetDef() const {
      return _jdef;
    }

    /// Return the area definition (FastJet-specific). May be null.
    const fastjet::AreaDefinition* areaDef() const {
      return _adef;
    }

    /// Get the subjet splitting variables for the given jet.
    vector<double> ySubJet(const fastjet::PseudoJet& jet) const;

    /// @brief Split a jet a la PRL100,242001(2008).
    /// Based on code from G.Salam, A.Davison.
    fastjet::PseudoJet splitJet(fastjet::PseudoJet jet, double& last_R) const;

    /// @brief Filter a jet a la PRL100,242001(2008).
    /// Based on code from G.Salam, A.Davison.
    fastjet::PseudoJet filterJet(fastjet::PseudoJet jet, double& stingy_R, const double def_R) const;

  private:

    Jets _pseudojetsToJets(const PseudoJets& pjets) const;

    void _init1(JetAlgName alg, double rparameter, double seed_threshold) {
      setName("FastJets");
      MSG_DEBUG("R parameter = " << rparameter);
      MSG_DEBUG("Seed threshold = " << seed_threshold);
      if (alg == KT) {
        _jdef = fastjet::JetDefinition(fastjet::kt_algorithm, rparameter, fastjet::E_scheme);
      } else if (alg == CAM) {
        _jdef = fastjet::JetDefinition(fastjet::cambridge_algorithm, rparameter, fastjet::E_scheme);
      } else if (alg == ANTIKT) {
        _jdef = fastjet::JetDefinition(fastjet::antikt_algorithm, rparameter, fastjet::E_scheme);
      } else if (alg == DURHAM) {
        _jdef = fastjet::JetDefinition(fastjet::ee_kt_algorithm, fastjet::E_scheme);
      } else {
        // Plugins:
        if (alg == SISCONE) {
          const double OVERLAP_THRESHOLD = 0.75;
          _plugin.reset(new fastjet::SISConePlugin(rparameter, OVERLAP_THRESHOLD));
        } else if (alg == PXCONE) {
          string msg = "PxCone currently not supported, since FastJet doesn't install it by default. ";
          msg += "Please notify the Rivet authors if this behaviour should be changed.";
          throw Error(msg);
          //_plugin.reset(new fastjet::PxConePlugin(rparameter));
        } else if (alg == ATLASCONE) {
          const double OVERLAP_THRESHOLD = 0.5;
          _plugin.reset(new fastjet::ATLASConePlugin(rparameter, seed_threshold, OVERLAP_THRESHOLD));
        } else if (alg == CMSCONE) {
          _plugin.reset(new fastjet::CMSIterativeConePlugin(rparameter, seed_threshold));
        } else if (alg == CDFJETCLU) {
          const double OVERLAP_THRESHOLD = 0.75;
          _plugin.reset(new fastjet::CDFJetCluPlugin(rparameter, OVERLAP_THRESHOLD, seed_threshold));
        } else if (alg == CDFMIDPOINT) {
          const double OVERLAP_THRESHOLD = 0.5;
          _plugin.reset(new fastjet::CDFMidPointPlugin(rparameter, OVERLAP_THRESHOLD, seed_threshold));
        } else if (alg == D0ILCONE) {
          const double min_jet_Et = 6.0;
          _plugin.reset(new fastjet::D0RunIIConePlugin(rparameter, min_jet_Et));
        } else if (alg == JADE) {
          _plugin.reset(new fastjet::JadePlugin());
        } else if (alg == TRACKJET) {
          _plugin.reset(new fastjet::TrackJetPlugin(rparameter));
        }
        _jdef = fastjet::JetDefinition(_plugin.get());
      }
    }

    void _init2(fastjet::JetAlgorithm type,
                     fastjet::RecombinationScheme recom, double rparameter) {
      setName("FastJets");
      _jdef = fastjet::JetDefinition(type, rparameter, recom);
    }

    void _init3(fastjet::JetDefinition::Plugin& plugin) {
      setName("FastJets");
      /// @todo Should we be copying the plugin?
      _plugin.reset(&plugin);
      _jdef = fastjet::JetDefinition(_plugin.get());
    }

  protected:

    /// Perform the projection on the Event.
    void project(const Event& e);

    /// Compare projections.
    int compare(const Projection& p) const;

  public:

    /// Do the calculation locally (no caching).
    void calc(const ParticleVector& ps);


  private:

    /// Jet definition
    fastjet::JetDefinition _jdef;

    /// Pointer to user-handled area definition
    fastjet::AreaDefinition* _adef;

    /// Cluster sequence
    shared_ptr<fastjet::ClusterSequence> _cseq;

    /// FastJet external plugin
    shared_ptr<fastjet::JetDefinition::Plugin> _plugin;

    /// Map of vectors of y scales. This is mutable so we can use caching/lazy evaluation.
    mutable map<int, vector<double> > _yscales;

    /// set of particles sorted by their PT2
    //set<Particle, ParticleBase::byPTAscending> _particles;
    map<int, Particle> _particles;

  };

}

#endif
