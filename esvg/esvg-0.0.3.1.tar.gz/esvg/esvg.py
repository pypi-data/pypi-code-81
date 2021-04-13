# -*- coding: utf-8 -*-

# This code is part of ESVG.
#
# (C) Copyright Easygraph 2020.
#
"""
ESVG engine main class. Contains methods for interpreting and transforming both
SVGs and ESVGs.
"""

from bs4 import BeautifulSoup
import json
import copy
import re

from . import easings


def linear_mapping(x, xmin, xmax, ymin=0, ymax=1):
    a = (ymax - ymin)/(xmax - xmin)
    b = ymin - a*xmin
    return a * x + b

def unit_inc(val,inc):
    """
        Returns an unit increment from an svg attribute given the str val and
        a float inc

        >>> unit_inc("80px",5)
        "85px"
    """
    # svg_units ref: https://oreillymedia.github.io/Using_SVG/guide/units.html
    # TODO Seguro que esto se puede hacer mejor pero no quiero meter re en requirements...
    SVG_UNITS = ["px","rem","ex","ch","em","vmin","min","in","cm","mm","pt","pc","vw","vh","vmax",
                 "grad","rad","deg","turn","s","ms","h"]
    for u in SVG_UNITS:
        if u in val:
            num_val = float(val.rsplit(u,1)[0])+inc
            return f"{num_val}{u}"
    return str(float(val)+inc)

def translate_inc(svg_elem,x,y):
    """
        Increases a svg element position given by a transform="translate(a,b)"
        by x and y in the unit of a and b.
    """
    # expresion regular para identificar el translate de los attrs del svg
    TRANSLATE_REGEX = "translate\((\d*[.]?\d*),*(\d*[.]?\d*)\)"
    # obtenemos el transform
    transform_str = svg_elem.attrs["transform"]
    # sacamos el antiguo x e y de los atributos
    re_x,re_y = re.findall(TRANSLATE_REGEX,transform_str)[0]
    # incrementamos x e y. Ojo a que la y es opcional en svg
    new_x = float(re_x) + x
    if re_y:
        new_y = float(re_y) + y
    else:
        new_y = 0
    # creamos la nueva invocacion a translate y la reemplazamos
    new_translate_str = f"translate({new_x},{new_y})"
    if re_y:
        new_transform_str = transform_str.replace(f"translate({re_x},{re_y})",new_translate_str)
    else:
        new_transform_str = transform_str.replace(f"translate({re_x})",new_translate_str)
    svg_elem.attrs["transform"] = new_transform_str


