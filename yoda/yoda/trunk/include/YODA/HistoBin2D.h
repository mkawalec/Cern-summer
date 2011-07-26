#ifndef YODA_HistoBin2D_h
#define YODA_HistoBin2D_h

#include "YODA/Bin2D.h"
#include "YODA/Exceptions.h"

namespace YODA {
    class HistoBin2D : public Bin2D {
    public:
        //Constructors:
        HistoBin2D(double lowEdgeX, double highEdgeX,
                   double lowEdgeY, double highEdgeY);

        HistoBin2D(std::vector<std::pair<std::pair<double,double>, std::pair<double,double> > >& edges);

        //Modifiers:
        void fill(std::pair<double,double>, double weight=1.0);
        void fill(double coordX, double coordY, double weight=1.0);

        void fillBin(double weight=1.0);
        void reset() {
            Bin2D::reset();
        }

        void scaleW(double scalefactor) {
            _xdbn.scaleW(scalefactor);
        }

        //Bin content info:
        
        //Note that area is actually a volume, kept to keep variable names 
        //the same with *1D
        double area() const;
        double height() const;
        double areaErr() const;
        double heightErr() const;

        //Operators:
        HistoBin2D& operator += (const HistoBin2D&);
        HistoBin2D& operator -= (const HistoBin2D&);

    protected:
        HistoBin2D& add(const HistoBin2D&);
        HistoBin2D& substract(const HistoBin2D&);
    };

    HistoBin2D operator + (const HistoBin2D& a, const HistoBin2D& b);
    HistoBin2D operator - (const HistoBin2D& a, const HistoBin2D& b);

}

#endif
