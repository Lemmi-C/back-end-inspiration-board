from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board
from app.routes.utility_file import validate_object, validate_field

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

#tested and works
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

#tested and works
@cards_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    card = validate_object(Card,card_id)
    
    return jsonify({"card":card.to_dict()})

#tested and works
@cards_bp.route("",methods=["POST"])
def create_one_card():
    request_body = request.get_json()

    board_id = request_body.get("board_id")
    validate_object(Board,board_id)

    message = request_body.get("message")
    validate_field(message, str)

    try:
        new_card = Card.from_dict(request_body)
    except:
        abort(make_response({"details": "Invalid data"},400))

    db.session.add(new_card)
    db.session.commit()

    response_body = {"card":new_card.to_dict()}

    return jsonify(response_body),201


#tested and works
@cards_bp.route("/<card_id>",methods=["DELETE"])
def delete_one_card(card_id):

    card = validate_object(Card,card_id)
    db.session.delete(card)
    db.session.commit()

    return jsonify({"details":f"Card {card_id} successfully deleted"}), 200

#tested and works
#update path ex cards/2/likes will update likes_count, field is object key  
@cards_bp.route("/<card_id>/<field>", methods=["PUT"])
def update_card(card_id,field):

    card = validate_object(Card,card_id)
    field = request.path.split("/")[-1] 
    request_body = request.get_json()

    if field == "likes":
        card.likes_count = request_body["likes_count"]
        validate_field(card.likes_count, int)
        
    elif field == "message" :
        card.message = request_body["message"]
        validate_field(card.message, str)
        
    else:
        abort(make_response({"error": "Invalid field specified"}, 400))

    db.session.commit()

    return jsonify({"card":card.to_dict()}),200
    

