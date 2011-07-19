// -*- C++ -*-
#include "Rivet/Rivet.hh"
#include "Rivet/Projections/Spherocity.hh"
#include "Rivet/Tools/Logging.hh"


namespace Rivet {


  void Spherocity::calc(const FinalState& fs) {
    calc(fs.particles());
  }


  void Spherocity::calc(const vector<Particle>& fsparticles) {
    vector<Vector3> threeMomenta;
    threeMomenta.reserve(fsparticles.size());
    foreach (const Particle& p, fsparticles) {
      const Vector3 p3 = p.momentum().vector3();
      threeMomenta.push_back(p3);
    }
    _calcSpherocity(threeMomenta);
  }


  void Spherocity::calc(const vector<FourMomentum>& fsmomenta) {
    vector<Vector3> threeMomenta;
    threeMomenta.reserve(fsmomenta.size());
    foreach (const FourMomentum& v, fsmomenta) {
      threeMomenta.push_back(v.vector3());
    }
    _calcSpherocity(threeMomenta);
  }


  void Spherocity::calc(const vector<Vector3>& fsmomenta) {
    _calcSpherocity(fsmomenta);
  }


  /////////////////////////////////////////////////


  // Inline functions to avoid template hell
  inline bool mod2Cmp(const Vector<2>& a, const Vector<2>& b) {
    return a.mod2() > b.mod2();
  }

  inline double dot(const Vector<2>& a, const Vector<2>& b) {
    return a[0]*b[0] + a[1]*b[1];
  }

  inline Vector<2> unit(const Vector<2>& v) {
    assert(mod(v) > 0);
    Vector<2> returnthis;
    returnthis.set(0, v[0]/mod(v));
    returnthis.set(1, v[1]/mod(v));
    return returnthis;
  }



  //// Do the general case spherocity calculation
  void _calcS(const vector<Vector3 >& perpmomenta, double& sphero, Vector3& saxis) {
    // According to the Salam paper, p5, footnote 4, the
    // axis n that minimises the Spherocity value ALWAYS coincides with the
    // direction of one of the transverse momentum vectors of the events particles.
    // Thus we carry out the calculation of Sphero for all particles and pick the
    // one that yields the smallerst values

    vector<Vector3> p = perpmomenta;
    vector<double> sval;


    // Prepare vector to store unit vector representation of all particle momenta
    // and also calculate the transverse momentum sum
    vector<Vector3> units;
    double sumperpmomenta = 0.0;
    foreach (const Vector3& p, perpmomenta) {
      units.push_back(Vector3(p.x(), p.y(), 0.0).unit());
      sumperpmomenta += p.mod();
    }

    // Spherocity calculation
    //
    // The outer loop is for iteration over all unit vectors
    foreach (const Vector3& u, units){
      double s =0.0;
      for (unsigned int k=0 ; k<p.size() ; k++)
        s += fabs(p[k].cross(u).mod()  );

      sval.push_back(s);
    }


    // Pick the solution with the smallest spherocity
    sphero = 999.;
    for (unsigned int i=0 ; i<units.size() ; i++)
      if (sval[i] < sphero){
        sphero = sval[i];
        saxis  = units[i];
      }

  }



  // Do the full calculation
  void Spherocity::_calcSpherocity(const vector<Vector3>& fsmomenta) {

    // Make a vector of the three-momenta in the final state
    // Explicitly set the z-component (parallel to beam axis) to zero
    // This creates a 3D-vector representation of the transverse momentum
    // but take the full information momentum vectors as input

    vector<Vector3> fsperpmomenta;
    // A small iteration over full momenta but set z-coord. to 0.0 to get transverse momenta
    foreach (const Vector3& p, fsmomenta) {
      fsperpmomenta.push_back(Vector3(p.x(), p.y(), 0.0));
    }

    // This returns the scalar sum of (transverse) momenta
    double perpmomentumSum(0.0);
    foreach (const Vector3& p, fsperpmomenta) {
      perpmomentumSum += mod(p);
    }

    // Clear the caches
    _spherocities.clear();
    _spherocityAxes.clear();

    // If there are fewer than 2 visible particles, we can't do much
    // This is blindly copied from the Thrust projection
    if (fsmomenta.size() < 2) {
      for (int i = 0; i < 3; ++i) {
        _spherocities.push_back(-1);
        _spherocityAxes.push_back(Vector3(0,0,0));
      }
      return;
    }

    // Handle special case of spherocity = 1 if there are only 2 particles
    // This is blindly copied from the Thrust projection
    if (fsmomenta.size() == 2) {
      Vector3 axis(0,0,0);
      _spherocities.push_back(1.0);
      _spherocities.push_back(0.0);
      _spherocities.push_back(0.0);
      axis = fsmomenta[0].unit();
      if (axis.z() < 0) axis = -axis;
      _spherocityAxes.push_back(axis);
      /// @todo Improve this --- special directions bad...
      /// (a,b,c) _|_ 1/(a^2+b^2) (b,-a,0) etc., but which combination minimises error?
      if (axis.z() < 0.75)
        _spherocityAxes.push_back( (axis.cross(Vector3(0,0,1))).unit() );
      else
        _spherocityAxes.push_back( (axis.cross(Vector3(0,1,0))).unit() );
      _spherocityAxes.push_back( _spherocityAxes[0].cross(_spherocityAxes[1]) );
      return;
    }

    // Temporary variables for calcs
    Vector3 axis(0,0,0);
    double val = 0.;

    // Get spherocity
    _calcS(fsperpmomenta, val, axis);
    MSG_DEBUG("Mom sum = " << perpmomentumSum);
    double spherocity = PI*PI* val*val / (4 * perpmomentumSum*perpmomentumSum);
    _spherocities.push_back(spherocity);

    // See if calclulated spherocity value makes sense
    if (spherocity < 0.0 || spherocity > 1.0) {
      MSG_WARNING("Spherocity = " << spherocity);
    }

    MSG_DEBUG("Spherocity value = " << spherocity);

    MSG_DEBUG("Sperocity axis = " << axis);

    _spherocityAxes.push_back(axis);


    //// Get spherocity minor
    ////
    ////
    //// The Beam axis is eZ = (0, 0, 1)
    ////
    //double perpMinor = 0.0;
    //const Vector3 ez = Vector3(0, 0, 1);
    //foreach (const Vector3& v, fsperpmomenta) {
      //Vector3 temp = Vector3(v[0], v[1], 0.0);
      //perpMinor += mod(temp.cross(_spherocityAxes[0]));
    //}
    //_spherocitys.push_back(perpMinor / perpmomentumSum);


    //// Manual check
    //double test = 0.;
    //Vector<2>  ex;
    //ex.set(0, 1.0);
    //ex.set(1, 0);
    //foreach (const Vector<2> & v, fsperpmomenta2D) {
      //test+=fabs(dot(ex, v));
    //}
    //if (test/perpmomentumSum < _spherocities[0]) {
      //std::cout << "Warning: " << test/perpmomentumSum << " > " << _spherocitys[0] << "     " << _spherocityAxes[0] << endl;
    //}

  }


}
