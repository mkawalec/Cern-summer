// -*- C++ -*-
#include "Rivet/Rivet.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/AnalysisHandler.hh"
#include "Rivet/AnalysisInfo.hh"
#include "Rivet/Analysis.hh"
#include "Rivet/Tools/Logging.hh"

namespace Rivet {
  namespace {
    string makeAxisCode(const size_t datasetId, const size_t xAxisId, const size_t yAxisId) {
      stringstream axisCode;
      axisCode << "d";
      if (datasetId < 10) axisCode << 0;
      axisCode << datasetId;
      axisCode << "-x";
      if (xAxisId < 10) axisCode << 0;
      axisCode << xAxisId;
      axisCode << "-y";
      if (yAxisId < 10) axisCode << 0;
      axisCode << yAxisId;
      return axisCode.str();
    }
  }


  ////////////////////////


  Analysis::Analysis(const string& name)
    : _crossSection(-1.0),
      _gotCrossSection(false),
      _analysishandler(NULL)
  {
    ProjectionApplier::_allowProjReg = false;
    _defaultname = name;

    AnalysisInfo* ai = AnalysisInfo::make(name);
    assert(ai != 0);
    _info.reset(ai);
    assert(_info.get() != 0);
  }

  double Analysis::sqrtS() const {
    return handler().sqrtS();
  }

  const ParticlePair& Analysis::beams() const {
    return handler().beams();
  }

  const PdgIdPair Analysis::beamIds() const {
    return handler().beamIds();
  }


  const string Analysis::histoDir() const {
    /// @todo This doesn't change: calc and cache at first use!
    string path = "/" + name();
    if (handler().runName().length() > 0) {
      path = "/" + handler().runName() + path;
    }
    while (find_first(path, "//")) {
      replace_all(path, "//", "/");
    }
    return path;
  }


  const string Analysis::histoPath(const string& hname) const {
    const string path = histoDir() + "/" + hname;
    return path;
  }


  Log& Analysis::getLog() const {
    string logname = "Rivet.Analysis." + name();
    return Log::getLog(logname);
  }


  size_t Analysis::numEvents() const {
    return handler().numEvents();
  }


  double Analysis::sumOfWeights() const {
    return handler().sumOfWeights();
  }


  ///////////////////////////////////////////


  bool Analysis::isCompatible(const ParticlePair& beams) const {
    return isCompatible(beams.first.pdgId(),  beams.second.pdgId(),
                        beams.first.energy(), beams.second.energy());
  }


  bool Analysis::isCompatible(PdgId beam1, PdgId beam2, double e1, double e2) const {
    PdgIdPair beams(beam1, beam2);
    pair<double,double> energies(e1, e2);
    return isCompatible(beams, energies);
  }


  bool Analysis::isCompatible(const PdgIdPair& beams, const pair<double,double>& energies) const {
    // First check the beam IDs
    bool beamIdsOk = false;
    foreach (const PdgIdPair& bp, requiredBeams()) {
      if (compatible(beams, bp)) {
        beamIdsOk =  true;
        break;
      }
    }
    if (!beamIdsOk) return false;

    // Next check that the energies are compatible (within 1%, to give a bit of UI forgiveness)
    bool beamEnergiesOk = requiredEnergies().size()>0 ? false : true;
    typedef pair<double,double> DoublePair;
    foreach (const DoublePair& ep, requiredEnergies()) {
      if ((fuzzyEquals(ep.first, energies.first, 0.01) && fuzzyEquals(ep.second, energies.second, 0.01)) ||
          (fuzzyEquals(ep.first, energies.second, 0.01) && fuzzyEquals(ep.second, energies.first, 0.01))) {
        beamEnergiesOk =  true;
        break;
      }
    }
    return beamEnergiesOk;

    /// @todo Need to also check internal consistency of the analysis'
    /// beam requirements with those of the projections it uses.
  }


  ///////////////////////////////////////////


  Analysis& Analysis::setCrossSection(double xs) {
    _crossSection = xs;
    _gotCrossSection = true;
    return *this;
  }

