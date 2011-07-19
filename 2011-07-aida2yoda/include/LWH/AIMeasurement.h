// -*- C++ -*-
#ifndef LWH_AIMeasurement_H
#define LWH_AIMeasurement_H

#ifndef LWH_USING_AIDA

/** @cond DONT_DOCUMENT_STRIPPED_DOWN_AIDA_INTERFACES */

namespace AIDA {

class IMeasurement {

public:
    virtual ~IMeasurement() {}
    virtual double value() const = 0;
    virtual double errorPlus() const = 0;
    virtual double errorMinus() const = 0;
    virtual bool setValue(double value) = 0;
    virtual bool setErrorPlus(double errorPlus) = 0;
    virtual bool setErrorMinus(double errorMinus) = 0;
};

}

/** @endcond */

#else
#include "AIDA/IMeasurement.h"
#endif

#endif /* LWH_AIMeasurement_H */
