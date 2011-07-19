// -*- C++ -*-
#ifndef RIVET_HistoHandler_HH
#define RIVET_HistoHandler_HH

#include "Rivet/Rivet.hh"
#include "Rivet/Tools/Logging.fhh"
#include "Rivet/Analysis.fhh"

namespace Rivet {

  /// Forward declaration of Histo base class.
  class AnalysisObject;


  /// @brief The projection handler is a central repository for histograms (and
  /// other analysis stats objects) to be used in a Rivet analysis run. This
  /// eliminates the need for analysis classes to contain large numbers of
  /// histogram pointer members, and allows histograms to be accessed via more
  /// user-friendly names than C++ variable names allow.
  ///
  /// The core of the HistoHandler design is that it is a singleton class,
  /// essentially a wrapper around a map of @c AnalysisObject*, indexed by a
  /// hash of the registering object and its local name for the registered
  /// projection.
  ///
  class HistoHandler {
  private:

    /// @name Construction. */
    //@{

    /// The standard constructor.
    HistoHandler() { }

    /// Private destructor means no inheritance from this class.
    ~HistoHandler();

    /// The assignment operator is hidden.
    HistoHandler& operator=(const HistoHandler&);

    /// The copy constructor is hidden.
    HistoHandler(const HistoHandler&);

    //@}


  public:

    /// Singleton getter function
    static HistoHandler& getInstance() {
      static HistoHandler _instance;
      return _instance;
    }


    ////////////////////////////////////////////////////////


  public:
    /// @name Histo registration. */
    //@{
    /// Copy an analysis object into a central collection and return the copy.
    const AnalysisObject* registerAnalysisObject(const Analysis& parent,
                                                 const AnalysisObject& histo,
                                                 const string& name);


    /// @name Histo retrieval. */
    //@{

    /// Retrieve a named histo for the given Analysis parent (const version).
    const AnalysisObject* getAnalysisObject(const Analysis& parent,
                                            const string& name) const {
      return _getAnalysisObject(parent, name);
    }


    /// Retrieve a named histo for the given Analysis parent (non-const version).
    AnalysisObject* getAnalysisObject(const Analysis& parent,
                                      const string& name) {
      return _getAnalysisObject(parent, name);
    }

    //@}


    /// Histo clearing method: deletes all known histos and empties the
    /// reference collections.
    void clear();


  private:

    AnalysisObject* _getAnalysisObject(const Analysis& parent,
                                             const string& name) const;

    /// Get a logger.
    Log& getLog() const;


  private:

    /// Typedef for histo pointer, to allow conversion to a smart pointer in this context.
    typedef const AnalysisObject* HistoHandle;

    /// Typedef for a vector of histo pointers.
    typedef vector<HistoHandle> HistoHandles;

    /// @brief Typedef for the structure used to contain named histos for a
    /// particular containing Analysis.
    typedef map<const string, HistoHandle> NamedHistos;

    /// Structure used to map a containing Analysis to its set of histos.
    typedef map<const Analysis*, NamedHistos> NamedHistosMap;

    /// Core data member, associating a given Analysis to its histos.
    NamedHistosMap _namedhistos;
  };


}

#endif