  double Analysis::crossSection() const {
    if (!_gotCrossSection || std::isnan(_crossSection)) {
      string errMsg = "You did not set the cross section for the analysis " + name();
      throw Error(errMsg);
    }
    return _crossSection;
  }

  double Analysis::crossSectionPerEvent() const {
    const double sumW = sumOfWeights();
    assert(sumW > 0);
    return _crossSection / sumW;
  }



  ////////////////////////////////////////////////////////////
  // Histogramming


  void Analysis::_cacheBinEdges() const {
    _cacheXAxisData();
    if (_histBinEdges.empty()) {
      MSG_TRACE("Getting histo bin edges from AIDA for paper " << name());
      _histBinEdges = getBinEdges(_dpsData);
    }
  }


  void Analysis::_cacheXAxisData() const {
    if (_dpsData.empty()) {
      MSG_TRACE("Getting DPS x-axis data from AIDA for paper " << name());
      _dpsData = getDPSXValsErrs(name());
    }
  }


  const BinEdges& Analysis::binEdges(const string& hname) const {
    _cacheBinEdges();
    MSG_TRACE("Using histo bin edges for " << name() << ":" << hname);
    const BinEdges& edges = _histBinEdges.find(hname)->second;
    if (getLog().isActive(Log::TRACE)) {
      stringstream edges_ss;
      foreach (const double be, edges) {
        edges_ss << " " << be;
      }
      MSG_TRACE("Edges:" << edges_ss.str());
    }
    return edges;
  }


  const BinEdges& Analysis::binEdges(size_t datasetId, size_t xAxisId, size_t yAxisId) const {
    const string hname = makeAxisCode(datasetId, xAxisId, yAxisId);
    return binEdges(hname);
  }


  BinEdges Analysis::logBinEdges(size_t nbins, double lower, double upper) {
    assert(lower>0.0);
    assert(upper>lower);
    double loglower=log10(lower);
    double logupper=log10(upper);
    vector<double> binedges;
    double stepwidth=(logupper-loglower)/double(nbins);
    for (size_t i=0; i<=nbins; ++i) {
      binedges.push_back(pow(10.0, loglower+double(i)*stepwidth));
    }
    return binedges;
  }

  Histo1DPtr Analysis::bookHisto1D(size_t datasetId, size_t xAxisId,
                                          size_t yAxisId, const string& title,
                                          const string& xtitle, const string& ytitle)
  {
    const string axisCode = makeAxisCode(datasetId, xAxisId, yAxisId);
    return bookHisto1D(axisCode, title, xtitle, ytitle);
  }


  Histo1DPtr Analysis::bookHisto1D(const string& hname, const string& title,
				   const string& xtitle, const string& ytitle)
  {
    // Get the bin edges (only read the AIDA file once)
    const BinEdges edges = binEdges(hname);
    const string path = histoPath(hname);
    Histo1DPtr hist( new Histo1D(edges,path,title) );
    addPlot(hist);
    MSG_TRACE("Made histogram " << hname <<  " for " << name());
    // hist->setXTitle(xtitle);
    // hist->setYTitle(ytitle);
    return hist;
  }


  Histo1DPtr Analysis::bookHisto1D(const string& hname,
				   size_t nbins, double lower, double upper,
				   const string& title,
				   const string& xtitle, const string& ytitle) {
    const string path = histoPath(hname);
    Histo1DPtr hist( new Histo1D(nbins, lower, upper, path, title) );
    addPlot(hist);
    MSG_TRACE("Made histogram " << hname <<  " for " << name());
    // hist->setXTitle(xtitle);
    // hist->setYTitle(ytitle);
    return hist;
  }


  Histo1DPtr Analysis::bookHisto1D(const string& hname,
				   const vector<double>& binedges,
				   const string& title,
				   const string& xtitle, 
				   const string& ytitle) {
    const string path = histoPath(hname);
    Histo1DPtr hist( new Histo1D(binedges, path, title) );
    addPlot(hist);
    MSG_TRACE("Made histogram " << hname <<  " for " << name());
    // hist->setXTitle(xtitle);
    // hist->setYTitle(ytitle);
    return hist;
  }

