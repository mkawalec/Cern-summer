// -*- C++ -*-

#include "Rivet/Rivet.hh"
#include "Rivet/Cuts.hh"

using std::ostringstream;

namespace Rivet {


  Cuts& Cuts::addCut(const string& quantity, const Comparison& comparison, const double value) {
    // If this quantity doesn't yet have any associated cuts, make a
    // default cut with effectively infinitely loose cuts.
    if (_cuts.find(quantity) == _cuts.end()) {
      _cuts[quantity] = BinaryCut();
    }
    // Combine cuts in the most restrictive way.
    switch (comparison) {
    case LESS_EQ:
      if (value < _cuts[quantity].getLowerThan()) {
        _cuts[quantity].setLowerThan(value);
      }
      break;
    case MORE_EQ:
      if (value > _cuts[quantity].getHigherThan()) {
        _cuts[quantity].setHigherThan(value);
      }
      break;
    case EQUAL:
      _cuts[quantity].setLowerThan(value);
      _cuts[quantity].setHigherThan(value);
      break;
    }

    // Allow method chaining.
    return *this;
  }



  bool Cuts::checkConsistency() const {
    for (Cuts::const_iterator c = begin(); c != end(); ++c) {
      if (c->second.getLowerThan() < c->second.getLowerThan()) {
        ostringstream msg;
        msg << "Constraints on " << c->first << " are incompatible: "
            << ">=" << c->second.getHigherThan() << " AND "
            << "<=" << c->second.getLowerThan();
        throw Error(msg.str());
      }
    }
    return true;
  }



  ostream& Cuts::print(ostream & os) const {
    for (Cuts::const_iterator cut = begin(); cut != end(); ++cut) {
      os << endl;
      os << setw(12) << std::left << cut->first;
      if (cut->second.getHigherThan() > -numeric_limits<double>::max()) {
        os << setw(3) << ">=";
        os << setw(10) << std::right << cut->second.getHigherThan();
      } else {
        os << setw(13) << "";
      }
      if (cut->second.getLowerThan() < numeric_limits<double>::max()) {
        os << setw(3) << "<=";
        os << setw(10) << std::right << cut->second.getLowerThan();
      } else {
        os << setw(13) << "";
      }
    }
    return os;
  }


}
