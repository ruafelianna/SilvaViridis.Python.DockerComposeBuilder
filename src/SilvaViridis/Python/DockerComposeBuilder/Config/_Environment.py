from os import getenv

class PathsConfig:
    BaseDataFolder : str = getenv("DCG_BASE_DATA_FOLDER", "data")
