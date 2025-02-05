from gilp import LP
from gilp import simplex_visual

lp = LP(A=[[2, 2],
           [2, 1]],
        b=[8, 6],
        c=[16, 10])
visual = simplex_visual(lp=lp)

visual.write_html("lego.html")
