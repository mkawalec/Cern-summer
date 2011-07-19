// -*- C++ -*-
#ifndef LWH_AIHistogramFactory_H
#define LWH_AIHistogramFactory_H

#ifndef LWH_USING_AIDA

/** @cond DONT_DOCUMENT_STRIPPED_DOWN_AIDA_INTERFACES */

namespace AIDA {
  
  class ICloud1D;
  class ICloud2D;
  class ICloud3D;
  class IBaseHistogram;
  class IHistogram1D;
  class IHistogram2D;
  class IHistogram3D;
  class IProfile1D;
  class IProfile2D;
  class IDataPointSet;
  
  class IHistogramFactory {
    
  public:
    
    virtual ~IHistogramFactory() {}
    
    virtual bool destroy(IBaseHistogram * hist) = 0;

    virtual IHistogram1D *
    createHistogram1D(const std::string &, const std::string &,
                      int, double, double, const std::string & = "") = 0;
    virtual IHistogram1D *
    createHistogram1D(const std::string &, int, double, double) = 0;
    virtual IHistogram1D *
    createHistogram1D(const std::string &, const std::string & ,
                      const std::vector<double> &, const std::string & = "") = 0;
    virtual IHistogram1D *
    createCopy(const std::string &, const IHistogram1D &) = 0;
    virtual IHistogram1D * add(const std::string &,
                               const IHistogram1D &, const IHistogram1D &) = 0;
    virtual IHistogram1D * subtract(const std::string &, const IHistogram1D &,
                                    const IHistogram1D &) = 0;
    virtual IHistogram1D * multiply(const std::string &, const IHistogram1D &,
                                    const IHistogram1D &) = 0;
    virtual IDataPointSet * divide(const std::string &, const IHistogram1D &,
                                   const IHistogram1D &) = 0;



    virtual IProfile1D *
    createProfile1D(const std::string &, const std::string &,
                      int, double, double, const std::string & = "") = 0;
    virtual IProfile1D *
    createProfile1D(const std::string &, int, double, double) = 0;
    virtual IProfile1D *
    createProfile1D(const std::string &, const std::string & ,
                      const std::vector<double> &, const std::string & = "") = 0;
    virtual IProfile1D *
    createCopy(const std::string &, const IProfile1D &) = 0;
    // virtual IProfile1D * add(const std::string &,
    //                            const IProfile1D &, const IProfile1D &) = 0;
    // virtual IProfile1D * subtract(const std::string &, const IProfile1D &,
    //                                 const IProfile1D &) = 0;
    // virtual IProfile1D * multiply(const std::string &, const IProfile1D &,
    //                                 const IProfile1D &) = 0;
    // virtual IDataPointSet * divide(const std::string &, const IProfile1D &,
    //                                const IProfile1D &) = 0;

    virtual IHistogram2D *
    createHistogram2D(const std::string & path, const std::string & title,
		      int nx, double xlo, double xup,
		      int ny, double ylo, double yup,
		      const std::string & = "") = 0;

    virtual IHistogram2D *
    createHistogram2D(const std::string & pathAndTitle,
		      int nx, double xlo, double xup,
		      int ny, double ylo, double yup) = 0;

    virtual IHistogram2D *
    createHistogram2D(const std::string & path, const std::string & title,
		      const std::vector<double> & xedges,
		      const std::vector<double> & yedges,
		      const std::string & = "") = 0;

    virtual IHistogram2D *
    createCopy(const std::string & path, const IHistogram2D & hist) = 0;

  };
  
}

/** @endcond */

#else
#include "AIDA/IHistogramFactory.h"
#endif

#endif /* LWH_AIHistogramFactory_H */
