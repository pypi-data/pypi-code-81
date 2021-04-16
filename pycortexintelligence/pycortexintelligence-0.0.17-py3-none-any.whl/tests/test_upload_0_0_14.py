from pycortexintelligence import functions as cortexfunctions

LOADMANAGER = 'https://api.cortex-intelligence.com'
username = input('Enter a username: ')
password = input('Enter a password: ')
plataform_url = input('Enter a plataform_url: ')
cubo_id = input('Enter the cube_id: ')


def test_send_example1():
    # Timeouts
    # You can set timeouts for the platform according to the size of the uploaded files
    # or use the default
    timeout = {
        'file': 300,
        'execution': 600,
    }

    # DataFormat are Optionally defined
    dafault_data_format = {
        "charset": "UTF-8",
        "quote": r"\"",
        "escape": r"\/\/",
        "delimiter": ",",
        "fileType": "CSV"
    }

    # Upload to Cortex
    response = cortexfunctions.upload_to_cortex(
        cubo_id=cubo_id,
        file_path='example_files/example1.csv',
        plataform_url=plataform_url,
        username=username,
        password=password,
        data_format=dafault_data_format,
        timeout=timeout,
        loadmanager=LOADMANAGER,
    )

    assert 1==1


