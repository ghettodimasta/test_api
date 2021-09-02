import ast
from flask import Flask, request
import uuid
from random import randint
from icecream import ic
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient(port=27017)
db = client.products


def new_num():
    nums = []
    for i in db.reviews.find():
        nums.append(i["id"])
    res = []
    for num in nums:
        ic(num)
        res.append(num)
    number = randint(10000, 99999)
    while number in res:
        number = randint(10000, 99999)
    return number


@app.route('/')
@app.route('/home')
def index():
    return 'Main page'


@app.route('/GetProducts', methods=['GET', 'POST'])
def get_names():
    """
    curl --header "Content-Type: application/json" \
      --request POST \
      --data '{"name":"iph","param_key":"arch","param_value": "arm"}' \
      http://localhost:5000/GetProducts
    """
    try:
        ans = []
        filters = ast.literal_eval(request.data.decode("UTF-8"))
        name = filters.get("name")
        params = filters.get("params")
    except:
        return {'success': False, 'res': f"Bad request: omitted argument"}
    try:
        names = []
        if params is None:
            if name is not None:
                for i in db.reviews.find():
                    if i["name"].find(name) >= 0:
                        names.append(i["name"])
                ic(names)
                if names is None:
                    return {'success': False, 'res': "Not found"}
        else:
            params_to_mongo = {}
            for key, value in params.items():
                params_to_mongo["params." + key] = value
            ic(params_to_mongo)
            result = db.reviews.find(params_to_mongo)
            for i in result:
                ic(i['name'])
                if name is not None:
                    if i["name"].find(name) >= 0:
                        names.append(i["name"])
                else:
                    names.append(i["name"])

        for name in names:
            ic(name)
            ans.append({'name': name})
        return {'success': True, 'res': ans}
    except Exception as e:
        return {'success': False, 'res': str(e)}


@app.route('/GetParams', methods=['GET', 'POST'])
def get_params():
    """
    curl --header "Content-Type: application/json" \
      --request POST \
      --data '{"id":"21494"}' \
      http://localhost:5000/GetParams
    """
    try:
        id = ast.literal_eval(request.data.decode("UTF-8"))['id']
        ic(id)
        product = db.reviews.find({"id": int(id)})[0]
        ic(product)
    except Exception as e:
        ic(e)
        return {'success': False, 'res': f"no such element"}
    return {'success': True,
            'res': {'name': product['name'], 'description': product['description'], "params": product['params']}}


@app.route('/CreateProduct', methods=['GET', 'POST'])
def new_product():
    """
    curl --header "Content-Type: application/json" \
      --request POST \
      --data '{"name":"some_test_phone","description":"test_desc_with_curl","parametrs":{"camera": "12px", "color": "red"}}' \
      http://localhost:5000/CreateProduct
    """
    try:
        product = ast.literal_eval(request.data.decode("UTF-8"))
        ic(product)
    except Exception as e:
        ic(e)
        return {'success': False, 'res': f"Bad request: omitted id, name, description"
                                         f" arguments"}
    try:
        good = {
            "id": new_num(),
            "name": product['name'],
            "description": product['description'],
            "params": product['parametrs']
        }
        db.reviews.insert_one(good)
        ic({'success': True, 'res': 'product added'})
        return {'success': True, 'res': 'product added'}
    except Exception as e:
        ic(e)
        return {'success': False, 'res': str(e)}


if __name__ == "__main__":
    app.run(debug=True)
