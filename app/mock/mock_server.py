from flask import Flask, jsonify, request

app = Flask(__name__)

# 必须确保这里的路径 和 config.yaml 里的 path 拼起来是一致的
# config.yaml: /api/v1/app/config
@app.route('/api/v1/app/config', methods=['POST'])
def config():
    return jsonify({
        "releaseVersion": "1.13.5",
        "translationService": "bing",
        "sensitiveConfig": {"maskConfig": {"maskPassword": True}},
        "translationServices": {"openai": {"models": "gpt-4|gpt-3.5"}}
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) # 记得用 5001