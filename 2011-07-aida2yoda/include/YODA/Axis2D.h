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
        typedef typename Utils::sortedvector<BIN> Bins;

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

        //_binHash is of type pair< vector <double>, vector <double> >, 
        // it is used for indexing the bin edges
        void _mkBinHash() {
            for (size_t i = 0; i < numBinsX(); i++) {
                _binHash.first.insert(make_pair(cachedBinEdges.first[i+1], i))   
            for (size_t j = 0; j < numBinsY(); j++) {
               _binHash.second.insert(make_pair(cachedBinEdges.second[j+1], j));
            }
        }
        
        void _mkAxis(const pair<vector <double>, vector<double> >& binedges) {
            const size_t nbinsX = binedges.first.size() - 1;
            const size_t nbinsY = binedges.second.size() -1;

            
