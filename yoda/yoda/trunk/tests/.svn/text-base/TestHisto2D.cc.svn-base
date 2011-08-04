#include "YODA/Histo2D.h"
#include "YODA/Profile1D.h"
#include <cmath>
#include <iostream>
#include <unistd.h>
#include <sys/time.h>

using namespace std;
using namespace YODA;


/// A stats printing function.
/**
 * This is a very, very unpolished version of a stats
 * printing function. It prints some stats sometimest 
 * looking at the full distribution and sometimes not.
 * A better verion is not to high in priority list now.
 */
void printStats(Histo2D& h, bool full=false){
    cout << "-----------------------------" << endl;
    cout << "LowEdgeX = " << h.lowEdgeX() << " HighEdgeX = " << h.highEdgeX() << endl;
    cout << "LowEdgeY = " << h.lowEdgeY() << " HighEdgeY = " << h.highEdgeY() << endl;

    cout << "Sum of weights is " << h.sumW(true) << ", squared: " << h.sumW2(true) << endl;

    if(full) {
        cout << "Means: " << h.xMean(true) << " " << h.yMean(true) << endl;
        cout << "Variance: " << h.xVariance(true) << " " << h.yVariance(true) << endl;
        cout << "StdDevs: " << h.xStdDev(true) << " " << h.yStdDev(true) << endl;
    }
    cout << "-----------------------------" << endl;
}

