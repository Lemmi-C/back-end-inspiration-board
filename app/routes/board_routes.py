from flask import Blueprint, request, jsonify, make_response,abort
from app import db
from app.models.board import Board
from app.routes.utility_file import validate_object, validate_field_not_empty

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

#validation works and path tested
@boards_bp.route("", methods=['GET'])
def handle_all_boards():
    boards = request.args.get("board_id")
    boards_query = Board.query

    boards_response = []
    boards = boards_query.all()

    for board in boards:
        boards_response.append(board.to_dict())
    return jsonify(boards_response), 200 

#validation works, tested path
@boards_bp.route("/<board_id>", methods=['GET'])
def handle_one_board(board_id):
    board = validate_object(Board, board_id)
    return jsonify({"board":board.to_dict()})

#validation works/ tested and paths work
@boards_bp.route("", methods=['POST'])
def create_board():
    request_body = request.get_json()

    title = request_body.get("title")
    owner = request_body.get("owner")
    validate_field_not_empty("title", title)
    validate_field_not_empty("owner", owner)

    try:
        new_board = Board.from_dict(request_body)
    except:
        abort(make_response({"details": "Invalid data"},400))

    db.session.add(new_board)
    db.session.commit()

    response_body = {"board":new_board.to_dict()}

    return jsonify(response_body),201
    

#tested and works 
@boards_bp.route("/<board_id>/cards", methods=['GET'])
def get_all_card_of_one_board(board_id):
    board = validate_object(Board, board_id)
    
    cards_response = []
    if board:
        cards_response = [card.to_dict() for card in board.cards]
    
    return jsonify(cards_response), 200

#tested and works
@boards_bp.route("/<board_id>",methods=["DELETE"])
def delete_one_card(board_id):

    board = validate_object(Board,board_id)
    db.session.delete(board)
    db.session.commit()

    return jsonify({"details":f"Board {board_id} successfully deleted"}), 200
    
