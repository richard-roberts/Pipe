import numpy as np
np.set_printoptions(precision=4, suppress=True)

class Curve(object):
    matrix = np.matrix([[-1.0,  3.0, -3.0,  1.0],
                        [ 3.0, -6.0,  3.0,  0.0],
                        [-3.0,  3.0,  0.0,  0.0],
                        [ 1.0,  0.0,  0.0,  0.0]])

    @staticmethod
    def coefficient_a(u):
        return np.power(1 - u, 3)

    @staticmethod
    def coefficient_b(u):
        return 3 * np.power(1 - u, 2) * u

    @staticmethod
    def coefficient_c(u):
        return 3 * (1 - u) * np.power(u, 2)

    @staticmethod
    def coefficient_d(u):
        return np.power(u, 3)

    @staticmethod
    def uniform_sample_set(n):
        return [i / (n - 1) for i in range(n)]

    @staticmethod
    def multiply_by_coefficient_matrix(vs):
        us = np.array([[v] for v in vs])

        def cubed():
            return us * us * us

        def squared():
            return us * us

        return np.hstack([cubed(), squared(), us, np.ones((len(vs), 1))]) * Curve.matrix

    def __init__(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.C = None

    def __str__(self):
        a = f"A:({self.a})"
        b = f"B:({self.b})"
        c = f"C:({self.c})"
        d = f"D:({self.d})"
        return "Curve[%s, %s, %s, %s]" % (a, b, c, d)

    def sample_at(self, us):
        samples = Curve.multiply_by_coefficient_matrix(us) * self.C
        points = []
        for i in range(samples.shape[0]):
            s = samples[i, :]
            point = np.array(s.tolist()[0])
            points.append(point)
        return points

    def sample_uniform(self, n):
        return self.sample_at(Curve.uniform_sample_set(n))

    def parameter_nearest_in_first_dimension(self, point, resolution):
        p0 = np.array(point[0])
        us = [i / (resolution - 1) for i in range(resolution)]
        U = Curve.multiply_by_coefficient_matrix(us)
        interps = [np.array([v[0]]) for v in U * self.C]
        distances = np.array(interps - p0)
        i = np.argmin((distances * distances).sum(1))
        u = i / (resolution - 1)
        return u

    def parameter_nearest_to_point(self, point, resolution):
        us = [i / (resolution - 1) for i in range(resolution)]
        U = Curve.multiply_by_coefficient_matrix(us)
        interps = U * self.C
        distances = np.array(interps - point)
        i = np.argmin((distances * distances).sum(1))
        u = i / (resolution - 1)
        return u

    def parameters_nearest_to_points(self, points, resolution):
        return [self.parameter_nearest_to_point(p, resolution) for p in points]

    def point_nearest_in_first_dimension(self, point, resolution):
        u = self.parameter_nearest_in_first_dimension(point, resolution)
        ret = self.sample_at([u])[0]
        return ret

    def point_nearest_to_point(self, point, resolution):
        u = self.parameter_nearest_to_point(point, resolution)
        ret = self.sample_at([u])[0]
        return ret

    def update(self):
        self.C = np.matrix(np.vstack((self.a, self.b, self.c, self.d)))

    def fit_to_points(self, points, t0, t1, us):
        self.a = points[0]
        self.d = points[-1]

        U = Curve.multiply_by_coefficient_matrix(us)
        c0 = np.array(U[:, 0])
        c1 = np.array(U[:, 1])
        c2 = np.array(U[:, 2])
        c3 = np.array(U[:, 3])

        # Setup matrix A
        p11 = np.sum(c1 ** 2)
        np.dot(t0, t1)
        p12 = np.dot(t0, t1) * np.sum(9 * c0 * c3)
        p21 = p12
        p22 = np.sum(c2 ** 2)
        A = np.matrix([[p11, p12], [p21, p22]])

        # Setup column b
        points_ab = [np.dot(t0, p) * u for (p, u) in zip(points, c1)]
        points_cd = [np.dot(t1, p) * u for (p, u) in zip(points, c2)]
        b1 = (np.sum(points_ab)
              - np.dot(t0, self.a) * np.sum(c1 * (c0 + c1))
              - np.dot(t0, self.d) * np.sum(c1 * (c2 + c3)))
        b2 = (np.sum(points_cd)
              - np.dot(t1, self.a) * np.sum(c2 * (c0 + c1))
              - np.dot(t1, self.d) * np.sum(c2 * (c2 + c3)))
        b = np.matrix([[b1], [b2]])

        # Solve for weights
        x = np.linalg.lstsq(A, b, rcond=None)
        x1 = x[0].item(0)
        x2 = x[0].item(1)

        # Set shape of curve to new points
        self.b = self.a + t0 * x1
        self.c = self.d + t1 * x2
        self.update()

    def fit_to_points_free(self, points, us):
        self.a = points[0]
        self.d = points[-1]
        C14 = np.matrix([ points[0], points[-1] ])
        anim = np.matrix(points)

        R = []
        for u in us:
            r_ = np.matrix([pow(u, 3), pow(u, 2), pow(u, 1), pow(u, 0)])
            r = r_ * Curve.matrix
            R.append(r)

        R = np.matrix(np.array(R))
        R23 = R[:, [1,2]]
        R14 = R[:, [0,3]]
        b = anim - R14 * C14
        
        c23,_resid,_rank,_s = np.linalg.lstsq(R23, b, rcond=None)
        self.b = c23[0,:]
        self.c = c23[1,:]
        self.update()

    def list_values(self):
        values = []
        values += list(self.a)
        values += list(self.b)
        values += list(self.c)
        values += list(self.d)
        return values

    @staticmethod
    def create_from_points(a, b, c, d):
        curve = Curve()
        curve.a = a
        curve.b = b
        curve.c = c
        curve.d = d
        curve.update()
        return curve

    @staticmethod
    def create_by_linear_interpolation(a, d):
        curve = Curve()
        curve.a = a
        curve.d = d
        curve.b = a + (d - a) * (1/3.0)
        curve.c = a + (d - a) * (2/3.0)
        curve.update()
        return curve

    @staticmethod
    def create_by_fitting_points(points, t0, t1):
        n = len(points)
        curve = Curve()
        us = Curve.uniform_sample_set(n)
        for i in range(4):
            curve.fit_to_points(points, t0, t1, us)
            us = curve.parameters_nearest_to_points(points, 100)
        return curve

    @staticmethod
    def create_by_fitting_points_free(points):
        n = len(points)
        curve = Curve()
        curve.fit_to_points_free(points, Curve.uniform_sample_set(n))
        return curve
