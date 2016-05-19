import unittest
from PyQt5.QtCore import QPoint
import logic


class Test(unittest.TestCase):
    def test_get_neighbours(self):
        points1 = [QPoint(0 ,0), QPoint(0, 1), QPoint(1, 0)]
        country1 = logic.Country(points1)
        points2 = [QPoint(1, 1), QPoint(0, 1), QPoint(1, 0)]
        country2 = logic.Country(points2)
        points3 = [QPoint(1, 1), QPoint(1, 3), QPoint(3, 1)]
        country3 = logic.Country(points3)
        countries = [country1, country2, country3]
        logic.get_neighbours(countries)
        self.assertEqual(country1.neighbours, [country2])
        self.assertEqual(country2.neighbours, [country1])
        self.assertEqual(country3.neighbours, [])

    def test_is_there_intersection(self):
        edges = [((0, 0), (1, 1)), ((1, 0), (0, 1))]
        self.assertTrue(logic.is_there_intersection(edges))
        edges = [((0, 0), (1, 1)), ((1, 0), (2, 0))]
        self.assertFalse(logic.is_there_intersection(edges))

    def test_paint_graph(self):
        points1 = [QPoint(0 ,0), QPoint(0, 1), QPoint(1, 0)]
        country1 = logic.Country(points1)
        points2 = [QPoint(1, 1), QPoint(0, 1), QPoint(1, 0)]
        country2 = logic.Country(points2)
        countries = [country1, country2]
        logic.get_neighbours(countries)
        logic.paint_graph(countries)
        self.assertEqual(country1.num_of_color, 0)
        self.assertEqual(country2.num_of_color, 1)

    def test_paint_country(self):
        points = [QPoint(0 ,0), QPoint(0, 1), QPoint(1, 0)]
        country = logic.Country(points)
        logic.paint_country(country)
        self.assertEqual(country.num_of_color, 0)


if __name__ == '__main__':
    unittest.main()