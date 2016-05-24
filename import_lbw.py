__author__ = 'mgiampieri'

# 16/05/24

# creates a vue mesh object at an arbitrary location that serves as a dummy.
# if desired real-world (or Vue) coordinates are known, the objects can be placed there too.
# get_species() allows user to select a plant from a list of all installed LW plants
# Other existing modules can be used to duplicate, move, and scale object, and
# LW is working to write code that replaces object with LW plant object suitable for use in Vue

import os


plants_dir = "C:\Program Files\Laubwerk\Plants/" # location of root LW plant directory
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

    return idx, plants, chosen_dir # this is the number of the plant, the total list of all plant variants found in the directory, and the full path to the plant's dir


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
def select_mesh():
    DeselectAll()
    SelectByType(6) # 6 is an internal vue code for the mesh object type.


# moves an object based on given x,y,z positions
def move_objects(object, new_x, new_y, new_z):
    if IsSelected() == true:
        object.SetPosition(new_x, new_y, new_z)




# if console is not open, this will open it so user can pick from a list of plants
display_console()
# create_mesh will create empty mesh objects and name and place them arbitrarily for now.
create_mesh(num_trees)
# returns chosen plant id, list of plants, and the path to the chosen plant's sub-directory
id, plant_list, plant_path = get_species(plants_dir)
# print plant_list[id] # prints out the chosen plant name
# print plant_path # prints out the full path to the plant's subdirectory