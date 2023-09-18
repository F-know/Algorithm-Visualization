from manimlib import *
import numpy
import random


class Tarjan(Scene):
    def construct(self) -> None:
        spd=[0.62]
        spd_min=1/17
        spd_k=0.96
        n=330
        sz=0.2
        sz2=0.125
        min_dis=0.07
        xscd=6
        ar_buff=0.05
        star_n=3
        dark=0.35

        pt=[]
        def dis(i,j):
            dx=i[0]-j[0]
            dy=i[1]-j[1]
            return dx*dx+dy*dy
        while len(pt)<n:
            now=[random.randint(-600,600),random.randint(-350,350)]
            now[0]=now[0]/100
            now[1]=now[1]/100
            suc=True
            for j in range(len(pt)):
                if dis(pt[j],now)<min_dis:
                    suc=False
                    break
            if suc:pt.append(now)
        e=[]
        for i in range(n):
            lst=[]
            for j in range(n):
                lst.append([dis(pt[i],pt[j]),j])
            lst.sort()
            for j in range(min(xscd,n)):
                k=lst[j][1]
                rd=random.randint(0,1)
                if rd==1:
                    _i=i
                    _k=k
                    if _i>_k:_i,_k=_k,_i
                    if [_i,_k] not in e:e.append([_i,_k])
        for i in range(len(e)):
            rd=random.randint(0,1)
            if rd==1:e[i][0],e[i][1]=e[i][1],e[i][0]
        _pt=VGroup(
            *(
                Circle(stroke_width=0).set_height(sz).set_opacity(1).set_color(WHITE).move_to([x,y,0])
                for [x,y] in pt
            )
        )
        _pt2 = VGroup(
            *(
                Circle(stroke_width=0).set_height(sz2).set_opacity(1).set_color(WHITE).move_to([x, y, 0])
                for [x, y] in pt
            )
        )
        # self.add(_pt)
        _ar=VGroup(
            *(
                Arrow(_pt[u].get_center(),_pt[v].get_center(),buff=ar_buff,opacity=0.6)
                for [u,v] in e
            )
        )
        # self.add(_ar)
        cs=[]
        while len(cs)<n:
            now=random_color()
            if now not in cs and now!=BLACK:
                cs.append(now)
        g=[*([] for i in range(n))]
        for i in range(len(e)):
            [u,v]=e[i]
            g[u].append(i)
        idx=[-1]
        dfn=[-1 for i in range(n)]
        low=[-1 for i in range(n)]
        vis=[0 for i in range(n)]
        stk=[]
        res=[]
        to=[-1 for i in range(n)]
        def dfs(u):
            if spd[0]>spd_min:
                spd[0]=spd[0]*spd_k
            idx[0]=idx[0]+1
            dfn[u]=idx[0]
            low[u]=idx[0]
            _pt[u].set_color(cs[dfn[u]])
            _pt2[u].set_color(cs[dfn[u]])
            self.play(
                FadeIn(_pt[u]),
                run_time=spd[0]
            )
            self.add(_pt2[u])
            stk.append(u)
            vis[u]=1
            # tmp=random.randint(1,3)
            # if tmp==1 and len(res)>10:
            #     s=random.randint(0,len(res)-1)
            #     self.play(
            #         *(
            #             Flash(_pt[v],color=_pt[v].get_color(),line_length=0.05,num_lines=8,flash_radius=0.15)
            #             for v in res[s]
            #         ),
            #         run_time=spd[0]*6
            #     )
            for i in g[u]:
                self.play(
                    GrowFromPoint(_ar[i],_pt[u].get_center()),
                    run_time=spd[0]
                )
                v=e[i][1]
                # self.play(
                #     _ar[i].animate.set_color(YELLOW),
                #     run_time=spd
                # )
                if dfn[v]==-1:
                    dfs(v)
                    if low[u]>low[v]:
                        low[u]=low[v]
                        tmp=_pt2[v].copy()
                        self.play(
                            tmp.animate.move_to(_pt2[u]),
                            FadeOutToPoint(_ar[i], _pt[u].get_center()),
                            run_time=spd[0]
                        )
                        _pt2[u].become(tmp)
                        self.remove(tmp)
                    else:
                        self.play(
                            FadeOutToPoint(_ar[i], _pt[u].get_center()),
                            run_time=spd[0]
                        )
                else:
                    if vis[v]==1:
                        if low[u]>low[v]:
                            low[u]=low[v]
                            tmp = _pt2[v].copy()
                            self.play(
                                tmp.animate.move_to(_pt2[u]),
                                FadeOutToPoint(_ar[i], _pt[u].get_center()),
                                run_time=spd[0]
                            )
                            _pt2[u].become(tmp)
                            self.remove(tmp)
                        else:
                            self.play(
                                FadeOutToPoint(_ar[i], _pt[u].get_center()),
                                run_time=spd[0]
                            )
                    else:
                        self.play(
                            FadeOutToPoint(_ar[i], _pt[u].get_center()),
                            run_time=spd[0]
                        )
            if dfn[u]!=low[u]:return
            tmp=[]
            while stk[-1]!=u:
                vis[stk[-1]]=0
                tmp.append(stk[-1])
                to[stk[-1]]=u
                stk.pop()
            vis[stk[-1]] = 0
            tmp.append(stk[-1])
            stk.pop()
            res.append(tmp)
            self.play(
                *(
                    _pt[v].animate.set_color(cs[dfn[u]])
                    for v in tmp
                ),
                *(
                    FadeOut(_pt2[v])
                    for v in tmp
                ),
                run_time=spd[0]
            )
            self.play(
                *(
                    _pt[v].animate.set_opacity(dark)
                    for v in tmp
                ),
                run_time=spd[0]
            )

        for i in range(n):
            if dfn[i]==-1:dfs(i)

        self.play(
            *(
                _pt[u].animate.set_opacity(1)
                for u in range(n)
            ),
        )
        self.play(
            *(
                _pt[u].animate.move_to(_pt[to[u]])
                for u in range(n) if to[u]!=-1
            ),
        )