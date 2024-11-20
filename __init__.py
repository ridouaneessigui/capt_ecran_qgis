def classFactory(iface):
    from .CaptureCartePlugin import CaptureCartePlugin  # Importez votre classe principale du plugin
    return CaptureCartePlugin(iface)
