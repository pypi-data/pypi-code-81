import pywin10ui

window = pywin10ui.Window("DEMO",200,200)

canvas = window.create()

button = pywin10ui.Button(canvas,1,1,"Button",100,20)
entry = pywin10ui.Entry(canvas,1,25,"Entry",100,20)
progress_bar = pywin10ui.Progress_bar(canvas,1,50,100,20,100,50)
select_box = pywin10ui.Select_box(canvas,1,75,"Select_box")

while 1:
    canvas.fill((240,240,240))
    button.mainloop()
    entry.mainloop()
    progress_bar.mainloop()
    select_box.mainloop()
    window.mainloop()