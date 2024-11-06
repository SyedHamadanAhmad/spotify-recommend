class Track:
    def __init__(self, acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence, tempo, key, mode):
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.speechiness = speechiness
        self.valence = valence
        self.tempo = tempo
        self.key = key
        self.mode = mode
    def __repr__(self):
        return (f"TrackFeatures(danceability={self.danceability}, energy={self.energy}, "
                f"instrumentalness={self.instrumentalness}, liveness={self.liveness}, "
                f"speechiness={self.speechiness}, valence={self.valence}, "
                f"tempo={self.tempo}, key={self.key}, mode={self.mode})")

