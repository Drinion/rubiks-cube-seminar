"""
Module for utility functions.
"""
import stash
import random
from ursina import *

def get_color_cubelet_name(a,b,c): return str(formatNumber(a)) + str(formatNumber(b)) + str(formatNumber(c))

def formatNumber(num):
    if num % 1 == 0:
        return int(num)
    else:
        if num > -0.5 and num < 0:
            num = -0.5
        elif num < -0.5 and num > -1:
            num = -1
        elif num < -1 and num > -1.5:
            num = -1.5
        elif num < 0.5 and num > 0:
            num = 0.5
        elif num > 0.5 and num < 1:
            num = 1
        elif num > 1 and num < 1.5:
            num = 1.5
        return num

def prepareEntity(parent):
    color_positions = [["r", Vec3(0,0,-0.5)], ["b", Vec3(0,0.5,0)], ["w", Vec3(-0.5,0,0)], ["y", Vec3(0.5,0,0)],["g", Vec3(0,-0.5,0)],["o", Vec3(0,0,0.5)]]

    for color_position in color_positions:
        color_cube = Entity(name=color_position[0], parent=parent, model="cube", color=color.clear, scale=0.1, position=color_position[1])

def find_cube(cube_conf):
    required_colors = list(cube_conf[1])

    for index, cube in enumerate(stash.CUBES):
        if index in stash.EDGE_INDICES:
            outer = []

            for color in required_colors:
                for color_cubelet in cube.children:
                    if color_cubelet.name == color:
                        for side in stash.OUTER_SIDES.values():
                            world_position = round(color_cubelet.world_position, 1)

                            if get_color_cubelet_name(world_position[0], world_position[1], world_position[2]) in side:
                                outer.append(True)

            if all(iter(outer)) and len(outer) == len(required_colors):
                for val_index, value in enumerate(stash.LABELS.values()):
                    if value == cube.name.split("_")[0]:
                        cube_rot_name = cube.name.split("_")[1]

                        return val_index, cube_rot_name

    for index, cube in enumerate(stash.CUBES):
        if index not in stash.EDGE_INDICES:
            outer = []

            for color in required_colors:
                for color_cubelet in cube.children:
                    if color_cubelet.name == color:
                        for side in stash.OUTER_SIDES.values():
                            world_position = round(color_cubelet.world_position, 1)

                            if get_color_cubelet_name(world_position[0], world_position[1], world_position[2]) in side:
                                outer.append(True)

            if all(iter(outer)) and len(outer) == len(required_colors):
                for val_index, value in enumerate(stash.LABELS.values()):
                    if value == cube.name.split("_")[0]:
                        cube_rot_name = cube.name.split("_")[1]

                        return val_index, cube_rot_name

def in_position(cube_config, name):
    if cube_config[1] != "skip":
        first_color = list(cube_config[1])[0]
        second_color = list(cube_config[1])[1]
    else:
        return "Color is Null"

    for cube in stash.CUBES:
        if cube.name.split("_")[1] == name:
            flippy_cube = cube

    first_side = stash.SIDES_BY_COLOR[first_color]
    second_side = stash.SIDES_BY_COLOR[second_color]
    outer = []

    for color_cube in flippy_cube.children:
        world_position = round(color_cube.world_position, 1)

        if color_cube.name == first_color:
            if get_color_cubelet_name(world_position[0], world_position[1], world_position[2]) in first_side:
                outer.append("First")

    for color_cube in flippy_cube.children:
        world_position = round(color_cube.world_position, 1)

        if color_cube.name == second_color:
            if get_color_cubelet_name(world_position[0], world_position[1], world_position[2]) in second_side:
                outer.append("Second")

    if len(list(cube_config[1])) == 3:
        third_color = list(cube_config[1])[2]
        third_side = stash.SIDES_BY_COLOR[third_color]

        for color_cube in flippy_cube.children:
            world_position = round(color_cube.world_position, 1)

            if color_cube.name == third_color:
                if get_color_cubelet_name(world_position[0], world_position[1], world_position[2]) in third_side:
                    outer.append("Third")

        return outer == ["First", "Second", "Third"]

    return outer == ["First", "Second"]

def check_second_layer():
    found = []

    for conf in stash.SECOND_LAYER_CONFS:
        pos, name = find_cube(conf)
        if in_position(conf, name):
            found.append(conf[0])

    return found == [1,5,18,22]

