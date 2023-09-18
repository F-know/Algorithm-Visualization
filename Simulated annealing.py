import math

from manimlib import *
import numpy
import random
import functools
import queue


class Simulated_annealing(Scene):
    def construct(self) -> None:
        _H=TexText("模拟退火").set_height(1).set_color(YELLOW_A)
        self.add(_H)
        self.wait(2)
        _H.generate_target().scale(0.3).to_corner(UR)
        self.play(MoveToTarget(_H))

        random.seed(18)

        sz=0.01
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


        n, m = 400, 10000

        def gtx(x):
            return -5+10/n*x
        def gty(y):
            return -3+6/m*y

        pt=[]
        itr,val=0,m
        while itr<n:
            nxt=min(n,itr+random.randint(1,10))
            f=random.randint(0,1)*2-1
            if val==0:
                f=1
            while itr<nxt:
                pt.append([itr,val])
                itr=itr+1
                val=val+f*random.randint(-m//20,m//10)
                if val<0:
                    val=max(0,val)
                    break

        _pt=VGroup(
            *(
                Dot([gtx(x),gty(y),0]).set_height(sz)
                for [x,y] in pt
            )
        )
        _pt.set_height(3,stretch=True).center().shift(DOWN*2)
        _e=VGroup(
            *(
                Line(_pt[i].get_center(),_pt[i+1].get_center()).set_stroke(width=1.3)
                for i in range(len(_pt)-1)
            )
        )
        play([FadeIn(_e)])

        T,d=n,0.998
        now=0
        def gt_l():
            return Line(_pt[now].get_center(),_pt[now].get_center()+DOWN*10).set_color(ORANGE)
        _now=gt_l()
        _T_t=TexText("Tempreture=").set_height(0.3).set_color(GREY)
        _T=DecimalNumber(T,num_decimal_places=1).set_height(0.3).next_to(_T_t)
        VGroup(_T,_T_t).move_to([-3,0,0])
        play([
            FadeIn(_T_t),
            FadeIn(_T),
            FadeIn(_now),
        ])
        while T>0.1:
            T_last=T
            T=T*d
            nxt=now+math.floor(random.uniform(-T,T))
            nxt=max(0,nxt)
            nxt=min(n-1,nxt)
            def gt_n():
                return Line(_pt[nxt].get_center(), _pt[nxt].get_center() + DOWN * 10).set_color(YELLOW)
            _nxt=gt_n()
            self.add(_nxt)
            play([
                ChangeDecimalToValue(_T,T)
            ],spd=(T_last-T)/50)
            self.remove(_nxt)
            if pt[nxt][1]>pt[now][1]:
                now=nxt
                self.remove(_now)
                self.remove(_now)
                _now=gt_l()
                self.add(_now)
                # play([
                #     Transform(_now,gt_l())
                # ],spd=(T_last-T)/50)
                self.add(_now)
            else:
                p=math.exp(-(pt[now][1]-pt[nxt][1])/10/T)
                # print(p)
                if random.uniform(0,1)<p:
                    now=nxt
                    self.remove(_now)
                    self.remove(_now)
                    _now = gt_l()
                    self.add(_now)
                    # play([
                    #     Transform(_now, gt_l())
                    # ], spd=(T_last - T) / 50)
                    self.add(_now)
            # play([
            #     ChangeDecimalToValue(_T,T*d)
            # ])
            T=T*d
        play([
            ChangeDecimalToValue(_T,0)
        ])
