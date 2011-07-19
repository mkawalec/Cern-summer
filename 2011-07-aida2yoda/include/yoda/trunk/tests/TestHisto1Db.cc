#include "YODA/Histo1D.h"
#include "YODA/WriterAIDA.h"
#include "YODA/WriterYODA.h"
#include "YODA/ReaderAIDA.h"
#include <cmath>
#include <vector>
#include <fstream>
// #include <unistd.h>

using namespace std;
using namespace YODA;


int main() {

  Histo1D h1(20, 0.0, 1.0);
  h1.setPath("/MyHisto1");
  Histo1D h2(40, 0.0, 1.0, "/MyHisto2");
  for (size_t n = 0; n < 2000; ++n) {
    const double num = rand()/static_cast<double>(RAND_MAX);
    //cout << "Filling with " << num << endl;
    h1.fill(num);
    h2.fill(num);
  }

  /// @todo Test equivalence of statistics between two histos with different binnings

  /// @todo Also test with another histo whose range is incomplete, to make sure
  /// that the under/overflows are working

  /// Write one histo out to stdout
  WriterYODA::write(cout, h1);

  /// Write two histos out to file
  vector<AnalysisObject*> hs;
  hs.push_back(&h1);
  hs.push_back(&h2);
  WriterAIDA::write("test.aida", hs);
  WriterAIDA::write("test.aida", hs.begin(), hs.end());

  vector<AnalysisObject*> hs2 = ReaderAIDA::create().read("test.aida");
  cout << hs2.size() << endl;
  assert(hs2.size() == 2);
  for (vector<AnalysisObject*>::const_iterator i = hs2.begin(); i != hs2.end(); ++i) {
    cout << (*i)->_aotype() << endl;
    // if ((*i)->_aotype() == "Histo1D") {

    // }
  }

  return EXIT_SUCCESS;
}