def check_yellow_cross():
    yellow_positions = ["1.510","1.501","1.5-10","1.50-1"]
    in_position = []

    for position in yellow_positions:
        for index, cube in enumerate(stash.CUBES):
            if cube.name.split("_")[0] in stash.SIDES["a"]:
                for color_cubelet in cube.children:
                    color_name = color_cubelet.name.split("_")[0]
                    world_position = round(color_cubelet.world_position, 1)

                    if get_color_cubelet_name(world_position[0], world_position[1], world_position[2]) == position and color_name == "y":
                        in_position.append(True)
                    elif get_color_cubelet_name(world_position[0], world_position[1], world_position[2]) == position and color_name != "y":
                        in_position.append(False)

    if in_position == [True, True, False, False]:
        shape = "ur" # Upper Right L shape
    elif in_position == [False, True, True, False]:
        shape = "lr" # Lower Right L shape
    elif in_position == [False, False, True, True]:
        shape = "ll" # Lower left L shape
    elif in_position == [True, False, False, True]:
        shape = "ul" # Upper left L shape
    elif in_position == [False, False, False, False]:
        shape = "dot" # Dot
    elif in_position == [True, False, True, False]:
        shape = "lv" # Line vertical
    elif in_position == [False, True, False, True]:
        shape = "lh" # Line horizontal
    else:
        shape = "cross"

    return all(iter(in_position)), shape

def check_yellow_edges():
    color_positions = ["11.50","101.5","1-1.50","10-1.5"]
    cube_names = ""

    for position in color_positions:
        for cube in stash.CUBES:
            if cube.name.split("_")[0] in stash.SIDES["a"]:
                for color_cube in cube.children:
                    color_name = color_cube.name.split("_")[0]
                    world_position = round(color_cube.world_position, 1)

                    if get_color_cubelet_name(world_position[0], world_position[1], world_position[2]) == position:
                        cube_names += color_name

    return cube_names.upper()

def yellow_corners_in_position():
    cube_configs = [[2, "byr"], [4, "boy"], [19, "ygr"], [21, "ogy"]]
    cube_names = []
    positions_state = []

    for index, config in enumerate(cube_configs):
        pos, name = find_cube(config)
        if pos == config[0]:
            positions_state.append(True)
        else:
            positions_state.append(False)

    correct_cube_index = next((i for i, j in enumerate(positions_state) if j), 4)

    return all(iter(positions_state)), correct_cube_index

def get_yellow_corner_orientation(cube):
    color_positions = ["1.51-1","1.511","1.5-1-1","1.5-11"]
    disoriented = 5

    for color_cube in cube.children:
        world_position = round(color_cube.world_position, 1)

        for index, position in enumerate(color_positions):
            if get_color_cubelet_name(world_position[0], world_position[1], world_position[2]) in position and not color_cube.name.split("_")[0] == "y":
                disoriented = index

    return disoriented

def get_orientation(cube, index):
    outer = []

    for color_cube in cube.children:
        world_position = round(color_cube.world_position, 1)

        for side in stash.SIDES_BY_COLOR.values():
            if get_color_cubelet_name(world_position[0], world_position[1], world_position[2]) in side:
                outer.append(color_cube.name)

    if index == 0:
        outer[0], outer[1], outer[2] = outer[0], outer[2], outer[1]
    elif index == 2:
        outer[0], outer[1], outer[2] = outer[0], outer[1], outer[2]
    elif index == 4:
        outer[0], outer[1], outer[2] = outer[2], outer[1], outer[0]
    elif index == 6:
        outer[0], outer[1], outer[2] = outer[2], outer[0], outer[1]
    elif index == 17:
        outer[0], outer[1], outer[2] = outer[0], outer[2], outer[1]
    elif index == 19:
        outer[0], outer[1], outer[2] = outer[0], outer[1], outer[2]
    elif index == 21:
        outer[0], outer[2] = outer[2], outer[0]
    elif index == 23:
        outer[0], outer[1], outer[2] = outer[2], outer[0], outer[1]

    return outer

def yellow_corners_oriented():
    cube_configs = [[2, "byr"], [4, "boy"], [19, "ygr"], [21, "ogy"]]
    cube_names = []
    positions_state = []
    desoriented = 0
    corner_state = 0
    corner_orientation = []

    for config_index, config in enumerate(cube_configs):
        for cube_index, cube in enumerate(stash.CUBES):
            if cube.name.split("_")[0] == stash.YELLOW_CORNER_POSITIONS[config_index]:
                desoriented = get_yellow_corner_orientation(cube)
                corner_orientation.append(get_orientation(cube, config[0]))

        positions_state.append(desoriented)

    for state in positions_state:
        if state != 5:
            return positions_state == [5,5,5,5], state, 7
        else:
            if positions_state == [5,5,5,5]:
                if corner_orientation[0] == ['y', 'g', 'o']:
                    return True, 5, 0
                elif corner_orientation[0] == ['r', 'y', 'g']:
                    return True, 5, 1
                elif corner_orientation[0] == ['b', 'y', 'o']:
                    return True, 5, 2
                elif corner_orientation[0] == ['r', 'b', 'y']:
                    return True, 5, 3
                else:
                    return True, 5, 3
