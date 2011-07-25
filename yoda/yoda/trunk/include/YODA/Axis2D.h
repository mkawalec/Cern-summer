#ifndef YODA_Axis2D_h
#define YODA_Axis2D_h

#include "YODA/AnalysisObject.h"
#include "YODA/Exceptions.h"
#include "YODA/Bin.h"
#include "YODA/Utils/sortedvector.h"
#include "YODA/Utils/MathUtils.h"
#include "YODA/Dbn2D.h"
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
        typedef typename std::vector<BIN> Bins;
        
    private:

        // Notice the fact that all the functions below make an error
        // of the size of fuzzyEquals tolerance!
        // Also, there are no checks in place to test if this edge set is not crossing itself
        bool _validateEdge(vector<pair<pair<double,double>, pair<double,double> > >& edges) {
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

            // So now, as we are sure that no ordinary crossings take place, 
            // let's look for 'full inclusions'.
        
        bool _findCutsY(pair<pair<double,double>, pair<double,double>& edge) {
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

        bool _findCutsX(pair<pair<double,double>, pair<double,double>& edge) {
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
                           !fuzzyEquals(_binHashSparse.first[i].second[j].second.fist, edge.first.second)) break;
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

        void _dropEdge(vector<pair<pair<double,double>, pair<double,double> > >& edges) {
            std::cerr << "A set of edges was dropped. No additional information is implemented yet, so none can be given. Have a good day." << endl;
        }

        //Do not initiate a global sort when another edges were found on the same level
        // needs to be adjusted accordingly
        void _addEdge(vector<pair<pair<double,double>, pair<double,double> > >& edges) {
            for(int j=0; j < edges.size(); j++) {
                pair<pair<double,double>, pair<double,double> > edge = edges[j];
                if(edge.first.first == edge.second.first) {
                    bool found = false;
                    for(int i=0; i < _binHashSparse.second.size(); i++) {
                    if(fuzzyEquals(_binHashSparse.second[i].first, edge.first.first)) {
                        _binHashSparse.second[i].second.push_back(
                            make_pair(_bins.size(),make_pair(edge.first.second, edge.second.second)));
                        _binHashSparse.second[i].second.sort();
                        found = true;
                        }
                    }
                    if(!found) {
                        vector<pair<double,double> > temp;
                        temp.push_back(make_pair(edge.first.second, edge.second.second));
                        _binHashSparse.second.push_back(make_pair(_bins.size(),make_pair(edge.first.first, temp)));
                    }
                }

                else if(edge.first.second == edge.second.second) {
                    bool found = false;
                    for(int i=0; i < _binHashSparse.first.size(); i++) {
                        if(fuzzyEquals(_binHashSparse.first[i].first, edge.first.second)) {
                            _binHashSparse.first[i].second.push_back(
                                make_pair(_bins.size(),make_pair(edge.first.first, edge.second.first)));
                            _binHashSparse.first[i].second.sort();
                            found = true;
                        }
                    }
                    if(!found) {
                        vector<pair<double,double> > temp;
                        temp.push_back(make_pair(edge.first.first, edge.second.first));
                        _binHashSparse.first.push_back(make_pair(_bins.size(),make_pair(edge.first.second, temp)));
                    }
                }
            }
            _bins.push_back(BIN(edges[0].first.first, edges[0].first.second, 
                                edges[1].second.first, edges[1].second.second));

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

                vector<pair<pair<double,double>, pair<double,double> > edges;
                edges.push_back(edge1); edges.push_back(edge2); edges.push_back(edge3); edge.push_back(edge4);
                //TODO: the _dropEdge() part should be moved into _addEdge() function and indicate which edge 
                //      is the conflicting one, not dropping the whole edgeset, as it is doing now. Same in addBins.
                if(_validateEdge(edges)) _addEdge(edges);
                else _dropEdge(edges);
            }
            _binHashSparse.first.regenCache();
            _binHashSparse.second.regenCache();
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
                                             make_pair((i+1)*coeffX, (j+1)*coeffY)));
                }
            }
            _mkAxis(edges);
        }

        /* This is a bin addition operator. It is given a set of boindary points (bottom-left
         * and top-right) that uniquely determine a bin and add a set of bins basing on that.
         * Please, try to include as many bins as possible in one call, as regeCache() is too
         * computationaly expensive to be called after one bin is added.
         */
        void addBin(const vector<pair<pair<double,double>, pair<double,double> > >& binedges) {
            for(int=0; i < binedges.size(); i++){
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
            _binHashSparse.first.regenCache();
            _binHashSparse.second.regenCache();
        }
        
        //Some helper functions:

        //numBins{X,Y} were dropped as there is no point for them in the sparse distribution.
        unsigned int numBinsTotal() const {
            return _bins.size();
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

        /* This is a function that returns in which bin can a given point be placed.
         * It will return -1 if the point if outside any of the bins (i.e. falls onto
         * an empty space). To get the index it uses two maps acting as caches, searches on
         * which should be executed in ln(n) time, so the total complexity should be in the 
         * bounds of O(ln(n)). 
         * An interesing point to note here is that the more irregular the structure, the faster
         * is the fill going to be (when it gets more regular the ln(n) part gets smaller, but
         * the n part which searches for a bin get bigger faster).
         * Notice that n in the above is not the total amount of bins but the number of edges
         * in the cache. 
         * double approx(double) returns a number floored at 5th decimal place.
         */
        int findBinIndex(double coordX, double coordY) const {
            size_t indexY = _binHashSparse.first._cache.lower_bound(approx(coordY));
            size_t indexX = _binHashSparse.second._cache.lower_bound(approx(coordX));

            if((indexY < _binHashSparse.first.size() - 1) && 
               (indexX < _binHashSparse.first.size() - 1)) {
                vector<size_t> binNumbers;
                for(int i=0; i < _binHashSparse.first[indexY].second.size(); i++) 
                    binNumbers.push_back(_binHashSparse.first[indexY].second[i].first);
                for(int i=0; i < _binHashSparse.second[indexX].second.size(); i++) 
                    binNumbers.push_back(_binHashSparse.second[indexX].second[i].first);
                
                binNumbers.sort();
                return search(binNumbers);
            }
            return -1;
        }

        int findBinIndex(double coordX, double coordY) const {
            size_t indexY = _binHashSparse.first._cache.lower_bound(approx(coordY));

            if(indexY < _binHashSparse.first.size() - 1) {
                for(int i=0; i < _binHashSparse.first[indexY].second.size(); i++){
                    if(_binHashSparse.first[indexY].second[i].second.first < coordX &&
                       _binHashSparse.first[indexY].second[i].second.second > coordX){
                        size_t indexX = _binHashSparse.second._cache.lower_bound(approx(coordX));
                        if(indexX < _binHashSparse.second.size() - 1){
                            for(int j=0; j < _binHashSparse.second[indexX].second.size(); j++) {
                                if(_binHashSparse.second[indexX].second[j].second.first < indexY &&
                                   _binHashSparse.second[indexX].second[j].second.second > indexY &&
                                   (_binHashSparse.first[indexX].second[j].first ==
                                   _binHashSparse,first[indexY].second[i].first)) 
                                    return _binHashSparse.first[indexX].second[j].second.first;
                            }
                        }
                    }
                }
            }
            return -1;
        }



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

        void scale(double scalefactor) {
            /// @todo Implement!
            throw std::runtime_error("Axis coordinate transformations not yet implemented!");
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
            return 1;
                //TODO
        }

        bool operator != (const Axis2D& other) const {
            return ! operator == (other);
        }

        //Adding two axises requires quite a bit of thorough validation. Is it needed at all?
        /*
        Axis2D<BIN>& operator += (const Axis2D<BIN>& toAdd) {
            if (*this != toAdd) {
                throw LogicError("YODA::Histo1D: Cannot add axes with different binnings.");
            }
            for (int i=0; i < bins().size(); i++) bins().at(i) += toAdd.bins().at(i);
    
            _dbn += toAdd._dbn;
            _underflow += toAdd._underflow;
            _overflow += toAdd._overflow;
            return *this;
        }*/
        
        //What does it mean exactly to substract two Axis2Ds?
        /*
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
        */    
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
           
   };
   /* 
    //TODO: Add a comparison operation for _binHashSparse (may not be needed)
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
    */
}

#endif
