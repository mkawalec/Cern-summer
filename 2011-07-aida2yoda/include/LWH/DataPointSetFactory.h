// -*- C++ -*-
#ifndef LWH_DataPointSetFactory_H
#define LWH_DataPointSetFactory_H
//
// This is the declaration of the DataPointSetFactory class.
//

#include "AIDataPointSetFactory.h"
#include "DataPointSet.h"
#include "Histogram1D.h"
#include "Histogram2D.h"
#include "Profile1D.h"
#include "Tree.h"
#include <string>
#include <stdexcept>

namespace LWH {

using namespace AIDA;

/**
 * Basic user-level interface for creating a factory
 * of IDataPointSet. The created objects are assumed to be
 * managed by the tree which is associated to the factory.
 */
class DataPointSetFactory: public IDataPointSetFactory {

public:

  /**
   * Standard constructor.
   */
  DataPointSetFactory(Tree & t)
    : tree(&t) {}

  /**
   * Destructor.
   */
  virtual ~DataPointSetFactory() {}

  /**
   * Create an empty IDataPointSet.
   * @param path  The path of the IDataPointSet. The path can either
   *              be a relative or full path.
   *              ("/folder1/folder2/dataName" and "../folder/dataName"
   *              are valid paths). All the directories in the path
   *              must exist. The characther `/` cannot be used in
   *              names; it is only used to delimit directories within
   *		    paths.
   * @param title The title of the IDataPointSet.
   * @param dim   The dimension of the IDataPoints that can be stored
   *              in the set.
   * @return      The newly created IDataPointSet.
   */
  virtual IDataPointSet *
  create(const std::string & path, const std::string & title, int dim) {
    DataPointSet * dset = new DataPointSet(dim);
    dset->setTitle(title);
    if ( !tree->insert(path, dset) ) {
      delete dset;
      dset = 0;
      throw std::runtime_error("LWH couldn't create DataPointSet '"
			       + title + "'." );
    }
    return dset;
  }

  /**
   * Create an empty IDataPointSet.
   * @param pathAndTitle The path of the IDataPointSet. The path can either be
   *                     a relative or full path. The last part of the path is
   *                     used as the title. ("/folder1/folder2/dataTitle" and
   *                     "../folder/dataTitle" are valid paths).
   *                     All the directories in the path must exist. The
   *                     characther `/` cannot be used in names; it is only
   *                     used to delimit directories within paths.
   * @param dim          The dimension of the IDataPoints that can be stored
   *                     in the set.
   * @return             The newly created IDataPointSet.
   */
  virtual IDataPointSet * create(const std::string & pathAndTitle, int dim) {
    std::string title = pathAndTitle.substr(pathAndTitle.rfind('/') + 1);
    return create(pathAndTitle, title, dim);
  }

  /**
   * Create a two dimensional IDataPointSet providing the data along y (the x
   * value is the index of the y value in the array).
   * @param path  The path of the IDataPointSet. The path can either be a
   *              relative or full path. ("/folder1/folder2/dataTitle" and
   *              "../folder/dataTitle" are valid paths). All the directories
   *              in the path must exist. The characther `/` cannot be used
   *              in names; it is only used to delimit directories within paths.
   * @param title The title of the IDataPointSet.
   * @param y     The array of the y values
   * @param ey    The array with the symmetric errors on y
   * @return      The created IDataPointSet.
   */
  virtual IDataPointSet *
  createY(const std::string & path, const std::string & title,
	  const std::vector<double> & y, const std::vector<double> & ey) {
    return createY(path, title, y, ey, ey);
  }

