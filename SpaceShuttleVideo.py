
from manimlib.imports import *
import os
import pyclbr

global  speedcolor
global  carcolor
global  dragcolor

speedcolor=BLUE
carcolor=GREEN
dragcolor=RED

class Intro(Scene):
    def construct(self):
        
        Maintext=TextMobject("Physics in action!")
        Maintext.scale(2)
        Maintext.move_to(UP)
        belowtext=TextMobject("Newton's 2nd law and separation of variables")
        belowtext.next_to(Maintext,2*DOWN)
        title=VGroup(Maintext,belowtext)
        self.wait(0.5)
        self.play(Write(title))
        self.wait(4)        
        
class Setup(Scene):
    
    
    def construct(self):
        
        Text1=TextMobject("Imagine a ","{Space Shuttle}"," with ","{speed $\\vec{v}$}"," landing.") 
        Text2=TextMobject("It gets slowed down by ","{air resistance}"," from a ","{parachute}",".")
        Text1.set_color_by_tex_to_color_map({
            "{Space Shuttle}": carcolor, "{speed $\\vec{v}$}":speedcolor,"{air resistance}": dragcolor,"{parachute}": dragcolor})
        Text2.set_color_by_tex_to_color_map({
            "{Space Shuttle}": carcolor, "{speed $\\vec{v}$}":speedcolor,"{air resistance}": dragcolor,"{parachute}": dragcolor})
        Text2.next_to(Text1,DOWN)
        r=VGroup(Text1,Text2)
        self.play(Write(r))
        self.wait(1.5)
        self.play(ApplyMethod(r.to_edge,UP))
        #self.wait(1)
        
        hullheight=1/2
        hullwidth=3/2/1.5
        wheelradius=0.4/2
        Startcorner=np.array([-4,-1,0])
        P1=np.array([0,0,0])+Startcorner
        P2=np.array([0,hullheight,0])+Startcorner
        P3=np.array([hullwidth,hullheight,0])+Startcorner
        P4=np.array([hullwidth+2,0,0])+Startcorner
        
        ShuttleHull=Polygon(P1,P2,P3,P4,P1,color=carcolor)
        
        wheel1=Circle(radius=wheelradius,color=carcolor)
        wheel1.move_to(ShuttleHull.get_center()+DOWN*hullheight/2+LEFT)
        wheel2=Circle(radius=wheelradius,color=carcolor)
        wheel2.move_to(ShuttleHull.get_center()+DOWN*hullheight/2+RIGHT)
        
        
        Chuteangle=PI/6
        S1=np.array([0,0,0])
        S2=np.array([-np.cos(Chuteangle),np.sin(Chuteangle),0])
        S3=np.array([-np.cos(Chuteangle),-np.sin(Chuteangle),0])
        S4=np.array([-np.cos(Chuteangle),0,0])
 
