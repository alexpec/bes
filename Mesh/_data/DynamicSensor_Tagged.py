# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v7.8.0 with dump python functionality
###

import sys
import salome
import math

salome.salome_init()
theStudy = salome.myStudy

#Adding Data Path
data_path = %%%systemParameter_data_path%%%


import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, data_path)


def CalculateElipsePoint(a, b, x):
	val = b * math.sqrt(1.0 - math.pow(x/a,2.0))
	return val

####################################################
##       Begin of NoteBook variables section      ##
####################################################
#Independent Parameters
'''
notebook.set("b", 9)
notebook.set("BarrelCenterline", 15)
notebook.set("BarrelRadius", 5)
notebook.set("VoidCenterline", 20)
notebook.set("VoidRadius", 4)
notebook.set("HeadTotalPoints", 10)
notebook.set("CalorimeterRadius", 2.5)
notebook.set("WarheadCenterline", "b")
notebook.set("a", "VoidRadius + BarrelRadius")
notebook.set("CalorimeterCenterline", "b + BarrelCenterline - VoidCenterline")
'''

b = %%%geometricParam_b%%% #9.0
BarrelCenterline = %%%geometricParam_BarrelCenterline%%%#15.0
BarrelRadius = %%%geometricParam_BarrelRadius%%%#5.0
VoidCenterline = %%%geometricParam_VoidCenterline%%%#20.0
VoidRadius = %%%geometricParam_VoidRadius%%%#4.0

#Constant
CalorimeterRadius = 2.5
HeadTotalPoints = 30

#Dependent Parameters
WarheadCenterline = b
a = VoidRadius + BarrelRadius
CalorimeterCenterline = b + BarrelCenterline - VoidCenterline


####################################################
##        End of NoteBook variables section       ##
####################################################
###
### GEOM component
###

#Salome Imports
import GEOM
from salome.geom import geomBuilder
import SALOMEDS

#Other Imports
import math
import numpy

geompy = geomBuilder.New(theStudy)

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

#Creating Barrel
Barrel = geompy.MakeFaceHW(BarrelCenterline, BarrelRadius, 2)
geompy.TranslateDXDYDZ(Barrel, 0, BarrelRadius/2.0 + VoidRadius, BarrelCenterline/2)

#Creating Head Sketch
geomObj_2 = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)
sk = geompy.Sketcher2D()
sk.addPoint(0.000000, 0.000000)

#Adding first point at the end of the calorimeter (x = 2.5 - calorimeter radius is constant)
sk.addSegmentAbsolute(0.000000, b)

points = numpy.linspace(0, a, HeadTotalPoints)
points_ref = []

for idx, i in enumerate(points):
	if i == 0: continue 
	y_point = CalculateElipsePoint(a, b, i)
	pp = geompy.MakeVertex(0.0, i, y_point)
	points_ref.append(pp)
	#print "Elipsoid points (%.2f, %.2f)" %(i, y_point)
	sk.addSegmentAbsolute(i, y_point)

#Closing Sketch
sk.close()


Head_sketch = sk.wire(geomObj_2)
geompy.Rotate(Head_sketch, OX, 90*math.pi/180.0)
geompy.Rotate(Head_sketch, OZ, 90*math.pi/180.0)

Head = geompy.MakeFaceWires([Head_sketch], 1)
geompy.TranslateDXDYDZ(Head, 0, 0, BarrelCenterline)

########################################
#Code to get the edges in the warhead
########################################
#edge_obj = geompy.GetEdgeNearPoint(Head, points_ref[1])
#edge_id = geompy.GetSubShapeID(Head, edge_obj)
#import pdb; pdb.set_trace()


Void = geompy.MakeFaceHW(VoidCenterline, VoidRadius, 2)
geompy.TranslateDXDYDZ(Void, 0, VoidRadius/2, VoidCenterline/2)

Calorimeter_Brute = geompy.MakeFaceHW(CalorimeterCenterline, CalorimeterRadius, 2)
geompy.TranslateDXDYDZ(Calorimeter_Brute, 0, CalorimeterRadius/2, VoidCenterline + CalorimeterCenterline/2)

Calorimeter = geompy.MakeCommonList([Head, Calorimeter_Brute], True)


Head_CutCalorimeter = geompy.MakeCutList(Head, [Calorimeter], True)

Warhead = geompy.MakeCutList(Head_CutCalorimeter, [Void], True)