  /**
   * Create a two dimensional IDataPointSet providing the data along y (the x
   * value is the index of the y value in the array).
   * @param path  The path of the IDataPointSet. The path can either be a
   *              relative or full path. ("/folder1/folder2/dataTitle" and
   *              "../folder/dataTitle" are valid paths). All the directories
   *              in the path must exist. The characther `/` cannot be used
   *              in names; it is only used to delimit directories within paths.
   * @param title The title of the IDataPointSet.
   * @param y     The array of the y values
   * @param eyp   The array with the plus errors on y
   * @param eym   The array with the minus errors on y
   * @return      The created IDataPointSet.
   */
  virtual IDataPointSet *
  createY(const std::string & path, const std::string & title,
	  const std::vector<double> & y, const std::vector<double> & eyp,
	  const std::vector<double>  & eym) {
    IDataPointSet * dset = create(path, title, 2);
    std::vector<double> x, ex;
    for ( int i = 0, N = y.size(); i < N; ++i ) {
      dset->addPoint(DataPoint(2));
      x.push_back(i);
      ex.push_back(0);
    }
    if ( !dset->setCoordinate(0, x, ex, ex) ||
         !dset->setCoordinate(1, y, eyp, eym) )
      throw std::runtime_error("LWH could add points to DataPointSet '" +
			       title +  "'." );
    return dset;
  }
    
  /**
   * Create a two dimensional IDataPointSet providing the data along y (the x
   value is the index of the y value in the array).
   * @param pathAndTitle The path of the IDataPointSet. The path can either be
   *                     a relative or full path. The last part of the path is
   *                     used as the title. ("/folder1/folder2/dataTitle" and
   *                     "../folder/dataTitle" are valid paths). All the
   *                     directories in the path must exist. The characther
   *                     `/` cannot be used in names; it is only used to
   *                     delimit directories within paths.
   * @param y            The array of the y values
   * @param ey           The array with the symmetric errors on y
   * @return             The created IDataPointSet.
   *
   */
  virtual IDataPointSet *
  createY(const std::string & pathAndTitle, const std::vector<double> & y,
	  const std::vector<double> & ey) {
    std::string title = pathAndTitle.substr(pathAndTitle.rfind('/') + 1);
    return createY(pathAndTitle, title, y, ey);
  }

  /**
   * Create a two dimensional IDataPointSet providing the data along y (the x
   * value is the index of the y value in the array).
   * @param pathAndTitle The path of the IDataPointSet. The path can either be
   *                     a relative or full path. The last part of the path is
   *                     used as the title. ("/folder1/folder2/dataTitle" and
   *                     "../folder/dataTitle" are valid paths). All the
   *                     directories in the path must exist. The characther
   *                     `/` cannot be used in names; it is only used to
   *                     delimit directories within paths.
   * @param y            The array of the y values
   * @param eyp          The array with the plus errors on y
   * @param eym          The array with the minus errors on y
   * @return             The created IDataPointSet.
   */
  virtual IDataPointSet *
  createY(const std::string & pathAndTitle,
	  const std::vector<double>  & y, const std::vector<double>  & eyp,
	  const std::vector<double>  & eym) {
    std::string title = pathAndTitle.substr(pathAndTitle.rfind('/') + 1);
    return createY(pathAndTitle, title, y, eyp, eym);
  }

  /**
   * Create a two dimensional IDataPointSet providing the data along x (the y
   * value is the index of the x value in the array).
   * @param path  The path of the IDataPointSet. The path can either be a
   *              relative or full path. ("/folder1/folder2/dataTitle" and
   *              "../folder/dataTitle" are valid paths). All the directories
   *              in the path must exist. The characther `/` cannot be used
   *              in names; it is only used to delimit directories within paths.
   * @param title The title of the IDataPointSet.
   * @param x     The array of the x values
   * @param ex    The array with the symmetric errors on x
   * @return      The created IDataPointSet.
   */
  virtual IDataPointSet *
  createX(const std::string & path, const std::string & title,
	  const std::vector<double>  & x, const std::vector<double>  & ex) {
    return createX(path, title, x, ex, ex);
  }

