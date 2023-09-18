from manimlib import *
import numpy
import random
import functools
import queue


class Andrew(Scene):
    def construct(self) -> None:
        _H=TexText("Andrew").set_height(1).set_color(YELLOW_A)
        self.add(_H)
        self.wait(2)
        _H.generate_target().scale(0.3).to_corner(UR)
        self.play(MoveToTarget(_H))

        random.seed(2)
        n=27
        sz=0.17
        min_dis=1.2
        xscd=2
        wg=1
        _buff=0.02
        _spd=1
        _spd_max=1/3
        _spd_k=0.95
        dark=0.2

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
            if dis(now,[0,0])>4.5*4.5:continue
            suc=True
            for j in range(len(pt)):
                if dis(pt[j],now)<min_dis:
                    suc=False
                    break
            if suc:pt.append(now)

        pt.sort()

        _pt=VGroup(
            *(
                Dot([x,y,0]).set_height(sz)
                for [x,y] in pt
            )
        )
        play([FadeIn(_pt)])
        play([_pt.animate.set_opacity(dark)])

        res=[]
        used=[0 for i in range(n)]
        e=[Line() for i in range(n)]

        x_n=Line()

        for i in range(n):
            if used[i]:continue
            if _spd>_spd_max:_spd=_spd*_spd_k
            tmp2=Line([_pt[i].get_x(),-10,0],[_pt[i].get_x(),10,0],color=BLUE,opacity=0.2)

            _pt[i].generate_target().set_color(YELLOW).set_opacity(1)
            if x_n not in self.get_mobjects():
                x_n.become(tmp2)
                play([
                    MoveToTarget(_pt[i]),
                    FadeIn(x_n),
                ],spd=_spd)
            else:
                play([
                    MoveToTarget(_pt[i]),
                    x_n.animate.move_to(tmp2)
                ],spd=_spd)

            if len(res)<2:
                if len(res)==0:
                    play([
                        _pt[i].animate.set_color(WHITE),
                    ],spd=_spd)
                else:
                    e[i].become(Line(_pt[i].get_center(),_pt[res[0]].get_center(),color=YELLOW))
                    play([
                        FadeIn(e[i])
                    ],spd=_spd)
                    play([
                        e[i].animate.set_color(WHITE),
                        _pt[i].animate.set_color(WHITE),
                    ],spd=_spd)
            else:
                e[i].become(Line(_pt[i].get_center(), _pt[res[-1]].get_center(), color=YELLOW))
                play([
                    FadeIn(e[i])
                ],spd=_spd)
                while len(res)>=2:
                    u=res[-1]
                    v=res[-2]
                    tmp=Line(_pt[i].get_center(),_pt[v].get_center(),color=YELLOW)

                    x1=pt[u][0]-pt[v][0]
                    x2=pt[i][0]-pt[v][0]
                    y1=pt[u][1]-pt[v][1]
                    y2=pt[i][1]-pt[v][1]
                    if x1*y2-x2*y1>0:

                        play([
                            FadeOut(e[i]),
                            FadeOut(e[u]),
                            FadeIn(tmp),
                            _pt[u].animate.set_opacity(dark),
                        ],spd=_spd)
                        e[i].become(tmp)
                        add([e[i]])
                        remove([tmp])


                        used[u]=0
                        res.pop()
                        if len(res)<2:
                            play([
                                e[i].animate.set_color(WHITE),
                                _pt[i].animate.set_color(WHITE),
                            ],spd=_spd)
                    else:
                        play([
                            e[i].animate.set_color(WHITE),
                            _pt[i].animate.set_color(WHITE),
                        ],spd=_spd)

                        break
            res.append(i)
            used[i]=1
        used[0]=0
        for i in range(n-1,-1,-1):
            if used[i]: continue
            if _spd > _spd_max: _spd = _spd * _spd_k
            tmp2 = Line([_pt[i].get_x(), -10, 0], [_pt[i].get_x(), 10, 0], color=BLUE, opacity=0.2)

            _pt[i].generate_target().set_color(YELLOW).set_opacity(1)
            if x_n not in self.get_mobjects():
                x_n.become(tmp2)
                play([
                    MoveToTarget(_pt[i]),
                    FadeIn(x_n),
                ],spd=_spd)
            else:
                play([
                    MoveToTarget(_pt[i]),
                    x_n.animate.move_to(tmp2)
                ],spd=_spd)
            if len(res) < 2:
                if len(res) == 0:
                    play([
                        _pt[i].animate.set_color(WHITE),
                    ],spd=_spd)
                else:
                    e[i].become(Line(_pt[i].get_center(), _pt[res[0]].get_center(), color=YELLOW))
                    play([
                        FadeIn(e[i])
                    ],spd=_spd)
                    play([
                        e[i].animate.set_color(WHITE),
                        _pt[i].animate.set_color(WHITE),
                    ],spd=_spd)
            else:
                e[i].become(Line(_pt[i].get_center(), _pt[res[-1]].get_center(), color=YELLOW))
                play([
                    FadeIn(e[i])
                ],spd=_spd)
                while len(res) >= 2:
                    u = res[-1]
                    v = res[-2]
                    tmp = Line(_pt[i].get_center(), _pt[v].get_center(), color=YELLOW)

                    x1 = pt[u][0] - pt[v][0]
                    x2 = pt[i][0] - pt[v][0]
                    y1 = pt[u][1] - pt[v][1]
                    y2 = pt[i][1] - pt[v][1]
                    if x1 * y2 - x2 * y1 > 0:

                        play([
                            FadeOut(e[i]),
                            FadeOut(e[u]),
                            FadeIn(tmp),
                            _pt[u].animate.set_opacity(dark),
                        ],spd=_spd)
                        e[i].become(tmp)
                        add([e[i]])
                        remove([tmp])

                        used[u] = 0
                        res.pop()
                        if len(res) < 2:
                            play([
                                e[i].animate.set_color(WHITE),
                                _pt[i].animate.set_color(WHITE),
                            ],spd=_spd)
                    else:
                        play([
                            e[i].animate.set_color(WHITE),
                            _pt[i].animate.set_color(WHITE),
                        ],spd=_spd)

                        break
            res.append(i)
            used[i] = 1
        res.pop()
        play([
            FadeOut(x_n)
        ],spd=_spd)
        wait(1)
        # add(Integer(len(res)).to_corner(DR))
        # for i in range(len(res)):
        #     j=(i+1)%len(res)
        #     add([Line(_pt[res[i]].get_center(),_pt[res[j]].get_center())])