# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_configuration_management']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.54.1,<2.0.0',
 'PyNaCl>=1.4.0,<2.0.0',
 'boto3>=1.17.27,<2.0.0',
 'cryptography>=3.3.1,<4.0.0',
 'django>=3.1.4,<4.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['generate_key = '
                     'django_configuration_management.cli:generate_key',
                     'github_secrets = '
                     'django_configuration_management.cli:github_secrets',
                     'iam_role = django_configuration_management.cli:iam_role',
                     'reencrypt = '
                     'django_configuration_management.cli:reencrypt',
                     'reveal_secrets = '
                     'django_configuration_management.cli:reveal_secrets',
                     'upsert_secret = '
                     'django_configuration_management.cli:upsert_secret']}

setup_kwargs = {
    'name': 'django-configuration-management',
    'version': '0.3.5',
    'description': 'A merge conflict-less solution to committing an encrypted configuration to the repo with secrets and non-secrets side-by-side.',
    'long_description': '# Quick start\n\nThis package features an opinionated configuration management system, focused on combining both secret\nand non-secret keys in the same configuration file. The values for secret keys are encrypted and can\nbe committed to the repo, but since each key is separated on a line-by-line basis, merge conflicts\nshouldn\'t cause much trouble.\n\nThis package is intended to be used with a django project, though it\'s currently not making use\nof any Django specific features.\n\nNeedless to say, this is in very early development.\n\n## Install\n\n`pip install django-configuration-management`\n\n## cli\n\n### Generate a key\n\nIn a terminal, enter:\n\n```bash\ngenerate_key\n```\n\nFollow the instructions printed to the console. For example, if you\'re setting up a production configuration,\nmake a file called `.env-production` in the root of your django project. Inside of it, save the key generated\nabove to a variable called `ENC_KEY`.\n\n### Upsert a secret\n\nTo insert or update a secret, enter:\n\n```bash\nupsert_secret --environment <your environment>\n```\n\nAnd follow the prompts.\n\n### Insert a non-secret\n\nSimply open the .yml file for the generated stage (the naming scheme is `config-<environment>.yaml`),\nand insert a row. It should look like this:\n\n```yaml\nUSERNAME: whatsup1994 # non-secret\nPASSWORD:\n  secret: true\n  value: gAAAAABf2_kxEgWXQzJ0SlRmDy6lbXe-d3dWD68W4aM26yiA0EO2_4pA5FhV96uMWCLwpt7N6Y32zXQq-gTJ3sREbh1GOvNh5Q==\n```\n\n### Insert an AWS Secret Manager secret\n\nAdd a row where the key name is your secret name in AWS Secret Manager, with a sub-key value pair of\n`use_aws: true`. It should look like this:\n\n```yaml\nsecrets/integrations/aws_secret:\n  use_aws: true\n  secret_keys:\n    - AWS_SECRET\n```\n\nThe secret in your AWS instance will need to conform to the naming patterns used elsewhere in\nthis repo, e.g., a properly structured AWS Secret Manager secret will look like\n\n```json\n{\n  "AWS_SECRET": "I\'m a secret"\n}\n```\n\nThe keys of this object will be translated into python variables for the Django settings\nmodule in much the same way the keys of the local yaml will be, but you must explicitly\ncall out which keys you want to load by specifying the attribute `secret_keys`.\n\nYour AWS credentials must also be set up correctly to make API calls to AWS.\n\n### Manually editing the file\n\nYou can change the values of non-secrets by hand, as well as the keynames, but clearly you must\nnot change the value of secrets by hand, as they\'re encrypted. Changing the order of any of the\nkeys is perfectly fine.\n\n### Print secrets to the console\n\nTo show the decrypted values of all the secrets in the console, enter:\n\n```bash\nreveal_secrets --environment <your-environment>\n```\n\n### Re-encrypt a config file\n\nTo re-encrypt all secret values for a given environment\'s config file, pass\n\n```bash\nreencrypt --environment <your-environment> --new-key <your-new-key>\n```\n\nIf you do not provide a key, a new one will be generated for you.\n\n## Configuring repository secrets from cli using `github_secrets`\n\nTo set secrets on a remote repository:\n\n1. Create a `GITHUB_ACCESS_TOKEN` variable in your local shell environment.\n   This variable should contain your github personal access token\n   (https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).\n2. `cd` into the local repository that you would like to set secrets for.\n3. Create a new file named `config-github.json` and add a JSON object where each\n   key is the name of the secret you would like to add to the remote repository.\n   The value can be an empty string or a brief description about the key.\n   e.g.\n   ```json\n   {\n     "AWS_ACCESS_KEY_ID": "Description",\n     "AWS_SECRET_ACCESS_KEY": "Description"\n   }\n   ```\n4. Run `github_secrets` to start running the script.\n5. This will run the script and prompt you to enter a value for each secret key in\n   the `config-github.json` file.\n6. You can press `enter` to skip providing a value for any secret.\n7. Once you have either provided a value or skipped all secrets in the `config-github.json` file,\n   the script will push the secrets to the remote repository of the current working directory.\n\n## Extras\n\nIn the root of your django project, you can create a file called `config-required.json`.\n\nThe JSON object can be a list or a dictionary. This is useful for validating the presence of your\nkeys on start-up.\n\nValidating secrets that come from AWS Secret Manager is done implicitly since you must specify\na `secret_keys` attribute in your .yaml. This is needed so that only AWS secrets that are\nexplicitly called out are loaded into your Django settings/Python environment.\n\n## Settings\n\nThere are two ways to use this library, if you don\'t mind a little magic, you can\nsimply inject the config by importing the following function in your django settings file,\nand passing in the current module.\n\n```python\n# settings.py\nfrom django_configuration_management import inject_config\n\n# development is the environment name\ninject_config("development", sys.modules[__name__])\n```\n\nSee the example project for a demonstration of this.\n\nIf you want more verbosity, you can import the following function which will return\nthe config as a normalized dictionary that\'s flat and has all secrets decrypted.\n\n```python\n# settings.py\nfrom django_configuration_management import get_config\n\n# config = {"USERNAME": "helloworld", "PASSWORD": "im decrypted}\nconfig = get_config("development")\n\nUSERNAME = config["USERNAME"]\n# ...\n```\n\n### Using without a .env\n\nIf you want to skip using the .env, you can set the optional argument `dotenv_required` to `False`\nwhen invoking either of the above two methods. Doing so means it then becomes your responsibility\nto load an environment variable called `ENC_KEY` that stores the relevant encryption key for the\nstage you\'re trying to load.\n\n```python\n# settings.py\nfrom django_configuration_management import get_config\n\n# Will error out if you didn\'t load ENC_KEY correctly\nconfig = get_config("development", dotenv_required=False)\n```\n\n---\n\nThis project uses [poetry](https://python-poetry.org/) for dependency management\nand packaging.\n',
    'author': 'Alex Drozd',
    'author_email': 'drozdster@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brno32/django-configuration-management',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
