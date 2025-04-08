from os.path import join as join_path
from pydantic import BaseModel, ConfigDict
from yaml import dump as to_yaml

from ._Container import Container
from .Config import PathsConfig

class Generator(BaseModel):
    containers : set[Container]

    model_config = ConfigDict(
        frozen = True,
    )

    def generate(
        self,
    ) -> None:
        files = {c.container_name: to_yaml(c.get_full_container()) for c in self.containers}
        for cname, file in files.items():
            with open(join_path(PathsConfig.YmlOutputFolder, f"{cname}.yml"), "w") as fd:
                fd.write(file)
