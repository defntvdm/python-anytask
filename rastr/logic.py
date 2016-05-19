import math

def draw_line(x1, y1, x2, y2, points, color, thick):
    dx = x2 - x1
    dy = y2 - y1
    errorX = 0
    errorY = 0

    if dx > 0:
        incX = 1
    elif dx == 0:
        incX = 0
    else:
        incX = -1

    if dy > 0:
        incY = 1
    elif dy == 0:
        incY = 0
    else:
        incY = -1

    dx = math.fabs(dx)
    dy = math.fabs(dy)
    if dy > dx:
        d = dy
    else:
        d = dx

    currentX = x1
    currentY = y1
    if type(points) is list:
        points[currentX][currentY]= color
    else:
        points[(currentX, currentY)] = color
    while currentX!=x2 or currentY!=y2:
        errorX = errorX + dx
        errorY = errorY + dy
        if errorX >= d:
            errorX = errorX - d
            currentX = currentX + incX
        if errorY >= d:
            errorY = errorY - d
            currentY = currentY + incY
        add_thickness_point(points, currentX, currentY, color, thick)

def draw_rect(x1, y1, x2, y2, points, color, thick):
    start_x = int(min(x1, x2))
    end_x = int(max(x1, x2))
    start_y = int(min(y1, y2))
    end_y = int(max(y1, y2))
    for i in range(start_x, end_x+1):
        add_thickness_point(points, i, start_y, color, thick)
        add_thickness_point(points, i, end_y, color, thick)
    for j in range(start_y, end_y+1):
        add_thickness_point(points, start_x, j, color, thick)
        add_thickness_point(points, end_x, j, color, thick)

def draw_ellipse(x1, y1, x2, y2, points, color, thick, width, height):
    a = abs(x1-x2)//2
    b = abs(y1-y2)//2
    center_x = min(x2, x1) + a
    center_y = min(y2, y1) + b
    if x2 == x1 or y2 == y1:
        return
    for i in range(min(x2, x1)-40*thick, min(max(x2, x1)+40*thick, width)):
        for j in range(min(y2, y1)-40*thick, min(max(y2, y1)+40*thick, height)):
            if a*b-thick*40 <= math.sqrt((i-center_x)*(i-center_x)*b*b +\
                (j-center_y)*(j-center_y)*a*a) <= a*b+40*thick:
                points[(i, j)] = color

def brush(x, y, points, new_color, width, height):
        stack = [(x, y)]
        if points[x][y]:
            color = points[x][y]
            while stack:
                i, j = stack.pop()
                if points[i+1][j] == color:
                    points[i+1][j] = new_color
                    stack.append((i+1, j))
                if points[i][j+1] == color:
                    points[i][j+1] = new_color
                    stack.append((i, j+1))
                if points[i-1][j] == color:
                    points[i-1][j] = new_color
                    stack.append((i-1, j))
                if points[i][j-1] == color:
                    points[i][j-1] = new_color
                    stack.append((i, j-1))
        else:
            while stack:
                i, j = stack.pop()
                if -1 < i < width-1 and -1 < j < height-1:
                    if not points[i+1][j]:
                        points[i+1][j] = new_color
                        stack.append((i+1, j))
                    if not points[i-1][j]:
                        points[i-1][j] = new_color
                        stack.append((i-1, j))
                    if not points[i][j+1]:
                        points[i][j+1] = new_color
                        stack.append((i, j+1))
                    if not points[i][j-1]:
                        points[i][j-1] = new_color
                        stack.append((i, j-1))

def add_thickness_point(points, x, y, color, thick):
    for i in range(-thick, thick):
        for j in range(-thick, thick):
            if i*i+j*j < thick*thick:
                if type(points) is list:
                    points[x+i][y+j] = color
                else:
                    points[(x+i, y+j)] = color
