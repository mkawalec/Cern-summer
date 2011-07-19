// -*- C++ -*-
#ifndef LWH_AIAnalysisFactory_H
#define LWH_AIAnalysisFactory_H

#ifndef LWH_USING_AIDA

#include <string>

/** @cond DONT_DOCUMENT_STRIPPED_DOWN_AIDA_INTERFACES */

namespace AIDA {

class IDataPointSetFactory;
class IFitFactory;
class IFunctionFactory;
class IPlotterFactory;
class ITupleFactory;
class ITreeFactory;
class ITree;
class IHistogramFactory;

class IAnalysisFactory {

public:

  virtual ~IAnalysisFactory() {};

  virtual ITreeFactory * createTreeFactory() = 0;
  virtual IHistogramFactory * createHistogramFactory(ITree & tree) = 0;
  virtual IDataPointSetFactory * createDataPointSetFactory(ITree &) = 0;
  virtual ITupleFactory * createTupleFactory(ITree &) = 0;
  virtual IFunctionFactory * createFunctionFactory(ITree &) = 0;
  virtual IFitFactory * createFitFactory() = 0;
  virtual IPlotterFactory * createPlotterFactory(int = 0, char * * = 0,
						 const std::string & = "",
						 const std::string & = "") = 0;

};

}

/** @endcond */

#else
#include "AIDA/IAnalysisFactory.h"
#endif

#endif /* LWH_AIAnalysisFactory_H */
