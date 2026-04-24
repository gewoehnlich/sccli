from sqlalchemy.orm import Session, sessionmaker

from core.repository import Repository
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
        access: str,
        artwork_url: str,
        created_at: str,
        description: str,
        duration: int,
        id: int,
        permalink_url: str,
        title: str,
        uri: str,
        urn: str,
        user_favorite: bool,
        user_playback_count: int,
    ) -> Track:
        track = Track(
            access=access,
            artwork_url=artwork_url,
            created_at=created_at,
            description=description,
            duration=duration,
            id=id,
            permalink_url=permalink_url,
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
        access: str,
        artwork_url: str,
        created_at: str,
        description: str,
        duration: int,
        id: int,
        permalink_url: str,
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
            track.created_at = created_at
            track.description = description
            track.duration = duration
            track.id = id
            track.permalink_url = permalink_url
            track.title = title
            track.uri = uri
            track.urn = urn
            track.user_favorite = user_favorite
            track.user_playback_count = user_playback_count

            session.commit()

        return track

    def store(
        self,
        access: str,
        artwork_url: str,
        created_at: str,
        description: str,
        duration: int,
        id: int,
        permalink_url: str,
        title: str,
        uri: str,
        urn: str,
        user_favorite: bool,
        user_playback_count: int,
    ) -> Track:
        with self.session_factory() as session:
            track = session.get(Track, id)

        if track is None:
            track = self.create(
                access=access,
                artwork_url=artwork_url,
                created_at=created_at,
                description=description,
                duration=duration,
                id=id,
                permalink_url=permalink_url,
                title=title,
                uri=uri,
                urn=urn,
                user_favorite=user_favorite,
                user_playback_count=user_playback_count,
            )
        else:
            track = self.update(
                access=access,
                artwork_url=artwork_url,
                created_at=created_at,
                description=description,
                duration=duration,
                id=id,
                permalink_url=permalink_url,
                title=title,
                uri=uri,
                urn=urn,
                user_favorite=user_favorite,
                user_playback_count=user_playback_count,
            )

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
