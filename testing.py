import sys, os, json
import numpy as np
from curve_util import Curve
import csv_util as csv

def motion_from_columns(rows, index, n_dimensions):
    points = []
    for row in rows:
        frame = float(row[0])
        point = []
        for i in range(n_dimensions):
            value = float(row[1 + index * n_dimensions + i])
            point.append(value)
        points.append(np.array(point))
    return points

def finite_differences(points):
    tangents = []
    n = len(points)
    for i in range(n):
        t = None
        if i == 0:
            t = points[1] - points[0]
        elif i == n - 1:
            t = points[-2] - points[-1]
        else:
            t = points[i] - points[i + 1]
        t = t / np.linalg.norm(t)
        tangents.append(t)
    return tangents


class ApproximatePoints(object):

    def __init__(self, points, max_n):
        self.points = points
        self.tangents = finite_differences(points)
        self.solution = None
        self.curves = None

        n = len(points)
        self.solution = [0, n-1]
        iters = 0
        while iters < max_n - 2:
            iters += 1
            largest_distance = 0
            index_of_largest_distance = -1
            for (i, j) in zip(self.solution[:-1], self.solution[1:]):
                distance, index = self.max_point_to_line_distance(self.points[i:j+1])
                if distance > largest_distance:
                    largest_distance = distance
                    index_of_largest_distance = index + i
            self.solution = sorted(self.solution + [index_of_largest_distance])
        
        self.curves = self.fit_curves_to_segments(self.solution)
        # error = self.sum_squared_distance_to_points(self.curves)

    def as_csv_row(self):
        row = []
        for curve in self.curves:
            row += curve.list_values()
        return row

    def max_point_to_line_distance(self, things):
        start = things[0]
        end = things[-1]
        es = end - start

        def distance_between_line_and_point(point):
            ps = point - start
            numerator = np.dot(ps, es)
            denominator = np.dot(es, es)

            if denominator == 0.0:
                return 999999999.0
            else:
                ratio = numerator / denominator
                return np.linalg.norm(ps - ratio * es)

        max_distance = 0.0
        index_of_max_distance = -1

        for i, p in enumerate(things):
            curr_distance = distance_between_line_and_point(p)
            if curr_distance > max_distance:
                max_distance = curr_distance
                index_of_max_distance = i

        return max_distance, index_of_max_distance

    def fit_curves_to_segments(self, keypoints):
        segments = []
        index_pairs = list(zip(keypoints[:-1], keypoints[1:]))
        for i, j in index_pairs:
            segment = self.points[i:j+1]
            segments.append(segment)

        curves = []
        for (segment, (i, j)) in zip(segments, index_pairs):
            tangent_from = self.tangents[i]
            tangent_to = self.tangents[j]
            curve = Curve.create_by_fitting_points(segment, tangent_from, tangent_to)
            curves.append(curve)
        return curves
        
    def sum_squared_distance_to_points(self, curves):
        samples = []
        for curve in curves:
            samples += curve.sample_at([0.25, 0.5, 0.75])

        nearest = []
        point_index = 0
        for sample in samples:
            p_after = self.points[point_index]
            while p_after[0] < sample[0]:
                point_index += 1
                p_after = self.points[point_index]
            p_before = self.points[point_index - 1]
            time_diff_points = p_after[0] - p_before[0]
            time_diff_sample = sample[0] - p_before[0]
            u = time_diff_sample / time_diff_points
            v = p_before + (p_after - p_before) * u
            nearest.append(v)
        
        return max(
            [
                np.linalg.norm(a - b)
                for (a, b) in zip(self.points, nearest)
            ]
        )

infile = sys.argv[1]
n_dimensions = int(sys.argv[2])
n = int(sys.argv[3])

name, ext = os.path.basename(infile).split(".")
dir = os.path.dirname(infile)
outfile = os.path.join(dir, f"{name}-filtered.{ext}")

header, rows = csv.read_header_and_rows_as_strings(infile)
n_points = int((len(header) - 1) / n_dimensions)

new_header = []
new_rows = []
for point_index in range(n_points):
    points = motion_from_columns(rows, point_index, n_dimensions)
    approx = ApproximatePoints(points, n)
    if point_index == 0:
        for curve in approx.curves:
            for key in ["a", "b", "c", "d"]:
                for i in range(n_dimensions):
                    new_header.append(f"{key}.{i}")
    row = approx.as_csv_row()
    new_rows.append(row)

csv.write_header_and_rows(outfile, new_header, new_rows)
print(outfile)