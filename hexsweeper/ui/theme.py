class Theme:
    def __init__(self, scale: float = 1.0):
        self.initial_scale = scale
        self.scale = scale
        self.background = (15, 15, 30)

        self.cover_outline = (255, 255, 255)
        self.cover_outline_width = 5
        self.cover_inner = (255, 180, 50)

        self.inner_outline = (170, 170, 170)
        self.inner_outline_width = 5
        self.inner = (140, 140, 140)

        self.shadow = (122, 90, 25)
        self.shadow_width = 10
        self.shadow_opacity: float = 0.5
