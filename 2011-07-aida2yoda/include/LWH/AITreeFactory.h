// -*- C++ -*-
#ifndef LWH_AITreeFactory_H
#define LWH_AITreeFactory_H

#ifndef LWH_USING_AIDA

#include <string>

/** @cond DONT_DOCUMENT_STRIPPED_DOWN_AIDA_INTERFACES */

namespace AIDA {

class ITree;

class ITreeFactory {

public:

  virtual ~ITreeFactory() {}

  virtual ITree * create(const std::string &, const std::string & = "",
			 bool = false, bool = false,
			 const std::string & = "") = 0;

  virtual ITree * create() = 0;

};

}

/** @endcond */

#else
#include "AIDA/ITreeFactory.h"
#endif

#endif /* LWH_AITreeFactory_H */
