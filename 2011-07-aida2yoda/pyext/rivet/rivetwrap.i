%module rivetwrap

%{
  #define SWIG_FILE_WITH_INIT
  #include "Rivet/Analysis.hh"
  #include "Rivet/AnalysisHandler.hh"
  #include "Rivet/AnalysisLoader.hh"
  #include "Rivet/AnalysisInfo.hh"
  #include "Rivet/Run.hh"
  #include "Rivet/Tools/Logging.hh"
  #include "Rivet/Event.hh"
  #include "Rivet/Particle.hh"
  #include "Rivet/ParticleName.hh"
  #include "Rivet/Projections/Beam.hh"
%}

// STL stuff
%include "std_string.i"
%include "std_vector.i"
%include "std_pair.i"
%include "std_map.i"
%template(StrList) std::vector<std::string>;
%template(DblPair) std::pair<double, double>;
%template(DblPairList) std::vector< std::pair<double, double> >;

// Histo format enum
%include "Rivet/HistoFormat.hh"

// Particle ID stuff
%include "Rivet/Particle.fhh"
%include "Rivet/ParticleName.hh"
%template(PdgIdPair) std::pair<Rivet::PdgId,Rivet::PdgId>;
%template(PdgIdPairList) std::vector<Rivet::PdgIdPair>;

// Logging interface
// Not mapping whole log interface, since we only want to be able to set log levels.
//%template(LogLevelMap) std::map<std::string, int>;
%ignore operator<<;
namespace Rivet {
  %rename(setLogLevel) Log::setLevel(const std::string&, int);
  class Log {
  public:
    enum Level {
      TRACE = 0, DEBUG = 10, INFO = 20, WARN = 30, WARNING = 30, ERROR = 40, CRITICAL = 50, ALWAYS = 50
    };
    static void setLevel(const std::string& name, int level);
  protected:
    Log(const std::string& name);
    Log(const std::string& name, int level);
  };
}
//%include "Rivet/Tools/Logging.hh"

// Rivet search paths
%include "Rivet/Tools/RivetPaths.hh"

// Main Rivet class mappings
namespace Rivet {

  std::string version();


  class Event {
    Event();
    Event(const HepMC::GenEvent&);
    const HepMC::GenEvent& genEvent() const;
    double weight() const;
  };

  class Particle {
    Particle();
    bool hasGenParticle() const;
    const HepMC::GenParticle& genParticle() const;
    const PdgId pdgId() const;
    const double mass() const;
    const double energy() const;
  };

  ParticlePair beams(const Event& e);

  PdgIdPair beamIds(const HepMC::GenEvent& e) {
    return beamIds(Event(e));
  }

  double sqrtS(const Event& e);

  // std::string toBeamsString(const PdgIdPair& pair);
  const std::string& toParticleName(PdgId p);
  PdgId toParticleId(const std::string& pname);


  // Mapping of just the metadata parts of the Analysis API
  class Analysis {
  public:
    virtual std::string name() const;
    virtual std::string spiresId() const;
    virtual std::string summary() const;
    virtual std::string description() const;
    virtual std::string runInfo() const;
    virtual std::string experiment() const;
    virtual std::string collider() const;
    virtual std::string year() const;
    virtual const std::vector<PdgIdPair>& requiredBeams() const;
    virtual const std::vector<std::pair<double,double> >& requiredEnergies() const;
    virtual std::vector<std::string> authors() const;
    virtual std::vector<std::string> references() const;
    virtual std::vector<std::string> todos() const;
    virtual std::string status() const;
    virtual std::string bibKey() const;
    virtual std::string bibTeX() const;
    virtual const bool isCompatible(PdgId beam1, PdgId beam2, double e1, double e2) const;
    virtual const bool isCompatible(const PdgIdPair& beamids, const std::pair<double, double>& beamenergies) const;
    virtual const bool isCompatible(const ParticlePair& beams) const;
    //AnalysisHandler& handler() const;
    bool needsCrossSection() const;
  private:
    Analysis();
  };


  class AnalysisHandler {
  public:
    AnalysisHandler(const std::string& runname);
    std::string runName() const;
    size_t numEvents() const;
    double sumOfWeights() const;
    double sqrtS() const;
    const ParticlePair& beams() const;
    const PdgIdPair beamIds() const;
    std::vector<std::string> analysisNames();
    AnalysisHandler& addAnalysis(const std::string& analysisname);
    AnalysisHandler& addAnalyses(const std::vector<std::string>& analysisnames);
    AnalysisHandler& removeAnalysis(const std::string& analysisname);
    AnalysisHandler& removeAnalyses(const std::vector<std::string>& analysisnames);
    void init(const HepMC::GenEvent& event);
    void analyze(const HepMC::GenEvent& event);
    void finalize();
    bool needCrossSection();
    AnalysisHandler& setCrossSection(double xs);
    double crossSection();
    void writeData(const std::string& filename);
  };


  class AnalysisLoader {
  public:
    static std::vector<std::string> analysisNames();
    static Analysis* getAnalysis(const std::string& analysisname);
  };


}

%include "Rivet/Run.hh"
