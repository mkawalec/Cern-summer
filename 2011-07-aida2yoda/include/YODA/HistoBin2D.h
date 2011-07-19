#ifndef YODA_HistoBin2D_h
#define YODA_HistoBin2D_h

#include "Yoda/Bin2D.h"
#include "YODA/Exceptions.h"

namespace YODA {
    class HistoBin2D : public Bin2D {
    public:
        //Constructors:
        HistoBin2D(double lowedgeX, double lowedgeY, double highedgeX, double highedgeY);
        HistoBin2D(std::pair<std::pair<double,double>, std::pair<double,double> > edges);

        //Modifiers:
        void fill(std::pair<double,double>, double weight=1.0)
        void fill(double coordX, double coordY, double weight=1.0)

        void fillBin(double weight=1.0)
