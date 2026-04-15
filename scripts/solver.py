from ursina import *
import argparse
import optimal.solver as sv
import numpy
from time import sleep
import stash
import utils
import random

def instantiate_sequence(cube):
    no_anim = cube.get_no_anim()

    if no_anim:
        seq = Sequence(cube.rotate_side)
    else:
        seq = Sequence(cube.rotate_side, Wait(1))

    return seq

def repeat_white_cross_sequence(cube):
    sfl = instantiate_sequence(cube)
    pos = cube.get_pos()
    seq_index = cube.get_sequence_index()
    no_anim = cube.get_no_anim()

    pos.append(stash.ALGO_CONFIGS[seq_index-1][0])
    cube.set_pos(pos)

    rotations = stash.CROSS_SEQUENCES[pos[-1]]["flip"][pos[-1]]

    for index, rotation in enumerate(list(rotations)):
        rotate_side = cube.rotate_side
        sfl.append(Func(rotate_side, rotation))
        if not no_anim:
            sfl.append(Wait(1))

    sfl.start()

def white_cross_sequence(cube):
    sr = instantiate_sequence(cube)
    seq_index = cube.get_sequence_index()
    names = cube.get_names()
    pos = cube.get_pos()
    no_anim = cube.get_no_anim()

    curr_pos, name = utils.find_cube(cube, stash.ALGO_CONFIGS[seq_index])
    names.append(name)
    pos.append(curr_pos)
    cube.set_names(name)
    cube.set_pos(pos)

    rotations = stash.CROSS_SEQUENCES[stash.ALGO_CONFIGS[seq_index][0]]["regular"][pos[-1]]

    for rotation in list(rotations):
        rotate_side = cube.rotate_side
        sr.append(Func(rotate_side, rotation))
        if not no_anim:
            sr.append(Wait(1))

    sr.start()
    seq_index += 1
    cube.set_sequence_index(seq_index)

def solve_white_cross(cube):
    seq_index = cube.get_sequence_index()
    names = cube.get_names()
    pos = cube.get_pos()
    no_anim = cube.get_no_anim()

    if seq_index > 0 and not utils.in_position(cube, stash.ALGO_CONFIGS[seq_index-1], names[-1]):
        print("Repeat white edge", stash.ALGO_CONFIGS[seq_index-1])
        repeat_white_cross_sequence(cube)
    else:
        print("White edge")
        white_cross_sequence(cube)

def repeat_white_corner_sequence(cube):
    seq_index = cube.get_sequence_index()
    pos = cube.get_pos()
    no_anim = cube.get_no_anim()

    scc = instantiate_sequence(cube)
    pos.append(stash.ALGO_CONFIGS[seq_index-1][0])
    cube.set_pos(pos)
    rotations = stash.CROSS_SEQUENCES[pos[-1]]["flip"][pos[-1]]

    for rotation in list(rotations):
        rotate_side = cube.rotate_side
        scc.append(Func(rotate_side, rotation))
        if not no_anim:
            scc.append(Wait(1))

    scc.start()

def repeat_last_white_corner_sequence():
    pos = cube.get_pos()
    no_anim = cube.get_no_anim()

    lwcs = instantiate_sequence(cube)
    pos.append(stash.ALGO_CONFIGS[7][0])
    cube.set_pos(pos)
    rotations = stash.CROSS_SEQUENCES[17]["flip"][17]

    for rotation in list(rotations):
        rotate_side = cube.rotate_side
        lwcs.append(Func(rotate_side, rotation))
        if not no_anim:
            lwcs.append(Wait(1))

    lwcs.start()

