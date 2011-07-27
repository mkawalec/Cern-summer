#ifndef YODA_Bin2D_h
#define YODA_Bin2D_h

#include "YODA/Bin.h"
#include "YODA/Dbn2D.h"
#include <string>
#include <utility>
#include <vector>
using namespace std;

namespace YODA {

    class Bin2D : public Bin {
    public:

        Bin2D(double lowedgeX, double lowedgeY, double highedgeX, double highedgeY);
        Bin2D(std::vector<std::pair<std::pair<double, double>, std::pair<double, double> > > edges);

        virtual void reset();

        
        double lowEdgeX() const;
        double xMin() const { return lowEdgeX(); }

        double lowEdgeY() const;
        double yMin() const { return lowEdgeY(); }

        double highEdgeX() const;
        double xMax() const { return highEdgeX(); }

        double highEdgeY() const;
        double yMax() const { return highEdgeY(); }

        double widthX() const;
        double widthY() const;
        
        std::pair<double, double> focus() const;
        std::pair<double, double> midpoint() const;


        //Now some distribution statistics:
        double xMean() const;
        double yMean() const;

        double xVariance() const;
        double yVariance() const;

        double xStdDev() const;
        double yStdDev() const;

        //Standar error, previously named StdError!
        double xStdErr() const;
        double yStdErr() const;


        //Some "raw distribution statistics"
        unsigned long numEntries() const;
        double sumW() const;
        double sumW2() const;
        double sumWX() const;
        double sumWY() const;
        double sumWXY() const;
        double sumWX2() const;
        double sumWY2() const;

        Bin2D& operator += (const Bin2D&);
        Bin2D& operator -= (const Bin2D&);

    protected:
        Bin2D& add(const Bin2D&);
        Bin2D& substract(const Bin2D&);
        
        std::vector<std::pair<std::pair<double,double>,std::pair<double,double> > > _edges;
        Dbn2D _dbn;

    };

    Bin2D operator + (const Bin2D& a, const Bin2D& b);
    Bin2D operator - (const Bin2D& a, const Bin2D& b);

}


#endif
