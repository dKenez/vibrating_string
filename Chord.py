from math import sin, cos, pi, exp


class Chord:
    __slots__ = ["length", "chord_coeff", "dampening", "res", "pinch_points", "fourier_res", "fx", "fx_fourier", "shape", "E_k", "F_k", "alpha_k"]

    def __init__(self, length, string_coeff, dampening, res, fourier_res, *pinch_points):
        self.length = length
        self.chord_coeff = string_coeff
        self.dampening = dampening
        self.res = res
        self.pinch_points = list(pinch_points)
        self.fourier_res = fourier_res
        self.fx = []

        self.get_pinch_points()
        self.init_shape_func()

        self.shape = self.chord_points_fourier(0)
        # self.shape = self.init_chord_points()

        self.E_k = []
        self.alpha_k = []

        self.get_coeffs()

    def refresh(self, t):
        self.shape = self.chord_points_fourier(t)

    def get_pinch_points(self):
        aux_list = self.pinch_points.copy()
        for point in aux_list:
            if not (0 < point[0] < self.length):  # and abs(point[1]) < 0.1):
                self.pinch_points.remove(point)

        self.pinch_points = sorted(self.pinch_points, key=lambda item: item[0])

        aux_list = self.pinch_points.copy()
        prev_x = 0
        for point in aux_list:
            if not point[0] > prev_x:
                self.pinch_points.remove(point)
            prev_x = point[0]

    def init_shape_func(self):
        prev_point = [0, 0]
        for point in self.pinch_points:
            a = (point[1] - prev_point[1]) / (point[0] - prev_point[0])
            b = point[1] - a * point[0]
            self.fx.append((prev_point[0], point[0], a, b))
            prev_point = point

        a = - prev_point[1] / (self.length - prev_point[0])
        b = - a * self.length
        self.fx.append((prev_point[0], self.length, a, b))

    def init_chord_points(self):
        dx = self.length / self.res
        x = 0
        yield 0, 0
        while x < self.length + (dx / 2):
            x += dx
            for func in self.fx:
                if func[0] < x <= func[1]:
                    yield x, func[2] * x + func[3]
                    break

    def get_coeffs(self):
        p = self.length
        c = self.chord_coeff
        res = self.fourier_res
        for k in range(1, res):
            self.alpha_k.append((k * pi * c) / p)

            b_k = 0
            for func in self.fx:
                # print(self.fx)
                i = func[0]
                j = func[1]
                a = func[2]
                b = func[3]
                # print("i: ", i)
                # print("j: ", j)
                # print("a: ", a)
                # print("b: ", b)
                b_k += (-k * pi * a * j * cos((k * pi * j) / p)) + (p * a * sin((k * pi * j) / p)) + (-k * pi * b * cos((k * pi * j) / p))
                # print("b_k: ", b_k)
                b_k += (k * pi * a * i * cos((k * pi * i) / p)) + (-p * a * sin((k * pi * i) / p)) + (k * pi * b * cos((k * pi * i) / p))
                # print("b_k: ", b_k)
            b_k *= 2/((pi ** 2) * (k ** 2))
            # print("b_k: ", b_k)
            self.E_k.append(b_k)

    def chord_points_fourier(self, t):
        for i in range(self.res):
            x = (self.length / self.res) * i
            y = 0
            for k in range(0, self.fourier_res - 1):
                y += self.E_k[k] * cos(self.alpha_k[k] * t) * sin((self.alpha_k[k] * x) / self.chord_coeff)
            y *= exp(-self.dampening * t)
            yield x, y



        # dx = self.length / self.res
        # x = 0
        # yield 0, 0
        # while x < self.length:
        #     x += dx
        #     y = 0
        #
