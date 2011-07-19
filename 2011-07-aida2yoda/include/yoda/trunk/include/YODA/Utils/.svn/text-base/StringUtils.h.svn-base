// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_STRINGUTILS_H
#define YODA_STRINGUTILS_H

namespace YODA {
  namespace Utils {

    /// Replace
    inline string encodeForXML(const string& in) {
      string out = in;
      typedef pair<string, string> CharsToEntities;
      vector<CharsToEntities> cs2es;
      cs2es.push_back(make_pair("&", "&amp;"));
      cs2es.push_back(make_pair("<", "&lt;"));
      cs2es.push_back(make_pair(">", "&gt;"));

      for (vector<CharsToEntities>::const_iterator c2e = cs2es.begin(); c2e != cs2es.end(); ++c2e) {
        string::size_type pos = -1;
        while ( ( pos = out.find(c2e->first, pos + 1) ) != string::npos ) {
          out.replace(pos, 1, c2e->second);
        }
      }
      return out;
    }

  }
}

#endif
