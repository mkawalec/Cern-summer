// -*- C++ -*-
#ifndef LWH_Tree_H
#define LWH_Tree_H
//
// This is the declaration of the Tree class.
//

#include "AITree.h"
#include "ManagedObject.h"
#include <fstream>
#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <string>

namespace LWH {


  using namespace AIDA;


  enum fileformat {
    flat,
    xml
    #ifdef HAVE_ROOT
    , root
    #endif
  };


  /**
   * The Tree class is a simple implementation of the AIDA::ITree
   * interface.
   */
  class Tree: public ITree {

  public:

    /** The AnalysisFactory is a friend. */
    friend class AnalysisFactory;

    /** A path is a vector of directory names. */
    typedef std::vector<std::string> Path;

    /** A set of paths */
    typedef std::set<Path> PathSet;

    /** Map of paths to objects. */
    typedef std::map<std::string, IManagedObject *> ObjMap;


  public:

    /**
     * The standard constructor.
     */
    //  Tree(std::string storename, bool xml = true)
    Tree(std::string storename, fileformat fchoice = xml)
      : name(storename), fform(fchoice), cwd(""), overwrite(true) {
      dirs.insert(Path());
      //: name(storename), flat(!xml), cwd("/"), overwrite(true) {
    }

    /**
     * The default constructor.
     */
    //Tree(): name(""), flat(false), cwd("/") {
    Tree(): name(""), fform(xml), cwd("") {
      dirs.insert(Path());
    }

    /**
     * The copy constructor.
     */
    Tree(const Tree & dt)
      //: ITree(dt), name(dt.name), flat(dt.flat), dirs(dt.dirs),
      : ITree(dt), name(dt.name), fform(dt.fform), dirs(dt.dirs),
        objs(dt.objs), cwd(dt.cwd), overwrite(true) {}

    /// Destructor.
    virtual ~Tree() {
      for ( ObjMap::iterator it = objs.begin(); it != objs.end(); ++it )
        delete it->second;
    }

    /**
     * Get the name of the store.
     * @return The store's name.
     */
    std::string storeName() const {
      return name;
    }

    /**
     * Get the IManagedObject at a given path in the ITree. The path can either be
     * absolute or relative to the current working directory.
     * @param path The path.
     * @return     The corresponding IManagedObject.
     */
    IManagedObject * find(const std::string & path) {
      ObjMap::const_iterator it = objs.find(path);
      return it == objs.end()? (IManagedObject *)0: it->second;
    }

    /**
     * LWH cannot get a mounted ITree at a given path in the current ITree.
     * @return     0 always.
     */
    ITree * findTree(const std::string &) {
      return 0;
    }

    /**
     * Change to a given directory.
     * @param dir The absolute or relative path of the directory we are
     * changing to.
     * @return false If the path does not exist.
     */
    bool cd(const std::string & dir) {
      PathSet::iterator it = dirs.find(purgepath(str2pth(fullpath(sts(dir)))));
      if ( it == dirs.end() ) return false;
      cwd = pth2str(*it);
      return true;
    }

    /**
     * Insert the ManagedObject \a o in the tree with the path \a str.
     */
    bool insert(std::string str, IManagedObject * o) {
      Path path = purgepath(str2pth(fullpath(str)));
      //PathSet::iterator theIterator;
      //for( theIterator = dirs.begin(); theIterator != dirs.end(); theIterator++ ) {
      //std::cout << "1:" << pth2str(*theIterator);
      //}
      //std::cout << std::endl;

      if ( dirs.find(path) == dirs.end() ) {
        std::string fullname = pth2str(path);
        path.pop_back();
        if ( dirs.find(path) != dirs.end() ) {
          ObjMap::iterator old = objs.find(fullname);
          if ( old == objs.end() || overwrite ) {
            if ( old != objs.end() ) {
              delete old->second;
              objs.erase(old);
            }
            objs[fullname] = o;
            return true;
          }
        }
      }
      return false;
    }

