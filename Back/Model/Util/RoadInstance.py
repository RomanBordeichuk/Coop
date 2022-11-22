from math import hypot, atan, copysign
from .LineInstance import Line
from .Consts import MaxVelocity
from math import pi

class Road:
    def __init__(self, nodes, start_node, end_node, number_of_lines, index):
        self.n_lines = number_of_lines
        self.start_node = start_node
        self.end_node = end_node
        self.max_velocity = MaxVelocity
        self.is_open: bool = True
        dx = nodes[start_node].apos[0] - nodes[end_node].apos[0]
        dy = nodes[start_node].apos[1] - nodes[end_node].apos[1]
        self.length = int(hypot(dx, dy))
        self.angle = (atan(dy / dx) + pi * (dx < 0)) if dx != 0.00 else copysign(pi / 2, dy)
        self.lines = {start_node: [], end_node: []}
        self.flow = 0
        self.K = 0
        self.index = index
        

        if number_of_lines == 1:
            self.lines[start_node] = [(Line(start_node, end_node, self))]
        else:
            for i in range(number_of_lines // 2):
                line = Line(start_node, end_node, self)
                self.lines[start_node].append(line)

            for i in range(number_of_lines // 2, number_of_lines):
                line = Line(end_node, start_node, self)
                self.lines[end_node].append(line)

    def __str__(self):
        return "Road: " + str(self.start_node) + ' ' + str(self.end_node)

    def Flow(self) -> None:
        self.flow = 0
        self.K = 0
        for node in self.lines.keys():
            for line in self.lines[node]:
                self.flow += line.comp() / len(self.lines[node])
                self.K += line.K / len(self.lines[node])