  /**
   * Create a two dimensional IDataPointSet providing the data along x (the y
   * value is the index of the x value in the array).
   * @param path  The path of the IDataPointSet. The path can either be a
   *              relative or full path. ("/folder1/folder2/dataTitle" and
   *              "../folder/dataTitle" are valid paths). All the directories
   *              in the path must exist. The characther `/` cannot be used
   *              in names; it is only used to delimit directories within paths.
   * @param title The title of the IDataPointSet.
   * @param x     The array of the x values
   * @param exp   The array with the plus errors on x
   * @param exm   The array with the minus errors on x
   * @return      The created IDataPointSet.
   */
  virtual IDataPointSet *
  createX(const std::string & path, const std::string & title,
	  const std::vector<double> & x, const std::vector<double> & exp,
	  const std::vector<double>  & exm) {
    IDataPointSet * dset = create(path, title, 2);
    std::vector<double> y, ey;
    for ( int i = 0, N = x.size(); i < N; ++i ) {
      dset->addPoint(DataPoint(2));
      y.push_back(i);
      ey.push_back(0);
    }
    if ( !dset->setCoordinate(0, x, exp, exm) ||
         !dset->setCoordinate(1, y, ey, ey) )
      throw std::runtime_error("LWH could add points to DataPointSet '" +
			       title +  "'." );
    return dset;
  }

  /**
   * Create a two dimensional IDataPointSet providing the data along x (the y
   * value is the index of the x value in the array).
   * @param pathAndTitle The path of the IDataPointSet. The path can either be
   *                     a relative or full path. The last part of the path is
   *                     used as the title. ("/folder1/folder2/dataTitle" and
   *                     "../folder/dataTitle" are valid paths). All the
   *                     directories in the path must exist. The characther
   *                     `/` cannot be used in names; it is only used to
   *                     delimit directories within paths.
   * @param x            The array of the x values
   * @param ex           The array with the symmetric errors on x
   * @return             The created IDataPointSet.
   */
  virtual IDataPointSet *
  createX(const std::string & pathAndTitle, const std::vector<double> & x,
	  const std::vector<double> & ex) {
    std::string title = pathAndTitle.substr(pathAndTitle.rfind('/') + 1);
    return createX(pathAndTitle, title, x, ex, ex);
  }

  /**
   * Create a two dimensional IDataPointSet providing the data along x (the y
   * value is the index of the x value in the array).
   * @param pathAndTitle The path of the IDataPointSet. The path can either be
   *                     a relative or full path. The last part of the path is
   *                     used as the title. ("/folder1/folder2/dataTitle" and
   *                     "../folder/dataTitle" are valid paths). All the
   *                     directories in the path must exist. The characther
   *                     `/` cannot be used in names; it is only used to
   *                     delimit directories within paths.
   * @param x            The array of the x values
   * @param exp          The array with the plus errors on x
   * @param exm          The array with the minus errors on x
   * @return             The created IDataPointSet.
   */
  virtual IDataPointSet *
  createX(const std::string & pathAndTitle, const std::vector<double> & x,
	  const std::vector<double> & exp, const std::vector<double> & exm) {
    std::string title = pathAndTitle.substr(pathAndTitle.rfind('/') + 1);
    return createX(pathAndTitle, title, x, exp, exm);
  }

  /**
   * Create a two dimensional IDataPointSet providing the data.
   * @param path  The path of the IDataPointSet. The path can either be a
   *              relative or full path. ("/folder1/folder2/dataTitle" and
   *              "../folder/dataTitle" are valid paths). All the directories
   *              in the path must exist. The characther `/` cannot be used
   *              in names; it is only used to delimit directories within paths.
   * @param title The title of the IDataPointSet.
   * @param x     The array of the x values
   * @param y     The array of the y values
   * @param exp   The array with the plus errors on x
   * @param eyp   The array with the plus errors on y
   * @param exm   The array with the minus errors on x
   * @param eym   The array with the minus errors on y
   * @return      The created IDataPointSet.
   */
  virtual IDataPointSet *
  createXY(const std::string & path, const std::string & title,
	   const std::vector<double> & x, const std::vector<double> & y,
	   const std::vector<double> & exp, const std::vector<double> & eyp,
	   const std::vector<double> & exm, const std::vector<double> & eym) {
    IDataPointSet * dset = create(path, title, 2);
    for ( int i = 0, N = y.size(); i < N; ++i ) dset->addPoint(DataPoint(2));
    if ( !dset->setCoordinate(0, x, exp, exm) ||
         !dset->setCoordinate(1, y, eyp, eym) )
      throw std::runtime_error("LWH could add points to DataPointSet '" +
			       title +  "'." );
    return dset;
  }

