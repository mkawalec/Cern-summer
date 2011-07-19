#ifndef YODA_Axis2D_h
#define YODA_Axis2D_h

#include "Yoda/AnalysisObject.h"
#include "YODA/Exceptions.h"
#include "YODA/Bin.h"
#include "YODA/Utils/sortedvector.h"
#include "YODA/Utils/MathUtils.h"
#include <string>
#include <cassert>
#include <cmath>
#include <algorithm>

using namespace std;

namespace YODA {
    template <typename BIN>
    class Axis2D {
    public:
        
        typedef BIN Bin;
        typedef typename Utils::sortedvector<Utils::sortedvector<BIN> > Bins;

        static inline pair<std::vector<double>, std::vector<double> > mkBinEdgesLinLin(double startX, startY, double endX, double endY, size_t nbinsX, size_t nbinsY) {
            return make_pair(linspace(startX, endX, nbinsX), linspace(startY, endY, nbinsY))
        }

        static inline pair<std::vector<double>, std::vector<double> > mkBinEdgesLinLog(double startX, startY, double endX, double endY, size_t nbinsX, size_t nbinsY) {
            return make_pair(linspace(startX, endX, nbinsX), logspace(startY, endY, nbinsY))
        }

        static inline pair<std::vector<double>, std::vector<double> > mkBinEdgesLogLog(double startX, startY, double endX, double endY, size_t nbinsX, size_t nbinsY) {
            return make_pair(logspace(startX, endX, nbinsX), logspace(startY, endY, nbinsY))
        }

        static inline pair<std::vector<double>, std::vector<double> > mkBinEdgesLogLin(double startX, startY, double endX, double endY, size_t nbinsX, size_t nbinsY) {
            return make_pair(logspace(startX, endX, nbinsX), linspace(startY, endY, nbinsY))
        }
}
    private:

        /* _binHash is of type pair< vector <double>, vector <double> >, 
         * it is used for indexing the bin edges
         * _cachedBinEdges is of type pair<vector<double>,vector<double> > 
         */
            
        void _mkBinHash() {
            for (size_t i = 0; i < numBinsX(); i++) {
                _binHash.first.insert(make_pair(_cachedBinEdges.first[i+1], i))  
            }
            for (size_t j = 0; j < numBinsY(); j++) {
               _binHash.second.insert(make_pair(_cachedBinEdges.second[j+1], j));
            }
        }
        
        void _mkAxis(const pair<vector<double>,vector<double> >& binedges) {
            const size_t nbinsX = binedges.first.size() - 1;
            const size_t nbinsY = binedges.second.size() -1;
            
            //Now we are pushing back the bins:
            for(int i=0; i<nbinY; i++) {
                Utils::sortedvector<BIN> Temp;
                for(int j=0; j<nbinX; j++) {
                    Temp.push_back( BIN(binedges.first[j], binedges.second[i], binedges.first[j+1], binedges.second[i+1]) ); 
                }
                Temp.sort();
                _bins.push_back(Temp);
            }
            _bins.sort();
            
            //Hashing the bin edges:
            _cachedBinEdges = binedges;
            std::sort(_cachedBinEdges.begin(), _cachedBinEdges.end());
            _mkBinHash();
        }

    public:
        //Constructors:
        
        //Default constructor with 
        Axis2D(const pair<vector<double>,vector<double> >& binedges) {
            assert(binedges.first.size() > 1 && binedges.second.size() > 1);
            _mkAxis(binedges);
        }

        //Most standard constructor, should be self-explanatory
        Axis2D(size_t nbinsX, double lowerX, double upperX, size_t nbinsY, double lowerY, double upperY) {
        _mkAxis( make_pair(linspace(nbinsX, lowerX, upperX), linspace(nbinsY, lowerY, upperY)) )
        }

        //Constructor allowing to specify a vector of vectors that house bins is not specified and
        // not supported as would make filling much more computationally involving

        
        //Some helper functions:

        //Functions returning different size statistics
        unsigned int numBinsX() const {
            return _bins[0].size();
        }
        unsigned int numBinsY() const {
            return _bins.size();
        }
        unsigned int numBinsTotal() const {
            return _bins.size()*_bins[0].size();
        }

        Bins& bins() {
            return _bins;
        }

        const Bins& bins() const {
            return _bins;
        }

        std::pair<pair<double,double>, pair<double,double> > binEdges(size_t binIdX, size_t binIdY) const {
            assert(binIdX < numBinsX() && binIdY < numBinsY());
            return make_pair(make_pair(_cachedBinEdges.first[binIdX], _cachedBinEdges.first[binIdX+1]), make_pair(_cachedBinEdges.second[binIdY], _cachedBinEdges.second[binIdY+1]));
        }

        //Edges:
        double lowEdgeX() const {
            return _bins.front().front().lowEdgeX();
        }
        double lowEdgeY() const {
            return _bins.front().front().lowEdgeY();
        }
        double highEdgeX() const {
            return _bins.front().back().highEdgeX();
        }
        double highEdgeY() const {
            return _bins.back().front().highEdgeY();
        }

