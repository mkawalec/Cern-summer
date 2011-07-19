#! /usr/bin/env python

import logging
import urllib2
import re

usage = """%prog <spiresid> [<spiresid2> ...]

Given SPIRES paper IDs, fetch the corresponding BibTeX db entry from the SPIRES
Web interface and write it to stdout.
"""

def fetch_spires_bibtex(spiresid):
    spiresurl = "http://www.slac.stanford.edu/spires/find/hep/www?key=%s&FORMAT=WWWBRIEFBIBTEX" % str(spiresid)
    logging.debug("Downloading SPIRES BibTeX from %s" % spiresurl)
    hreq = urllib2.urlopen(spiresurl)
    bibtexhtml = hreq.read()
    hreq.close()
    #logging.debug(bibtexhtml)
    return bibtexhtml


def extract_bibtex(spireshtml):
    ## Extract BibTeX block from HTML
    re_spiresbibtex = re.compile(r'<!-- START RESULTS -->.*?<pre>(.*?)</pre>', re.MULTILINE | re.DOTALL)
    m = re_spiresbibtex.search(spireshtml)
    if m is None:
        return None, None
    bib = m.group(1).strip()

    ## Get BibTeX key
    re_bibtexkey = re.compile(r'^@.+?{(.+?),$', re.MULTILINE)
    m = re_bibtexkey.search(bib)
    if m is None:
        return None, bib
    key = m.group(1)

    ## Return key and BibTeX
    return key, bib


def get_bibtex_from_spires(spiresid):
    html = fetch_spires_bibtex(spiresid)
    key, bibtex = extract_bibtex(html)
    return key, bibtex


def get_bibtexs_from_spires(spiresids):
    bibdb = {}
    for spiresid in spiresids:
        key, bibtex = get_bibtex_from_spires(spiresid)
        if key and bibtex:
            bibdb[spiresid] = (key, bibtex)
    return bibdb


if __name__ == '__main__':
    ## Parse command line options
    from optparse import OptionParser
    parser = OptionParser(usage=usage)
    opts, args = parser.parse_args()

    ## Make individual bibinfo files
    for sid in args:
        key, bibtex = get_bibtex_from_spires(sid)
        import sys
        f = sys.stdout
        f.write("BibKey: %s\n" % key)
        f.write("BibTeX: '%s'\n" % bibtex)

    # ## Build ref db
    # bibdb = get_bibtexs_from_spires(args)
    # for sid, (key, bibtex) in bibdb.iteritems():
    #     print key, "=>\n", bibtex

    # ## Pickle ref db
    # import cPickle as pickle
    # fpkl = open("spiresbib.pkl", "w")
    # pickle.dump(bibdb)
    # fpkl.close()
