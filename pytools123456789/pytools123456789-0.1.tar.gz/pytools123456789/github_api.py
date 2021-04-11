import requests


def buscar_avatar(usuario):
    """
    Função para buscar avatar usuário Github
    :param usuario: str nome usuário
    :return: avatar usuário
    """
    url = f'https://api.github.com/users/{usuario}'

    resp = requests.get(url)
    return resp.json()['avatar_url']


if __name__ == "__main__":
    print(buscar_avatar('MarcosAntonioSoares'))
