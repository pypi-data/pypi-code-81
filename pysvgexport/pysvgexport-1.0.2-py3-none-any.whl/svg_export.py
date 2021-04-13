import asyncio
import io
import os
import time

from PIL import Image
from pyppeteer import launch

from pysvgexport.js_function import retrieve_input_props, transform_svg_element, transform_output_element

chromium = os.environ.get("CHROMIUM_EXECUTABLE_PATH")
empty_page = os.environ.get("EMPTY_PAGE_URL", "about:blank")


class SVGExport:
    def __init__(self, svg_data, capture_options, output_options):
        self.svg_data = svg_data
        self.capture_options = {
            "left": 0,
            "top": 0,
            **capture_options
        }
        self.output_options = output_options

    def execute(self):
        return asyncio.get_event_loop().run_until_complete(self.render_svg())

    async def render_svg(self):
        browser_options = {
            'headless': True,
            'args': ['--no-sandbox', '--font-render-hinting=none']
        }
        if os.environ.get("CHROMIUM_EXECUTABLE_PATH"):
            browser_options.update({'executablePath': os.environ.get("CHROMIUM_EXECUTABLE_PATH")})

        browser = await launch(browser_options)
        page = await browser.newPage()
        await page.goto(empty_page)
        html = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>svg</title>
            </head>
            <body style="
                    margin: 0 !important;
                    border: 0 !important;
                    padding: 0 !important;
                  ">
                <div id="output_frame_29010701" style="
                    margin: 0 !important;
                    border: 0 !important;
                    padding: 0 !important;
                    position: fixed !important;
                "> 
                    {self.svg_data}
                </div>
            </body>
            </html>
        '''

        await page.setContent(html)

        svg_element = await page.querySelector('svg')
        input_props = await page.evaluate(retrieve_input_props, svg_element)

        clip = {
            "x": self.capture_options['left'] - input_props['left'] * self.capture_options['scale'],
            "y": self.capture_options['top'] - input_props['top'] * self.capture_options['scale']
        }

        await page.evaluate(transform_svg_element, input_props, self.capture_options['scale'], clip)

        clip['x'] = max(clip['x'], 0)
        clip['y'] = max(clip['y'], 0)

        await page.evaluate(transform_output_element, input_props, self.capture_options, clip)

        output_element = await page.querySelector('#output_frame_29010701')
        time.sleep(0.5)
        image_data = await output_element.screenshot(self.output_options)
        result_image = Image.open(io.BytesIO(image_data))
        await browser.close()
        return result_image