def white_corner_sequence(cube, increment):
    scr = instantiate_sequence(cube)
    seq_index = cube.get_sequence_index()
    names = cube.get_names()
    pos = cube.get_pos()
    no_anim = cube.get_no_anim()

    curr_pos, name = utils.find_cube(cube, stash.ALGO_CONFIGS[seq_index])

    if increment:
        names.append(name)
    pos.append(curr_pos)

    cube.set_names(names)
    cube.set_pos(pos)

    rotations = stash.CROSS_SEQUENCES[stash.ALGO_CONFIGS[seq_index][0]]["regular"][pos[-1]]

    for rotation in list(rotations):
        rotate_side = cube.rotate_side
        scr.append(Func(rotate_side, rotation))

        if no_anim:
            scr.append(Wait(1))

    scr.start()

    if increment:
        seq_index += 1
        cube.set_sequence_index(seq_index)


def solve_white_corners(cube):
    seq_index = cube.get_sequence_index()
    names = cube.get_names()
    pos = cube.get_pos()
    no_anim = cube.get_no_anim()

    if not utils.in_position(cube, stash.ALGO_CONFIGS[seq_index-1], names[-1]):
        repeat_white_corner_sequence(cube)
    elif seq_index == 7:
        curr_pos, name = utils.find_cube(cube, stash.ALGO_CONFIGS[7])
        pos.append(curr_pos)
        cube.set_pos(pos)
        in_position = utils.in_position(cube, stash.ALGO_CONFIGS[7], name)

        if in_position:
            seq_index += 1
            cube.set_sequence_index(seq_index)
        elif curr_pos == stash.ALGO_CONFIGS[7][0]: # Rotate
            repeat_last_white_corner_sequence(cube)
        else:
            white_corner_sequence(cube, False)
    else:
        white_corner_sequence(cube, True)

def repeat_second_layer_sequence(cube):
    seq_index = cube.get_sequence_index()
    names = cube.get_names()
    pos = cube.get_pos()
    no_anim = cube.get_no_anim()

    if seq_index >= 12:
        cube.set_sequence_index(8)

    ssl = instantiate_sequence(cube)
    pos.append(stash.ALGO_CONFIGS[seq_index-1][0])
    cube.set_pos(pos)
    rotations = stash.CROSS_SEQUENCES[pos[-1]]["flip"][pos[-1]]

    for rotation in list(rotations):
        rotate_side = cube.rotate_side
        ssl.append(Func(rotate_side, rotation))
        if not no_anim:
            ssl.append(Wait(1))

    ssl.start()

def check_and_update_sequence_index(cube):
    seq_index = cube.get_sequence_index()
    skip = cube.get_skip()

    if seq_index >= 12:
        cube.set_sequence_index(8)
    else:
        seq_index += 1
        cube.set_sequence_index(seq_index)

    cube.set_skip(True)

def update_sequence_index(cube):
    seq_index = cube.get_sequence_index()
    skip = cube.get_skip()

    if seq_index >= 12 and not utils.check_second_layer(cube):
        cube.set_sequence_index(8)
    else:
        seq_index += 1
        cube.set_sequence_index(seq_index) # Might be incremented to 12 here. So on second invocation, the current index may be at 12.

    cube.set_skip(False)

def second_layer_sequence(cube):
    seq_index = cube.get_sequence_index()
    skip = cube.get_skip()
    cubelets = cube.get_cubes()
    names = cube.get_names()
    pos = cube.get_pos()
    no_anim = cube.get_no_anim()

    if seq_index >= 12:
        cube.set_sequence_index(8)

    cube_configs = stash.ALGO_CONFIGS
    smr = instantiate_sequence(cube)
    curr_pos, name = utils.find_cube(cube, cube_configs[seq_index])

    for cubelet in cubelets:
        if cubelet.name.split("_")[1] == name:
            second_layer_cube = cubelet

    names.append(name)
    pos.append(curr_pos)

    cube.set_names(names)
    cube.set_pos(pos)

    if second_layer_cube.name.split("_")[0] in stash.SIDES["a"]:
        rotations = stash.CROSS_SEQUENCES[cube_configs[seq_index][0]]["regular"][pos[-1]]

        for rotation in list(rotations):
            smr.append(Func(cube.rotate_side, rotation))

            if not no_anim:
                smr.append(Wait(1))

        smr.start()
        update_sequence_index(cube)
    else:
        check_and_update_sequence_index(cube)

    return "All complete"

