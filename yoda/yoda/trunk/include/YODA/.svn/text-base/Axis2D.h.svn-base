#ifndef YODA_Axis2D_h
#define YODA_Axis2D_h

#include "YODA/AnalysisObject.h"
#include "YODA/Exceptions.h"
#include "YODA/Bin.h"
#include "YODA/Utils/sortedvector.h"
#include "YODA/Utils/cachedvector.h"
#include "YODA/Utils/MathUtils.h"
#include "YODA/Dbn2D.h"
#include <string>
#include <cassert>
#include <cmath>
#include <algorithm>

using namespace std;

//And a big number for the low/high search:
const double _largeNum = 10000000000000.0;

namespace YODA {
    template <typename BIN>
    class Axis2D {
    public:
        
        typedef BIN Bin;
        typedef typename std::vector<BIN> Bins;
        
    private:

        /// Edge validator
        /** Checks if an edge is vertical or horisontal and launches
          * an appropriate checking function
          */
        bool _validateEdge(vector<pair<pair<double,double>, pair<double,double> > >& edges) {
            bool ret = true;
            for(unsigned int i=0; i < edges.size(); i++) {
                if(fuzzyEquals(edges[i].first.first, edges[i].second.first)) ret =  _findCutsY(edges[i]);
                else if(fuzzyEquals(edges[i].first.second, edges[i].second.second)) ret =  _findCutsX(edges[i]);
                else ret = false;
                
                if(!ret) return false;
            }
            return true;
        }

        /// Inclusion validator
        /** An uncompleted function that checks if there exist a group of bins 
          * included in each other. It will be invoked before adding two Axises2D
          */
        bool _validateInclusion(pair<Utils::cachedvector<pair<double,vector<pair<size_t, pair<double,double> > > > >, Utils::cachedvector<pair<double,std::vector<pair<size_t, pair<double,double> > > > > >& edges) {
            /// Making sure that the cache we will be using soon is correct and actual:
            edges.first.regenCache();
            edges.second.regenCache();

            /// Now, checking if any of the edges is cutting any other:
            for(unsigned int i=0; i < edges.first.size(); i++) {
                for(unsigned int j = 0; j < edges.first[i].second.size(); j++) {
                    size_t startX = edges.second._cache.lower_bound(approx(edges.first[i].second[j].second.first));
                    size_t endX = edges.second._cache.upper_bound(edges.first[i].second[j].second.second);
                    for(int p = startX; p < endX; p++) {
                        if(edges.first[i].first > edges.second[i].second[p].second.first &&
                           edges.first[i].first < edges.second[i].second[p].second.second){
                            return false;
                        }
                    }
                }
            }

            //TODO: Check inclusion
        }

        /// @name Binary search functions
        //@{
        /** I am exploiting the fact that we are operating on 
          * a sorted vector all the time. Therefore employing 
          * binary search to find the lower bound seems to be 
          * a logical step.
          */
        size_t _binaryS(Utils::cachedvector<pair<double, vector<pair<size_t, pair<double,double> > > > >& toSearch, double value, size_t lower, size_t higher) {
            if(lower == higher) return lower;
            size_t where = (higher+lower)/2;
            
            if(value >= toSearch[where].first) {
                if(where == toSearch.size() - 1) return where;
                if(value <= toSearch[where+1].first) return where;
                return _binaryS(toSearch, value, where, higher);
            }
            if(where == 0) return where;
            if(value >= toSearch[where-1].first) return where;
            return _binaryS(toSearch, value, lower, where);
        }
        //@}
        /// Function checking the cuts of horizontal segments
        /** It searches for edges s.t. they may cut the edge in question and
          * then checks if a cut indeed occurs.
          */
        bool _findCutsX(pair<pair<double,double>, pair<double,double> >& edge) {
            size_t i = _binaryS(_binHashSparse.second, edge.first.first, 0, _binHashSparse.second.size());
            size_t end = _binaryS(_binHashSparse.second, edge.second.first, 0, _binHashSparse.second.size());
            for(; i < end; i++) {
                    
                    for(unsigned int j = 0; j < _binHashSparse.second[i].second.size(); j++) {
                        if(_binHashSparse.second[i].second[j].second.first < edge.first.second &&
                           _binHashSparse.second[i].second[j].second.second > edge.first.second &&
                           !fuzzyEquals(_binHashSparse.second[i].second[j].second.first, edge.first.second) &&
                           !fuzzyEquals(_binHashSparse.second[i].second[j].second.second, edge.first.second)) {
                            return false;
                        }
                    }
                }
            return true;
        }

