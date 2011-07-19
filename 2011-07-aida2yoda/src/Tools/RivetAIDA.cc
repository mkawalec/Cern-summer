#include "Rivet/RivetAIDA.hh"
#include "Rivet/Rivet.hh"
#include "Rivet/RivetBoost.hh"
#include "Rivet/Tools/Utils.hh"
#include "Rivet/Tools/RivetPaths.hh"
#include "LWH/AnalysisFactory.h"
#include "TinyXML/tinyxml.h"
#include <sstream>
#include <stdexcept>
using namespace std;

namespace Rivet {


  /// Get an AIDA system (LWH impl.)
  AIDA::IAnalysisFactory* createAnalysisFactory() {
    return new LWH::AnalysisFactory();
  }


  string getDatafilePath(string papername) {
    const string path =  findAnalysisRefFile(papername + ".aida");
    if (!path.empty()) return path;
    throw Rivet::Error("Couldn't find ref data file '" + papername + ".aida" +
                       " in $RIVET_REF_PATH, " + getRivetDataPath() + ", or .");
    return "";
  }


  map<string, vector<DPSXYPoint> > getDPSXYValsErrs(string papername) {
    // Get filename
    const string xmlfile = getDatafilePath(papername);

    // Open AIDA XML file
    TiXmlDocument doc(xmlfile);
    doc.LoadFile();
    if (doc.Error()) {
      string err = "Error in " + string(doc.Value());
      err += ": " + string(doc.ErrorDesc());
      cerr << err << endl;
      throw Error(err);
    }

    // Return value, to be populated
    map<string, vector<DPSXYPoint> > rtn;

    try {
      // Walk down tree to get to the <paper> element
      const TiXmlNode* aidaN = doc.FirstChild("aida");
      if (!aidaN) throw Error("Couldn't get <aida> root element");
      for (const TiXmlNode* dpsN = aidaN->FirstChild("dataPointSet"); dpsN; dpsN = dpsN->NextSibling()) {
        const TiXmlElement* dpsE = dpsN->ToElement();
        const string plotname = dpsE->Attribute("name");
        const string plotpath = dpsE->Attribute("path");
        /// Check path to make sure that this is a reference histogram.
        if (plotpath.find("/REF") != 0) {
          cerr << "Skipping non-reference histogram " << plotname << endl;
          continue;
        }

        /// @todo Check that "path" matches filename
        vector<DPSXYPoint> points;
        for (const TiXmlNode* dpN = dpsN->FirstChild("dataPoint"); dpN; dpN = dpN->NextSibling()) {
          const TiXmlNode* xMeasN = dpN->FirstChild("measurement");
          const TiXmlNode* yMeasN = xMeasN->NextSibling();
          if (xMeasN && yMeasN)  {
            const TiXmlElement* xMeasE = xMeasN->ToElement();
            const TiXmlElement* yMeasE = yMeasN->ToElement();
            const string xcentreStr   = xMeasE->Attribute("value");
            const string xerrplusStr  = xMeasE->Attribute("errorPlus");
            const string xerrminusStr = xMeasE->Attribute("errorMinus");
            const string ycentreStr   = yMeasE->Attribute("value");
            const string yerrplusStr  = yMeasE->Attribute("errorPlus");
            const string yerrminusStr = yMeasE->Attribute("errorMinus");
            //if (!centreStr) throw Error("Couldn't get a valid bin centre");
            //if (!errplusStr) throw Error("Couldn't get a valid bin err+");
            //if (!errminusStr) throw Error("Couldn't get a valid bin err-");
            istringstream xssC(xcentreStr);
            istringstream xssP(xerrplusStr);
            istringstream xssM(xerrminusStr);
            istringstream yssC(ycentreStr);
            istringstream yssP(yerrplusStr);
            istringstream yssM(yerrminusStr);
            double xcentre, xerrplus, xerrminus, ycentre, yerrplus, yerrminus;
            xssC >> xcentre; xssP >> xerrplus; xssM >> xerrminus;
            yssC >> ycentre; yssP >> yerrplus; yssM >> yerrminus;
            //cout << "  " << centre << " + " << errplus << " - " << errminus << endl;
            DPSXYPoint pt(xcentre, xerrminus, xerrplus, ycentre, yerrminus, yerrplus);
            points.push_back(pt);
          } else {
            cerr << "Couldn't get <measurement> tag" << endl;
            /// @todo Throw an exception here?
          }
        }

        // Add to the map
        rtn[plotname] = points;
      }

    }
    // Write out the error
    /// @todo Rethrow as a general XML failure.
    catch (std::exception& e) {
      cerr << e.what() << endl;
      throw;
    }

    // Return
    return rtn;
  }

