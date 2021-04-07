REQUIREMENTS_LIST = [
    'django',
    'pre-commit',
]


class requirements:
    '''
        Object used to handle the requirements list
    '''
    requirements_list = REQUIREMENTS_LIST

    @classmethod
    def get_requirements_as_string(cls):
        '''
            Return a string fitting the requirements.txt
        '''
        requirements = '# Run pip install -r requirements.txt\n'
        for requirement in cls.requirements_list:
            requirements += f'{requirement}\n'
        return requirements
