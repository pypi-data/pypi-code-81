"""Rawls rendering details information
"""

# main imports
import re

# class imports
from .sampler import Sampler
from .integrator import Integrator
from .camera import Camera
from .film import Film
from .lookAt import LookAt
from .vector import Vector3f
from .filter import Filter
from .accelerator import Accelerator

expected_comments = [
    'Film', 'Samples', 'Filter', 'Sampler', 'Accelerator', 'Integrator',
    'Camera', 'LookAt'
]


class Details():
    """Details information used to rendering current image
    
    Arguments:
        film: {Film} -- x and y resolution of image
        samples: {int} -- number of samples used for generate image
        pixelfilter: {Filter} -- pixelfilter instance with information
        sampler: {Sampler} -- sampler instance with information
        accelerator: {Accelerator} -- accelerator instance with information
        integrator: {Integrator} -- integrator instance with information
        camera {Camera} -- camera instance with information
        lookAt {LookAt} -- look at instance with eye, point and up information
    """
    def __init__(self, film, samples, pixelfilter, sampler, accelerator,
                 integrator, camera, lookAt, additionals):
        """Details information used to rendering current image
        
        Arguments:
            film: {Film} -- x and y resolution of image
            samples: {int} -- number of samples used for generate image
            pixelfilter: {Filter} -- pixelfilter instance with information
            sampler: {Sampler} -- sampler instance with information
            accelerator: {Accelerator} -- accelerator instance with information
            integrator: {Integrator} -- integrator instance with information
            camera {Camera} -- camera instance with information
            lookAt {LookAt} -- look at instance with eye, point and up information
        """
        self.samples = samples
        self.pixelfilter = pixelfilter
        self.film = film
        self.accelerator = accelerator
        self.integrator = integrator
        self.sampler = sampler
        self.camera = camera
        self.lookAt = lookAt

        self.additionals = additionals

    @classmethod
    def fromcomments(self, comments):
        """Instanciate Details object with all comments information
        
        Arguments:
            comments: {str} -- extracted comments data

        Returns:
            {Details} -- details information instance
        """
        comments_line = comments.split('\n')

        samples = 1 # default number of sample..
        additionals = {}  # init additionals

        film = Film('', [], [], [])
        pixelfilter = Filter('', [], [], [])
        sampler = Sampler('', [], [], [])
        accelerator = Accelerator('', [], [], [])
        integrator = Integrator('', [], [], [])
        camera = Camera('', [], [], [])
        lookAt = LookAt([0, 0, 0], [0, 0, 0], [0, 0, 0])

        for index, line in enumerate(comments_line):

            if 'Film' in line:
                film_name = line.split(' ')[-1]

                params_names, params_values, params_types = self._extract_params(
                    comments_line[index + 1])
                film = Film(film_name, params_names, params_values,
                            params_types)

            if 'Samples' in line:
                samples = int(line.split(' ')[-1])

            if 'Filter' in line:

                # check if filter is used
                if len(line.split(' ')) >= 2:
                    filter_name = line.split(' ')[-1]

                    params_names, params_values, params_types = self._extract_params(
                        comments_line[index + 1])
                    pixelfilter = Filter(filter_name, params_names,
                                         params_values, params_types)
                else:
                    pixelfilter = Filter('', [], [], [])

            if 'Sampler' in line:
                sampler_name = line.split(' ')[-1]

                params_names, params_values, params_types = self._extract_params(
                    comments_line[index + 1])
                sampler = Sampler(sampler_name, params_names, params_values,
                                  params_types)

            if 'Accelerator' in line:

                if len(line.split(' ')) >= 2:
                    accelerator_name = line.split(' ')[-1]

                    params_names, params_values, params_types = self._extract_params(
                        comments_line[index + 1])
                    accelerator = Accelerator(accelerator_name, params_names,
                                              params_values, params_types)

                else:
                    accelerator = Accelerator('', [], [], [])

            if 'Integrator' in line:
                integrator_name = line.split(' ')[-1]

                params_names, params_values, params_types = self._extract_params(
                    comments_line[index + 1])
                integrator = Integrator(integrator_name, params_names,
                                        params_values, params_types)

            if 'Camera' in line:
                camera_name = line.split(' ')[-1]

                params_names, params_values, params_types = self._extract_params(
                    comments_line[index + 1])
                camera = Camera(camera_name, params_names, params_values,
                                params_types)

            if 'LookAt' in line:
                info = line.split()
                del info[0]
                info = [float(i) for i in info]

                eye = Vector3f(info[0], info[1], info[2])
                point = Vector3f(info[3], info[4], info[5])
                up = Vector3f(info[6], info[7], info[8])

                lookAt = LookAt(eye, point, up)

            # check if additionals comments already use
            if line.startswith('#') and not any(
                [f in line for f in expected_comments]):

                additional_key = line.split(' ')[0][1:]
                additional_value = line.split(' ')[-1]

                additionals[additional_key] = additional_value

        return Details(film, samples, pixelfilter, sampler, accelerator,
                       integrator, camera, lookAt, additionals)

    @classmethod
    def _extract_params(self, line):
        """Extract params information of module
        Arguments:
            line: {str} -- params line of rawls file of renderer element

        Returns:
            [([{str}], [{str}], [{str}])] -- tuple of names, values and types of params extracted
        """
        params = re.findall(r'"[a-z]*\ [a-z]*"', line)

        params_names = [p.split(' ')[-1].replace('"', '') for p in params]
        params_types = [p.split(' ')[0].replace('"', '') for p in params]

        values = re.findall(r'\[([0-9.]*|"[a-z.]*"|"[A-Za-z0-9._-]*")\ ?\]',
                            line)

        params_values = [
            p.replace('[', '').replace(']', '').strip().replace('"', '')
            for p in values
        ]

        return (params_names, params_values, params_types)

    def __str__(self):
        """Display Details object representation
        
        Returns:
            {str} -- details information
        """
        return '\tSamples: {0}\n\t{1}\n\t{2}\n\t{3}\n\t{4}\n\t{5}\n\t{6}\n\t{7}'.format(
            self.samples, self.pixelfilter, self.film, self.sampler,
            self.accelerator, self.integrator, self.camera, self.lookAt)

    def to_rawls(self):
        """Display Details information for .rawls file
        
        Returns:
            {str} -- details information for .rawls file
        """
        return '#Samples {0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}'.format(
            self.samples, self.pixelfilter.to_rawls(), self.film.to_rawls(),
            self.sampler.to_rawls(), self.accelerator.to_rawls(),
            self.integrator.to_rawls(), self.camera.to_rawls(),
            self.lookAt.to_rawls())
