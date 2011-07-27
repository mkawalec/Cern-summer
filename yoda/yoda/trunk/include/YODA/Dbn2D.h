#ifndef YODA_Dbn2D_h
#define YODA_Dbn2D_h

#include "YODA/Exceptions.h"

namespace YODA {
    class Dbn2D {
    public:
        
        Dbn2D() {
            reset();
        }

        void fill(double valX, double valY, double weight=1.0);
        void fill(std::pair<double,double> val, double weight=1.0);
        void reset();

        void scaleW(double sf) {
            _sumW *= sf;
            _sumW2 *= sf*sf;
            _sumWX *= sf;
            _sumWX2 *= sf*sf;
            _sumWY *= sf;
            _sumWY2 *= sf*sf;
            _sumWXY *= sf;
        }

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
