from flask import Blueprint, request, jsonify, make_response,abort
from app import db
from app.models.board import Board
from app.routes.utility_file import validate_object, validate_field


boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

#tested and works
@boards_bp.route("", methods=['GET'])
def handle_all_boards():
    boards = request.args.get("board_id")
    boards_query = Board.query

    boards_response = []
    boards = boards_query.all()

    for board in boards:
        boards_response.append(board.to_dict())
    return jsonify(boards_response), 200 

#tested and works
@boards_bp.route("/<board_id>", methods=['GET'])
def handle_one_board(board_id):
    board = validate_object(Board, board_id)
    return jsonify({"board":board.to_dict()})

#tested and works
@boards_bp.route("", methods=['POST'])
def create_board():
    request_body = request.get_json()

    owner = request_body.get("owner")
    title = request_body.get("title")

    validate_field(owner, str)
    validate_field(title, str)
    
    try:
        new_board = Board.from_dict(request_body)
    except:
        print("hit the break")
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
def delete_one_board(board_id):

    board = validate_object(Board,board_id)
    db.session.delete(board)
    db.session.commit()

    return jsonify({"details":f"Board {board_id} successfully deleted"}), 200


#tested and works
#update path ex boards/2/owner will update owner, field is object key  
@boards_bp.route("/<board_id>/<field>", methods=["PUT"])
def update_board(board_id,field):

    board = validate_object(Board,board_id)
    field = request.path.split("/")[-1] 
    request_body = request.get_json()

    if field == "owner":
        board.owner = request_body["owner"]
        validate_field(board.owner, str)
        
    elif field == "title" :
        board.title = request_body["title"]
        validate_field(board.title, str)
        
    else:
        abort(make_response({"error": "Invalid field specified"}, 400))

    db.session.commit()

    return jsonify({"board":board.to_dict()}),200