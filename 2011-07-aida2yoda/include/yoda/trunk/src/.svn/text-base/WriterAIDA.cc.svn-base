// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#include "YODA/WriterAIDA.h"
#include "YODA/Utils/StringUtils.h"

#include <iostream>
using namespace std;

namespace YODA {


  void WriterAIDA::writeHeader(std::ostream& stream) {
    stream << "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
    stream << "<!DOCTYPE aida SYSTEM \"http://aida.freehep.org/schemas/3.0/aida.dtd\">\n";
    stream << "<aida>\n";
    stream << "  <implementation version=\"1.0\" package=\"YODA\"/>\n";
  }


  void WriterAIDA::writeFooter(std::ostream& stream) {
    stream << "</aida>\n";
  }


  void WriterAIDA::writeHisto1D(std::ostream& os, const Histo1D& h) {
    Scatter2D tmp = mkScatter(h);
    tmp.setAnnotation("Type", "Histo1D");
    writeScatter2D(os, tmp);
  }


  void WriterAIDA::writeProfile1D(std::ostream& os, const Profile1D& p) {
    Scatter2D tmp = mkScatter(p);
    tmp.setAnnotation("Type", "Profile1D");
    writeScatter2D(os, tmp);
  }


  void WriterAIDA::writeScatter2D(std::ostream& os, const Scatter2D& s) {
    string name = "";
    string path = "/";
    const size_t slashpos = s.path().rfind("/");
    if (slashpos != string::npos) {
      name = s.path().substr(slashpos+1, s.path().length() - slashpos - 1);
      path = s.path().substr(0, slashpos+1);
    }
    os << "  <dataPointSet name=\"" << Utils::encodeForXML(name) << "\""
       << " title=\"" << Utils::encodeForXML(s.title()) << "\""
       << " path=\"" << Utils::encodeForXML(path) << "\">\n";
    os << "    <dimension dim=\"0\" title=\"\" />\n";
    os << "    <dimension dim=\"1\" title=\"\" />\n";
    os << "    <annotation>\n";
    typedef pair<string,string> sspair;
    foreach (const sspair& kv, s.annotations()) {
      os << "      <item key=\"" << Utils::encodeForXML(kv.first)
         << "\" value=\"" << Utils::encodeForXML(kv.second) << "\" />\n";
    }
    if (!s.hasAnnotation("Type")) {
      os << "      <item key=\"Type\" value=\"Scatter2D\" />\n";
    }
    os << "    </annotation>\n";
    foreach (Point2D pt, s.points()) {
      os << "    <dataPoint>\n";
      os << "      <measurement value=\"" << pt.x()
         << "\" errorMinus=\"" << pt.xErrMinus() << "\" errorPlus=\"" << pt.xErrPlus() << "\"/>\n";
      os << "      <measurement value=\"" << pt.y()
         << "\" errorMinus=\"" << pt.yErrMinus() << "\" errorPlus=\"" << pt.yErrPlus() << "\"/>\n";
      os << "    </dataPoint>\n";
    }
    os << "  </dataPointSet>\n";
    os << flush;
  }


}
