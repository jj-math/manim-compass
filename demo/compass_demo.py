from manim import *
from manim_compass import *

class Scene_Name(Scene):
    def construct(self):

        compass = Compass().to_edge(LEFT)
        ruler = Ruler().to_edge(DOWN)
        pen = Pencil().to_corner(DR)
        self.play(
            FadeIn(compass,ruler,pen),
        )
        self.wait()

        line = Line(1.5*LEFT,1.5*RIGHT)
        A,B = line.get_start_and_end()

        self.play(
            PutRuler(ruler,A,B)
        )
        self.wait()

        self.play(
            MovePencilTipTo(pen,A)
        )
        self.wait()

        self.play(
            DrawPath(pen,line)
        )
        self.wait()

        self.play(
            PutRulerAway(ruler,point = 3.25*DOWN),
            PutPencilAway(pen,point = 3.25*DR + RIGHT)
        )
        self.wait()

        self.play(
            PutCompass(compass,niddle_pos=A,pen_pos=B)
        )

        arc1 = get_arc(
            niddle_pos=A,
            pen_pos=B,
            angle = PI/3 + 0.2
        )
        self.play(
            DrawArc(compass,arc1)
        )
        self.wait()

        self.play(
            PutCompass(compass,niddle_pos=B,pen_pos=A)
        )

        self.play(
            RotateCompass(compass,PI/3 + 0.2)
        )

        arc2 = get_arc(
            niddle_pos=B,
            pen_pos=compass.get_pen_tip(),
            angle = -TAU/3 - 0.4
        )
        self.play(
            DrawArc(compass,arc2)
        )
        self.wait()

        self.play(
            PutCompassAway(compass,point = 4.5*LEFT)
        )

        C = A + rotate_vector(B-A,PI/3)
        self.play(
            PutRuler(ruler,A,C),
            MovePencilTipTo(pen,C)
        )

        self.play(
            DrawPath(pen,Line(C,A))
        )
        self.play(
            PutRulerAway(ruler,point = 3.25*DOWN),
            PutPencilAway(pen,point = 3.25*DR + RIGHT)
        )

       

        
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