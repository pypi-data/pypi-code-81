from simanim import *

def setup(m):
	PixelsPerUnit(5)
	ViewBox((0, 0), 90, 60)
	m.x = InputFloat(30.0, (0, 30))
	m.pos = 0
	m.uspori = InputList(1, [1, 10, 40])

def update(m):
	m.pos = m.pos + 1
	if m.pos > 90:
		Finish()

def draw(m):
	krug = Circle((m.pos,20),10)
	krug.fill_color = '#007f00'
	Draw(krug)
	tekst = Text((0,m.uspori),'cao')
	tekst.pen_color = 'black'
	Draw(tekst)
	box = Box((20,20),20,10)
	box.line_width = 1
	Draw(box)
	tocak = Image('wheel.png', (10, 10), 10, 10)
	Draw(tocak)
	vec_v = Arrow((1, 0), (10, 10))
	vec_v.pen_color = '#0000a0'
	vec_v.head_len = 1.5

	Draw(vec_v)		

	poly = PolyLine([(10,10),(25,5),(1,50)])
	poly.pen_color = 'black'
	Draw(poly)

	with Rotate((30, 30), 3.14):
		Draw(tekst)

	tekst = Text((0,m.x),'cao 2')
	Draw(tekst)

Run(setup, update, draw)