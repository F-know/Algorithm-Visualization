from manimlib import *
import numpy
import random

n = 60
FK = numpy.array([-5,3,0])
sz = 10.0/(n+2)
st = sz*3


class Node():
    def __init__(self):
        self.s = [0,0]
        self.p = 0
        self.v = 0
        self.d = 0
        self.vertice = Circle(color=YELLOW,fill_opacity=1).set_height(1.2*sz)
        self.edge = [Line(), Line()]


class Splay(Scene):
    def construct(self) -> None:
        spd = 1.5

        tr = [Node() for i in range(n+3)]
        rt = 2
        idx = 2

        def get_tree(x):
            stk = VGroup()
            def dfs(x):
                stk.add(tr[x].vertice)
                if tr[x].s[0] != 0:
                    stk.add(tr[x].edge[0])
                    dfs(tr[x].s[0])
                if tr[x].s[1] != 0:
                    stk.add(tr[x].edge[1])
                    dfs(tr[x].s[1])
            dfs(x)

            return stk

        def rotate(x):
            y = tr[x].p
            z = tr[y].p
            k = tr[y].s[1] == x
            l = tr[z].s[1] == y

            # ------
            actions = []
            actions.append(tr[x].vertice.animate.shift(UP * st))
            actions.append(tr[y].vertice.animate.shift(DOWN * st))

            def addline_act(line, u, v):
                def upd(mob, alpha):
                    mob.become(Line(tr[u].vertice.get_center(), tr[v].vertice.get_center())).set_opacity(alpha)

                return UpdateFromAlphaFunc(line, upd)

            def removeline_act(line, u, v):
                def upd(mob, alpha):
                    mob.become(Line(tr[u].vertice.get_center(), tr[v].vertice.get_center())).set_opacity(1 - alpha)

                return UpdateFromAlphaFunc(line, upd)

            def keepline_act(line, u, v):
                def upd(mob):
                    mob.become(Line(tr[u].vertice.get_center(), tr[v].vertice.get_center()))

                return UpdateFromFunc(line, upd)
            if tr[x].s[k] != 0:
                actions.append(get_tree(tr[x].s[k]).animate.shift(UP * st))
                actions.append(keepline_act(tr[x].edge[k], x, tr[x].s[k]))
            if tr[y].s[k ^ 1] != 0:
                actions.append(get_tree(tr[y].s[k ^ 1]).animate.shift(DOWN * st))
                actions.append(keepline_act(tr[y].edge[k^1], y, tr[y].s[k^1]))

            tmp1 = Line()
            if tr[x].s[k ^ 1] != 0:
                actions.append(removeline_act(tr[x].edge[k ^ 1], tr[x].s[k ^ 1], x))
                actions.append(addline_act(tmp1, tr[x].s[k ^ 1], y))
            tmp2 = Line()
            if z != 0:
                actions.append(removeline_act(tr[z].edge[l], y, z))
                actions.append(addline_act(tmp2, x, z))
            actions.append(keepline_act(tr[y].edge[k], x, y))

            self.play(
                *(act for act in actions),
                run_time=spd
            )

            tr[x].edge[k ^ 1].become(tr[y].edge[k])
            tr[y].edge[k].become(tmp1)
            tr[z].edge[l].become(tmp2)
            self.remove(tmp1, tmp2)
            if tr[x].s[k ^ 1] == 0:
                self.add(tr[x].edge[k ^ 1])
                self.remove(tr[y].edge[k])
            # ------

            tr[z].s[tr[z].s[1] == y] = x
            tr[x].p = z
            tr[y].s[k] = tr[x].s[k ^ 1]
            tr[tr[x].s[k ^ 1]].p = y
            tr[x].s[k ^ 1] = y
            tr[y].p = x

        def splay(x):
            while tr[x].p != 0:
                y = tr[x].p
                z = tr[y].p
                if z != 0:
                    if (tr[y].s[1] == x) ^ (tr[z].s[1] == y):
                        rotate(x)
                    else:
                        rotate(y)
                rotate(x)

        def insert(v, x, p=0, d=0):
            if x == 0:
                x = idx
                if p != 0:
                    tr[p].s[v > tr[p].v] = x
                tr[x].v = v
                tr[x].p = p
                tr[x].d = d

                # -----
                self.play(tr[x].vertice.animate.move_to(FK + [v * sz, -d * st, 0]),run_time=spd)
                if p != 0:
                    tr[p].edge[v > tr[p].v].become(Line(tr[p].vertice.get_center(), tr[x].vertice.get_center()))
                    self.play(GrowFromPoint(tr[p].edge[v > tr[p].v], tr[p].vertice.get_center()), run_time=spd)
                # -----



                return
            insert(v, tr[x].s[v > tr[x].v], x, d + 1)


        tr[2].s[0] = 1
        tr[2].v = n+1
        tr[1].p = 2
        tr[1].d = 1

        lst = [i+1 for i in range(n)]
        random.shuffle(lst)

        #------
        tr[1].vertice.set_color(WHITE).move_to(FK+[0,-st,0])
        tr[2].vertice.set_color(WHITE).move_to(FK+[(n+1)*sz,0,0])
        tr[2].edge[0].become(Line(tr[2].vertice.get_center(),tr[1].vertice.get_center()))
        self.play(
            FadeIn(tr[1].vertice),
            FadeIn(tr[2].vertice),
            FadeIn(tr[2].edge[0]),
            run_time=spd
        )

        # def randomcolor():
        #     colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        #     color = ""
        #     for i in range(6):
        #         color += colorArr[random.randint(0, 14)]
        #     return "#" + color

        for i in range(n):
            tr[i+3].vertice.move_to(FK+[lst[i]*sz,-6,0]).set_color(random_color())
            self.play(FadeIn(tr[i+3].vertice),run_time=0.1)

        self.wait()

        #------

        for v in lst:
            idx += 1
            insert(v, rt)

            splay(idx)
            rt = idx

            # -----
            self.play(tr[idx].vertice.animate.set_color(WHITE), run_time=spd)
            # -----
            if spd >= 0.15:
                spd *= 0.84

        now = get_tree(rt)
        now.generate_target()
        now.target.scale(0.8).to_edge(UP)
        self.play(
            MoveToTarget(now)
        )
        splay_text = TexText("SPLAY").set_color(YELLOW).set_height(1.5).to_edge(DOWN)
        self.play(
            Write(splay_text)
        )