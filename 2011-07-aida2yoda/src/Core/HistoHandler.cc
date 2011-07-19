// -*- C++ -*-
#include "Rivet/Rivet.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/HistoHandler.hh"
#include "Rivet/Analysis.hh"
#include <algorithm>

namespace Rivet {


  // Get a logger.
  Log& HistoHandler::getLog() const {
    return Log::getLog("Rivet.HistoHandler");
  }


  void HistoHandler::clear() {
    _namedhistos.clear();
  }


  // Delete contained pointers.
  HistoHandler::~HistoHandler() {
    clear();
  }


  const AnalysisObject* HistoHandler::registerAnalysisObject(const Analysis& parent,
                                                             const AnalysisObject& ao,
                                                             const string& name) {
    getLog() << Log::TRACE << "Trying to register"
             << " analysis object " << &ao
             << " for parent " << &parent << "(" << parent.name() << ")"
             << " with name '" << name << "'" << endl;

    // If this name is already registered for this analysis, throw a complaint
    NamedHistosMap::const_iterator nhs = _namedhistos.find(&parent);
    if (nhs != _namedhistos.end()) {
      NamedHistos::const_iterator nh = nhs->second.find(name);
      if (nh != nhs->second.end()) {
        stringstream ss;
        ss << "Histogram \"" << name
           << "\" already exists for parent analysis " << &parent;
        throw Error(ss.str());
      }
    }

    _namedhistos[&parent][name] = &ao;
    //return *(_namedhistos[&parent][name]);
    return const_cast<AnalysisObject*>(_namedhistos[&parent][name]);
  }



  AnalysisObject* HistoHandler::_getAnalysisObject(const Analysis& parent,
                                                         const string& name) const {
    getLog() << Log::TRACE << "Searching for child histo '"
             << name << "' of " << &parent << endl;

    NamedHistosMap::const_iterator nhs = _namedhistos.find(&parent);
    if (nhs == _namedhistos.end()) {
      stringstream ss;
      ss << "Couldn't find any histograms for parent analysis " << &parent;
      throw Error(ss.str());
    }

    NamedHistos::const_iterator nh = nhs->second.find(name);
    if (nh == nhs->second.end()) {
      stringstream ss;
      ss << "Couldn't find histogram \"" << name
         << "\" for parent analysis " << &parent;
      throw Error(ss.str());
    }

    //return *(nh->second);
    AnalysisObject* rtn = const_cast<AnalysisObject*>(nh->second);
    return rtn;
  }


}