        /// Checking the cuts of vertical segments
        bool _findCutsY(pair<pair<double,double>, pair<double,double> >& edge) {
            size_t i = _binaryS(_binHashSparse.first, edge.first.second, 0, _binHashSparse.first.size());
            size_t end = _binaryS(_binHashSparse.first, edge.second.second, 0, _binHashSparse.first.size());
            for(; i < end; i++) {
                    
                    for(unsigned int j = 0; j < _binHashSparse.first[i].second.size(); j++) {
                        if(_binHashSparse.first[i].second[j].second.first < edge.first.first &&
                           _binHashSparse.first[i].second[j].second.second > edge.first.first &&
                           !fuzzyEquals(_binHashSparse.first[i].second[j].second.first, edge.first.first) &&
                           !fuzzyEquals(_binHashSparse.first[i].second[j].second.second, edge.first.first)) {
                            return false;
                        }
                    }
                }
            return true;
        }
        
        /// What to execute when an edge is dropped.
        void _dropEdge(vector<pair<pair<double,double>, pair<double,double> > >& edges) {
            std::cerr << "A set of edges was dropped. No additional information is implemented yet, so none can be given. Have a good day." << endl;
        }

        /// Function that adds an edge after it was verified by _validateEdge()
        void _addEdge(vector<pair<pair<double,double>, pair<double,double> > >& edges) {
            for(unsigned int j=0; j < edges.size(); j++) {
                pair<pair<double,double>, pair<double,double> > edge = edges[j];
                if(edge.first.first == edge.second.first) {
                    bool found = false;
                    size_t i = _binaryS(_binHashSparse.second, edge.first.first, 0, _binHashSparse.second.size())-1;
                    if(i < 0) i = 0;
                    size_t end = i+3;
                    for(; i < _binHashSparse.second.size() && i < end ; i++) {
                    if(fuzzyEquals(_binHashSparse.second[i].first, edge.first.first)) {
                        _binHashSparse.second[i].second.push_back(
                            make_pair(_bins.size(),make_pair(edge.first.second, edge.second.second)));
                        found = true;
                        }
                    }
                    if(!found) {
                        vector<pair<size_t, pair<double,double> > > temp;
                        temp.push_back(make_pair(_bins.size(), make_pair(edge.first.second, edge.second.second)));
                        _binHashSparse.second.push_back(make_pair(edge.first.first,temp));
                        sort(_binHashSparse.second.begin(), _binHashSparse.second.end());
                    }
                }

                else if(edge.first.second == edge.second.second) {
                    bool found = false;
                    size_t i = _binaryS(_binHashSparse.first, edge.first.second, 0, _binHashSparse.first.size())-1;
                    if(i < 0) i = 0;
                    size_t end = i+3;
                    for(; i < _binHashSparse.first.size() && i < end; i++) {
                        if(fuzzyEquals(_binHashSparse.first[i].first, edge.first.second)) {
                            _binHashSparse.first[i].second.push_back(
                                make_pair(_bins.size(),make_pair(edge.first.first, edge.second.first)));
                            found = true;
                        }
                    }
                    if(!found) {
                        vector<pair<size_t, pair<double,double> > > temp;
                        temp.push_back(make_pair(_bins.size(), make_pair(edge.first.first, edge.second.first)));
                        _binHashSparse.first.push_back(make_pair(edge.second.second, temp));
                        sort(_binHashSparse.first.begin(), _binHashSparse.first.end());
                    }
                }
            }
            _bins.push_back(BIN(edges));
        }
        
