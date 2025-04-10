from os import getenv

class PathsConfig:
    @staticmethod
    def BaseDataFolder() -> str:
        return getenv("DCG_BASE_DATA_FOLDER", "data")
