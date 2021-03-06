#!/usr/bin/python
# -*- coding: ISO-8859-15 -*-
# =============================================================================
# Copyright (c) 2009 Tom Kralidis
#
# Authors : Tom Kralidis <tomkralidis@hotmail.com>
#
# Contact email: tomkralidis@hotmail.com
# =============================================================================

"""
API for OGC Filter Encoding (FE) constructs and metadata.

Filter Encoding: http://www.opengeospatial.org/standards/filter

Currently supports version 1.1.0 (04-095).
"""

from owslib.etree import etree
from owslib import util

# default variables

schema = 'http://schemas.opengis.net/filter/1.1.0/filter.xsd'

namespaces = {
    None : 'http://www.opengis.net/ogc',
    'gml': 'http://www.opengis.net/gml',
    'ogc': 'http://www.opengis.net/ogc',
    'xs' : 'http://www.w3.org/2001/XMLSchema',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

schema_location = '%s %s' % (namespaces['ogc'], schema)

class FilterRequest(object):
    """ filter class """
    def __init__(self, version='1.1.0'):
        """

        filter Constructor

        Parameters 
        ----------

        - parent: parent etree.Element object (default is None)
        - version: version (default is '1.1.0')

        """

        self.version = version

    def setfilter(self, parent=None):
        if parent is None:
            tmp = etree.Element(util.nspath('Filter', namespaces['ogc']))
            tmp.set(util.nspath('schemaLocation', namespaces['xsi']), schema_location)
            return tmp
        else:
            etree.SubElement(parent, util.nspath('Filter', namespaces['ogc']))

    def setpropertyisequalto(self, parent, propertyname, literal, matchcase=True):
        """

        construct a PropertyIsEqualTo

        Parameters
        ----------

        - parent: parent etree.Element object
        - propertyname: the PropertyName
        - literal: the Literal value
        - matchcase: whether to perform a case insensitve query (default is True)

        """

        tmp = etree.SubElement(parent, util.nspath('PropertyIsEqualTo', namespaces['ogc']))
        if matchcase is False:
            tmp.set('matchCase', 'false')
        etree.SubElement(tmp, util.nspath('PropertyName', namespaces['ogc'])).text = propertyname
        etree.SubElement(tmp, util.nspath('Literal', namespaces['ogc'])).text = literal
    
    def setbbox(self, parent, bbox):
        """

        construct a BBOX search predicate

        Parameters
        ----------

        - parent: parent etree.Element object
        - bbox: the bounding box in the form [minx,miny,maxx,maxy]

        """

        tmp = etree.SubElement(parent, util.nspath('BBOX', namespaces['ogc']))
        etree.SubElement(tmp, util.nspath('PropertyName', namespaces['ogc'])).text = 'ows:BoundingBox'
        tmp2 = etree.SubElement(tmp, util.nspath('Envelope', namespaces['gml']))
        etree.SubElement(tmp2, util.nspath('lowerCorner', namespaces['gml'])).text = '%s %s' % (bbox[0], bbox[1])
        etree.SubElement(tmp2, util.nspath('upperCorner', namespaces['gml'])).text = '%s %s' % (bbox[2], bbox[3])

    def setpropertyislike(self, parent, propertyname, literal, wildcard='%', singlechar='_', escapechar='\\'):  
        """

        construct a PropertyIsLike

        Parameters
        ----------

        - parent: parent etree.Element object
        - propertyname: the PropertyName
        - literal: the Literal value
        - wildcard: the wildCard character (default is '%')
        - singlechar: the singleChar character (default is '_')
        - escapechar: the escapeChar character (default is '\')

        """

        tmp = etree.SubElement(parent, util.nspath('PropertyIsLike', namespaces['ogc']))
        tmp.set('wildCard', wildcard)
        tmp.set('singleChar', singlechar)
        tmp.set('escapeChar', escapechar)
        etree.SubElement(tmp, util.nspath('PropertyName', namespaces['ogc'])).text = propertyname
        etree.SubElement(tmp, util.nspath('Literal', namespaces['ogc'])).text = literal

    def setsortby(self, parent, propertyname, order='ASC'):
        """

        constructs a SortBy element

        Parameters
        ----------

        - parent: parent etree.Element object
        - propertyname: the PropertyName
        - order: the SortOrder (default is 'ASC')

        """

        tmp = etree.SubElement(parent, util.nspath('SortBy', namespaces['ogc']))
        tmp2 = etree.SubElement(tmp, util.nspath('SortProperty', namespaces['ogc']))
        etree.SubElement(tmp2, util.nspath('PropertyName', namespaces['ogc'])).text = propertyname
        etree.SubElement(tmp2, util.nspath('SortOrder', namespaces['ogc'])).text = order

class FilterCapabilities(object):
    """ Abstraction for Filter_Capabilities """
    def __init__(self, elem):
        # Spatial_Capabilities
        self.spatial_operands = [f.text for f in elem.findall(util.nspath('Spatial_Capabilities/GeometryOperands/GeometryOperand', namespaces['ogc']))]
        self.spatial_operators = []
        for f in elem.findall(util.nspath('Spatial_Capabilities/SpatialOperators/SpatialOperator', namespaces['ogc'])):
            self.spatial_operators.append(f.attrib['name'])

        # Temporal_Capabilities
        self.temporal_operands = [f.text for f in elem.findall(util.nspath('Temporal_Capabilities/TemporalOperands/TemporalOperand', namespaces['ogc']))]
        self.temporal_operators = []
        for f in elem.findall(util.nspath('Temporal_Capabilities/TemporalOperators/TemporalOperator', namespaces['ogc'])):
            self.temporal_operators.append(f.attrib['name'])

        # Scalar_Capabilities
        self.scalar_comparison_operators = [f.text for f in elem.findall(util.nspath('Scalar_Capabilities/ComparisonOperators/ComparisonOperator', namespaces['ogc']))]
