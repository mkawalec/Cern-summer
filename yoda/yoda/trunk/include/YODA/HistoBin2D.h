#ifndef YODA_HistoBin2D_h
#define YODA_HistoBin2D_h

#include "YODA/Bin2D.h"
#include "YODA/Exceptions.h"
#include <cmath>

namespace YODA {
    class HistoBin2D : public Bin2D {
    public:
        /// Constructor accepting a set of extremal points of a bin 
        HistoBin2D(double lowEdgeX, double highEdgeX,
                   double lowEdgeY, double highEdgeY);

        /// Constructor accepting a set of all edges of a bin
        HistoBin2D(std::vector<std::pair<std::pair<double,double>, std::pair<double,double> > >& edges);
        
        //Default constructor
        HistoBin2D();

        /// A fill() function accepting the coordinates as std::pair
        void fill(std::pair<double,double>, double weight=1.0);

        /// A fill() function accepting coordinates as spearate numbers
        void fill(double coordX, double coordY, double weight=1.0);

        /// A function that fills this particular bin.
        void fillBin(double weight=1.0);

        /// A reset function
        void reset() {
            Bin2D::reset();
        }

        /// Rescalling the height of a bin
        void scaleW(double scalefactor) {
            _dbn.scaleW(scalefactor);
        }

        
        //TODO: Is it a volume? Looks like height.
        /// The volume of a bin
        double volume() const { return sumW(); }

        /// The height of a bin
        double height() const { return volume()/(widthX()*widthY()); }

        /// Error on volume
        double volumeErr() const{ return sqrt(sumW2()); }

        ///Error on height
        double heightErr() const{ return volumeErr()/(widthX()*widthY());}

        
        /// Addition operator
        HistoBin2D& operator += (const HistoBin2D&);

        /// Substracion operator
        HistoBin2D& operator -= (const HistoBin2D&);

    protected:
        HistoBin2D& add(const HistoBin2D&);
        HistoBin2D& substract(const HistoBin2D&);
    };

    HistoBin2D operator + (const HistoBin2D& a, const HistoBin2D& b);
    HistoBin2D operator - (const HistoBin2D& a, const HistoBin2D& b);

}

#endif
