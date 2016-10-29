#!/usr/bin/env python3

import unittest
import logic


class Tests(unittest.TestCase):
    def test_get_table(self):
        table = logic.get_table(100, 100, 9)
        for i in range(100):
            for j in range(100):
                self.assertEqual(table[i][j] < 10 and table[i][j] > 0, True)

    def test_shift_down(self):
        for_down = [[1, 2, 3, 4, 5, 6],
                    [0, 1, 0, 2, 0, 3],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 0, 1, 1]]
        res_down = [[0, 2, 0, 0, 0, 6],
                    [1, 1, 3, 4, 5, 3],
                    [1, 1, 1, 2, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1]]
        logic.WIDTH = 6
        logic.HEIGHT = 6
        logic.shift_down(for_down)
        for i in range(6):
            for j in range(6):
                self.assertEqual(for_down[i][j], res_down[i][j])

    def test_shift_left(self):
        for_left = [[1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [1, 0, 1, 0, 1, 1]]
        res_left = [[1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 0, 0]]
        logic.shift_left(for_left, [])
        for i in range(6):
            for j in range(6):
                self.assertEqual(for_left[i][j], res_left[i][j])

    def test_burst(self):
        for_burst = [[1, 2, 2, 1, 1, 1],
                     [1, 2, 2, 1, 1, 1],
                     [1, 2, 2, 1, 1, 1],
                     [1, 2, 2, 1, 1, 1],
                     [1, 2, 2, 2, 2, 1],
                     [1, 2, 2, 1, 2, 1],
                     [1, 2, 2, 1, 2, 2]]
        res_burst = [[1, 0, 0, 1, 1, 1],
                     [1, 0, 0, 1, 1, 1],
                     [1, 0, 0, 1, 1, 1],
                     [1, 0, 0, 1, 1, 1],
                     [1, 0, 0, 0, 0, 1],
                     [1, 0, 0, 1, 0, 1],
                     [1, 0, 0, 1, 0, 0]]
        logic.WIDTH = 6
        logic.HEIGHT = 7
        logic.burst(4, 2, for_burst, [], [])
        for i in range(7):
            for j in range(6):
                self.assertEqual(for_burst[i][j], res_burst[i][j])

    def test_change_the_result(self):
        for_change = [[1, 0, 1, 1, 1, 1, 1, 1],
                      [1, 1, 0, 1, 1, 1, 0, 1],
                      [1, 1, 1, 1, 0, 1, 1, 0],
                      [1, 0, 1, 1, 1, 1, 1, 0],
                      [1, 1, 0, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 1, 0, 1, 1],
                      [1, 1, 0, 1, 1, 1, 1, 1]]
        logic.WIDTH = 8
        logic.HEIGHT = 7
        num = logic.recount_result(for_change)
        self.assertEqual(num, 10)

    def test_solutions_true(self):
        for_check = [[1, 1, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1],
                     [1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1],
                     [1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1]]
        logic.WIDTH = 6
        logic.HEIGHT = 6
        self.assertEqual(logic.is_there_cell_to_burst(for_check), True)

    def test_solutions_false(self):
        for_check = [[1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1],
                     [1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1],
                     [1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1]]
        logic.WIDTH = 6
        logic.HEIGHT = 6
        self.assertEqual(logic.is_there_cell_to_burst(for_check), False)


if __name__ == '__main__':
    unittest.main()