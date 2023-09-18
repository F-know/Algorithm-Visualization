from manimlib import *
import numpy
import random
import functools
import queue


class Welzl(Scene):
    def construct(self) -> None:
        _H=TexText("Welzl").set_height(1).set_color(YELLOW_A)
        self.add(_H)
        self.wait(2)
        _H.generate_target().scale(0.3).to_corner(UR)
        self.play(MoveToTarget(_H))

        random.seed(2)
        n=33
        sz=0.23
        min_dis=0.55
        xscd=2
        wg=1
        _buff=0.02
        _spd=1
        _spd_max=1/3
        _spd_k=0.95
        dark=0.25

        def add(mod):
            self.add(*(its for its in mod))
        def remove(mod):
            self.remove(*(its for its in mod))
        def play(ag, spd=_spd):
            self.play(
                *(its for its in ag),
                run_time=spd
            )
        def wait(spd):
            self.wait(spd)

        pt=[]
        def dis(i,j):
            dx=i[0]-j[0]
            dy=i[1]-j[1]
            return dx*dx+dy*dy
        while len(pt)<n:
            now=[random.randint(-30,30),random.randint(-300,300)]
            now[0]=now[0]*3/20
            now[1]=now[1]/100
            if dis(now,[0,0])>3*3:continue
            suc=True
            for j in range(len(pt)):
                if dis(pt[j],now)<min_dis:
                    suc=False
                    break
            if suc:pt.append(now)

        random.shuffle(pt)

        _pt=VGroup(
            *(
                Dot([x,y,0]).set_height(sz)
                for [x,y] in pt
            )
        )
        play([FadeIn(_pt)])
        play([
            *(
                _pt[i].animate.set_opacity(dark)
                for i in range(1,n)
            )
        ],_spd*2)
        res=[pt[0][0],pt[0][1],sz*0.75]
        cir=Circle().move_to([pt[0][0],pt[0][1],0]).set_height(sz*0.75*2).set_color(BLUE)
        play([
            FadeIn(cir)
        ])
        # print([res[0],res[1],0])
        def upd(lst):
            tmp=Circle().move_to([res[0],res[1],0]).set_height(res[2]*2).set_color(BLUE)
            wait(_spd/2)
            play([
                Transform(cir, tmp),
                *(
                    _pt[i].animate.set_opacity(dark)
                    for i in range(n) if out(i) and not i in lst
                ),
                *(
                    _pt[i].animate.set_opacity(1)
                    for i in range(n) if not out(i) or i in lst
                ),
            ],_spd*2)
            wait(_spd/2)
        def upd2(lst):

            def upd3(_pt,alph):
                for i in lst:
                    if out(i):
                        _pt[i].set_opacity(dark+(1-dark)*alph)
            play([
                *(
                    _pt[i].animate.set_color(ORANGE)
                    for i in range(n) if i in lst
                ),
                *(
                    _pt[i].animate.set_color(WHITE)
                    for i in range(n) if i not in lst
                ),
                UpdateFromAlphaFunc(_pt,upd3)
            ],_spd/2)

        def out(id):
            return dis(pt[id],[res[0],res[1]])>res[2]*res[2]
        for i in range(n):
            upd2([i])
            if out(i):
                res=[pt[i][0],pt[i][1],sz*0.75]
                upd([i])
                for j in range(i):
                    upd2([i,j])
                    if out(j):
                        res=[(pt[i][0]+pt[j][0])/2,(pt[i][1]+pt[j][1])/2,math.sqrt(dis(pt[i],pt[j]))/2]
                        upd([i,j])
                        for k in range(j):
                            upd2([i,j,k])
                            if out(k):
                                u = pt[i]
                                v = pt[j]
                                w = pt[k]
                                a = (v[0] - u[0]) * 2
                                b = (v[1] - u[1]) * 2
                                c = dis(v, [0, 0]) - dis(u, [0, 0])
                                d = (w[0] - v[0]) * 2
                                e = (w[1] - v[1]) * 2
                                f = dis(w, [0, 0]) - dis(v, [0, 0])
                                res=[(b*f-e*c)/(b*d-e*a),(d*c-a*f)/(b*d-e*a),0]
                                res[2]=math.sqrt(dis(u,[res[0],res[1]]))
                                upd([i,j,k])


