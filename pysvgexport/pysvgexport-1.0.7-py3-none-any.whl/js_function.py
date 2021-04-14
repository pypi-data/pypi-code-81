retrieve_input_props = '''
    (svg_element) => {
        let el = svg_element;
        let widthAttr = el.getAttribute('width');
        let heightAttr = el.getAttribute('height');
        let viewBoxAttr = el.getAttribute('viewBox');
        if (widthAttr && heightAttr && !/\%\s*$/.test(widthAttr) && !/\%\s*$/.test(heightAttr)) {
            return {
                size: true,
                left: 0,
                top: 0,
                width: el.width.animVal.value,
                height: el.height.animVal.value
            };
        } else if (viewBoxAttr && el.viewBox) {
            return {
                viewbox: true,
                left: el.viewBox.animVal.x,
                top: el.viewBox.animVal.y,
                width: el.viewBox.animVal.width,
                height: el.viewBox.animVal.height
            };
        } else {
            let box = el.getBBox();
            return {
                bbox: true,
                left: box.x,
                top: box.y,
                width: box.width,
                height: box.height
            };
        }
    }
'''

transform_svg_element = '''
    (input, scale, clip) => {
        const svg = document.getElementsByTagName('svg')[0];
        if (!input.viewbox && !svg.getAttribute('viewBox')) {
            svg.setAttribute('viewBox', '0 0 ' + input.width + ' ' + input.height);
            svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
        }
        svg.removeAttribute('width');
        svg.removeAttribute('height');
    
        svg.style.setProperty('margin', 0, 'important');
        svg.style.setProperty('border', 0, 'important');
        svg.style.setProperty('padding', 0, 'important');
        svg.style.setProperty('position', 'fixed', 'important');
    
        if (clip.x < 0) {
            svg.style.setProperty('left', Math.abs(clip.x) + 'px', 'important');
        } else {
            svg.style.setProperty('left', 0, 'important');
        }
    
        if (clip.y < 0) {
            svg.style.setProperty('top', Math.abs(clip.y) + 'px', 'important');
        } else {
            svg.style.setProperty('top', 0, 'important');
        }
    
        svg.style.setProperty('width', (input.width * scale) + 'px', 'important');
        svg.style.setProperty('height', (input.height * scale) + 'px', 'important');
    }
'''

transform_output_element = '''
    (input, output, clip) => {
        const svg = document.getElementById('output_frame_29010701');
        svg.style.setProperty('left', clip.x + 'px', 'important');
        svg.style.setProperty('top', clip.y + 'px', 'important');

        svg.style.setProperty('width', input.width * output.scale + 'px', 'important');
        svg.style.setProperty('height', input.height * output.scale + 'px', 'important');
    }
'''
