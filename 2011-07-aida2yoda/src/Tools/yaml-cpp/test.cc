#include <fstream>
#include <string>
#include <iostream>
#include "yaml.h"

using namespace std;

int main()
{
  ifstream io("test.yaml");
  YAML::Parser parser(io);

  YAML::Node doc;
  parser.GetNextDocument(doc);
  
  const YAML::Node& things = doc["things"];
  string s;
  for (YAML::Iterator it = things.begin(); it != things.end(); ++it) {
    *it >> s;
    cout << "&&& " << s << " &&&" << endl;
  }

  const YAML::Node& stuff = doc["stuff"];
  int a;
  for (YAML::Iterator it = stuff.begin(); it != stuff.end(); ++it) {
    *it >> a;
    cout << "%%% " << a << " %%%" << endl;
  }

  const YAML::Node& desc = doc["desc"];
  string d;
  desc >> d;
  cout << "*** " << d << " ***" << endl;

  parser.GetNextDocument(doc);

  return 0;
}
