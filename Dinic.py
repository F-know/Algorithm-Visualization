from manimlib import *
import numpy
import random
import functools
import queue


class Dinic(Scene):
    def construct(self) -> None:
        random.seed(6)
        spd=[1/8]
        spd_min=1/17
        spd_k=0.96
        n=40
        sz=0.3
        min_dis=1
        xscd=4
        ar_buff=0
        e_buff=0.07
        dark=0.11

        _Dinic=TexText("Dinic").set_height(1.5).set_color("#FFFFCD")
        self.add(_Dinic)
        self.wait()
        _Dinic.generate_target().scale(0.3).to_corner(UR)
        self.play(MoveToTarget(_Dinic))

        pt=[]
        def dis(i,j):
            dx=i[0]-j[0]
            dy=i[1]-j[1]
            return dx*dx+dy*dy
        pt.append([-6,0])
        pt.append([6,0])
        while len(pt)<n:
            now=[random.randint(-400,400),random.randint(-350,350)]
            now[0]=now[0]/100
            now[1]=now[1]/100
            suc=True
            for j in range(len(pt)):
                if dis(pt[j],now)<min_dis:
                    suc=False
                    break
            if suc:pt.append(now)
        def cmp(u,v):
            return u[0]-v[0]
        pt.sort(key=functools.cmp_to_key(cmp))
        e=[]
        for i in range(n):
            lst=[]
            for j in range(n):
                if j!=i:
                    lst.append([dis(pt[i],pt[j]),j])
            lst.sort()
            if i==0 or i==n-1:
                for j in range(min(xscd,n)):
                    k=i
                    if i==0:k=k+j+1
                    else: k=k-j-1
                    rd=random.randint(3,3)
                    if rd!=0:
                        _i=i
                        _k=k
                        if _i>_k:_i,_k=_k,_i
                        if [_i,_k] not in e:e.append([_i,_k])
            else:
                for j in range(min(xscd,n)):
                    k=lst[j][1]
                    rd=random.randint(0,3)
                    if rd!=0:
                        _i=i
                        _k=k
                        if _i>_k:_i,_k=_k,_i
                        if [_i,_k] not in e:e.append([_i,_k])
        for i in range(len(e)):
            if e[i][0]>e[i][1]:e[i][0],e[i][1]=e[i][1],e[i][0]
        _pt=VGroup(
            *(
                Dot([x,y,0]).set_height(sz)
                for [x,y] in pt
            )
        )

        class _E:
            def __init__(self, u, v):
                p=[v[0]-u[0],v[1]-u[1]]
                l=math.sqrt(p[0]*p[0]+p[1]*p[1])
                # l=p[0]*p[0]+p[1]*p[1]
                # print(u[0],u[1])
                # print(v[0],v[1])
                p[0]=p[0]/l
                p[1]=p[1]/l
                q=[-p[1]*0.7,p[0]*0.7]
                self.ver=[]
                self.ver.append([u[0]+p[0]*e_buff+q[0]*e_buff,u[1]+p[1]*e_buff+q[1]*e_buff])
                self.ver.append([v[0]-p[0]*e_buff+q[0]*e_buff,v[1]-p[1]*e_buff+q[1]*e_buff])
                self.ver.append([v[0]-p[0]*e_buff-q[0]*e_buff,v[1]-p[1]*e_buff-q[1]*e_buff])
                self.ver.append([u[0]+p[0]*e_buff-q[0]*e_buff,u[1]+p[1]*e_buff-q[1]*e_buff])
                self.ver.reverse()
                # print(self.ver[0][0],self.ver[0][1])
                # print(self.ver[1][0],self.ver[1][1])
                # print(self.ver[2][0],self.ver[2][1])
                # print(self.ver[3][0],self.ver[3][1])
                self.rec=Polygon(
                    [self.ver[0][0],self.ver[0][1],0],
                    [self.ver[1][0],self.ver[1][1],0],
                    [self.ver[2][0],self.ver[2][1],0],
                    [self.ver[3][0],self.ver[3][1],0],
                )
                self.fff=Polygon(
                    [self.ver[0][0],self.ver[0][1],0],
                    [self.ver[1][0],self.ver[1][1],0],
                    [self.ver[2][0],self.ver[2][1],0],
                    [self.ver[3][0],self.ver[3][1],0],
                ).set_opacity(1).set_stroke(opacity=0)
                self.w=math.ceil(l*5)
                self.f=self.w
            def set_f(self,f):
                k=f/self.w
                ver=[]
                ver.append([self.ver[0][0],self.ver[0][1],0])
                ver.append([self.ver[0][0]*(1-k)+self.ver[1][0]*k,self.ver[0][1]*(1-k)+self.ver[1][1]*k,0])
                ver.append([self.ver[3][0]*(1-k)+self.ver[2][0]*k,self.ver[3][1]*(1-k)+self.ver[2][1]*k,0])
                ver.append([self.ver[3][0],self.ver[3][1],0])
                self.f=f
                return Polygon(*(it for it in ver)).set_opacity(1)
        _e=[]
        for [u,v] in e:
            _e.append(_E(pt[u],pt[v]))

        def upd_f(i, f):
            tmp = _e[i].set_f(f)
            return _e[i].fff.animate.become(tmp),
        def set_f(i,f):
            tmp=_e[i].set_f(f)
            _e[i].fff.become(tmp)
        def upd_color(i,color):
            self.play(
                _e[i].rec.animate.set_color(color),
                _e[i].fff.animate.set_color(color),
                run_time=spd[0]
            )
        def upd_opacity(i,opacity):
            self.play(
                _e[i].rec.animate.set_stroke(opacity=opacity),
                _e[i].fff.animate.set_opacity(opacity),
                run_time=spd[0]
            )

        for i in range(len(_e)):
            set_f(i,0)
            _e[i].rec.set_stroke(opacity=0),
            _e[i].fff.set_opacity(0),

        self.add(
            *(
                it.rec
                for it in _e
            ),
            *(
                it.fff
                for it in _e
            ),
        )
        self.play(
            FadeIn(_pt[0]),
            FadeIn(_pt[n-1]),
            run_time=spd[0]*8
        )
        _S=TexText("S").scale(1.2).next_to(_pt[0],UP).set_color("#FFFFCD")
        _T=TexText("T").scale(1.2).next_to(_pt[n-1],UP).set_color("#FFFFCD")
        self.play(
            FadeIn(_S),
            FadeIn(_T),
            run_time=spd[0] * 8
        )
        self.play(
            *(
                FadeIn(_pt[i])
                for i in range(1,n-1)
            ),
            run_time=spd[0] * 8
        )
        self.play(
            *(
                it.rec.animate.set_stroke(opacity=1)
                for it in _e
            ),
            *(
                it.fff.animate.set_opacity(1)
                for it in _e
            ),
            run_time=spd[0]*8
        )
        MF=VGroup(
            TexText("Max Flow:").set_height(0.4).set_color(BLUE),
            Integer(0).set_height(0.4)
        ).arrange(DOWN).to_corner(DR)
        self.play(
            FadeIn(MF),
            run_time=spd[0]*8
        )

        color=[
            "#000000",
            "#FFEF00",
            "#FFCF00",
            "#FFBF00",
            "#FF9F00",
            "#FF7F00",
            "#FF6F00",
            "#FF4F00",
            "#FF2F00",
            "#FF0F00",
            "#FF0000",
            "#E3170D",
            "#B0171F",
            "#B03060",
            "#872657",
        ]
        gr=[*([] for i in range(n))]
        eg=[]
        for i in range(len(e)):
            [u,v]=e[i]
            w=_e[i].w
            gr[u].append(len(eg))
            eg.append([v,w])
            gr[v].append(len(eg))
            eg.append([u,0])

        dep=[*(0 for i in range(n))]
        cur=[*(0 for i in range(n))]

        def upd_dep(i,d):
            dep[i]=d
            self.play(
                _pt[i].animate.set_color(color[d]),
                run_time=spd[0]
            )

        self.play(
            *(
                _e[i].rec.animate.set_stroke(opacity=dark)
                for i in range(len(_e))
            ),
            *(
                _e[i].fff.animate.set_opacity(dark)
                for i in range(len(_e))
            ),
            run_time=spd[0]*8
        )
        def bfs():
            for i in range(n):
                dep[i]=0
                cur[i]=0
            upd_dep(0,1)

            q=queue.Queue()
            q.put(0)
            while not q.empty():
                u=q.get()
                for i in gr[u]:
                    [v,w]=eg[i]
                    if w>0 and dep[v]==0:
                        upd_opacity(i//2,1)
                        upd_dep(v,dep[u]+1)
                        q.put(v)
            self.play(
                *(
                    _e[i].rec.animate.set_stroke(opacity=dark)
                    for i in range(len(_e))
                ),
                *(
                    _e[i].fff.animate.set_opacity(dark)
                    for i in range(len(_e))
                ),
                run_time=spd[0] * 8
            )
            self.wait(spd[0]*8)
            return dep[n-1]>0

        stk=[]
        def dfs(u,_in):
            if u==n-1:
                self.play(
                    *(
                        _e[i // 2].rec.animate.set_color(BLUE)
                        for i in stk
                    ),
                    *(
                        _e[i // 2].fff.animate.set_color(BLUE)
                        for i in stk
                    ),
                    run_time=spd[0]*8
                )
                for i in stk:
                    if i%2==0:
                        _e[i//2].fff.generate_target().become(_e[i//2].set_f(_e[i//2].f+_in).set_color(BLUE))
                    else:
                        _e[i//2].fff.generate_target().become(_e[i//2].set_f(_e[i//2].f-_in).set_color(BLUE))
                self.play(
                    *(
                        MoveToTarget(_e[i//2].fff)
                        for i in stk
                    ),
                    ChangeDecimalToValue(MF[1],MF[1].get_value()+_in),
                    run_time=spd[0]*24
                )
                self.play(
                    *(
                        _e[i // 2].rec.animate.set_color(WHITE)
                        for i in stk
                    ),
                    *(
                        _e[i // 2].fff.animate.set_color(WHITE)
                        for i in stk
                    ),
                    run_time=spd[0]*8
                )
                return _in
            _out=0
            for i in range(cur[u],len(gr[u])):
                j=gr[u][i]
                [v,w]=eg[j]
                if(w>0 and dep[v]==dep[u]+1):
                    upd_opacity(j//2,1)
                    stk.append(j)
                    f=dfs(v,min(w,_in))
                    stk.pop()
                    upd_opacity(j//2,dark)
                    eg[j][1]=eg[j][1]-f
                    eg[j^1][1]=eg[j^1][1]+f
                    _in=_in-f
                    _out=_out+f
                    if _in==0:return _out
                cur[u]=cur[u]+1
            return _out

        while bfs():
            now=dfs(0,1000)
            self.play(
                *(
                    _pt[i].animate.set_color(WHITE)
                    for i in range(n)
                ),
                run_time=spd[0] * 8
            )
            self.wait(spd[0]*16)

        self.play(
            *(
                _pt[i].animate.set_color(WHITE)
                for i in range(n)
            ),
            run_time=spd[0] * 8
        )
        self.play(
            *(
                _e[i].rec.animate.set_stroke(opacity=1)
                for i in range(len(_e))
            ),
            *(
                _e[i].fff.animate.set_opacity(1)
                for i in range(len(_e))
            ),
            run_time=spd[0]*8
        )
        all_g=VGroup(
            _pt,
            _S,
            _T,
            *(
                _e[i].rec
                for i in range(len(_e))
            ),
            *(
                _e[i].fff
                for i in range(len(_e))
            ),
        )
        all_g.generate_target().scale(0.8).to_corner(UL)
        MF.generate_target().scale(1.7).to_corner(DR)
        self.play(
            MoveToTarget(all_g),
            MoveToTarget(MF),
            run_time=spd[0]*16
        )
        self.wait()
        # SpeechBubble
