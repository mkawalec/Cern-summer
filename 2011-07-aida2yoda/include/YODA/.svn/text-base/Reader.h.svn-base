// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_Reader_h
#define YODA_Reader_h

#include "YODA/AnalysisObject.h"
#include "YODA/Histo1D.h"
#include "YODA/Profile1D.h"
#include "YODA/Scatter2D.h"
#include <string>
#include <fstream>
#include <vector>

namespace YODA {


  /// Pure virtual base class for various output writers.
  class Reader {
  public:

    /// Virtual destructor
    virtual ~Reader() {}


    /// @name Reading multiple analysis objects,
    //@{

    /// @brief Read in a collection of objects @a objs from output stream @a stream.
    /// This version fills (actually, appends to) a supplied vector, avoiding copying,
    /// and is hence CPU efficient.
    virtual void read(std::istream& stream, std::vector<AnalysisObject*>& aos) = 0;

    /// @brief Read in a collection of objects from output stream @a stream.
    /// This version returns a vector by value, involving copying, and is hence less
    /// CPU efficient than the alternative version where a vector is filled by reference.
    std::vector<AnalysisObject*> read(std::istream& stream) {
      std::vector<AnalysisObject*> rtn;
      read(stream, rtn);
      return rtn;
    }

    /// @brief Read in a collection of objects @a objs from file @a filename.
    /// This version fills (actually, appends to) a supplied vector, avoiding copying,
    /// and is hence CPU efficient.
    void read(const std::string& filename, std::vector<AnalysisObject*>& aos) {
      std::ifstream instream;
      instream.open(filename.c_str());
      read(instream, aos);
      instream.close();
    }

    /// @brief Read in a collection of objects from output stream @a stream.
    /// This version returns a vector by value, involving copying, and is hence less
    /// CPU efficient than the alternative version where a vector is filled by reference.
    std::vector<AnalysisObject*> read(const std::string& filename) {
      std::vector<AnalysisObject*> rtn;
      read(filename, rtn);
      return rtn;
    }

    //@}



  protected:
    // virtual void readGenericAO(std::istream& stream) = 0;
    // // virtual void readHisto(std::istream& stream, const Histo1D& h) = 0;
    // // virtual void readProfile(std::istream& stream, const Profile1D& p) = 0;
    // virtual void readScatter(std::istream& stream, const Scatter2D& p) = 0;

  };


}

#endif
