// -*- C++ -*-
#ifndef LWH_AIBaseHistogram_H
#define LWH_AIBaseHistogram_H
//

#ifndef LWH_USING_AIDA

/** @cond DONT_DOCUMENT_STRIPPED_DOWN_AIDA_INTERFACES */

namespace AIDA {

  class IBaseHistogram {
    
  public:
    
    virtual ~IBaseHistogram() {}

    virtual int dimension() const = 0;
    virtual bool reset() = 0;
    virtual int entries() const = 0;
    

    ///////////////////////////////////


    /**
     * Get the main title.
     * @return The title.
     *
     */
    std::string title() const {
      return theTitle;
    }

    /**
     * Set the main title.
     * @param title The new title.
     * @return false If the title cannot be set.
     *
     */
    bool setTitle(const std::string & title) {
      theTitle = title;
      return true;
    }



    /**
     * Get the x-axis title.
     * @return The title.
     *
     */
    std::string xtitle() const {
      return theXTitle;
    }

    /**
     * Set the x-axis title.
     * @param title The new title.
     * @return false If the title cannot be set.
     *
     */
    bool setXTitle(const std::string & xtitle) {
      theXTitle = xtitle;
      return true;
    }



    /**
     * Get the y-axis title.
     * @return The title.
     *
     */
    std::string ytitle() const {
      return theYTitle;
    }

    /**
     * Set the y-axis title.
     * @param title The new title.
     * @return false If the title cannot be set.
     *
     */
    bool setYTitle(const std::string & ytitle) {
      theYTitle = ytitle;
      return true;
    }

    /**
     * Get the z-axis title.
     * @return The title.
     *
     */
    std::string ztitle() const {
      return theZTitle;
    }

    /**
     * Set the z-axis title.
     * @param title The new title.
     * @return false If the title cannot be set.
     *
     */
    bool setZTitle(const std::string & ztitle) {
      theZTitle = ztitle;
      return true;
    }


  protected:
    std::string theTitle;
    std::string theXTitle;
    std::string theYTitle;
    std::string theZTitle;

  };
  

} // namespace AIDA

/** @endcond */
  
#else
#include "AIDA/IBaseHistogram.h"
#endif

#endif /* LWH_AIBaseHistogram_H */
