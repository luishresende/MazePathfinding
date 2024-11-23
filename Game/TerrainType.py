class TerrainType:
    def __init__(self, name, default_coast, rgb_color, texture_image=None):
        self.name = name
        self.default_coast = default_coast
        self.rgb_color = rgb_color
        self.texture_image = texture_image