        /** This funcion looks on the orientation of an edge and
         * if it is incorrect, returns the correct orientation.
         */
        void _fixOrientation(pair<pair<double,double>, pair<double,double> >& edge) {
            if(fuzzyEquals(edge.first.first, edge.second.first)) {
                if(edge.first.second > edge.second.second) {
                    double temp = edge.second.second;
                    edge.second.second = edge.first.second; 
                    edge.first.second = temp;
                }
            }
            else if(edge.first.first > edge.second.first) {
                double temp = edge.first.first;
                edge.first.first = edge.second.first; 
                edge.second.first = temp;
            }
        }

        /// A function if charge of adding the edges.
        void _mkAxis(const vector<pair<pair<double,double>,pair<double,double> > >& binedges) {
            for(unsigned int i=0; i < binedges.size(); i++) {
                pair<pair<double,double>, pair<double,double> > edge1 = 
                    make_pair(binedges[i].first, 
                              make_pair(binedges[i].first.first, binedges[i].second.second));
                pair<pair<double,double>, pair<double,double> > edge2 =
                    make_pair(make_pair(binedges[i].first.first, binedges[i].second.second),
                              binedges[i].second);
                pair<pair<double,double>, pair<double,double> > edge3 =
                    make_pair(make_pair(binedges[i].second.first, binedges[i].first.second), 
                              binedges[i].second);
                pair<pair<double,double>, pair<double,double> > edge4 =
                    make_pair(binedges[i].first,
                              make_pair(binedges[i].second.first, binedges[i].first.second));

                _fixOrientation(edge1); _fixOrientation(edge2);
                _fixOrientation(edge3); _fixOrientation(edge4);

                vector<pair<pair<double,double>, pair<double,double> > > edges;
                edges.push_back(edge1); edges.push_back(edge2); 
                edges.push_back(edge3); edges.push_back(edge4);

                //TODO: the _dropEdge() part should be moved into _addEdge() function and indicate which edge 
                //      is the conflicting one, not dropping the whole edgeset, as it is doing now. Same in addBins.
                if(_validateEdge(edges))  _addEdge(edges);
                else _dropEdge(edges);
                
            }
            
            
            //Setting all the caches
            _binHashSparse.first.regenCache();
            _binHashSparse.second.regenCache();
            _regenDelimiters();
        }

        /// Generating the extrema of the graph.
        void _regenDelimiters() {
            double highEdgeX = -_largeNum;
            double highEdgeY = -_largeNum;
            double lowEdgeX = _largeNum;
            double lowEdgeY = _largeNum;

            for(unsigned int i=0; i < _bins.size(); i++) {
                if(_bins[i].xMin() < lowEdgeX) lowEdgeX = _bins[i].xMin();
                if(_bins[i].xMax() > highEdgeX) highEdgeX = _bins[i].xMax();
                if(_bins[i].yMin() < lowEdgeY) lowEdgeY = _bins[i].yMin();
                if(_bins[i].yMax() > highEdgeY) highEdgeY = _bins[i].yMax();
            }

            _lowEdgeX = lowEdgeX;
            _highEdgeX = highEdgeX;
            _lowEdgeY = lowEdgeY;
            _highEdgeY = highEdgeY;
        }

    public:
        /// @name Constructors:
        //@{
        
        /// Empty constructor:
        Axis2D() {
            vector<pair<pair<double,double>, pair<double,double> > > edges;
            _mkAxis(edges);
        }
        
        ///Default constructor 
        Axis2D(const vector<pair<pair<double,double>, pair<double,double> > >& binedges) {
            _mkAxis(binedges);
        }

        ///Most standard constructor, should be self-explanatory
        Axis2D(size_t nbinsX, double lowerX, double upperX, size_t nbinsY, double lowerY, double upperY) {
            vector<pair<pair<double,double>, pair<double,double> > > edges;
            double coeffX = (upperX - lowerX)/(double)nbinsX;
            double coeffY = (upperY - lowerX)/(double)nbinsY;

            for(double i=lowerX; i < upperX; i+=coeffX) {
                for(double j=lowerY; j < upperY; j+=coeffY) {
                    edges.push_back(make_pair(make_pair(i, j), 
                                              make_pair((double)(i+coeffX), (double)(j+coeffY))));
                }
            }
            _mkAxis(edges);
        }
        //@}

