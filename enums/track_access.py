import enum


class TrackAccess(enum.Enum):
    PLAYABLE = "playable"
    PREVIEW = "preview"
    BLOCKED = "blocked"
