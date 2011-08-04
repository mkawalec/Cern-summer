// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_AnalysisObject_h
#define YODA_AnalysisObject_h

#include "YODA/Exceptions.h"
#include "YODA/Config/BuildConfig.h"
#include <string>
#include <map>

namespace YODA {

  /// AnalysisObject is the base class for histograms and scatters
  class AnalysisObject {

  public:

    /// Collection type for annotations, as a string-string map.
    typedef std::map<std::string, std::string> Annotations;


    /// @name Creation and destruction
    //@{

    /// Default constructor
    AnalysisObject() { }

    /// Constructor giving a type, a path and an optional title
    AnalysisObject(const std::string& type, const std::string& path, const std::string& title="") {
      setAnnotation("Type", type);
      setPath(path);
      setTitle(title);
    }

    /// Constructor giving a type, a path, another AO to copy annotation from, and an optional title
    AnalysisObject(const std::string& type, const std::string& path,
                   const AnalysisObject& ao, const std::string& title="") {
      setAnnotations(ao.annotations());
      setAnnotation("Type", type);
      setPath(path);
      setTitle(title);
    }

    /// Default destructor
    virtual ~AnalysisObject() { }

    /// Reset this analysis object
    virtual void reset() = 0;

    //@}


  public:

    ///@name Annotations
    //@{

    /// @brief Add or set an annotation by name
    /// Note: Templated on arg type, but stored as a string.
    template <typename T>
    void setAnnotation(const std::string& name, const T& value) {
      _annotations[name] = boost::lexical_cast<std::string>(value);
    }

    /// @brief Add or set an annotation by name
    /// Note: Templated on arg type, but stored as a string. Synonym for setAnnotation
    template <typename T>
    void addAnnotation(const std::string& name, const T& value) {
      setAnnotation(name, value);
    }

    /// Check if an annotation is defined
    bool hasAnnotation(const std::string& name) const {
      return _annotations.find(name) != _annotations.end();
    }

    /// Get all the annotations (as const ref)
    const Annotations& annotations() const {
      return _annotations;
    }

    /// Set all annotations at once
    void setAnnotations(const Annotations& anns) {
      _annotations = anns;
    }

    /// @brief Get an annotation by name (as a string)
    const std::string& annotation(const std::string& name) const {
      Annotations::const_iterator v = _annotations.find(name);
      if (v == _annotations.end()) {
        std::string missing = "YODA::AnalysisObject: No annotation named " + name;
        throw AnnotationError(missing);
      }
      return v->second;
    }

    /// @brief Get an annotation by name (copied to another type)
    /// Note: templated on return type, with default as string
    template <typename T>
    const T annotation(const std::string& name) const {
      std::string s = annotation(name);
      return boost::lexical_cast<T>(s);
    }


    /// Delete an annotation by name
    void rmAnnotation(const std::string& name) {
      _annotations.erase(name);
    }

    /// Delete an annotation by name
    void clearAnnotations() {
      _annotations.clear();
    }

    //@}


    /// @name Standard annotations
    //@{

    /// Get the AO title.
    /// Returns a null string if undefined, rather than throwing an exception cf. the Title annotation.
    const std::string title() const {
      try {
        return annotation("Title");
      } catch (AnnotationError& ae) {
        return "";
      }
    }

    /// Set the AO title
    void setTitle(const std::string& title) {
      setAnnotation("Title", title);
    }

    /// Get the AO path.
    /// Returns a null string if undefined, rather than throwing an exception cf. the Title annotation.
    const std::string path() const {
      try {
        return annotation("Path");
      } catch (AnnotationError& ae) {
        return "";
      }
    }

    /// Set the AO path
    void setPath(const std::string& path) {
      if (path.length() > 0 && path.find("/") != 0) {
        throw AnnotationError("Histo paths must start with a slash (/) character.");
      }
      setAnnotation("Path", path);
    }

    //@}


  public:

    /// @name Persistency hooks
    //@{

    /// @todo Maybe make these private, and make Writer a friend of AO

    /// Get name of the analysis object type, for persistency
    virtual std::string _aotype() const {
      return annotation("Type");
    }

    //@}


  private:

    /// The annotations indexed by name
    std::map<std::string,std::string> _annotations;

  };


}

#endif // YODA_AnalysisObject_h