#        chutearc=ArcBetweenPoints(S2,S3,color=dragcolor)
       

        parachute=Polygon(S1,S2,S3,S1,S4,color=dragcolor)
        
        chutearc=Arc(arc_center=S4,radius=np.sin(Chuteangle),start_angle=PI/2,angle=PI,color=dragcolor)
        chutearc.move_arc_center_to(S4)
        FullCraft=Mobject()
        FullCraft.add(ShuttleHull,wheel1,wheel2)
        FullChute=Mobject()
        FullChute.add(chutearc,parachute)
        
        
        
                
        speedlabel=TexMobject("\\vec{v}",color=speedcolor)
        speedarrow=Arrow(FullCraft.get_center()+np.array([1.5,0,0]),FullCraft.get_center()+np.array([4,0,0]),color=speedcolor)
        speedlabel.next_to(speedarrow,UP,buff=SMALL_BUFF)
        speedvector=Mobject()
        speedvector.add(speedarrow,speedlabel)
        
        
        draglabel=TexMobject("\\vec{F_d}","=-k","\\vec{v}","t")
        draglabel.set_color_by_tex_to_color_map({
            "{F_d}": dragcolor,
            "{v}":speedcolor})
        
        dragarrow=Arrow(FullChute.get_center()+np.array([1.5,0,0]),FullChute.get_center()+np.array([1.5-2.5,0,0]),color=dragcolor)
        draglabel.next_to(dragarrow,UP,buff=SMALL_BUFF)
        dragvector=Mobject()
        dragvector.add(dragarrow,draglabel)
        
        
        
        def update_chute(FullChute):
            FullChute.next_to(FullCraft,LEFT)
            
        def update_speedvector(speedvector):
            speedvector.next_to(FullCraft,RIGHT)
            
        def update_dragvector(dragvector):
            dragvector.next_to(FullChute,LEFT)
        
    
        FullChute.add_updater(update_chute)
        speedvector.add_updater(update_speedvector)
        dragvector.add_updater(update_dragvector)
        
        self.add(dragvector)        
        self.add(speedvector)
        self.add(FullCraft)
        self.add(FullChute)


        self.play(ShowCreation(FullCraft),ShowCreation(FullChute),ShowCreation(speedvector),ShowCreation(dragvector))
        
        CONFIG={"rate_func":exponential_decay}
        self.play(FullChute.scale,3.5,dragvector.scale,0.5 , speedvector.scale,0.1, FullCraft.to_edge, RIGHT,run_time=3.5)
        CONFIG={"rate_func":smooth}
        self.wait(3)
        
        Text3=TextMobject("Drag force, $\\vec{F_d}$"," depends on ","{speed}"," and time,") 
        Text4=TextMobject("because the ","{parachute}"," takes time to deploy.")
        Text3.set_color_by_tex_to_color_map({
            "{Space Shuttle}": carcolor, "{speed}":speedcolor,"{F_d}": dragcolor,"{parachute}": dragcolor})
        Text4.set_color_by_tex_to_color_map({
            "{Space Shuttle}": carcolor, "{speed $\\vec{v}$}":speedcolor,"{air resistance}": dragcolor,"{parachute}": dragcolor})
        Text4.next_to(Text3,DOWN)
        r2=VGroup(Text3,Text4)
        r2.move_to(Text1)
        self.play(Transform(r,r2))
        self.wait(3)
        
        questiontext=TexMobject("\\text{How does }","\\vec{v}","\\text{ change with time?}")
        questiontext.set_color_by_tex_to_color_map({
            "{v}": speedcolor})
        rectangle = Rectangle(height=0.75, width=7,fill_color=BLACK, fill_opacity=1, color=GOLD_A)
        
        questiontext.move_to(rectangle.get_center())
        
        self.play(ShowCreation(rectangle),Write(questiontext),run_time=3)
        self.wait(3)
        
        
        
class N2(Scene):
    def construct(self):
        
        hullheight=1/2
        hullwidth=3/2/1.5
        wheelradius=0.4/2
        Startcorner=np.array([-1,-3,0])
        P1=np.array([0,0,0])+Startcorner
        P2=np.array([0,hullheight,0])+Startcorner
        P3=np.array([hullwidth,hullheight,0])+Startcorner
        P4=np.array([hullwidth+2,0,0])+Startcorner
        
        ShuttleHull=Polygon(P1,P2,P3,P4,P1,color=carcolor)
        
        wheel1=Circle(radius=wheelradius,color=carcolor)
        wheel1.move_to(ShuttleHull.get_center()+DOWN*hullheight/2+LEFT)
        wheel2=Circle(radius=wheelradius,color=carcolor)
        wheel2.move_to(ShuttleHull.get_center()+DOWN*hullheight/2+RIGHT)
        
        
        Chuteangle=PI/6
        S1=np.array([0,0,0])
        S2=np.array([-np.cos(Chuteangle),np.sin(Chuteangle),0])
        S3=np.array([-np.cos(Chuteangle),-np.sin(Chuteangle),0])
        S4=np.array([-np.cos(Chuteangle),0,0])
 
