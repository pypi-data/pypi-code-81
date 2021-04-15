"""Rawls class used to open `.rawls` path image
"""

# main imports
import math
import numpy as np
import struct
import copy
import os

# image processing imports
from PIL import Image

# package imports
from .scene.details import Details

# astropy
from astropy.io import fits

extensions = ['png', 'rawls', 'fits']
expected_comments = ['']


class Rawls():
    """Rawls class used to open `.rawls` path image

    Attributes:
        shape: {(int, int, int)} -- describe shape of the image
        data: {ndrray} -- buffer data numpy array
        details: {Details} -- details instance information
        gamma_converted: {Details} -- specify if Rawls instance is gamma converted or not
    """
    def __init__(self, shape, data, details, gamma_converted=False):
        """Rawls constructor

        Attributes:
            shape: {(int, int, int)} -- describe shape of the image
            data: {ndrray} -- buffer data numpy array
            details: {Details} -- details instance information
            gamma_converted: {Details} -- specify if Rawls instance is gamma converted or not
        """

        self.shape = shape
        self.data = data
        self.details = details
        self.gamma_converted = gamma_converted

    @classmethod
    def load(self, filepath):
        """Open data of rawls or fits file
        
        Arguments:
            filepath: {str} -- path of the .rawls or .fits file to open

        Returns:
            {Rawls} : Rawls instance
        """

        extension = filepath.split('.')[-1]

        if extension not in ['rawls', 'fits']:
            raise Exception('filepath used is not valid')

        if '.rawls' in filepath:
            f = open(filepath, "rb")

            # finding data into files
            ihdr_line = 'IHDR'
            ihdr_found = False

            comments_line = 'COMMENTS'
            comments_found = False

            data_line = 'DATA'
            data_found = False

            # prepare rawls object data
            img_chanels = None
            img_width = None
            img_height = None

            comments = ""
            data = None

            # read first line
            line = f.readline()
            line = line.decode('utf-8')

            while not ihdr_found:

                if ihdr_line in line:
                    ihdr_found = True

                    # read shape info line
                    shape_size = int(f.readline().replace(b'\n', b''))

                    values = f.read(shape_size)
                    f.read(1)

                    img_width, img_height, img_chanels = struct.unpack(
                        'III', values)

            line = f.readline()
            line = line.decode('utf-8')

            while not comments_found:

                if comments_line in line:
                    comments_found = True

            # get comments information
            while not data_found:

                line = f.readline()
                line = line.decode('utf-8')

                if data_line in line:
                    data_found = True
                else:
                    comments += line

            # default read data size
            line = f.readline()

            buffer = b''
            # read buffer image data (here samples)
            for _ in range(img_height):

                line = f.read(4 * img_chanels * img_width)
                buffer += line

                # skip new line char
                f.read(1)

            # build numpy array from
            data = np.array(
                np.ndarray(shape=(img_height, img_width, img_chanels),
                           dtype='float32',
                           buffer=buffer))

            f.close()

            details = Details.fromcomments(comments)

            return Rawls(data.shape, data, details)

        if '.fits' in filepath:

            hdu = fits.open(filepath)

            # get comments
            hdr = hdu[0].header

            comments = hdr['Samples'] + '\n'
            comments += "#" + hdr['Filter'][1:].replace('#', '\n\t#') + '\n'
            comments += "#" + hdr['Film'][1:].replace('#', '\n\t#') + '\n'
            comments += "#" + hdr['Sampler'][1:].replace('#', '\n\t#') + '\n'
            comments += "#" + hdr['Accel'][1:].replace('#', '\n\t#') + '\n'
            comments += "#" + hdr['Inte'][1:].replace('#', '\n\t#') + '\n'
            comments += "#" + hdr['Camera'][1:].replace('#', '\n\t#') + '\n'
            comments += "#" + hdr['LookAt'][1:].replace('#', '\n\t#')

            # extract additionals
            additionals = hdr['Extra']
            for item in additionals.split('#'):
                key, value = item.split(' ')
                comments += "\n#" + key + ' ' + value

            details = Details.fromcomments(comments)

            return Rawls(hdu[0].data.shape, hdu[0].data, details)

    @classmethod
    def fusion(self, rawls_image_1, rawls_image_2):
        """Fusion two rawls images together based on their number of samples
        
        Arguments:
            rawls: {Rawls} -- first Rawls image to merge
            rawls: {Rawls} -- second Rawls image to merge

        Returns:
            {Rawls} -- Rawls instance
        """

        if not isinstance(rawls_image_1, Rawls):
            raise Exception("`rawls_image_1` parameter is not of Rawls type")

        if not isinstance(rawls_image_2, Rawls):
            raise Exception("`rawls_image_2` parameter is not of Rawls type")

        # compute merge between two `Rawls` instances
        total_samples = float(rawls_image_1.details.samples +
                              rawls_image_2.details.samples)

        image_1_percent = rawls_image_1.details.samples / total_samples
        image_2_percent = rawls_image_2.details.samples / total_samples

        buffer_image_1 = rawls_image_1.data * image_1_percent
        buffer_image_2 = rawls_image_2.data * image_2_percent

        output_buffer = np.add(buffer_image_1, buffer_image_2)

        # update details informations (here samples used)
        details = copy.deepcopy(rawls_image_1.details)
        details.samples = int(total_samples)

        return Rawls(output_buffer.shape, output_buffer, details)

    def save(self, outfile, gamma_convert=True):
        """Save rawls image into new file
        
        Arguments:
            outfile: {str} -- output filename (rawls or png)
            gamma_convert: {bool} -- necessary or not to convert using gamma (default: True)
        """

        # check if expected extension can be managed
        extension = outfile.split('.')[-1]

        if extension not in extensions:
            raise Exception("Can't save image using `" + extension +
                            "` extension..")

        # check if necessary to construct output folder
        folder_path = os.path.split(outfile)

        if len(folder_path[0]) > 1:

            if not os.path.exists(folder_path[0]):
                os.makedirs(folder_path[0])

        # save image using specific extension
        if extension == 'rawls':
            h, w, c = self.shape
            f = open(outfile, 'wb')

            f.write(b'IHDR\n')
            f.write(bytes(str(self.data.ndim * 4), 'utf-8') + b'\n')
            f.write(
                struct.pack('i', w) + struct.pack('i', h) +
                struct.pack('i', c) + b'\n')

            f.write(b'COMMENTS\n')
            f.write(bytes(self.details.to_rawls() + '\n', 'utf-8'))

            # save additionnals comments data
            for key, value in self.details.additionals.items():
                add_str = '#{0} {1}'.format(key, value)
                f.write(bytes(add_str + '\n', 'utf-8'))

            f.write(b'DATA\n')
            # integer is based on 4 bytes
            f.write(struct.pack('i', h * w * c * 4) + b'\n')

            for i in range(h):
                for j in range(w):

                    for k in range(c):
                        f.write(struct.pack('f', self.data[i][j][k]))
                f.write(b'\n')

            f.close()

        elif extension == 'png':
            self.to_png(outfile, gamma_convert)

        elif extension == 'fits':

            # using NASA fits file format
            hdu = fits.PrimaryHDU()
            hdu.data = self.data

            # add all rawls based comments (details of the scene)
            hdu.header['Samples'] = "#Samples " + str(self.details.samples)

            hdu.header['Filter'] = self.details.pixelfilter.to_rawls().replace(
                '\n', '').replace('\t', '')
            hdu.header['Film'] = self.details.film.to_rawls().replace(
                '\n', '').replace('\t', '')
            hdu.header['Sampler'] = self.details.sampler.to_rawls().replace(
                '\n', '').replace('\t', '')
            hdu.header['Accel'] = self.details.accelerator.to_rawls().replace(
                '\n', '').replace('\t', '')
            hdu.header['Inte'] = self.details.integrator.to_rawls().replace(
                '\n', '').replace('\t', '')
            hdu.header['Camera'] = self.details.camera.to_rawls().replace(
                '\n', '').replace('\t', '')
            hdu.header['LookAt'] = self.details.lookAt.to_rawls().replace(
                '\n', '').replace('\t', '')

            # save additionnals comments data
            additionals = ""
            for key, value in self.details.additionals.items():
                additionals += key + ' ' + value + "#"

            hdu.header['Extra'] = additionals[:-1]

            hdu.writeto(outfile, overwrite=True)

    def __clamp(self, n, smallest, largest):
        """Clamp number using two numbers
        
        Arguments:
            n: {float} -- the number to clamp
            smallest: {float} -- the smallest number interval
            largest: {float} -- the larget number interval
        
        Returns:
            {float} -- the clamped value

        Example:

        >>> from rawls.rawls import Rawls
        >>> path = 'images/example_1.rawls'
        >>> rawls_img = Rawls.load(path)
        >>> rawls_img._Rawls__clamp(300, 0, 255)
        255
        >>> rawls_img._Rawls__clamp(200, 0, 255)
        200
        """
        return max(smallest, min(n, largest))

    def __gamma_correct(self, value):
        """Correct gamma of luminance value
        
        Arguments:
            value: {float} -- luminance value to correct
        
        Returns:
            {float} -- correct value with specific gamma

        Example:

        >>> from rawls.rawls import Rawls
        >>> path = 'images/example_1.rawls'
        >>> rawls_img = Rawls.load(path)
        >>> rawls_img._Rawls__gamma_correct(0.80)
        0.9063317533440594
        >>> rawls_img._Rawls__gamma_correct(0.55)
        0.7673756580558262
        """
        if value <= 0.0031308:
            return 12.92 * value
        else:
            return 1.055 * math.pow(value, float(1. / 2.4)) - 0.055

    def __gamma_convert(self, value):
        """Correct gamma value and clamp it
        
        Arguments:
            value: {float} -- luminance value to correct and clamp
        
        Returns:
            {float} -- final chanel value
        """
        return self.__clamp(255. * self.__gamma_correct(value) + 0., 0., 255.)

    def gammaConvert(self):
        """Convert gamma of luminance chanel values of rawls image
        
        Returns:
            {ndarray} -- image buffer with converted gamma values
        """

        if not self.gamma_converted:
            height, width, chanels = self.shape

            for y in range(height):
                for x in range(width):
                    for c in range(chanels):
                        self.data[y][x][c] = self.__gamma_convert(
                            self.data[y][x][c])

            self.gamma_converted = True

    def add_comment(self, key, value):
        """Add additionals comments into `.rawls` file

        Args:
            key: {str} -- expected key
            value: {str} -- expected key value for this key

        Raises:
            Exception: key already exists into additionnals details
        """
        # check if key does not already exist
        if key not in self.details.additionals:
            self.details.additionals[key] = value
        else:
            raise Exception(
                '`{}` key already exists into additionnals details'.format(
                    key))

    def del_comment(self, key):
        """Delete additionals comments into `.rawls` file

        Args:
            key: {str} -- expected key

        Raises:
            Exception: key not exists into additionnals details
        """
        # check if key does not already exist
        if key in self.details.additionals:
            del self.details.additionals[key]
        else:
            raise Exception(
                '`{}` key not exists into additionnals details'.format(key))

    def to_pil(self, gamma_convert=True):
        """Convert current rawls image into PIL RGB Image
        
        Arguments:
            gamma_convert: {bool} -- necessary or not to convert using gamma (default: True)

        Returns:
            {PIL} -- RGB image converted
        
        Example:

        >>> import numpy as np
        >>> from rawls.rawls import Rawls
        >>> path = 'images/example_1.rawls'
        >>> rawls_img = Rawls.load(path)
        >>> rawls_pil_img = rawls_img.to_pil()
        >>> np.array(rawls_pil_img).shape
        (133, 300, 3)
        """
        if gamma_convert:
            self.gammaConvert()  # convert image to gamma if necessary

        # prepare input data
        input_data = np.array(self.data, 'uint8')

        # check if only one channel
        if self.data.ndim == 3:
            h, w, c = self.shape

            if c == 1:
                input_data = input_data.reshape(h, w)

        return Image.fromarray(input_data)

    def to_png(self, outfile, gamma_convert=True):
        """Save rawls image into PNG
        
        Arguments:
            outfile: {str} -- PNG output filename
            gamma_convert: {bool} -- necessary or not to convert using gamma (default: True)
        """

        if '/' in outfile:

            output_path, _ = os.path.split(outfile)

            if not os.path.exists(output_path):
                os.makedirs(output_path)

        if '.png' not in outfile:
            raise Exception('output filename is not `.png` format')

        self.to_pil(gamma_convert).save(outfile)

    def h_flip(self):
        """Flip horizontally current Rawls instance 
        """
        self.data = np.flip(self.data, axis=1)

    def v_flip(self):
        """Flip vectically current Rawls instance 
        """
        self.data = np.flip(self.data, axis=0)

    def copy(self):
        """Copy current Rawls instance
        
        Returns:
            {Rawls} -- Rawls copy of current instance
        """
        return copy.deepcopy(self)

    def normalize(self, max_value=None):
        """Give new Rawls instance with normalized data
        
        Arguments:
            max_value {float} -- max expected value for normalization (default: {max data value})
        
        Returns:
            {Rawls} -- Rawls instance with normalized data
        """
        min_value = np.min(self.data)

        normalized_data = self.data
        # check negative values
        if min_value < 0:
            normalized_data = self.data + abs(min_value)

        # default max value
        if max_value is None:
            max_value = np.max(normalized_data)

        normalized_data /= max_value

        return Rawls(normalized_data.shape, normalized_data, self.details,
                     self.gamma_converted)

    def __str__(self):
        """Display Rawls information
        
        Returns:
            {str} Rawls information
        """

        additionals_comments = ''

        # add additionnals comments
        for key, value in self.details.additionals.items():
            additionals_comments += '\n\t{0}: {1}'.format(key, value)

        return "--------------------------------------------------------\nShape: \n\t{0}\nDetails: \n{1}\nAdditionnals:{2}\nGamma converted: \n\t{3}\n--------------------------------------------------------".format(
            self.shape, self.details, additionals_comments,
            self.gamma_converted)