Compound_1 = geompy.MakeCompound([Barrel, Void, Calorimeter, Warhead])

Sensor = geompy.Sew(Compound_1, 1e-07)

#Creating Groups of Faces
Calorimeter_1 = geompy.CreateGroup(Sensor, geompy.ShapeType["FACE"])
geompy.UnionIDs(Calorimeter_1, [23])

Warhead_1 = geompy.CreateGroup(Sensor, geompy.ShapeType["FACE"])
geompy.UnionIDs(Warhead_1, [46])

Barrel_1 = geompy.CreateGroup(Sensor, geompy.ShapeType["FACE"])
geompy.UnionIDs(Barrel_1, [2])

Air = geompy.CreateGroup(Sensor, geompy.ShapeType["FACE"])
geompy.UnionIDs(Air, [12])


#Creadting Groups of Edges
AirBottomLine = geompy.CreateGroup(Sensor, geompy.ShapeType["EDGE"])
geompy.UnionIDs(AirBottomLine, [14])

BarrelBottomLine = geompy.CreateGroup(Sensor, geompy.ShapeType["EDGE"])
geompy.UnionIDs(BarrelBottomLine, [4])

ExtLine = geompy.CreateGroup(Sensor, geompy.ShapeType["EDGE"])
geompy.UnionIDs(ExtLine, [52, 84, 78, 68, 62, 50, 80, 74, 64, 48, 58, 86, 76, 70, 60, 54, 88, 82, 72, 66, 56, 7])

CalorimeterLine = geompy.CreateGroup(Sensor, geompy.ShapeType["EDGE"])
geompy.UnionIDs(CalorimeterLine, [41, 39, 35, 31, 37, 33, 29, 27])

#Adding Geometry to Study
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Calorimeter, 'Calorimeter' )
geompy.addToStudy( Barrel, 'Barrel' )
geompy.addToStudy( Head_sketch, 'Head_sketch' )
geompy.addToStudy( Head, 'Head' )
geompy.addToStudy( Void, 'Void' )
geompy.addToStudy( Head_CutCalorimeter, 'Head_CutCalorimeter' )
geompy.addToStudy( Warhead, 'Warhead' )
geompy.addToStudy( Compound_1, 'Compound_1' )
geompy.addToStudy( Sensor, 'Sensor' )

#Adding Face Groups to Study
geompy.addToStudyInFather( Sensor, Calorimeter_1, 'Calorimeter' )
geompy.addToStudyInFather( Sensor, Warhead_1, 'Warhead' )
geompy.addToStudyInFather( Sensor, Barrel_1, 'Barrel' )
geompy.addToStudyInFather( Sensor, Air, 'Air' )

#Adding Edges Groups to Study
geompy.addToStudyInFather( Sensor, AirBottomLine, 'AirBottomLine' )
geompy.addToStudyInFather( Sensor, BarrelBottomLine, 'BarrelBottomLine' )
geompy.addToStudyInFather( Sensor, ExtLine, 'ExtLine' )
geompy.addToStudyInFather( Sensor, CalorimeterLine, 'CalorimeterLine' )

#################################################################################
# CREATING THE MESH
#################################################################################


###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
Mesh_1 = smesh.Mesh(Sensor)
GMSH_2D = Mesh_1.Triangle(algo=smeshBuilder.GMSH_2D)
Gmsh_Parameters = GMSH_2D.Parameters()
Gmsh_Parameters.SetMinSize( 0 )
Gmsh_Parameters.Set2DAlgo( 4 )
Gmsh_Parameters.SetRecombineAll( 1 )
Gmsh_Parameters.SetSubdivAlgo( 1 )
Gmsh_Parameters.SetRemeshAlgo( 1 )
Gmsh_Parameters.SetSmouthSteps( 2 )
Gmsh_Parameters.SetMaxSize( 0.5 )
Gmsh_Parameters.SetIs2d( 1 )
isDone = Mesh_1.Compute()

#Creating Groups From Geometry
Calorimeter_2 = Mesh_1.GroupOnGeom(Calorimeter_1,'Calorimeter',SMESH.FACE)
Warhead_2 = Mesh_1.GroupOnGeom(Warhead_1,'Warhead',SMESH.FACE)
Barrel_2 = Mesh_1.GroupOnGeom(Barrel_1,'Barrel',SMESH.FACE)
Air_1 = Mesh_1.GroupOnGeom(Air,'Air',SMESH.FACE)
AirBottomLine_1 = Mesh_1.GroupOnGeom(AirBottomLine,'AirBottomLine',SMESH.EDGE)
BarrelBottomLine_1 = Mesh_1.GroupOnGeom(BarrelBottomLine,'BarrelBottomLine',SMESH.EDGE)
ExtLine_1 = Mesh_1.GroupOnGeom(ExtLine,'ExtLine',SMESH.EDGE)
CalorimeterLine_1 = Mesh_1.GroupOnGeom(CalorimeterLine,'CalorimeterLine',SMESH.EDGE)

