from .saberes import SaberesConfig, Saber, SaberesDataSet, \
    SaberesDataStore, Balaio, Mucua, Mocambo, Mocambola
from .sankofa import Sankofa

from pathlib import Path
from configparser import ConfigParser

import argparse, os

parser = argparse.ArgumentParser("criar_mucua")
parser.add_argument("--path", help="Caminho absoluto da pasta para os dados do Baobáxia", type=str)
parser.add_argument("--balaio", help="Nome do Balaio", type=str)
parser.add_argument("--mucua", help="Nome da Mucua local onde instalar o Baobáxia", type=str)
parser.add_argument("--mocambo", help="Nome do Mocambo de base dessa Mucua local", type=str)
parser.add_argument("--mocambola", help="Username para criar um Mocambola", type=str)
parser.add_argument("--email", help="Email do Mocambola", type=str)
parser.add_argument("--password", help="Password para o Mocambola", type=str)
parser.add_argument("--smid_len", help="Numero de carateres para os IDs", type=int)
parser.add_argument("--slug_name_len", help="Numero de carateres para os nomes abreviados", type=int)
parser.add_argument("--slug_smid_len", help="Numero de carateres para os IDs abreviados", type=int)
parser.add_argument("--slug_sep", help="Caracter separador para o identificativo", type=str)


args = parser.parse_args()


def install(*, path: str, balaio: str, mucua: str, mocambo: str, mocambola: str,
            email: str, password: str, smid_len: int, slug_name_len: int,
            slug_smid_len: int, slug_sep: str):
    """Instalador do Baobáxia

    :param path: Caminho absoluto da pasta para os dados do Baobáxia
    :type path: str
    :param balaio: Nome do Balaio
    :type balaio: str
    :param mucua: Nome da Mucua local onde instalar o Baobáxia
    :type mucua: str
    :param mocambo: Nome do Mocambo de base dessa Mucua local
    :type mocambo: str
    :param mocambola: Username para criar um Mocambola
    :type mocambola: str
    :param email: Email do Mocambola
    :type email: str
    :param password: Password para o Mocambola
    :type password: str
    :param smid_len: Numero de carateres para os IDs
    :type smid_len: int
    :param slug_name_len: Numero de carateres para os nomes abreviados
    :type slug_name_len: int
    :param slug_smid_len: Numero de carateres para os IDs abreviados
    :type slug_smid_len: int
    :param slug_sep: Caracter separador para o identificativo
    :type slug_sep: str

    """
    
    mocambola_criado = Mocambola(
        username = mocambola,
        email = email
    )
    
    data_path = Path(path)

    if data_path.is_absolute:
        config = SaberesConfig(
            data_path = data_path,
            balaio_local = balaio,
            mucua_local = mucua,
            smid_len = smid_len, 
            slug_name_len = slug_name_len,
            slug_smid_len = slug_smid_len,
            slug_sep = slug_sep
        )
        datastore = SaberesDataStore(config)
        dataset = datastore.create_dataset(
            mocambola=mocambola_criado,
            model=Balaio)
        balaio_saber = dataset.settle_saber(
            path=Path('.'),
            name=balaio,
            data=Balaio(),
            slug_dir=True)
        dataset.model = Mucua
        dataset.balaio = balaio_saber.slug
        mucua_saber = dataset.settle_saber(
            path=Path('.'),
            name=mucua,
            data=Mucua(),
            slug_dir=True)
        dataset.model = Mocambo
        dataset.mucua = mucua_saber.slug
        mocambo_saber = dataset.settle_saber(
            path=Path('.'),
            name=mocambo,
            data=Mocambo(),
            slug_dir=True)
        (config.data_path / balaio_saber.slug / \
         mucua_saber.slug / mocambo_saber.slug / 'mocambolas').mkdir()
        mocambola_saber = dataset.settle_saber(
            path=mocambo_saber.path / 'mocambolas',
            name=mocambola,
            data=mocambola_criado,
            slug_dir=True)

        Sankofa.create_balaio(balaio=balaio_saber.slug,
                              description=mucua_saber.slug,
                              config=config)
        
        Sankofa.add(saberes=[mucua_saber,
                             mocambo_saber,
                             mocambola_saber],
                    mocambola=mocambola_criado,
                    config=config)

    config_file = ConfigParser()
    
    config_file['default'] = {
        "data_path": path,
        "saber_file_ext": ".baobaxia",
        "balaio_local": balaio_saber.slug,
        "mucua_local": mucua_saber.slug,
        "smid_len": smid_len,
        "slug_smid_len": slug_smid_len,
        "slug_name_len": slug_name_len,
        "slug_sep": slug_sep
    }

    try:     
        with open(os.path.join(os.path.expanduser("~"), '.baobaxia.conf'), 'w') as writefile:
            config_file.write(writefile)
    except IOError:
        pass

def criar_mucua():
    install(**args.__dict__)


