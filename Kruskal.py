from manimlib import *
import numpy
import random
import functools
import queue


class Kruskal(Scene):
    def construct(self) -> None:
        _H = TexText("Kruskal").set_height(1).set_color(YELLOW_A)
        self.add(_H)
        self.wait(2)
        _H.generate_target().scale(0.3).to_corner(UR)
        self.play(MoveToTarget(_H))

        random.seed(5)
        n = 15
        sz = 0.17
        min_dis = 1.2
        xscd = 3
        wg = 1
        _buff = 0.02
        _spd = 1
        _spd_max = 1 / 3
        _spd_k = 0.95
        dark = 0.2
        line_wid=6

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

        pt = []

        def dis(i, j):
            dx = i[0] - j[0]
            dy = i[1] - j[1]
            return dx * dx + dy * dy

        while len(pt) < n:
            now = [random.randint(-500, 100), random.randint(-250, 300)]
            now[0] = now[0] / 100
            now[1] = now[1] / 100
            suc = True
            for j in range(len(pt)):
                if dis(pt[j], now) < min_dis:
                    suc = False
                    break
            if suc: pt.append(now)
        e=[]
        for i in range(n):
            lst=[]
            for j in range(n):
                if j!=i:
                    lst.append([dis(pt[i],pt[j]),j])
            lst.sort()
            for j in range(xscd):
                k=lst[j][1]
                rd=random.randint(0,3)
                if rd!=0:
                    _i=i
                    _k=k
                    if _i>_k:_i,_k=_k,_i
                    if [_i,_k] not in e:e.append([_i,_k])
        _pt=VGroup(
            *(
                Dot([x,y,0]).set_height(sz)
                for [x,y] in pt
            )
        )
        _e=VGroup(
            *(
                Line(_pt[u].get_center(),_pt[v].get_center()).set_stroke(width=line_wid)
                for [u,v] in e
            )
        )
        _e2=VGroup(
            *(
                Line(_pt[u].get_center(),_pt[v].get_center()).set_stroke(width=line_wid,opacity=dark)
                for [u,v] in e
            )
        )
        lft_ver=VGroup(
            *(
                _pt[u].copy()
                for [u, v] in e
            )
        )
        rht_ver=VGroup(
            *(
                _pt[v].copy()
                for [u, v] in e
            )
        )
        play([
            FadeIn(_pt),
            FadeIn(_e),
            FadeIn(_e2),
            FadeIn(lft_ver),
            FadeIn(rht_ver),
        ],_spd*2.2)

        def get_left_point(i):
            return [2,3-(i+0.5)*(5.5/len(e))]

        def get_line_angle(i):
            u=pt[e[i][0]]
            v=pt[e[i][1]]
            dx=v[0]-u[0]
            dy=v[1]-u[1]
            return -math.atan2(dy,dx)

        tmp1=[get_left_point(i) for i in range(len(e))]
        tmp2=[get_line_angle(i) for i in range(len(e))]

        def get_upd(i):
            def upd(mob,al):
                mob.restore()
                mob.rotate(tmp2[i]*al)
                now=mob.get_start()
                dx=tmp1[i][0]-now[0]
                dy=tmp1[i][1]-now[1]
                dx=dx*al
                dy=dy*al
                mob.shift([dx,dy,0])
                # lft_ver[i].move_to(mob.get_start())
                # rht_ver[i].move_to(mob.get_end())
            return upd
        def get_upd2(i):
            def upd(mob):
                mob[0].move_to(_e[i].get_start())
                mob[1].move_to(_e[i].get_end())
            return upd


        for i in range(len(e)):
            _e[i].save_state()

        subtitie = TexText("将边按照边权（长度）从小到大排序").set_height(0.35).to_edge(DOWN)

        play([
            Write(subtitie)
        ],_spd*1.5/2)

        play([
            LaggedStart(
                *(
                    UpdateFromAlphaFunc(_e[i], get_upd(i))
                    for i in range(len(e))
                ),
                lag_ratio=0.1
            ),
            *(
                UpdateFromFunc(VGroup(lft_ver[i],rht_ver[i]),get_upd2(i))
                for i in range(len(e))
            ),
        ],4*_spd)



        ord=[i for i in range(len(e))]
        def _k(x):
            return dis(pt[e[x][0]],pt[e[x][1]])

        ord.sort(key=_k)
        pos=[0 for i in range(len(e))]
        for i in range(len(e)):
            pos[ord[i]]=i
        wait(1)
        play([
            *(
                 _e[i].animate.shift(DOWN * (pos[i] - i) * (5.5 / len(e)))
                 for i in range(len(e))
            ),
            *(
                 UpdateFromFunc(VGroup(lft_ver[i], rht_ver[i]), get_upd2(i))
                 for i in range(len(e))
            ),
        ],4*_spd)

        # return
        play([
            FadeOut(subtitie)
        ], _spd * 1.5/2)
        subtitie = TexText("依次加入生成树中").set_height(0.35).to_edge(DOWN)
        play([
            Write(subtitie)
        ], _spd * 1.5/2)

        g=[[] for i in range(n)]
        def is_link(x,y,tmp):
            vis=[0 for i in range(n)]
            stk=[]
            stk2=[]
            def dfs(u):
                vis[u]=1
                stk2.append(u)
                if u==y:return True
                for [v,i] in g[u]:
                    if vis[v]:continue
                    stk.append(i)
                    if dfs(v):return True
                    stk.pop()
                stk2.pop()
                return False
            if dfs(x):
                play([
                    *(
                        _e[i].animate.set_color(RED)
                        for i in stk
                    ),
                    *(
                        _pt[u].animate.set_color(RED)
                        for u in stk2
                    ),
                    _pt[x].animate.set_color(RED),
                    _pt[y].animate.set_color(RED),
                    lft_ver[tmp].animate.set_color(RED),
                    rht_ver[tmp].animate.set_color(RED),
                ],_spd*1.5)
                play([
                    *(
                        _e[i].animate.set_color(WHITE)
                        for i in stk
                    ),
                    *(
                        _pt[u].animate.set_color(WHITE)
                        for u in stk2
                    ),
                    _pt[x].animate.set_color(WHITE),
                    _pt[y].animate.set_color(WHITE),
                    lft_ver[tmp].animate.set_color(WHITE),
                    rht_ver[tmp].animate.set_color(WHITE),
                    FadeOut(_e[tmp]),
                ],_spd*1.5)
                remove([
                    lft_ver[tmp],
                    rht_ver[tmp],
                ])
                return True
            else:
                return False

        def get_upd2(i):
            def upd(mob):
                mob[0].move_to(_e[i].get_start())
                mob[1].move_to(_e[i].get_end())
            return upd

        flag=[1 for i in range(len(e))]
        for _i in range(len(e)):

            if _i==6:
                play([
                    FadeOut(subtitie)
                ], _spd * 1.5/2)
                subtitie = TexText("如果加边后出现了环，则舍弃这条边").set_height(0.35).to_edge(DOWN)
                play([
                    Write(subtitie)
                ], _spd * 1.5/2)
            if _i==14:
                play([
                    FadeOut(subtitie),
                ],_spd*0.75)
                subtitie = TexText("（判环操作可以用并查集来实现）").set_height(0.35).to_edge(DOWN)
                play([
                    Write(subtitie)
                ], _spd*0.75)

            i=ord[_i]
            flag[i]=0
            def upd(mob,al):
                mob.restore()
                mob.rotate(-tmp2[i]*al)
                now=mob.get_start()
                res=_e2[i].get_start()
                dx=res[0]-now[0]
                dy=res[1]-now[1]
                dx=dx*al
                dy=dy*al
                mob.shift([dx,dy,0])
            play([
                _e[i].animate.set_color(YELLOW),
                lft_ver[i].animate.set_color(YELLOW),
                rht_ver[i].animate.set_color(YELLOW),
                _pt[e[i][0]].animate.set_color(YELLOW),
                _pt[e[i][1]].animate.set_color(YELLOW),
                _e2[i].animate.set_color(YELLOW),
            ])
            _e[i].save_state()

            play([
                UpdateFromAlphaFunc(_e[i],upd),
                *(
                    _e[j].animate.set_y(3-(5.5/(len(e)-_i-1))*(pos[j]-_i-0.5))
                    for j in range(len(e)) if flag[j]
                 ),
                *(
                    UpdateFromFunc(VGroup(lft_ver[j], rht_ver[j]), get_upd2(j))
                    for j in range(len(e)) if flag[j] or j==i
                )
            ])
            _e2[i].set_color(WHITE)
            if(is_link(e[i][0],e[i][1],i)):
                lalala=0
            else:
                play([
                    _e[i].animate.set_color(BLUE),
                    _pt[e[i][0]].animate.set_color(BLUE),
                    _pt[e[i][1]].animate.set_color(BLUE),
                    lft_ver[i].animate.set_color(BLUE),
                    rht_ver[i].animate.set_color(BLUE),
                ])
                play([
                    _e[i].animate.set_color(WHITE),
                    _pt[e[i][0]].animate.set_color(WHITE),
                    _pt[e[i][1]].animate.set_color(WHITE),
                    lft_ver[i].animate.set_color(WHITE),
                    rht_ver[i].animate.set_color(WHITE),
                ])
                remove([
                    lft_ver[i],
                    rht_ver[i],
                ])
                g[e[i][0]].append([e[i][1], i])
                g[e[i][1]].append([e[i][0], i])

        play([
            VGroup(
                *(
                    _e[i]
                    for i in range(len(e)) if _e[i] in self.get_mobjects()
                ),
                _e2,
                _pt,
            ).animate.shift(RIGHT*2)
        ])

        play([
            FadeOut(subtitie)
        ], _spd * 1.5)
        subtitie = TexText("最终就得到了最小生成树").set_height(0.35).to_edge(DOWN)
        play([
            Write(subtitie)
        ], _spd * 1.5)