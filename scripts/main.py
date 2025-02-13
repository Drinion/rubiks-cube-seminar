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
        stash.NO_ANIM = False
        self.init_argparse()

    @classmethod
    def reparent_to_scene(self):
        for cube in stash.CUBES:
            if cube.parent == stash.PARENT:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
                label = cube.name.split("_")[1]
                cube.name = self.get_name(int(cube.position[0]), int(cube.position[1]), int(cube.position[2]), label)

        stash.PARENT.rotation = 0

    def update_cube_pos_names(self):
        for cube in stash.CUBES:
            world_pos = round(cube.world_position, 1)
            label = cube.name.split("_")[1]
            cube.name = self.get_name(int(world_pos[0]), int(world_pos[1]), int(world_pos[2]), label)

    @classmethod
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
        stash.PARENT = Entity(name="PARENT", model="cube", color=color.black, scale_1=1, position=(0,0,0))
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
                    stash.CUBES.append(cube)

    def emulate_cube(self, content):
        labels = content.split(",")

        for index, cube in enumerate(stash.CUBES):
            cube_name_pos = cube.name.split("_")[0]
            cube.name = cube_name_pos + "_" + labels[index] + "-" + f"{index}"

        for cube in stash.CUBES:
            label = cube.name.split("_")[1].split("-")[0].strip()
            rotation_sequence = stash.ROTATIONS[label]
            self.rotate_cubelet(cube, rotation_sequence)

    def rotate_cubelet(self, cube, rotation_sequence):
        sequence_values = list(rotation_sequence)

        for value in sequence_values:
            if value == "N":
                print("Value is N")
            else:
                if value == "x":
                    cube.rotation_x += 90
                elif value == "y":
                    cube.rotation_y += 90
                elif value == "z":
                    cube.rotation_z += 90

    def solving_step(self):
        index = stash.SEQUENCE_INDEX

        if index >= 0 and index < 5:
            solver.solve_white_cross()
        elif index >= 5 and index < 8:
            solver.solve_white_corners()
        elif index >= 8 and not stash.LAST_LAYER and not utils.check_second_layer():
            solver.solve_second_layer()
        elif utils.check_second_layer() and stash.SEQUENCE_INDEX < 12 and not stash.LAST_LAYER:
            stash.SEQUENCE_INDEX = 12
        elif index == 12 and not stash.LAST_LAYER:
            solver.solve_yellow_cross()
        elif index == 13 and utils.check_yellow_cross() and not stash.LAST_LAYER:
            solver.solve_yellow_edges()
        elif index == 14 and not stash.LAST_LAYER:
            solver.solve_yellow_corners()
        elif index >= 15:
            stash.LAST_LAYER = True
            solver.orient_yellow_corners()

    def optim_solve(self):
        solver.optim_solve_cube()

    def randomize_cube(self):
        solver.randomize_cube()

    def animate_optim_sequence(self):
        solver.animate_optim_sequence()

    def input(self, key, *args):
        if key in ["a", "b", "c", "d", "e", "f", "g", "h", "j", "k", "l", "o"]:
            self.rotate_side(key)
        elif key == "space":
            self.update_cube_pos_names()
            self.solving_step()
        elif key == "r":
            self.randomize_cube()
        elif key == "x":
            self.update_cube_pos_names()
            if stash.INVOCATIONS < 1:
                self.optim_solve()
                stash.INVOCATIONS += 1
            elif stash.INVOCATIONS > 10:
                stash.INVOCATIONS = 0
        elif key == "y":
            if stash.OPTIM_SEQUENCE != "":
                self.animate_optim_sequence()
            else:
                print("Compute optim sequence first")

        super().input(key)

    @classmethod
    def rotate_side(self, index):
        self.reparent_to_scene()

        if index != "7":
            side = stash.SIDES[index]
            for cubelet in stash.CUBES:
                name = cubelet.name.split("_")[0]
                if name in side:
                    cubelet.parent = stash.PARENT
            if index == "a" or index == "b" or index == "g" or index == "h":
                direction = 90
                if index == "b" or index == "g":
                    direction = -90
                if stash.NO_ANIM:
                    stash.PARENT.rotation_x += direction
                else:
                    stash.PARENT.animate_rotation_x(direction, duration=.20)
            elif index == "c" or index == "d" or index == "j" or index == "k":
                direction = 90
                if index == "d" or index == "j":
                    direction = -90
                if stash.NO_ANIM:
                    stash.PARENT.rotation_y += direction
                else:
                    stash.PARENT.animate_rotation_y(direction, duration=.20)
            elif index == "e" or index == "f" or index == "l" or index == "o":
                direction = 90
                if index == "e" or index == "o":
                    direction = -90
                if stash.NO_ANIM:
                    stash.PARENT.rotation_z += direction
                else:
                    stash.PARENT.animate_rotation_z(direction, duration=.20)
        else:
            print("Cubelet already in position")


    def init_argparse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--file", help="Config filepath")
        parser.add_argument("-na", "--no-anim", help="Disables animation")
        parser.add_argument("-e", "--exec", help="Permutes cube according to permutation sequence")

        self.args = parser.parse_args()

        if self.args.no_anim == "T":
            stash.NO_ANIM = True

        if self.args.file:
            file = open(self.args.file, "r")
            content = file.readline()
            file.close()

            self.emulate_cube(content)
            print("VALID?", validator.validate_config())
            if not validator.validate_config():
                error_text = Text("Invalid Config!", scale=0.1, origin=(0,0))

        if self.args.exec:
            file = open(self.args.exec, "r")
            solution = file.readline().strip("\n")
            file.close()
            solver.solve_cube_with_given_string(solution)

if __name__ == '__main__':
    cube = Cube()
    cube.run()
