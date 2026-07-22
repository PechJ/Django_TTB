from .gemeinden import GEMEINDEN
from .feuerwehren import FEUERWEHREN

def get_gemeinde(landkreis, kommune):
    return GEMEINDEN.get((landkreis, kommune))

def get_feuerwehr(name):
    return FEUERWEHREN.get(name)
