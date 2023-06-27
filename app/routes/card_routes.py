from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card


cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

@cards_bp.route("", methods=["GET"])
def get_all_cards():
    card = request.args.get("card_id")
    cards_query = Card.query
    #GET BY FILTER
    #if id:
        #cards = cards_query.filterby(card)
    #else:
    cards = cards_query.all()

    card_response = []
    for card in cards:
        card_response.append(card.to_dict())
    return jsonify(card_response)