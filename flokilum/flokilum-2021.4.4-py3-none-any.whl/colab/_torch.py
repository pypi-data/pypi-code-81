def torch(version = "1.8.1+cu111"):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from torch import __version__ as INFO
        if INFO != version:
            command(F"pip install torch=={version} -f https://download.pytorch.org/whl/torch_stable.html")
    except:
        command(F"pip install torch=={version} -f https://download.pytorch.org/whl/torch_stable.html")
        from torch import __version__ as INFO

    # try:
    #     from torch import __version__ as INFO
    #     if parse(INFO) < parse(version):
    #         command("pip install --upgrade torch")
    # except:
    #     command("pip install --upgrade torch")
    #     from torch import __version__ as INFO

    import torch
    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    print(F"{'torch, device'.rjust(50)} : {INFO}, {device}")

    return import_module("torch"), device
