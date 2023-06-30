from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)

    cards = db.relationship("Card", back_populates="board")

    def to_dict(self):
        board_as_dict = {}
        board_as_dict["id"] = self.board_id
        board_as_dict["title"] = self.title
        board_as_dict["owner"] = self.owner
        # if we want cards to be grabbed by the get path boards/board_id we can implement below
        # if self.cards: 
        #board_as_dict["cards"] = [card.to_dict() for card in self.cards]
        return board_as_dict


    @classmethod
    def from_dict(cls, board_data):
        new_board = Board(title=board_data["title"],
                        board_id=board_data["board_id"])
        return new_board
        
        #no missing title or owner