    /**
     * Get the path of the current working directory.
     * @return The path of the current working directory.
     */
    std::string pwd() const {
      return cwd;
    }

    /**
     * List, into a given output stream, all the IManagedObjects, including
     * directories (but not "." and ".."), in a given path. Directories end
     * with "/". The list can be recursive.
     * @param path      The path where the list has to be performed
     *                  (by default the current directory ".").
     * @param recursive If <code>true</code> the list is extended recursively
     *                  in all the directories under path (the default is
     *                  <code>false</code>.
     * @param os        The output stream into which the list is dumped
     *                  (by default the standard output).
     * @return false If the path does not exist.
     *
     */
    bool ls(const std::string & path = ".", bool recursive = false,
            std::ostream & os = std::cout) const {
      std::vector<std::string> names = listObjectNames(path, recursive);
      if ( names.empty() ) return false;
      for ( int i = 0, N = names.size(); i < N; ++i )
        os << names[i] << std::endl;
      return true;
    }

    /**
     * Get the list of names of the IManagedObjects under a given path,
     * including directories (but not "." and ".."). Directories end with "/".
     * The returned names are appended to the given path unless the latter is ".".
     * @param path      The path where the list has to be performed
     *                  (by default the current directory ".").
     * @param recursive If <code>true</code> the list is extended recursively
     *                  in all the directories under path (the default is
     *                   <code>false</code>.
     */
    std::vector<std::string> listObjectNames(const std::string & path = ".",
                                             bool recursive = false) const {
      std::vector<std::string> ret;
      PathSet::iterator it = dirs.find(purgepath(str2pth(fullpath(sts(path)))));
      if ( it == dirs.end() ) return ret;
      std::string dir = pth2str(*it) + "/";
      if ( path == "/" ) dir = "/";
      if ( recursive ) {
        for ( ObjMap::const_iterator oi = objs.begin(); oi != objs.end(); ++oi )
          if ( oi->first.substr(0, dir.length()) == dir )
            ret.push_back(oi->first);
      } else {
        for ( ObjMap::const_iterator oi = objs.begin(); oi != objs.end(); ++oi )
          if ( stn(oi->first) + "/" == dir ) ret.push_back(oi->first);
        for ( PathSet::iterator pit = dirs.begin(); pit != dirs.end(); ++pit) {
          std::string pth = pth2str(*pit);
          if (stn(pth) + "/"  == dir && pth + "/" != dir )
            ret.push_back(pth + "/");
        }
      }

      if ( path == "." )
        for ( int i = 0, N = ret.size(); i < N; ++i )
          ret[i] = ret[i].substr(dir.size());

      return ret;
    }

    /**
     * Not implemented in LWH.
     */
    std::vector<std::string> listObjectTypes(const std::string & = ".",
                                             bool = false) const {
      return std::vector<std::string>();
    }

    /**
     * Create a new directory. Given a path only the last directory
     * in it is created if all the intermediate subdirectories already exist.
     * @param dir The absolute or relative path of the new directory.
     * @return false If a subdirectory within the path does
     * not exist or it is not a directory. Also if the directory already exists.
     */
    bool mkdir(const std::string & dir) {
      Path p = purgepath(str2pth(fullpath(sts(dir))));
      Path base = p;
      base.pop_back();
      if ( dirs.find(base) == dirs.end() ) return false;
      dirs.insert(p);
      return true;
    }

    /**
     * Create a directory recursively. Given a path the last directory
     * and all the intermediate non-existing subdirectories are created.
     * @param dir The absolute or relative path of the new directory.
     * @return false If an intermediate subdirectory
     *             is not a directory, or if the directory already exists.
     */
    bool mkdirs(const std::string & dir) {
      return mkdirs(purgepath(str2pth(fullpath(sts(dir)))));
    }