  /**
   * Create a two dimensional IDataPointSet providing the data.
   * @param path  The path of the IDataPointSet. The path can either be a
   *              relative or full path. ("/folder1/folder2/dataTitle" and
   *              "../folder/dataTitle" are valid paths). All the directories
   *              in the path must exist. The characther `/` cannot be used
   *              in names; it is only used to delimit directories within paths.
   * @param title The title of the IDataPointSet.
   * @param x     The array of the x values
   * @param y     The array of the y values
   * @param ex    The array with the symmetric errors on x
   * @param ey    The array with the symmetric errors on y
   * @return      The created IDataPointSet.
   */
  virtual IDataPointSet *
  createXY(const std::string & path, const std::string & title,
	   const std::vector<double> & x, const std::vector<double> & y,
	   const std::vector<double> & ex, const std::vector<double> & ey) {
    return createXY(path, title, x, y, ex, ey, ex, ey);
  }

  /**
   * Create a two dimensional IDataPointSet providing the data.
   * @param pathAndTitle The path of the IDataPointSet. The path can either be
   *                     a relative or full path. The last part of the path is
   *                     used as the title. ("/folder1/folder2/dataTitle" and
   *                     "../folder/dataTitle" are valid paths). All the
   *                     directories in the path must exist. The characther
   *                     `/` cannot be used in names; it is only used to
   *                     delimit directories within paths.
   * @param x            The array of the x values
   * @param y            The array of the y values
   * @param exp          The array with the plus errors on x
   * @param eyp          The array with the plus errors on y
   * @param exm          The array with the minus errors on x
   * @param eym          The array with the minus errors on y
   * @return             The created IDataPointSet.
   */
  virtual IDataPointSet *
  createXY(const std::string & pathAndTitle,
	   const std::vector<double> & x, const std::vector<double> & y,
	   const std::vector<double> & exp, const std::vector<double> & eyp,
	   const std::vector<double> & exm, const std::vector<double> & eym) {
    std::string title = pathAndTitle.substr(pathAndTitle.rfind('/') + 1);
    return createXY(pathAndTitle, title, x, y, exp, eyp, exm, eym);
  }

  /**
   * Create a two dimensional IDataPointSet providing the data.
   * @param pathAndTitle The path of the IDataPointSet. The path can either be
   *                     a relative or full path. The last part of the path is
   *                     used as the title. ("/folder1/folder2/dataTitle" and
   *                     "../folder/dataTitle" are valid paths). All the
   *                     directories in the path must exist. The characther
   *                     `/` cannot be used in names; it is only used to
   *                     delimit directories within paths.
   * @param x            The array of the x values
   * @param y            The array of the y values
   * @param ex           The array with the symmetric errors on x
   * @param ey           The array with the symmetric errors on y
   * @return             The created IDataPointSet.
   */
  virtual IDataPointSet *
  createXY(const std::string & pathAndTitle,
	   const std::vector<double> & x, const std::vector<double> & y,
	   const std::vector<double> & ex, const std::vector<double> & ey) {
    std::string title = pathAndTitle.substr(pathAndTitle.rfind('/') + 1);
    return createXY(pathAndTitle, title, x, y, ex, ey, ex, ey);
  }

