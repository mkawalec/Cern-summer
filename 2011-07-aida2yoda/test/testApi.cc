#include "Rivet/AnalysisHandler.hh"
#include "HepMC/GenEvent.h"
#include "HepMC/IO_GenEvent.h"

using namespace std;

int main() {
  // New type
  Rivet::AnalysisHandler rivet;

  // Specify the analyses to be used
  rivet.addAnalysis("EXAMPLE");
  // rivet.addAnalysis("D0_2008_S7554427");

  //vector<string> moreanalyses(1, "D0_2007_S7075677");
  vector<string> moreanalyses(1, "MC_JETS");
  rivet.addAnalyses(moreanalyses);

  // Initialise: obsolete, but allowed for compatibility
  rivet.init();

  std::istream* file = new std::fstream("testApi.hepmc", std::ios::in);
  HepMC::IO_GenEvent hepmcio(*file);
  HepMC::GenEvent* evt = hepmcio.read_next_event();
  double sum_of_weights = 0.0;
  while (evt) {
    // Analyse current event
    rivet.analyze(*evt);
    sum_of_weights += evt->weights()[0];

    // Clean up and get next event
    delete evt; evt = 0;
    hepmcio >> evt;
  }
  delete file; file = 0;

  rivet.setCrossSection(1.0);
  rivet.setSumOfWeights(sum_of_weights); //< Not necessary, but allowed
  rivet.finalize();
  rivet.writeData("out.aida");

  return 0;
}
