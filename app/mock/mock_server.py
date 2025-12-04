from flask import Flask, jsonify
app = Flask(__name__)

# 模拟那个巨大的返回体
mock_response = {
    "releaseVersion": "1.13.5",
    "translationService": "bing",
    "sensitiveConfig": {"maskConfig": {"maskPassword": True}},
    "translationServices": {"openai": {"models": "gpt-4|gpt-3.5"}}
}

@app.route('/api/v1/app/config', methods=['POST'])
def config():
    return jsonify(mock_response)

if __name__ == '__main__':
    app.run(port=5000)