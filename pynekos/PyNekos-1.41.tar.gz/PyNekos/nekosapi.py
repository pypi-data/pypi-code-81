import requests
import json
import os
from bs4 import BeautifulSoup


class NekoException(Exception):
    """ Base exception class for nekosapi.py. """
    pass


class MissedCredentials(NekoException):
    """ Credentials error. No credentials provided. """
    pass


class LoginError(NekoException):
    """ Login error. Impossible to login, credentials wrong. """
    pass


class MissingToken(NekoException):
    """ Token error. No toking provided. """
    pass


class TokenError(NekoException):
    """ Token error. Invalid token. """
    pass


class ImageError(NekoException):
    """ Image error. The image doesn't exist. """
    pass


class TypoError(NekoException):
    """ Type error. The type doesn't exist. """
    pass


class ImageTypoError(NekoException):
    """ Image type error. Wrong extension for image. """
    pass


class MissingParameters(NekoException):
    """ Missing parameters error. Required parameters don't given. """
    pass


class InvalidValue(NekoException):
    """ Invalid value error. The value given is invalid. """
    pass


class UserError(NekoException):
    """ User error. The user doesn't exist. """
    pass


class FilesizeError(NekoException):
    """ Size error. The image is too big. """
    pass


class TagsizeError(NekoException):
    """ Size error. The tag is too big. """
    pass


