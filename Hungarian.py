from manimlib import *
import numpy
import random
import functools
import queue


class Hungarian_algorithm(Scene):
    def construct(self) -> None:

        random.seed(5)
        n = 7
        sz = 0.17
        min_dis = 1.2
        xscd = 3
        wg = 1
        _buff = 0.02
        _spd = 1
        _spd_max = 1 / 3
        _spd_k = 0.95
        dark = 0.25
        line_wid=6

        _U=2
        _D=-3
        _L=-1.5
        _R=1.5

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
        for i in range(n):
            pt.append([_L,_U-(_U-_D)/(n-1)*i])
        for i in range(n):
            pt.append([_R,_U-(_U-_D)/(n-1)*i])

        e=[]
        g=[[]for i in range(n)]
        stk=[i for i in range(n,n*2)]
        for i in range(n):
            random.shuffle(stk)
            cnt=random.randint(1,xscd)
            for j in range(cnt):
                e.append([i,stk[j]])
                g[i].append(len(e)-1)

        for i in range(n):
            g[i].sort(key=lambda x:e[x][1])

        _pt=VGroup(
            *(
                Dot([x,y,0]).set_height(sz)
                for [x,y] in pt
            )
        )
        _e=VGroup(
            *(
                Line(_pt[u].get_center(),_pt[v].get_center())
                for [u,v] in e
            )
        )
        txt1=TexText("给你一张二分图").set_height(0.25).move_to([-4,1,0])
        play([Write(txt1)])
        play([
            FadeIn(_pt),
            FadeIn(_e),
        ])
        play([
            _e.animate.set_opacity(dark)
        ])
        txt2=TexText("每个点最多只能参与一次匹配").set_height(0.25).move_to([-4,0,0])
        play([Write(txt2)])

        match_txt=TexText("匹配数：").set_height(0.5).move_to([3,0,0])
        match_num=Integer(0).set_height(0.5).move_to([5,0,0]).set_color(BLUE)

        def rd_match(seed,flag):
            random.seed(seed)
            ord=[i for i in range(len(e))]
            random.shuffle(ord)
            ok=[0 for i in range(n*2)]
            cnt=0
            tmp_stk=[]
            for i in ord:
                tmp=random.randint(0,1)
                if tmp and not (ok[e[i][0]] or ok[e[i][1]]):
                    ok[e[i][0]]=1
                    ok[e[i][1]]=1
                    cnt=cnt+1
                    tmp_stk.append(i)
            match_edge=VGroup(
                *(
                    Line(_pt[e[i][0]].get_center(),_pt[e[i][1]].get_center()).set_color(BLUE)
                    for i in tmp_stk
                )
            )
            if not flag:
                play([
                    FadeIn(match_edge)
                ])
                wait(_spd)
                play([
                    FadeOut(match_edge)
                ])
            else:
                match_num.set_value(cnt)
                play([
                    FadeIn(match_edge),
                    FadeIn(match_num),

                ])
                wait(_spd)
                play([
                    FadeOut(match_edge),
                    FadeOut(match_num),
                ])


        for i in range(3):
            rd_match(i,0)

        txt3 = TexText("最多能匹配多少点对？").set_height(0.25).move_to([-4, -1.25, 0]).set_color(YELLOW)
        play([Write(txt3)])
        play([Write(match_txt)])


        for i in range(3,6):
            rd_match(i,1)

        play([
            FadeOut(_pt),
            FadeOut(_e),
            FadeOut(txt1),
            FadeOut(txt2),
            FadeOut(txt3),
            FadeOut(match_txt),
        ])

        _H = TexText("匈牙利算法").set_height(1).set_color(YELLOW_A)
        self.play(FadeIn(_H))
        self.wait(2)
        _H.generate_target().scale(0.3).to_corner(UR)
        self.play(MoveToTarget(_H))

        match_num.set_value(0)
        play([
            FadeIn(_pt),
            FadeIn(_e),
            FadeIn(match_txt),
            FadeIn(match_num),
        ])




        mch=[-1 for i in range(n*2)]
        vis=[-1 for i in range(n*2)]

        _mch=[Line() for i in range(n*2)]

        path=[]

        def change_color():
            _len=len(path)
            tmp_dot=[]
            for i in range(0,_len,2):
                tmp_dot.append(Dot(path[i].get_start()).set_height(sz))
                tmp_dot.append(Dot(path[i].get_end()).set_height(sz))

            seg=1
            def get_pos(i):
                return [-_len*seg/2+i*seg,3,0]

            sv=[]
            for p in tmp_dot:
                add([p])
                x,y,z=p.get_center()
                sv.append([x,y,z])

            def fun(pth):
                for i in range(_len):
                    if not i&1:
                        pth[i].become(Line(tmp_dot[i].get_center(),tmp_dot[i+1].get_center()).set_color(YELLOW))
                    else:
                        pth[i].become(Line(tmp_dot[i+1].get_center(), tmp_dot[i].get_center()).set_color(BLUE))

            play([
                *(
                    tmp_dot[i].animate.move_to(get_pos(i))
                    for i in range(_len+1)
                ),
                UpdateFromFunc(VGroup(*(l for l in path)),fun)
            ],_spd*1.5)

            play([
                *(
                    path[i].animate.set_color(BLUE)
                    for i in range(0,_len,2)
                ),
                *(
                    path[i].animate.set_color(YELLOW)
                    for i in range(1, _len, 2)
                ),
                ChangeDecimalToValue(match_num,match_num.get_value()+1)
            ])

            def fun2(pth):
                for i in range(_len):
                    if not i & 1:
                        pth[i].become(Line(tmp_dot[i].get_center(), tmp_dot[i + 1].get_center()).set_color(BLUE))
                    else:
                        pth[i].become(Line(tmp_dot[i + 1].get_center(), tmp_dot[i].get_center()).set_color(YELLOW))

            play([
                *(
                    tmp_dot[i].animate.move_to(sv[i])
                    for i in range(_len + 1)
                ),
                UpdateFromFunc(VGroup(*(l for l in path)), fun2)
            ], _spd * 1.5)

            for p in tmp_dot:
                remove([p])

        def dfs(u,tg):
            if vis[u]==tg:
                return False
            vis[u]=tg
            for i in g[u]:
                v=e[i][1]
                if mch[v]==u:continue
                tmp_line=_e[i].copy().set_opacity(1).set_color(YELLOW)
                play([
                    GrowFromPoint(tmp_line,_pt[u].get_center())
                ])
                path.append(tmp_line)
                if mch[v]==-1:

                    play([
                        FlashAround(_pt[v])
                    ])

                    if len(path)==1:
                        play([
                            path[0].animate.set_color(BLUE),
                            ChangeDecimalToValue(match_num,match_num.get_value()+1)
                        ])

                    else:
                        change_color()
                        play([
                            *(
                                FadeOut(path[j])
                                for j in range(1,len(path),2)
                            )
                        ])

                    path.clear()

                    mch[v]=u
                    _mch[v].become(tmp_line)
                    add([
                        _mch[v]
                    ])
                    remove([
                        tmp_line
                    ])

                    return True


                path.append(_mch[v])
                # _go(_mch[v])
                if dfs(mch[v],tg):
                    mch[v]=u
                    _mch[v].become(tmp_line)
                    add([
                        _mch[v]
                    ])
                    remove([
                        tmp_line
                    ])
                    return True
                # _back(_mch[v])
                path.pop()
                path.pop()

                play([
                    FadeOutToPoint(tmp_line, _pt[u].get_center())
                ])

        ar=Arrow([0,0,0],[0.5,0,0],buff=0).set_color(ORANGE).next_to(_pt[0],LEFT)

        for i in range(n):
            if i==0:
                play([FadeIn(ar)])
            else:
                play([ar.animate.next_to(_pt[i],LEFT)])
            play([
                FlashAround(_pt[i])
            ])
            dfs(i,i)

        AC=TexText("AC").scale(1.5).set_color(GREEN).next_to(match_txt,DOWN).shift(RIGHT/2).shift(DOWN)
        play([
            match_txt.animate.become(TexText("最大匹配数：").set_height(0.5).move_to([3.5, 0, 0]).scale(0.78))
        ])
        play([
            FadeIn(AC)
        ])





