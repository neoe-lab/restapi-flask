
from flask import Flask, jsonify, make_response, request
app = Flask(__name__)
order = {
    "item1":{
        "product": 'notebook',
        "size" : 'small',
        "price": 20
    },
    "item2":{
        "product": 'notebook',
        "size" : 'small',
        "price": 20
    }
    
}
@app.route('/')
def main():
    return 'this is main'
@app.route('/orders')
def get_item_details():
    response = make_response(jsonify(order),200)
    return response
@app.route('/orders/<itemid>')
def get_unit_item_details(itemid):
    if itemid in order:
        response=make_response(jsonify(order[itemid]),200)
        return response
    return "Item not found"

@app.route('/orders/<itemid>/<detail>')
def get_detail(itemid,detail):
    item = order[itemid].get(detail)
    if item:
        response = make_response(jsonify(item),200)
        return response
    return "Item not found"
    
# create item product
@app.route('/orders/<itemid>',methods=['POST'])
def post_item_details(itemid):
    req = request.get_json()
    if itemid in order:
        response = make_response(jsonify({"error": "Order ID already exists"}),200)
        return response
    order.update({itemid:req})
    response = make_response(jsonify({"message": "New order created"}),201)
    return response

@app.route('/orders/<itemid>',methods=['PUT'])
def put_item_details(itemid): # overwrite/create order
    req = request.get_json()
    if itemid in order:
        # order.update({itemid:req})
        order[itemid]=req
        response = make_response(jsonify({"message": "Item Update"}),200)
        return response
    order[itemid]=req
    response = make_response(jsonify({"message": "New Item created"}),201)
    return response
@app.route('/orders/<itemid>',methods=['PATCH'])
def path_item_details(itemid): # add patch or update data
    req = request.get_json()
    print(req.items())
    if itemid in order:
        for k,v in req.items():
            order[itemid][k]=v
            response = make_response(jsonify({"message": "Item Update"}),200)
            return response
    order[itemid]=req
    response = make_response(jsonify({"message": "New Item created"}),201)
    return response


@app.route('/orders/<itemid>',methods=['DELETE'])
def delate_item_details(itemid): # delate
    if itemid in order:
        del order[itemid]
        response = make_response(jsonify({"message": "Delete items"}),204)
        return response
    response = make_response(jsonify({"error": "Order ID already exists"}),404)
    return response


if __name__ == '__main__':
    app.run(debug=True)