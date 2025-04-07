from __future__ import annotations

type Configuration = ConfigurationStr | ConfigurationDict

type ConfigurationStr = str

type ConfigurationDict = dict[str, Configuration | list[Configuration]]