int main() {
    
    /// Creating a histogram and measuring the time it takes to do it.
    struct timeval startTime;
    struct timeval endTime;
    gettimeofday(&startTime, NULL);
    Histo2D h(200, 0, 100, 200, 0, 100);
    gettimeofday(&endTime, NULL);

    double tS = (startTime.tv_sec*1000000 + startTime.tv_usec)/(double)1000000;
    double tE = (endTime.tv_sec*1000000 + endTime.tv_usec)/(double)1000000;
    cout << "Time to create 40K bins: " << tE - tS << "s" << endl;
    printStats(h);
    
    
    /// Trying to fill a bin.
    gettimeofday(&startTime, NULL);
    for (int i=0; i < 2000000; i++) {
        int out = h.fill(16.0123, 12.213, 2);
        if(out == -1) {
            cout << "I wasn't able to find the bin, something must be incorecct in search algorithm:" << endl;
            return -1;
        }
    }
    gettimeofday(&endTime, NULL);

    tS = (startTime.tv_sec*1000000 + startTime.tv_usec)/(double)1000000;
    tE = (endTime.tv_sec*1000000 + endTime.tv_usec)/(double)1000000;
    cout << "Time taken to fill 2M bins: " << tE - tS << "s" << endl; 
    if((tE - tS) > 50.0) {
        cout << "Performance is not sufficient. Probably broken caches?" << endl;
        return -1;
    }

    printStats(h, true);
    cout << h.numBinsTotal() << endl;   
    
    /// Testing if fill() function does what it should
    unsigned int beforeAdd = h.numBinsTotal();
    cout << "Does a too high bin exist? " << h.fill(10000, 34234, 1) << endl;
    if(h.numBinsTotal() != beforeAdd) {
        cout << "An incorrect bin seems to have been added. The other solution is an error in numBinsTotal()" << endl;
        return -1;
    }

    h.isGriddy();

    /// Checking if everything is still working as desired.
    /** 
     * It is actually a good thing to do, as at some earlier stages 
     * in developement adding a broken bin destroyed the cache of edges.
     */
    int originIndex = h.fill(0.0, 0.0, 1);
    cout << "And is the origin working in the right way? " << originIndex << endl;
    if(originIndex == -1) {
        cout << "The origin was not found!" << endl;
        return -1;
    }

    printStats(h, true);
    
    /// Now, adding a square that is in a non-overlapping location:
    beforeAdd = h.numBinsTotal();
    h.addBin(150, 150, 200, 200);
    cout << "Added proprely? " << h.fill(150.1, 150.1, 1) << " Size: " << h.numBinsTotal() << endl;
    if(beforeAdd == h.numBinsTotal()) {
        cout << "A bin that should be added wasn't added." << endl;
        return -1;
    }

    /// Checking if a broken bin triggers _dropEdge().
    beforeAdd = h.numBinsTotal();
    h.addBin(0.756, 0.213, 12.1234, 23);
    cout << "Size: " << h.numBinsTotal() << endl;
    if(beforeAdd != h.numBinsTotal()) {
        cout << "Detection of overlapping edges doesn't work!" << endl;
        return -1;
    }

    int fillTest = h.fill(0.0, 1.0, 1);
    cout << "And a fill sanity check: " << fillTest << endl;
    if(fillTest == -1) {
        cout << "An undefined error with fill had occured." << endl;
        return -1;
    }

    /// A check testing mostly _fixOrientation()
    cout << "Now, how about another quadrant? " << endl;
    beforeAdd = h.numBinsTotal();
    h.addBin(-12, -12, -1, -1);
    if(beforeAdd == h.numBinsTotal()) {
        cout << "A bin that should be added could not be added." << endl;
        return -1;
    }

    fillTest = h.fill(-3, -3, 1);
    cout << "Trying to fill the newly created bin: " << fillTest << endl;
    if(fillTest == -1 || fillTest != (int)h.numBinsTotal() - 1) {
        cout << "Could not fill the bin that should be filled" << endl;
        return -1;
    }
    
    /// And a scaling test.
    printStats(h, true);
    cout << "Scaling: " << endl;

    gettimeofday(&startTime, NULL);
    h.scale(2.0, 3.0);
    gettimeofday(&endTime, NULL);
    tS = (startTime.tv_sec*1000000 + startTime.tv_usec)/(double)1000000;
    tE = (endTime.tv_sec*1000000 + endTime.tv_usec)/(double)1000000;

    cout << "Time to scale: " << tE - tS << "s" << endl;
    printStats(h, true);

    fillTest = h.fill(180, 180, 1);
    cout << "Was everything scaled as it should be? " << fillTest << endl;
    if(fillTest == -1) {
        cout << "Something went wrong while scaling." << endl;
        return -1;
    }

    /// Addition/Substraction:
    Histo2D first(100, 0, 100, 100, 0, 100);
    first.fill(1,1,1);
    Histo2D second(100, 0, 100, 100, 0, 100);
    second.fill(1,1,1);

    Histo2D added(first+second);
    Histo2D substracted(first-second);
    //Histo2D divided(first / second);

    printStats(added);
    printStats(substracted);
    //printStats(divided);

    ///And now, test cuts:

    cout << endl << endl << endl << "Testing cuts: " << endl;
    Histo2D sampleHisto(50, 0, 100, 39, 0, 10);
    sampleHisto.fill(0,0,123121);
    cout << sampleHisto.sumW(false) << " " << sampleHisto.sumW2(false) << endl;
    printStats(sampleHisto);
    if(!fuzzyEquals(sampleHisto.sumW(false), (double)123121)) {
        cout << "Something is wrong with weight filling!!" << endl;
        return -1;
    }
    if(!fuzzyEquals(sampleHisto.sumW2(false), 1.51588e+10)) {
        cout << "Something is wrong with weight squared!" << endl;
        return -1;
    }

    Histo1D atY(sampleHisto.cutterX(0));
    cout << atY.sumW(false) << " " <<atY.numBins() << endl;
    if(!fuzzyEquals(atY.sumW(false), sampleHisto.sumW(false))){
        cout << "Something is wrong with weights when cut parallell to X axis." << endl;
        return -1;
    }

    Histo1D atX(sampleHisto.cutterY(0));
    cout << atX.sumW(false) << " " << atX.numBins() << endl;
    if(!fuzzyEquals(atX.sumW(false), sampleHisto.sumW(false))){
        cout << "Something is wrong with weights when cut parallell to Y axis." << endl;
        return -1;
    }


    Histo1D atX2(sampleHisto.cutterX(2));
    cout << atX2.sumW(false) << " " << atX2.numBins() << endl;
    if(!fuzzyEquals(atX2.sumW(false), 0)){
        cout << "Probably the cuts are not done properly!" << endl;
        return -1;
    }
    
    return EXIT_SUCCESS;
}
