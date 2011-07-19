// -*- C++ -*-
#ifndef RIVET_IsolationProjection_HH
#define RIVET_IsolationProjection_HH

#include "Rivet/Event.hh"
#include "Rivet/Projection.hh"
#include "Rivet/Math/Units.hh"
#include "Rivet/Projections/IsolationEstimators.hh"
#include <boost/shared_ptr.hpp>

namespace Rivet{


  /// PROJ1 can be either FinalState projections or JetAlg projections
  /// PROJ1::entity_type and PROJ2::entity_type can be either Particle of Jet
  template <typename PROJ1, typename PROJ2,
            typename EST = typename isohelper<typename PROJ1::entity_type, typename PROJ2::collection_type>::estimatorhelper>
  class IsolationProjection : public Projection {
    public:
    /// Constructor
    IsolationProjection(PROJ1& iso,
                        PROJ2& ctrl,
                        EST* estimator,
                        double ptmin = 0*GeV) :
      _estimator(estimator),
      _ptmin(ptmin)
    {
      setName("IsolationProjection");
      addProjection(iso, "ToBeIsolated");
      addProjection(ctrl, "Control");
    }	

    /// Get the isolation values for the isofinalstate
    const vector<pair<const typename PROJ1::entity_type*, double> >
    isolatedParticles(double maxiso = numeric_limits<double>::max()) const;

    virtual const Projection* clone() const {
      return new IsolationProjection(*this);
    }

  protected:

    /// Apply the projection to the event.
    virtual void project(const Event& e);

    /// Compare projections.
    virtual int compare(const Projection& p) const;
		

  private:
 
    /// the estimator
    boost::shared_ptr<EST> _estimator;

    /// The isolation cone radius
    //double _coneRadius;

    /// The minimum pt to trigger isolation calculation
    double _ptmin;

    /// the isolation parameter value for each particle in _isofsp
    /// the _isofsp MUST live, these particle pointers are potentially dangerous, let's try....
    vector<pair<const typename PROJ1::entity_type*, double> > _isovalues;
  };


  template<typename PROJ1, typename PROJ2, typename EST>
  inline const vector<pair<const typename PROJ1::entity_type*, double> > IsolationProjection<PROJ1, PROJ2, EST>
  ::isolatedParticles(double maxiso) const {
    vector<pair<const typename PROJ1::entity_type*, double> > out;
    for (typename vector<pair<const typename PROJ1::entity_type*, double> >::const_iterator i = _isovalues.begin(); i != _isovalues.end(); ++i){
      if (i->second < maxiso) out.push_back(*i);
    }
    return out;
  }


  template<typename PROJ1, typename PROJ2, typename EST>
  inline void IsolationProjection<PROJ1, PROJ2, EST>::project(const Event& e){
    Log& log = getLog();
    _isovalues.clear();
    /// projetc the final states
    const PROJ1& isofs  = applyProjection<PROJ1>(e, "ToBeIsolated");
    /// copy of particles is suboptimal, but FinalState returns
    /// particles by referencem while JetAlg returns jets by value
    const typename PROJ1::collection_type isopart = isofs.entities();
    const PROJ2& ctrlfs = applyProjection<PROJ2>(e, "Control");
    const typename PROJ2::collection_type ctrlpart = ctrlfs.entities();
    for (typename PROJ1::collection_type::const_iterator iiso = isopart.begin(); iiso != isopart.end(); ++iiso){
      if (iiso->getMomentum().pT() < _ptmin) continue;
      double isolation = _estimator->estimate(*iiso, ctrlpart);
      log << Log::DEBUG << "Isolation for particle with momentum " << iiso->getMomentum()
          << " is " << isolation << endl;
      _isovalues.push_back(make_pair(&(*iiso), isolation));
    }
  }

  template<typename PROJ1, typename PROJ2, typename EST>
  inline int IsolationProjection<PROJ1, PROJ2, EST>::compare(const Projection& p) const{
    const IsolationProjection & other = dynamic_cast<const IsolationProjection &>(p);
    //first check the final states	
    int isofscmp = mkNamedPCmp(other, "ToBeIsolated");
    if (isofscmp != EQUIVALENT) return isofscmp;
    int isoctrlcmp = mkNamedPCmp(other, "Control");
    if (isoctrlcmp != EQUIVALENT) return isoctrlcmp;
    // compare the ptmin of the isolated colection
    int ptmincmp = cmp(_ptmin, other._ptmin);
    if (ptmincmp != EQUIVALENT) return ptmincmp;
    // compare the estimators
    //if (cmp(*(_estimator.get()),*(other._estimator.get())) == EQUIVALENT) cout << "Estimatori uguali!" << endl;
    return cmp(*(_estimator.get()),*(other._estimator.get()));
  }

}

#endif
