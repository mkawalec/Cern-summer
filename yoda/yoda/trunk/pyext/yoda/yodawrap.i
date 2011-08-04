%module yodawrap

%{
  #define SWIG_FILE_WITH_INIT
  #include "YODA/Histo1D.h"
  #include "YODA/Profile1D.h"

  #include "YODA/Histo2D.h"

  #include "YODA/Point2D.h"
  #include "YODA/Scatter2D.h"

  #include "YODA/Point3D.h"
  #include "YODA/Scatter3D.h"

  #include "YODA/WriterYODA.h"
  #include "YODA/WriterAIDA.h"
  using namespace YODA;
%}


// STL class support
%include "std_string.i"
%include "std_vector.i"
%include "std_list.i"
%include "std_set.i"
%include "std_map.i"
%template(DoubleList) std::vector<double>;
%template(DoublePair) std::pair<double, double>;
%template(IntDoubleDict) std::map<size_t, double>;

////////////////////////////////////////////////


// YODA base object
%include "YODA/AnalysisObject.h"
namespace YODA {
  %extend AnalysisObject {
    %template(setAnnotation) setAnnotation<std::string>;
    %template(addAnnotation) addAnnotation<std::string>;
  };
}


// Bins
%include "YODA/Bin.h"
%include "YODA/Bin1D.h"
%include "YODA/Bin2D.h"


// Histos
%feature("ignore") std::vector<YODA::HistoBin1D>::vector(size_type size);
%feature("ignore") std::vector<YODA::HistoBin1D>::resize(size_type size);
%feature("ignore") std::vector<YODA::HistoBin1D>::pop();
%include "YODA/HistoBin1D.h"
%include "YODA/Histo1D.h"
%template(HistoBin1Ds) std::vector<YODA::HistoBin1D>;

%include "YODA/HistoBin2D.h"
%include "YODA/Histo2D.h"
%template(HistoBin2Ds) std::vector<YODA::HistoBin2D>;


// Profile histos
%feature("ignore") std::vector<YODA::ProfileBin1D>::vector(size_type size);
%feature("ignore") std::vector<YODA::ProfileBin1D>::resize(size_type size);
%feature("ignore") std::vector<YODA::ProfileBin1D>::pop();
%include "YODA/ProfileBin1D.h"
%include "YODA/Profile1D.h"
%template(ProfileBin1Ds) std::vector<YODA::ProfileBin1D>;


// // Scatter plot errors
// %ignore YODA::ErrorCombiner;
// %include "YODA/Error.h"
// %template(PointError1D) YODA::PointError<1>;
// %template(PointError2D) YODA::PointError<2>;
// %template(PointError3D) YODA::PointError<3>;
// //%template(ErrorSet1D) YODA::ErrorSet<1>; // ?
// //%template(ErrorSet2D) YODA::ErrorSet<2>; // ?
// //%template(ErrorSet3D) YODA::ErrorSet<3>; // ?


// // Scatter plot points
// %ignore YODA::Point::error(size_t dim, ErrorCombiner& ec);
// %ignore YODA::Point::symmError(size_t dim, ErrorCombiner& ec);
// %ignore YODA::Point::errors(size_t dim, ErrorCombiner& ec);
// %ignore YODA::Point::symmErrors(size_t dim, ErrorCombiner& ec);
// %include "YODA/Point.h"


// // Scatter plots
// %include "YODA/Scatter.h"
// %template(Point1D) YODA::Point<1>;
// %template(Point2D) YODA::Point<2>;
// %template(Point3D) YODA::Point<3>;
// %template(Scatter1D) YODA::Scatter<1>;
// %template(Scatter2D) YODA::Scatter<2>;
// %template(Scatter3D) YODA::Scatter<3>;


// Scatter plots
%ignore operator ==(const YODA::Point2D&, const YODA::Point2D&);
%ignore operator !=(const YODA::Point2D&, const YODA::Point2D&);
%ignore operator <(const YODA::Point2D&, const YODA::Point2D&);
%ignore operator <=(const YODA::Point2D&, const YODA::Point2D&);
%ignore operator >(const YODA::Point2D&, const YODA::Point2D&);
%ignore operator >=(const YODA::Point2D&, const YODA::Point2D&);
%include "YODA/Point2D.h"
%include "YODA/Scatter2D.h"

%ignore operator ==(const YODA::Point3D&, const YODA::Point3D&);
%ignore operator !=(const YODA::Point3D&, const YODA::Point3D&);
%ignore operator <(const YODA::Point3D&, const YODA::Point3D&);
%ignore operator <=(const YODA::Point3D&, const YODA::Point3D&);
%ignore operator >(const YODA::Point3D&, const YODA::Point3D&);
%ignore operator >=(const YODA::Point3D&, const YODA::Point3D&);
%include "YODA/Point3D.h"
%include "YODA/Scatter3D.h"


// I/O
%template(AOVector) std::vector<AnalysisObject*>;
%template(AOList) std::list<AnalysisObject*>;
%template(AOSet) std::set<AnalysisObject*>;
%include "YODA/Writer.h"
%include "YODA/WriterAIDA.h"
%include "YODA/WriterYODA.h"
// %inline %{
//   namespace YODA {
//     Writer* get_writer(const std::string& name) {
//       if (name == "AIDA") return &WriterAIDA::create();
//       if (name == "YODA") return &WriterYODA::create();
//       return 0;
//     }
//   }
// %}
