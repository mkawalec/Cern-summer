#! /usr/bin/env python

"""
Library for describing and building data plots.

TODO:
 * Structure of semantic/logical plot element representation.
 * Helper functions (on axis, plot, etc.) for coordinate trfs.
 * Rendering backends: TikZ and pyglet
"""

__version__ = "0.0.2"


class StyleConfig(object):
    """Object containing style information like font, font size, text color, etc."""
    pass


class PicElement(object):
    """A base class for any object which will be drawn, for common location of
    things like z-index."""
    # TODO: connect to the canvas at this point?

    def __init__(self):
        self.zindex = None

    def __cmp__(self, other):
        return cmp(self.zindex, other.zindex)


class PicElementContainer(dict):
    """A container for objects to be drawn, providing a local coordinate system
    and grouping of picture elements. The 'add' method is used to populate"""

    # TODO: If container has its own z-index, hierarchically use this when rendering contents?

    def add(self, obj, name=None):
        key = name
        if key is None:
            key = "_%d" % len(self)
        if key in self:
            raise Exception("PicElement key '%s' already exists in container" % key)
        self[key] = obj

    def __iter__(self):
        """Iterator over pic element contents which respects z-ordering."""
        for x in sorted(self.values()):
            yield x

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        if name in self.__dict__ or not isinstance(value, PicElement):
            dict.__setattr__(self, name, value)
        else:
            self.add(value, name)

    def __setitem__(self, name, value):
        self.__setattr__(name, value):


class Shape(PicElement):
    """Base class for shape primitives."""
    # TODO: Stroke and fill properties (and more... corner radii, etc.?) specified here
    def __init__(self):
        PicElement.__init__(self)


class Rect(Shape):
    """A box containing text, placeable on the plot or axes with reference to
    any of several anchor points and in several coordinate systems."""

    def __init__(self, x1, y1, x2, y2):
        Shape.__init__(self)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return "Rect[%s, %s, %s, %s]" % (self.x1, self.y1, self.x2, self.y2)



class Canvas(PicElementContainer):
    """A single 'sheet' on which to draw things. Also contains the default style
    configuration for attached drawing objects."""

    def __init__(self, xsize, ysize):
        PicElementContainer.__init__(self)
        self.xsize = xsize
        self.ysize = ysize
        self.current_zindex = 0

    # TODO: Specify the LaTeX preamble contents (programmatically) per-canvas

    # TODO: Global (module) object with default config

    # TODO: Encapsulate all coord trfs in objects?

    def _coords_x_abs_from_rel(self, xrel):
        return self.xsize * xrel
    def _coords_y_abs_from_rel(self, yrel):
        return self.ysize * yrel
    def _coords_xy_abs_from_rel(self, xrel, yrel):
        return self.xsize * xrel, self.ysize * yrel

    def _coords_x_rel_from_abs(self, xabs):
        return xabs / self.xsize
    def _coords_y_rel_from_abs(self, yabs):
        return yabs / self.ysize
    def _coords_xy_rel_from_abs(self, xabs, yabs):
        return xabs / self.xsize, yabs / self.ysize


# class Plot(object):
#     """A plot object with a title, annotations, etc. Does it need to exist or is
#     this just a more natural name for Axes?"""
#     # TODO So I guess this is an optional level to hold the title?
#     pass


class Axes(object):
    """I never liked this term in matplotlib... but it's probably the most
    natural, esp. if we have a Plot object above it"""
    pass

class Axis(object):
    """A single axis with automatic or manual tick marks, etc."""
    pass

class SharedAxes(object):
    """API element for grouping several axes together and sharing the actual
    axis representations between them. Should allow for:

     * Customising plot separation
     * Customising repeated tick marks

    Should this class only represent one direction of axes sharing? That would
    be easier, and maybe also clearer from an API point of view. Maybe
    generalise to higher dimensions (well, just 2D!) with an AxesGrid.
    """
    pass

class Text(object):
    pass

class TextBox(object):
    """A box containing text, placeable on the plot or axes with reference to
    any of several anchor points and in several coordinate systems."""
    pass

class Legend(object):
    """A specific box implementation for plot legends.
    TODO: Must have a sensible default behaviour,  but also be very customisable.
    """
    pass

class Graph(object):
    """Base class for all graph types."""
    pass

class BarGraph(Graph):
    """Provide options for how the bars are joined or not."""
    pass

class LineGraph(Graph):
    """Include smoothing algorithms"""
    pass

class ScatterGraph(Graph):
    """2D to start with... 3D would be better with a different object, tied to a
    3D axes and with a viewing angle configuration API."""
    pass

class ColourOrContourGraph(Graph):
    """How to represent these different sorts of 2D data representations in the
    API? The rendering methods might be quite different -- we could just overlay
    a contour object on top of a 2D colour plot to get """
    pass

class LegoOrSurfaceGraph(Graph):
    pass



if __name__ == "__main__":
    c = Canvas(14, 10)
    c.add(Rect(0.1, 0.2, 0.6, 0.7), "box1")
    c.box2 = Rect(0.5, 0.7, 0.8, 1.0)

    out  = "\\documentclass[11pt]{article}\n"
    out += "\\usepackage{amsmath,amssymb}\n"
    out += "\\usepackage[margin=0cm,paperwidth=%fcm,paperheight=%fcm]{geometry}\n" % (c.xsize, c.ysize)
    out += "\\usepackage{tikz}\n"
    out += "\\pagestyle{empty}\n"
    out += "\\usepackage[osf]{mathpazo}\n"
    out += "\\begin{document}\n"
    out += "\\thispagestyle{empty}\n"
    out += "\\begin{tikzpicture}\n"
    for obj in c:
        if isinstance(obj, Rect):
            x1, y1 = c._coords_xy_abs_from_rel(obj.x1, obj.y1)
            x2, y2 = c._coords_xy_abs_from_rel(obj.x2, obj.y2)
            out += " \\draw (%f,%f) -- (%f,%f);\n" % (x1, y1, x2, y2)
            out += " \\draw (%f,%f) rectangle (%f,%f);\n" % (x1, y1, x2, y2)
    out += "\\end{tikzpicture}\n"
    out += "\\end{document}\n"

    #print out
    import tex2pix
    r = tex2pix.Renderer(tex=out)
    r.mk("test.pdf")
