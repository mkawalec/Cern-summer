// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#include "YODA/AnalysisObject.h"
#include "YODA/Exceptions.h"
using namespace std;

namespace YODA {

  const string& AnalysisObject::annotation(const string& name) const {
    map<string,string>::const_iterator v = _annotations.find(name);
    if (v == _annotations.end()) {
      string missing = "YODA::AnalysisObject: No annotation named " + name;
      throw AnnotationError(missing);
    }
    return v->second;
  }

}