    /**
     * Create a directory recursively. Given a Path the last directory
     * and all the intermediate non-existing subdirectories are created.
     * @param p The full Path of the new directory.
     * @return false If an intermediate subdirectory
     *             is not a directory, or if the directory already exists.
     */
    bool mkdirs(Path p) {
      if ( dirs.find(p) != dirs.end() ) return true;
      dirs.insert(p);
      p.pop_back();
      return mkdirs(p);
    }

    /**
     * Remove a directory and all the contents underneeth.
     * @param dir The absolute or relative path of the directory to be removed.
     * @return false If path does not exist or if it is not
     *             a directory or if the directory is not empty.
     */
    bool rmdir(const std::string & dir) {
      Path path = purgepath(str2pth(fullpath(sts(dir))));
      if ( dirs.find(path) == dirs.end() ) return false;
      for ( ObjMap::const_iterator it = objs.begin(); it != objs.end(); ++it )
        if ( it->first.substr(0, dir.length()) == dir ) return false;
      dirs.erase(path);
      return true;
    }

    /**
     * Remove and delete an IManagedObject by specifying its path.
     * @param path The absolute or relative path of the IManagedObject to be
     * removed.
     * @return false If path does not exist.
     */
    bool rm(const std::string & path) {
      ObjMap::iterator it = objs.find(fullpath(path));
      if ( it == objs.end() ) return false;
      delete it->second;
      objs.erase(it);
      return true;
    }

    /**
     * Get the full path of an IManagedObject.
     * @param o The IManagedObject whose path is to be returned.
     * @return  The object's absolute path.
     *          If the object does not exist, an empty string is returned.
     */
    std::string findPath(const IManagedObject & o) const {
      for ( ObjMap::const_iterator it = objs.begin(); it != objs.end(); ++it )
        if ( it->second == &o ) return it->first;
      return "";
    }

    /**
     * Move an IManagedObject or a directory from one directory to another.
     * @param oldp The path of the IManagedObject [not direcoty] to be moved.
     * @param newp The path of the diretory in which the object has to be
     * moved to.
     * @return false If either path does not exist.
     */
    bool mv(const std::string & oldp, const std::string & newp) {
      Path newpath = purgepath(str2pth(fullpath(sts(newp))));
      std::string foldp = fullpath(oldp);
      Path oldpath = purgepath(str2pth(foldp));
      ObjMap::iterator it = objs.find(foldp);
      //std::cout << 1 << std::endl;
      if ( it == objs.end() ) return false;
      //std::cout << 2 << std::endl;
      // Changed from != by AB: surely the directory you're copying to must
      // exist? Why can't we just change the name in the same directory?
      if ( dirs.find(newpath) == dirs.end() ) return false;
      newpath.push_back(oldpath.back());
      //std::cout << 3 << std::endl;
      if ( !insert(pth2str(newpath), it->second) ) return false;
      //std::cout << 4 << std::endl;
      objs.erase(foldp);
      return true;
    }

    /**
     * Print all histograms to the supplied filename, in the supplied format.
     * @return false if something went wrong.
     */
    bool commit(std::string storename) {
      // Back up state
      const std::string oldname = name;
      // Set up temporary state
      name = storename;
      // Do the do
      const bool rtn = commit();
      // Reset!
      name = oldname;
      return rtn;
    }

