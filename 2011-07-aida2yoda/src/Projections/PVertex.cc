// -*- C++ -*-
#include "Rivet/Rivet.hh"
#include "Rivet/Projections/PVertex.hh"
#include "HepMC/GenVertex.h"
#include "HepMC/GenEvent.h"

namespace Rivet {


  void PVertex::project(const Event& e) {
    // We'll *try* to do it right, in case any generators are doing the right thing...
    _thePVertex = e.genEvent().signal_process_vertex();
    getLog() << Log::DEBUG << "PVertex ptr from HepMC = " << _thePVertex << endl;
    if (!_thePVertex) {
      // Since no signal vertices are filled in existing Fortran & C++ MC's,
      // the decay vertex from first vertex in event with 2 incoming particles
   
      HepMC::GenEvent::vertex_const_iterator vIt = e.genEvent().vertices_begin();
      while((*vIt)->particles_in_size() != 2 && vIt != e.genEvent().vertices_end()){
        ++vIt;
      }
   
      if(vIt != e.genEvent().vertices_end()) _thePVertex = *vIt;
    }
    assert(_thePVertex);
    const unsigned int pVertexParticleSize = _thePVertex->particles_in_size();
    if (pVertexParticleSize != 2 ) {
      stringstream ss;
      ss << "Wrong number of Primary Vertex particles: " << pVertexParticleSize;
      throw Error(ss.str());
    }
  }


}
