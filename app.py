from flask import Flask, render_template, request, session, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

def clear_table(table):
    db.session.query(table).delete()
    db.session.commit()
app=Flask(__name__)

app.secret_key="penelope"

db_host = "my-map-db.c1koo6aek7nd.us-east-2.rds.amazonaws.com" 
db_name = "postgres"
db_user = "postgres"
db_pass = "110Pauldrive!"
db_port = 5432

DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

db = SQLAlchemy(app)


class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Boolean, default=False)
    def __init__(self, active=False):
        self.active=active

class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    lat = db.Column(db.Numeric(10, 7), nullable=True)
    long = db.Column(db.Numeric(10, 7), nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=True)
    role = db.Column(db.String, nullable=True)
    team = db.Column(db.String, nullable=True)
    host = db.Column(db.Boolean, nullable=True)
    
    
    def __init__(self, name, game_id, lat=None, long=None, role=None, team=None, host=False):
        self.name = name
        self.game_id = game_id
        self.lat = lat
        self.long = long
        self.role = role
        self.team = team
        self.host = host



    
engine = create_engine(DATABASE_URL)

def reset_db():
    
    db.drop_all()
    db.create_all()
    print("database wiped")



@app.route("/")
def index():

    return render_template("index.html")

@app.route("/create")
def create_game():
    return render_template("create_game.html")

@app.route("/join")
def join_game():
    
    return render_template("join_game.html")

@app.route("/update_lobby", methods=["POST"])
def update_lobby():
    game_code = request.get_json()
    game_id=game_code['game_id']
    lobby_list = Player.query.filter_by(game_id=game_id).all()
    return_list = []
    is_host = False
    for i in lobby_list:
        return_list.append(i.name)
        if i.host==True:
            is_host = True
    if is_host == False and len(lobby_list)>0:
        lobby_list[0].host = True
        db.session.commit()


    return jsonify(return_list)

@app.route("/lobby", methods=["POST", "GET"])
def lobby():
    print(request.method)
    if request.method == "GET":
        return "<p>Hello<p>"
    if "create" in request.form:
        game = Game()
        db.session.add(game)
        db.session.commit()
        game_id = game.id
        name = request.form['name']
        player = Player(name, game_id, host=True)
        db.session.add(player)
        db.session.commit()

        session['player_id'] = player.id

      

    if "join" in request.form:
        game_id = request.form["join"]
        games = Game.query.filter_by(id=game_id).all()
        if len(games)==1:
            name = request.form["name"]
            player = Player(name, game_id)
            db.session.add(player)
            db.session.commit()

            session['player_id'] = player.id

        else:
            return render_template("join_game.html")
            
    
    lobby_list = Player.query.filter_by(game_id=game_id).all()
    for i in lobby_list:
        if i.host == True:
            player_host = i.name

    return render_template("lobby.html", name=name, game_id=game_id, player_host=player_host)

@app.route('/game', methods=["POST", "GET"])
def game():
    player_id = session.get("player_id")
    if player_id is None:
        return redirect("/")
    if request.method == 'POST':
        player_id = session['player_id']
        player = Player.query.filter_by(id=player_id).all()[0]
        role = request.form['role']
        team = request.form['team']
        game_id = player.game_id
    if request.method == "GET":
        player_id = session['player_id']
        player = Player.query.filter_by(id=player_id).all()[0]
        role = player.role
        team = player.team
        game_id = player.game_id

    if player.role==None:
        
        player.role = role
        player.team = team
        db.session.commit()
        
    if team == "Team 1":
        if role == "Hostage":
            return render_template("team_1_hostage.html", game_id=game_id)
        if role == "Searcher":
            return render_template("team_1_searcher.html", game_id=game_id) 
    
    if team == "Team 2":
        if role == "Hostage":
            return render_template("team_2_hostage.html", game_id=game_id)
        if role == "Searcher":
            return render_template("team_2_searcher.html", game_id=game_id) 
        
    return render_template("index.html")

@app.route('/update_location', methods=["POST"])
def update_location():
    data = request.get_json()
    lat = data["lat"]
    longitude = data["long"]
    game_id = data["game_id"]
    lobby_list = Player.query.filter_by(game_id=game_id).all()
    all_locations = []
    player_id = session["player_id"]
    player = Player.query.get(player_id)
    player.lat = lat
    player.long= longitude
    db.session.commit()

    for i in lobby_list:
        all_locations.append([i.name, i.team, i.id, i.role, i.lat, i.long])

    send_locations = []
    if player.team == "Team 1":
        for i in lobby_list:
            if i.team == "Team 2":
                send_locations.append([i.name, i.team, i.id, i.role, i.lat, i.long])
    if player.team == "Team 2":
        for i in lobby_list:
            if i.team == "Team 1":
                send_locations.append([i.name, i.team, i.id, i.role, i.lat, i.long])
    
    return send_locations

@app.route('/testing')
def testing():
    return render_template("team_2_hostage.html")
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    