import math
import time
import FA
import serial as serial

fa = FA.Create()
fa.ComOpen(3)  # Check your computer's bluetooth settings to get the correct port for this value.


angle = 0  # Starting angle always defined as "0" degrees.
turn = []  # a placeholder for turn commands.
final_movement_list = []  # The final list of movement commands the robot executes, a list of strings.


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0  # distance from the origin
        self.h = 0  # heuristic value
        self.f = 0  # total cost of the node

    def __eq__(self, other):
        return self.position == other.position


def turns(reversed_list):
    global turn
    global angle
    global final_movement_list

    
    for node in range(len(reversed_list)-1):    
        m = 0
        if reversed_list[node][1] < reversed_list[node + 1][1]: m += 1
        if angle == 90: m += 10
        if angle == 180: m += 20
        if angle == 270: m += 40
        
        match m:
            case 0:
                angle = 270
                turn.append(angle)
                final_movement_list.append("left")
            case 1:
                angle = 90
                turn.append(angle)
                final_movement_list.append("right")
            case 10:
                angle = 0
                turn.append(angle)
                final_movement_list.append("left")
            case 11:
                angle = 180
                turn.append(angle)
                final_movement_list.append("right")
            case 20 | 21:
                angle = 90
                turn.append(angle)
                final_movement_list.append("left")
            case 40:
                angle = 0
                turn.append(angle)
                final_movement_list.append("right")
            case 41:
                angle = 0
                turn.append(angle)
                final_movement_list.append("left")
            case _:
                final_movement_list.append("forward")
        final_movement_list.append("forward")
        
        """
        if angle == 0 and reversed_list[node][1] > reversed_list[node + 1][1]:  # angle 0, y value decreases, turn left
            angle = 270
            turn.append(angle)
            final_movement_list.append("left")
            final_movement_list.append("forward")
            continue
        if angle == 0 and reversed_list[node][1] < reversed_list[node + 1][1]:  # angle 0, y value increases, turn right
            angle = 90
            turn.append(angle)
            final_movement_list.append("right")
            final_movement_list.append("forward")
            continue
        if angle == 180 and reversed_list[node][1] > reversed_list[node + 1][1]:  # angle 180, y value decreases, turn left
            angle = 90
            turn.append(angle)
            final_movement_list.append("left")
            final_movement_list.append("forward")
            continue
        if angle == 180 and reversed_list[node][1] < reversed_list[node + 1][1]:  # angle 180, y value increases, turn left
            angle = 90
            turn.append(angle)
            final_movement_list.append("left")
            final_movement_list.append("forward")
            continue
        if angle == 90 and reversed_list[node][0] > reversed_list[node + 1][0]:  # angle 90, x value decreases, turn left
            angle = 0
            turn.append(angle)
            final_movement_list.append("left")
            final_movement_list.append("forward")
            continue
        if angle == 90 and reversed_list[node][0] < reversed_list[node + 1][0]:  # angle 90, x value increases, turn right
            angle = 180
            turn.append(angle)
            final_movement_list.append("right")
            final_movement_list.append("forward")
            continue
        if angle == 270 and reversed_list[node][0] > reversed_list[node + 1][0]:  # angle 270, x value decreases, turn right
            angle = 0
            turn.append(angle)
            final_movement_list.append("right")
            final_movement_list.append("forward")
            continue
        if angle == 270 and reversed_list[node][0] < reversed_list[node + 1][0]:  # angle 270, x value increases, turn left
            angle = 180
            turn.append(angle)
            final_movement_list.append("left")
            final_movement_list.append("forward")
            continue
        else:
            # turn.append("forward")
            final_movement_list.append("forward")
    
    for node in range(len(reversed_list) - 1):
        x_diff = reversed_list[node][0] - reversed_list[node + 1][0]
        y_diff = reversed_list[node][1] - reversed_list[node + 1][1]

        if angle == 0 and y_diff > 0:
            angle = 270
        elif angle == 0 and y_diff < 0:
            angle = 90
        elif angle == 180 and y_diff > 0:
            angle = 90
        elif angle == 180 and y_diff < 0:
            angle = 90
        elif angle == 90 and x_diff > 0:
            angle = 0
        elif angle == 90 and x_diff < 0:
            angle = 180
        elif angle == 270 and x_diff > 0:
            angle = 0
        elif angle == 270 and x_diff < 0:
            angle = 180
        else:
            final_movement_list.append("forward")
            continue
    """
    turn.append(angle)
    final_movement_list.extend(["left", "forward"])
    print("Final angle: " + str(angle))
    print("MOVEMENT SOLUTION: " + str(final_movement_list))


def navigate():
    for x in range(len(final_movement_list)):
        if final_movement_list[x] == "forward":
            fa.Forwards(87.5)
            time.sleep(0.0)
        if final_movement_list[x] == "left":
            fa.Left(86)
            time.sleep(0.0)
        if final_movement_list[x] == "right":
            fa.Right(86)
            time.sleep(0.0)
    fa.SetMotors(0, 0)
    fa.ComClose()


def a_star(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Move current from the open list to the closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal node
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
                # print(path[-1])
            print("Steps taken: " + str(-1 + len(path)))

            path_reversed = path[::-1]
            turns(path_reversed)
            return "Press a button to start navigating."
            # return path_reversed  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares, only horizontals and verticals
            # [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)], if you want diagonals too
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > \
                    (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            if Node(current_node, node_position) in closed_list:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)
            print(current_node.position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = math.sqrt(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] -
                                                                                      end_node.position[1]) ** 2))
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def main():

    maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    start = (9, 1)
    end = (3, 3)

    path = a_star(maze, start, end)
    navigate()
    # print(path)


if __name__ == '__main__':
    main()
