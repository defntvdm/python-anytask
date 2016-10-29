#!/usr/bin/env python3

from PyQt5.QtGui import QPolygon

class Country(QPolygon):
    def __init__(self, points):
        super().__init__(points)
        self.neighbours = []
        self.variants_of_color = [0, 1, 2, 3]
        self.num_of_color = -1

def get_neighbours(countries):
    for country1 in countries:
        for country2 in countries:
            num = 0
            if country1 == country2:
                continue
            else:
                for point1 in country1:
                    for point2 in country2:
                        if point1 == point2:
                            num += 1
                        if num == 2:
                            country1.neighbours.append(country2)

def paint_graph(countries):
    for country in countries:
        paint_country(country)

def paint_country(main_country):
    if main_country.num_of_color == -1:
        color = main_country.variants_of_color[0]
        main_country.num_of_color = color
        for country in main_country.neighbours:
            if color in country.variants_of_color:
                country.variants_of_color.remove(color)
        for country in main_country.neighbours:
            paint_country(country)

def is_there_intersection(edges):
    for line1 in edges:
        for line2 in edges:
            point1 = line1[0]
            point2 = line1[1]
            point3 = line2[0]
            point4 = line2[1]
            dir1 = (point2[0] - point1[0], point2[1] - point1[1])
            dir2 = (point4[0] - point3[0], point4[1] - point3[1])

            a1 = -dir1[1]
            b1 = dir1[0]
            d1 = -(a1*point1[0] + b1*point1[1])

            a2 = -dir2[1]
            b2 = dir2[0]
            d2 = -(a2*point3[0] + b2*point3[1])

            seg1_line2_start = a2*point1[0] + b2*point1[1] + d2
            seg1_line2_end = a2*point2[0] + b2*point2[1] + d2

            seg2_line1_start = a1*point3[0] + b1*point3[1] + d1
            seg2_line1_end = a1*point4[0] + b1*point4[1] + d1

            if not(seg1_line2_start * seg1_line2_end >= 0 or seg2_line1_start * seg2_line1_end >= 0):
                return True
    return False

