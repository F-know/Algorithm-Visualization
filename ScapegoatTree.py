from manimlib import *
import numpy
import random
import functools
import queue


class Scapegoat(Scene):
    def construct(self) -> None:
        _H = TexText("替罪羊树").set_height(1).set_color(YELLOW_A)
        self.add(_H)
        self.wait(2)
        _H.generate_target().scale(0.3).to_corner(UR)
        self.play(MoveToTarget(_H))

        random.seed(4)
        n = 65
        m = 10
        sz=0.23
        _buff = 0.02
        _spd = 1
        alph=0.7

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

        def noAct():
            return Square().move_to([100,100,0]).animate.move_to([100,100,0])

        def gtx(i):
            return -5+10/n*i
        def gty(i):
            return 3-6/m*i

        class Node():
            def __init__(self):
                self.s=[-1,-1]
                self.d=0
                self.f=-1
                self.c=0
                self.ver=Dot().set_height(sz).set_color(BLUE)
                self.edg=[Line(),Line()]

        nd=[*(Node() for i in range(n))]

        global root
        root=-1

        global bad
        bad=-1

        def insert(x):
            nd[x].ver.move_to([gtx(x),gty(m),0])
            play([
                FadeIn(nd[x].ver)
            ])
            global root
            if root==-1:
                play([
                    nd[x].ver.animate.set_y(gty(0))
                ])
                root=x
            else:
                def dfs(u):
                    v=nd[u].s[x>u]
                    if v!=-1:
                        dfs(v)
                    else:
                        nd[u].s[x>u]=x
                        nd[x].f=u
                        nd[x].d=nd[u].d+1
                        nd[x].c=1
                        play([
                            nd[x].ver.animate.set_y(gty(nd[x].d))
                        ])
                        nd[u].edg[x>u]=Line(nd[u].ver.get_center(),nd[x].ver.get_center()).set_color(BLUE)
                        play([
                            GrowFromPoint(nd[u].edg[x>u],nd[u].ver.get_center())
                        ])
                    l=0
                    r=0
                    if nd[u].s[0]!=-1:l=nd[nd[u].s[0]].c
                    if nd[u].s[1]!=-1:r=nd[nd[u].s[1]].c
                    nd[u].c=1+l+r
                    if l/(nd[u].c+0)>alph or r/(nd[u].c+0)>alph:
                        global bad
                        bad=u
                dfs(root)

        def rebuild(x):
            stk=[]
            def dfs(u):
                if nd[u].s[0]!=-1:dfs(nd[u].s[0])
                stk.append(u)
                if nd[u].s[1]!=-1:dfs(nd[u].s[1])
            dfs(x)
            f=nd[x].f
            low=max(*(nd[i].d for i in stk))+1

            play([
                *(
                    nd[i].ver.animate.set_color(YELLOW)
                    for i in stk
                ),
                *(
                    FadeOut(li)
                    for i in stk for li in nd[i].edg if li in self.get_mobjects()
                ),
                FadeOut(nd[f].edg[x>f]) if f!=-1 else noAct()
            ],_spd*2)
            play([
                *(
                    nd[i].ver.animate.set_y(gty(low))
                    for i in stk
                )
            ],_spd*2)
            showLine=[]
            def build(l,r,d):
                if l>r:return -1
                mid=(l+r)//2
                nd[stk[mid]].d=d
                ll=build(l,mid-1,d+1)
                rr=build(mid+1,r,d+1)
                nd[stk[mid]].c=1
                if ll!=-1:
                    nd[stk[mid]].c=nd[stk[mid]].c+nd[ll].c
                    nd[ll].f=stk[mid]
                    showLine.append([stk[mid],ll])
                if rr!=-1:
                    nd[stk[mid]].c=nd[stk[mid]].c+nd[rr].c
                    nd[rr].f = stk[mid]
                    showLine.append([stk[mid], rr])
                nd[stk[mid]].s[0]=ll
                nd[stk[mid]].s[1]=rr
                return stk[mid]
            x=build(0,len(stk)-1,nd[x].d)
            nd[x].f=f
            if f!=-1:
                showLine.append([f,x])
                nd[f].s[x>f]=x
            else:
                global root
                root=x
            play([
                *(
                    nd[i].ver.animate.set_y(gty(nd[i].d))
                    for i in stk
                )
            ],_spd*2)
            for u,v in showLine:
                nd[u].edg[v>u]=Line(nd[u].ver.get_center(),nd[v].ver.get_center()).set_color(BLUE)
            play([
                *(
                    FadeIn(nd[u].edg[v>u])
                    for u,v in showLine
                ),
                *(
                    nd[i].ver.animate.set_color(BLUE)
                    for i in stk
                )
            ],_spd*2)



        ord=[*(i for i in range(n))]
        random.shuffle(ord)
        for i in range(n):
            insert(ord[i])
            if bad!=-1:
                # stkl=[]
                # def dfsl(x):
                #     if x==-1:return
                #     dfsl(nd[x].s[0])
                #     stkl.append(x)
                #     dfsl(nd[x].s[1])
                # dfsl(nd[bad].s[0])
                # stkr = []
                # def dfsr(x):
                #     if x == -1: return
                #     dfsr(nd[x].s[0])
                #     stkr.append(x)
                #     dfsr(nd[x].s[1])
                # dfsr(nd[bad].s[1])
                # if len(stkl)<len(stkr):
                #     play([
                #         *(
                #             nd[i].ver.animate.set_color(WHITE)
                #             for i in stkl
                #         ),
                #         *(
                #             nd[i].ver.animate.set_color(ORANGE)
                #             for i in stkr
                #         ),
                #     ],_spd*2)
                # else:
                #     play([
                #         *(
                #             nd[i].ver.animate.set_color(WHITE)
                #             for i in stkr
                #         ),
                #         *(
                #             nd[i].ver.animate.set_color(ORANGE)
                #             for i in stkl
                #         ),
                #     ],_spd*2)
                rebuild(bad)
                bad=-1