from typing import Callable
from simanim.abstract.core import AnimVars, AnimContext, InputFloat, InputList
from .driver import DrawingDriverJs
import inspect
import js

class Animation:
        def __init__(self, anim_context: AnimContext, animation_key: str):
            self.anim_context = anim_context
            self.animation_key = animation_key
            self.input_getters: Dict[str,Callable[[],float]] = dict()
            self.endAnimation = False

        # ovde dodati definicije metoda koje želimo da budu pozivana iz JS dela implementacije
        # JS deo implementacije pokrene skript sa animacijom praktično samo da bi se napravio objekat
        # ove klase (tj. instancu animacije), a posle poziva metode iz instance animacije po potrebi (više detalja u komentaru ispod)
        def queueFrame(self):
            driver = DrawingDriverJs(self.anim_context.settings, self.animation_key)
            self.anim_context.driver(driver)
            self.anim_context.draw_frame()
            self.anim_context.driver(None)
            self.updateBetweenFrames()

        def updateBetweenFrames(self):
            cont = self.anim_context.updates_between_frames()
            if not cont:
                self.endAnimation = True

        def resetAnimation(self):
            self.anim_context.reset(self.input_getters)
            self.endAnimation = False

        def setVarGetters(self, var_values):
            for var_name, var_meta in self.anim_context.vars._input_vars.items():
                var_input_element_id = var_values[var_name]
                self.input_getters[var_name] = lambda var_input_element_id = var_input_element_id, t=type(var_meta.default) if isinstance(var_meta, InputList) else type(float()) : t(js.document.getElementById(var_input_element_id).value)
            self.anim_context.reset(self.input_getters)

        def getVars(self):
            vars = []
            for var_name, var_meta in self.anim_context.vars._input_vars.items():
                if isinstance(var_meta, InputFloat):
                    var_meta.type = 'InputFloat'
                    vars.append({'name':var_name,'meta' :var_meta})
                elif isinstance(var_meta, InputList):
                    var_meta.type = 'InputList'
                    vars.append({'name':var_name,'meta' :var_meta})
            return vars

        def getEndAnimation(self):
            return self.endAnimation



# U odnosu na qt verziju, računati da će deo posla da se radi u javascript nakon što se završi izvršavanje skripta. 
# U globalnom kontekstu ovog modula će sostati animation_instance i javacrript deo implementacije treba prvo da
# pozove skript, a posle da pristupa objektu u aanimation_instance. Pristup iz JS bi trebalo da može da se napravisa:
#
# animation_instance = pyodide.RunPython(`
# from simanim.pyodide.qui import animation_instance
# animation_instance`)
#
# Onda u klasu Animation dodajemo metode koje želimo da budu eksponirane prema JS delu implementacije. Na taj način će deo koda
# iz Qt verzije možda da se prenese u nutar tih metoda, a deo da se imlementira kao adevatna funkcionalnost u JS delu.
#
# Imati u vidu da svaki modul u pythonu ima svoj
# globalni scope, a da je ono što je u globalnom scopeu skripta, praktično globalni scope ad-hoc modula u kome se izvršava skript.
# To bi trebalo znači da ako čuvamo nešto u globalnom scope-u ovog module, to će ostati i kada se skript pozove sa praznim 
# rečnikom za globlane promenljive, ali u svakom slučaju ćemo nekako produvati da se to dohvati.
#
# Ako bude bilo potrebno da postoji više animacija istovremeno aktivno, i to će biti moguće, samo ćemo onda imati više
# Animation klasa u jednom rečniku i svaka instanca animacije će po nekom ključu da bude dohvaćena. Neće biti problem što
# imamo samo jednu instancu Python interpretera, jer svaki skrišt napravi svoj Animation objekat i sve što je specifično
# za tu animaciju stoji u posebnom objektu. Samo će JS deo implementacije da pre pokretanja skripta u nekoj globalnoj promenljivoj
# stavi kako će da se zove instanca animacije koja se pravi, pa bi se u funkciji ispod instanca animacije stavila u rečnik pod tim 
# ključem. 
def Run(setup_handler:Callable[[AnimVars], None], update_handler:Callable[[AnimVars], None], draw_handler:Callable[[AnimVars], None]):
    global animation_instance
    if 'animation_instance' not in globals():
        animation_instance = dict()
    anim_context = AnimContext(setup_handler, update_handler, draw_handler)
    fr = inspect.stack()
    for i in fr:
        caller_frame = i[0]
        global_scope = dict(caller_frame.f_globals.items())
        if 'animation_instance_key' in global_scope:
            animation_key = global_scope['animation_instance_key']
    animation_instance[animation_key] = Animation(anim_context, animation_key)


