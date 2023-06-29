from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.routes.utility_file import validate_object

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=['GET'])
def handle_all_boards():
    boards_response = []
    boards = Board.query.all()
    for board in boards:
        boards_response.append({
            "board_id": board.board_id,
            "title": board.title,
            "owner": board.owner
        })
    return jsonify(boards_response), 200 

@boards_bp.route("/<board_id>", methods=['GET'])
def handle_one_board(board_id):
    board = validate_object(Board, board_id)
    return {
        "board_id": board.board_id,
        "title": board.title,
        "owner": board.owner
    }, 200

@boards_bp.route("", methods=['POST'])
def create_board():
    request_body = request.get_json()

    if 'title' not in request_body or 'owner' not in request_body:
        return {"error": "Must provide title and owner"}, 400
    
    if not isinstance(request_body["title"],str) or not isinstance(request_body["owner"],str):
            return {"error": "Invalid input. Must provide text not numbers"}, 400

    new_board = Board(title=request_body['title'], owner=request_body['owner'])

    db.session.add(new_board)
    db.session.commit()

    return {
        "board_id": new_board.board_id,
        "title": new_board.title,
        "owner": new_board.owner
    }, 201

#Path to retrieve all cards from selected board 
@boards_bp.route("/<board_id>/cards", methods=['GET'])
def get_all_card_of_one_board(board_id):
    board = validate_object(Board, board_id)

    cards_response = []
    for card in board.cards:
        cards_response.append({
            "card_id": card.card_id,
            "message": card.message,
            "likes_count": card.likes_count,
            "board_id": card.board_id
        })
    
    return jsonify(cards_response), 200

@boards_bp.route("/<board_id>",methods=["DELETE"])
def delete_one_card(board_id):

    board = validate_object(Board,board_id)
    db.session.delete(board)
    db.session.commit()

    return jsonify({"details":f"Board {board_id} successfully deleted"}), 200
    
