import cv2
from os import path
import numpy as np
import easygui
import matplotlib.pyplot as plt
from Routine import Routine
import parameters as p

# img[0] -> vertical imagen
# img[1] -> horizontal de imagen


class Image:

    def __init__(self, rotation=0, adjust=0):
        self.file = easygui.fileopenbox(title="Select an image",
                                        default="*.jpg",
                                        filetypes=[["*.jpg", "*.png",
                                                    "Images files"]])
        self.file_name = path.basename(self.file)
        self.arr = np.fromfile(self.file, np.uint8)
        self.full_cmap = cv2.imdecode(self.arr, cv2.IMREAD_COLOR_RGB)
        self.rotate(rotation)
        if adjust == 1:
            self.adjust_undersize()
        # easygui.msgbox(f"Image {self.file_name} uploaded",
        #                title="Photo-printer")

    @property
    def cmap(self):
        return self.full_cmap[:, :, 2]

    def rotate(self, rotation: int):  # 1->90°counterclockwise -1->90°clockwise
        if rotation >= 0:
            self.full_cmap = np.rot90(self.full_cmap, rotation % 3)
        else:
            self.full_cmap = np.rot90(self.full_cmap, rotation % 3 + 1)
        self.adjust_oversize()

    def adjust_oversize(self):
        ratio_x = self.size[0]/p.PROJ_LENGTH
        ratio_y = self.size[1]/p.PROJ_WIDTH
        if ratio_x > ratio_y and self.size[0] > p.PROJ_LENGTH:
            self.full_cmap = cv2.resize(self.full_cmap,
                                        (p.PROJ_LENGTH, int(self.size[1]/self.size[0]*p.PROJ_LENGTH)))
        elif ratio_x < ratio_y and self.size[1] > p.PROJ_WIDTH:
            self.full_cmap = cv2.resize(self.full_cmap,
                                        (int(self.size[0]/self.size[1]*p.PROJ_WIDTH), p.PROJ_WIDTH))
        elif self.size[1] > p.PROJ_WIDTH:
            self.full_cmap = cv2.resize(self.full_cmap,
                                        (int(self.size[0]/self.size[1]*p.PROJ_WIDTH), p.PROJ_WIDTH))

    def adjust_undersize(self):
        ratio_x = self.size[0]/p.PROJ_LENGTH
        ratio_y = self.size[1]/p.PROJ_WIDTH
        if ratio_x > ratio_y and self.size[0] < p.PROJ_LENGTH:
            self.full_cmap = cv2.resize(self.full_cmap,
                                        (p.PROJ_LENGTH, int(self.size[1]/self.size[0]*p.PROJ_LENGTH)))
        elif ratio_x > ratio_y and self.size[1] < p.PROJ_WIDTH:
            self.full_cmap = cv2.resize(self.full_cmap,
                                        (int(self.size[0]/self.size[1]*p.PROJ_WIDTH), p.PROJ_WIDTH))
        elif self.size[1] < p.PROJ_WIDTH:
            self.full_cmap = cv2.resize(self.full_cmap,
                                        (int(self.size[0]/self.size[1]*p.PROJ_WIDTH), p.PROJ_WIDTH))

    def show(self):
        plt.title(f"{self.file_name} - {self.size}")
        plt.xlabel("x [pix]")
        plt.ylabel("y [pix]")
        plt.imshow(self.full_cmap)
        plt.show()

    @property
    def size(self):
        return (self.full_cmap.shape[1], self.full_cmap.shape[0])

    @property
    def ratio(self):
        return self.size[0]/self.size[1]

    @property
    def cmap_norm(self):
        return (1/255)*self.full_cmap

    def generate_routine(self, mode: int):
        return Routine(self.cmap, mode, self.file_name)


if __name__ == "__main__":
    img = Image(rotation=1, adjust=1)
    print(p.PROJ_LENGTH, p.PROJ_WIDTH)
    img.show()
