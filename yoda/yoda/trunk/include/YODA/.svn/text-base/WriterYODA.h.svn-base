// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_WRITERYODA_H
#define YODA_WRITERYODA_H

#include "YODA/AnalysisObject.h"
#include "YODA/Writer.h"

#include <vector>
#include <string>
#include <ostream>


namespace YODA {


  /// @brief Persistency writer for YODA flat text format.
  class WriterYODA : public Writer {
  public:

    /// Singleton creation function
    static Writer& create() {
      static WriterYODA _instance;
      return _instance;
    }


    // Include definitions of all write methods (all fulfilled by Writer::write(...))
    #include "YODA/WriterMethods.icc"


  protected:

    void writeHeader(std::ostream& stream);
    void writeFooter(std::ostream& stream);

    void writeHisto1D(std::ostream& stream, const Histo1D& h);
    void writeProfile1D(std::ostream& stream, const Profile1D& p);
    void writeScatter2D(std::ostream& stream, const Scatter2D& s);


  private:

    /// Private since it's a singleton.
    WriterYODA() { }

  };


}

#endif
