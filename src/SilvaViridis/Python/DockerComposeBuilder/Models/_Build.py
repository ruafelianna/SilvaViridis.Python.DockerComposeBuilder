from pydantic import BaseModel, ConfigDict, validate_call

from SilvaViridis.Python.Common.Text import NonEmptyString

from ..Common import ConfigurationDict

class Build(BaseModel):
    context : NonEmptyString
    dockerfile_inline : NonEmptyString

    model_config = ConfigDict(
        frozen = True,
    )

    @validate_call
    def get_full_build(
        self,
    ) -> ConfigurationDict:
        return {
            "context": self.context,
            "dockerfile_inline": self.dockerfile_inline,
        }

    def __repr__(
        self,
    ) -> str:
        return repr({
            "context": self.context,
            "dockerfile_inline" : self.dockerfile_inline,
        })