def is_solvable(cube, config):
    curr_pos, name = utils.find_cube(cube, config)
    cubelets = cube.get_cubes()
    names = cube.get_names()
    pos = cube.get_pos()

    for cubelet in cubelets:
        if cubelet.name.split("_")[1] == name:
            second_layer_cube = cubelet

    names.append(name)
    pos.append(curr_pos)

    cube.set_names(names)
    cube.set_pos(pos)

    return second_layer_cube.name.split("_")[0] in stash.SIDES["a"]

def is_rotatable(cube, config):
    curr_pos, name = utils.find_cube(cube, config)
    names = cube.get_names()
    pos = cube.get_pos()
    names.append(name)
    pos.append(curr_pos)

    return curr_pos == config[0] and not utils.in_position(cube, config, names[-1])

def solve(cube, config):
    smr = instantiate_sequence(cube)
    pos = cube.get_pos()
    no_anim = cube.get_no_anim()
    rotations = stash.CROSS_SEQUENCES[config[0]]["regular"][pos[-1]]

    for rotation in list(rotations):
        smr.append(Func(cube.rotate_side, rotation))
        if not no_anim:
            smr.append(Wait(1))
    smr.start()

def rotate(cube, config):
    ssl = instantiate_sequence(cube)
    pos = cube.get_pos()
    no_anim = cube.get_no_anim()
    pos.append(config[0])
    cube.set_pos(pos)

    rotations = stash.CROSS_SEQUENCES[pos[-1]]["flip"][pos[-1]]

    for rotation in list(rotations):
        rotate_side = cube.rotate_side
        ssl.append(Func(rotate_side, rotation))
        if not no_anim:
            ssl.append(Wait(1))

    ssl.start()

def solve_second_layer(cube):
    seq_index = cube.get_sequence_index()
    skip = cube.get_skip()
    cubelets = cube.get_cubes()
    names = cube.get_names()
    pos = cube.get_pos()
    no_anim = cube.get_no_anim()
    n_solv_and_n_rot = cube.get_n_solv_and_n_rot()

    if seq_index >= 12 and not utils.check_second_layer(cube):
        cube.set_sequence_index(8)

    configs = stash.ALGO_CONFIGS
    solvable = is_solvable(configs[seq_index])
    rotatable = is_rotatable(configs[seq_index])

    if solvable:
        solve(configs[seq_index])
        seq_index += 1
        cube.set_sequence_index(seq_index)
    elif rotatable:
        rotate(configs[seq_index])
        seq_index += 1
        cube.set_sequence_index(seq_index)
    elif not solvable and not rotatable:
        n_solv_and_n_rot += 1
        cube.set_n_sol_and_n_rot(n_solv_and_n_rot)

        if n_solv_and_n_rot >= 2:
            config = stash.ALGO_CONFIGS[seq_index]
            indices = [3, 11, 13, 20]
            ra = instantiate_sequence(cube)
            algo = random.choice(indices)
            print("Break symmetry", (config, algo))
            rotations = stash.CROSS_SEQUENCES[config[0]]["regular"][algo]

            for rotation in list(rotations):
                rotate_side = cube.rotate_side
                ra.append(Func(rotate_side, rotation))
                if not no_anim:
                    ra.append(Wait(1))

            cube.set_n_solv_and_n_rot(0)
        else:
            seq_index += 1
            cube.set_sequence_index(seq_index)

def yellow_cross_sequence(cube, yellow_shape):
    sycr = instantiate_sequence(cube)
    rotations = stash.CROSS_SEQUENCES[666][yellow_shape][0]
    no_anim = cube.get_no_anim()

    for rotation in list(rotations):
        sycr.append(Func(cube.rotate_side, rotation))
        if not no_anim:
            sycr.append(Wait(1))

    sycr.start()

