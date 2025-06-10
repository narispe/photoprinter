import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt
import parameters as p
from tqdm import tqdm
import time

# rutina = capa eje y0 |-> capa eje x0 |-> capa eje y1 ...
# regular intensidad por exposicon de tiempo o por otro control de laser

# img[0] -> vertical imagen
# img[1] -> horizontal de imagen


class Routine:

    def __init__(self, img_map: ndarray, mode: int, name: str):
        self.name = name
        self.img_map = img_map.astype(int)
        self.size = img_map.shape[0]*img_map.shape[1]
        self.rel_route = self.generate_route(self.img_size)
        self.frame_offset = np.array([(p.PROJ_LENGTH-img_map.shape[1])/2,
                                      (p.PROJ_WIDTH-img_map.shape[0])/2],
                                     dtype=int)
        if mode == 0:  # tiempo cte de exp & control exp por pwm laser
            self.delays = p.EXP_TIME * np.ones((self.size,)).astype(int)
            self.pwms = np.reshape(img_map, (self.size,))
        elif mode == 1:  # tiempo variable de exp & laser cte
            self.pwms = np.ones((self.size,)).astype(int)
            self.delays = p.EXP_TIME/255 * np.reshape(img_map, (self.size,))

    @property
    def img_size(self):
        return (self.img_map.shape[1], self.img_map.shape[0])

    @property
    def canvas_size(self):
        return (self.canvas_map.shape[1], self.canvas_map.shape[0])

    @property
    def route(self):  # - HEAD
        points = self.rel_route+self.frame_offset
        return points.astype(int)

    @property
    def frame_points(self):
        return np.array([[0, 0],
                         [0, max(self.route[:, 1])],
                         [max(self.route[:, 0]), max(self.route[:, 1])],
                         [max(self.route[:, 0]), 0]], dtype=int) + self.frame_offset

    @property
    def duration(self):
        return self.size*(p.STEPPER_T_MIN+p.EXP_TIME)/1e9/60

    @property
    def canvas_map(self):
        frame = np.zeros((p.PROJ_WIDTH, p.PROJ_LENGTH))
        frame[self.frame_offset[1]:self.frame_offset[1]+self.img_map.shape[0],
              self.frame_offset[0]:self.frame_offset[0]+self.img_map.shape[1]] = self.img_map
        return frame

    def generate_route(self, dim):  # zig-zag}
        x_max, y_max = dim
        route = []
        for x in tqdm(range(x_max + 1), desc="Creating routine"):
            y_range = range(y_max + 1) if x % 2 == 0 else range(y_max, -1, -1)
            route.extend([[x, y] for y in y_range])
        print(np.array(route, dtype=int))
        return np.array(route, dtype=int)

    def show_im(self):
        plt.title(f"{self.name} - {self.img_size}")
        plt.xlabel("x [pix]")
        plt.ylabel("y [pix]")
        plt.imshow(self.img_map, cmap="grey")
        plt.show()

    def show_canvas(self):
        plt.title(f"{self.name} - {self.canvas_size}")
        plt.xlabel("x [pix]")
        plt.ylabel("y [pix]")
        plt.imshow(self.canvas_map, cmap="grey")
        plt.show()

    def simulate_route(self):
        pass


if __name__ == "__main__":
    from Image import Image
    t = Image()
    r = t.generate_routine(0)
    r.show_im()
    r.show_canvas()
    r.simulate_route()
