// -*- C++ -*-
#ifndef LWH_AnalysisFactory_H
#define LWH_AnalysisFactory_H
//
// This is the declaration of the AnalysisFactory class.
//

#include "AIAnalysisFactory.h"
#include "TreeFactory.h"
#include "HistogramFactory.h"
#include "DataPointSetFactory.h"
#include <set>

/**
 * The LWH namespace contains a Light-Weight Histogram package which
 * implements the most rudimentary histogramming facilities according
 * to the <a href="http://aida.freehep.org">AIDA</a> interface
 * specifications. Currently the only thing that is supported is
 * simple, equally binned, one dimensional histograms and data
 * points. It is mainly intended to be used in applications where one
 * needs to fill simple histograms and output them. With LWH it is
 * then possible to do this without the overhead of a full AIDA
 * implementation, but still having the option to use a full
 * implementation later on with minimal changes. Note also that since
 * LWH consists only of header files, the installation is trivial -
 * just put the header files where they can be found by your compiler.
 */
namespace LWH {

using namespace AIDA;

/**
 * The "master" factory from which other factories are obtained.
 * Typically accessed by:
 * <pre>IAnalysisFactory* af = AIDA_createAnalysisFactory();</pre>
 */
class AnalysisFactory: public IAnalysisFactory {

public:
  /// Destructor.
  virtual ~AnalysisFactory() {
    clear();
  }

  /**
   * Create an ITreeFactory.
   * @return The ITreeFactory.
   */
  ITreeFactory * createTreeFactory() {
    return new TreeFactory;
  }

  /**
   * Create an HistogramFactory.
   * @param tree The ITree which created histograms will be associated to.
   * @return     The IHistogramFactory.
   *
   */
  IHistogramFactory * createHistogramFactory(ITree & tree) {
    Tree & tr = dynamic_cast<Tree &>(tree);
    HistogramFactory * hf = new HistogramFactory(tr);
    histfacs.insert(hf);
    return hf;
  }

  /**
   * Not implemented in LWH.
   * @return     null pointer always.
   *
   */
  IDataPointSetFactory * createDataPointSetFactory(ITree & tree) {
    Tree & tr = dynamic_cast<Tree &>(tree);
    DataPointSetFactory * df = new DataPointSetFactory(tr);
    datafacs.insert(df);
    return df;
  }

  /**
   * Not implemented in LWH.
   * @return     null pointer always.
   */
  ITupleFactory * createTupleFactory(ITree &) {
    return 0;
  }

  /**
   * Not implemented in LWH.
   * @return     null pointer always.
   */
  IFunctionFactory * createFunctionFactory(ITree &) {
    return 0;
  }

  /**
   * Not implemented in LWH.
   * @return     null pointer always.
   */
  IPlotterFactory * createPlotterFactory(int = 0, char * * = 0,
					 const std::string & = "",
					 const std::string & = "") {
    return 0;
  }

  /**
   * Not implemented in LWH.
   * @return     null pointer always.
   */
  IFitFactory * createFitFactory() {
    return 0;
  }

private:

  /** Delete all produced factories. */
  void clear() {
    for ( std::set<HistogramFactory *>::iterator it = histfacs.begin();
	  it != histfacs.end(); ++it ) delete *it;
    for ( std::set<DataPointSetFactory *>::iterator it = datafacs.begin();
	  it != datafacs.end(); ++it ) delete *it;
    for ( std::set<TreeFactory *>::iterator it = treefacs.begin();
	  it != treefacs.end(); ++it ) delete *it;
    histfacs.clear();
    datafacs.clear();
    treefacs.clear();
  }

  /** The histogram factories. */
  std::set<HistogramFactory *> histfacs;

  /** The dataset factories. */
  std::set<DataPointSetFactory *> datafacs;

  /** The tree factories. */
  std::set<TreeFactory *> treefacs;

};

}

#endif /* LWH_AnalysisFactory_H */
