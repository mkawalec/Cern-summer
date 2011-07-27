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

        // Notice the fact that all the functions below make an error
        // of the size of fuzzyEquals tolerance!
        // Also, there are no checks in place to test if this edge set is not crossing itself
        bool _validateEdge(vector<pair<pair<double,double>, pair<double,double> > > edges) {
            bool ret = true;
            for(int i=0; i < edges.size(); i++) {
                if(edges[i].first.first == edges[i].second.first) ret =  _findCutsY(edges[i]);
                else if(edges[i].first.second == edges[i].second.second) ret =  _findCutsX(edges[i]);
                else ret = false;
                
                if(!ret) return false;
            }
            return true;
        }

        //This function will check if all of the edges are spanning figures not mutually inclusive
        //First it will check if the edges cross. It will also be used to check if _binHashSparse 
        //contains errors, prior to computation.
        bool _validateInclusion(pair<Utils::cachedvector<pair<double,vector<pair<size_t, pair<double,double> > > > >, Utils::cachedvector<pair<double,std::vector<pair<size_t, pair<double,double> > > > > >& edges) {
            //Making sure that the cache we will be using soon is correct and actual:
            edges.first.regenCache();
            edges.second.regenCache();

            //Now, checking if any of the edges is cutting any other:
            for(int i=0; i < edges.first.size(); i++) {
                for(int j = 0; j < edges.first[i].second.size(); j++) {
                    size_t startX = edges.second._cache.lower_bound(approx(edges.first[i].second[j].second.first));
                    size_t endX = edges.second._cache.upper_bound(edges.first[i].second[j].second.second);
                    for(int p = startX; p < endX; p++) {
                        //We are not checking the edges as we are fine with overlapping bins
                        //The partially overlapping ones will be filtered out in next pass
                        if(edges.first[i].first > edges.second[i].second[p].second.first &&
                           edges.first[i].first < edges.second[i].second[p].second.second){
                            return false;
                        }
                    }
                }
            }

            //TODO: Check inclusion
        }

        bool _findCutsY(pair<pair<double,double>, pair<double,double> > edge) {
            for(int i=0; i < _binHashSparse.second.size(); i++) {
                /* An optimisation check that guarantees that we are not looking at edges that
                 * are surely out of our range of interest. The second condition is put in place
                 * to correct for possible rounding errors in double numbers.
                 */
                if(edge.second.second < _binHashSparse.second[i].first &&
                   !fuzzyEquals(_binHashSparse.second[i].first, edge.second.second)) break;

                if(fuzzyEquals(_binHashSparse.second[i].first, edge.first.second) ||
                  (_binHashSparse.second[i].first > edge.first.second &&
                   _binHashSparse.second[i].first < edge.second.second) ||
                   fuzzyEquals(_binHashSparse.second[i].first, edge.second.second)) {
                    for(int j=0; j < _binHashSparse.second[i].second.size(); j++) {
                        
                        //Same type of check as above.
                        if(_binHashSparse.second[i].second[j].second.first > edge.first.first &&
                            !fuzzyEquals(_binHashSparse.second[i].second[j].second.first, edge.first.first)) break;
                            
                        if(fuzzyEquals(_binHashSparse.second[i].second[j].second.first, edge.first.first) ||
                           (_binHashSparse.second[i].second[j].second.first < edge.first.first &&
                            _binHashSparse.second[i].second[j].second.second > edge.first.first) ||
                           fuzzyEquals(_binHashSparse.second[i].second[j].second.second, edge.first.first)) {
                            return false;
                        }
                    }
                }
            }
            return true;
        }

        bool _findCutsX(pair<pair<double,double>, pair<double,double> > edge) {
            for(int i=0; i < _binHashSparse.first.size(); i++) {
                //Sanity check, for more comments see above:
                if(edge.second.first < _binHashSparse.first[i].first &&
                   !fuzzyEquals(edge.second.first, _binHashSparse.first[i].first)) break;

                if(fuzzyEquals(_binHashSparse.first[i].first, edge.first.first) ||
                  (_binHashSparse.first[i].first > edge.first.first &&
                   _binHashSparse.first[i].first < edge.second.first ) ||
                   fuzzyEquals(_binHashSparse.first[i].first, edge.second.first)) {
                    for(int j=0; j < _binHashSparse.first[i].second.size(); j++) {
                        
                        if(_binHashSparse.first[i].second[j].second.first > edge.first.second &&
                           !fuzzyEquals(_binHashSparse.first[i].second[j].second.first, edge.first.second)) break;

                        if(fuzzyEquals(_binHashSparse.first[i].second[j].second.first, edge.first.second) ||
                           (_binHashSparse.first[i].second[j].second.first < edge.first.second &&
                            _binHashSparse.first[i].second[j].second.second > edge.first.second) ||
                           fuzzyEquals(_binHashSparse.first[i].second[j].second.second, edge.first.second)) {
                            return false;
                        }
                    }
                }
            }
            return true;
        }
        
        //TODO: Something a bit more elaborate??
        void _dropEdge(vector<pair<pair<double,double>, pair<double,double> > > edges) {
            std::cerr << "A set of edges was dropped. No additional information is implemented yet, so none can be given. Have a good day." << endl;
        }

        //Do not initiate a global sort when another edges were found on the same level
        // needs to be adjusted accordingly
        void _addEdge(vector<pair<pair<double,double>, pair<double,double> > > edges) {
            for(int j=0; j < edges.size(); j++) {
                pair<pair<double,double>, pair<double,double> > edge = edges[j];
                if(edge.first.first == edge.second.first) {
                    bool found = false;
                    for(int i=0; i < _binHashSparse.second.size(); i++) {
                    if(fuzzyEquals(_binHashSparse.second[i].first, edge.first.first)) {
                        _binHashSparse.second[i].second.push_back(
                            make_pair(_bins.size(),make_pair(edge.first.second, edge.second.second)));
                        sort(_binHashSparse.second[i].second.begin(), _binHashSparse.second[i].second.end());
                        found = true;
                        }
                    }
                    if(!found) {
                        vector<pair<size_t, pair<double,double> > > temp;
                        temp.push_back(make_pair(_bins.size(), make_pair(edge.first.second, edge.second.second)));
                        _binHashSparse.second.push_back(make_pair(edge.first.first,temp));
                    }
                }

                else if(edge.first.second == edge.second.second) {
                    bool found = false;
                    for(int i=0; i < _binHashSparse.first.size(); i++) {
                        if(fuzzyEquals(_binHashSparse.first[i].first, edge.first.second)) {
                            _binHashSparse.first[i].second.push_back(
                                make_pair(_bins.size(),make_pair(edge.first.first, edge.second.first)));
                            sort(_binHashSparse.first[i].second.begin(), _binHashSparse.first[i].second.end());
                            found = true;
                        }
                    }
                    if(!found) {
                        vector<pair<size_t, pair<double,double> > > temp;
                        temp.push_back(make_pair(_bins.size(), make_pair(edge.first.first, edge.second.first)));
                        _binHashSparse.first.push_back(make_pair(edge.second.second, temp));
                    }
                }
            }
            _bins.push_back(BIN(edges[0].first.first, edges[0].first.second, 
                                edges[1].second.first, edges[1].second.second));
        }

        // Note the orientation! The edge vectors must be oriented 'to the right' or 'upwards'
        // for all procedures to work fine!!111!!!11
        void _mkAxis(const vector<pair<pair<double,double>,pair<double,double> > >& binedges) {
            for(int i=0; i < binedges.size(); i++) {
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
                //TODO: Add a function that fixes orientation if it is wrong

                vector<pair<pair<double,double>, pair<double,double> > > edges;
                edges.push_back(edge1); edges.push_back(edge2); edges.push_back(edge3); edges.push_back(edge4);
                //TODO: the _dropEdge() part should be moved into _addEdge() function and indicate which edge 
                //      is the conflicting one, not dropping the whole edgeset, as it is doing now. Same in addBins.
                if(_validateEdge(edges)) _addEdge(edges);
                else _dropEdge(edges);
            }

            //Setting all the caches
            _binHashSparse.first.regenCache();
            _binHashSparse.second.regenCache();
            _regenDelimiters();
        }

        void _regenDelimiters() {
            double highEdgeX = -_largeNum;
            double highEdgeY = -_largeNum;
            double lowEdgeX = _largeNum;
            double lowEdgeY = _largeNum;

            for(int i=0; i < _bins.size(); i++) {
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
        //Constructors:
        
        //Default constructor with 
        Axis2D(const vector<pair<pair<double,double>, pair<double,double> > >& binedges) {
            _mkAxis(binedges);
        }

        //Most standard constructor, should be self-explanatory
        Axis2D(size_t nbinsX, double lowerX, double upperX, size_t nbinsY, double lowerY, double upperY) {
            vector<pair<pair<double,double>, pair<double,double> > > edges;
            double coeffX = (upperX - lowerX)/(double)nbinsX;
            double coeffY = (upperY - lowerX)/(double)nbinsY;

            for(int i=0; i < coeffX - 1; i++) {
                for(int j=0; j < coeffY - 1; j++) {
                   edges.push_back(make_pair(make_pair(i*coeffX, j*coeffY), 
                                             make_pair((double)(i+1)*coeffX, (double)(j+1)*coeffY)));
                }
            }
            _mkAxis(edges);
        }

        /* This is a bin addition operator. It is given a set of boindary points (bottom-left
         * and top-right) that uniquely determine a bin and add a set of bins basing on that.
         * Please, try to include as many bins as possible in one call, as regenCache() is too
         * computationaly expensive to be called after each one bin is added.
         */
        void addBin(const vector<pair<pair<double,double>, pair<double,double> > >& binedges) {
            for(int i = 0; i < binedges.size(); i++){
                vector<pair<pair<double,double>, pair<double,double> > > temp;
                
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
                temp.push_back(edge1); temp.push_back(edge2); 
                temp.push_back(edge3); temp.push_back(edge4);
                if(_validateEdge(binedges)) _addEdge(binedges);
                else _dropEdge(binedges);
            }

            //Setting all the caches
            _binHashSparse.first.regenCache();
            _binHashSparse.second.regenCache();
            _regenDelimiters();
        }
        
        //Some helper functions:

        //numBins{X,Y} were dropped as there is no point for them in a sparse distribution.
        unsigned int numBinsTotal() const {
            return _bins.size();
        }

        double lowEdgeX() {
            return _lowEdgeX;
        }

        double highEdgeX() {
            return _highEdgeX;
        }

        double lowEdgeY() {
            return _lowEdgeY;
        }

        double highEdgeY() {
            return _highEdgeY;
        }

        const double lowEdgeX() const {
            return _lowEdgeX;
        }

        const double highEdgeX() const {
            return _highEdgeX;
        }

        const double lowEdgeY() const {
            return _lowEdgeY;
        }

        const double highEdgeY() const {
            return _highEdgeY;
        }

        Bins& bins() {
            return _bins;
        }

        const Bins& bins() const {
            return _bins;
        }

        BIN& bin(size_t index) {
            if(index >= _bins.size()) throw RangeError("YODA::Histo2D: index out of range");
            return _bins[index];
        }

        const BIN& bin(size_t index) const{
            if(index >= _bins.size()) throw RangeError("YODA::Histo2D: index out of range");
            return _bins[index];
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

        const Dbn2D& underflow() const {
            return _underflow;
        }

        Dbn2D& underflow() {
            return _underflow;
        }

        /* This version of findBinIndex is searching for the edge on the left
         * that is enclosing the point and then finds an edge on the bottom
         * that does the same and if it finds two edges that are a part of 
         * the same square it returns that if had found a bin. If no bin is 
         * found, ie. (coordX, coordY) is a point in empty space -1 is returned.
         */
        //TODO: Make _binHashSparse.first/second.second a memeber of Utils::cachedvector
        int findBinIndex(double coordX, double coordY) const {
            size_t indexY = (*_binHashSparse.first._cache.lower_bound(approx(coordY))).second;

            if(indexY < _binHashSparse.first.size() - 1) {
                for(int i=0; i < _binHashSparse.first[indexY].second.size(); i++){
                    if(_binHashSparse.first[indexY].second[i].second.first < coordX &&
                       _binHashSparse.first[indexY].second[i].second.second > coordX){
                        size_t indexX = (*_binHashSparse.second._cache.lower_bound(approx(coordX))).second;
                        if(indexX < _binHashSparse.second.size() - 1){
                            for(int j=0; j < _binHashSparse.second[indexX].second.size(); j++) {
                                if(_binHashSparse.second[indexX].second[j].second.first < indexY &&
                                   _binHashSparse.second[indexX].second[j].second.second > indexY &&
                                   (_binHashSparse.first[indexX].second[j].first ==
                                   _binHashSparse.first[indexY].second[i].first)) 
                                    return _binHashSparse.first[indexX].second[j].second.first;
                            }
                        }
                    }
                }
            }
            return -1;
        }

        /* This function looks for a first (and, as we assume, the only) occurence
         * of four the same numbers in row. If it exists, it means that a rectangle
         * was detected. Even though it is a part of a wrong implementation of findBinIndex,
         * I won't delete it right now.
         */
        int search(vector<size_t> numbers) {
            size_t binNum = -1; size_t count = -1;
            for(int i=0; i < numbers.size(); i++) {
                if(binNum != numbers[i]) {
                    count = 1;
                    binNum = numbers[i];
                }
                else if(count < 4) count++;
                else if(count == 4) return binNum;
            }
            return -1;
        }

        void reset() {
            _dbn.reset();
            _underflow.reset();
            _overflow.reset();
            for (size_t i=0; i<_bins.size(); i++) _bins[i].reset();
        }

        //TODO: In-bin stats scalling (x/y Mean, Variance, stdDev...)
        void scale(double scaleX = 1.0, double scaleY = 1.0) {
            // Two loops are put on purpose, just to protect
            // against improper _binHashSparse
            for(int i=0; i < _binHashSparse.first.size(); i++) {
                _binHashSparse.first[i].first *= scaleY;
                for(int j=0; j < _binHashSparse.first[i].second.size(); j++){
                    _binHashSparse.first[i].second[j].second.first *=scaleX;
                    _binHashSparse.first[i].second[j].second.second *=scaleX;
                }
            }
            for(int i=0; i < _binHashSparse.second.size(); i++) {
                _binHashSparse.second[i].first *= scaleX;
                for(int j=0; j < _binHashSparse.second[i].second.size(); j++){
                    _binHashSparse.second[i].second[j].second.first *=scaleY;
                    _binHashSparse.second[i].second[j].second.second *=scaleY;
                }
            }

            // Now, as we have the map rescaled, we need to update the bins
            // in their own structure in order to have high/low edges correct
            for(int i=0; i < _bins.size(); i++){
                _bins[i].highEdgeX() *= scaleX;
                _bins[i].lowEdgeX() *= scaleX;

                _bins[i].highEdgeY() *= scaleY;
                _bins[i].lowEdgeY() *= scaleY;
            }

            //And making sure that we have correct boundaries set after rescaling
            _regenDelimiters();
        }

        void scaleW(double scalefactor) {
            _dbn.scaleW(scalefactor);
            _underflow.scaleW(scalefactor);
            _overflow.scaleW(scalefactor);
            for (int i=0; i<_bins.size(); i++) _bins[i].scaleW(scalefactor);
        }
       
       // Operators:
       /* This is also not trivial as both the location and contents of the bins must be checked.
        * Disregard if not needed for analyses.
        */
        bool operator == (const Axis2D& other) const {
            return _binHashSparse == other._binHashSparse;
        }

        bool operator != (const Axis2D& other) const {
            return ! operator == (other);
        }

        // Since adding two histos that have a different binning requires a thorough validation,
        // I just assume that it is only possible to add two histos that are exactly the same.
        Axis2D<BIN>& operator += (const Axis2D<BIN>& toAdd) {
            if (*this != toAdd) {
                throw LogicError("YODA::Histo1D: Cannot add axes with different binnings.");
            }
            for (int i=0; i < bins().size(); i++) bins().at(i) += toAdd.bins().at(i);
    
            _dbn += toAdd._dbn;
            _underflow += toAdd._underflow;
            _overflow += toAdd._overflow;
            return *this;
        }
        
        
        Axis2D<BIN>& operator -= (const Axis2D<BIN>& toSubstract) {
            if (*this != toSubstract) {
                throw LogicError("YODA::Histo1D: Cannot add axes with different binnings.");
            }
            for (int i=0; i < bins().size(); i++) bins().at(i) -= toSubstract.bins().at(i);
            
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
        std::pair<Utils::cachedvector<pair<double,std::vector<pair<size_t, pair<double,double> > > > >,
                  Utils::cachedvector<pair<double,std::vector<pair<size_t, pair<double,double> > > > > > 
                  _binHashSparse;

        //Low/High edges:
        double _highEdgeX, _highEdgeY, _lowEdgeX, _lowEdgeY;

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

#endif
