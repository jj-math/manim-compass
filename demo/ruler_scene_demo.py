from manim import *
from manim_compass import *

class Scene_Name(SingleRulerScene):
    def setup(self):
        super().setup()

    def construct(self):

        self.play(
            FadeIn(self.ruler,self.pencil)
        )

        A,B = LEFT,3*UR
        self.play(
            FadeIn(*[Dot(point) for point in [A,B]])
        )
        self.wait()
        
        line = self.draw_line_with_pencil(start = A, end = B, color = RED)
        self.wait()
        self.put_ruler_back()
        
        self.wait()

with tempconfig(
    {
        "quality": "low_quality", # low_quality   medium_quality   high_quality
        "preview": True,
        "tex_template":TexTemplateLibrary.ctex,
        # "renderer": "opengl"
    }
):
    Scene_Name().render()