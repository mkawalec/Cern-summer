#include "YODA/Bin2D.h"

#include <cassert>
#include <cmath>
using namespace std;

namespace YODA {
    Bin2D::Bin2D(double lowedgeX, double lowedgeY, 
                 double highedgeX, double highedgeY) 
    {
        assert(lowedgeX < highedgeX && lowedgeY < highedgeY);

        pair<pair<double,double>, pair<double,double> > edge1 =
            make_pair(make_pair(lowedgeX, lowedgeY), 
                      make_pair(lowedgeX, highedgeY));
        pair<pair<double,double>, pair<double,double> > edge2 =
            make_pair(make_pair(lowedgeX, highedgeY),
                      make_pair(highedgeX, highedgeY));
        pair<pair<double,double>, pair<double,double> > edge3 =
            make_pair(make_pair(highedgeX, lowedgeY),
                      make_pair(highedgeX, highedgeY));
        pair<pair<double,double>, pair<double,double> > edge4 =
            make_pair(make_pair(lowedgeX, lowedgeY),
                      make_pair(highedgeX, lowedgeY));

        _edges.push_back(edge1); _edges.push_back(edge2);
        _edges.push_back(edge3); _edges.push_back(edge4);
    }

    Bin2D::Bin2D(std::vector<std::pair<std::pair<double,double>, 
                 std::pair<double,double> > > edges) 
    {
        assert(edges.size() == 4);
     
        _edges.push_back(edges[0]); _edges.push_back(edges[1]);
        _edges.push_back(edges[2]); _edges.push_back(edges[3]);
    }

    void Bin2D::reset() {
        _dbn.reset();
    }

    double Bin2D::lowedgeX() const { return _edges[0].first.first;  }
    double Bin2D::lowedgeY() const { return _edges[0].first.second; }
    double Bin2D::highedgeX() const {return _edges[1].second.first; }
    double Bin2D::highedgeY() const {return _edges[1].second.second;}

    double Bin2D::widthX() const {
        return _edges[1].second.first - _edges[0].first.first;
    }
    double Bin2D::widthY() const {
        return _edges[0].second.second - _edges[0].first.second;
    }

    std::pair<double,double> Bin2D::focus() const {
        if(_dbn.sumW() != 0) return make_pair(xMean(), yMean());
        else return midpoint();
    }

    std::pair<double,double> Bin2D::midpoint() const {
        return make_pair(edges[1].second.first-edges[0].first.first,
                         edges[0].second.second-edges[0].first.second);
    }

    double Bin2D::xMean() const {
        return _dbn.xMean();
    }
    double Bin2D::yMean() const {
        return _dbn.yMean();
    }

    double Bin2D::xVariance() const {
        return _dbn.xVariance();
    }
    double Bin2D::yVariance() const {
        return _dbn.yVariance();
    }

    double Bin2D::xStdDev() const {
        return _dbn.xStdDev();
    }
    double Bin2D::yStdDev() const {
        return _dbn.yStdDev();
    }

    double Bin2D::xStdErr() const {
        return _dbn.xStdErr();
    }
    double Bin2D::yStdErr() const {
        return _dbn.yStdErr();
    }

    unsigned long Bin2D::numEntries() const {
        return _dbn.numEntries();
    }

    double Bin2D::sumW() const {
        return _dbn.sumW();
    }
    double Bin2D::sumW2() const {
        return _dbn.sumW2();
    }
    double Bin2D::sumWX() const {
        return _dbn.sumWX();
    }
    double Bin2D::sumWY() const {
        return _dbn.sumWY();
    }
    double Bin2D::sumWXY() const {
        return _dbn.sumWXY();
    }
    double Bin2D::sumWX2() const {
        return _dbn.sumWX2();
    }
    double Bin2D::sumWY2() const {
        return _dbn.sumWY2();
    }

    Bin2D& Bin2D::add(const Bin2D& b) {
        assert(_edges == b._edges);
        _dbn += b._dbn;
        return *this;
    }

    Bin2D& Bin2D::substract(const Bin2D& b) {
        assert(_edges == b._edges);
        _dbn -= b._dbn;
        return *this;
    }

    Bin2D& Bin2D::operator += (const Bin2D& b) { return add(b); }
    Bin2D& Bin2D::operator -= (const Bin2D& b) { return substract(b); }

    Bin2D operator + (const Bin2D& a, const Bin2D& b) {
        Bin2D rtn = a;
        rtn += b;
        return rtn;
    }

    Bin2D operator - (const Bin2D& a, const Bin2D& b) {
        Bin2D rtn = a;
        rtn -= a;
        return rtn;
    }
}





