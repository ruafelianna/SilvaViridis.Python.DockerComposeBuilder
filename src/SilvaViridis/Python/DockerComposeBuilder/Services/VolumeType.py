from enum import Enum

class VolumeType(Enum):
    volume = 0
    bind = 1
    tmpfs = 2
    npipe = 3
    cluster = 4
