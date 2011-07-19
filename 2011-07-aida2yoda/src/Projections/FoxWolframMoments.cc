// -*- C++ -*-
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FoxWolframMoments.hh"
#include "Rivet/Cmp.hh"

namespace Rivet {
 
    int FoxWolframMoments::compare(const Projection& p) const {
        return mkNamedPCmp(p, "FS");
    }
 
 
    void FoxWolframMoments::project(const Event& e) {
        Log log = getLog();
     
        // Project into final state and get total visible momentum
        const FinalState& fs             = applyProjection<FinalState>(e, "VFS");

/*        const FastJets &jetProjC4   = applyProjection<FastJets>(e, "JetsC4");
		Jets theJetsC4  = jetProjC4.jetsByPt(20.0);
     
        Jets goodJetsC4;
		foreach(const Jet& jet, theJetsC4)
		{
            //const double jetphi = jet.momentum().azimuthalAngle(ZERO_2PI);
            //const double jeteta = jet.momentum().pseudorapidity();
            const double jpt    = jet.momentum().pT();
         
			if( jpt > 20.0 && goodJetsC4.size() < 4 )// && fabs(jeteta) < 2.5 )
            {
                goodJetsC4.push_back(jet);
            }
		}
  */
        // remember: # pairs = N! / ( r! * (N-r)! )
     
        // N.B.: Autocorrelations are included! Treat them separately as diagonal elements.
        // see: http://cepa.fnal.gov/psm/simulation/mcgen/lund/pythia_manual/pythia6.3/pythia6301/node215.html
     
        double sumEnergy = 0.0;
        for (ParticleVector::const_iterator pi = fs.particles().begin(); pi != fs.particles().end(); ++pi)
        //for ( Jets::const_iterator pi = goodJetsC4.begin() ; pi != goodJetsC4.end() ; ++pi )
        {
            sumEnergy += pi->momentum().E();

            const FourMomentum pi_4 = pi->momentum();

            for (ParticleVector::const_iterator pj = pi+1; pj != fs.particles().end(); ++pj)
            //for ( Jets::const_iterator pj = pi + 1 ; pj != goodJetsC4.end() ; ++pj )
            {
                if ( pi == pj ) continue;
             
                const FourMomentum pj_4 = pj->momentum();
             
                // Calculate x_ij = cos(theta_ij)
                double x_ij = 1.0;
                if ( pi != pj ) {
                    double denom =  pi_4.vector3().mod() * pj_4.vector3().mod();
                    x_ij = pi_4.vector3().dot( pj_4.vector3() ) / denom;
                }
             
                //log << Log::DEBUG << "x_ij = " << x_ij << endl;
             
                //const double core = fabs( pi_4 * pj_4 ); //  / sumet2 ;
				const double core = pi_4.vector3().mod() * pi_4.vector3().mod();
				
                for ( int order = 0; order < MAXMOMENT ; ++order ) {
                    // enter a factor 2.0 because ij = ji. Use symmetry to speed up!
                    _fwmoments[order] += 2.0 * core * gsl_sf_legendre_Pl( order, x_ij ) ;
                }
            } // end loop over p_j
         
            // Now add autocorrelations
            // Obviously cos(theta_ij) = 1.0
            // Note that P_l(1) == 1 for each l
            for ( int order = 0; order < MAXMOMENT ; ++order ) {
                    _fwmoments[order] += fabs( pi_4 * pi_4 );
            }
        } // end loop over p_i
     
     
        log << Log::DEBUG << "sumEnergy = " << sumEnergy << endl;
     
        for ( int order = 0; order < MAXMOMENT ; ++order ) {
            _fwmoments[order] /= (sumEnergy*sumEnergy);
        }
     
        // Normalize to H0
        for ( int order = 1; order < MAXMOMENT ; ++order ) {
            _fwmoments[order] /= _fwmoments[0];
        }
    }
 
}
