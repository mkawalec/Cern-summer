// -*- C++ -*-
#include "Rivet/Rivet.hh"
#include "Rivet/Projections/VisibleFinalState.hh"
#include "Rivet/Cmp.hh"
#include "Rivet/Tools/Utils.hh"
#include <algorithm>

namespace Rivet {


  namespace {
    void _setup_vfs(VetoedFinalState& vfs) {
      vfs.vetoNeutrinos();
      vfs.addVetoId(1000022); // lightest neutralino
      vfs.addVetoId(1000039); // gravitino
      /// @todo More?
    }
  }


  VisibleFinalState::VisibleFinalState() {
    setName("VisibleFinalState");
    VetoedFinalState vfs;
    _setup_vfs(vfs);
    addProjection(vfs, "VetoedFS");
  }


  VisibleFinalState::VisibleFinalState(double mineta, double maxeta, double minpt) {
    setName("VisibleFinalState");
    VetoedFinalState vfs(FinalState(mineta, maxeta, minpt));
    _setup_vfs(vfs);
    addProjection(vfs, "VetoedFS");
  }


  VisibleFinalState::VisibleFinalState(const FinalState& fsp) {
    setName("VisibleFinalState");
    VetoedFinalState vfs(fsp);
    _setup_vfs(vfs);
    addProjection(vfs, "VetoedFS");
  }


  int VisibleFinalState::compare(const Projection& p) const {
    return mkNamedPCmp(p, "VetoedFS");
  }


  void VisibleFinalState::project(const Event& e) {
    const FinalState& vfs = applyProjection<FinalState>(e, "VetoedFS");
    _theParticles = vfs.particles();
  }


}