class Neko:
    """
    User-level interface with the Nekos.moe API.
    ...

    Attributes
    ----------
    token : str
        token used to post images (default is None)
    username : str
        username of a valid account (default is None)
    password : str
        password of a valid account (default is None)

    Methods
    -------
    get_token()
        Prints the token of the user of the credentials provided.
    regen_token()
        Regenerates the token of the user of the credentials providen. Need to make another instance with the new to
        ken.
    get_image(image_id)
        Returns a json with data about the image with given id.
    random_image(**kwargs)
        Returns a json with data about random images given some parameters.
    search_image(**kwargs)
        Search for images given some parameters and return a json with data about them.
    get_link(image_id, down=False)
        It's a shortcut for the link of the image with the given ID. If the `down` param is set to True, downloads
        the image to the current directory.
    get_thumbnail(image_id, down=False)
        It's a shortcut for the link of the image thumbnail with the given ID. If the `down` param is set to True,
        downloads the image thumbnail to the current directory.
    _send_image(filename, filepath, endpoint, data, headers)
        Private method that make the request uploading the image to the site.
    upload_image(**kwargs)
        Uploads a local image, image from a danbooru post or image from a url to the site.
    get_user(user_id)
        Returns a json with data about a user with given id.
    search_user(cls, **kwargs)
        Search for users given some parameters and return a json with data about them.
    """
    def __init__(self, token=None, username=None, password=None):
        """
        Parameters
        ----------
        token : str, optional
            Token used to post images (default is None)
        username : str, optional
            Username of a valid account (default is None)
        password : str, optional
            Password of a valid account (default is None)
        """
        self.token = token
        self.username = username
        self.password = password
        self.URL_BASE_API = 'https://nekos.moe/api/v1'
        self.URL_BASE = 'https://nekos.moe'

    def get_token(self):
        """Prints the token of the user of the credentials provided.

        Returns
        -------
        json
            json containing the token.

        Raises
        ------
        MissedCredentials
            If no username or password passed in the instance.
        LoginError
            If can't login, incorrect credentials.
        """
        if self.username is None or self.password is None:
            raise MissedCredentials('No credentials providen.')

        payload = {"username": f"{self.username}", "password": f"{self.password}"}
        headers = {'content-type': 'application/json'}
        r = requests.post(f'{self.URL_BASE_API}/auth', data=json.dumps(payload), headers=headers)
        if r.status_code == 401:
            raise LoginError('Incorrect username or password.')
        return r.json()

    def regen_token(self):
        """Regenerates the token of the user of the credentials providen.

        Need to make another instance with the new token.

        Returns
        -------
        function
            function that returns the token.

        Raises
        ------
        MissingToken
            If no token provided in the instance.
        TokenError
            If token's wrong.
        """
        if self.token is None:
            raise MissingToken('No token provided.')

        print('Regenerating token...')
        r = requests.post(f'{self.URL_BASE_API}/auth/regen', headers={"Authorization": f"{self.token}"})
        if r.status_code == 401:
            raise TokenError('Invalid token.')
        print('Token regenerated!')
        if self.username and self.password:
            return self.get_token()

    @classmethod
    def get_image(cls, image_id):
        """Returns a json with data about the image with given id.

        Params
        ----------
        **image_id** : str - the id of the image

        Returns
        -------
        json
            json with data about the image.

        Raises
        ------
        ImageError
            If the image doesn't exist.
        """
        r = requests.get(f'https://nekos.moe/api/v1/images/{image_id}')  # Making the request
        if r.status_code == 404:
            raise ImageError('Image not found')
        img_json = r.json()
        img_json['image']['url'] = f'https://nekos.moe/image/{image_id}'  # Implementing the image url
        img_json['image']['thumbnail'] = f'https://nekos.moe/thumbnail/{image_id}'  # Implementing the thumbnail url
        return img_json

    @classmethod
    def random_image(cls, **kwargs):
        """Returns a json with data about random images given some parameters.

        Params
        ----------------
        **nsfw** : boolean (default is False)\n
        **count** : int : 1-100 (default is 1)

        Returns
        -------
        json
            json with data about a random image.

        Raises
        ------
        InvalidValue
            If the count param is above 100
        """
        _p = {'nsfw': False, 'count': 1}
        _p.update(**kwargs)

        if 0 <= _p["count"] >= 101:
            raise InvalidValue('The count value must be between 1 and 100')

        # Converting the boolean values to string to avoid query params problem.
        # See: https://reqbin.com/7p9kenci
        payload = {"nsfw": 'true' if _p['nsfw'] is True else 'false', "count": _p['count']}
        r = requests.get(f'https://nekos.moe/api/v1/random/image', params=payload)  # Making the request
        json_imgs = r.json()  # Creating the json
        for i in range(0, len(json_imgs["images"])):
            _id = json_imgs["images"][i]["id"]
            json_imgs["images"][i]['url'] = f'https://nekos.moe/image/{_id}'  # Implementing the image url
            json_imgs["images"][i]['thumbnail'] = f'https://nekos.moe/thumbnail/{_id}'  # Implementing the thumbnail url
        return json_imgs

    @classmethod
    def search_image(cls, **kwargs):
        """Search for images given some parameters and return a json with data about them.

        Params
        ----------------
        **id** : string (default is None)\n
        **nsfw** : boolean (default is False)\n
        **uploader** : string (default is None)\n
        **artist** : string (default is None)\n
        **tags** : list (default is None)\n
        **sort** : string (default is "newest") - avaible: `newest, likes, oldest, relevance`\n
        **posted_before** : string (default is None) - separated by . - YYYY.MM.DD\n
        **posted_after** : string (default is None) - separated by . - YYYY.MM.DD\n
        **skip** : int (default is 0)\n
        **limit** : int : 1-50 (default is 1)

        Returns
        -------
        json
            json with data about the images.

        Raises
        ------
        InvalidValue
            If the limit param is above 50
        """
        _p = {'nsfw': False, 'limit': 20, 'skip': 0, 'sort': 'newest'}
        _p.update(**kwargs)

        if _p['limit'] > 50:
            raise InvalidValue('The limit value must be at most 50')
        _p['nsfw'] = 'true' if _p['nsfw'] is True else 'false'  # Fixing problem with the boolean value

        r = requests.post(f'https://nekos.moe/api/v1/images/search', data=json.dumps(_p),
                          headers={'content-type': 'application/json'})  # Making the request
        json_imgs = r.json()  # Creating the json
        for i in range(0, len(json_imgs["images"])):
            _id = json_imgs["images"][i]["id"]
            json_imgs["images"][i]['url'] = f'https://nekos.moe/image/{_id}'  # Implementing the image url
            json_imgs["images"][i]['thumbnail'] = f'https://nekos.moe/thumbnail/{_id}'  # Implementing the thumbnail url
        return json_imgs

    @classmethod
    def get_link(cls, image_id, down=False):
        """It's a shortcut for the link of the image with the given ID.

        If the `down` param is set to True, downloads the image to the current directory.

        Params
        ----------------
        **image_id** : string (default is None)\n
        **down** : boolean : (default is False)

        Returns
        ----------------
        string
            the url of the image with the given ID. If `down` param set to True, returns the file downloaded.
        """
        if down is False:
            return f'https://nekos.moe/image/{image_id}'
        else:
            img = requests.get(f'https://nekos.moe/image/{image_id}')  # Making the request
            # Saving the image on the current directory
            with open(f'{os.getcwd()}/{image_id}.{img.headers["Content-Type"].split("/")[-1]}', 'wb') as f:
                f.write(img.content)
            return f'Downloaded {image_id}.{img.headers["Content-Type"].split("/")[-1]} successfully!'

    @classmethod
    def get_thumbnail(cls, image_id, down=False):
        """It's a shortcut for the link of the image thumbnail with the given ID.

        If the `down` param is set to True, downloads the image thumbnail to the current directory.

        Params
        ----------------
        **image_id** : string (default is None)\n
        **down** : boolean : (default is False)

        Returns
        ----------------
        string
            the url of the image thumbnail with the given ID. If `down` param set to True, returns the file downloaded.
        """
        if down is False:
            return f'https://nekos.moe/thumbnail/{image_id}'
        else:
            img = requests.get(f'https://nekos.moe/thumbnail/{image_id}')  # Making the request
            # Saving the image on the current directory
            with open(f'{os.getcwd()}/{image_id}.{img.headers["Content-Type"].split("/")[-1]}', 'wb') as f:
                f.write(img.content)
            return f'Downloaded {image_id}.{img.headers["Content-Type"].split("/")[-1]} successfully!'

    @staticmethod
    def _send_image(filename, filepath, endpoint, data, headers):
        """Private method that make the request uploading the image to the site.

        Params
        ----------------
        **filename** : string\n
        **filepath** : string\n
        **endpoint** : string\n
        **data** : dict\n
        **headers** : dict\n

        Returns
        ----------------
        json
            json with data about the upload.

        Raises
        ------
        TokenError
            If the token is wrong. Can't upload.
        """
        files = {"image": (filename, open(filepath, 'rb'), 'image/jpg', {'Expires': '0'})}
        r = requests.post(endpoint, data=data, headers=headers, files=files)
        if r.status_code == 401:
            raise TokenError('Invalid token.')
        json_img_post = json.loads(r.text)
        return json_img_post

    def upload_image(self, **kwargs):
        """Uploads a local image, image from a danbooru post or image from a url to the site.

        Params
        ----------------
        **image** : string - imagename.extension (local), id of post (danbooru), image url (url)\n
        image can be up to 3 MB and must be a png or jpg/jpeg file\n
        **upload_type** : string - `danbooru, local, url`\n
        **tags** : list\n
        tags can be up to 50 characters long and there can be up to 120 tags\n
        **nsfw** : boolean (default is False)\n
        **image_path** : path to the image - required *only* for **local** uploads.

        Returns
        ----------------
        function
            returns the function that makes the upload..

        Raises
        ------
        TokenError
            If the token is wrong. Can't upload.
        MissingParameters
            Some needed parameters is missing.
        TagsizeError
            If there's more than 120 tags or if any tag has more than 50 characters.
        ImageError
            Invalid URL or invalid danbooru ID, can't find the image.
        FilesizeError
            Image that have more than 3MB.
        ImageTypoError
            Image is not png or jpg/jpeg
        TypoError
            `upload_type` param wrong.
        """
        if self.token is None:
            raise TokenError('No token provided.')

        _p = {'artist': 'unknown', 'nsfw': False}
        _p.update(**kwargs)
        _p['nsfw'] = 'true' if _p['nsfw'] is True else ''  # Fixing problem with the boolean value

        # Verification for missing required parameters
        if not _p.get('image'):
            raise MissingParameters(f'Required parameters don\'t given: <image>')
        elif not _p.get('upload_type'):
            raise MissingParameters(f'Required parameters don\'t given: <upload_type>')
        elif _p.get('upload_type') != 'danbooru' and not _p.get('tags'):
            raise MissingParameters(f'Required parameters don\'t given: <tags>')
        elif _p.get('upload_type') == 'local' and not _p.get('image_path'):
            raise MissingParameters(f'Required parameters don\'t given: <image_path>')

        endpoint = f"{self.URL_BASE_API}/images"
        headers = {"Authorization": f'{self.token}'}

        # URL upload
        if _p['upload_type'] == 'url':
            # Checking the length of the tag list and length of characters of each tag
            for _ in _p['tags']:
                if len(_) > 50 or len(_p['tags']) > 120:
                    raise TagsizeError('Tags can be up to 50 characters long and there can be up to 120 tags')

            img = requests.get(_p['image'])  # Making the request
            if img.status_code in [400, 404, 403]:
                raise ImageError('Image not found - Invalid URL')
            # Saving the image
            with open(f'image.{img.headers["Content-Type"].split("/")[-1]}', 'wb') as f:
                f.write(img.content)

            # Checking the filesize and extension
            if os.stat(f'image.{img.headers["Content-Type"].split("/")[-1]}').st_size > 3145728:
                raise FilesizeError('The filesize must be at most 3MB')
            elif img.headers['Content-Type'] not in ['image/jpeg', 'image/jpg', 'image/png']:
                raise ImageTypoError('The image must be a png or jpg/jpeg file')

            # Uploading and removing the image
            try:
                a = self._send_image(f'image.{img.headers["Content-Type"].split("/")[-1]}',
                                     f'{os.getcwd()}/image.{img.headers["Content-Type"].split("/")[-1]}',
                                     endpoint, _p, headers)
            except Exception as e:
                print(f'Upload failed! Aborting... - {e}')
                os.remove(f'{os.getcwd()}/image.{img.headers["Content-Type"].split("/")[-1]}')
            else:
                os.remove(f'{os.getcwd()}/image.{img.headers["Content-Type"].split("/")[-1]}')
                return a

        # Local upload
        elif _p['upload_type'] == 'local':
            # Checking the length of the tag list and length of characters of each tag
            for _ in _p['tags']:
                if len(_) > 50 or len(_p['tags']) > 120:
                    raise TagsizeError('Tags can be up to 50 characters long and there can be up to 120 tags')

            return self._send_image(_p['image'], _p['image_path'], endpoint, _p, headers)

        # Danbooru upload
        elif _p['upload_type'] == 'danbooru':
            # Scraping informations of the danbooru posts (tags, artist, image url)
            r = requests.get(f'https://danbooru.donmai.us/posts/{_p["image"]}')  # Making the request of the post url
            if r.status_code != 200:
                raise ImageError('Image not found')
            soup = BeautifulSoup(r.content, 'html.parser')  # Creating the parser
            artist = soup.find('li', {'class': 'tag-type-1'}).get('data-tag-name')  # Finding the artist
            class_tags = soup.findAll('li', {'class': 'tag-type-0'})  # Finding the tags
            image_url = soup.find('img', {'id': 'image'}).get('src')  # Finding the image url
            img_tags = []
            for i in class_tags:
                img_tags.append(i.get('data-tag-name'))  # Appending the tags to the list of tags

            img = requests.get(image_url)  # Making the request of the image url
            # Saving the image
            with open(f'image.{img.headers["Content-Type"].split("/")[-1]}', 'wb') as f:
                f.write(img.content)

            # Checking the filesize and extension
            if os.stat(f'image.{img.headers["Content-Type"].split("/")[-1]}').st_size > 3145728:
                raise FilesizeError('The filesize must be at most 3MB')
            elif img.headers['Content-Type'] not in ['image/jpeg', 'image/jpg', 'image/png']:
                raise ImageTypoError('The image must be a png or jpg/jpeg file')

            _p["artist"] = artist
            _p["tags"] = img_tags if len(img_tags) < 120 else img_tags[:121]

            # Uploading and removing the image
            try:
                a = self._send_image(f'image.{img.headers["Content-Type"].split("/")[-1]}',
                                     f'{os.getcwd()}/image.{img.headers["Content-Type"].split("/")[-1]}',
                                     endpoint, _p, headers)
            except Exception as e:
                print(f'Upload failed! Aborting... - {e}')
                os.remove(f'{os.getcwd()}/image.{img.headers["Content-Type"].split("/")[-1]}')
            else:
                os.remove(f'{os.getcwd()}/image.{img.headers["Content-Type"].split("/")[-1]}')
                return a
        else:
            raise TypoError('Upload type unrecognized.')

    @classmethod
    def get_user(cls, user_id):
        """Returns a json with data about a user with given id.

        Params
        ----------------
        **user_id** : string\n

        Returns
        ----------------
        json
            json with data about the user.

        Raises
        ------
        UserError
            The user doesn't exist.
        """
        r = requests.get(f'https://nekos.moe/api/v1/user/{user_id}')
        if r.status_code == 404:
            raise UserError('No user with that id.')
        return r.json()

    @classmethod
    def search_user(cls, **kwargs):
        """Search for users given some parameters and return a json with data about them.

        Params
        ----------------
        **query** : string (default is None)\n
        **skip** : int (default is 0)\n
        **limit** : int : 0-100 (default is 20)

        Returns
        ----------------
        json
            json with data about the users.

        Raises
        ------
        InvalidValue
            If `limit` value is above 100.
        """
        _p = {'limit': 20, 'skip': 0}
        _p.update(**kwargs)

        if _p['limit'] > 100:
            raise InvalidValue('The limit value must be at most 100')

        r = requests.post(f'https://nekos.moe/api/v1/users/search', data=json.dumps(_p),
                          headers={'content-type': 'application/json'})
        return r.json()
