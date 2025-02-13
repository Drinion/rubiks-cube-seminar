from ursina import *
import argparse
import optimal.solver as sv
import numpy
from time import sleep
import stash
from main import Cube
import utils
import random

def instantiate_sequence():
    if stash.NO_ANIM:
        seq = Sequence(Cube.rotate_side)
    else:
        seq = Sequence(Cube.rotate_side, Wait(1))

    return seq

def repeat_white_cross_sequence():
    sfl = instantiate_sequence()
    stash.POS.append(stash.ALGO_CONFIGS[stash.SEQUENCE_INDEX-1][0])
    rotations = stash.CROSS_SEQUENCES[stash.POS[-1]]["flip"][stash.POS[-1]]

    for index, rotation in enumerate(list(rotations)):
        rotate_side = Cube.rotate_side
        sfl.append(Func(rotate_side, rotation))
        if not stash.NO_ANIM:
            sfl.append(Wait(1))

    sfl.start()

def white_cross_sequence():
    sr = instantiate_sequence()
    pos, name = utils.find_cube(stash.ALGO_CONFIGS[stash.SEQUENCE_INDEX])
    stash.NAMES.append(name)
    stash.POS.append(pos)
    rotations = stash.CROSS_SEQUENCES[stash.ALGO_CONFIGS[stash.SEQUENCE_INDEX][0]]["regular"][stash.POS[-1]]

    for rotation in list(rotations):
        rotate_side = Cube.rotate_side
        sr.append(Func(rotate_side, rotation))
        if not stash.NO_ANIM:
            sr.append(Wait(1))

    sr.start()
    stash.SEQUENCE_INDEX += 1

def solve_white_cross():
    if stash.SEQUENCE_INDEX > 0 and not utils.in_position(stash.ALGO_CONFIGS[stash.SEQUENCE_INDEX-1], stash.NAMES[-1]):
        print("Repeat white edge", stash.ALGO_CONFIGS[stash.SEQUENCE_INDEX-1])
        repeat_white_cross_sequence()
    else:
        print("White edge")
        white_cross_sequence()

def repeat_white_corner_sequence():
    scc = instantiate_sequence()
    stash.POS.append(stash.ALGO_CONFIGS[stash.SEQUENCE_INDEX-1][0])
    rotations = stash.CROSS_SEQUENCES[stash.POS[-1]]["flip"][stash.POS[-1]]

    for rotation in list(rotations):
        rotate_side = Cube.rotate_side
        scc.append(Func(rotate_side, rotation))
        if not stash.NO_ANIM:
            scc.append(Wait(1))

    scc.start()

def repeat_last_white_corner_sequence():
    lwcs = instantiate_sequence()
    stash.POS.append(stash.ALGO_CONFIGS[7][0])
    rotations = stash.CROSS_SEQUENCES[17]["flip"][17]

    for rotation in list(rotations):
        rotate_side = Cube.rotate_side
        lwcs.append(Func(rotate_side, rotation))
        if not stash.NO_ANIM:
            lwcs.append(Wait(1))

    lwcs.start()

def white_corner_sequence(increment):
    scr = instantiate_sequence()
    pos, name = utils.find_cube(stash.ALGO_CONFIGS[stash.SEQUENCE_INDEX])

    if increment:
        stash.NAMES.append(name)
    stash.POS.append(pos)
    rotations = stash.CROSS_SEQUENCES[stash.ALGO_CONFIGS[stash.SEQUENCE_INDEX][0]]["regular"][stash.POS[-1]]

    for rotation in list(rotations):
        rotate_side = Cube.rotate_side
        scr.append(Func(rotate_side, rotation))
        if not stash.NO_ANIM:
            scr.append(Wait(1))

    scr.start()

    if increment:
        stash.SEQUENCE_INDEX += 1


def solve_white_corners():
    if not utils.in_position(stash.ALGO_CONFIGS[stash.SEQUENCE_INDEX-1], stash.NAMES[-1]):
        repeat_white_corner_sequence()
    elif stash.SEQUENCE_INDEX == 7:
        pos, name = utils.find_cube(stash.ALGO_CONFIGS[7])
        stash.POS.append(pos)
        in_position = utils.in_position(stash.ALGO_CONFIGS[7], name)
        if in_position:
            stash.SEQUENCE_INDEX += 1
        elif pos == stash.ALGO_CONFIGS[7][0]: # Rotate
            repeat_last_white_corner_sequence()
        else:
            white_corner_sequence(False)
    else:
        white_corner_sequence(True)

