// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_Writer_h
#define YODA_Writer_h

#include "YODA/AnalysisObject.h"
#include "YODA/Histo1D.h"
#include "YODA/Profile1D.h"
#include "YODA/Scatter2D.h"
#include <string>
#include <fstream>

namespace YODA {


  /// Pure virtual base class for various output writers.
  class Writer {
  public:

    /// Virtual destructor
    virtual ~Writer() {}


    /// @name Writing a single analysis object.
    //@{

    /// Write out object @a ao to output stream @a stream.
    void write(std::ostream& stream, const AnalysisObject& ao);

    /// Write out object @a ao to file @a filename.
    void write(const std::string& filename, const AnalysisObject& ao);

    //@}


    /// @name Writing multiple analysis objects by collection.
    //@{

    /// Write out a collection of objects @a objs to output stream @a stream.
    void write(std::ostream& stream, const std::vector<AnalysisObject*>& aos) {
      write(stream, aos.begin(), aos.end());
    }
    /// Write out a collection of objects @a objs to file @a filename.
    void write(const std::string& filename, const std::vector<AnalysisObject*>& aos) {
      write(filename, aos.begin(), aos.end());
    }


    /// Write out a collection of objects @a objs to output stream @a stream.
    void write(std::ostream& stream, const std::list<AnalysisObject*>& aos) {
      write(stream, aos.begin(), aos.end());
    }
    /// Write out a collection of objects @a objs to file @a filename.
    void write(const std::string& filename, const std::list<AnalysisObject*>& aos) {
      write(filename, aos.begin(), aos.end());
    }


    /// Write out a collection of objects @a objs to output stream @a stream.
    void write(std::ostream& stream, const std::set<AnalysisObject*>& aos) {
      write(stream, aos.begin(), aos.end());
    }
    /// Write out a collection of objects @a objs to file @a filename.
    void write(const std::string& filename, const std::set<AnalysisObject*>& aos) {
      write(filename, aos.begin(), aos.end());
    }


    /// Write out a collection of objects @a objs to output stream @a stream.
    void write(std::ostream& stream, const std::deque<AnalysisObject*>& aos) {
      write(stream, aos.begin(), aos.end());
    }
    /// Write out a collection of objects @a objs to file @a filename.
    void write(const std::string& filename, const std::deque<AnalysisObject*>& aos) {
      write(filename, aos.begin(), aos.end());
    }

    //@}


    /// @name Writing multiple analysis objects by iterator range.
    //@{

    /// Write out the objects specified by start iterator @a begin and end
    /// iterator @a end to output stream @a stream.
    template <typename AOITER>
    void write(std::ostream& stream, const AOITER& begin, const AOITER& end) {
      writeHeader(stream);
      for (AOITER ipao = begin; ipao != end; ++ipao) {
        writeBody(stream, **ipao);
      }
      writeFooter(stream);
    }

    /// Write out the objects specified by start iterator @a begin and end
    /// iterator @a end to file @a filename.
    template <typename AOITER>
    void write(const std::string& filename,
               const AOITER& begin,
               const AOITER& end) {
      std::ofstream outstream;
      outstream.open(filename.c_str());
      write(outstream, begin, end);
      outstream.close();
    }

    //@}


  protected:

    /// Main writer elements
    virtual void writeHeader(std::ostream& stream) = 0;
    void writeBody(std::ostream& stream, const AnalysisObject& ao);
    virtual void writeFooter(std::ostream& stream) = 0;

    /// Specific AO type writer implementations
    virtual void writeHisto1D(std::ostream& os, const Histo1D& h) = 0;
    virtual void writeProfile1D(std::ostream& os, const Profile1D& p) = 0;
    virtual void writeScatter2D(std::ostream& os, const Scatter2D& s) = 0;

  };


}

#endif
