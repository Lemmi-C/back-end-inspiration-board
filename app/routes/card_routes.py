from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.routes.utility_file import validate_object

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

@cards_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    card = validate_object(Card,card_id)
    return make_response(jsonify({"card":card.to_dict()}))

@cards_bp.route("",methods=["POST"])
def create_one_card():
    request_body = request.get_json()
    try:
        new_card = Card.from_dict(request_body)
    except:
        abort(make_response({"details": "Invalid data"},400))

    db.session.add(new_card)
    db.session.commit

    reponse_body = {"card":new_card.to_dict()}
    return jsonify(reponse_body,201)