    /**
     * Print all histograms to the current filename.
     * @return false if something went wrong.
     */
    bool commit() {
      std::ofstream of(name.c_str());
      if ( !of ) return false;
      if (fform==xml) {
        of
          << "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!DOCTYPE aida SYSTEM "
          << "\"http://aida.freehep.org/schemas/3.0/aida.dtd\">\n"
          << "<aida version=\"3.0\">\n"
          << "<implementation version=\"1.0\" package=\"LWH\"/>" << std::endl;
      }

      #ifdef HAVE_ROOT
      #include "TFile.h"
      TFile* file = 0;
      if (fform==root) {
        file = new TFile(name.c_str(),"RECREATE");
      }
      #endif

      for ( ObjMap::const_iterator it = objs.begin(); it != objs.end(); ++it ) {
        ManagedObject * o = dynamic_cast<ManagedObject *>(it->second);
        if (!o) continue;
        std::string path = it->first.substr(0, it->first.rfind('/'));
        std::string name = it->first.substr(it->first.rfind('/') + 1);

        switch(fform) {
        case flat:
          o->writeFLAT(of, path, name);
          break;
        case xml:
          o->writeXML(of, path, name);
          break;
          #ifdef HAVE_ROOT
        case root:
          o->writeROOT(file, path, name);
          break;
          #endif
        }
      }

      if (fform==xml) of << "</aida>" << std::endl;

#ifdef HAVE_ROOT
      if(fform==root) file->Close();
#endif

      return of.good();
    }


    /**
     * Not implemented in LWH.
     */
    void setOverwrite(bool o = true) {
      overwrite = o;
    }

    /**
     * Not implemented in LWH.
     * @return false always.
     */
    bool cp(const std::string &, const std::string &, bool = false) {
      return false;
    }

    /**
     * Not implemented in LWH.
     * @return false always.
     */
    bool symlink(const std::string &, const std::string &) {
      return false;
    }

    /**
     * Not implemented in LWH.
     * @return false always.
     */
    bool mount(const std::string &, ITree &, const std::string &) {
      return false;
    }

    /**
     * Not implemented in LWH.
     * @return false always.
     */
    bool unmount(const std::string &) {
      return false;
    }

    /**
     * Calls commit().
     */
    bool close() {
      return commit();
    }

    /**
     * Not implemented in LWH.
     * @return null pointer always.
     */
    void * cast(const std::string &) const {
      return 0;
    }

  protected:

    /** Strip trailing slash. */
    std::string sts(std::string s) const {
      if ( s[s.length() - 1] == '/' ) s = s.substr(0, s.length() - 1);
      if ( s[s.length() - 1] == '/' ) return "";
      return s;
    }

    /** Strip trailing name */
    std::string stn(std::string s) const {
      std::string::size_type slash = s.rfind('/');
      return s.substr(0, slash);
    }

    /** Get proper full path from possibly relative path. */
    std::string fullpath(std::string d) const {
      if ( d.empty() ) d = cwd;
      else if ( d[0] != '/' ) d = cwd + "/" + d;
      return pth2str(purgepath(str2pth(d)));
    }

    /** Convert a string containing a path to a Path object. */
    Path str2pth(std::string s) const {
      Path pth;
      std::string::size_type i = s.find_first_not_of("/");
      while ( i != std::string::npos ) {
        s = s.substr(i);
        i = s.find_first_of("/");
        pth.push_back(s.substr(0, i));
        if ( i == std::string::npos ) return pth;
        s = s.substr(i);
        i = s.find_first_not_of("/");
      }
      return pth;
    }

    /** Convert a Path object to a corresponding string. */
    std::string pth2str(const Path & pth) const {
      std::string str;
      for ( int i = 0, N = pth.size(); i < N; ++i ) str += "/" + pth[i];
      return str;
    }

    /** Remove '..' and '.' components of the given Path object. */
    Path purgepath(const Path & pth) const {
      Path p;
      for ( int i = 0, N = pth.size(); i < N; ++i ) {
        if ( pth[i] == ".." ) p.pop_back();
        else if ( pth[i] != "." ) p.push_back(pth[i]);
      }
      return p;
    }

  private:

    /** The filename to print histograms to. */
    std::string name;

    /** Format to write out in: AIDA XML, "flat" or ROOT. */
    fileformat fform;

    /** The set of defined directories. */
    PathSet dirs;

    /** The set of defined objects. */
    ObjMap objs;

    /** The current working directory. */
    std::string cwd;

    /** Overwrite strategy. */
    bool overwrite;

  };

}

#endif /* LWH_Tree_H */