#        chutearc=ArcBetweenPoints(S2,S3,color=dragcolor)
       

        parachute=Polygon(S1,S2,S3,S1,S4,color=dragcolor)
        
        chutearc=Arc(arc_center=S4,radius=np.sin(Chuteangle),start_angle=PI/2,angle=PI,color=dragcolor)
        chutearc.move_arc_center_to(S4)
        FullCraft=Mobject()
        FullCraft.add(ShuttleHull,wheel1,wheel2)
        FullChute=Mobject()
        FullChute.add(chutearc,parachute)
        FullChute.next_to(FullCraft,LEFT)
        
        
                
        speedlabel=TexMobject("\\vec{v}",color=speedcolor)
        speedarrow=Arrow(FullCraft.get_center()+np.array([1.5,0,0]),FullCraft.get_center()+np.array([4,0,0]),color=speedcolor)
        speedlabel.next_to(speedarrow,UP,buff=SMALL_BUFF)
        speedvector=Mobject()
        speedvector.add(speedarrow,speedlabel)
        
        
        draglabel=TexMobject("\\vec{F_d}","=-k","\\vec{v}","t")
        draglabel.set_color_by_tex_to_color_map({
            "{F_d}": dragcolor,
            "{v}":speedcolor})
        
        dragarrow=Arrow(FullChute.get_center()+np.array([1.5,0,0]),FullChute.get_center()+np.array([1.5-2.5,0,0]),color=dragcolor)
        draglabel.next_to(dragarrow,UP,buff=SMALL_BUFF)
        dragvector=Mobject()
        dragvector.add(dragarrow,draglabel)
        dragvector.next_to(FullChute,LEFT)  
        
        self.play(ShowCreation(FullCraft),ShowCreation(FullChute),ShowCreation(speedvector),ShowCreation(dragvector))
        
        
        Headtext=TextMobject("Newton's 2nd law:")
        Headtext.move_to(3*UP+3.5*LEFT)
        N2eq1=TexMobject("\\sum \\vec{F} = m \\vec{a}")
        N2eq1.next_to(Headtext,DOWN)
        
        
        N2eq2=TexMobject("{\\vec{F_d}}","= m \\vec{a} ")#= m \\frac{d\\vec{v}}{dt^2} 
        N2eq2.next_to(N2eq1,DOWN)
        N2eq2.set_color_by_tex_to_color_map({
            "{F_d}": dragcolor})
        
        
        N2eq3=TexMobject("-k","\\vec{v}","t= m ","{d ","\\vec{v}","\\over dt","} ")#= m \\frac{d\\vec{v}}{dt^2} 
        N2eq3.next_to(N2eq2,DOWN)
        N2eq3.set_color_by_tex_to_color_map({
            "{v}": BLUE})
        
        N2eq4=TexMobject("-k","{v}","\\hat{x}t= m\\hat{x}","{d ","{v}","\\over dt","} ")#= m \\frac{d\\vec{v}}{dt^2} 
        N2eq4.next_to(N2eq2,DOWN)
        N2eq4.set_color_by_tex_to_color_map({
            "{v}": BLUE})
        
        N2eq5=TexMobject("-k","{v}","t= m","{d ","{v}","\\over dt","} ")#= m \\frac{d\\vec{v}}{dt^2} 
        N2eq5.next_to(N2eq2,DOWN)
        N2eq5.set_color_by_tex_to_color_map({
            "{v}": BLUE})
        
        N2eq6=TexMobject("m","{d ","{v}","\\over dt","} ","=-k","{v}","t")#= m \\frac{d\\vec{v}}{dt^2} 
        N2eq6.next_to(N2eq2,DOWN)
        N2eq6.set_color_by_tex_to_color_map({
            "{v}": BLUE})
        
        N2eq7=TexMobject("{d ","{v}","\\over dt","} ","=- \\frac{k}{m} ","{v}","t")#= m \\frac{d\\vec{v}}{dt^2} 
        N2eq7.next_to(N2eq2,DOWN)
        N2eq7.set_color_by_tex_to_color_map({
            "{v}": BLUE})
        
        
        
        
        
       
        
        
        
        
        
        
        self.play(Write(Headtext), Write(N2eq1)) #N2 draws on screen
        self.wait(5) #"It says: How much the ball changes its speed depends on all the forces acting on it"
        self.play(Write(N2eq2))
        self.wait(5)# The Gravity and Drag on the ball are given by these expressions
        self.play(Write(N2eq3))
        self.wait(5)# Let us write the vectors as the product of their magnitude and directions
        self.play(Transform(N2eq3,N2eq4))
        self.wait(5)#Let us look only at the magnitudes since they are all in the y-direction 
        self.play(Transform(N2eq3,N2eq5))
        self.wait(2)#Rearrange this to isolate the derivative
        self.play(Transform(N2eq3,N2eq6))
        self.wait(3)
        self.play(Transform(N2eq3,N2eq7))
        self.wait(2) #Let us tidy things up a bit