  // IHistogram2D*
  // Analysis::bookHistogram2D(const string& hname,
  // 			    size_t nxbins, double xlower, double xupper,
  // 			    size_t nybins, double ylower, double yupper,
  // 			    const string& title, const string& xtitle,
  // 			    const string& ytitle, const string& ztitle) {
  //   _makeHistoDir();
  //   const string path = histoPath(hname);
  //   IHistogram2D* hist =
  //     histogramFactory().createHistogram2D(path, title, nxbins, xlower, xupper,
  // 					   nybins, ylower, yupper);
  //   MSG_TRACE("Made 2D histogram " << hname <<  " for " << name());
  //   hist->setXTitle(xtitle);
  //   hist->setYTitle(ytitle);
  //   hist->setZTitle(ztitle);
  //   return hist;
  // }


  // IHistogram2D*
  // Analysis::bookHistogram2D(const string& hname,
  // 			    const vector<double>& xbinedges,
  // 			    const vector<double>& ybinedges,
  // 			    const string& title, const string& xtitle,
  // 			    const string& ytitle, const string& ztitle) {
  //   _makeHistoDir();
  //   const string path = histoPath(hname);
  //   IHistogram2D* hist =
  //     histogramFactory().createHistogram2D(path, title, xbinedges, ybinedges);
  //   MSG_TRACE("Made 2D histogram " << hname <<  " for " << name());
  //   hist->setXTitle(xtitle);
  //   hist->setYTitle(ytitle);
  //   hist->setZTitle(ztitle);
  //   return hist;
  // }


  /////////////////


  Profile1DPtr Analysis::bookProfile1D(size_t datasetId, size_t xAxisId,
				       size_t yAxisId, const string& title,
				       const string& xtitle, const string& ytitle) {
    const string axisCode = makeAxisCode(datasetId, xAxisId, yAxisId);
    return bookProfile1D(axisCode, title, xtitle, ytitle);
  }


  Profile1DPtr Analysis::bookProfile1D(const string& hname, const string& title,
				       const string& xtitle, const string& ytitle)
  {
    // Get the bin edges (only read the AIDA file once)
    const BinEdges edges = binEdges(hname);
    const string path = histoPath(hname);
    Profile1DPtr prof( new Profile1D(edges, path, title) );
    addPlot(prof);
    MSG_TRACE("Made profile histogram " << hname <<  " for " << name());
    // prof->setXTitle(xtitle);
    // prof->setYTitle(ytitle);
    return prof;
  }


  Profile1DPtr Analysis::bookProfile1D(const string& hname,
				       size_t nbins, double lower, double upper,
				       const string& title,
				       const string& xtitle, const string& ytitle) {
    const string path = histoPath(hname);
    Profile1DPtr prof( new Profile1D(nbins, lower, upper, path, title) );
    addPlot(prof);
    MSG_TRACE("Made profile histogram " << hname <<  " for " << name());
    // prof->setXTitle(xtitle);
    // prof->setYTitle(ytitle);
    return prof;
  }


  Profile1DPtr Analysis::bookProfile1D(const string& hname,
				       const vector<double>& binedges,
				       const string& title,
				       const string& xtitle, const string& ytitle) {
    const string path = histoPath(hname);
    Profile1DPtr prof( new Profile1D(binedges, path, title) );
    addPlot(prof);
    MSG_TRACE("Made profile histogram " << hname <<  " for " << name());
    // prof->setXTitle(xtitle);
    // prof->setYTitle(ytitle);
    return prof;
  }


  ///////////////////



  Scatter2DPtr Analysis::bookScatter2D(const string& hname, const string& title,
				       const string& xtitle, const string& ytitle) {
    const string path = histoPath(hname);
    Scatter2DPtr dps( new Scatter2D(path, title) );
    addPlot(dps);
    MSG_TRACE("Made data point set " << hname <<  " for " << name());
    // dps->setXTitle(xtitle);
    // dps->setYTitle(ytitle);
    return dps;
  }


