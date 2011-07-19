#ifndef RIVET_EXCEPTIONS_HH
#define RIVET_EXCEPTIONS_HH

#include <string>
#include <exception>
#include <stdexcept>

namespace Rivet {


  /// @brief Generic runtime Rivet error.
  class Error : public std::runtime_error {
  public:
    Error(const std::string& what) : std::runtime_error(what) {}
  };


  /// @brief Rivet::Exception is a synonym for Rivet::Error.
  typedef Error Exception;


  /// @brief Error for e.g. use of invalid bin ranges.
  class RangeError : public Error {
  public:
    RangeError(const std::string& what) : Error(what) {}
  };


  /// @brief Error specialisation for places where alg logic has failed.
  class LogicError : public Error {
  public:
    LogicError(const std::string& what) : Error(what) {}
  };


  /// @brief Error specialisation for failures relating to particle ID codes.
  class PidError : public Error {
  public:
    PidError(const std::string& what) : Error(what) {}
  };


  /// @brief Errors relating to event/bin weights
  /// Arises in computing statistical quantities because e.g. the bin
  /// weight is zero or negative.
  class WeightError : public Error {
  public:
    WeightError(const std::string& what) : Error(what) {}
  };


}

#endif
