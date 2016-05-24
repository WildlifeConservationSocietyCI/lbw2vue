#
# Loads a plant model, creates the geometry and stores it in obj format according to this
# documentation: http://paulbourke.net/dataformats/obj/
# This example intentionally doesn't do a lot of error checking, as it's meant to be minimal and
# clearly only serve as a basic example of how to use the laubwerk module.
#
# Copyright Laubwerk GmbH
#

import sys, laubwerk

def main():
	# check for the command line arguments to be present
	if len(sys.argv) < 2:
	    print 'Please provide the path to a Laubwerk plant file as command line argument\n'
	    print 'Example:\n'
	    print 'lbwtoobj.py C:\Program Files\Laubwerk\Plants\Acer_campestre\Acer_campestre.lbw.gz\n'
	    sys.exit()

	objfile = open("Acer_campestre.obj", "w")
	lbwToObj(sys.argv[1], objfile)


def lbwToObj(lbwfile, objfile):
	""" Load an LBW file and write it into a file-like object in OBJ format
	"""

	# load the plant model
	plant = laubwerk.load(lbwfile)

	# pick the default model in the plant file (all models can be accessed through plant.models)
	model = plant.defaultModel

	# generate the actual model geometry with default quality settings and the default (season) qualifier
	# a list of valid qualifiers can be retrieved through plant.qualifiers
	mesh = model.getMesh(model.defaultQualifier)

	objfile.write("# obj file written by laubwerk python example\n")
	if len(mesh.name) > 0:
		objfile.write("o " + mesh.name + "\n")
	else:
		objfile.write("o mesh\n")

	# write vertices
	for point in mesh.points:
		objfile.write("v " + str(point[0]) + " " + str(point[1]) + " " + str(point[2]) + "\n")
		
	objfile.write("\n")

	# write texture vertices
	for uv in mesh.uvs:
		objfile.write("vt " + str(uv[0]) + " " + str(uv[1]) + " 0\n")
		
	objfile.write("\n")

	# write vertex normals
	for normal in mesh.normals:
		objfile.write("vn " + str(normal[0]) + " " + str(normal[1]) + " " + str(normal[2]) + "\n")

	objfile.write("\n")

	# write polygons in format f v/vt/vn v/vt/vn v/vt/vn v/vt/vn
	for polygon, texverts in zip(mesh.polygons, mesh.texverts):
		objfile.write("f")
		for idx, texidx in zip(polygon, texverts):
			objfile.write(" " + str(idx+1) + "/" + str(texidx+1) + "/" + str(idx+1))
		objfile.write("\n")


if __name__ == "__main__":
    main()