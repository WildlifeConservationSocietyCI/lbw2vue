# 16/05/24

# creates a vue mesh object at an arbitrary location that serves as a dummy.
# if desired real-world (or Vue) coordinates are known, the objects can be placed there too.
# get_species() allows user to select a plant from a list of all installed LW plants
# Other existing modules can be used to duplicate, move, and scale object, and
# LW is working to write code that replaces object with LW plant object suitable for use in Vue

import os, sys, tempfile

# Import laubwerk module after setting the import path accordingly. Not sure why we have to do this, because
# the Laubwerk installer usually sets PYTHONPATH, which should be used automatically.
sys.path.append('C:\Program Files\Laubwerk\Python')
import laubwerk

# import the lbwtoobj helper script
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import lbwtoobj2


plants_dir = "C:\\Program Files\\Laubwerk\\Plants\\" # location of root LW plant directory
num_trees = 10 # specify number of objects to create (for use in create_mesh below)


# display console so user can see list of plant choices
def display_console():
    if DisplayPythonConsole(true) == false:
        DisplayPythonConsole(true)


# very simplistic, but this prints a list of all available plants and allows the user to select one based on an index position
# later on will look into using wxPy to build this out more but this provides basic functionality
def get_species(dir):
    plants = [name for name in os.listdir(dir)
        if os.path.isdir(os.path.join(dir, name))]

    for item in enumerate(plants):
        print "[%d] %s" % item

    try:
        idx = int(raw_input("Enter the plant's number"))
    except ValueError:
        "Unrecognized plant number. Please try again."

    try:
        chosen = plants[idx]
    except IndexError:
        print "Try a number in range."

    chosen_dir = dir+chosen

    return idx, plants, chosen_dir, chosen# this is the number of the plant, the total list of all plant variants found in the directory, the full path to the plant's dir, and plant's scientific name


# create a given number of Vue mesh objects based on provided quantity. They have null geometry but have a position, name, and index position
def create_mesh(num_objects):
    counter = num_objects + 1
    pos = []
    j = 1
    for i in range(counter):
        print i, num_objects
        i = AddMesh()
        name = "placeholder_mesh_"+str(j)
        i.SetName(name)
        i.SetPosition(j*10,j*10,0) # places objects arbitrarily based on order of creation
        pos_i = i.Position()
        print pos_i
        pos.append(pos_i) # writes position to a list for reference
        j += 1
    return pos


# import object- depending on how the LW integration goes, this could be used to import .obj files into Vue and placed either at scene origin or at some other place
def import_object(filepath, pos_x = 0, pos_y = 0, pos_z = 0):
    n = ImportObject(filepath)
    n_pos = n.SetPosition(pos_x, pos_y, pos_z)
    return n_pos


# opens a csv file and reads x,y,z coordinates to a list. It would make sense to pair this with the coordinate translation module from add_camera.py
def open_coord_file(filename):
    with open(filename, "r") as file:
        x_y_z = []
        for line in file:
            pos_x = line.split(",")[0]
            pos_y = line.split(",")[1]
            pos_z = line.split(",")[2]
            x_y_z.append(zip(pos_x,pos_y,pos_z))
    return x_y_z


# selects all mesh objects, deselects all other object types
def select_obj():
    DeselectAll()
    SelectByType(43) # 43 is an internal vue code for this object type.


# moves an object based on given x,y,z positions
def move_objects(object, new_x, new_y, new_z):
    if IsSelected() == true:
        object.SetPosition(new_x, new_y, new_z)




# if console is not open, this will open it so user can pick from a list of plants
display_console()
# create_mesh will create empty mesh objects and name and place them arbitrarily for now.
#create_mesh(num_trees)
# returns chosen plant id, list of plants, and the path to the chosen plant's sub-directory
id, plant_list, plant_path, plant_name = get_species(plants_dir)
# print plant_list[id] # prints out the chosen plant name
# print plant_path # prints out the full path to the plant's subdirectory

# generate the plant master filename
lbwPlantFilename = os.path.join(plant_path, os.path.basename(plant_path) + ".lbw.gz")

# TODO: determine a proper scene scale
scale = 0.01

# create temporary obj and mtl files
tempObjFile = tempfile.NamedTemporaryFile(suffix=".obj", delete=False)
tempMtlFile = tempfile.NamedTemporaryFile(suffix=".mtl", delete=False)
myPlant = laubwerk.load(lbwPlantFilename)
lbwtoobj2.writeObjByHandle(myPlant, myPlant.defaultModel, "summer", tempObjFile, scale, tempMtlFile)