#Reorienting Inverse Face
Mesh_1.Reorient2D(Warhead_2,[ 1, 0, 0 ],[ 0, 0, 0 ])

#Rotating Mesh
[ Calorimeter_rotated, Warhead_rotated, Barrel_rotated, Air_rotated, AirBottomLine_rotated, BarrelBottomLine_rotated, ExtLine_rotated, CalorimeterLine_rotated, Calorimeter_top, Warhead_top, Barrel_top, Air_top, AirBottomLine_top, BarrelBottomLine_top, ExtLine_top, CalorimeterLine_top ] = Mesh_1.RotationSweepObjects( [ Mesh_1 ], [ Mesh_1 ], [ Mesh_1 ], SMESH.AxisStruct( 0, 0, 0, 0, 0, 1 ), 0.0785398, 1, 1e-05, 1 )

#Removing the Edges To Export to UNV
Mesh_1.RemoveGroup( CalorimeterLine_top )
Mesh_1.RemoveGroup( ExtLine_top )
Mesh_1.RemoveGroup( BarrelBottomLine_top )
Mesh_1.RemoveGroup( AirBottomLine_top )
Mesh_1.RemoveGroup( AirBottomLine_1 )
Mesh_1.RemoveGroup( BarrelBottomLine_1 )
Mesh_1.RemoveGroup( ExtLine_1 )
Mesh_1.RemoveGroup( CalorimeterLine_1 )

aStudyBuilder = theStudy.NewBuilder()
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(CalorimeterLine_top))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(ExtLine_top))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(BarrelBottomLine_top))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(AirBottomLine_top))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(AirBottomLine_1))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(BarrelBottomLine_1))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(ExtLine_1))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(CalorimeterLine_1))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)

## Set names of Mesh objects
smesh.SetName(GMSH_2D.GetAlgorithm(), 'GMSH_2D')
smesh.SetName(Air_top, 'Air_top')
smesh.SetName(AirBottomLine_rotated, 'AirBottomLine_rotated')
smesh.SetName(Gmsh_Parameters, 'Gmsh Parameters')
smesh.SetName(Calorimeter_2, 'Calorimeter')
smesh.SetName(Warhead_2, 'Warhead')
smesh.SetName(Barrel_2, 'Barrel')
smesh.SetName(Air_1, 'Air')
smesh.SetName(Calorimeter_top, 'Calorimeter_top')
smesh.SetName(Warhead_top, 'Warhead_top')
smesh.SetName(Barrel_top, 'Barrel_top')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(ExtLine_rotated, 'ExtLine_rotated')
smesh.SetName(BarrelBottomLine_rotated, 'BarrelBottomLine_rotated')
smesh.SetName(CalorimeterLine_rotated, 'CalorimeterLine_rotated')
smesh.SetName(Air_rotated, 'Air_rotated')
smesh.SetName(Barrel_rotated, 'Barrel_rotated')
smesh.SetName(Warhead_rotated, 'Warhead_rotated')
smesh.SetName(Calorimeter_rotated, 'Calorimeter_rotated')
'''
smesh.SetName(CalorimeterLine_1, 'CalorimeterLine')
smesh.SetName(CalorimeterLine_top, 'CalorimeterLine_top')
smesh.SetName(ExtLine_1, 'ExtLine')
smesh.SetName(ExtLine_top, 'ExtLine_top')
smesh.SetName(AirBottomLine_1, 'AirBottomLine')
smesh.SetName(AirBottomLine_top, 'AirBottomLine_top')
smesh.SetName(BarrelBottomLine_1, 'BarrelBottomLine')
smesh.SetName(BarrelBottomLine_top, 'BarrelBottomLine_top')
'''
Mesh_1.ExportUNV(data_path + "/" + %%%systemParameter_UNV_MeshName%%%)

#THE PRINT BELOW MUST BE ADDED IN ORDER TO NOT HOLD THE SUBPROCESS
print "Process Finished!"


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