def repeat_second_layer_sequence():
    if stash.SEQUENCE_INDEX >= 12:
        stash.SEQUENCE_INDEX = 8

    ssl = instantiate_sequence()
    stash.POS.append(stash.ALGO_CONFIGS[stash.SEQUENCE_INDEX-1][0])
    rotations = stash.CROSS_SEQUENCES[stash.POS[-1]]["flip"][stash.POS[-1]]

    for rotation in list(rotations):
        rotate_side = Cube.rotate_side
        ssl.append(Func(rotate_side, rotation))
        if not stash.NO_ANIM:
            ssl.append(Wait(1))

    ssl.start()

def check_and_update_sequence_index():
    if stash.SEQUENCE_INDEX >= 12:
        stash.SEQUENCE_INDEX = 8
    else:
        stash.SEQUENCE_INDEX += 1
    stash.SKIP = True

def update_sequence_index():
    if stash.SEQUENCE_INDEX >= 12 and not utils.check_second_layer():
        stash.SEQUENCE_INDEX = 8
    else:
        stash.SEQUENCE_INDEX += 1 # Might be incremented to 12 here. So on second invocation, the current index may be at 12.

    stash.SKIP = False

def second_layer_sequence():
    """
    Refactor
    """
    if stash.SEQUENCE_INDEX >= 12:
        stash.SEQUENCE_INDEX = 8

    cube_configs = stash.ALGO_CONFIGS
    smr = instantiate_sequence()
    pos, name = utils.find_cube(cube_configs[stash.SEQUENCE_INDEX])

    for cube in stash.CUBES:
        if cube.name.split("_")[1] == name:
            second_layer_cube = cube

    stash.NAMES.append(name)
    stash.POS.append(pos)

    if second_layer_cube.name.split("_")[0] in stash.SIDES["a"]:
        rotations = stash.CROSS_SEQUENCES[cube_configs[stash.SEQUENCE_INDEX][0]]["regular"][stash.POS[-1]]

        for rotation in list(rotations):
            smr.append(Func(Cube.rotate_side, rotation))

            if not stash.NO_ANIM:
                smr.append(Wait(1))

        smr.start()
        update_sequence_index()
    else:
        check_and_update_sequence_index()

    return "All complete"

def is_solvable(config):
    pos, name = utils.find_cube(config)

    for cube in stash.CUBES:
        if cube.name.split("_")[1] == name:
            second_layer_cube = cube

    stash.NAMES.append(name)
    stash.POS.append(pos)

    return second_layer_cube.name.split("_")[0] in stash.SIDES["a"]

def is_rotatable(config):
    pos, name = utils.find_cube(config)
    stash.NAMES.append(name)
    stash.POS.append(pos)

    return pos == config[0] and not utils.in_position(config, stash.NAMES[-1])

def solve(config):
    smr = instantiate_sequence()
    rotations = stash.CROSS_SEQUENCES[config[0]]["regular"][stash.POS[-1]]

    for rotation in list(rotations):
        smr.append(Func(Cube.rotate_side, rotation))
        if not stash.NO_ANIM:
            smr.append(Wait(1))
    smr.start()

def rotate(config):
    ssl = instantiate_sequence()
    stash.POS.append(config[0])
    rotations = stash.CROSS_SEQUENCES[stash.POS[-1]]["flip"][stash.POS[-1]]

    for rotation in list(rotations):
        rotate_side = Cube.rotate_side
        ssl.append(Func(rotate_side, rotation))
        if not stash.NO_ANIM:
            ssl.append(Wait(1))

    ssl.start()
def solve_second_layer():
    """
    Refactor
    """
    if stash.SEQUENCE_INDEX >= 12 and not utils.check_second_layer():
        stash.SEQUENCE_INDEX = 8

    configs = stash.ALGO_CONFIGS
    solvable = is_solvable(configs[stash.SEQUENCE_INDEX])
    rotatable = is_rotatable(configs[stash.SEQUENCE_INDEX])

    if solvable:
        solve(configs[stash.SEQUENCE_INDEX])
        stash.SEQUENCE_INDEX += 1
    elif rotatable:
        rotate(configs[stash.SEQUENCE_INDEX])
        stash.SEQUENCE_INDEX += 1
    elif not solvable and not rotatable:
        stash.N_SOLV_AND_N_ROT += 1

        if stash.N_SOLV_AND_N_ROT >= 2:
            config = stash.ALGO_CONFIGS[stash.SEQUENCE_INDEX]
            indices = [3, 11, 13, 20]
            ra = instantiate_sequence()
            algo = random.choice(indices)
            print("Break symmetry", (config, algo))
            rotations = stash.CROSS_SEQUENCES[config[0]]["regular"][algo]

            for rotation in list(rotations):
                rotate_side = Cube.rotate_side
                ra.append(Func(rotate_side, rotation))
                if not stash.NO_ANIM:
                    ra.append(Wait(1))

            stash.N_SOLV_AND_N_ROT = 0
            # stash.SEQUENCE_INDEX += 1
        else:
            stash.SEQUENCE_INDEX += 1

