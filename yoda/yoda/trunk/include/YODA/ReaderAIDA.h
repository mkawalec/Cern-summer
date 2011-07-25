// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_READERAIDA_H
#define YODA_READERAIDA_H

#include "YODA/AnalysisObject.h"
#include "YODA/Reader.h"

namespace YODA {


  /// @brief Persistency reader for AIDA XML format.
  class ReaderAIDA : public Reader {
  public:

    /// Singleton creation function
    static Reader& create() {
      static ReaderAIDA _instance;
      return _instance;
    }


    void read(std::istream& stream, std::vector<AnalysisObject*>& aos) {
      _readDoc(stream, aos);
    }

    // Include definitions of all read methods (all fulfilled by Reader::read(...))
    //#include "YODA/ReaderMethods.icc"



  protected:

    void _readDoc(std::istream& stream, vector<AnalysisObject*>& aos);
    //void readGenericAO(std::istream& stream);
    // virtual void readHisto(std::istream& stream, const Histo1D& h);
    // virtual void readProfile(std::istream& stream, const Profile1D& p);
    //void readScatter(std::istream& stream, const Scatter2D& p);


  private:

    /// Private constructor, since it's a singleton.
    ReaderAIDA() { }

  };


}

#endif
