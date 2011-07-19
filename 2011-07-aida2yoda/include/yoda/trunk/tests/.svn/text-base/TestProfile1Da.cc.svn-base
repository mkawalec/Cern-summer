#include "YODA/Profile1D.h"
#include <cmath>
#include <iostream>
#include <unistd.h>

using namespace std;
using namespace YODA;


int main() {

  Profile1D h(20, 0.0, 1.0);
  for (size_t n = 0; n < 10000; ++n) {
    const double x = rand()/static_cast<double>(RAND_MAX);
    const double y = rand()/static_cast<double>(RAND_MAX) * 20 * x;
    h.fill(x, y, 2);
  }

  const vector<ProfileBin1D>& bins = h.bins();
  for (vector<ProfileBin1D>::const_iterator b = bins.begin(); b != bins.end(); ++b) {
    cout << b->mean() << ", " << b->stdDev() << ", " << b->stdErr() << endl;
  }

  return EXIT_SUCCESS;
}
