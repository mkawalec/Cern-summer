// ----------------------------------------------------------------------
//
// ParticleIDMethods.hh
// Author:  Lynn Garren, Andy Buckley
//
//  various utilities to extract information from the particle ID
//
//  In the standard numbering scheme, the PID digits (base 10) are:
//            +/- n nr nl nq1 nq2 nq3 nj
//  It is expected that any 7 digit number used as a PID will adhere to
//  the Monte Carlo numbering scheme documented by the PDG.
//  Note that many "new" particles not explicitly defined already
//  can be expressed within this numbering scheme.
//
//  These are the same methods that can be found in HepPDT::ParticleID
// ----------------------------------------------------------------------
#ifndef RIVET_PARTICLE_ID_METHODS_HH
#define RIVET_PARTICLE_ID_METHODS_HH

#include "Rivet/Particle.hh"


namespace Rivet {

  namespace PID {


    /// @name PID operations on Rivet::Particle wrapper
    //@{

    // /// if this is a nucleus (ion), get A
    // /// Ion numbers are +/- 10LZZZAAAI.
    // int A(const int & pid );

    // /// if this is a nucleus (ion), get Z
    // /// Ion numbers are +/- 10LZZZAAAI.
    // int Z(const int & pid );

    // /// if this is a nucleus (ion), get nLambda
    // /// Ion numbers are +/- 10LZZZAAAI.
    // int lambda( const int & pid );

    /// absolute value of particle ID
    int abspid( const int & pid );

    
    /// is this a valid ID?
    bool isValid( const int & pid );
    /// is this a valid meson ID?
    bool isMeson( const int & pid );
    /// is this a valid baryon ID?
    bool isBaryon( const int & pid );
    /// is this a valid diquark ID?
    bool isDiQuark( const int & pid );
    /// is this a valid hadron ID?
    bool isHadron( const int & pid );
    /// is this a valid lepton ID?
    bool isLepton( const int & pid );
    /// is this a valid ion ID?
    bool isNucleus( const int & pid );
    /// is this a valid pentaquark ID?
    bool isPentaquark( const int & pid );
    /// is this a valid SUSY ID?
    bool isSUSY( const int & pid );
    /// is this a valid R-hadron ID?
    bool isRhadron( const int & pid );

    /// does this particle contain an up quark?
    bool hasUp( const int & pid );
    /// does this particle contain a down quark?
    bool hasDown( const int & pid );
    /// does this particle contain a strange quark?
    bool hasStrange( const int & pid );
    /// does this particle contain a charm quark?
    bool hasCharm( const int & pid );
    /// does this particle contain a bottom quark?
    bool hasBottom( const int & pid );
    /// does this particle contain a top quark?
    bool hasTop( const int & pid );

    /// jSpin returns 2J+1, where J is the total spin
    int jSpin( const int & pid );
    /// sSpin returns 2S+1, where S is the spin
    int sSpin( const int & pid );
    /// lSpin returns 2L+1, where L is the orbital angular momentum
    int lSpin( const int & pid );

    /// return 3 times the charge (3 x quark charge is an int)
    int threeCharge( const int & pid );
    /// return the charge
    inline double charge( const int & pid ) { return threeCharge(pid)/3.0; }

    //@}


    /////////////////////////



    /// @name PID operations on Rivet::Particle wrapper
    //@{

    /// if this is a nucleus (ion), get A
    /// Ion numbers are +/- 10LZZZAAAI.
    // int A(const Particle& p) { return A(p.pdgId()); }

    /// if this is a nucleus (ion), get Z
    /// Ion numbers are +/- 10LZZZAAAI.
    // int Z(const Particle& p) { return Z(p.pdgId()); }

    /// if this is a nucleus (ion), get nLambda
    /// Ion numbers are +/- 10LZZZAAAI.
    // int lambda( const Particle& p) { return lambda(p.pdgId()); }

    /// absolute value of particle ID
    inline int abspid( const Particle& p) { return abspid(p.pdgId()); }

    /// is this a valid meson ID?
    inline bool isMeson( const Particle& p ) { return isMeson(p.pdgId()); }
    /// is this a valid baryon ID?
    inline bool isBaryon( const Particle& p ) { return isBaryon(p.pdgId()); }
    /// is this a valid diquark ID?
    inline bool isDiQuark( const Particle& p ) { return isDiQuark(p.pdgId()); }
    /// is this a valid hadron ID?
    inline bool isHadron( const Particle& p ) { return isHadron(p.pdgId()); }
    /// is this a valid lepton ID?
    inline bool isLepton( const Particle& p ) { return isLepton(p.pdgId()); }
    /// is this a valid ion ID?
    inline bool isNucleus( const Particle& p ) { return isNucleus(p.pdgId()); }
    /// is this a valid pentaquark ID?
    inline bool isPentaquark( const Particle& p ) { return isPentaquark(p.pdgId()); }
    /// is this a valid SUSY ID?
    inline bool isSUSY( const Particle& p ) { return isSUSY(p.pdgId()); }
    /// is this a valid R-hadron ID?
    inline bool isRhadron( const Particle& p ) { return isRhadron(p.pdgId()); }

    /// does this particle contain an up quark?
    inline bool hasUp( const Particle& p ) { return hasUp(p.pdgId()); }
    /// does this particle contain a down quark?
    inline bool hasDown( const Particle& p ) { return hasDown(p.pdgId()); }
    /// does this particle contain a strange quark?
    inline bool hasStrange( const Particle& p ) { return hasStrange(p.pdgId()); }
    /// does this particle contain a charm quark?
    inline bool hasCharm( const Particle& p ) { return hasCharm(p.pdgId()); }
    /// does this particle contain a bottom quark?
    inline bool hasBottom( const Particle& p ) { return hasBottom(p.pdgId()); }
    /// does this particle contain a top quark?
    inline bool hasTop( const Particle& p ) { return hasTop(p.pdgId()); }

    /// jSpin returns 2J+1, where J is the total spin
    inline int jSpin( const Particle& p ) { return jSpin(p.pdgId()); }
    /// sSpin returns 2S+1, where S is the spin
    inline int sSpin( const Particle& p ) { return sSpin(p.pdgId()); }
    /// lSpin returns 2L+1, where L is the orbital angular momentum
    inline int lSpin( const Particle& p ) { return lSpin(p.pdgId()); }

    /// return 3 times the charge (3 x quark charge is an int)
    inline int threeCharge( const Particle& p ) { return threeCharge(p.pdgId()); }
    /// return the charge
    inline double charge( const Particle& p ) { return threeCharge(p)/3.0; }

    //@}

  }

}

#endif
