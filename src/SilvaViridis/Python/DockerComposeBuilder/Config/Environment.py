from os import getenv

class NetworkConfig:
    BaseDomain : str = getenv("DCG_BASE_DOMAIN", "example.com")

class PathsConfig:
    BaseDataFolder : str = getenv("DCG_BASE_DATA_FOLDER", "data")
