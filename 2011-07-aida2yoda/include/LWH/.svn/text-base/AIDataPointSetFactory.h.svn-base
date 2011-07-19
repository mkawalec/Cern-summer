// -*- C++ -*-
#ifndef LWH_AIDataPointSetFactory_H
#define LWH_AIDataPointSetFactory_H

#ifndef LWH_USING_AIDA

/** @cond DONT_DOCUMENT_STRIPPED_DOWN_AIDA_INTERFACES */

namespace AIDA {

class IDataPointSet;
class IHistogram1D;
class IHistogram2D;
class IProfile1D;

class IDataPointSetFactory {

public:
    virtual ~IDataPointSetFactory() { /* nop */; }
    virtual IDataPointSet *
    create(const std::string &, const std::string &, int ) = 0;
    virtual IDataPointSet * create(const std::string &, int) = 0;
    virtual IDataPointSet *
    createY(const std::string &, const std::string &,
	    const std::vector<double> &, const std::vector<double> &) = 0;
    virtual IDataPointSet *
    createY(const std::string &, const std::string &,
	    const std::vector<double> &, const std::vector<double> &,
	    const std::vector<double>  &) = 0;
    virtual IDataPointSet *
    createY(const std::string &, const std::vector<double> &,
	    const std::vector<double> &) = 0;
    virtual IDataPointSet *
    createY(const std::string &, const std::vector<double> &,
	    const std::vector<double> &, const std::vector<double> &) = 0;
    virtual IDataPointSet *
    createX(const std::string &, const std::string &,
	    const std::vector<double> &, const std::vector<double> &) = 0;
    virtual IDataPointSet *
    createX(const std::string &, const std::string &,
	    const std::vector<double> &, const std::vector<double> &,
	    const std::vector<double> &) = 0;
    virtual IDataPointSet *
    createX(const std::string &, const std::vector<double> &,
	    const std::vector<double> &) = 0;
    virtual IDataPointSet *
    createX(const std::string &, const std::vector<double> &,
	    const std::vector<double> &, const std::vector<double> &) = 0;
    virtual IDataPointSet *
    createXY(const std::string &, const std::string &,
	     const std::vector<double> &, const std::vector<double> &,
	     const std::vector<double> &, const std::vector<double> &,
	     const std::vector<double> &, const std::vector<double> &) = 0;
    virtual IDataPointSet *
    createXY(const std::string &, const std::string &,
	     const std::vector<double> &, const std::vector<double> &,
	     const std::vector<double> &, const std::vector<double> &) = 0;
    virtual IDataPointSet *
    createXY(const std::string &, const std::vector<double> &,
	     const std::vector<double> &, const std::vector<double> &,
	     const std::vector<double> &, const std::vector<double> &,
	     const std::vector<double> &) = 0;
    virtual IDataPointSet *
    createXY(const std::string &, const std::vector<double> &,
	     const std::vector<double> &, const std::vector<double> &,
	     const std::vector<double> &) = 0;
    virtual IDataPointSet *
    createXYZ(const std::string &, const std::string &,
	      const std::vector<double> &, const std::vector<double> &,
	      const std::vector<double> &, const std::vector<double> &,
	      const std::vector<double> &, const std::vector<double> &,
	      const std::vector<double> &, const std::vector<double> &,
	      const std::vector<double> &) = 0;
    virtual IDataPointSet *
    createXYZ(const std::string &, const std::string &,
	      const std::vector<double> &, const std::vector<double> &,
	      const std::vector<double> &, const std::vector<double> &,
	      const std::vector<double> &, const std::vector<double> &) = 0;
    virtual IDataPointSet *
    createXYZ(const std::string &, const std::vector<double> &,
	      const std::vector<double> &, const std::vector<double> &,
	      const std::vector<double> &, const std::vector<double> &,
	      const std::vector<double> &, const std::vector<double> &,
	      const std::vector<double> &, const std::vector<double> &) = 0;
    virtual IDataPointSet *
    createXYZ(const std::string &, const std::vector<double> &,
	      const std::vector<double> &, const std::vector<double> &,
	      const std::vector<double> &, const std::vector<double> &,
	      const std::vector<double> &) = 0;
    virtual IDataPointSet *
    createCopy(const std::string &, const IDataPointSet &) = 0;
    virtual bool destroy(IDataPointSet *) = 0;
    virtual IDataPointSet * create(const std::string &, const IHistogram1D &,
				   const std::string & = "") = 0;
    virtual IDataPointSet * create(const std::string &, const IHistogram2D &,
				   const std::string & = "") = 0;
    virtual IDataPointSet * create(const std::string &, const IProfile1D &,
				   const std::string & = "") = 0;

};

}

/** @endcond */

#else
#include "AIDA/IDataPointSetFactory.h"
#endif

#endif /* LWH_AIDataPointSetFactory_H */