        /// @name Addition operators:
        //@{
        /** This is a bin addition operator. It is given a set of boindary points (bottom-left
         * and top-right) that uniquely determine a bin and it adds a set of bins basing on that.
         * Please, try to include as many bins as possible in one call, as regenCache() is too
         * computationaly expensive to be called for each single bin in a series.
         */
        void addBin(const vector<pair<pair<double,double>, pair<double,double> > >& vertexCoords) {
            _mkAxis(vertexCoords);
        }

        void addBin(double lowX, double lowY, double highX, double highY) {
            vector<pair<pair<double,double>, pair<double,double> > > coords;
            coords.push_back(make_pair(make_pair(lowX, lowY), make_pair(highX, highY)));
            
            addBin(coords);
        }
        //@}

        /// @name Some helper functions:
        //@{

        /// Return a total number of bins in Histo

        /// Checks if our bins form a grid. 
        /** Uses a very neat property of _binCacheSparse, 
          * namely that it will containg the same number of
          * edges on inner sides and half the number on outer ones*/
        int isGriddy() {
            unsigned int sizeX = _binHashSparse.first[0].second.size();
            for(unsigned int i=1; i < _binHashSparse.first.size(); i++) {
                if(i == _binHashSparse.first.size() - 1) {
                    if(_binHashSparse.first[i].second.size() != sizeX) {
                        return -1;
                    }
                }
                else if(_binHashSparse.first[i].second.size() != 2*sizeX) {
                    return -1;
                }
            }
            unsigned int sizeY = _binHashSparse.second[0].second.size();
            for(unsigned int i=1; i < _binHashSparse.second.size(); i++) {
                if(i!= _binHashSparse.second.size() - 1) {
                    if(2*sizeY != _binHashSparse.second[i].second.size()) {
                        return -1;
                    }
                }
                else if(_binHashSparse.second[i].second.size() != sizeY) return -1;
            }
            return 0;
        }


        unsigned int numBinsTotal() const {
            return _bins.size();
        }

        /// Get inf(X) (non-const version)
        double lowEdgeX() {
            return _lowEdgeX;
        }

        /// Get sup(X) (non-const version)
        double highEdgeX() {
            return _highEdgeX;
        }

        /// Get inf(Y) (non-const version) 
        double lowEdgeY() {
            return _lowEdgeY;
        }

        /// Get sup(Y) (non-const version)
        double highEdgeY() {
            return _highEdgeY;
        }

        /// Get inf(X) (const version)
        const double lowEdgeX() const {
            return _lowEdgeX;
        }

        /// Get sup(X) (const version)
        const double highEdgeX() const {
            return _highEdgeX;
        }

        /// Get inf(Y)
        const double lowEdgeY() const {
            return _lowEdgeY;
        }
        
        ///Get sup(Y)
        const double highEdgeY() const {
            return _highEdgeY;
        }

        /// Get the bins from an Axis (non-const version)
        Bins& bins() {
            return _bins;
        }

        /// Get the bins from an Axis (const version)
        const Bins& bins() const {
            return _bins;
        }
    
        /// Get a bin with a given index (non-const version)
        BIN& bin(size_t index) {
            if(index >= _bins.size()) throw RangeError("YODA::Histo2D: index out of range");
            return _bins[index];
        }

        /// Get a bin with a given index (const version)
        const BIN& bin(size_t index) const{
            if(index >= _bins.size()) throw RangeError("YODA::Histo2D: index out of range");
            return _bins[index];
        }

        /// Get a bin at given coordinates (non-const version)
        BIN& binByCoord(double x, double y) {
            int ret = findBinIndex(x, y);
            if(ret != -1) return bin(ret);
            else throw RangeError("No bin found!!");
        }

        /// Get a bin at given coordinates (const version)
        const BIN& binByCoord(double x, double y) const {
            return bin(findBinIndex(x, y));
        }

        /// Get a bin at given coordinates (non-const version)
        BIN& binByCoord(pair<double, double>& coords) {
            return bin(findBinIndex(coords.first, coords.second));
        }
        
