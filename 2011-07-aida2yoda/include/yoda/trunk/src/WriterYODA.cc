// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#include "YODA/WriterYODA.h"

#include <iostream>
#include <iomanip>

using namespace std;

namespace YODA {


  void WriterYODA::writeHeader(std::ostream& os) {
    // os <<
    //   "# BEGIN PLOT\n"
    //   "LogY=0\n"
    //   "Title=Test Histo\n"
    //   "# END PLOT\n\n";
  }


  void WriterYODA::writeFooter(std::ostream& os) {
    os << flush;
  }


  void _writeAnnotations(std::ostream& os, const AnalysisObject& ao) {
    // os << "Path=" << h.path() << "\n";
    // os << "Title=" << h.title() << "\n";
    typedef pair<string,string> sspair;
    foreach (const sspair& kv, ao.annotations()) {
      os << kv.first << "=" << kv.second << "\n";
    }
  }


  void WriterYODA::writeHisto1D(std::ostream& os, const Histo1D& h) {
    ios_base::fmtflags oldflags = os.flags();
    const int precision = 6;
    os << scientific << showpoint << setprecision(precision);

    os << "# BEGIN HISTO1D " << h.path() << "\n";
    _writeAnnotations(os, h);
    os << "# Mean: " << h.mean() << "\n";
    os << "# Area: " << h.integral() << "\n";
    os << "# xlow\t\t xhigh\t\t yval\t\t yerr\t\t sumw\t\t sumw2\t\t sumwx\t\t sumwx2\n";
    for (vector<HistoBin1D>::const_iterator b = h.bins().begin(); b != h.bins().end(); ++b) {
      os << b->lowEdge() << '\t' << b->highEdge() << '\t';
      os << b->height() << '\t' << b->heightError() << '\t';
      os << b->sumW() << '\t' << b->sumW2() << '\t';
      os << b->sumWX() << '\t' << b->sumWX2() << '\n';
    }
    os << "# END HISTO1D\n\n";

    os.flags(oldflags);
  }


  void WriterYODA::writeProfile1D(std::ostream& os, const Profile1D& p) {
    ios_base::fmtflags oldflags = os.flags();
    const int precision = 6;
    os << scientific << showpoint << setprecision(precision);

    os << "# BEGIN PROFILE1D\n";
    _writeAnnotations(os, p);
    os << "# xlow\t xhigh\t yval\t yerr\t sumw\t sumw2\t sumwx\t sumwx2\t sumwy\t sumwy2 \n";
    for (vector<ProfileBin1D>::const_iterator b = p.bins().begin(); b != p.bins().end(); ++b) {
      os << b->lowEdge() << "\t" << b->highEdge() << "\t";
      os << b->mean() << "\t" << b->stdErr() << "\t";
      os << b->sumW() << "\t" << b->sumW2() << "\t";
      os << b->sumWX() << "\t" << b->sumWX2() << "\t";
      os << b->sumWY() << "\t" << b->sumWY2();
      os << "\n";
    }
    os << "# END PROFILE1D\n";

    os.flags(oldflags);
  }


  void WriterYODA::writeScatter2D(std::ostream& os, const Scatter2D& s) {
    ios_base::fmtflags oldflags = os.flags();
    const int precision = 6;
    os << scientific << showpoint << setprecision(precision);

    os << "# BEGIN SCATTER2D\n";
    _writeAnnotations(os, s);
    os << "# xval\t xerr-\t xerr+\t yval\t yerr-\t yerr+ \n";
    foreach (Point2D pt, s.points()) {
      os << pt.x() << "\t" << pt.xErrMinus() << "\t" << pt.xErrMinus() << "\t";
      os << pt.y() << "\t" << pt.yErrMinus() << "\t" << pt.yErrMinus() << "\n";
    }
    os << "# END SCATTER2D\n";

    os << flush;
    os.flags(oldflags);
  }


}