def solve_yellow_cross(cube):
    solved, shape = utils.check_yellow_cross(cube)
    seq_index = cube.get_sequence_index()

    if not solved:
        yellow_cross_sequence(cube, shape)
    else:
        seq_index += 1
        cube.set_sequence_index(seq_index)

def yellow_edges_sequence(cube, pos_state):
    syed = instantiate_sequence(cube)
    rotations = stash.CROSS_SEQUENCES[777][pos_state][0]
    seq_index = cube.get_sequence_index()
    no_anim = cube.get_no_anim()

    for rotation in list(rotations):
        syed.append(Func(cube.rotate_side, rotation))
        if not no_anim:
            syed.append(Wait(1))

    syed.start()

    if utils.check_yellow_edges(cube).upper() == "BOGR":
        seq_index += 1
        cube.set_sequence_index(seq_index)

def solve_yellow_edges(cube):
    positions_state = utils.check_yellow_edges(cube).upper()
    seq_index = cube.get_sequence_index()

    if seq_index > 0 and positions_state != "BOGR":
        yellow_edges_sequence(positions_state)
    else:
        seq_index += 1
        cube.set_sequence_index(seq_index)

def yellow_corners_sequence(cube, correct_cube_index):
    syc = instantiate_sequence(cube)
    in_position, correct_corner_pos = utils.yellow_corners_in_position(cube) # Check if correct_corner_pos is Null
    seq_index = cube.get_sequence_index()
    no_anim = cube.set_no_anim()

    if no_anim:
        syc = Sequence(cube.rotate_side)
    else:
        syc = Sequence(cube.rotate_side, Wait(1))
    rotations = stash.CROSS_SEQUENCES[888][correct_corner_pos][0]
    for rotation in list(rotations):
        syc.append(Func(cube.rotate_side, rotation))
        if not no_anim:
            syc.append(Wait(1))
    syc.start()

    in_position, index = utils.yellow_corners_in_position(cube)

    if in_position:
        seq_index += 1
        cube.set_sequence_index(seq_index)

def solve_yellow_corners(cube):
    position_state, correct_cube_index = utils.yellow_corners_in_position(cube)
    seq_index = cube.get_sequence_index()

    if not position_state:
        yellow_corners_sequence(correct_cube_index)
    else:
        seq_index += 1
        cube.set_sequence_index(seq_index)

def orient_yellow_corners_sequence(cube, desoriented):
    no_anim = cube.set_no_anim()
    soc = instantiate_sequence(cube)
    rotations = stash.CROSS_SEQUENCES[999][desoriented][0]

    for rotation in list(rotations):
        soc.append(Func(cube.rotate_side, rotation))
        if not no_anim:
            soc.append(Wait(1))
    soc.start()

def rotate_last_layer(cube, rotation):
    rll = instantiate_sequence(cube)
    rotations = stash.CROSS_SEQUENCES[999]["last_layer"][rotation]
    no_anim = cube.set_no_anim()

    for rotation in list(rotations):
        rll.append(Func(cube.rotate_side, rotation))

        if not stash.NO_ANIM:
            rll.append(Wait(1))

    rll.start()

def orient_yellow_corners(cube):
    oriented, desoriented, last_rotation = utils.yellow_corners_oriented(cube)
    seq_index = cube.get_sequence_index()

    if not oriented:
        orient_yellow_corners_sequence(cube, desoriented)
    elif oriented and last_rotation != 7:
        rotate_last_layer(cube, last_rotation)
    else:
        seq_index += 1
        cube.set_sequence_index(seq_index)

def randomize_cube(cube):
    seq = "abcdef"
    length = random.randint(1, 100)
    random_rotations = "".join(random.choices(seq, k=length))
    no_anim = cube.set_no_anim()

    if not no_anim:
        cube.set_reset(True)
        cube.set_no_anim(True)

    rcc = Sequence(cube.rotate_side)

    for rotation in list(random_rotations):
        rotate_side = cube.rotate_side
        rcc.append(Func(rotate_side, rotation))

    rcc.start()
    cube.set_sequence_index(0)

