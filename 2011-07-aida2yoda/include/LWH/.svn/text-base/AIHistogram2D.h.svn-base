// -*- C++ -*-
#ifndef LWH_AIHistogram2D_H
#define LWH_AIHistogram2D_H

#ifndef LWH_USING_AIDA

/** @cond DONT_DOCUMENT_STRIPPED_DOWN_AIDA_INTERFACES */

#include "AIHistogram1D.h"

namespace AIDA {

class IAxis;

class IHistogram2D : virtual public IHistogram {

public: 

    virtual ~IHistogram2D() { /* nop */; }

    /**
     * Fill the IHistogram2D with a couple of values and the
     * corresponding weight.
     * @param x      The x value to be filled in.
     * @param y      The y value to be filled in.
     * @param weight The corresponding weight (by default 1).
     * @return false If the weight is <0 or >1 (?).
     *
     */
    virtual bool fill(double x, double y, double weight = 1.) = 0;

    /**
     * The weighted mean along the x axis of a given bin. 
     * @param indexX The x bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @param indexY The y bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The mean of the corresponding bin along the x axis.
     *
     */
    virtual double binMeanX(int indexX, int indexY) const = 0;

    /**
     * The weighted mean along the y axis of a given bin.
     * @param indexX The x bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @param indexY The y bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The mean of the corresponding bin along the y axis.
     *
     */
    virtual double binMeanY(int indexX, int indexY) const = 0;

    /**
     * Number of entries in the corresponding bin (ie the number of times fill was called for this bin).
     * @param indexX The x bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @param indexY The y bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return       The number of entries in the corresponding bin. 
     *
     */
    virtual int binEntries(int indexX, int indexY) const = 0;

    /**
     * Sum of all the entries of the bins along a given x bin.
     * This is equivalent to <tt>projectionX().binEntries(index)</tt>.
     * @param index The x bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The number of entries in the corresponding set of bins. 
     *
     */
    virtual int binEntriesX(int index) const = 0;

    /**
     * Sum of all the entries of the bins along a given y bin.
     * This is equivalent to <tt>projectionY().binEntries(index)</tt>.
     * @param index The y bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The number of entries in the corresponding set of bins. 
     *
     */
    virtual int binEntriesY(int index) const = 0;

    /**
     * Total height of a give bin (ie the sum of the weights in this bin).
     * @param indexX The x bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @param indexY The y bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return       The height of the corresponding bin.
     *
     */
    virtual double binHeight(int indexX, int indexY) const = 0;

    /**
     * Sum of all the heights of the bins along a given x bin.
     * This is equivalent to <tt>projectionX().binHeight(index)</tt>.
     * @param index The x bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The sum of the heights in the corresponding set of bins. 
     *
     */
    virtual double binHeightX(int index) const = 0;

    /**
     * Sum of all the heights of the bins along a given y bin.
     * This is equivalent to <tt>projectionY().binHeight(index)</tt>.
     * @param index The y bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The sum of the heights in the corresponding set of bins. 
     *
     */
    virtual double binHeightY(int index) const = 0;

    /**
     * The error of a given bin.
     * @param indexX The x bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @param indexY The y bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return       The error on the corresponding bin.
     *
     */
    virtual double binError(int indexX, int indexY) const = 0;

    /**
     * The mean of the IHistogram2D along the x axis.
     * @return The mean of the IHistogram2D along the x axis.
     *
     */
    virtual double meanX() const = 0;

    /**
     * The mean of the IHistogram2D along the y axis.
     * @return The mean of the IHistogram2D along the y axis.
     *
     */
    virtual double meanY() const = 0;

    /**
     * The RMS of the IHistogram2D along the x axis.
     * @return The RMS if the IHistogram2D along the x axis.
     *
     */
    virtual double rmsX() const = 0;

    /**
     * The RMS of the IHistogram2D along the y axis.
     * @return The RMS if the IHistogram2D along the y axis.
     *
     */
    virtual double rmsY() const = 0;

    /**
     * Get the x axis of the IHistogram2D.
     * @return The x coordinate IAxis.
     *
     */
    virtual const IAxis & xAxis() const = 0;

    /**
     * Get the y axis of the IHistogram2D.
     * @return The y coordinate IAxis.
     *
     */
    virtual const IAxis & yAxis() const = 0;

    /**
     * Get the bin number corresponding to a given coordinate along the x axis.
     * This is a convenience method, equivalent to <tt>xAxis().coordToIndex(coord)</tt>.
     * @see IAxis#coordToIndex(double)
     * @param coord The coordinalte along the x axis.
     * @return      The corresponding bin number.
     *
     */
    virtual int coordToIndexX(double coord) const = 0;

    /**
     * Get the bin number corresponding to a given coordinate along the y axis.
     * This is a convenience method, equivalent to <tt>yAxis().coordToIndex(coord)</tt>.
     * @see IAxis#coordToIndex(double)
     * @param coord The coordinalte along the y axis.
     * @return      The corresponding bin number.
     *
     */
    virtual int coordToIndexY(double coord) const = 0;

    /**
     * Add to this IHistogram2D the contents of another IHistogram2D.
     * @param hist The IHistogram2D to be added to this IHistogram2D.
     * @return false If the IHistogram2Ds binnings are incompatible.
     *
     */
    virtual bool add(const IHistogram2D & hist) = 0;
}; // class
} // namespace AIDA
/** @endcond */

#else
#include "AIDA/IHistogram2D.h"
#endif

#endif /* LWH_AIHistogram2D_H */

