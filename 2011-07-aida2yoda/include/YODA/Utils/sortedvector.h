#ifndef YODA_SORTEDVECTOR_H
#define YODA_SORTEDVECTOR_H

#include <vector>
#include <algorithm>
#include <stdexcept>
#include <iostream>

namespace YODA {
  namespace Utils {


    /// @brief Specialisation of std::vector to allow indexed access to ordered elements
    /// @todo Need to template on the value-comparison definition?
    template <typename T>
    class sortedvector : public std::vector<T> {
    public:

      /// @brief Insertion operator (push_back should not be used!)
      void insert(const T& val) {
        this->push_back(val);
      }
      
      void sort(){
        std::sort(this->begin(), this->end());
      }
      
    };


  }
}

#endif