        /// Get a bin at given coordinates (const version)
        const BIN& binByCoord(pair<double, double>& coords) const {
            return bin(findBinIndex(coords.first, coords.second));
        }

        /// Get a total distribution (non-const version)
        Dbn2D& totalDbn() {
            return _dbn;
        }

        /// Get a total distribution (const version)
        const Dbn2D& totalDbn() const{
            return _dbn;
        }

        /// Get the overflow distribution (non-const version)
        Dbn2D& overflow() {
            return _overflow;
        }

        /// Get the overflow distribution (const version)
        const Dbn2D& overflow() const {
            return _overflow;
        }

        /// Get the underflow distribution (non-const version)
        Dbn2D& underflow() {
            return _underflow;
        }

        /// Get the underflow distribution (const version)
        const Dbn2D& underflow() const {
            return _underflow;
        }

        /// Get the binHash(non-const version)
        std::pair<Utils::cachedvector<pair<double,std::vector<pair<size_t, pair<double,double> > > > >,
                  Utils::cachedvector<pair<double,std::vector<pair<size_t, pair<double,double> > > > > > getHash() {
            return _binHashSparse;
        }
        
        /// Get the binHash(const version)
        const std::pair<Utils::cachedvector<pair<double,std::vector<pair<size_t, pair<double,double> > > > >,
                  Utils::cachedvector<pair<double,std::vector<pair<size_t, pair<double,double> > > > > > getHash() const {
            return _binHashSparse;
        }


        /** This version of findBinIndex is searching for an edge on the left
         *  that is enclosing the point and then finds an edge on the bottom
         *  that does the same and if it finds two edges that are a part of 
         *  the same square it returns that it had found a bin. If no bin is 
         *  found, ie. (coordX, coordY) is a point in empty space -1 is returned.
         */
        int findBinIndex(double coordX, double coordY) const {
            coordX += 0.0000000001; coordY += 0.00000000001;

            size_t indexY = (*_binHashSparse.first._cache.lower_bound(approx(coordY))).second;

            if(indexY < _binHashSparse.first.size()) {
                for(unsigned int i = 0;  i < _binHashSparse.first[indexY].second.size(); i++){
                    if(_binHashSparse.first[indexY].second[i].second.first < coordX &&
                       _binHashSparse.first[indexY].second[i].second.second > coordX){
                        size_t indexX = (*_binHashSparse.second._cache.lower_bound(approx(coordX))).second;
                        if(indexX < _binHashSparse.second.size()){
                            for(unsigned int j=0; j < _binHashSparse.second[indexX].second.size(); j++) {
                                if(_binHashSparse.second[indexX].second[j].second.first < coordY &&
                                   (_binHashSparse.second[indexX].second[j].second.second > coordY) &&
                                   (_binHashSparse.second[indexX].second[j].first ==
                                   _binHashSparse.first[indexY].second[i].first)) 
                                    return _binHashSparse.second[indexX].second[j].first;
                            }
                        }
                    }
                }
            }
            return -1;
        }

        /// Resetts the axis
        void reset() {
            _dbn.reset();
            _underflow.reset();
            _overflow.reset();
            for (size_t i=0; i<_bins.size(); i++) _bins[i].reset();
        }

        /// Scales the axis in a given direction by a specified coefficient
        void scale(double scaleX = 1.0, double scaleY = 1.0) {
            // Two loops are put on purpose, just to protect
            // against improper _binHashSparse
            for(unsigned int i=0; i < _binHashSparse.first.size(); i++) {
                _binHashSparse.first[i].first *= scaleY;
                for(unsigned int j=0; j < _binHashSparse.first[i].second.size(); j++){
                    _binHashSparse.first[i].second[j].second.first *=scaleX;
                    _binHashSparse.first[i].second[j].second.second *=scaleX;
                }
            }
            for(unsigned int i=0; i < _binHashSparse.second.size(); i++) {
                _binHashSparse.second[i].first *= scaleX;
                for(unsigned int j=0; j < _binHashSparse.second[i].second.size(); j++){
                    _binHashSparse.second[i].second[j].second.first *=scaleY;
                    _binHashSparse.second[i].second[j].second.second *=scaleY;
                }
            }

            _binHashSparse.first.regenCache();
            _binHashSparse.second.regenCache();

            // Now, as we have the map rescaled, we need to update the bins
            // in their own structure in order to have high/low edges correct
            for(unsigned int i=0; i < _bins.size(); i++) _bins[i].scale(scaleX, scaleY);
            _dbn.scale(scaleX, scaleY);
            _underflow.scale(scaleX, scaleY);
            _overflow.scale(scaleX, scaleY);

            //And making sure that we have correct boundaries set after rescaling
            _regenDelimiters();
        }

