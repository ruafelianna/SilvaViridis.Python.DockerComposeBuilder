from os import getenv

class PathsConfig:
    BaseDataFolder : str = getenv("DCG_BASE_DATA_FOLDER", "data")
    YmlOutputFolder : str = getenv("DCG_YML_OUTPUT_FOLDER", "compose")

class NetworkConfig:
    BaseDomainName : str = getenv("DCG_BASE_DOMAIN_NAME", "example.com")
