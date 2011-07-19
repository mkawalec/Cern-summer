#include "YODA/Histo1D.h"
#include <cmath>
#include <iostream>
#include <unistd.h>

using namespace std;
using namespace YODA;

bool compareHeight(const HistoBin1D& a, const HistoBin1D& b) {
  return a.height() < b.height();
}


int main() {

  Histo1D h(20, 0.0, 1.0);
  for (size_t n = 0; n < 1000; ++n) {
    const double num = rand()/static_cast<double>(RAND_MAX);
    //cout << "Filling with " << num << endl;
    h.fill(num);
  }

  cout << "Mean value = " << h.mean() << " +- " << h.stdDev() << endl;
  cout << "Total area = " << h.integral() << endl;

  const HistoBin1D& highestBin = *( max_element(h.bins().begin(), h.bins().end(), compareHeight) );
  const double maxHeight = highestBin.height();

  cout << "Histo:" << endl;
  for (vector<HistoBin1D>::const_iterator b = h.bins().begin(); b != h.bins().end(); ++b) {
    const int numElements = static_cast<int>(round(20 * b->height()/maxHeight));
    cout << string().insert(0, numElements, '=') << "  ";
    cout << (isatty(1) ? "\033[0;37m" : "")
         << b->height()
         << (isatty(1) ? "\033[0m" : "") << endl;
  }

  return EXIT_SUCCESS;
}
