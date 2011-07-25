#ifndef YODA_SORTEDVECTOR_H
#define YODA_SORTEDVECTOR_H

#include <vector>
#include <algorithm>
#include <stdexcept>
#include <iostream>
#include <map>

namespace YODA {
    namespace Utils {
        template <typename T>
        class cachedvector : public std::vector<T> {
        public:
            cachedvector(){}
            cachedvector(const std::vector<T>& vec) : std::vector<T>(vec) {}

            //We will see if the following will work:
            void regenCache(){
                _cache.clear();
                for(size_t i=0; i<this->size(); i++) 
                    _cache.insert(std::make_pair(this->at(i).first(), i));
            }
            
            //Cache ended as a public function since rewriting lowerBound() is pointless.
            std::map<T.first, size_t> _cache;
        };
    }
}