#               


        solvetext=TextMobject("Separate variables!")
        solvetext.move_to(3*UP+3.5*RIGHT)
        N2eq8=TexMobject("{d ","{v}","\\over dt}","=-\\frac{k}{m} ","{v}","t")#= m \\frac{d\\vec{v}}{dt^2} 
        N2eq8.next_to(solvetext,DOWN)
        N2eq8.set_color_by_tex_to_color_map({
            "{v}": BLUE})
        
        
        N2eq9=TexMobject("{d ","{v}","\\over ","{v}","}=- \\frac{k}{m} t dt")#= m \\frac{d\\vec{v}}{dt^2} 
        N2eq9.next_to(N2eq8,DOWN)
        N2eq9.set_color_by_tex_to_color_map({
            "{v}": speedcolor})
        
        
        N2eq10=TexMobject("\int^","{v}","_{v_0}{d ","{v}","\\over ","{v}"," } = -\\frac{k}{m} \int_{0}^{t} t dt")        
        N2eq10.next_to(N2eq9,DOWN)
        N2eq10.set_color_by_tex_to_color_map({
            "{v}": speedcolor})
    
        
        N2eq11=TexMobject("\ln \\left({","{v}","\\over v_0}  \\right) = -{k\\over 2m}  t^2")    #{-v_t d ","{u}","\\over ","{u}"," }     
        N2eq11.next_to(N2eq9,DOWN)
        N2eq11.set_color_by_tex_to_color_map({"{v}": BLUE, "{u}":GREEN}) 
        
        N2eq12=TexMobject("{v}","(t)=v_0\\exp \\left( -{k\\over 2m}  t^2 \\right) ")    #{-v_t d ","{u}","\\over ","{u}"," }     
        N2eq12.next_to(N2eq9,DOWN)
        N2eq12.set_color_by_tex_to_color_map({"{v}": BLUE, "{u}":GREEN}) 
        
        
    
        self.play(Write(solvetext), Write(N2eq8)) #N2 draws on screen
        self.wait(5) #"It says: How much the ball changes its speed depends on all the forces acting on it"
        self.play(Write(N2eq9))
        self.wait(5)# The Gravity and Drag on the ball are given by these expressions
        self.play(Write(N2eq10))
        self.wait(5)
        self.play(Transform(N2eq10,N2eq11))
        self.wait(5)
        self.play(Transform(N2eq10,N2eq12))
        self.wait(5)
        cleartext=TexMobject("   ")
        self.play(ApplyMethod(N2eq10.move_to,UP*2.25),Transform(N2eq9,cleartext),Transform(N2eq8,cleartext),Transform(solvetext,cleartext),Transform(N2eq3,cleartext),Transform(N2eq2,cleartext),Transform(N2eq1,cleartext),Transform(Headtext,cleartext))
        self.wait(2)
        
        Toptext=TextMobject("{Speed}"," decreases as a Gaussian.")
        Toptext.to_edge(UP)
        Toptext.set_color_by_tex_to_color_map({"{Speed}": BLUE}) 
        
        self.play(Write(Toptext))
        self.wait(3)
        chartext=TextMobject("Characteristic time:")
        chartext.move_to(DOWN*0.75)
        tautext=TexMobject("\\tau = \\sqrt{2m \\over k}")
        tautext.next_to(chartext,DOWN)
        
        self.play(Write(chartext))
        self.play(Write(tautext))
        
        N2eq13=TexMobject("{v}","(t)=v_0\\exp \\left( -{t^2\\over \\tau^2}   \\right) ")    #{-v_t d ","{u}","\\over ","{u}"," }     
        N2eq13.move_to(2.25*UP)
        N2eq13.set_color_by_tex_to_color_map({"{v}": BLUE, "{u}":GREEN}) 
        
        self.play(Transform(N2eq10,N2eq13))
        self.wait(3)
        
        questiontext=TextMobject("Let's graph it!")
        questiontext.move_to(UP*0.5)
        box = Rectangle(height=0.75, width=5,fill_color=BLACK, fill_opacity=1, color=GOLD_A)
        box.move_to(UP*0.5)
        self.play(ShowCreation(box),Write(questiontext),run_time=3)
                
        
        self.wait(3)


