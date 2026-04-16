from ursina import *
import argparse
import numpy
from time import sleep
import stash
import solver
import utils
import validator
from typing import List, Tuple, Optional

class Cube(Ursina):
    # Constants
    ROTATION_AXES = {
        'x': ('a', 'b', 'g', 'h'),
        'y': ('c', 'd', 'j', 'k'),
        'z': ('e', 'f', 'l', 'o'),
    }
    ROTATION_DIRECTIONS = {
        'a': 90, 'b': -90, 'g': -90, 'h': 90,
        'c': 90, 'd': -90, 'j': -90, 'k': 90,
        'e': -90, 'f': 90, 'l': 90, 'o': -90,
    }

    def __init__(self):
        super().__init__()
        self.cubes: List[Entity] = []
        self.sequence_index: int = 0
        self.second_completed: bool = False
        self.last_layer: bool = False
        self.names: List[str] = []
        self.pos: List[Tuple[int, int, int]] = []
        self.solution: List[str] = []
        self.no_anim: bool = False
        self.parent: Optional[Entity] = None
        self.skip: bool = False
        self.reset: bool = False
        self.n_solv_and_n_rot: int = 0
        self.invocations: int = 0
        self.optim_sequence: str = ""
        self.camera = EditorCamera()
        self.camera.world_position = (0, 0, 0)
        window.fullscreen = False
        self.construct_cube()
        self.init_argparse()

    # --- Properties ---
    @property
    def parent_entity(self) -> Entity:
        if not self.parent:
            self.parent = Entity(name="PARENT", model="cube", color=color.black, scale_1=1, position=(0, 0, 0))
        return self.parent

    # --- Core Methods ---
    def reparent_to_scene(self) -> None:
        for cube in self.cubes:
            if cube.parent == self.parent_entity:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
                label = cube.name.split("_")[1]
                cube.name = self._get_name(*map(int, cube.position), label)
        self.parent_entity.rotation = 0

    def update_cube_pos_names(self) -> None:
        for cube in self.cubes:
            world_pos = round(cube.world_position, 1)
            label = cube.name.split("_")[1]
            cube.name = self._get_name(*map(int, world_pos), label)

    @staticmethod
    def _get_name(a: int, b: int, c: int, label: str) -> str:
        return f"{a}{b}{c}_{label}"

    def _get_vector(self, name: str) -> Tuple[int, int, int]:
        coordinates = []
        for char in name:
            if char == "-":
                coordinates.append("-1")
            else:
                coordinates.append(char)
        return tuple(map(int, coordinates[:3]))

    def construct_cube(self) -> None:
        unordered_cubes = []
        for i in range(1, -2, -1):
            for j in range(1, -2, -1):
                for k in range(1, -2, -1):
                    if (i, j, k) == (0, 0, 0):
                        continue
                    cube = Entity(
                        name=self._get_name(i, j, k, "n"),
                        parent=scene,
                        model="custom_cube",
                        texture="rubik_texture",
                        scale_1=1,
                        position=Vec3(i, j, k),
                    )
                    utils.prepareEntity(cube)
                    unordered_cubes.append(cube)
        for label_pos in stash.LABELS.values():
            for cube in unordered_cubes:
                if cube.name.split("_")[0] == label_pos:
                    self.cubes.append(cube)

    def emulate_cube(self, content: str) -> None:
        labels = content.split(",")
        for index, cubelet in enumerate(self.cubes):
            cube_name_pos = cubelet.name.split("_")[0]
            cubelet.name = f"{cube_name_pos}_{labels[index]}-{index}"
        for cubelet in self.cubes:
            label = cubelet.name.split("_")[1].split("-")[0].strip()
            rotation_sequence = stash.ROTATIONS[label]
            self._rotate_cubelet(cubelet, rotation_sequence)

    def _rotate_cubelet(self, cubelet: Entity, rotation_sequence: str) -> None:
        for value in rotation_sequence:
            if value == "N":
                print("Value is N")
            elif value == "x":
                cubelet.rotation_x += 90
            elif value == "y":
                cubelet.rotation_y += 90
            elif value == "z":
                cubelet.rotation_z += 90

    def solving_step(self) -> None:
        index = self.sequence_index
        if 0 <= index < 5:
            solver.solve_white_cross(self)
        elif 5 <= index < 8:
            solver.solve_white_corners(self)
        elif 8 <= index < 12 and not self.last_layer and not utils.check_second_layer(self):
            solver.solve_second_layer(self)
        elif utils.check_second_layer(self) and index < 12 and not self.last_layer:
            self.sequence_index = 12
        elif index == 12 and not self.last_layer:
            solver.solve_yellow_cross(self)
        elif index == 13 and utils.check_yellow_cross(self) and not self.last_layer:
            solver.solve_yellow_edges(self)
        elif index == 14 and not self.last_layer:
            solver.solve_yellow_corners(self)
        elif index >= 15:
            self.last_layer = True
            solver.orient_yellow_corners(self)

    def randomize_cube(self) -> None:
        solver.randomize_cube(self)

    def animate_optim_sequence(self) -> None:
        solver.animate_optim_sequence(self)

    def optim_solve(self) -> None:
        solver.optim_solve_cube(self)

    # --- Input Handling ---
    def input(self, key: str, *args) -> None:
        if key in self.ROTATION_DIRECTIONS:
            self.rotate_side(key)
        elif key == "space":
            self.update_cube_pos_names()
            self.solving_step()
        elif key == "r":
            self.randomize_cube()
        elif key == "x":
            self.update_cube_pos_names()
            if self.invocations < 1:
                self.optim_solve()
                self.invocations += 1
            elif self.invocations > 10:
                self.invocations = 0
        elif key == "y":
            if self.optim_sequence:
                self.animate_optim_sequence()
            else:
                print("Compute optim sequence first")
        super().input(key)

    def rotate_side(self, index: str) -> None:
        self.reparent_to_scene()
        if index in stash.SIDES:
            side = stash.SIDES[index]
            parent = self.parent_entity
            for cubelet in self.cubes:
                if cubelet.name.split("_")[0] in side:
                    cubelet.parent = parent
            axis, direction = self._get_rotation_axis_and_direction(index)
            if self.no_anim:
                setattr(parent, f"rotation_{axis}", getattr(parent, f"rotation_{axis}") + direction)
            else:
                parent.animate(f"rotation_{axis}", getattr(parent, f"rotation_{axis}") + direction, duration=0.20)

    def _get_rotation_axis_and_direction(self, index: str) -> Tuple[str, int]:
        for axis, keys in self.ROTATION_AXES.items():
            if index in keys:
                return axis, self.ROTATION_DIRECTIONS[index]
        return "x", 90

    # --- Argument Parsing ---
    def init_argparse(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--file", help="Config filepath")
        parser.add_argument("-na", "--no-anim", help="Disables animation")
        parser.add_argument("-e", "--exec", help="Permutes cube according to permutation sequence")
        args = parser.parse_args()
        if args.no_anim == "T":
            self.no_anim = True
        if args.file:
            with open(args.file, "r") as f:
                content = f.readline()
            self.emulate_cube(content)
            if not validator.validate_config(self):
                error_text = Text("Invalid Config!", scale=0.1, origin=(0, 0))
        if args.exec:
            with open(args.exec, "r") as f:
                solution = f.readline().strip("\n")
            solver.solve_cube_with_given_string(self, solution)

if __name__ == '__main__':
    cube = Cube()
    cube.run()
