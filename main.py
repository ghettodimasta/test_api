import ast
import json
import sqlite3
from flask import Flask, request, Response, send_from_directory, flash, redirect, url_for, jsonify
import uuid
from random import randint
from icecream import ic
from tables import *
import numpy as np
from itertools import chain
import base64

app = Flask(__name__)


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
        name = None
        param_key = None
        param_value = None
        ans = []
        filters = ast.literal_eval(request.data.decode("UTF-8"))
        if 'name' in filters.keys() and 'param_key' in filters.keys() and 'param_value' in filters.keys():
            print("Y")
            return {'success': False, 'res': "Wrong json parametrs"}
        if 'name' in filters.keys():
            name = filters['name']
        elif 'param_key' in filters.keys() and 'param_value' in filters.keys():
            param_key = filters['param_key']
            param_value = filters['param_value']
        else:
            return {'success': False, 'res': "Wrong json parametrs"}
    except:
        return {'success': False, 'res': f"Bad request: omitted argument"}
    try:

        sqn = sql.select('products', fields='name')
        names = []

        for n in sqn:
            if name is not None:
                if n[0].find(name) >= 0:
                    names.append(n[0])
            elif name is None and param_key is None and param_value is None:
                names.append(n[0])
        ic(names)
        for i in names:
            ic(i)
            ans.append({"name": i})

        if param_key is not None and param_value is not None:
            sqp = sql.select('products', fields='params')
            ic(sqp)
            params = []
            for p in sqp:
                ic(p[0])
                if param_key in p[0] and param_value in p[0].values():
                    ic(param_key)
                    ic(param_value)
                    params.append(p[0])
                    ic(params)
            if not params:
                return {'success': True, 'res': ans}
            ic(params)
            filter_res = []
            for i in params:
                i = json.dumps(i)
                ic(i)
                name = sql.select('products', fields='name', where="params = %s", values=(i,))
                ic(name)
                if name not in filter_res:
                    filter_res.append(name)
                filter_res_opt = []
                ic(filter_res)
                for i in filter_res:
                    filter_res_opt+=i
                ic(filter_res_opt)

            for i in filter_res_opt:
                ic(i)
                ic("".join(i))
                names.append("".join(i))
            for name in names:
                ic(name)
                ans.append({'name': name})
        return {'success': True, 'res': ans}
    except Exception as e:
        return {'success': False, 'res': e}


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
        product = sql.select('products', fields='*', where='id = %s', values=(id,), one=True)
        ic(product)
    except Exception as e:
        ic(e)
        return {'success': False, 'res': f"Bad request: omitted id argument"}
    return {'success': True, 'res': {'name': product[1], "params": product[3]}}


def new_num():
    nums = sql.select('products', 'id')
    res = []
    for num in nums:
        ic(num[0])
        res.append(num[0])
    number = randint(10000, 99999)
    while number in res:
        number = randint(10000, 99999)
    return number


@app.route('/CreateProduct', methods=['GET', 'POST'])
def new_product():
    """ Try to use
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
        sql.insert('products',
                   values=(new_num(), product['name'], product['description'], json.dumps(product['parametrs'])))
        ic({'success': True, 'res': 'product added'})
        return {'success': True, 'res': 'product added'}
    except Exception as e:
        ic(e)
        return {'success': False, 'res': str(e)}


if __name__ == "__main__":
    # ic(new_num())
    app.run(debug=True)