  /**
   * Create a three dimensional IDataPointSet providing the data.
   * @param path  The path of the IDataPointSet. The path can either be a
   *              relative or full path. ("/folder1/folder2/dataTitle" and
   *              "../folder/dataTitle" are valid paths). All the directories
   *              in the path must exist. The characther `/` cannot be used
   *              in names; it is only used to delimit directories within paths.
   * @param title The title of the IDataPointSet.
   * @param x     The array of the x values
   * @param y     The array of the y values
   * @param z     The array of the z values
   * @param exp   The array with the plus errors on x
   * @param eyp   The array with the plus errors on y
   * @param ezp   The array with the plus errors on z
   * @param exm   The array with the minus errors on x
   * @param eym   The array with the minus errors on y
   * @param ezm   The array with the minus errors on z
   * @return      The created IDataPointSet.
   */
  virtual IDataPointSet *
  createXYZ(const std::string & path, const std::string & title,
	    const std::vector<double> & x, const std::vector<double> & y,
	    const std::vector<double> & z, const std::vector<double> & exp,
	    const std::vector<double> & eyp, const std::vector<double> & ezp,
	    const std::vector<double> & exm, const std::vector<double> & eym,
	    const std::vector<double>  & ezm) {
    IDataPointSet * dset = create(path, title, 3);
    for ( int i = 0, N = z.size(); i < N; ++i ) dset->addPoint(DataPoint(3));
    if ( !dset->setCoordinate(0, x, exp, exm) ||
         !dset->setCoordinate(1, y, eyp, eym) ||
         !dset->setCoordinate(2, z, ezp, ezm) )
      throw std::runtime_error("LWH could not add points to DataPointSet '" +
			       title +  "'." );
    return dset;
  }

  /**
   * Create a three dimensional IDataPointSet providing the data.
   * @param path  The path of the IDataPointSet. The path can either be a
   *              relative or full path. ("/folder1/folder2/dataTitle" and
   *              "../folder/dataTitle" are valid paths). All the directories
   *              in the path must exist. The characther `/` cannot be used
   *              in names; it is only used to delimit directories within paths.
   * @param title The title of the IDataPointSet.
   * @param x     The array of the x values
   * @param y     The array of the y values
   * @param z     The array of the z values
   * @param ex    The array with the symmetric errors on x
   * @param ey    The array with the symmetric errors on y
   * @param ez    The array with the symmetric errors on z
   * @return      The created IDataPointSet.
   */
  virtual IDataPointSet *
  createXYZ(const std::string & path, const std::string & title,
	    const std::vector<double> & x, const std::vector<double> & y,
	    const std::vector<double> & z, const std::vector<double> & ex,
	    const std::vector<double> & ey, const std::vector<double> & ez) {
    return createXYZ(path, title, x, y, z, ex, ey, ez, ex, ey, ez);
  }

  /**
   * Create a two dimensional IDataPointSet providing the data.
   * @param pathAndTitle The path of the IDataPointSet. The path can either be
   *                     a relative or full path. The last part of the path is
   *                     used as the title. ("/folder1/folder2/dataTitle" and
   *                     "../folder/dataTitle" are valid paths). All the
   *                     directories in the path must exist. The characther
   *                     `/` cannot be used in names; it is only used to
   *                     delimit directories within paths.
   * @param x            The array of the x values
   * @param y            The array of the y values
   * @param z            The array of the z values
   * @param exp          The array with the plus errors on x
   * @param eyp          The array with the plus errors on y
   * @param ezp          The array with the plus errors on z
   * @param exm          The array with the minus errors on x
   * @param eym          The array with the minus errors on y
   * @param ezm          The array with the minus errors on z
   * @return             The created IDataPointSet.
   */
  virtual IDataPointSet *
  createXYZ(const std::string & pathAndTitle, const std::vector<double> & x,
	    const std::vector<double> & y, const std::vector<double> & z,
	    const std::vector<double> & exp, const std::vector<double> & eyp,
	    const std::vector<double> & ezp, const std::vector<double> & exm,
	    const std::vector<double> & eym, const std::vector<double> & ezm) {
    std::string title = pathAndTitle.substr(pathAndTitle.rfind('/') + 1);
    return createXYZ(pathAndTitle, title, x, y, z,
		     exp, eyp, ezp, exm, eym, ezm);
  }

