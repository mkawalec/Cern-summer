// -*- C++ -*-
#ifndef RIVET_AnalysisBuilder_HH
#define RIVET_AnalysisBuilder_HH

#include "Rivet/Rivet.hh"
#include "Rivet/Analysis.fhh"
#include "Rivet/AnalysisLoader.hh"
#include "Rivet/Tools/Logging.fhh"

namespace Rivet {


  /// @cond ANALYSIS_PLUGIN_DETAILS

  /// @brief Interface for analysis builders
  class AnalysisBuilderBase {
  public:
    AnalysisBuilderBase() { }
    virtual ~AnalysisBuilderBase() { }

    virtual Analysis* mkAnalysis() const = 0;

    const string name() const {
      Analysis* a = mkAnalysis();
      string rtn = a->name();
      delete a;
      return rtn;
    }

  protected:
    void _register() {
      AnalysisLoader::_registerBuilder(this);
    }
  };


  /// @brief Self-registering analysis plugin builder
  template <typename T>
  class AnalysisBuilder : public AnalysisBuilderBase {
  public:
    AnalysisBuilder() {
      _register();
    }

    Analysis* mkAnalysis() const {
      return new T();
    }
  };

  /// @endcond

}

#endif