class ESVG:
    """Implements a `.esvg` file interpreter, used for esvg data loading and
    SVG conversion.
    """

    BS_PARSER = "lxml"
    XML_PROLOG = '<?xml version="1.0" encoding="utf-8"?>\n'
    GENERATOR = "<!-- Generator: Easygraph 0.0.1, SVG Export. -->\n"

    EASING_DICT = {
        "poly5" : easings.poly5,
        "circquarter" : easings.circ_quarter,
        "spring" : easings.spring
    }
    DEFAULT_N_KEYFRAMES = 20

    def __init__(self,in_path=None, data_path=None):
        """Initates an ESVG interpreter.

        Args:
            in_path (:obj: `str`, optional): path to `.esvg` file to be read.
            data_path (:obj: `str`, optional): path to data file to load.
        """

        self.in_path = in_path
        self.data_path = data_path

        if in_path:
            # cargar archivo
            self.fp = open(in_path)
            # crear soup
            self._load_esvg(self.fp.read())
        
        if data_path:
            self._load_data(data_path)

    def _load_esvg(self, esvg: str):
        
        esvg_soup = BeautifulSoup(esvg, ESVG.BS_PARSER)

        # identificamos etiqueta xml
        self.heading = ESVG.XML_PROLOG
        self.encoding = 'utf-8'
        # identificar <data>
        self.data = esvg_soup.data
        
        # identificar placeholders
        self.defs_refs = [c for c in self.data.children if c.name == 'def']
        # crear lista de placeholders
        self.defs = {}
        for d in self.defs_refs:
            self.defs[d.attrs['name']] = dict(d.attrs)
            self.defs[d.attrs['name']]["bind_defs"] = []
        
        # identificar tiempos
        self.times_refs = [c for c in self.data.children if c.name == 'time']
        # crear lista de tiempos
        self.times = {}
        for d in self.times_refs:
            self.times[d.attrs['name']] = dict(d.attrs)

        # identificar <svg>
        self.svg = esvg_soup.svg
        # buscar referencias a placeholders
        for r in self.defs.values():
            name = r['name']
            svg_refs = []
            if r['type'] != "text":
                refs = self.svg.find_all((lambda tag: any([(f'@{name}' in v) for v in tag.attrs.values()])))
                svg_refs += [{'ref': r, 'attrs': [k for k in r.attrs.keys() if (f'@{name}') in r.attrs[k] ]} for r in refs ]

            # TODO: Concertar una forma de escapar los '@'
            refs = self.svg.find_all(lambda tag: tag.name=="text" and  any([(f"@{name}" in c) for c in tag.contents]))
            if refs:
                r['has_contents'] = True
                svg_refs += [{'ref': r, 'attrs': ["contents"]} for r in refs]
            # guardar referencia al atributo
            r["svg_refs"] = svg_refs 

        # buscar y guardar referencias "bind" a placeholders
        for r in self.defs.values():
            if "bind" in r:
                self.defs[r["bind"]]["bind_defs"] += [r['name']]

        # identificar copies
        self.copies_refs = [c for c in self.data.children if c.name == 'copy']
        # crear lista de repeats
        self.copies = {}
        for c in self.copies_refs:
            self.copies[c.attrs['name']] = dict(c.attrs)
            # identificar elemento svg
            svg_elem = esvg_soup.svg.find(id=c["elementid"])
            # buscar las propiedades de placeholder de ese elemento
            # TODO: antes buscabamos del elemento en si los phs,
            # ahora de los phs buscamos el elemento
            svg_ph_props = [ph for ph in self.defs if any((svg_elem == ph_svg_ref['ref']) for ph_svg_ref in self.defs[ph]['svg_refs']) ]
            # de esas comprobar cuales son multiples
            svg_multiple_ph_props = [ph for ph in svg_ph_props if "multiple" in self.defs[ph]]
            self.copies[c.attrs['name']]['svg_elem'] = svg_elem
            self.copies[c.attrs['name']]['svg_ph_props'] = svg_ph_props
            self.copies[c.attrs['name']]['svg_multiple_props'] = svg_multiple_ph_props

        # si no hay copies
        if not len(self.copies_refs):
            # guarda los valores por defecto
            self._load_default_data()


        self.esvg_soup = esvg_soup

        pass

    @property
    def _defs_server_view(self):
        client_keys = ['svg_refs', 'bind', 'bind_defs']
        view = {}
        for key, def_dict in self.defs.items():
            view[key] = { k: def_dict[k] for k in def_dict.keys() if k not in client_keys }
        return view

    @property
    def _times_server_view(self):
        return { k: self.times[k] for k in self.times.keys() }

    @property
    def _copies_server_view(self):
        client_keys = ['svg_elem', 'svg_ph_props', 'svg_multiple_props']
        view = {}
        for key, copy_dict in self.copies.items():
            view[key] = { k: copy_dict[k] for k in copy_dict.keys() if k not in client_keys }
        return view


    DEFAULT_DUR = "1s"
    DEFAULT_UNIT = "px"

    def _load_default_data(self):
        # TODO: Aquí deberíamos guardar el resto de propiedades por defecto, como las de animación
        self.values = { placeholder: { 'dynamic':False, 'value': self.defs[placeholder].get('default',self.defs[placeholder]['min']) } for placeholder in self.defs.keys() }
        pass

    def _user_data_to_svg_data(self, prop, value):
        '''
            value: number in [0, 1] if numeric or slider
        '''
        svg_value = None
        # interpolamos el valor para adaptarlo a grafica SVG si necesario
        def_prop = self.defs[prop]
        if (def_prop['type'] == 'numeric' or def_prop['type'] == 'slider'):
            # TODO: Catch error
            svg_value = float(def_prop['max']) * value + float(def_prop['min'])
        else:
            svg_value = value

        svg_value = {'dynamic': False, 'value': svg_value}

        if 'time' in def_prop.keys(): # Valor animado
            svg_value = self._set_animation(svg_value, def_prop, self.times[def_prop['time']])

        return svg_value

    def _prepare_multiple_dict(self, placeholders):
        new_placeholders = {}
        for ph_name, ph_object in placeholders.items():
            # si no es una lista se copia
            if type(ph_object) != list:
                new_placeholders[ph_name] = self._user_data_to_svg_data(ph_name, ph_object)
            # de lo contrario es que tenemos valores multiples
            else:
                def_prop = self.defs[ph_name]
                if 'multiple' not in def_prop:
                    pass # TODO: Raise value error
                # Si el valor es de tipo numerico o slider lo llevamos a [0, 1]
                if (def_prop['type'] == 'numeric' or def_prop['type'] == 'slider'):
                    M = float(def_prop.get('sup',max(ph_object)))
                    m = float(def_prop.get('inf',min(ph_object)))
                    values = [ linear_mapping(value, m, M) for value in ph_object]
                else:
                    values = ph_object
                new_placeholders[ph_name] = [self._user_data_to_svg_data(ph_name, value) for value in values ]

        return new_placeholders

    def _prepare_bind(self,placeholders):
        old_placeholders = list(placeholders.keys())
        for ph_name in old_placeholders:
            for ph_bind_name in self.defs[ph_name]['bind_defs']:
                placeholders[ph_bind_name] = placeholders[ph_name]

        return placeholders

    def _prepare_copy_svg(self,placeholders):
        # por cada copy
        for c in self.copies.values():
            # identificar elemento svg
            svg_elem = c['svg_elem']
            # de esas comprobar cuales son multiples
            svg_multiple_ph_props = c['svg_multiple_props']
            svg_ph_props = c['svg_ph_props']
            # repetimos tantas veces como min( len(p) for p in element.placeholders multiples )
            copy_times = min(( len(placeholders[ph]) if type(placeholders[ph])==list else 0) for ph in svg_multiple_ph_props) - 1

            # TODO: Poner timeoffset en _dynamic_fill
            # set del timeoffset en el def adecuado
            # TODO: ¿y si establecen el offset sin segundos?
            time_offset = float(c.get("timeoffset","0s").rsplit('s',1)[0])
            if time_offset:
                for ph in svg_multiple_ph_props:
                    self.defs[ph]['time_offset'] = time_offset

            x_offset = float(c.get("xoffset",0))
            y_offset = float(c.get("yoffset",0))
            rgb_offset = c.get("rgboffset",None)

            use_translate = ("transform" in svg_elem.attrs and "translate" in svg_elem["transform"])

            if rgb_offset:
                rgb_offset = tuple(map(float,rgb_offset.split(',')))

            if not use_translate:
                if x_offset and not "x" in svg_elem.attrs:
                    svg_elem.attrs['x'] = "0"
                if y_offset and not "y" in svg_elem.attrs:
                    svg_elem.attrs['y'] = "0"

            # se toma el elemento inicial
            prev_elem = svg_elem
            # por cada vez que haya que copiar
            for _ in range(copy_times):
                # copiamos del anterior
                new_elem = copy.copy(prev_elem)
                # aplicamos offsets
                if not use_translate:
                    if x_offset:
                        new_elem.attrs['x'] = unit_inc(new_elem.attrs['x'],x_offset)
                    if y_offset:
                        new_elem.attrs['y'] = unit_inc(new_elem.attrs['y'],y_offset)
                else:
                    translate_inc(new_elem,x_offset,y_offset)
                if rgb_offset:
                    # TODO: Habra que atender a si se incrementa un fill, un linefill, un background, etc.
                    pass
                # insertamos despues del previo
                prev_elem.insert_after(new_elem) 
                for ph in svg_ph_props:
                    ph_def = self.defs[ph]
                    # lo añadimos al svg_refs del def para los fills
                    if ph_def['type'] != "text": 
                        new_svg_ref = {'ref': new_elem, 'attrs': [k for k in new_elem.attrs.keys() if (f"@{ph}") in new_elem.attrs[k] ]}
                        ph_def['svg_refs'].append(new_svg_ref)
                    if 'has_contents' in ph_def:
                        new_svg_ref = {'ref': new_elem, 'attrs': ["contents"]}
                        ph_def['svg_refs'].append(new_svg_ref)
                # cambiamos de elemento previo para el bucle
                prev_elem = new_elem
            pass
        pass

    def _set_animation(self, ph_object, def_ref,time):
        ph_animation = {}
        ph_animation['time'] = time['dur']
        ph_animation['start'] = time.get('start',"0s")
        # TODO: Obtener default del default con una funcion
        ph_animation['units'] = def_ref.get('units',ESVG.DEFAULT_UNIT)
        easing = time.get('easing','linear')
        easing_params = [(float(v) if v!='' else None) for v in time.get('easingparams','').split(';')]
        initial, final = float(def_ref['min']), ph_object['value']
        if easing == 'linear':
            ph_animation['values'] = [initial, final]
        else:
            #linear_vals = [(initial + (i/ESVG.DEFAULT_N_KEYFRAMES)*(final-initial)) for i in range(ESVG.DEFAULT_N_KEYFRAMES+1)]
            easing_vals = [ESVG.EASING_DICT[easing](*easing_params)(v/ESVG.DEFAULT_N_KEYFRAMES) for v in range(ESVG.DEFAULT_N_KEYFRAMES+1)]
            ph_animation['values'] = [initial+e*(final-initial) for e in easing_vals]
        # TODO: Esto estaba así antes, pero para animaciones con start != 0 se ve raro
        #return {'dynamic': True, 'value': ph_object['value'], 'animation': ph_animation}
        return {'dynamic': True, 'value': initial, 'animation': ph_animation}

    def _get_values_from_placeholders(self, placeholders):
        for ph_name, ph_object in placeholders.items(): 
            self.values[ph_name] = ph_object

    def _load_data_json(self, data_path: str):
        # TODO: reescribimos values, ¿no?
        self.values = {}
        with open(data_path) as f: 
            json_data = json.load(f)
            placeholders = json_data["data"]
           
            placeholders = self._prepare_bind(placeholders)
            self._prepare_copy_svg(placeholders) # Do only if copies exists
            placeholders = self._prepare_multiple_dict(placeholders)
            self._get_values_from_placeholders(placeholders)
    
    def _load_data_json_dict(self, json_string):
        self.values = {}
        json_data = json.loads(json_string)
        placeholders = json_data['data']
        placeholders = self._prepare_bind(placeholders)
        self._prepare_copy_svg(placeholders) # Do only if copies exists
        placeholders = self._prepare_multiple_dict(placeholders)
        self._get_values_from_placeholders(placeholders)

    def load_data(self, data_path: str):
        """Loads the data to be filled onto the ESVG.

        Args:
            data_path (:obj: `str`): path to data file to load.
        """

        if ".json" in data_path:
            self._load_data_json(data_path)
        
        pass

    def _static_fill(self,placeholder):
        for i,r in enumerate(self.defs[placeholder]['svg_refs']):
            ref = r['ref']
            ph_value = self.values[placeholder]
            for attr in r['attrs']:
                # obtener el valor
                if type(ph_value)==list:
                    new_value = self.values[placeholder][i]['value']
                else:
                    new_value = self.values[placeholder]['value']
                if attr != 'contents':
                    # reemplazar (por si hay expresiones tipo transform(@x,@y))
                    new_attr = ref.attrs[attr].replace(f"@{placeholder}",str(new_value))
                    # asignar
                    ref.attrs[attr] = new_attr
                else:
                    # los campos de tipo text solo tienen un elemento en contents
                    # que es todo el texto incluido (no importa los \n que haya)
                    new_text = ref.contents[0].replace(f"@{placeholder}",str(new_value))
                    ref.string.replace_with(new_text)

    @classmethod
    def _animate_time_fill(cls, animate, ph_animation):
        time = ph_animation['time']
        start = ph_animation['start']
        animate.attrs['dur'] = time
        animate.attrs['begin'] = start
        animate.attrs['fill'] = "freeze"

    @classmethod
    def _animate_value_fill(cls,animate, placeholder, ph_animation, attr, svg_ref):
        str_values = [str(u)+ph_animation["units"] for u in ph_animation["values"]] 
        new_attrs = [svg_ref.attrs[attr].replace(f"@{placeholder}",val) for val in str_values]
        animate.attrs['values'] = ';'.join(new_attrs) 
        animate.attrs['attributeName'] = attr

    def _dynamic_fill(self, placeholder):
        # funcion para realizar el fill dinamico de un svg una vez cargados los datos
        ph_list = self.values[placeholder]
        ph_def = self.defs[placeholder]
        if type(ph_list) != list:
            ph_list = [ph_list]*len(self.defs[placeholder]['svg_refs'])
        for i,ph_object in enumerate(ph_list):
            ph_animation = ph_object['animation']
            if "time_offset" in ph_def:
                ph_animation['start'] = unit_inc(ph_animation['start'],i*ph_def['time_offset'])
            # por cada referencia de los placeholders
            r = self.defs[placeholder]['svg_refs'][i]
            ref = r['ref']
            # creamos una tag animate (no se añade a ningun lado)
            animate = self.esvg_soup.new_tag("animate")
            values = ph_animation['values']
            # los valores pueden ser par valor-keyframe o solo la lista de valores
            if type(values[0]) == tuple:
                # unzipeamos valores y keyframes y añadimos los ultimos al tag
                values, keyframes = zip(*values)
                animate.attrs['keyTimes'] = ';'.join([str(k) for k in keyframes])

            # llenamos los values del animate
            ESVG._animate_time_fill(animate,ph_animation)

            # hay que crear un animate por atributo, asi que ahora los copiamos
            for attr in r['attrs']:
                if attr != 'contents':
                    ESVG._animate_value_fill(animate,placeholder,ph_animation,attr,ref)
                    new_anim = copy.copy(animate)
                    ref.append(new_anim)

    def _write_heading(self, f):
        f.write(self.heading.encode(self.encoding))
        f.write(ESVG.GENERATOR.encode(self.encoding))

    def toSVG(self, out_path=None, to_file=True):
        """Transforms the ESVG with the previously filled data into a SVG.

        Args:
            out_path (:obj: `str`, optional): path to saved svg file. If not
            given any, it defaults to the same path where the .esvg was stored.
            to_file (:obj: `bool`, optional): If False, returns str with the
            .svg data.
        """
        if not out_path and to_file:
            out_path = f'{self.in_path[:-4]}svg'

        for placeholder in self.values.keys():
            # dividimos el 'data fill' segun el dato sea estatico o dinamico
            if 'time' in self.defs[placeholder]:
                self._dynamic_fill(placeholder)
            self._static_fill(placeholder)

        if to_file:
            with open(out_path, 'wb') as f:
                self._write_heading(f)
                f.write(self.svg.encode(self.encoding))
        else:
            ret = self.heading.encode(self.encoding) + ESVG.GENERATOR.encode(self.encoding)
            ret += self.svg.encode(self.encoding)
            return ret

    def toGIF(self, out_path=None, to_file=True):
        """Transforms the ESVG object with previously filled data into a GIF.


        Args:
            out_path (:obj: `str`, optional): path to saved svg file. If not
            given any, it defaults to the same path where the .esvg was stored.
            to_file (:obj: `bool`, optional): If False, returns str with the
            .gif data.
            
        """
        if not out_path and to_file:
            out_path = f'{self.in_path[:-4]}svg'

        svg = self.toSVG(to_file=False)
        # TODO: Seguir investigando una librería de parseo svg -> gif
        pass


    @classmethod
    def generateSVG(cls,in_path: str,data_path: str,out_path=None, to_file=True):
        """Generates a SVG given a `.esvg` file and its data file.

        Args:
            in_path (str): path to `.esvg` file to be read.
            data_path (str): path to data file to load.
            out_path (str): path to saved svg file.
        """
        tmp_esvg = ESVG(in_path)
        tmp_esvg.load_data(data_path)
        return tmp_esvg.toSVG(out_path,to_file=to_file)

    @classmethod
    def uploadESVG(cls, esvg: str):
        """Creates an ESVG instance given str data of the .esvg file.

        Args:
            esvg (str): the .esvg file read as a str

        Returns:
            ESVG object with the esvg str parsed and loaded.

        """
        return_esvg = ESVG()
        return_esvg._load_esvg(esvg)
        return return_esvg
