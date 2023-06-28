from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)


def to_dict(self):
    card_as_dict = {}
    card_as_dict["id"] = self.card_id
    card_as_dict["message"] = self.message
    card_as_dict["likes_count"] = self.likes_count
    return card_as_dict

@classmethod
def from_dict(cls, card_data):
    new_card = Card(card_id=card_data["card_id"],
                    message=card_data["message"])
    return new_card
    