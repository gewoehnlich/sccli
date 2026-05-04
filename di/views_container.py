from views.track_view import TrackView


class ViewsContainer:
    track = TrackView(
        fields=['id', 'title', 'duration']
    )
