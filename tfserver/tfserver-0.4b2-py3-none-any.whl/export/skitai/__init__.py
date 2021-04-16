
def __setup__ (pref):
    import tfserver

    if "TF_MODELS" in pref.config:
        for alias, model in pref.config.TF_MODELS.items ():
            config = {}
            if isinstance (model, (list, tuple)):
                model, config = model
            tfserver.add_model (alias, model, **config)

    if "GPU_LIMIT" not in pref.config:	# Mb or None
        pref.config.GPU_LIMIT = 'growth'

    if "GPU_DEVICES" not in pref.config:
        pref.config.GPU_DEVICES = []

    assert pref.config.GPU_LIMIT == 'growth' or isinstance (pref.config.GPU_LIMIT, (int, float)), 'GPU_LIMIT should be growth or Memory Mbytes'
    assert isinstance (pref.config.GPU_DEVICES, (list, tuple)), 'GPU_DEVICES should be GPU index list'
