from typing import Callable


type ConfigFileData = dict[str, str | None]
type ShellOutputMethod = Callable[[str], None]