  /**
   * Create a two dimensional IDataPointSet providing the data.
   * @param pathAndTitle The path of the IDataPointSet. The path can either be
   *                     a relative or full path. The last part of the path is
   *                     used as the title. ("/folder1/folder2/dataTitle" and
   *                     "../folder/dataTitle" are valid paths). All the
   *                     directories in the path must exist. The characther
   *                     `/` cannot be used in names; it is only used to
   *                     delimit directories within paths.
   * @param x            The array of the x values
   * @param y            The array of the y values
   * @param z            The array of the z values
   * @param exp          The array with the symmetric errors on x
   * @param eyp          The array with the symmetric errors on y
   * @param ezp          The array with the symmetric errors on z
   * @return             The created IDataPointSet.
   */
  virtual IDataPointSet *
  createXYZ(const std::string & pathAndTitle, const std::vector<double> & x,
	    const std::vector<double> & y, const std::vector<double> & z,
	    const std::vector<double> & ex, const std::vector<double> & ey,
	    const std::vector<double> & ez) {
    std::string title = pathAndTitle.substr(pathAndTitle.rfind('/') + 1);
    return createXYZ(pathAndTitle, title, x, y, z, ex, ey, ez, ex, ey, ez);
  }

  /**
   * Make a copy of a given IDataPointSet.
   * @param path  The path of the IDataPointSet. The path can either be a
   *              relative or full path. ("/folder1/folder2/dataTitle" and
   *              "../folder/dataTitle" are valid paths). All the directories
   *              in the path must exist. The characther `/` cannot be used
   *              in names; it is only used to delimit directories within paths.
   * @param dataPointSet The IDataPointSet to be copied.
   * @return             The copy of the given IDataPointSet.
   */
  virtual IDataPointSet *
  createCopy(const std::string & path, const IDataPointSet & dataPointSet) {
    IDataPointSet * dset =
      create(path, dataPointSet.title(), dataPointSet.dimension());
    for ( int i = 0, N = dataPointSet.size(); i < N; ++i )
      dset->addPoint(*dataPointSet.point(i));
    return dset;
  }

  /**
   * Destroy a given IDataPointSet.
   * @param dataPointSet  The IDataPointSet to be destroyed.
   * @return false If dataPointSet cannot be destroyed.
   */
  virtual bool destroy(IDataPointSet * dataPointSet) {
    IManagedObject * mo = dynamic_cast<IManagedObject *>(dataPointSet);
    if ( !mo ) return false;
    return tree->rm(tree->findPath(*mo));
  }

  /**
   * Create an IDataPointSet from an IHistogram1D.
   * @param path  The path of the IDataPointSet. The path can either
   *              be a relative or full path.
   *              ("/folder1/folder2/dataName" and "../folder/dataName"
   *              are valid paths). All the directories in the path
   *              must exist. The characther `/` cannot be used in
   *              names; it is only used to delimit directories within
   *		    paths.
   * @param hist    The IHistogram1D from which the data is taken.
   * @param options Options, currently not specified
   * @return        The newly created IDataPointSet.
   */
  virtual IDataPointSet *
  create(const std::string & path, const IHistogram1D & hist,
         const std::string & = "") {
    IDataPointSet * dset = create(path, hist.title(), 2);
    //std::cout << hist.xtitle() << " & " << hist.ytitle() << std::endl;

    dset->setXTitle(hist.xtitle());
    dset->setYTitle(hist.ytitle());
    std::vector<double> x, y, ex, ey;
    for ( int i = 2, N = hist.axis().bins() + 2; i < N; ++i ) {
      dset->addPoint(DataPoint(2));
      //x.push_back(hist.binMean(i - 2)); // < "Dynamic" version
      // Shouldn't IAxis have a binCentre(size_t binId) method? (According to Java AIDA v3.3.0 API)
      x.push_back((hist.axis().binLowerEdge(i - 2) + hist.axis().binUpperEdge(i - 2))/2.0);
      ex.push_back(hist.axis().binWidth(i - 2)/2.0);
      /// @todo This is not really the height or error: width needs to be included...
      const double binwidth = hist.axis().binWidth(i - 2);
      y.push_back(hist.binHeight(i - 2)/binwidth);
      //ey.push_back(hist.binError(i - 2)/2.0/binwidth);
      ey.push_back(hist.binError(i - 2)/binwidth);
    }
    if ( !dset->setCoordinate(0, x, ex, ex) ||
         !dset->setCoordinate(1, y, ey, ey) )
      throw std::runtime_error("LWH could add points to DataPointSet '" +
			       hist.title() +  "'." );
    return dset;
  }