# we need to close the files so Vue can import it
tempObjFile.close()
tempMtlFile.close()

# use Vue's built in import functionality to get the geometry imported
vueObj = ImportObject(tempObjFile.name, -1, False, -1)

#center = (bbox.GetMax() + bbox.GetMin()) * 0.5
#print center

# name plant based on folder name
vueObj.SetName(plant_name)

# In Vue, the default Pivot is apparently always centered. We counteract that by subtracting the position.
vueObj.SetPivotPosition(-vueObj.Position()[0], -vueObj.Position()[1], -vueObj.Position()[2])

# make sure to remove the temporary OBJ file so we don't fill up the hard drive
os.remove(tempObjFile.name)
os.remove(tempMtlFile.name)

# TODO: store the file as a .vob
#result = ExportObject(EONString strFilename, boolean bUseParameterizer = true, EONString dstColorPath = "", EONString dstBumpPath = "", EONString dstAlphaPath = "", EONString srcPreviewPicture = "")


#
# everything below this point are leftovers of a (probably futile) attempt to copy the plant geometry
# directly into a Vue mesh object without having to go through a temporary OBJ file. This can probably
# be removed.
#
if False:

    try:
        # load the laubwerk plant file
        lbwMyPlant = laubwerk.load("C:/Program Files/Laubwerk/Plants/Acer_campestre/Acer_campestre.lbw.gz")
    except IOError:
       print 'Plant file is missing'
       sys.exit(0)

    # pick a specific model from the plant file
    lbwMyModel = lbwMyPlant.defaultModel

    # generate the actual tree geometry
    lbwMyMesh = lbwMyModel.getMesh(qualifierName="summer", maxBranchLevel=3, minThickness=0.3, leafAmount=1.0, leafDensity=1.0, maxSubDivLevel=1)



    vueMesh = AddMesh()
    vueMesh.SetName(lbwMyPlant.name)
    vueMesh.SetPosition(0, 0, 0) # place object at the origin


    #while len(points)%3 != 0:
    #   points.append((0.0, 0.0, 0.0))

    # copy points and rearrange y and z coordinates along the way
    # we have to make a copy, because tuples don't allow reassignments
    points = []
    for point in lbwMyMesh.points:
        points.append((point[0], point[2], -point[1]))

    print len(points)

    #vertices = [(0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (0.0, 10.0, 0.0), (0.0, 0.0, 10.0), (10.0, 0.0, 10.0), (0.0, 10.0, 10.0)]
    vueMesh.SetTriangleVertices(points, False)


    vertexIndices = []
    for polygon in lbwMyMesh.polygons:
        if len(polygon) == 3:
            vertexIndices.append((polygon[0], polygon[1], polygon[2]))
        elif len(polygon) == 4:
            vertexIndices.append((polygon[0], polygon[1], polygon[2]))
            vertexIndices.append((polygon[2], polygon[3], polygon[0]))
        else:
            # TODO: We would need to implement a real triangulation to get this right
            print "Polygon with more than four vertices encountered and ignored"

    vertexIndices = vertexIndices[vueMesh.CountMeshFaces():]
    vueMesh.SetMeshFaceVertexIndices(vertexIndices)


    print vueMesh.CountMeshVertices()


"""
    vertexList = vueMesh.MeshFaceVertexIndices()
    vertexList.append((0.0, 0.0, 0.0))
    vertexList.append((10.0, 0.0, 0.0))
    vertexList.append((0.0, 10.0, 0.0))
    vertexList.append((0.0, 0.0, 10.0))
    vertexList.append((10.0, 0.0, 10.0))
    vertexList.append((0.0, 10.0, 10.0))
    print len(vertexList)
    """
"""
    vueMesh.SetMeshVertices([(0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (0.0, 10.0, 0.0), (0.0, 0.0, 10.0), (10.0, 0.0, 10.0), (0.0, 10.0, 10.0)])
    vueMesh.SetMeshFaceVertexIndices([(0, 1, 2), (3, 4, 5)])
    print vueMesh.CountMeshVertices()
    """

"""
    vueMesh.SetMeshVertices([(0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (0.0, 10.0, 0.0)])
    vueMesh.SetMeshFaceVertexIndices([(0, 1, 2)])
"""