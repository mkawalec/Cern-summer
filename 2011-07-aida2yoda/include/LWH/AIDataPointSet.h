// -*- C++ -*-
#ifndef LWH_AIDataPointSet_H
#define LWH_AIDataPointSet_H

#ifndef LWH_USING_AIDA

/** @cond DONT_DOCUMENT_STRIPPED_DOWN_AIDA_INTERFACES */

namespace AIDA {

class IAnnotation;
class IDataPoint;

/**
 * Basic user-level interface class for holding and managing
 * a single set of "data points".
 *
 * @author The AIDA team (http://aida.freehep.org/)
 *
 */

  class IDataPointSet {

  public:
    virtual ~IDataPointSet() { /* nop */; }
    virtual IAnnotation & annotation() = 0;
    virtual const IAnnotation & annotation() const = 0;
    //virtual std::string title() const = 0;
    // virtual bool setTitle(const std::string & title) = 0;
    virtual int dimension() const = 0;
    virtual void clear() = 0;
    virtual int size() const = 0;
    virtual IDataPoint * point(int index) = 0;
    virtual bool setCoordinate(int coord, const std::vector<double>  & val, const std::vector<double>  & err) = 0;
    virtual bool setCoordinate(int coord, const std::vector<double>  & val, const std::vector<double>  & errp, const std::vector<double>  & errm) = 0;
    virtual const IDataPoint * point(int index) const = 0;
    virtual IDataPoint * addPoint() = 0;
    virtual bool addPoint(const IDataPoint & point) = 0;
    virtual bool removePoint(int index) = 0;
    virtual double lowerExtent(int coord) const = 0;
    virtual double upperExtent(int coord) const = 0;
    virtual bool scale(double scaleFactor) = 0;
    virtual bool scale(double scaleFactor, int coord) = 0;
    virtual bool scaleValues(double scaleFactor) = 0;
    virtual bool scaleErrors(double scaleFactor) = 0;
    virtual void * cast(const std::string & className) const = 0;


    ///////////////////////////////////


    /**
     * Get the main title.
     * @return The title.
     *
     */
    std::string title() const {
      return theTitle;
    }

    /**
     * Set the main title.
     * @param title The new title.
     * @return false If the title cannot be set.
     *
     */
    bool setTitle(const std::string & title) {
      theTitle = title;
      return true;
    }



    /**
     * Get the x-axis title.
     * @return The title.
     *
     */
    std::string xtitle() const {
      return theXTitle;
    }

    /**
     * Set the x-axis title.
     * @param title The new title.
     * @return false If the title cannot be set.
     *
     */
    bool setXTitle(const std::string & xtitle) {
      theXTitle = xtitle;
      return true;
    }



    /**
     * Get the y-axis title.
     * @return The title.
     *
     */
    std::string ytitle() const {
      return theYTitle;
    }

    /**
     * Set the y-axis title.
     * @param title The new title.
     * @return false If the title cannot be set.
     *
     */
    bool setYTitle(const std::string & ytitle) {
      theYTitle = ytitle;
      return true;
    }

    /**
     * Get the z-axis title.
     * @return The title.
     *
     */
    std::string ztitle() const {
      return theZTitle;
    }

    /**
     * Set the z-axis title.
     * @param title The new title.
     * @return false If the title cannot be set.
     *
     */
    bool setZTitle(const std::string & ztitle) {
      theZTitle = ztitle;
      return true;
    }

    /**
     * Get the z-axis title.
     * @return The title.
     *
     */
    std::string title(int i) const {
      switch ( i ) {
      case 0: return theXTitle;
      case 1: return theYTitle;
      case 2: return theZTitle;
      default: return "";
      }
    }

    /**
     * Set the <i>-axis title.
     * @param title The new title.
     * @return false If the title cannot be set.
     *
     */
    bool setTitle(int i, const std::string & title) {
      if ( i == 0 ) theXTitle = title;
      else if ( i == 1 ) theYTitle = title;
      else if ( i == 2 ) theZTitle = title;
      else return false;
      return true;
    }


  protected:
    std::string theTitle;
    std::string theXTitle;
    std::string theYTitle;
    std::string theZTitle;

  };


}

/** @endcond */

#else
#include "AIDA/IDataPointSet.h"
#endif

#endif /* LWH_AIDataPointSet_H */
