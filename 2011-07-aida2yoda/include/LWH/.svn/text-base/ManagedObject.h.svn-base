// -*- C++ -*-
#ifndef LWH_ManagedObject_H
#define LWH_ManagedObject_H
//
// This is the declaration of the ManagedObject class.
//

#include "AIManagedObject.h"
#include <iostream>

#ifdef HAVE_ROOT
  #include "TFile.h"
#endif

namespace LWH {

using namespace AIDA;

/**
 * The creator of trees.
 */
class ManagedObject: public IManagedObject {

public:

  /// Destructor.
  virtual ~ManagedObject() {}

  /**
   * Encode sensitive characters as XML entities.
   */
  std::string encodeForXML(const std::string& in) {
    std::string out = in;
    typedef std::pair<std::string, std::string> CharsToEntities;
    std::vector<CharsToEntities> cs2es;
    // Ampersand has to be first!
    cs2es.push_back(std::make_pair("&", "&amp;"));
    cs2es.push_back(std::make_pair("\"", "&quot;"));
    cs2es.push_back(std::make_pair("<", "&lt;"));
    cs2es.push_back(std::make_pair(">", "&gt;"));

    for (std::vector<CharsToEntities>::const_iterator c2e = cs2es.begin();
         c2e != cs2es.end(); ++c2e) {
      size_t pos = 0;
      while (true) {
        if (pos != 0) ++pos;
        pos = out.find(c2e->first, pos);
        if (pos != std::string::npos) {
          out.replace(pos, 1, c2e->second);
        } else {
          break;
        }
      }
    }
    return out;
  }


  /**
   * Write out the object to the given stream in XML format.
   */
  virtual bool writeXML(std::ostream & os,
			std::string path, std::string name) = 0;

  /**
   * Write out the object to the given stream in simple table format.
   */
  virtual bool writeFLAT(std::ostream & os,
			 std::string path, std::string name) = 0;



#ifdef HAVE_ROOT
  /**
   * Write out the object to the given TFile in Root format.
   */
  virtual bool writeROOT(TFile* file,
			 std::string path, std::string name) = 0;
#endif


};

}

#endif /* LWH_ManagedObject_H */
