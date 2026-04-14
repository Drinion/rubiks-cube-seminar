from ursina import *

import argparse
import numpy
from time import sleep
import stash
import solver
import utils
import validator

class Cube(Ursina):
    def __init__(self):
        super().__init__()
        self.camera = EditorCamera()
        self.camera.world_position = (0,0,0)
        window.fullscreen = False
        self.construct_cube()
        self.init_argparse()
        self.cubes = []
        self.sequence_index = 0
        self.second_completed = 0
        self.last_layer = False
        self.names = []
        self.pos = []
        self.solution = []
        self.no_anim = False
        self.parent = ""
        self.skip = False
        self.reset = False
        self.n_solv_and_n_rot = 0
        self.invocations = 0
        self.optim_sequence = ""


    def reparent_to_scene(self):
        for cube in self.cubes:
            if cube.parent == self.get_parent():
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
                label = cube.name.split("_")[1]
                cube.name = self.get_name(int(cube.position[0]), int(cube.position[1]), int(cube.position[2]), label)
    
        self.get_parent().rotation = 0

    def update_cube_pos_names(self):
        for cube in self.cubes:
            world_pos = round(cube.world_position, 1)
            label = cube.name.split("_")[1]
            cube.name = self.get_name(int(world_pos[0]), int(world_pos[1]), int(world_pos[2]), label)

    def get_name(self,a,b,c,label): return str(int(a)) + str(int(b)) + str(int(c)) + "_" + label

    def get_vector(self, name):
        coordinates = []

        for index in iter(range(len(name))):
            if name[index] == "-":
                coordinates.append("-1")
                next(iter(range(len(name))))
            else:
                coordinates.append(list(name)[index])
                index += 1

        return (int(coordinates[0]), int(coordinates[1]), int(coordinates[2]))

    def construct_cube(self):
        self.set_parent(Entity(name="PARENT", model="cube", color=color.black, scale_1=1, position=(0,0,0)))
        unordered_cubes = []

        for i in range(1,-2,-1):
            for j in range(1,-2,-1):
                for k in range(1,-2,-1):
                    if (i,j,k) == (0,0,0):
                        continue

                    cube = Entity(name=self.get_name(i,j,k,"n"), parent=scene, model="custom_cube", texture="rubik_texture", scale_1=1, position=Vec3(i,j,k))
                    utils.prepareEntity(cube)

                    unordered_cubes.append(cube)

        for label_pos in stash.LABELS.values():
            for cube in unordered_cubes:
                name_label_pos = cube.name.split("_")[0]
                if name_label_pos == label_pos:
                    self.cubes.append(cube)

    def emulate_cube(self, content):
        labels = content.split(",")

        for index, cubelet in enumerate(self.cubes):
            cube_name_pos = cube.name.split("_")[0]
            cubelet.name = cube_name_pos + "_" + labels[index] + "-" + f"{index}"

        for cubelet in self.cubes:
            label = cubelet.name.split("_")[1].split("-")[0].strip()
            rotation_sequence = stash.ROTATIONS[label]
            self.rotate_cubelet(cubelet, rotation_sequence)

    def rotate_cubelet(self, cubelet, rotation_sequence):
        sequence_values = list(rotation_sequence)

        for value in sequence_values:
            if value == "N":
                print("Value is N")
            else:
                if value == "x":
                    cubelet.rotation_x += 90
                elif value == "y":
                    cubelet.rotation_y += 90
                elif value == "z":
                    cubelet.rotation_z += 90

    def solving_step(self):
        index = self.get_sequence_index()

        if index >= 0 and index < 5:
            solver.solve_white_cross(self)
        elif index >= 5 and index < 8:
            solver.solve_white_corners(self)
        elif index >= 8 and not self.get_last_layer() and not utils.check_second_layer(self):
            solver.solve_second_layer(self)
        elif utils.check_second_layer(self) and index < 12 and not self.get_last_layer():
            self.set_sequence_index(12)
        elif index == 12 and not self.get_last_layer():
            solver.solve_yellow_cross(self)
        elif index == 13 and utils.check_yellow_cross(self) and not self.get_last_layer():
            solver.solve_yellow_edges(self)
        elif index == 14 and not self.get_last_layer():
            solver.solve_yellow_corners(self)
        elif index >= 15:
            self.set_last_layer(True)
            solver.orient_yellow_corners(self)

    def optim_solve(self):
        solver.optim_solve_cube(self)

    def randomize_cube(self):
        solver.randomize_cube(self)

    def animate_optim_sequence(self):
        solver.animate_optim_sequence(self)

    def input(self, key, *args):
        invocations = self.get_invocations()

        if key in ["a", "b", "c", "d", "e", "f", "g", "h", "j", "k", "l", "o"]:
            self.rotate_side(key)
        elif key == "space":
            self.update_cube_pos_names()
            self.solving_step()
        elif key == "r":
            self.randomize_cube()
        elif key == "x":
            self.update_cube_pos_names()
            if invocations < 1:
                self.optim_solve()
                invocations += 1
                self.set_invocations(invocations)
            elif self.get_invocations() > 10:
                self.set_invocations(0)
        elif key == "y":
            if self.get_optim_sequence() != "":
                self.animate_optim_sequence()
            else:
                print("Compute optim sequence first")

        super().input(key)

    def rotate_side(self, index):
        self.reparent_to_scene()

        if index != "7":
            side = stash.SIDES[index]
            parent = self.get_parent()

            for cubelet in self.cubes:
                name = cubelet.name.split("_")[0]
                if name in side:
                    cubelet.parent = parent
            if index == "a" or index == "b" or index == "g" or index == "h":
                direction = 90
                if index == "b" or index == "g":
                    direction = -90
                if self.get_no_anim():
                    parent.rotation_x += direction
                else:
                    parent.animate_rotation_x(direction, duration=.20)
            elif index == "c" or index == "d" or index == "j" or index == "k":
                direction = 90
                if index == "d" or index == "j":
                    direction = -90
                if self.get_no_anim():
                    parent.rotation_y += direction
                else:
                    parent.animate_rotation_y(direction, duration=.20)
            elif index == "e" or index == "f" or index == "l" or index == "o":
                direction = 90
                if index == "e" or index == "o":
                    direction = -90
                if self.get_no_anim():
                    parent.rotation_z += direction
                else:
                    parent.animate_rotation_z(direction, duration=.20)
        else:
            print("Cubelet already in position")


    def init_argparse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--file", help="Config filepath")
        parser.add_argument("-na", "--no-anim", help="Disables animation")
        parser.add_argument("-e", "--exec", help="Permutes cube according to permutation sequence")

        self.args = parser.parse_args()

        if self.args.no_anim == "T":
            self.set_no_anim(True)

        if self.args.file:
            file = open(self.args.file, "r")
            content = file.readline()
            file.close()

            self.emulate_cube(content)
            print("VALID?", validator.validate_config(self))
            if not validator.validate_config(self):
                error_text = Text("Invalid Config!", scale=0.1, origin=(0,0))

        if self.args.exec:
            file = open(self.args.exec, "r")
            solution = file.readline().strip("\n")
            file.close()
            solver.solve_cube_with_given_string(self, solution)

    def set_sequence_index(self, index):
        self.sequence_index = index

    def get_sequence_index(self):
        return self.sequence_index

    def set_second_completed(self, val):
        self.second_completed = val

    def get_second_completed(self):
        return self.second_completed

    def set_last_layer(self, val):
        self.last_layer = val

    def get_last_layer(self):
        return self.last_layer

    def set_names(self, val):
        self.names = val

    def get_names(self):
        return self.names

    def set_pos(self, val):
        self.pos = val

    def get_pos(self):
        return self.pos

    def set_solution(self, val):
        self.solution = val

    def get_solution(self):
        return self.solution

    def set_no_anim(self, val):
        self.no_anim = val

    def get_no_anim(self):
        return self.no_anim

    def set_parent(self, val):
        self.parent = val

    def get_parent(self):
        return self.parent

    def set_skip(self, val):
        self.skip = val

    def get_skip(self):
        return self.skip

    def set_reset(self, val):
        self.reset = val

    def get_reset(self):
        return self.reset

    def set_n_solv_and_n_rot(self, val):
        self.n_solv_and_n_rot = val

    def get_n_solv_and_n_rot(self):
        return self.n_solv_and_n_rot

    def set_invocations(self, val):
        self.invocations = val

    def get_invocations(self):
        return self.invocations

    def set_optim_sequence(self, val):
        self.optim_sequence = val

    def get_optim_sequence(self):
        return self.optim_sequence

if __name__ == '__main__':
    cube = Cube()
    cube.run()
