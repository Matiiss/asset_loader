import tkinter as tk
from tkinter import filedialog
import pathlib

import pygame
from asset_loader import AssetLoader


def main():  # just for testing... obviously
    tk.Tk().withdraw()
    initial_dir = str(pathlib.Path(__file__).parent.parent)
    asset_path = filedialog.askopenfilename(initialdir=initial_dir)
    if not asset_path:
        exit()

    screen = pygame.display.set_mode((900, 500))
    x_pos, y_pos = 0, 0

    assets = AssetLoader(asset_path, scale=True, new_size=8)
    all_surfs = assets.get_combined()
    # all_surfs = assets.flip_y(all_surfs)
    all_surfs = assets.flip_x(all_surfs)

    for i, s in enumerate(all_surfs):
        screen.blit(s, (x_pos, y_pos))
        x_pos += 80
        if x_pos >= 800:
            x_pos = 0
            y_pos += 80
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()


if __name__ == '__main__':
    main()
