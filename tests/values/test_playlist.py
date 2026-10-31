from unittest.mock import Mock

import pytest

import values.playlist as playlist_module
from exceptions.playlist_errors import (
    PlaylistEmptyError,
    PlaylistInvalidIndexError,
)
from models.track import Track
from values.playlist import Playlist


def make_tracks(count: int) -> tuple[Track, ...]:
    return tuple(Mock(spec=Track) for _ in range(count))


def test_empty_playlist_has_no_index() -> None:
    playlist = Playlist(tracks=())

    assert playlist.index is None
    assert len(playlist) == 0


def test_non_empty_playlist_defaults_to_first_track() -> None:
    playlist = Playlist(tracks=make_tracks(3))

    assert playlist.index == 0


def test_explicit_index_is_kept() -> None:
    playlist = Playlist(tracks=make_tracks(3), index=2)

    assert playlist.index == 2


@pytest.mark.parametrize("index", [-1, 3, 100])
def test_out_of_range_index_raises(index: int) -> None:
    with pytest.raises(PlaylistInvalidIndexError):
        Playlist(tracks=make_tracks(3), index=index)


def test_explicit_index_on_empty_playlist_raises() -> None:
    with pytest.raises(PlaylistInvalidIndexError):
        Playlist(tracks=(), index=0)


def test_current_is_none_for_empty_playlist() -> None:
    assert Playlist(tracks=()).current() is None


def test_current_returns_track_at_index() -> None:
    tracks = make_tracks(3)

    assert Playlist(tracks=tracks, index=1).current() is tracks[1]


def test_select_returns_track_and_updates_index() -> None:
    tracks = make_tracks(3)
    playlist = Playlist(tracks=tracks)

    result = playlist.select(2)

    assert result is tracks[2]
    assert playlist.index == 2
    assert playlist.current() is tracks[2]


@pytest.mark.parametrize("index", [-1, 3])
def test_select_invalid_index_raises_and_keeps_state(index: int) -> None:
    playlist = Playlist(tracks=make_tracks(3), index=1)

    with pytest.raises(PlaylistInvalidIndexError):
        playlist.select(index)

    assert playlist.index == 1


def test_select_on_empty_playlist_raises() -> None:
    with pytest.raises(PlaylistInvalidIndexError):
        Playlist(tracks=()).select(0)


def test_next_moves_forward_and_returns_the_new_track() -> None:
    tracks = make_tracks(3)
    playlist = Playlist(tracks=tracks)

    assert playlist.next() is tracks[1]
    assert playlist.index == 1
    assert playlist.next() is tracks[2]
    assert playlist.index == 2


def test_next_wraps_to_the_first_track() -> None:
    tracks = make_tracks(3)
    playlist = Playlist(tracks=tracks, index=2)

    assert playlist.next() is tracks[0]
    assert playlist.index == 0


def test_prev_moves_backward_and_returns_the_new_track() -> None:
    tracks = make_tracks(3)
    playlist = Playlist(tracks=tracks, index=2)

    assert playlist.prev() is tracks[1]
    assert playlist.index == 1


def test_prev_wraps_to_the_last_track() -> None:
    tracks = make_tracks(3)
    playlist = Playlist(tracks=tracks, index=0)

    assert playlist.prev() is tracks[2]
    assert playlist.index == 2


def test_next_and_prev_on_single_track_stay_on_it() -> None:
    tracks = make_tracks(1)
    playlist = Playlist(tracks=tracks)

    assert playlist.next() is tracks[0]
    assert playlist.prev() is tracks[0]
    assert playlist.index == 0


def test_next_then_prev_returns_to_the_start() -> None:
    tracks = make_tracks(4)
    playlist = Playlist(tracks=tracks, index=1)

    playlist.next()
    playlist.prev()

    assert playlist.index == 1


@pytest.mark.parametrize("method", ["next", "prev", "random"])
def test_navigation_on_empty_playlist_raises(method: str) -> None:
    playlist = Playlist(tracks=())

    with pytest.raises(PlaylistEmptyError):
        getattr(playlist, method)()


def test_random_on_single_track_returns_it() -> None:
    tracks = make_tracks(1)
    playlist = Playlist(tracks=tracks)

    assert playlist.random() is tracks[0]
    assert playlist.index == 0


def test_random_updates_current_track() -> None:
    playlist = Playlist(tracks=make_tracks(5))

    result = playlist.random()

    assert playlist.current() is result


def test_random_never_repeats_the_current_track() -> None:
    playlist = Playlist(tracks=make_tracks(3))

    previous = playlist.index
    for _ in range(300):
        playlist.random()
        assert playlist.index != previous
        previous = playlist.index


def test_random_can_reach_every_other_track() -> None:
    playlist = Playlist(tracks=make_tracks(4), index=0)
    seen: set[int | None] = set()

    for _ in range(200):
        playlist.select(0)
        playlist.random()
        seen.add(playlist.index)

    assert seen == {1, 2, 3}


@pytest.mark.parametrize(
    ("drawn", "expected_index"),
    [
        (0, 0),
        (1, 1),
        (2, 3),
    ],
)
def test_random_skips_the_current_index(
    monkeypatch: pytest.MonkeyPatch,
    drawn: int,
    expected_index: int,
) -> None:
    calls: list[int] = []

    def fake_randrange(stop: int) -> int:
        calls.append(stop)
        return drawn

    monkeypatch.setattr(playlist_module, "randrange", fake_randrange)
    playlist = Playlist(tracks=make_tracks(4), index=2)

    playlist.random()

    assert calls == [3]
    assert playlist.index == expected_index
