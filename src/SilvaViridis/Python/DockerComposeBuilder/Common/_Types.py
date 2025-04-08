from __future__ import annotations

type Configuration = ConfigurationStr | ConfigurationDict | ConfigurationTuple[ConfigurationStr]

type ConfigurationStr = str

type ConfigurationDict = dict[str, Configuration | list[Configuration]]

type ConfigurationTuple[T : Configuration] = tuple[ConfigurationStr, T]