        /// Scales the heights of the bins
        void scaleW(double scalefactor) {
            _dbn.scaleW(scalefactor);
            _underflow.scaleW(scalefactor);
            _overflow.scaleW(scalefactor);
            for (unsigned int i=0; i<_bins.size(); i++) _bins[i].scaleW(scalefactor);
        }
       //@}

       /// @name Operators:
       //@{

        /// Equality operator
        bool operator == (const Axis2D& other) const {
            return _binHashSparse == other._binHashSparse;
        }

        /// Non-equality operator
        bool operator != (const Axis2D& other) const {
            return ! operator == (other);
        }

        /// Addition operator
        /** At this stage it is only possible to add two histograms with
          * the same binnings. Compatible but not equal binning soon to come
          */
        Axis2D<BIN>& operator += (const Axis2D<BIN>& toAdd) {
            if (*this != toAdd) {
                throw LogicError("YODA::Histo1D: Cannot add axes with different binnings.");
            }
            for (unsigned int i=0; i < bins().size(); i++) bins().at(i) += toAdd.bins().at(i);
    
            _dbn += toAdd._dbn;
            _underflow += toAdd._underflow;
            _overflow += toAdd._overflow;
            return *this;
        }
        
        /// Substraciton operator
        Axis2D<BIN>& operator -= (const Axis2D<BIN>& toSubstract) {
            if (*this != toSubstract) {
                throw LogicError("YODA::Histo1D: Cannot add axes with different binnings.");
            }
            for (unsigned int i=0; i < bins().size(); i++) bins().at(i) -= toSubstract.bins().at(i);
            
            _dbn -= toSubstract._dbn;
            _underflow -= toSubstract._underflow;
            _overflow -= toSubstract._overflow;
            return *this;
        }
        //@}

    private:
        
        /// Bins contained in this histogram
        Bins _bins;

        /// Underflow distribution
        Dbn2D _underflow;

        /// Overflow distribution
        Dbn2D _overflow;

        /// The total distribution
        Dbn2D _dbn;
       
        /// Bin hash structure
        /** First in pair is holding the horizontal edges indexed by first.first 
          * which is an y coordinate. The last pair specifies x coordinates (begin, end) of 
          * the horizontal edge. 
          * Analogous for the second member of the pair.
          */
        std::pair<Utils::cachedvector<pair<double,std::vector<pair<size_t, pair<double,double> > > > >,
                  Utils::cachedvector<pair<double,std::vector<pair<size_t, pair<double,double> > > > > > 
                  _binHashSparse;

        /// Low/High edges:
        double _highEdgeX, _highEdgeY, _lowEdgeX, _lowEdgeY;

   };
   
    /// Additon operator
    template <typename BIN>
    Axis2D<BIN> operator + (const Axis2D<BIN>& first, const Axis2D<BIN>& second) {
        Axis2D<BIN> tmp = first;
        tmp += second;
        return tmp;
    }

    /// Substraciton operator
    template <typename BIN>
    Axis2D<BIN> operator - (const Axis2D<BIN>& first, const Axis2D<BIN>& second) {
        Axis2D<BIN> tmp = first;
        tmp -= second;
        return tmp;
    }
    
    /// Less-than operator
    inline bool operator < (const pair<vector<double>, vector<double> >& a, const pair<vector<double>, vector<double> >& b) {
        if(a.first == b.first) return a.second < b.second;
        return a.first < b.first;
    }
    
}

#endif
