################################################################################
#
# This module generate pattern for paper model of OpenDive
# (http://www.durovis.com/opendive.html) compatible 3D glasses
# Copyright (C) 2014 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.gnu.org/licenses/gpl-2.0.html
#
################################################################################

__doc__="""This module generate pattern for paper model of OpenDive
    (http://www.durovis.com/opendive.html) compatible 3D glasses.

    Usage Example:
    python pmdive.py --page_width=210 --pupillary_distance=70 --noscript output.svg
    """

from xml.dom import minidom
import math
STYLE="""
polyline {
    fill: none;
    stroke: black;
    stroke-width: 50
}
circle {
    fill: none;
    stroke: black;
    stroke-width: 50
}
rect {
    fill: none;
    stroke: black;
    stroke-width: 50
}
line {
    fill: none;
    stroke: black;
    stroke-width: 20;
    stroke-dasharray: 200,200
}
"""
SCRIPT="""
var params = { };
var svgparams = document.getElementsByTagName( "param" );
for (var i = 0; i < svgparams.length; ++i) {
    params[ svgparams[i].attributes["name"].value ] = svgparams[i].attributes["value"].value;
}

var actions = new function () {
    this.list = [];
    this.splice = function (s, l, action) {
        if (this.list.indexOf(action) < 0) {
            this.list.splice(s, l, action);
        }
    };
    this.push = function (action) {
        if (this.list.indexOf(action) < 0) {
            this.list.push(action);
        }
    };
    this.join = function (separator) {
        return this.list.join(separator);
    };
}

if (location.href.indexOf( '?' ) != -1) {
    location.href.split( '?' )[1].split(/&|;/).forEach(
        function( i ) {
            var varval = i.split( '=' );
            switch (unescape(varval[0])) {
                case "pd":
                    actions.push('updateCircles');
                    varval[0] = 'pupillary_distance';
                    break;
                case "dimensions":
                    var dimensions = varval[1].toLowerCase().split('x');
                    params[ 'device_width' ] = unescape(dimensions[1]);
                    params[ 'device_depth' ] = unescape(dimensions[2]);
                    varval = ['device_height', dimensions[0]];
                    actions.splice(0, 0, 'updateSymbols');
                    break;
                case "page_width":
                    actions.splice(0, 0, 'updateSymbols');
                    actions.push('updateViewBox');
                    break;
                case "page_height":
                    actions.splice(0, 0, 'updateSymbols');
                    actions.push('updateViewBox');
                    break;
                case "device_width": actions.splice(0, 0, 'updateSymbols'); break;
                case "device_height": actions.splice(0, 0, 'updateSymbols'); break;
                case "device_depth": actions.splice(0, 0, 'updateSymbols'); break;
                case "device_screen_middle": actions.splice(0, 0, 'updateSymbols'); break;
                case "lens_focal_length": actions.splice(0, 0, 'updateSymbols'); break;
                case "lens_diameter": actions.push('updateCircles'); break;
                case "pupillary_distance": actions.push('updateCircles'); break;
                case "strap_width": actions.push('updateStrapWidth'); break;
                case "page": actions.push('updatePages'); break;
                case "logo": actions.push('updateLogo'); break;
                default: break;
            }
            params[ unescape(varval[0]) ] = unescape(varval[1]);
        }
    )
}

function point(x, y) {
    this.x = x;
    this.y = y;
    this.toString = function (separator) {
        return x + ',' + y;
    }
}

function getScreenMiddle(params, side) {
    if (params.device_screen_middle == '') {
        return params.device_height/2;
    }
    if (side == 'Right') {
        return params.device_height - params.device_screen_middle;
    } else {
        return params.device_screen_middle;
    }
}

function getPoints(params, side) {
    var points = [];
    var last = null;
    points.push(last = new point(1300, Math.round(Math.sqrt(Math.pow(params.device_width / 2 - 25, 2) + Math.pow(params.lens_focal_length, 2)) * 100) + 9000))
    points.splice(0, 0, new point(0, last.y - 1200));
    points.push(last = new point(Math.round(getScreenMiddle(params, side) * 100 + 100), last.y));
    points.push(last = new point(5800, 9000));
    points.push(last = new point(Math.round(Math.sqrt(Math.pow(getScreenMiddle(params, side) - 58, 2) + Math.pow(params.lens_focal_length, 2)) * 100) + 5800, Math.round((params.device_width / 2 - 25) * 100) + 9000));
    angle = Math.atan((last.y -9000) / (last.x - 5800.0)) + Math.atan(1);
    angle1 = Math.atan((points[2].y - 9000) / (points[2].x - 5800.0));
    if (Math.abs(angle1) > angle) {
        angle1 = angle;
    }
    points.splice(4, 0, new point(Math.round(5800 + Math.abs(Math.cos(angle1) * 1414)), Math.round(Math.abs(Math.sin(angle1) * 1414)) + 9000));
    points.splice(5, 0, new point(points[5].x - Math.round(Math.abs(Math.sin(angle - Math.atan(1)) * 1000)), points[5].y + Math.round(Math.abs(Math.cos(angle - Math.atan(1)) * 1000))));
    points.push(last = new point(last.x, last.y + 1000));
    points.push(last = new point(last.x + 1000, last.y));
    points.push(last = new point(last.x, last.y - (params.device_width * 100) - 2000));
    points.push(last = new point(last.x - 1000, last.y));
    points.push(last = new point(last.x, last.y + 1000));
    points.push(last = new point(points[5].x, 13000 - points[5].y));
    if (angle > Math.asin(1)) {
        points.push(last = new point(5800, 3300));
    } else {
        points.push(last = new point(points[4].x, 13000 - points[4].y));
    }
    points.push(last = new point(5800, 4000));
    points.push(last = new point(5600, 4000));
    points.push(last = new point(5600, 0));
    points.push(last = new point(5600, 4000));
    points.push(last = new point(5800, 4000));
    points.push(last = new point(Math.round(getScreenMiddle(params, side) * 100 + 100), Math.round(Math.sqrt(Math.pow(params.device_width / 2 - 25, 2) + Math.pow(params.lens_focal_length - 1, 2)) * 100) + last.y));
    points.push(last = new point(last.x + Math.round(params.device_depth * 100 + 100), last.y));
    points.push(last = new point(last.x, last.y + Math.round(params.device_depth * 100 + 100)));
    points.push(last = new point(points[19].x, last.y));
    points.push(last = new point(points[20].x, last.y));
    points.push(last = new point(last.x + Math.round(Math.sqrt(Math.pow(getScreenMiddle(params, side) - 58, 2) + Math.pow(params.lens_focal_length, 2)) * 100), Math.round((params.device_width / 2 - 25) * 100) + last.y));
    points.push(last = new point(last.x, last.y + 5000));
    points.push(last = new point(points[23].x, points[23].y + Math.round(params.device_width * 100 + 100)));
    points.push(new point(1300, last.y));
    points.push(last = new point(0, last.y - 1200));
    return points;
}

function updateSymbols(params) {
    var rpoints = getPoints(params, 'Right');
    if (params.device_screen_middle == "" || params.device_screen_middle == params.device_height / 2) {
        var lpoints = rpoints;
    } else {
        var lpoints = getPoints(params, 'Left');
    }
    var nl = document.getElementsByTagName( "polyline" );
    nl[0].setAttribute("points", rpoints.slice(0,17).join(' '));
    nl[2].setAttribute("points", rpoints.slice(16).join(' '));
    nl[3].setAttribute("points", '0,400 800,400 1800,4000 1800,' + rpoints[19].y + ' 0,' +  rpoints[19].y);
    nl[4].setAttribute("points", lpoints.slice(0,17).join(' '));
    nl[6].setAttribute("points", lpoints.slice(16).join(' '));
    nl[7].setAttribute("points", '0,400 800,400 1800,4000 1800,' + lpoints[19].y + ' 0,' +  lpoints[19].y);
    nl = document.getElementsByTagName( "rect" );
    var strap_width = params.strap_width * 100 + 200;
    var y_int=Math.round(6500 - (strap_width / 2));
    for (var i = 0; i < nl.length; ++i) {
        nl[i].setAttribute("y", y_int);
        nl[i].setAttribute("height", strap_width);
    }
    y_int = Math.round((rpoints[25].y - rpoints[24].y - strap_width)/2) + rpoints[24].y;
    nl[3].setAttribute("x", rpoints[24].x - 1200);
    nl[3].setAttribute("y", y_int);
    nl[4].setAttribute("x", rpoints[24].x - 2100);
    nl[4].setAttribute("y", y_int);
    nl[8].setAttribute("x", lpoints[24].x - 1200);
    nl[8].setAttribute("y", y_int);
    nl[9].setAttribute("x", lpoints[24].x - 2100);
    nl[9].setAttribute("y", y_int);
    nl = document.getElementsByTagName( "line" );
    nl[1].setAttribute("x1", rpoints[6].x);
    nl[1].setAttribute("y1", rpoints[6].y - 100);
    nl[1].setAttribute("x2", rpoints[8].x);
    nl[1].setAttribute("y2", rpoints[6].y - 100);
    nl[2].setAttribute("x1", rpoints[3].x);
    nl[2].setAttribute("y1", rpoints[3].y);
    nl[2].setAttribute("x2", rpoints[6].x);
    nl[2].setAttribute("y2", rpoints[6].y);
    nl[3].setAttribute("x1", rpoints[6].x);
    nl[3].setAttribute("y1", rpoints[6].y);
    nl[3].setAttribute("x2", rpoints[11].x);
    nl[3].setAttribute("y2", rpoints[11].y);
    nl[4].setAttribute("x1", rpoints[11].x);
    nl[4].setAttribute("x2", rpoints[11].x);
    nl[4].setAttribute("y2", rpoints[11].y);
    nl[5].setAttribute("x1", rpoints[11].x);
    nl[5].setAttribute("y1", rpoints[11].y + 100);
    nl[5].setAttribute("x2", rpoints[8].x);
    nl[5].setAttribute("y2", rpoints[11].y + 100);
    nl[8].setAttribute("x2", rpoints[11].x);
    nl[8].setAttribute("y2", rpoints[11].y);
    nl[12].setAttribute("y1", rpoints[19].y);
    nl[12].setAttribute("x2", rpoints[19].x);
    nl[12].setAttribute("y2", rpoints[19].y);
    nl[13].setAttribute("x1", rpoints[19].x);
    nl[13].setAttribute("y1", rpoints[19].y);
    nl[13].setAttribute("x2", rpoints[22].x);
    nl[13].setAttribute("y2", rpoints[22].y);
    nl[14].setAttribute("y1", rpoints[22].y);
    nl[14].setAttribute("x2", rpoints[22].x);
    nl[14].setAttribute("y2", rpoints[22].y);
    nl[15].setAttribute("x1", rpoints[22].x + 100);
    nl[15].setAttribute("y1", rpoints[22].y);
    nl[15].setAttribute("x2", rpoints[22].x + 100);
    nl[15].setAttribute("y2", rpoints[26].y);
    nl[16].setAttribute("x1", rpoints[23].x);
    nl[16].setAttribute("y1", rpoints[23].y);
    nl[16].setAttribute("x2", rpoints[23].x);
    nl[16].setAttribute("y2", rpoints[26].y);
    nl[18].setAttribute("x1", lpoints[6].x);
    nl[18].setAttribute("y1", lpoints[6].y - 100);
    nl[18].setAttribute("x2", lpoints[8].x);
    nl[18].setAttribute("y2", lpoints[6].y - 100);
    nl[19].setAttribute("x1", lpoints[3].x);
    nl[19].setAttribute("y1", lpoints[3].y);
    nl[19].setAttribute("x2", lpoints[6].x);
    nl[19].setAttribute("y2", lpoints[6].y);
    nl[20].setAttribute("x1", lpoints[6].x);
    nl[20].setAttribute("y1", lpoints[6].y);
    nl[20].setAttribute("x2", lpoints[11].x);
    nl[20].setAttribute("y2", lpoints[11].y);
    nl[21].setAttribute("x1", lpoints[11].x);
    nl[21].setAttribute("x2", lpoints[11].x);
    nl[21].setAttribute("y2", lpoints[11].y);
    nl[22].setAttribute("x1", lpoints[11].x);
    nl[22].setAttribute("y1", lpoints[11].y + 100);
    nl[22].setAttribute("x2", lpoints[8].x);
    nl[22].setAttribute("y2", lpoints[11].y + 100);
    nl[25].setAttribute("x2", lpoints[11].x);
    nl[25].setAttribute("y2", lpoints[11].y);
    nl[29].setAttribute("y1", lpoints[19].y);
    nl[29].setAttribute("x2", lpoints[19].x);
    nl[29].setAttribute("y2", lpoints[19].y);
    nl[30].setAttribute("x1", lpoints[19].x);
    nl[30].setAttribute("y1", lpoints[19].y);
    nl[30].setAttribute("x2", lpoints[22].x);
    nl[30].setAttribute("y2", lpoints[22].y);
    nl[31].setAttribute("y1", lpoints[22].y);
    nl[31].setAttribute("x2", lpoints[22].x);
    nl[31].setAttribute("y2", lpoints[22].y);
    nl[32].setAttribute("x1", lpoints[22].x + 100);
    nl[32].setAttribute("y1", lpoints[22].y);
    nl[32].setAttribute("x2", lpoints[22].x + 100);
    nl[32].setAttribute("y2", lpoints[26].y);
    nl[33].setAttribute("x1", lpoints[23].x);
    nl[33].setAttribute("y1", lpoints[23].y);
    nl[33].setAttribute("x2", lpoints[23].x);
    nl[33].setAttribute("y2", lpoints[26].y);
    var trx = (Math.max(rpoints[8].x, rpoints[24].x) + Math.max(lpoints[8].x, lpoints[24].x)) / 2 + 50;
    if (trx > (params.page_width * 50)) {
        trx = Math.round(params.page_width * 50);
    }
    var pages = document.getElementsByTagName( "g" );
    for (var i = 0; i < 2; ++i) {
        var tr = pages[i].getAttribute( "transform" ).split(",")[1];
        pages[i].setAttribute( "transform", "translate(" + trx + "," + tr );
    }
    var nl = document.getElementsByTagName( "image" );
    nl[0].setAttribute( "height", params.device_width * 100 + 100 );
    nl[0].setAttribute( "width", params.device_height * 100 + 200 );
    nl[0].setAttribute( "transform", 'translate(' + rpoints[19].x + ',' + rpoints[26].y + ') scale(-1,-1)');
}

function updateViewBox(params) {
    var svg = document.getElementsByTagName( "svg" )[0];
    svg.setAttribute( "width", params.page_width + "mm" );
    svg.setAttribute( "height", params.page_height + "mm" );
    svg.setAttribute( "viewBox", "0 0 " +  (params.page_width * 100) + " " + (params.page_height * 100));
};

function updateCircles (params) {
    var r = params.lens_diameter * 50 - 200;
    var cx = params.pupillary_distance * 50; 
    var nl = document.getElementsByTagName( "circle" );
    for (var i = 0; i < nl.length; ++i) {
        nl[i].setAttribute( "cx", cx );
        if (i == 1 || i == 4) {
            nl[i].setAttribute( "r", r + 200 );
        } else {
            nl[i].setAttribute( "r", r );
        }
    }
}

function updateStrapWidth (params) {
    var strap_width = params.strap_width * 100 + 200;
    var nl = document.getElementsByTagName( "rect" );
    var yu = Math.round(6500 - strap_width/2);
    var yd = Math.round(nl[3].getAttribute( "y" )/1 + nl[3].getAttribute( "height" )/2 - strap_width/2);
    for (var i = 0; i < nl.length; ++i) {
        if ( [3,4,8,9].indexOf(i) < 0 ) {
            nl[i].setAttribute( "y", yu );
        } else {
            nl[i].setAttribute( "y", yd );
        }
        nl[i].setAttribute( "height", strap_width );
    }
}

function updateLogo (params) {
    var nl = document.getElementsByTagName( "image" );
    nl[0].setAttribute( "xlink:href", params.logo );
}

function updatePages(params) {
    var pages = document.getElementsByTagName( "g" );
    if (params.page == "1") {
        pages[0].setAttribute("visibility", "visible");
        pages[1].setAttribute("visibility", "hidden");
    } else if (params.page == "2") {
        pages[0].setAttribute("visibility", "hidden");
        pages[1].setAttribute("visibility", "visible");
        var tr = pages[1].getAttribute("transform").split(",")[0] + ",50)";
        pages[1].setAttribute("transform", tr);
    } else {
        pages[0].setAttribute("visibility", "visible");
        pages[1].setAttribute("visibility", "visible");
        tr = pages[0].getAttribute("transform");
        pages[1].setAttribute("transform", tr);
    }
}

for (var action in actions.list) {
    eval(actions.list[action])(params);
}
"""

