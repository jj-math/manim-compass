# from manim import *
__all__ = [
    'Pencil',
]
from pathlib import Path

from manim.mobject.svg.svg_mobject import SVGMobject
from manim.mobject.geometry.line import Line
from manim.constants import PI,ORIGIN

class Pencil(SVGMobject):
    '''铅笔'''
    def __init__(self, height = 2,angle = PI/4):
        super().__init__(
            file_name = Path(__file__).resolve().parent / "assets/pencil.svg",
            height = height
        )
        self.rotate(angle = -angle)
        self._nib = self.submobjects[3]

    def get_nib(self):
        '''获取笔尖的位置'''
        return self._nib.get_all_points()[7]
    
    def get_nid_vector(self):
        '''获取笔杆的方向'''
        return Line(
            self.get_nib(),
            self.submobjects[1].get_center()
        ).get_unit_vector()
    
    def move_nid_to(self,point = ORIGIN):
        '''平移铅笔: 使笔尖移动到 point'''
        self.shift(
            point - self.get_nib()
        )
        return self