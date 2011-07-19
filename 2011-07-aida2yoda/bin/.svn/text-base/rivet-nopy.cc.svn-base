#include "Rivet/AnalysisHandler.hh"
#include "HepMC/IO_GenEvent.h"

using namespace std;

int main(int argc, char** argv) {
  if (argc < 2) {
    cerr << "Usage: " << argv[0] << " <hepmcfile> <ana1> [<ana2> ...]" << endl;
    return 1;
  }

  Rivet::AnalysisHandler ah;
  for (int i = 2; i < argc; ++i) {
    ah.addAnalysis(argv[i]);
  }

  std::istream* file = new std::fstream(argv[1], std::ios::in);
  HepMC::IO_GenEvent hepmcio(*file);
  HepMC::GenEvent* evt = hepmcio.read_next_event();
  while (evt) {
    ah.analyze(*evt);
    delete evt; evt = 0;
    hepmcio >> evt;
  }
  delete file; file = 0;

  ah.setCrossSection(1.0);
  ah.finalize();
  ah.writeData("out.aida");

  return 0;
}
