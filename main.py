from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from random import choice
from flask import jsonify


'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    cafes=db.session.execute(db.select(Cafe)).scalars().all()
    random_cafes=choice(cafes)
    return jsonify(cafes={
        "can_take_calls":random_cafes.can_take_calls,
        "coffee_price":random_cafes.coffee_price,
        "has_sockets":random_cafes.has_sockets,
        "has_toilet":random_cafes.has_toilet,
        "has_wifi":random_cafes.has_wifi,
        "id":random_cafes.id,
        "img_url":random_cafes.img_url,
        "location":random_cafes.location,
        "map_url":random_cafes.map_url,
        "name":random_cafes.name,
        "seats":random_cafes.seats,
    }        
    )

@app.route("/all")
def all_cafes():
    #Method-01
    allcafes_db=db.session.execute(db.select(Cafe)).scalars().all()
    
    all_cafes_list=[]
    for i in allcafes_db:
        all_cafes_list.append({
        "can_take_calls":i.can_take_calls,
        "coffee_price":i.coffee_price,
        "has_sockets":i.has_sockets,
        "has_toilet":i.has_toilet,
        "has_wifi":i.has_wifi,
        "id":i.id,
        "img_url":i.img_url,
        "location":i.location,
        "map_url":i.map_url,
        "name":i.name,
        "seats":i.seats,
            })
    return jsonify(cafes=all_cafes_list)
    


#Method-1
# @app.route("/search/loc=<loc>")
# def search_cafe(loc):
#     search_cafes=db.session.execute(db.select(Cafe).where(Cafe.location==loc)).scalars().all()
#     if search_cafes:
#         all_cafes_list=[]
#         for i in search_cafes:
#             all_cafes_list.append({
#             "can_take_calls":i.can_take_calls,
#             "coffee_price":i.coffee_price,
#             "has_sockets":i.has_sockets,
#             "has_toilet":i.has_toilet,
#             "has_wifi":i.has_wifi,
#             "id":i.id,
#             "img_url":i.img_url,
#             "location":i.location,
#             "map_url":i.map_url,
#             "name":i.name,
#             "seats":i.seats,
#                 })
#         return jsonify(cafes=all_cafes_list)
#     else:
#         return jsonify(error={'Not Found':"Sorry, we don't have a cafe at that location"})



@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    # Note, this may get more than one cafe per location
    all_cafes = result.scalars().all()
    if all_cafes:
        all_cafes_list=[]
        for i in all_cafes:
            all_cafes_list.append({
            "can_take_calls":i.can_take_calls,
            "coffee_price":i.coffee_price,
            "has_sockets":i.has_sockets,
            "has_toilet":i.has_toilet,
            "has_wifi":i.has_wifi,
            "id":i.id,
            "img_url":i.img_url,
            "location":i.location,
            "map_url":i.map_url,
            "name":i.name,
            "seats":i.seats,
                })
        return jsonify(cafes=all_cafes_list)
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})



@app.route("/add",methods=["POST"])
def add_cafe():
    # cafe_name=request.args.get("name")
    # cafe_map_url=request.args.get("map_url")
    new_cafe=Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"Sucess":f"Sucessfully Added the new Cafe!!!"})


# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<id>",methods=["PATCH"])
def update_price(id):
    cafe_id=id
    new_price=request.form.get("new_price")
    cafe_searched=db.get_or_404(Cafe,cafe_id)
    if cafe_searched:
        cafe_searched.price=new_price
        db.session.commit()
        return jsonify(response={"sucess":"Sucessfully updated the price"}),200
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}),404




# HTTP DELETE - Delete Record
API_KEY="ithuku-key-eh-theva_illa"
@app.route("/report-closed/<cafe_id>")
def delete_cafe(cafe_id):
    given_api_key=request.args.get("api-key")
    if given_api_key==API_KEY:
        searching_cafe=db.get_or_404(Cafe,cafe_id)
        if searching_cafe:
            # delete_cafe_=db.session.execute(db.select(Cafe).where(Cafe.id==cafe_id)).scalar()
            db.session.delete(searching_cafe)
            db.session.commit()
            return jsonify(Sucess="Deleted the Cafe"),200
        else:
            return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}),404

    else:
        return jsonify(error="Sorry, that's not allowed. Make sure you have the correct api_key."),403


if __name__ == '__main__':
    app.run(debug=True)






