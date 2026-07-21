__all__ = [
    'SingleRulerScene'
]
# from manim import *
from manim.mobject.geometry.line import Line
from manim.scene.moving_camera_scene import MovingCameraScene
from manim.animation.creation import Create
from manim.animation.composition import AnimationGroup
from manim.animation.transform import Restore
from manim.constants import *
from manim.utils.color import *

from ..compass import Ruler,Pencil
from ..animations import DrawPath

class SingleRulerScene(MovingCameraScene):
    def setup(self):
        self.ruler = Ruler(width = 0.4,length = 8).to_edge(DOWN)
        self.pencil = Pencil(height = 1).to_edge(RIGHT)
        self.pen_pos = self.pencil.get_center()
        self.ruler.save_state()

    def draw_line_with_pencil(self,start,end,added_anims = None,**kwargs):
        run_time = kwargs.pop('run_time',1.0)
        color = kwargs.pop('color',WHITE)
        stroke_width = kwargs.pop('stroke_width',4)
        line = Line(start,end,color = color,stroke_width = stroke_width)
        self.play(
            AnimationGroup(
                self.ruler.animate.set_ruler(start,end),
                self.pencil.animate.move_nid_to(start),
                lag_ratio = 1.0
            ),
            run_time = 0.5*run_time
        )
        anims = [
            DrawPath(self.pencil,line),
            Create(line),
        ]
        if added_anims is not None:
            anims.extend(added_anims)
        self.play(*anims, run_time = 0.5*run_time,**kwargs)
        return line
    
    def put_ruler_back(self,added_anims = None,run_time = 0.5,**kwargs):
        anims = [
            Restore(self.ruler),
            self.pencil.animate.move_to(self.pen_pos)
        ]
        if added_anims is not None:
            anims.extend(added_anims)
        self.play(*anims,run_time = run_time,**kwargs)