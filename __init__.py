import os
import typing as t

import pygame


class AssetLoader:
    def __init__(
            self,
            path: t.Union[str, bytes, os.PathLike],
            scale: bool = False,
            new_size: t.Union[int, t.Tuple[int, int]] = None,
            transparent_color: t.Union[pygame.Color, t.Tuple[int, int, int]] = (255, 255, 255),
            row_color: t.Union[pygame.Color, t.Tuple[int, int, int, int]] = (255, 255, 0, 255),
            col_color: t.Union[pygame.Color, t.Tuple[int, int, int, int]] = (0, 0, 255, 255),
            converter: t.Union[pygame.Surface.convert,
                               pygame.Surface.convert_alpha] = pygame.Surface.convert
    ) -> None:
        """Creates a 2D tuple of surfaces from the given sprite sheet.
        Each inner tuple will contain all sprites on the according row.

        :param path: path to the sprite sheet
        :param scale: determines whether each surface will be scaled
        :param new_size: scale of the surface, if a single integer is provided
                         the surface size will be multiplied by that number when scaling,
                         if a two element tuple is provided, it will scale to that size
        :param transparent_color: the color to set as transparent on the surfaces,
                                  use None to disable
        :param row_color: marker color to indicate rows
        :param col_color: marker color to indicate columns
        :param converter: specify to `convert` or to `convert_alpha`, doesn't convert
                          if None is provided, default is `convert`
        """
        self.sprites = []
        sprite_sheet = pygame.image.load(path)

        row_start = None
        col_start = 0
        sprite_sheet_width = sprite_sheet.get_width()

        for y in range(sprite_sheet.get_height()):
            color = sprite_sheet.get_at((0, y))
            if color == row_color:
                if row_start is None:
                    row_start = y
                    continue
                _sprites = []
                height = y - row_start - 1
                for x in range(sprite_sheet_width):
                    color = sprite_sheet.get_at((x, row_start))
                    if color == col_color:
                        width = x - col_start
                        rect = pygame.Rect(col_start, row_start + 1, width, height)
                        sprite = sprite_sheet.subsurface(rect)
                        if scale and new_size is not None:
                            if isinstance(new_size, int):
                                _w, _h = sprite.get_size()
                                sprite = pygame.transform.scale(sprite, (_w * new_size, _h * new_size))
                            elif isinstance(new_size, tuple) and len(new_size) == 2:
                                sprite = pygame.transform.scale(sprite, new_size)
                        if converter is not None:
                            sprite = converter(sprite)
                        if transparent_color is not None:
                            sprite.set_colorkey(transparent_color)
                        _sprites.append(sprite)
                        col_start = x
                self.sprites.append(tuple(_sprites))
                col_start = 0
                row_start = y
        self.sprites = tuple(self.sprites)

    def get_row(self, row) -> t.Tuple[pygame.Surface]:
        """Returns a tuple of all surfaces in the requested row."""

        return self.sprites[row]

    @staticmethod
    def flip_y(surfaces: t.Iterable[pygame.Surface], reverse: bool = True
               ) -> t.Tuple[t.Union[pygame.Surface, pygame.SurfaceType], ...]:
        """Returns a tuple of flipped surfaces on the y axis."""
        if reverse:
            return tuple(reversed([pygame.transform.flip(s, True, False) for s in surfaces]))
        elif not reverse:
            return tuple(pygame.transform.flip(s, True, False) for s in surfaces)

    @staticmethod
    def flip_x(surfaces: t.Iterable[pygame.Surface]
               ) -> t.Tuple[t.Union[pygame.Surface, pygame.SurfaceType], ...]:
        """Returns a tuple of flipped surfaces on the x axis."""

        return tuple(pygame.transform.flip(s, False, True) for s in surfaces)

    def get_combined(self
                     ) -> t.Tuple[t.Union[pygame.Surface, pygame.SurfaceType], ...]:
        """Returns all surfaces in a single tuple."""

        lst = []
        for tpl in self.sprites:
            lst.extend(tpl)
        return tuple(lst)
