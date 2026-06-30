from manim import *
from manim_compass import *

class Scene_Name(CompassScene):
    def setup(self):
        super().setup()

    def construct(self):

        self.play(
            FadeIn(self.compass,self.ruler,self.pencil)
        )

        line = Line(ORIGIN,3*RIGHT)
        A,B = line.get_start_and_end()
        C = A + 3*UR

        self.set_ruler(start = A,end = B)

        lineAB = self.draw_line(start = A,end = B+RIGHT)
        lineAC = self.draw_line(start = A,end = C)
        self.put_pencil_away(3*UR+RIGHT*2)
        self.put_ruler_aside(3.25*DOWN)

        arc1 = self.draw_arc(niddle_point=A,pen_point=B)
        self.put_compass_aside(5*LEFT)
        

        self.compass_move_niddle_tip_to(pos = A)
        self.split_cmpass_span(span = 2)
        arc2 = get_arc(
            niddle_pos = A,
            pen_pos = self.compass.get_pen_tip(),
            angle = PI/4
        )
        self.rotate_compass_about_niddle_tip(arc2)
        self.put_compass_aside(5*RIGHT)
        
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