  Scatter2DPtr Analysis::bookScatter2D(const string& hname,
				       size_t npts, double lower, double upper,
				       const string& title,
				       const string& xtitle, const string& ytitle) {
    Scatter2DPtr dps = bookScatter2D(hname, title, xtitle, ytitle);
    const double binwidth = (upper-lower)/npts;
    for (size_t pt = 0; pt < npts; ++pt) {
      const double bincentre = lower + (pt + 0.5) * binwidth;
      // \todo YODA check
      dps->addPoint(bincentre, 0, binwidth/2.0, 0);
      // IMeasurement* meas = dps->point(pt)->coordinate(0);
      // meas->setValue(bincentre);
      // meas->setErrorPlus(binwidth/2.0);
      // meas->setErrorMinus(binwidth/2.0);
    }
    return dps;
  }


  Scatter2DPtr Analysis::bookScatter2D(size_t datasetId, size_t xAxisId,
				       size_t yAxisId, const string& title,
				       const string& xtitle, const string& ytitle) {
    // Get the bin edges (only read the AIDA file once)
    _cacheXAxisData();
    // Build the axis code
    const string axisCode = makeAxisCode(datasetId, xAxisId, yAxisId);
    //const map<string, vector<DPSXPoint> > xpoints = getDPSXValsErrs(papername);
    MSG_TRACE("Using DPS x-positions for " << name() << ":" << axisCode);
    Scatter2DPtr dps = bookScatter2D(axisCode, title, xtitle, ytitle);
    const vector<DPSXPoint> xpts = _dpsData.find(axisCode)->second;
    for (size_t pt = 0; pt < xpts.size(); ++pt) {
      // \todo YODA check
      dps->addPoint(xpts[pt].val, xpts[pt].errminus, xpts[pt].errplus, 0, 0, 0);
      // IMeasurement* meas = dps->point(pt)->coordinate(0);
      // meas->setValue(xpts[pt].val);
      // meas->setErrorPlus(xpts[pt].errplus);
      // meas->setErrorMinus(xpts[pt].errminus);
    }
    MSG_TRACE("Made DPS " << axisCode <<  " for " << name());
    return dps;
  }


  void Analysis::normalize(Histo1DPtr histo, double norm) {
    if (!histo) {
      MSG_ERROR("Failed to normalize histo=NULL in analysis "
                << name() << " (norm=" << norm << ")");
      return;
    }
    const string hpath = histo->path();
    MSG_TRACE("Normalizing histo " << hpath << " to " << norm);

    double oldintg = 0.0;
    int nBins = histo->numBins();
    for (int iBin = 0; iBin != nBins; ++iBin) {
      oldintg += histo->bin(iBin).area();
    }
    if (oldintg == 0.0) {
      MSG_WARNING("Histo " << hpath << " has null integral during normalization");
      return;
    }

    // Scale by the normalisation factor.
    scale(histo, norm/oldintg);
  }


  void Analysis::scale(Histo1DPtr histo, double scale) {
    if (!histo) {
      MSG_ERROR("Failed to scale histo=NULL in analysis "
                << name() << " (scale=" << scale << ")");
      return;
    }
    const string hpath = histo->path();
    MSG_TRACE("Scaling histo " << hpath);

    vector<double> x, y, ex, ey;
    for (size_t i = 0, N = histo->numBins(); i < N; ++i) {
      x.push_back( histo->bin(i).midpoint() );
      ex.push_back(histo->bin(i).width()*0.5);

      // We'd like to do this: y.push_back(histo->binHeight(i) * scale);
      y.push_back(histo->bin(i).height()*scale);

      // We'd like to do this: ey.push_back(histo->binError(i) * scale);
      ey.push_back(histo->bin(i).heightError()*scale);
    }

    string title = histo->title();
    // string xtitle = histo->xtitle();
    // string ytitle = histo->ytitle();


    // \todo YODA

    // tree().mkdir("/tmpnormalize");
    // tree().mv(hpath, "/tmpnormalize");

    Scatter2DPtr dps( new Scatter2D(x, y, ex, ey, hpath, title) );
    addPlot(dps);

    // dps->setXTitle(xtitle);
    // dps->setYTitle(ytitle);

    // tree().rm(tree().findPath(dynamic_cast<AIDA::IManagedObject&>(*histo)));
    // tree().rmdir("/tmpnormalize");

    // // Set histo pointer to null - it can no longer be used.
    // histo = 0;
  }