class SVG(object):
    def __init__(self, page_width=297, page_height=420):
        imp = minidom.getDOMImplementation('')
        dt = imp.createDocumentType('svg',
            '-//W3C//DTD SVG 1.1//EN',
            'http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd')
        self.doc = imp.createDocument('http://www.w3.org/2000/svg', 'svg', dt)
        self.root = self.doc.getElementsByTagName('svg')[0]
        self.root.setAttribute('version', '1.1')
        self.root.setAttribute('width', '%smm'%page_width)
        self.root.setAttribute('height', '%smm'%page_height)
        self.root.setAttribute('viewBox', '0 0 %s00 %s00'%(page_width, page_height))
        self.root.setAttribute('preserveAspectRatio', 'xMinYMin slice')
        self.root.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
        self.root.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')

    def setAttributes(self, node, attrs):
        for (key, value) in attrs.iteritems():
            node.setAttribute(key, value)

    def element(self, ename, parent=None, attributes={}, **kwargs):
        el = self.doc.createElement(ename)
        for (key, value) in attributes.iteritems():
            el.setAttribute(key, value)
        for (key, value) in kwargs.iteritems():
            if key not in ('attributes', 'parent'):
                el.setAttribute(key, value)
        if parent is not None:
            parent.appendChild(el)
        return el

    def textNode(self, ename, data, parent=None, **kwargs):
        el = self.element(ename, parent, **kwargs)
        tn = self.doc.createTextNode(data)
        el.appendChild(tn)

    def hidePage(self, page=None):
        pages = self.doc.getElementsByTagName("g")
        if page == None:
            pages[0].setAttribute("visibility", "visible")
            pages[1].setAttribute("visibility", "visible")
            tr = pages[0].getAttribute("transform")
            pages[1].setAttribute("transform", tr)
        elif page == 2:
            pages[0].setAttribute("visibility", "visible")
            pages[1].setAttribute("visibility", "hidden")
        elif page == 1:
            pages[0].setAttribute("visibility", "hidden")
            pages[1].setAttribute("visibility", "visible")
            tr = pages[1].getAttribute("transform").split(",")[0] + ",50)"
            pages[1].setAttribute("transform", tr)