  /**
   * Create an IDataPointSet from an IHistogram2D.
   * @param path  The path of the IDataPointSet. The path can either
   *              be a relative or full path.
   *              ("/folder1/folder2/dataName" and "../folder/dataName"
   *              are valid paths). All the directories in the path
   *              must exist. The characther `/` cannot be used in
   *              names; it is only used to delimit directories within
   *		    paths.
   * @param hist    The IHistogram2D from which the data is taken.
   * @param options Options, currently not specified
   * @return        The newly created IDataPointSet.
   */
  virtual IDataPointSet *
  create(const std::string & path, const IHistogram2D & hist,
         const std::string & = "") {
    IDataPointSet * dset = create(path, hist.title(), 3);
    //std::cout << hist.xtitle() << " & " << hist.ytitle() << std::endl;

    dset->setXTitle(hist.xtitle());
    dset->setYTitle(hist.ytitle());
    std::vector<double> x, y, z, ex, ey, ez;
    for ( int ix = 2, Nx = hist.xAxis().bins() + 2; ix < Nx; ++ix )
      for ( int iy = 2, Ny = hist.yAxis().bins() + 2; iy < Ny; ++iy ) {
      dset->addPoint(DataPoint(3));
      //x.push_back(hist.binMean(i - 2)); // < "Dynamic" version
      // Shouldn't IAxis have a binCentre(size_t binId) method? (According to Java AIDA v3.3.0 API)
      x.push_back((hist.xAxis().binLowerEdge(ix - 2) +
		   hist.xAxis().binUpperEdge(ix - 2))/2.0);
      ex.push_back(hist.xAxis().binWidth(ix - 2)/2.0);
      /// @todo This is not really the height or error: width needs to be included...
      y.push_back((hist.yAxis().binLowerEdge(iy - 2) +
		   hist.yAxis().binUpperEdge(iy - 2))/2.0);
      ey.push_back(hist.yAxis().binWidth(iy - 2)/2.0);
      /// @todo This is not really the height or error: width needs to be included...
      const double binwidth = hist.xAxis().binWidth(ix - 2)*
	hist.yAxis().binWidth(iy - 2);
      z.push_back(hist.binHeight(ix - 2, iy - 2)/binwidth);
      //ey.push_back(hist.binError(i - 2)/2.0/binwidth);
      ez.push_back(hist.binError(ix - 2, iy - 2)/binwidth);
    }
    if ( !dset->setCoordinate(0, x, ex, ex) ||
         !dset->setCoordinate(1, y, ey, ey) ||
         !dset->setCoordinate(2, z, ez, ez) )
      throw std::runtime_error("LWH could not add points to DataPointSet '" +
			       hist.title() +  "'." );
    return dset;
  }