  // void Analysis::normalize(AIDA::IHistogram2D*& histo, double norm) {
  //   if (!histo) {
  //     MSG_ERROR("Failed to normalize histo=NULL in analysis "
  //               << name() << " (norm=" << norm << ")");
  //     return;
  //   }
  //   const string hpath = tree().findPath(dynamic_cast<const AIDA::IManagedObject&>(*histo));
  //   MSG_TRACE("Normalizing histo " << hpath << " to " << norm);

  //   double oldintg = 0.0;
  //   int nxBins = histo->xAxis().bins();
  //   int nyBins = histo->yAxis().bins();
  //   for (int ixBin = 0; ixBin != nxBins; ++ixBin)
  //     for (int iyBin = 0; iyBin != nyBins; ++iyBin) {
  //     // Leaving out factor of binWidth because AIDA's "height"
  //     // already includes a width factor.
  // 	oldintg += histo->binHeight(ixBin, iyBin); // * histo->axis().binWidth(iBin);
  //   }
  //   if (oldintg == 0.0) {
  //     MSG_WARNING("Histo " << hpath << " has null integral during normalization");
  //     return;
  //   }

  //   // Scale by the normalisation factor.
  //   scale(histo, norm/oldintg);
  // }


  // void Analysis::scale(AIDA::IHistogram2D*& histo, double scale) {
  //   if (!histo) {
  //     MSG_ERROR("Failed to scale histo=NULL in analysis "
  //               << name() << " (scale=" << scale << ")");
  //     return;
  //   }
  //   const string hpath =
  //     tree().findPath(dynamic_cast<const AIDA::IManagedObject&>(*histo));
  //   MSG_TRACE("Scaling histo " << hpath);

  //   vector<double> x, y, z, ex, ey, ez;
  //   for (size_t ix = 0, Nx = histo->xAxis().bins(); ix < Nx; ++ix)
  //     for (size_t iy = 0, Ny = histo->yAxis().bins(); iy < Ny; ++iy) {
  // 	x.push_back(0.5 * (histo->xAxis().binLowerEdge(ix) +
  // 			   histo->xAxis().binUpperEdge(ix)));
  // 	ex.push_back(histo->xAxis().binWidth(ix)*0.5);
  // 	y.push_back(0.5 * (histo->yAxis().binLowerEdge(iy) +
  // 			   histo->yAxis().binUpperEdge(iy)));
  // 	ey.push_back(histo->yAxis().binWidth(iy)*0.5);

  // 	// "Bin height" is a misnomer in the AIDA spec: width is neglected.
  // 	// We'd like to do this: y.push_back(histo->binHeight(i) * scale);
  // 	z.push_back(histo->binHeight(ix, iy)*scale/
  // 		    (histo->xAxis().binWidth(ix)*histo->yAxis().binWidth(iy)));
  // 	// "Bin error" is a misnomer in the AIDA spec: width is neglected.
  // 	// We'd like to do this: ey.push_back(histo->binError(i) * scale);
  // 	ez.push_back(histo->binError(ix, iy)*scale/
  // 		     (histo->xAxis().binWidth(ix)*histo->yAxis().binWidth(iy)));
  //   }

  //   string title = histo->title();
  //   string xtitle = histo->xtitle();
  //   string ytitle = histo->ytitle();
  //   string ztitle = histo->ztitle();

  //   tree().mkdir("/tmpnormalize");
  //   tree().mv(hpath, "/tmpnormalize");

  //   Scatter2DPtr dps =
  //     datapointsetFactory().createXYZ(hpath, title, x, y, z, ex, ey, ez);
  //   dps->setXTitle(xtitle);
  //   dps->setYTitle(ytitle);
  //   dps->setZTitle(ztitle);

  //   tree().rm(tree().findPath(dynamic_cast<AIDA::IManagedObject&>(*histo)));
  //   tree().rmdir("/tmpnormalize");

  //   // Set histo pointer to null - it can no longer be used.
  //   histo = 0;
  // }

  void Analysis::addPlot(AnalysisObjectPtr ao) {
    _plotobjects.push_back(ao);
  }

}
