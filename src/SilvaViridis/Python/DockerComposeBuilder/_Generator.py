from pydantic import BaseModel, ConfigDict
from yaml import dump as to_yaml

from SilvaViridis.Python.Common.Text import NonEmptyString

from .Categories import Services

class Generator(BaseModel):
    services : Services

    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        frozen = True,
    )

    def generate(
        self,
        container_name : NonEmptyString,
    ) -> str:
        return to_yaml(self.services.get_full_services(container_name))