class RawlsSamples(Rawls):
    """RawlsSamples class used to open `.rawls` path image of only 1 sample with its sample coord

    Attributes:
        shape: {(int, int, int)} -- describe shape of the image
        data: {ndarray} -- buffer data numpy array
        samples: {ndarray} -- buffer with samples coord
        details: {Details} -- details instance information
        gamma_converted: {Details} -- specify if Rawls instance is gamma converted or not
    """
    def __init__(self, shape, data, samples, details, gamma_converted=False):
        """RawlsSamples constructor

        Attributes:
            shape: {(int, int, int)} -- describe shape of the image
            data: {ndrray} -- buffer data numpy array
            samples: {ndarray} -- buffer with samples coord
            details: {Details} -- details instance information
            gamma_converted: {Details} -- specify if Rawls instance is gamma converted or not
        """

        super().__init__(shape, data, details, gamma_converted)
        self.samples = samples

    @classmethod
    def load(self, filepath):
        """Open data of rawls file
        
        Arguments:
            filepath: {str} -- path of the .rawls or .fits file to open

        Returns:
            {RawlsSamples} : RawlsSamples instance
        """

        extension = filepath.split('.')[-1]

        if extension not in ['rawls']:
            raise Exception('filepath used is not valid')

        if '.rawls' in filepath:
            f = open(filepath, "rb")

            # finding data into files
            ihdr_line = 'IHDR'
            ihdr_found = False

            comments_line = 'COMMENTS'
            comments_found = False

            data_line = 'DATA'
            data_found = False

            samples_line = 'COORDS'
            samples_found = False

            # prepare rawls object data
            img_chanels = None
            img_width = None
            img_height = None

            comments = ""
            data = None

            # read first line
            line = f.readline()
            line = line.decode('utf-8')

            while not ihdr_found:

                if ihdr_line in line:
                    ihdr_found = True

                    # read shape info line
                    shape_size = int(f.readline().replace(b'\n', b''))

                    values = f.read(shape_size)
                    f.read(1)

                    img_width, img_height, img_chanels = struct.unpack(
                        'III', values)

            line = f.readline()
            line = line.decode('utf-8')

            while not comments_found:

                if comments_line in line:
                    comments_found = True

            # get comments information
            while not data_found:

                line = f.readline()
                line = line.decode('utf-8')

                if data_line in line:
                    data_found = True
                else:
                    comments += line

            # default read data size
            line = f.readline()

            buffer = b''
            # read buffer image data (here samples)
            for _ in range(img_height):

                line = f.read(4 * img_chanels * img_width)
                buffer += line

                # skip new line char
                f.read(1)

            # build numpy array from
            data = np.array(
                np.ndarray(shape=(img_height, img_width, img_chanels),
                           dtype='float32',
                           buffer=buffer))

            # get samples information
            while not samples_found:

                line = f.readline()
                line = line.decode('utf-8')

                if samples_line in line:
                    samples_found = True

            # default read data size
            line = f.readline()

            samples_buffer = b''
            # read buffer image data (here samples)
            for _ in range(img_height):

                line = f.read(4 * 2 * img_width)
                samples_buffer += line

                # skip new line char
                f.read(1)

            # build numpy array from
            samples_data = np.array(
                np.ndarray(shape=(img_height, img_width, 2),
                           dtype='float32',
                           buffer=samples_buffer))

            f.close()

            #details = Details.fromcomments(comments)

            return RawlsSamples(data.shape, data, samples_data, None)