  map<string, vector<DPSXPoint> > getDPSXValsErrs(string papername) {
    // Get filename
    const string xmlfile = getDatafilePath(papername);

    // Open AIDA XML file
    TiXmlDocument doc(xmlfile);
    doc.LoadFile();
    if (doc.Error()) {
      string err = "Error in " + string(doc.Value());
      err += ": " + string(doc.ErrorDesc());
      cerr << err << endl;
      throw Error(err);
    }

    // Return value, to be populated
    map<string, vector<DPSXPoint> > rtn;

    try {
      // Walk down tree to get to the <paper> element
      const TiXmlNode* aidaN = doc.FirstChild("aida");
      if (!aidaN) throw Error("Couldn't get <aida> root element");
      for (const TiXmlNode* dpsN = aidaN->FirstChild("dataPointSet"); dpsN; dpsN = dpsN->NextSibling()) {
        const TiXmlElement* dpsE = dpsN->ToElement();
        const string plotname = dpsE->Attribute("name");
        const string plotpath = dpsE->Attribute("path");
        /// Check path to make sure that this is a reference histogram.
        if (plotpath.find("/REF") != 0) {
          cerr << "Skipping non-reference histogram " << plotname << endl;
          continue;
        }

        /// @todo Check that "path" matches filename
        vector<DPSXPoint> points;
        for (const TiXmlNode* dpN = dpsN->FirstChild("dataPoint"); dpN; dpN = dpN->NextSibling()) {
          const TiXmlNode* xMeasN = dpN->FirstChild("measurement");
          if (xMeasN) {
            const TiXmlElement* xMeasE = xMeasN->ToElement();
            const string centreStr = xMeasE->Attribute("value");
            const string errplusStr = xMeasE->Attribute("errorPlus");
            const string errminusStr = xMeasE->Attribute("errorMinus");
            //if (!centreStr) throw Error("Couldn't get a valid bin centre");
            //if (!errplusStr) throw Error("Couldn't get a valid bin err+");
            //if (!errminusStr) throw Error("Couldn't get a valid bin err-");
            istringstream ssC(centreStr);
            istringstream ssP(errplusStr);
            istringstream ssM(errminusStr);
            double centre, errplus, errminus;
            ssC >> centre; ssP >> errplus; ssM >> errminus;
            //cout << "  " << centre << " + " << errplus << " - " << errminus << endl;
            DPSXPoint pt(centre, errminus, errplus);
            points.push_back(pt);
          } else {
            cerr << "Couldn't get <measurement> tag" << endl;
            /// @todo Throw an exception here?
          }
        }

        // Add to the map
        rtn[plotname] = points;
      }

    }
    // Write out the error
    /// @todo Rethrow as a general XML failure.
    catch (std::exception& e) {
      cerr << e.what() << endl;
      throw;
    }

    // Return
    return rtn;
  }



  map<string, BinEdges> getBinEdges(string papername) {
    const map<string, vector<DPSXPoint> > xpoints = getDPSXValsErrs(papername);
    return getBinEdges(xpoints);
  }



  map<string, BinEdges> getBinEdges(const map<string, vector<DPSXPoint> >& xpoints) {

    map<string, BinEdges> rtn;
    for (map<string, vector<DPSXPoint> >::const_iterator dsit = xpoints.begin(); dsit != xpoints.end(); ++dsit) {
      const string plotname = dsit->first;
      list<double> edges;
      foreach (const DPSXPoint& xpt, dsit->second) {
        const double lowedge = xpt.val - xpt.errminus;
        const double highedge = xpt.val + xpt.errplus;
        edges.push_back(lowedge);
        edges.push_back(highedge);
      }

      //cout << "*** " << edges << endl;

      // Remove duplicates (the careful testing is why we haven't used a set)
      //cout << edges.size() << " edges -> " << edges.size()/2 << " bins" << endl;
      for (list<double>::iterator e = edges.begin(); e != edges.end(); ++e) {
        list<double>::iterator e2 = e;
        while (e2 != edges.end()) {
          if (e != e2) {
            if (fuzzyEquals(*e, *e2)) {
              edges.erase(e2++);
            }
          }
          ++e2;
        }
      }
      //cout << edges.size() << " edges after dups removal (should be #bins+1)" << endl;
      //cout << "@@@ " << edges << endl;

      // Add to the map
      rtn[plotname] = BinEdges(edges.begin(), edges.end());
    }

    // Return
    return rtn;
  }


}
