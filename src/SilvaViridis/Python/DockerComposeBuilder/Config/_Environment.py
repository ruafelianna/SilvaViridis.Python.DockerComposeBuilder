from os import getenv

class PathsConfig:
    @staticmethod
    def BaseDataFolder() -> str:
        return getenv("DCG_BASE_DATA_FOLDER", "data")

    @staticmethod
    def YmlOutputFolder() -> str:
        return getenv("DCG_YML_OUTPUT_FOLDER", "compose")

class NetworkConfig:
    @staticmethod
    def BaseDomainName() -> str:
        return getenv("DCG_BASE_DOMAIN_NAME", "example.com")