  /**
   * Create an IDataPointSet from an IProfile1D.
   * @param path  The path of the IDataPointSet. The path can either
   *              be a relative or full path.
   *              ("/folder1/folder2/dataName" and "../folder/dataName"
   *              are valid paths). All the directories in the path
   *              must exist. The characther `/` cannot be used in
   *              names; it is only used to delimit directories within
   *		    paths.
   * @param prof    The IProfile1D from which the data is taken.
   * @param options Options, currently not specified
   * @return        The newly created IDataPointSet.
   */
  virtual IDataPointSet *
  create(const std::string & path, const IProfile1D & prof,
	 const std::string & = "") {
    //std::cout << "########## " << prof.title() << std::endl;
    IDataPointSet * dset = create(path, prof.title(), 2);
    dset->setXTitle(prof.xtitle());
    dset->setYTitle(prof.ytitle());
    std::vector<double> x, y, ex, ey;
    for ( int i = 2, N = prof.axis().bins() + 2; i < N; ++i ) {
      dset->addPoint(DataPoint(2));
      //x.push_back(prof.binMean(i - 2)); // < "Dynamic" version
      // Shouldn't IAxis have a binCentre(size_t binId) method? (According to Java AIDA v3.3.0 API)
      x.push_back((prof.axis().binLowerEdge(i - 2) + prof.axis().binUpperEdge(i - 2))/2.0);
      ex.push_back(prof.axis().binWidth(i - 2)/2.0);
      y.push_back(prof.binHeight(i - 2));
      //ey.push_back(prof.binError(i - 2)/2.0);
      ey.push_back(prof.binError(i - 2));
    }
    if ( !dset->setCoordinate(0, x, ex, ex) ||
         !dset->setCoordinate(1, y, ey, ey) )
      throw std::runtime_error("LWH could add points to DataPointSet '" +
			       prof.title() +  "'." );
    return dset;
  }


  /**
   * LWH cannot handle a IHistogram3D.
   */
  virtual IDataPointSet * create(const std::string &, const IHistogram3D &,
				 const std::string & = "") {
    return error<IDataPointSet>("IHistogram3D");
  }

  /**
   * LWH cannot handle a ICloud1.
   */
  virtual IDataPointSet * create(const std::string &, const ICloud1D &,
				 const std::string & = "") {
    return error<IDataPointSet>("ICloud1D");
  }

  /**
   * LWH cannot handle a ICloud2D.
   */
  virtual IDataPointSet * create(const std::string &, const ICloud2D &,
				 const std::string & = "") {
    return error<IDataPointSet>("ICloud2D");
  }

  /**
   * LWH cannot handle a ICloud3D.
   */
  virtual IDataPointSet * create(const std::string &, const ICloud3D &,
				 const std::string & = "") {
    return error<IDataPointSet>("ICloud3D");
  }

  /**
   * LWH cannot handle a IProfile2D.
   */
  virtual IDataPointSet * create(const std::string &, const IProfile2D &,
				 const std::string & = "") {
    return error<IDataPointSet>("IProfile2D");
  }

  /**
   * LWH cannot handle the addition of data points.
   */
  virtual IDataPointSet * add(const std::string &,
			      const IDataPointSet &, const IDataPointSet &) {
    return error<IDataPointSet>("addition of data points");
  }

  /**
   * LWH cannot handle the subtraction of data points.
   */
  virtual IDataPointSet * subtract(const std::string &, const IDataPointSet &,
				   const IDataPointSet &) {
    return error<IDataPointSet>("subtraction of data points");
  }

  /**
   * LWH cannot handle the multiplication of data points.
   */
  virtual IDataPointSet * multiply(const std::string &, const IDataPointSet &,
				   const IDataPointSet &) {
    return error<IDataPointSet>("multiplication of data points");
  }

  /**
   * LWH cannot handle the division of data points.
   */
  virtual IDataPointSet * divide(const std::string &, const IDataPointSet &,
				 const IDataPointSet &) {
    return error<IDataPointSet>("division of data points");
  }

  /**
   * LWH cannot handle the weighted mean of data points.
   */
  virtual IDataPointSet *
  weightedMean(const std::string &, const IDataPointSet &,
	       const IDataPointSet &) {
    return error<IDataPointSet>("weighted means of data points");
  }
  
private:

  /** Throw a suitable error. */
  template <typename T>
  static T * error(std::string feature) {
    throw std::runtime_error("LWH cannot handle " + feature + ".");
    return 0;
  }

  /** The tree where the actual data sets are stored. */
  Tree * tree;

};
}

#endif
