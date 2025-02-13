"""
Checks validity of cubes configuration.
Validation according to https://puzzling.stackexchange.com/questions/53846/how-to-determine-whether-a-rubiks-cube-is-solvable
and algebra paper.
NOTE: The above mentioned properties only ensure validity if the rubiks cube has been permuted. They do not guarantee validity if some of the cubelets are invalid. This is the case when:
    - There are duplicate cubelets
    - A cubelet has duplicate colors (not possible in our case)

    We also check the orientation of the whole cube by checking the colors of the center cubes.
"""
import utils
import stash
from ursina import *

def check_edges():
    edge_count = 0

    for index, cube in enumerate(stash.CUBES):
        for color_cubelet in cube.children:
            world_position = round(color_cubelet.world_position, 1)
            first_cube_pos = utils.find_cube([index, "rg"])
            second_cube_pos = utils.find_cube([index, "rb"])
            third_cube_pos = utils.find_cube([index, "og"])
            fourth_cube_pos = utils.find_cube([index, "ob"])

            if utils.get_color_cubelet_name(world_position[0], world_position[1], world_position[2]) in stash.EDGE_VALIDATION_POSITIONS:
                if color_cubelet.name == "o" or color_cubelet.name == "r":
                    edge_count += 1
                if color_cubelet.name == "g" or color_cubelet.name == "b" and not (first_cube_pos == index or second_cube_pos == index or third_cube_pos == index or fourth_cube_pos == index):
                    edge_count += 1

    return edge_count % 2 == 0

def check_duplicates():
    outer_colors = []

    for index, cube in enumerate(stash.CUBES):
        outer_colors.append(utils.get_orientation(cube, index))

    for index_one, outer_color_one in enumerate(outer_colors):
        for index_two, outer_color_two in enumerate(outer_colors):
            if set(outer_color_one) == set(outer_color_two) and index_one != index_two:
                return False

    return True

def check_middle_pieces():
    middle_pieces_indices = [8,10,12,14,16,25]
    colors = []
    correct = []

    for index, cube in enumerate(stash.CUBES):
        for color_cube in cube.children:
            world_position = round(color_cube.world_position, 1)

            for side in stash.SIDES_BY_COLOR.values():
                if utils.get_color_cubelet_name(world_position[0], world_position[1], world_position[2]) in side:
                    colors.append(color_cube.name)

        if index == 8:
            if colors[0] == "b":
                correct.append("b")
            else:
                correct.append(" ")
        elif index == 10:
            if colors[0] == "r":
                correct.append("r")
            else:
                correct.append(" ")
        elif index == 12:
            if colors[0] == "y":
                correct.append("y")
            else:
                correct.append(" ")
        elif index == 14:
            if colors[0] == "o":
                correct.append("o")
            else:
                correct.append(" ")
        elif index == 16:
            if colors[0] == "w":
                correct.append("w")
            else:
                correct.append(" ")
        elif index == 25:
            if colors[0] == "g":
                correct.append("g")
            else:
                correct.append(" ")

        colors = []

    return correct == ["b", "r", "y", "o", "w", "g"]

def check_corners():
    corner_count = 0

    for index, cube in enumerate(stash.CUBES):
        if index in stash.CORNER_ORIENTATIONS_CLOCKWISEUP["top"]:
            orientation = utils.get_orientation(cube, index)
        elif index in stash.CORNER_ORIENTATIONS_CLOCKWISEUP["bottom"]:
            orientation = utils.get_orientation(cube, index)
        elif index in stash.CORNER_ORIENTATIONS_COUNTERCLOCKWISEUP["top"]:
            orientation = utils.get_orientation(cube, index)
        elif index in stash.CORNER_ORIENTATIONS_COUNTERCLOCKWISEUP["bottom"]:
            orientation = utils.get_orientation(cube, index)
        if orientation[1] == "r" or orientation[1] == "o":
            corner_count += 1
        if orientation[2] == "r" or orientation[2] == "o":
            corner_count += -1

    return corner_count % 3 == 0

def check_permutation_parity():
    swap_count = 0
    for index, cube in enumerate(stash.CUBES):
        config = stash.ALL_CUBE_CONFIGS[index]
        pos = utils.find_cube(config)

        if pos != index:
            swap_count += 1

    return swap_count % 2 == 0

def validate_config():
    edges_valid = check_edges()
    corners_valid = check_corners()
    parity_valid = check_permutation_parity()
    middle_pieces_valid = check_middle_pieces()
    no_duplicates_valid = check_duplicates()
    print("EDGES VALID?", edges_valid)
    print("CORNERS VALID?", corners_valid)
    print("PARITY VALID?", parity_valid)
    print("MIDDLE PIECES VALID?", middle_pieces_valid)
    print("NO DUPLICATES VALID?", no_duplicates_valid)

    return edges_valid and corners_valid and parity_valid and middle_pieces_valid and no_duplicates_valid
