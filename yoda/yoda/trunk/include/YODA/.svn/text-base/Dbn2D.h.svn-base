#ifndef YODA_Dbn2D_h
#define YODA_Dbn2D_h

#include "YODA/Exceptions.h"

namespace YODA {
    class Dbn2D {
    public:
        
        Dbn2D() {
            reset();
        }
        /// fill() requesting coordinates as two diferent numbers
        void fill(double valX, double valY, double weight=1.0);

        /// fill() accepting coordinates as a pair
        void fill(std::pair<double,double> val, double weight=1.0);
        void reset();

        /// Scaling the height of a bin
        void scaleW(double sf) {
            _sumW *= sf;
            _sumW2 *= sf*sf;
            _sumWX *= sf;
            _sumWX2 *= sf*sf;
            _sumWY *= sf;
            _sumWY2 *= sf*sf;
            _sumWXY *= sf;
        }

        /// Scaling the dimensions of a distribution
        void scale(double scaleX, double scaleY) {
            _sumWX *= scaleX;
            _sumWX2 *= scaleX*scaleX;
            _sumWY *= scaleY;
            _sumWY2 *= scaleY*scaleY;
            _sumWXY *= scaleX*scaleY;
        }
        
        /// Setters
        void setW(double sumW)      { _sumW = sumW;}
        void setW2(double sumW2)    { _sumW2 = sumW2;}
        void setWX(double sumWX)    { _sumWX = sumWX;}
        void setWY(double sumWY)    { _sumWY = sumWY;}
        void setWX2(double sumWX2)  { _sumWX2 = sumWX2;}
        void setWY2(double sumWY2)  { _sumWY2 = sumWY2;}
        void setWXY(double sumWXY)  { _sumWXY = sumWXY;}
        void setNumfills(unsigned long numFills) {_numFills = numFills;}

        /// Some in-distribution variables. Should be self-evident.
        double xMean() const;
        double yMean() const;

        double xVariance() const;
        double yVariance() const;

        double xStdDev() const;
        double yStdDev() const;

        double xStdErr() const;
        double yStdErr() const;

        unsigned long numEntries() const;
        double effNumEntries() const;
        double sumW() const;
        double sumW2() const;
        double sumWX() const;
        double sumWY() const;
        double sumWXY() const;
        double sumWX2() const;
        double sumWY2() const;
    
        Dbn2D& operator += (const Dbn2D&);
        Dbn2D& operator -= (const Dbn2D&);

    protected:   
        Dbn2D& add(const Dbn2D&);
        Dbn2D& substract(const Dbn2D&);

    private:

        unsigned long _numFills;
        double _sumW;
        double _sumW2;
        double _sumWX;
        double _sumWY;
        double _sumWX2;
        double _sumWY2;
        double _sumWXY;

    };

    Dbn2D operator + (const Dbn2D& a, const Dbn2D& b);
    Dbn2D operator - (const Dbn2D& a, const Dbn2D& b);
}

#endif
