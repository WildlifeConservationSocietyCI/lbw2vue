#
# Loads a plant model, creates the geometry and stores it in obj format according to this
# documentation:
# http://paulbourke.net/dataformats/obj/
# http://paulbourke.net/dataformats/mtl/
# This example intentionally doesn't do a lot of error checking, as it's meant to be minimal and
# clearly only serve as a basic example of how to use the laubwerk module.
#
# Copyright Laubwerk GmbH
#

import sys, argparse, glob, os, laubwerk


def linearToSrgb(color):
	"""Convert a color from linear to sRGB
	"""
	retCol = [0, 0, 0]
	for i in range(3):
		if color[i] > 0.0031308:
		    retCol[i] = 1.055 * (pow(color[i], (1.0 / 2.4))) - 0.055;
		else:
		    retCol[i] = 12.92 * color[i];

	return retCol

def writeObjByHandle(plant, model, qualifier, objfile, scale = 1.0, mtlfile=None):
	# generate the actual model geometry with default quality settings and the default (season) qualifier
	# a list of valid qualifiers can be retrieved through plant.qualifiers
	mesh = model.getMesh(qualifier)

	objfile.write("# obj file written by laubwerk python example\n")


	# do an initial run through the mesh to determine the used materials
	matidSet = set()
	for matid in mesh.matids:
		matidSet.add(matid)

	if mtlfile:
		objfile.write('mtllib ' + mtlfile.name + '\n')

	if len(mesh.name) > 0:
		objfile.write("o " + mesh.name + "\n")
	else:
		objfile.write("o mesh\n")

	# write vertices
	for point in mesh.points:
		objfile.write("v " + str(point[0] * scale) + " " + str(point[1] * scale) + " " + str(point[2] * scale) + "\n")
		
	objfile.write("\n")

	# write texture vertices
	for uv in mesh.uvs:
		objfile.write("vt " + str(uv[0]) + " " + str(1.0 - uv[1]) + " 0\n")
		
	objfile.write("\n")

	# write vertex normals
	for normal in mesh.normals:
		objfile.write("vn " + str(normal[0]) + " " + str(normal[1]) + " " + str(normal[2]) + "\n")

	objfile.write("\n")

	# write polygons in format f v/vt/vn v/vt/vn v/vt/vn v/vt/vn
	# reorder the faces in material groups
	for matid in matidSet:
		# find and specify material
		materialName = ""
		for material in plant.materials:
			if material.matid == matid:
				if mtlfile:
					objfile.write('usemtl ' + material.name + '\n')
				objfile.write('g ' + material.name + '\n')
				materialName = material.name
				break

		nFaces = 0
		for polygon, texverts, polyMatid in zip(mesh.polygons, mesh.texverts, mesh.matids):
			if polyMatid == matid:
				objfile.write("f")
				for idx, texidx in zip(polygon, texverts):
					objfile.write(" " + str(idx+1) + "/" + str(texidx+1) + "/" + str(idx+1))
				objfile.write("\n")
				nFaces = nFaces + 1

		#print str(matid) + ' ' + materialName + ' ' + str(nFaces)

		
	if mtlfile:
		# write mtl file
		mtlfile.write("# mtl file written by laubwerk python example\n")

		for material, i in zip(plant.materials, range(len(plant.materials))):
			if material.matid in matidSet:
				#print material.name

				mtlfile.write('newmtl ' + material.name + '\n')

				mtlFront = material.getFront()
				myKd = linearToSrgb(mtlFront.diffuseColor)
				mtlfile.write('\tKd ' + str(myKd[0]) + ' '  + str(myKd[1]) + ' ' + str(myKd[2]) + '\n')
				mtlfile.write('\tNi 1.3333\n') # ior
				if len(mtlFront.diffuseTexture):
					mtlfile.write('\tmap_Kd ' + mtlFront.diffuseTexture + '\n')
				if len(mtlFront.bumpTexture) > 0:
					mtlfile.write('\tbump ' + mtlFront.bumpTexture + '\n')
				if len(material.alphaTexture) > 0:
					atsplit = os.path.splitext(material.alphaTexture)
					mtlfile.write('\tmap_d ' + atsplit[0] + '_a' + atsplit[1] + '\n')
				#if len(material.alphaTexture) > 0:
				#	mtlfile.write('\tmap_Tf ' + os.path.basename(material.alphaTexture) + '\n')


def writeObjByName(plant, model, qualifier, objFileName, scale=1.0, mtlFileName=None):

	objfile = open(objFileName, "w")

	mtlfile = None
	if mtlFileName:
		mtlfile = open(mtlFileName, "w")

	writeObjByHandle(plant, model, qualifier, objfile, scale, mtlfile)



def main():
	#
	# prepare command line arguments
	#
	argParse = argparse.ArgumentParser(description='Convert LBW file(s) to OBJ.')
	argParse.add_argument('inPath', metavar='path', type=str, nargs=1, help='The path or filename to convert (accepts wildcards).')
	argParse.add_argument('--qualifier', '-q', dest='qualifier', default='all', type=str, help='The qualifier name to use, accepts wildcards. If not specified or special keyword "all" is used, all qualifiers get exported. The special keyword "default" will cause the default qualifier to be used.')
	argParse.add_argument('--model', '-m', type=str, dest='model', default='all', help='The name of the model to export. If not specified or special keyword "all" is used all models get exported. The special keyword "default" will export only the default model.')
	argParse.add_argument('--scale', '-s', type=float, dest='scale', default=1.0, help='A scale multiplier to use when writing the vertices of the OBJ file.')
	#argParse.add_argument('--info', '-i', type)

	#
	# process command line arguments
	#
	args = argParse.parse_args()

	#
	# find the file(s) to export
	#
	inFileList = glob.glob(args.inPath[0])

	#
	# iterate through all input files
	#
	for inFile in inFileList:
		inFileBase = os.path.basename(inFile)
		print 'Exporting ' + inFileBase + '...'

		# load the plant model
		plant = laubwerk.load(inFile)

		# pick the default model in the plant file (all models can be accessed through plant.models)
		#model = plant.defaultModel
		for model in plant.models:

			if not args.model == 'all' and model.name != args.model and not (args.model == 'default' and model == plant.defaultModel):
				continue

			print '\t' + model.name + '...'

			# run through the available qualifiers
			for qualifier in model.qualifiers:

				if not args.qualifier == 'all' and qualifier != args.qualifier and not (args.qualifier == 'default' and qualifier == model.defaultQualifier):
					continue

				print '\t\t' + qualifier + '...'

				objFileName = inFileBase
				while not os.path.splitext(objFileName)[1] == '':
					objFileName = os.path.splitext(objFileName)[0]
				objFileName = objFileName + '_' + model.name + '_' + qualifier + '.obj'
				mtlFileName = os.path.splitext(objFileName)[0] + '.mtl'
				writeObjByName(plant, model, qualifier, objFileName, args.scale, mtlFileName)
		


if __name__ == "__main__":
    main()