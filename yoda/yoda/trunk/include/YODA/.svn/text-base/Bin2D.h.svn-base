#ifndef YODA_Bin2D_h
#define YODA_Bin2D_h

#include "YODA/Bin.h"
#include "YODA/Dbn2D.h"
#include "YODA/HistoBin1D.h"
#include <string>
#include <utility>
#include <vector>
using namespace std;

namespace YODA {

    class Bin2D : public Bin {
    public:
        
        /// Constructor that is mostly used in manual bin addition.
        /** Mostly used when creating a bin manually
          * since it requires the smallest amount 
          * of infromation transferred. All 4 edges
          * are then constructed from extremal points which coordinates
          * are provided.
          */
        Bin2D(double lowedgeX, double lowedgeY, double highedgeX, double highedgeY);

        /// A constructor usually used by functions creating Bins in bulk.
        /** Since all the edges are provided by an external function
          * it creates a Bin slightly faster (this claim is very weakly true).
          * It is not suggested to use it if it is just needed to add few bins to 
          * an already created Histo2D.
          */
        Bin2D(std::vector<std::pair<std::pair<double, double>, std::pair<double, double> > > edges);

        Bin2D();

        /// Resetter of all Bin data
        virtual void reset();
        
        /// Scaling function.
        void scale(double scaleX, double scaleY);
        
        /// What this and the following functions return should be self-evident.
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


        /// Some distribution statistics:
        double xMean() const;
        double yMean() const;

        double xVariance() const;
        double yVariance() const;

        double xStdDev() const;
        double yStdDev() const;

        /// Standard error:
        double xStdErr() const;
        double yStdErr() const;


        /// Some "raw distribution statistics"
        unsigned long numEntries() const;
        double sumW() const;
        double sumW2() const;
        double sumWX() const;
        double sumWY() const;
        double sumWXY() const;
        double sumWX2() const;
        double sumWY2() const;

        /// Setters
        void setW(double sumW);
        void setW2(double sumW2);
        void setWX(double sumWX);
        void setWY(double sumWY);
        void setWX2(double sumWX2);
        void setWY2(double sumWY2);
        void setWXY(double sumWXY);

        ///@name Transformers
        //@{

        /// Transform, taking X coordinates as a bin width
        HistoBin1D transformX();

        /// Transform, taking Y coordinates as bin width
        HistoBin1D transformY();

        /// Addition operators:
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
