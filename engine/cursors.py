from engine import assets


class GameCursors:
    def __init__(self):
        self.cursors = {
            "arrow": (assets.load_image("resources/cursors/arrow.png"), -1, -1),
            "aim": (assets.load_image("resources/cursors/aim.png"), -16, -16),
        }

    def get(self, cursor: str):
        # check params type
        if type(cursor) is not str:
            raise TypeError("'cursor' has to be string")

        return self.cursors[cursor]
