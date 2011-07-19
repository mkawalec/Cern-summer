// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_NVECTOR_H
#define YODA_NVECTOR_H

#include <vector>
#include <utility>

namespace YODA {
  namespace Utils {

    /// Utility fixed size vector
    template <typename T, size_t N>
    class nvector {
    public:

      /// @name Constructors
      //@{
      nvector() {
        for (size_t i = 0; i < N; ++i) {
          _vals[i] = 0;
        }
      }

      nvector(const nvector<T,N>& other) {
        for (size_t i = 0; i < N; ++i) {
          _vals[i] = other[i];
        }
      }

      nvector(const std::vector<T>& stdvec) {
        assert(stdvec.size() == N);
        for (size_t i = 0; i < N; ++i) {
          _vals[i] = stdvec[i];
        }
      }
      //@}


      /// @name Iterators
      //@{
      typedef T* iterator;
      typedef const T* const_iterator;

      const_iterator begin() const {
        return &_vals[0];
      }

      iterator begin() {
        return &_vals[0];
      }

      const_iterator end() const {
        return begin()+N;
      }

      iterator end() {
        return begin()+N;
      }
      //@}


      /// @name Accessors
      //@{
      size_t size() const {
        return N;
      }

      const T& at(size_t n) const {
        return _vals[n];
      }

      T& operator[](size_t n) {
        return _vals[n];
      }

      const T& operator[](size_t n) const {
        return _vals[n];
      }
      //@}


    private:
      T _vals[N];

    };


  }
}

#endif
