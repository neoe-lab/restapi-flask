from flask import Flask, jsonify, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Myapp(db.Model):
    order_id = db.Column(db.Integer,primary_key = True)
    size = db.Column(db.String(500))
    topping = db.Column(db.String(500))
    crust = db.Column(db.String(500))

class MyAppSchema(ma.Schema):
    class Meta:
        fields = ('order_id','size','topping','crust')

my_app_schema = MyAppSchema(many=True)

@app.route('/')
def about():
    return 'about'

@app.route('/orders')
def get_order():
    entries = Myapp.query.all()
    result = my_app_schema.dump(entries)
    return jsonify(result)

@app.route('/order',methods=["POST"])
def post_order():
    req=request.get_json()
    order_id = req['order_id']
    size = req['size']
    toppings = req['toppings']
    crust = req['crust']
    new_entry = Myapp(order_id=order_id,size=size,toppings=toppings,crust=crust)
    
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for("get_order"))        

if __name__ == '__main__':
    db.create_all()
    app.run()