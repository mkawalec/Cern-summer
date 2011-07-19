// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_READERYODA_H
#define YODA_READERYODA_H

#include "YODA/AnalysisObject.h"
#include "YODA/Reader.h"

#include <vector>
#include <string>
#include <istream>


namespace YODA {


  /// @brief Persistency reader from YODA flat text data format.
  class ReaderYODA : public Reader {
  public:

    static Reader& create() {
      static ReaderYODA _instance;
      return _instance;
    }

  protected:
    void writeHeader(std::ostream& stream);
    void writeFooter(std::ostream& stream);

    void writeHisto(std::ostream& stream, const Histo1D& h);
    void writeProfile(std::ostream& stream, const Profile1D& p);
    void writeScatter2D(std::ostream& stream, const Scatter2D& s);

  private:
    ReaderYODA() { }

  };


}

#endif
