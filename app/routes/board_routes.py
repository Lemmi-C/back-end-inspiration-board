from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=['GET'])
def handle_boards():
    boards_response = []
    boards = Board.query.all()
    for board in boards:
        boards_response.append({
            "board_id": board.board_id,
            "title": board.title,
            "owner": board.owner
        })
    return jsonify(boards_response)

@boards_bp.route("", methods=['POST'])
def create_board():
    request_body = request.get_json()

    if 'title' not in request_body or 'owner' not in request_body:
        return {"error": "Must provide title and owner"}

    new_board = Board(title=request_body['title'], owner=request_body['owner'])

    db.session.add(new_board)
    db.session.commit()

    return {
        "board_id": new_board.board_id,
        "title": new_board.title,
        "owner": new_board.owner
    }, 201

    