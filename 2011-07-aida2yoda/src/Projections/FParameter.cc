// -*- C++ -*-
#include "Rivet/Projections/FParameter.hh"
#include "Rivet/Cmp.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Tools/Utils.hh"

namespace Rivet {

  FParameter::FParameter(const FinalState& fsp) {
    setName("FParameter");
    addProjection(fsp, "FS");
    clear();
  }


  void FParameter::clear() {
    _lambdas = vector<double>(2, 0);
  }


  void FParameter::project(const Event& e) {
    const ParticleVector prts = applyProjection<FinalState>(e, "FS").particles();
    calc(prts);
  }


  void FParameter::calc(const FinalState& fs) {
    calc(fs.particles());
  }

  void FParameter::calc(const vector<Particle>& fsparticles) {
    vector<Vector3> threeMomenta;
    threeMomenta.reserve(fsparticles.size());
    foreach (const Particle& p, fsparticles) {
      const Vector3 p3 = p.momentum().vector3();
      threeMomenta.push_back(p3);
    }
    _calcFParameter(threeMomenta);
  }

  void FParameter::calc(const vector<FourMomentum>& fsmomenta) {
    vector<Vector3> threeMomenta;
    threeMomenta.reserve(fsmomenta.size());
    foreach (const FourMomentum& v, fsmomenta) {
      threeMomenta.push_back(v.vector3());
    }
    _calcFParameter(threeMomenta);
  }

  void FParameter::calc(const vector<Vector3>& fsmomenta) {
    _calcFParameter(fsmomenta);
  }

  // Actually do the calculation
  void FParameter::_calcFParameter(const vector<Vector3>& fsmomenta) {

    // Return (with "safe nonsense" sphericity params) if there are no final state particles.
    if (fsmomenta.empty()) {
      getLog() << Log::DEBUG << "No particles in final state..." << endl;
      clear();
      return;
    }

    // A small iteration over full momenta but set z-coord. to 0.0 to get transverse momenta
    vector <Vector3> fsperpmomenta;
    foreach (const Vector3& p, fsmomenta) {
      fsperpmomenta.push_back(Vector3(p.x(), p.y(), 0.0));
    }

    // Iterate over all the final state particles.
    Matrix<2> mMom;
    getLog() << Log::DEBUG << "Number of particles = " << fsperpmomenta.size() << endl;
    foreach (const Vector3& p3, fsperpmomenta) {

      double prefactor = 1.0/mod(p3);

      Matrix<2> mMomPart;
      for (size_t i = 0; i < 2; ++i) {
        for (size_t j = 0; j < 2; ++j) {
          mMomPart.set(i,j, p3[i]*p3[j]);
        }
      }
      mMom += prefactor * mMomPart;
    }

    getLog() << Log::DEBUG << "Linearised transverse momentum tensor = " << endl << mMom << endl;

    // Check that the matrix is symmetric.
    const bool isSymm = mMom.isSymm();
    if (!isSymm) {
      getLog() << Log::ERROR << "Error: momentum tensor not symmetric:" << endl;
      getLog() << Log::ERROR << "[0,1] vs. [1,0]: " << mMom.get(0,1) << ", " << mMom.get(1,0) << endl;
      getLog() << Log::ERROR << "[0,2] vs. [2,0]: " << mMom.get(0,2) << ", " << mMom.get(2,0) << endl;
      getLog() << Log::ERROR << "[1,2] vs. [2,1]: " << mMom.get(1,2) << ", " << mMom.get(2,1) << endl;
    }
    // If not symmetric, something's wrong (we made sure the error msg appeared first).
    assert(isSymm);

    // Diagonalize momentum matrix.
    const EigenSystem<2> eigen2 = diagonalize(mMom);
    getLog() << Log::DEBUG << "Diag momentum tensor = " << endl << eigen2.getDiagMatrix() << endl;
 
    // Reset and set eigenvalue parameters.
    _lambdas.clear();
    const EigenSystem<2>::EigenPairs epairs = eigen2.getEigenPairs();
    assert(epairs.size() == 2);
    for (size_t i = 0; i < 2; ++i) {
      _lambdas.push_back(epairs[i].first);
    }

    // Debug output.
    getLog() << Log::DEBUG << "Lambdas = ("
             << lambda1() << ", " << lambda2() << ")" << endl;
    getLog() << Log::DEBUG << "Sum of lambdas = " << lambda1() + lambda2() << endl;
  }
}
