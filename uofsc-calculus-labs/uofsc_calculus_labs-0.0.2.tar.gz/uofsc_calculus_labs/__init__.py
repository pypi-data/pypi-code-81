
import ipywidgets as widgets
from IPython.core.display import display, HTML

from sage.repl.ipython_kernel.all_jupyter import slider
from sage.repl.ipython_kernel.all_jupyter import input_box
from sage.repl.ipython_kernel.all_jupyter import selector



## Calc 1 Riemann Sum Calculator
def midpoint(n = slider(1, 100, 1, 4), f = input_box(default = "x^2", type = str), start = input_box(default = "0", type = str),
             end = input_box(default = "1", type = str), endpoint_rule = selector(['Left', 'Midpoint', 'Right'], nrows=1, label="Endpoint rule")):
    a = N(start)
    b = N(end)
    func = sage_eval(f + "+ 0*x", locals={'x':x})
    dx = (b-a)/n
    if endpoint_rule == "Left":
        xs = [q*dx + a for q in range(n)]
        ys = [func(x=x_val) for x_val in xs]
    elif endpoint_rule == "Midpoint":
        xs = [q*dx+dx/2 + a for q in range(n)]
        ys = [func(x=x_val) for x_val in xs]
    elif endpoint_rule == "Right":
        xs = [q*dx + dx + a for q in range(n)]
        ys = [func(x=x_val) for x_val in xs]
    rects = Graphics()
    for q in range(n):
        xm = xs[q]
        ym = ys[q]
        if endpoint_rule == "Left":
            rects = rects + line([[xm,0],[xm,ym],[xm+dx,ym],[xm+dx,0]], rgbcolor = (1,0,0)) + point((xm,ym), rgbcolor = (1,0,0))
        elif endpoint_rule == "Midpoint":
            rects = rects + line([[xm-dx/2,0],[xm-dx/2,ym],[xm+dx/2,ym],[xm+dx/2,0]], rgbcolor = (1,0,0)) + point((xm,ym), rgbcolor = (1,0,0))
        elif endpoint_rule == "Right":
            rects = rects + line([[xm-dx,0],[xm-dx,ym],[xm,ym],[xm,0]], rgbcolor = (1,0,0)) + point((xm,ym), rgbcolor = (1,0,0))
    min_y = min(0, find_local_minimum(func,a,b)[0])
    max_y = max(0, find_local_maximum(func,a,b)[0])
    
    pretty_print(html('<h3>Numerical integrals with the midpoint rule</h3>'))
    pretty_print(html(r'$\int_{a}^{b}{f(x) \ dx} {\, \approx} \sum_i{f(x_i) \Delta x}$'))
    if endpoint_rule == "Left":
        estimation = RDF(dx*sum([ys[q] for q in range(n)]))
        print("Left Endpoint estimated answer: " + str(estimation))
    elif endpoint_rule == "Midpoint":
        estimation = RDF(dx*sum([ys[q] for q in range(n)]))
        print("Midpoint estimated answer: " + str(estimation))
    elif endpoint_rule == "Right":
        estimation = RDF(dx*sum([ys[q] for q in range(n)]))
        print("Right Endpoint estimated answer: " + str(estimation))
    answer = integral_numerical(func,a,b,max_points = 200)[0]
    print("\nSage numerical answer: " + str(answer))
    print("\nError in estimation: " + str(answer - estimation))
    show(plot(func,a,b) + rects, xmin = a, xmax = b, ymin = min_y, ymax = max_y)
    
def Interactive_Riemann_Sums():
    var('x')
    im = widgets.interact_manual(midpoint)
    im.widget.children[5].add_class("top-spacing-class")
    display(HTML(
         "<style>.top-spacing-class {margin-top: 20px;}</style>"
    ))
    im.widget.children[5].description = 'Evaluate'



## Calc 2 Solve for x in u-substitution
def solve_for_x(sub,x):
    a = 0
    b = pi/2
    xTest = uniform(a, b)
    uTest = sub.rhs().substitute(x = xTest)
    
    ## If first test point was not in domain, then choose a different test point in a range which gets wider and wider
    if (imag(uTest) != 0):
        count = 0
        while(imag(uTest) != 0):
            a = 0 - 10^count
            b = 10 + 10^count
            xTest = randint(a, b)
            uTest = sub.rhs().substitute(x = xTest)
            count = count + 1
    
    ## Find the correct solution. Had to round for precision issues
    for i in solve(sub,x):
        if(imag(i.rhs().substitute(u=uTest)) == 0):
            xTest = round(xTest,6)
            test = round(i.rhs().substitute(u = uTest),6)
            if (xTest == test):
                return i


## Calc 2 Plot Taylor Polynomial
def plot_taylor_approx(order = slider(1, 10, 1, 1), f = input_box(default = "e^x", type = str), 
                       center = input_box(default = "0", type = str), radius = input_box(default = "1", type = str)):
    x0 = N(center)
    r = N(radius)-.1
    func = sage_eval(f + "+ 0*x", locals={'x':x})
    p = plot(func,x0-r,x0+r)
    dot = point((round(x0,8), round(func.substitute(x=x0),8)), pointsize=100,rgbcolor=(1,0,0))
    ft = func.taylor(x,x0,order)
    pt = plot(ft, x0-r, x0+r, color="green", thickness=2)
    pretty_print(html(r'$f(x)\;=\;%s$'%latex(func)))
    pretty_print(html(r'$\hat{f}(x;%s)\;=\;%s+\mathcal{O}(x^{%s})$'%(center,latex(ft),order+1)))
    show(dot + p + pt)
 
def Plot_Taylor_Polynomials():
    var('x')
    im = widgets.interact_manual(plot_taylor_approx)
    im.widget.children[4].add_class("top-spacing-class")
    display(HTML(
         "<style>.top-spacing-class {margin-top: 20px;}</style>"
    ))
    im.widget.children[4].description = 'Evaluate'