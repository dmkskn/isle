


class Movie:
    def __init__(self, tmdb_id=None, **kwargs):
        self.tmdb_id = tmdb_id or kwargs["id"]
        for key in kwargs.keys() - {"id"}:
            setattr(self, key, kwargs[key])



