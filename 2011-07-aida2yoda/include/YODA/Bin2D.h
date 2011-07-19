#ifndef YODA_Bin2D_h
#define YODA_Bin2D_h

#include "YODA/Bin.h"
#include "YODA/Dbn2D.h"
#include <string>
#include <utility>

namespace YODA {

    class Bin2D : public Bin {
    public:

        Bin2D(double lowedgeX, double lowedgeY, double highedgeX, double highedgeY);
        Bin2D(std::pair<std::pair<double, double>, std::pair<double, double> > edges);

        virtual void reset();

        
        double lowEdgeX() const;
        double xMin() const { return lowEdgeX(); }

        double lowEdgeY() const;
        double yMin() const { return lowEdgeY(); }

        double highEdgeX() const;
        double xMax() const { return highEdgeX(); }

        double highEdgeY() const;
        double yMax() const { return highEdgeY(); }

        std::pair<double, double> edgesX() const;
        std::pair<double, double> edgesY() const;

        double widthX() const;
        double widthY() const;
        
        std::pair<double, double> focus() const;
        std::pair<double, double> midpoint() const;


        //Now some distribution statistics:
        double xMean() const;
        double yMean() const;
        std::pair<double, double> Mean() const;

        double xVariance() const;
        double yVariance() const;
        std::pair<double, double> Variance() const;

        double xStdDev() const;
        double yStdDev() const;
        std::pair<double, double> StdDev() const;

        //Standar error, previously named StdError!
        double xStdErr() const;
        double yStdErr() const;
        std::pair<double, double> StdErr() const;


        //Some "raw distribution statistics"
        unsigned long numEntries() const;
        double sumW() const;
        double sumW2() const;
        double sumWX() const;
        double sumWY() const;
        double sumWXY() const;
        double sumX2() const;
        double sumY2() const;

        Bin2D& operator += (const Bin2D&);
        Bin2D& operator -= (const Bin2D&);

    protected:
        Bin2D& add(const Bin2D&);
        Bin2D& substract(const Bin2D&);

    };

    Bin2D operator + (const Bin2D& a, const Bin2D& b);
    Bin2D operator - (const Bin2D& a, const Bin2D& b);

    //Comparison functions that _may_ be used for sorting later, we will see...
    inline bool smallerX(const Bin2D& a, const Bin2D& b) {
        return b.edgesX().first > a.edgesX().first;
    }
    
    inline bool smallerY(const Bin2D& a, const Bin2D& b) {
        return b.edgesY().first > a.edgesY().first;
    }
}


#endif
