#include "YODA/Utils/sortedvector.h"
#include <iostream>
#include <cstdlib>
#include <set>

using namespace std;
using namespace YODA;

int main() {
  Utils::sortedvector<int> sv;
  sv.insert(1);
  sv.insert(5);
  sv.insert(3);
  sv.insert(2);
  sv.insert(4);

  // for (utils::sortedvector<int>::const_iterator it = sv.begin(); it != sv.end(); ++it) {
  //   cout << *it << endl;
  // }

  cout << "sv[3]: " << sv[3] << " == 4: "
       << boolalpha << (sv[3] == 4)
       << endl;

  return (sv[3] == 4) ? EXIT_SUCCESS : EXIT_FAILURE;
}
