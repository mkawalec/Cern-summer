## Flags for building all plugins
AM_LDFLAGS = $(LDFLAGS) -module -avoid-version -L$(FASTJETLIBPATH)
LIBS = $(FASTJETCONFIGLIBADD)
lib_LTLIBRARIES =

noinst_LTLIBRARIES = libRivetAnalysisTools.la
libRivetAnalysisTools_la_SOURCES = \
    MC_JetAnalysis.cc

## ANALYSIS CATEGORIES
##
## Unvalidated analyses: add new standard analyses here, and only
## move them into the collider-specific standard plugin libraries
## once they have been finished and checked. The --enable-unvalidated
## flag is needed to install the unvalidated analyses.
##
## Preliminary analyses: validated analyses whose experimental paper has not
## been fully accepted for publication should go here. Analyses in this group
## are considered safe to use but the reference data may yet change. In
## progressing from preliminary status to a permanent published analyses
## collection, the analysis name is very likely to change, so you should ensure
## that any Rivet-using scripts are not broken by such name changes when
## upgrading between Rivet versions. These analyses will not be available if
## Rivet is built with the --disable-preliminary configure flag.
##
## Obsolete analyses: as mentioned above, when a preliminary analysis becomes
## permanent its name will change to reflect its newly published status via the
## publication's SPIRES ID. The previous form of the analysis, possibly with
## different reference histograms, will be retained for one major version of
## Rivet with a status of "obsolete" before being removed, to give users time to
## migrate their run scripts, i.e. if an analysis is marked as obsolete in
## version 1.4.2, it will remain in Rivet's distribution until version
## 1.5.0. Obsolete analyses will not be available if Rivet is built with the
## --disable-obsolete configure flag.


lib_LTLIBRARIES += RivetALICEAnalyses.la
RivetALICEAnalyses_la_SOURCES = \
    ALICE_2010_S8706239.cc \
    ALICE_2010_S8625980.cc \
    ALICE_2010_S8624100.cc


lib_LTLIBRARIES += RivetATLASAnalyses.la
RivetATLASAnalyses_la_SOURCES = \
    ATLAS_2010_S8591806.cc \
    ATLAS_2010_S8817804.cc \
    ATLAS_2010_S8894728.cc \
    ATLAS_2010_S8914702.cc \
    ATLAS_2010_S8918562.cc \
    ATLAS_2010_S8919674.cc \
    ATLAS_2011_S8924791.cc \
    ATLAS_2011_S8971293.cc \
    ATLAS_2010_S8994773.cc \
    ATLAS_2011_S8983313.cc \
    ATLAS_2011_S9002537.cc
if ENABLE_UNVALIDATED
RivetATLASAnalyses_la_SOURCES += \
    ATLAS_2010_CONF_2010_049.cc \
    ATLAS_2011_S9019561.cc \
    ATLAS_2011_CONF_2011_090.cc
endif


lib_LTLIBRARIES += RivetCMSAnalyses.la
RivetCMSAnalyses_la_SOURCES = \
    CMS_2011_S8957746.cc


lib_LTLIBRARIES += RivetLHCbAnalyses.la
RivetLHCbAnalyses_la_SOURCES =
if ENABLE_UNVALIDATED
RivetLHCbAnalyses_la_SOURCES += \
    LHCB_2010_S8758301.cc
endif


lib_LTLIBRARIES += RivetCDFAnalyses.la
RivetCDFAnalyses_la_SOURCES = \
    CDF_1988_S1865951.cc \
    CDF_1990_S2089246.cc \
    CDF_1994_S2952106.cc \
    CDF_1996_S3418421.cc \
    CDF_1998_S3618439.cc \
    CDF_2000_S4155203.cc \
    CDF_2000_S4266730.cc \
    CDF_2001_S4517016.cc \
    CDF_2001_S4563131.cc \
    CDF_2001_S4751469.cc \
    CDF_2002_S4796047.cc \
    CDF_2004_S5839831.cc \
    CDF_2005_S6080774.cc \
    CDF_2005_S6217184.cc \
    CDF_2006_S6450792.cc \
    CDF_2006_S6653332.cc \
    CDF_2007_S7057202.cc \
    CDF_2008_S7540469.cc \
    CDF_2008_S7828950.cc \
    CDF_2008_S8093652.cc \
    CDF_2008_S8095620.cc \
    CDF_2009_S8233977.cc \
    CDF_2009_S8383952.cc \
    CDF_2009_S8436959.cc \
    CDF_2010_S8591881_DY.cc \
    CDF_2010_S8591881_QCD.cc
if ENABLE_PRELIMINARY
RivetCDFAnalyses_la_SOURCES += \
    CDF_2009_NOTE_9936.cc
endif
if ENABLE_OBSOLETE
RivetCDFAnalyses_la_SOURCES += \
    CDF_2008_LEADINGJETS.cc \
    CDF_2008_NOTE_9351.cc
