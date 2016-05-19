import unittest
import logic


class Tests(unittest.TestCase):
    def test_draw_line(self):
        points = [[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]]
        x1 = 0
        y1 = 0
        x2 = 3
        y2 = 3
        color = 5
        thick = 1
        logic.draw_line(x1, y1, x2, y2, points, color, thick)
        new_points = [[5, 0, 0, 0],
                      [0, 5, 0, 0],
                      [0, 0, 5, 0],
                      [0, 0, 0, 5]]
        for i in range(4):
            for j in range(4):
                self.assertEquals(points[i][j], new_points[i][j])

    def test_draw_rect(self):
        points = [[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]]
        x1 = 0
        y1 = 0
        x2 = 3
        y2 = 3
        color = 5
        thick = 1
        logic.draw_rect(x1, y1, x2, y2, points, color, thick)
        new_points = [[5, 5, 5, 5],
                      [5, 0, 0, 5],
                      [5, 0, 0, 5],
                      [5, 5, 5, 5]]
        for i in range(4):
            for j in range(4):
                self.assertEquals(points[i][j], new_points[i][j])

    def test_brush(self):
        points = [[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]]
        x1 = 0
        y1 = 0
        color = 5
        logic.brush(x1, y1, points, color, 4, 4)
        new_points = [[5, 5, 5, 5],
                      [5, 5, 5, 5],
                      [5, 5, 5, 5],
                      [5, 5, 5, 0]]
        for i in range(4):
            for j in range(4):
                self.assertEquals(points[i][j], new_points[i][j])

    def test_draw_ellipse(self):
        points = {}
        x1 = 0
        y1 = 0
        x2 = 3
        y2 = 3
        color = 5
        thick = 1
        logic.draw_ellipse(x1, y1, x2, y2, points, color, thick, 4, 4)
        for i in range(4):
            for j in range(4):
                self.assertEquals(points[(i, j)], 5)

    def test_thickness_point(self):
        x = 2
        y = 2
        points = [[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]]
        color = 5
        thick = 2
        logic.add_thickness_point(points, x, y, color, thick)
        new_points = [[0, 0, 0, 0],
                      [0, 5, 5, 5],
                      [0, 5, 5, 5],
                      [0, 5, 5, 5]]
        for i in range(4):
            for j in range(4):
                self.assertEquals(points[i][j], new_points[i][j])

if __name__ == '__main__':
    unittest.main()
