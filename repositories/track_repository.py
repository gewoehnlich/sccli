from sqlalchemy.orm import Session, sessionmaker
from core.repository import Repository
from enums.track_access import TrackAccessEnum
from models.track import Track


class TrackRepository(Repository):
    session_factory: sessionmaker[Session]

    def __init__(
        self,
        session_factory: sessionmaker[Session],
    ) -> None:
        self.session_factory = session_factory

    def get(
        self,
    ) -> Track | None:
        with self.session_factory() as session:
            return session.get(Track, None)

    def create(
        self,
        access: TrackAccessEnum,
        artwork_url: str,
        comment_count: int,
        created_at: str,
        description: str,
        duration: int,
        favoritings_count: int,
        id: int,
        metadata_artist: str | None,
        permalink_url: str,
        playback_count: int,
        reposts_count: int,
        stream_url: str,
        title: str,
        uri: str,
        urn: str,
        user_favorite: bool,
        user_playback_count: int,
    ) -> Track:
        track = Track(
            access=access,
            artwork_url=artwork_url,
            comment_count=comment_count,
            created_at=created_at,
            description=description,
            duration=duration,
            favoritings_count=favoritings_count,
            id=id,
            metadata_artist=metadata_artist,
            permalink_url=permalink_url,
            playback_count=playback_count,
            reposts_count=reposts_count,
            stream_url=stream_url,
            title=title,
            uri=uri,
            urn=urn,
            user_favorite=user_favorite,
            user_playback_count=user_playback_count,
        )

        with self.session_factory() as session:
            session.add(instance=track)
            session.commit()

        return track

    def update(
        self,
        access: TrackAccessEnum,
        artwork_url: str,
        comment_count: int,
        created_at: str,
        description: str,
        duration: int,
        favoritings_count: int,
        id: int,
        metadata_artist: str | None,
        permalink_url: str,
        playback_count: int,
        reposts_count: int,
        stream_url: str,
        title: str,
        uri: str,
        urn: str,
        user_favorite: bool,
        user_playback_count: int,
    ) -> Track:
        with self.session_factory() as session:
            track = session.get(Track, id)

            if track is None:
                raise ValueError(f"Track {id} not found")

            track.access = access
            track.artwork_url = artwork_url
            track.comment_count = comment_count
            track.created_at = created_at
            track.description = description
            track.duration = duration
            track.favoritings_count = favoritings_count
            track.id = id
            track.metadata_artist = metadata_artist
            track.permalink_url = permalink_url
            track.playback_count = playback_count
            track.reposts_count = reposts_count
            track.stream_url = stream_url
            track.title = title
            track.uri = uri
            track.urn = urn
            track.user_favorite = user_favorite
            track.user_playback_count = user_playback_count

            session.commit()

        return track

    def delete(
        self,
        id: int,
    ) -> None:
        with self.session_factory() as session:
            track = session.get(Track, id)

            if track is None:
                raise ValueError("Account not found")

            session.delete(track)
            session.commit()