endif
if ENABLE_UNVALIDATED
RivetCDFAnalyses_la_SOURCES += \
    CDF_1993_S2742446.cc \
    CDF_1996_S3108457.cc \
    CDF_1996_S3349578.cc \
    CDF_1997_S3541940.cc \
    CDF_2008_S7541902.cc \
    CDF_2008_S7782535.cc
endif


lib_LTLIBRARIES += RivetD0Analyses.la
RivetD0Analyses_la_SOURCES = \
    D0_2000_S4480767.cc \
    D0_2001_S4674421.cc \
    D0_2004_S5992206.cc \
    D0_2006_S6438750.cc \
    D0_2007_S7075677.cc \
    D0_2008_S6879055.cc \
    D0_2008_S7554427.cc \
    D0_2008_S7662670.cc \
    D0_2008_S7719523.cc \
    D0_2008_S7837160.cc \
    D0_2008_S7863608.cc \
    D0_2009_S8202443.cc \
    D0_2009_S8320160.cc \
    D0_2009_S8349509.cc \
    D0_2010_S8566488.cc \
    D0_2010_S8570965.cc \
    D0_2010_S8671338.cc \
    D0_2010_S8821313.cc
if ENABLE_UNVALIDATED
RivetD0Analyses_la_SOURCES += \
    D0_1996_S3214044.cc \
    D0_1996_S3324664.cc
endif


lib_LTLIBRARIES += RivetHERAAnalyses.la
RivetHERAAnalyses_la_SOURCES = \
    H1_1994_S2919893.cc \
    H1_2000_S4129130.cc
if ENABLE_UNVALIDATED
RivetHERAAnalyses_la_SOURCES += \
    H1_1995_S3167097.cc \
    ZEUS_2001_S4815815.cc
endif

lib_LTLIBRARIES += RivetPetraAnalyses.la
RivetPetraAnalyses_la_SOURCES = \
    JADE_1998_S3612880.cc \
    TASSO_1990_S2148048.cc

lib_LTLIBRARIES += RivetLEPAnalyses.la
RivetLEPAnalyses_la_SOURCES = \
    ALEPH_1991_S2435284.cc \
    ALEPH_1996_S3486095.cc \
    ALEPH_1996_S3196992.cc \
    ALEPH_2004_S5765862.cc \
    DELPHI_1995_S3137023.cc \
    DELPHI_1996_S3430090.cc \
    OPAL_1998_S3780481.cc \
    OPAL_2001_S4553896.cc \
    OPAL_2004_S6132243.cc
if ENABLE_PRELIMINARY
RivetLEPAnalyses_la_SOURCES += \
    DELPHI_2002_069_CONF_603.cc
endif
if ENABLE_UNVALIDATED
RivetLEPAnalyses_la_SOURCES += \
    DELPHI_2003_WUD_03_11.cc \
    OPAL_1993_S2692198.cc
endif


lib_LTLIBRARIES += RivetRHICAnalyses.la
RivetRHICAnalyses_la_SOURCES = \
    STAR_2006_S6500200.cc \
    STAR_2006_S6860818.cc \
    STAR_2006_S6870392.cc
if ENABLE_PRELIMINARY
RivetRHICAnalyses_la_SOURCES += \
    STAR_2009_UE_HELEN.cc
endif
if ENABLE_UNVALIDATED
RivetRHICAnalyses_la_SOURCES += \
    STAR_2008_S7869363.cc \
    STAR_2008_S7993412.cc
endif


lib_LTLIBRARIES += RivetSPSAnalyses.la
RivetSPSAnalyses_la_SOURCES = \
    UA1_1990_S2044935.cc \
    UA5_1982_S875503.cc \
    UA5_1986_S1583476.cc \
    UA5_1987_S1640666.cc \
    UA5_1988_S1867512.cc \
    UA5_1989_S1926373.cc


lib_LTLIBRARIES += RivetMiscAnalyses.la
RivetMiscAnalyses_la_SOURCES = \
    PDG_Hadron_Multiplicities.cc \
    PDG_Hadron_Multiplicities_Ratios.cc \
    JADE_OPAL_2000_S4300807.cc \
    BELLE_2006_S6265367.cc
if ENABLE_UNVALIDATED
RivetMiscAnalyses_la_SOURCES += \
    E735_1998_S3905616.cc \
    SFM_1984_S1178091.cc
endif


lib_LTLIBRARIES += RivetMCAnalyses.la
RivetMCAnalyses_la_SOURCES = \
    ExampleAnalysis.cc \
    MC_GENERIC.cc \
    MC_JETS.cc \
    MC_PHOTONJETS.cc \
    MC_HJETS.cc \
    MC_WJETS.cc \
    MC_WPOL.cc \
    MC_WWJETS.cc \
    MC_ZJETS.cc \
    MC_ZZJETS.cc \
    MC_LEADINGJETS.cc \
    MC_DIPHOTON.cc \
    MC_SUSY.cc
if ENABLE_UNVALIDATED
RivetMCAnalyses_la_SOURCES += \
    MC_DIJET.cc \
    MC_PHOTONJETUE.cc \
    MC_TTBAR.cc \
    MC_XS.cc
endif