class VGraph(GraphScene):
    CONFIG = {
        "x_min" : 0,
        "x_max" : 3,
        "y_min" : 0,
        "y_max" : 1.3,
        "graph_origin" : DL*3+2*LEFT ,
        "function_color" : RED ,
        "axes_color" : GOLD_E,
        "y_tick_frequency" : 0.1 ,
        "y_labeled_nums" : range(0,2),
        "y_label_decimal":3,
        "y_axis_label": "${v \\over v_0}$",
        "y_label_direction":2*LEFT,
        "exclude_zero_label": True,


        "x_labeled_nums" :range(0,4,1),        
        "x_axis_label": "${t\\over\\tau}$",
        "x_label_direction":DOWN ,
        
                        

    }   

    def construct(self):
        ### Set up the graph ###
        self.setup_axes(animate=True)
        
        N2eq13=TexMobject("{v}","(t)=v_0\\exp \\left( -{t^2\\over \\tau^2}   \\right) ")    #{-v_t d ","{u}","\\over ","{u}"," }     
        N2eq13.move_to(3.25*UP)
        N2eq13.set_color_by_tex_to_color_map({"{v}": BLUE, "{u}":GREEN}) 
    
        tautext=TexMobject("\\tau = \\sqrt{2m \\over k}")
        tautext.next_to(N2eq13,DOWN)
        
    
        self.play(Write(N2eq13),Write(tautext))
    
        func_graph=self.get_graph(self.vfunc,color=BLUE)
        graph_lab = self.get_graph_label(func_graph,label="v(t)" )
        self.play(ShowCreation(func_graph),Write(graph_lab))
        self.wait(5)
        
        bigmsmallc=TextMobject("Small m or big k:")
        bigmsmallc.set_color_by_tex_to_color_map({"Small m or big k:": RED})
        bigmsmallc.next_to(tautext,DOWN)
        
        cartext1=TextMobject("Shuttle slows down fast!")
        cartext1.set_color_by_tex_to_color_map({"Shuttle slows down fast!": RED})
        cartext1.next_to(tautext,DOWN)
        
        self.play(Write(bigmsmallc))
        self.wait(3)
        func_graph2=self.get_graph(self.vfunc2,color=RED)
        self.play(ShowCreation(func_graph2))
        self.wait(3)
        self.play(Transform(bigmsmallc,cartext1))
        self.wait(5)
        
        
        smallmsbigc=TextMobject("Big m or small k:")
        smallmsbigc.set_color_by_tex_to_color_map({"Big m or small k:": GREEN})
        smallmsbigc.next_to(tautext,DOWN*1.5)

        cartext2=TextMobject("Shuttle stays")
        cartext2.set_color_by_tex_to_color_map({"Shuttle stays": GREEN})
        cartext2.next_to(tautext,DOWN*1.5)

        cartext3=TextMobject("in motion longer!")
        cartext3.set_color_by_tex_to_color_map({"in motion longer!": GREEN})
        cartext3.next_to(cartext2,DOWN)
        
        rr=VGroup(cartext2,cartext3)

        self.play(Transform(bigmsmallc,smallmsbigc))
        self.wait(3)
        func_graph3=self.get_graph(self.vfunc3,color=GREEN)
        self.play(ShowCreation(func_graph3))
        self.play(Transform(bigmsmallc,rr))
        self.wait(5)
        
        questiontext=TextMobject("Thanks for watching!")
        #questiontext.move_to(UP*0.5)
        box = Rectangle(height=0.75, width=7,fill_color=BLACK, fill_opacity=1, color=GOLD_A)
        #box.move_to(UP*0.5)
        box.move_to(UP*0.25)
        questiontext.move_to(UP*0.25)
        
        self.play(ShowCreation(box),Write(questiontext),run_time=3)
        self.wait(5)
        
    
    def vfunc(self,t):
        return np.exp(-t**2)
    def vfunc2(self,t):
        return np.exp(-(t/0.2)**2)
    def vfunc3(self,t):
        return np.exp(-(t/5)**2)
    