        //Maybe throwing different errors for X and Y?
        BIN& bin(size_t indexX, size_t indexY) {
            if(indexX >= numBinsX() || indexY >= numBinsY()) {
                throw RangeError("YODA::Histo: index out of range");
            return _bins[indexY][indexX];
        }
        const BIN& bin(size_t indexX, size_t indexY) const{
            if(indexX >= numBinsX() || indexY >= numBinsY()) {
                throw RangeError("YODA::Histo: index out of range");
            return _bins[indexY][indexX];
        }

        BIN& binByCoord(double x, double y) {
            return bin(findBinIndex(x, y));
        }

        const BIN& binByCoord(double x, double y) const {
            return bin(findBinIndex(x, y));
        }
        BIN& binByCoord(pair<double, double>& coords) {
            return bin(findBinIndex(coords.first, coords.second));
        }

        const BIN& binByCoord(pair<double, double>& coords) const {
            return bin(findBinIndex(coords.first, coords.second));
        }



        Dbn2D& totalDbn() {
            return _dbn;
        }
        const Dbn2D& totalDbn() const{
            return _dbn;
        }

        Dbn2D& overflow() {
            return _overflow;
        }
        const Dbn2D& overflow() const {
            return _overflow;
        }

        pair<double,double> findBinIndex(double coordX, double coordY) const {
            if (coordX < _cachedBinEdges.first[0] || coordY < _cachedBinEdges.second[0] || coordX >= _cachedBinEdges.first[numBinsX] || coordY >= _cachedBinEdges.second[numBinsY]) {
                throw RangeError("Coordinate is outside the valid range: you should request the underflow or overflow");
            }

            size_t x =  _binHash.first.upper_bound(coordX) -> second;
            size_t y =  _binHash.second.lower_bound(coordY) -> second;
            return make_pair(x, y);
        }

        void reset() {
            _dbn.reset();
            _underflow.reset();
            _overflow.reset();
            for (int i=0; i<_bins.size(); i++) {
                for (typename Bins::iterator b = _bins[i].begin(); b != _bins[i].end(); b++) {
                    b -> reset();
                }
            }
        }

        void scale(double scalefactor) {
            /// @todo Implement!
            throw std:runtime_error("Axis coordinate transformations not yet implemented!");
        }

        void scaleW(double scalefactor) {
            _dbn.scaleW(scalefactor);
            _underflow.scaleW(scalefactor);
            _overflow.scaleW(scalefactor);
            for (int i=0; i<_bins.size(); i++) {
                for (typename Bins::iterator b = _bins.begin(); b != _bins.end(); b++) {
                    b -> scaleW(scalefactor);
                }
            }
        // Operators:
        bool operator == (const Axis2D& other) const {
            return 
                _cachedBinEdges.first == _cachedBinEdges.first;
                _cachedBinEdges.second == _cachedBinEdges.second;
        }

        bool operator != (const Axis2D& other) const {
            return ! operator == (other);
        }

        //We must use at() as bins() is a function
        Axis2D<BIN>& operator += (const Axis2D<BIN>& toAdd) {
            if (*this != toAdd) {
                throw LogicError("YODA::Histo1D: Cannot add axes with different binnings.");
            }
            for (int i=0; i < bins().size(); i++) {
                for (size_t j = 0; j < bins.at(i).size(); i++) {
                    bins().at(i).at(j) += toAdd.bins().at(i).at(j);
                }
            }
                _dbn += toAdd._dbn;
                _underflow += toAdd._underflow;
                _overflow += toAdd._overflow;
                return *this;
            }
        
        Axis2D<BIN>& operator -= (const Axis2D<BIN>& toSubstract) {
            if (*this != toSubstract) {
                throw LogicError("YODA::Histo1D: Cannot add axes with different binnings.");
            }
            for (int i=0; i < bins().size(); i++) {
                for (size_t j = 0; j < bins.at(i).size(); i++) {
                    bins().at(i).at(j) -= toAdd.bins().at(i).at(j);
                }
            }
                _dbn -= toSubstract._dbn;
                _underflow -= toSubstract._underflow;
                _overflow -= toSubstract._overflow;
                return *this;
            }
            
    private:
        //Bins contained in this histogram:
        Bins _bins;
        Dbn2D _underflow;
        Dbn2D _overflow;
        Dbn2D _dbn;
        
        std::pair<std::vector<double>, std::vector<double> > _cachedBinEdges;
        std::pair<std::map<double,size_t>, std::map<double,size_t> > _binHash;
           
   };

    template <typename BIN>
    Axis2D<BIN> operator + (const Axis2D<BIN>& first, const Axis2D<BIN>& second) {
        Axis2D<BIN> tmp = first;
        tmp += second;
        return tmp;
    }

    template <typename BIN>
    Axis2D<BIN> operator - (const Axis2D<BIN>& first, const Axis2D<BIN>& second) {
        Axis2D<BIN> tmp = first;
        tmp -= second;
        return tmp;
    }
    
    inline bool operator < (const pair<vector<double>, vector<double> >& a, const pair<vector<double>, vector<double> >& b) {
        if(a.first == b.first) return a.second < b.second;
        return a.first < b.first;
    }
}