def yellow_cross_sequence(yellow_shape):
    sycr = instantiate_sequence()
    rotations = stash.CROSS_SEQUENCES[666][yellow_shape][0]

    for rotation in list(rotations):
        sycr.append(Func(Cube.rotate_side, rotation))
        if not stash.NO_ANIM:
            sycr.append(Wait(1))

    sycr.start()

def solve_yellow_cross():
    solved, shape = utils.check_yellow_cross()
    print("Shape", shape)

    if not solved:
        yellow_cross_sequence(shape)
    else:
        stash.SEQUENCE_INDEX += 1

def yellow_edges_sequence(pos_state):
    syed = instantiate_sequence()
    rotations = stash.CROSS_SEQUENCES[777][pos_state][0]

    for rotation in list(rotations):
        syed.append(Func(Cube.rotate_side, rotation))
        if not stash.NO_ANIM:
            syed.append(Wait(1))

    syed.start()

    if utils.check_yellow_edges().upper() == "BOGR":
        stash.SEQUENCE_INDEX += 1

def solve_yellow_edges():
    positions_state = utils.check_yellow_edges().upper()
    if stash.SEQUENCE_INDEX > 0 and positions_state != "BOGR":
        yellow_edges_sequence(positions_state)
    else:
        stash.SEQUENCE_INDEX += 1

def yellow_corners_sequence(correct_cube_index):
    syc = instantiate_sequence()
    in_position, correct_corner_pos = utils.yellow_corners_in_position() # Check if correct_corner_pos is Null
    if stash.NO_ANIM:
        syc = Sequence(Cube.rotate_side)
    else:
        syc = Sequence(Cube.rotate_side, Wait(1))
    rotations = stash.CROSS_SEQUENCES[888][correct_corner_pos][0]
    for rotation in list(rotations):
        syc.append(Func(Cube.rotate_side, rotation))
        if not stash.NO_ANIM:
            syc.append(Wait(1))
    syc.start()

    in_position, index = utils.yellow_corners_in_position()

    if in_position:
        stash.SEQUENCE_INDEX += 1

def solve_yellow_corners():
    position_state, correct_cube_index = utils.yellow_corners_in_position()
    if not position_state:
        yellow_corners_sequence(correct_cube_index)
    else:
        stash.SEQUENCE_INDEX += 1

def orient_yellow_corners_sequence(desoriented):
    soc = instantiate_sequence()
    rotations = stash.CROSS_SEQUENCES[999][desoriented][0]
    for rotation in list(rotations):
        soc.append(Func(Cube.rotate_side, rotation))
        if not stash.NO_ANIM:
            soc.append(Wait(1))
    soc.start()

def rotate_last_layer(rotation):
    rll = instantiate_sequence()
    rotations = stash.CROSS_SEQUENCES[999]["last_layer"][rotation]
    for rotation in list(rotations):
        rll.append(Func(Cube.rotate_side, rotation))
        if not stash.NO_ANIM:
            rll.append(Wait(1))

    rll.start()

def orient_yellow_corners():
    oriented, desoriented, last_rotation = utils.yellow_corners_oriented()
    if not oriented:
        orient_yellow_corners_sequence(desoriented)
    elif oriented and last_rotation != 7:
        rotate_last_layer(last_rotation)
    else:
        stash.SEQUENCE_INDEX += 1

def randomize_cube():
    seq = "abcdef"
    length = random.randint(1, 100)
    random_rotations = "".join(random.choices(seq, k=length))

    if not stash.NO_ANIM:
        stash.RESET = True
        stash.NO_ANIM = True

    rcc = Sequence(Cube.rotate_side)

    for rotation in list(random_rotations):
        rotate_side = Cube.rotate_side
        rcc.append(Func(rotate_side, rotation))

    rcc.start()
    stash.SEQUENCE_INDEX = 0

### OPTIMAL SOLVER ###

def get_input_string():
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
        for cube in stash.CUBES:
            if cube.name.split("_")[0] in stash.SIDES[side[1]]:
                for color_cube in cube.children:
                   world_position = round(color_cube.world_position, 1)
                   position_string = utils.get_color_cubelet_name(world_position[0],
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

def animate_optim_sequence():
    oss = instantiate_sequence()
    sequence = stash.OPTIM_SEQUENCE

    for rotation in list(sequence):
        oss.append(Func(Cube.rotate_side, rotation))
        oss.append(Wait(1))

    oss.start()

def solve_cube_with_given_string(sequence):
    stash.OPTIM_SEQUENCE = sequence

def optim_solve_cube():
    input_string = get_input_string()
    swapped_list = swappington(input_string)
    swapped_string = "".join(swapped_list)
    output = sv.solve(swapped_string)
    print("OPTIM SEQUENCE", translate_output_string(output))
    stash.OPTIM_SEQUENCE = translate_output_string(output)
