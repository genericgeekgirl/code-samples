from flask import Flask, jsonify, request, make_response
import json

app = Flask(__name__)

items_list = []

@app.route('/receive', methods=['POST', 'GET'])

def receive():

    req = request.get_json(silent=True, force=True)
    action = req['result']['action']
    
    if action == "item.add":
        item = req['result']['parameters']['item']
        
        items_list.append(item)
        output = {"displayText": "You added " + item + "."}
        
    elif action == "item.list":        
        output = {"displayText": "Items on list: " + ", ".join(items_list)}

    elif action == "item.remove":
        item = req['result']['parameters']['item']

        items_list.remove(item)

        output = {"displayText": "You removed " + item + "."}
        
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True)