class pmDive(object):
    """This class provides pmDive attributes and functions for generating svg file with pmDive pattern.

    Attributes:

    page_width -- target page width in mm (default:297mm)
    page_height -- target page height in mm (default:420mm)
    device_width -- the width of the smartphone in mm
    device_height -- the height of the smartphone in mm
    device_depth -- the depth of the smartphone in mm
    dimensions -- dimensions in form HxWxD
    device_screen_middle -- the middle of the smartphones screen (default: None if
        the middle of screen is the middle of the smartphone)
    lens_focal_length -- the focal length of the lens in mm (default: 40mm)
    lens_diameter -- the diameter of the lens in mm (default:26mm)
    strap_width -- the width of mask strap in mm
    pupillary_distance -- the pupillary distance in mm
    pd -- alias for pupillary_distance
    page -- page number (1 or 2) for multipage output (default: None)
    noscript -- do not add JavaScript to target SVG file
    logo -- logo file (in png, jpg or svg format)
    """

    page_width=297
    page_height=420
    device_width=65.5
    device_height=132.6
    device_depth=6.18
    device_screen_middle=None
    lens_focal_length=40
    lens_diameter=26
    strap_width=40
    pupillary_distance=60
    page=None
    noscript=False
    logo='data:image/svg+xml;utf8,%3Csvg xmlns="http://www.w3.org/2000/svg"%3E%3Ctext x="270" y="500" font-family="Verdana" font-size="200"%3EPM%3C/text%3E%3Ctext x="100" y="700" font-family="Verdana" font-size="800"%3EDive%3C/text%3E%3C/svg%3E'
    pd=None
    dimensions=None

    def __init__(self, **kwargs):
        for var, val in kwargs.iteritems():
            setattr(self, var, val)

    def __setattr__(self, name, value):
        if name == 'dimensions':
            values = value.lower().split('x')
            if len(values) == 3:
                if not (49<float(values[1])<101 and 4<float(values[2])<21):
                    raise AttributeError("Property value out of range")
                super(pmDive, self).__setattr__('device_width', float(values[1]))
                super(pmDive, self).__setattr__('device_depth', float(values[2]))
                value = values[0]
                name = 'device_height'
        if str(value) == 'None':
            value = None
        else:
            value = float(value)
        limits = {'page_width':99<value<499,
                  'page_height':99<value<499,
                  'device_width':49<value<101,
                  'device_height':89<value<201,
                  'device_depth':4<value<21,
                  'device_screen_middle':29<value<201 or value == None,
                  'lens_focal_length':29<value<51,
                  'lens_diameter':19<value<31,
                  'strap_width':19<value<47,
                  'pupillary_distance':49<value<81,
                  'pd':49<value<81,
                  'page':0<value<3 or value == None,
                  'noscript':0<value<3 or value == None,
                  'logo':True,
                  'dimensions':True,
                  }
        if name == 'pd':
            name = 'pupillary_distance'
        if name not in limits:
            raise AttributeError("Incorrect property name: %s"%name)
        if limits[name] is False:
            raise AttributeError("Property value out of range")
        if name == 'device_height':
            super(pmDive, self).__setattr__('device_screen_middle', None)
        super(pmDive, self).__setattr__(name, value)

    def getScreenMiddle(self, side='Right'):
        if self.device_screen_middle is None:
            return self.device_height/2
        if side=='Right':
            return self.device_height-self.device_screen_middle
        else:
            return self.device_screen_middle

    def getPoints(self, side='Right'):
        points = []
        points.append((1300, int(round(((self.device_width/2-25)**2+self.lens_focal_length**2)**.5*100)) + 9000))
        points.insert(0, (0, points[-1][1]-1200))
        points.append((int(self.getScreenMiddle(side)*100+100), points[-1][1]))
        points.append((5800,9000))
        points.append(((int(round(((self.getScreenMiddle(side)-58)**2+self.lens_focal_length**2)**.5*100)))+5800, int(round((self.device_width/2-25)*100))+9000))
        angle = math.atan((points[-1][1]-9000)/(points[-1][0]-5800.0))+math.atan(1)
        angle1 = math.atan((points[2][1]-9000)/(points[2][0]-5800.0))
        if abs(angle1) > angle:
            angle1 = angle
        points.insert(4, (int(round(5800+abs(math.cos(angle1)*1414))), int(round(abs(math.sin(angle1)*1414))) + 9000))
        points.insert(5, (points[5][0]-int(round(abs(math.sin(angle-math.atan(1))*1000))), points[5][1]+int(round(abs(math.cos(angle-math.atan(1))*1000)))))
        points.append((points[-1][0],points[-1][1]+1000))
        points.append((points[-1][0]+1000,points[-1][1]))
        points.append((points[-1][0],points[-1][1] - int(self.device_width*100) - 2000))
        points.append((points[-1][0]-1000,points[-1][1]))
        points.append((points[-1][0],points[-1][1]+1000))
        points.append((points[5][0], 13000 - points[5][1]))
        if angle > math.asin(1):
            points.append((5800,3300))
        else:
            points.append((points[4][0], 13000 - points[4][1]))
        points.append((5800,4000))
        points.append((5600,4000))
        points.append((5600,0))
        points.append((5600,4000))
        points.append((5800,4000))
        points.append((int(self.getScreenMiddle(side)*100+100), int(round(((self.device_width/2-25)**2+(self.lens_focal_length-1)**2)**.5*100))+points[-1][1]))
        points.append((points[-1][0]+int(round(self.device_depth*100+100)), points[-1][1]))
        points.append((points[-1][0],points[-1][1]+int(round(self.device_depth*100+100))))
        points.append((points[-3][0], points[-1][1]))
        points.append((points[-3][0], points[-1][1]))
        points.append((points[-1][0] + int(round(((self.getScreenMiddle(side)-58)**2+self.lens_focal_length**2)**.5*100)), int(round((self.device_width/2-25)*100))+points[-1][1]))
        points.append((points[-1][0],points[-1][1]+5000))
        points.append((points[-3][0],points[-3][1]+int(round(self.device_width*100+100))))
        points.append((1300,points[-1][1]))
        points.append((0,points[-2][1]-1200))
        return points

    def getSymbols(self, svg, points):
        cx_int = int(round(self.pupillary_distance*50))
        r_int = int(round(self.lens_diameter*50))
        strap_width=int(self.strap_width*100+200)
        usymbol = svg.element('symbol', None, id='RightUpSide')
        svg.element('polyline', usymbol, points=' '.join(['%s,%s'%p for p in points[:17]]))
        svg.element('polyline', usymbol, points='0,7600 800,7600 1800,4000 800,400 0,400')
        svg.element('circle', usymbol, cx=str(cx_int), cy='6500', r=str(r_int-200))
        svg.element('circle', usymbol, cx=str(cx_int), cy='1500', r=str(r_int))
        y_int=int(round(6500 - strap_width/2))
        svg.element('rect', usymbol, x='5600', y=str(y_int), width='200', height=str(strap_width))
        svg.element('rect', usymbol, x='6800', y=str(y_int), width='200', height=str(strap_width))
        svg.element('rect', usymbol, x='7800', y=str(y_int), width='200', height=str(strap_width))
        svg.element('line', usymbol, x1='0', y1='9000', x2='5800', y2='9000')
        svg.element('line', usymbol, x1=str(points[6][0]), y1=str(points[6][1]-100), x2=str(points[8][0]), y2=str(points[6][1]-100))
        svg.element('line', usymbol, x1=str(points[3][0]), y1=str(points[3][1]), x2=str(points[6][0]), y2=str(points[6][1]))
        svg.element('line', usymbol, x1=str(points[6][0]), y1=str(points[6][1]), x2=str(points[11][0]), y2=str(points[11][1]))
        svg.element('line', usymbol, x1=str(points[11][0]), y1='9000', x2=str(points[11][0]), y2=str(points[11][1]))
        svg.element('line', usymbol, x1=str(points[11][0]), y1=str(points[11][1]+100), x2=str(points[8][0]), y2=str(points[11][1]+100))
        svg.element('line', usymbol, x1='5800', y1='9000', x2='5800', y2='4000')
        svg.element('line', usymbol, x1='1800', y1='4000', x2='5800', y2='4000')
        svg.element('line', usymbol, x1='5800', y1='4000', x2=str(points[11][0]), y2=str(points[11][1]))
        svg.element('line', usymbol, x1='0', y1='0', x2='5600', y2='0')
        symbol = svg.element('symbol', None, id='RightDownSide')
        svg.element('polyline', symbol, points=' '.join(['%s,%s'%p for p in points[16:]]))
        svg.element('polyline', symbol, points='0,400 800,400 1800,4000 1800,%s 0,%s'%(str(points[19][1]),str(points[19][1])))
        svg.element('circle', symbol, cx=str(cx_int), cy='1500', r=str(r_int-200))
        y_int=int(round(((points[25][1]-points[24][1])-strap_width)/2)+points[24][1])
        svg.element('rect', symbol, x=str(points[24][0]-1200), y=str(y_int), width='200', height=str(strap_width))
        svg.element('rect', symbol, x=str(points[24][0]-2100), y=str(y_int), width='200', height=str(strap_width))
        svg.element('line', symbol, x1='0', y1='0', x2='5600', y2='0')
        svg.element('line', symbol, x1='1800', y1='4000', x2='5800', y2='4000')
        svg.element('line', symbol, x1='1800', y1=str(points[19][1]), x2=str(points[19][0]), y2=str(points[19][1]))
        svg.element('line', symbol, x1=str(points[19][0]), y1=str(points[19][1]), x2=str(points[22][0]), y2=str(points[22][1]))
        svg.element('line', symbol, x1='0', y1=str(points[22][1]), x2=str(points[22][0]), y2=str(points[22][1]))
        svg.element('line', symbol, x1=str(points[22][0]+100), y1=str(points[22][1]), x2=str(points[22][0]+100), y2=str(points[26][1]))
        svg.element('line', symbol, x1=str(points[23][0]), y1=str(points[23][1]), x2=str(points[23][0]), y2=str(points[26][1]))
        return usymbol, symbol

    def buildSVG(self):
        svg=SVG(self.page_width, self.page_height)
        svg.textNode('title', "Poor Man's Dive", svg.root)
        svg.textNode('desc', "Poor Man's Dive is a pattern for paper model of OpenDive (http://www.durovis.com/opendive.html) compatible 3D glasses.", svg.root)
        metadata = svg.element('metadata', svg.root)
        rdfRDF = svg.element('rdf:RDF', metadata, attributes={"xmlns:rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#","xmlns:cc":"http://creativecommons.org/ns#"})
        ccWork = svg.element('cc:Work', rdfRDF, attributes={"xmlns:dc":"http://purl.org/dc/elements/1.1/","rdf:about":""})
        svg.textNode('dc:format', "image/svg+xml", ccWork)
        svg.element('dc:type', ccWork, attributes={"rdf:resource":"http://purl.org/dc/dcmitype/StillImage"})
        svg.textNode('dc:creator', "Egor Puzanov", ccWork)
        svg.element('dc:license', ccWork, attributes={"rdf:resource":"http://creativecommons.org/licenses/by-sa/3.0/"})
        svg.element('cc:license', ccWork, attributes={"rdf:resource":"http://creativecommons.org/licenses/by-sa/3.0/"})
        svg.textNode('cc:attributionName', "Egor Puzanov", ccWork)
        ccLicense = svg.element('cc:License', rdfRDF, attributes={"rdf:about":"http://creativecommons.org/licenses/by-sa/3.0/"})
        svg.element('cc:permits', ccLicense, attributes={"rdf:resource":"http://creativecommons.org/ns#Reproduction"})
        svg.element('cc:permits', ccLicense, attributes={"rdf:resource":"http://creativecommons.org/ns#Distribution"})
        svg.element('cc:requires', ccLicense, attributes={"rdf:resource":"http://creativecommons.org/ns#Notice"})
        svg.element('cc:requires', ccLicense, attributes={"rdf:resource":"http://creativecommons.org/ns#Attribution"})
        svg.element('cc:permits', ccLicense, attributes={"rdf:resource":"http://creativecommons.org/ns#DerivativeWorks"})
        svg.element('cc:requires', ccLicense, attributes={"rdf:resource":"http://creativecommons.org/ns#ShareAlike"})
        svg.element('param', svg.root, name="page_width", value=str(self.page_width))
        svg.element('param', svg.root, name="page_height", value=str(self.page_height))
        svg.element('param', svg.root, name="device_width", value=str(self.device_width))
        svg.element('param', svg.root, name="device_height", value=str(self.device_height))
        svg.element('param', svg.root, name="device_depth", value=str(self.device_depth))
        svg.element('param', svg.root, name="device_screen_middle", value=str(self.device_screen_middle or ""))
        svg.element('param', svg.root, name="lens_focal_length", value=str(self.lens_focal_length))
        svg.element('param', svg.root, name="lens_diameter", value=str(self.lens_diameter))
        svg.element('param', svg.root, name="pupillary_distance", value=str(self.pupillary_distance))
        svg.element('param', svg.root, name="strap_width", value=str(self.strap_width))
        svg.element('param', svg.root, name="page", value=str(self.page or ""))
        defs = svg.element('defs', svg.root)
        style = svg.element('style', defs, type='text/css')
        style.appendChild(svg.doc.createCDATASection(STYLE))
        rpoints = self.getPoints('Right')
        usymbol, symbol = self.getSymbols(svg, rpoints)
        defs.appendChild(usymbol)
        defs.appendChild(symbol)
        if self.getScreenMiddle() != self.device_height/2:
            lpoints = self.getPoints('Left')
            usymbol, symbol = self.getSymbols(svg, lpoints)
        else:
            lpoints = rpoints
            usymbol = usymbol.cloneNode(True)
            symbol = symbol.cloneNode(True)
        usymbol.setAttribute('id', 'LeftUpSide')
        symbol.setAttribute('id', 'LeftDownSide')
        defs.appendChild(usymbol)
        defs.appendChild(symbol)
        translate = [(max(rpoints[8][0], rpoints[24][0])+max(lpoints[8][0], lpoints[24][0]))/2+50, rpoints[1][1]+50]
        if translate[0]>self.page_width*50:
            translate[0] = int(round(self.page_width*50)) + 50
        g = svg.element('g', svg.root, visibility='hidden' if self.page == 2 else 'visible', id='page1', transform='translate(%s,%s)'%tuple(translate))
        svg.element('use', g, **{'xlink:href':'#LeftUpSide', 'transform':'scale(-1,-1)'})
        svg.element('use', g, **{'xlink:href':'#RightUpSide', 'transform':'scale(1,-1)'})
        if self.page == 2:
            translate[1] = 50
        g = svg.element('g', svg.root, visibility='hidden' if self.page == 1 else 'visible', id='page2', transform='translate(%s,%s)'%tuple(translate))
        svg.element('image', g, **{'x':'0','y':'0','height':str(int(self.device_width*100+100)),'width':str(int(self.device_height*100+200)), 'xlink:href':self.logo, 'transform':'translate(%s,%s) scale(-1,-1)'%(rpoints[19][0],rpoints[26][1])})
        svg.element('use', g, **{'xlink:href':'#LeftDownSide', 'transform':'scale(-1,1)'})
        svg.element('use', g, **{'xlink:href':'#RightDownSide'})
        if not self.noscript:
            script = svg.element('script', svg.root, type='application/ecmascript')
            script.appendChild(svg.doc.createCDATASection(SCRIPT))
        return svg

if __name__ == '__main__':
    import sys, getopt
    lopts = ['help', 'noscript']
    for attr, val in pmDive.__dict__.iteritems():
        if attr.startswith('__') or callable(val) or attr in lopts: continue
        lopts.append('%s='%attr)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", lopts)
    except getopt.GetoptError:
        print __doc__
        sys.exit(2)
    pd = pmDive()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print pd.__doc__
            sys.exit()
        if opt == "--noscript":
            arg = True
        setattr(pd, opt[2:], arg)
    if not args:
        args.append('pmdive.svg')
    d=pd.buildSVG()
    f = open(args[0], 'w+')
    f.write(d.doc.toprettyxml())
    f.close()
