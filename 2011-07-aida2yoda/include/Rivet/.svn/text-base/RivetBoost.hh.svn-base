#ifndef RIVET_RIVETBOOST_HH
#define RIVET_RIVETBOOST_HH

#include "boost/smart_ptr.hpp"
#include "boost/lexical_cast.hpp"
#include "boost/assign.hpp"

#include "boost/foreach.hpp"
#define foreach BOOST_FOREACH

#include <boost/random.hpp>
#include <boost/algorithm/string.hpp>

namespace Rivet {


  // Smart pointers
  using boost::shared_ptr;

  // Clever casts
  using boost::lexical_cast;
  using boost::bad_lexical_cast;

  // Clever assignment shortcuts
  using namespace boost::assign;

  // Strings
  using namespace boost;

  // Random numbers
  typedef boost::minstd_rand RngBase;
  typedef boost::uniform_real<> UniformRealDist;
  typedef boost::variate_generator<RngBase&, UniformRealDist> UniformRealRNG;
  typedef boost::uniform_int<> UniformIntDist;
  typedef boost::variate_generator<RngBase&, UniformIntDist> UniformIntRNG;


}

#endif