### OPTIMAL SOLVER ###

def get_input_string(cube):
    cubelets = cube.get_cubes()
    index = 0
    sides = [(stash.OUTER_SIDES[0], "a"), (stash.OUTER_SIDES[3], "d"), (stash.OUTER_SIDES[5], "f"), (stash.OUTER_SIDES[1], "b"), (stash.OUTER_SIDES[2], "c"), (stash.OUTER_SIDES[4], "e")]
    cubestring = []

    side_mapping = {
        "y": "U",
        "w": "D",
        "b": "L",
        "g": "R",
        "o": "B",
        "r": "F"
    }

    for side in sides:
        for cubelet in cubelets:
            if cubelet.name.split("_")[0] in stash.SIDES[side[1]]:
                for color_cube in cubelet.children:
                   world_position = round(color_cube.world_position, 1)
                   position_string = utils.get_color_cubelet_name(cube,
                                                                  world_position[0],
                                                                  world_position[1],
                                                                  world_position[2])
                   if position_string in side[0]:
                       cubestring.append(side_mapping[color_cube.name.split("_")[0]])

    cubestring = "".join(cubestring)

    return cubestring

def swappington(orig_seq):
    new_sequence = [0] * 54
    swaps = {
        # Yellow side
        0: 6,
        1: 3,
        2: 0,
        3: 7,
        4: 4,
        5: 1,
        6: 8,
        7: 5,
        8: 2,
        # Green side
        9:  15,
        10: 12,
        11: 9,
        12: 10,
        13: 11,
        14: 14,
        15: 17,
        16: 16,
        17: 13,
        # Red side
        18: 24,
        19: 21,
        20: 18,
        21: 25,
        22: 22,
        23: 19,
        24: 26,
        25: 23,
        26: 20,
        # White side
        27: 27,
        28: 33,
        29: 30,
        30: 28,
        31: 34,
        32: 31,
        33: 29,
        34: 35,
        35: 32,
        # Blue side
        36: 44,
        37: 41,
        38: 38,
        39: 37,
        40: 36,
        41: 39,
        42: 42,
        43: 43,
        44: 40,
        # Orange side
        45: 47,
        46: 50,
        47: 53,
        48: 46,
        49: 49,
        50: 52,
        51: 45,
        52: 48,
        53: 51
    }
    print("orig seq length", (orig_seq, len(orig_seq)))

    for index, seq_char in enumerate(list(orig_seq)):
        print(index)
        new_sequence[swaps[index]] = seq_char

    return new_sequence


def translate_output_string(sequence):
    rot_mapping = {
        "U1": "a",
        "U2": "aa",
        "U3": "g",
        "B1": "e",
        "B2": "ee",
        "B3": "l",
        "D1": "b",
        "D2": "bb",
        "D3": "h",
        "R1": "d",
        "R2": "dd",
        "R3": "k",
        "L1": "c",
        "L2": "cc",
        "L3": "j",
        "F1": "f",
        "F2": "ff",
        "F3": "o"
    }
    output_sequence = []
    output_string = ""

    for char in list(sequence.split(" "))[:-1]:
        output_sequence.append(rot_mapping[char])

    output_string = "".join(output_sequence)

    return output_string

def animate_optim_sequence(cube):
    oss = instantiate_sequence(cube)
    sequence = stash.OPTIM_SEQUENCE

    for rotation in list(sequence):
        oss.append(Func(cube.rotate_side, rotation))
        oss.append(Wait(1))

    oss.start()

def solve_cube_with_given_string(sequence):
    stash.OPTIM_SEQUENCE = sequence

def optim_solve_cube(cube):
    input_string = get_input_string(cube)
    swapped_list = swappington(input_string)
    swapped_string = "".join(swapped_list)
    output = sv.solve(swapped_string)
    stash.OPTIM_SEQUENCE = translate_output_string(output)
