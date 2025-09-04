
from flask import Flask, request, jsonify

app = Flask(__name__)
app.url_map.strict_slashes = False  # aceita /github-webhook e /github-webhook/

@app.before_request
def log_before():
    app.logger.info(">> %s %s", request.method, request.path)

@app.after_request
def log_after(resp):
    app.logger.info("<< %s %s -> %s", request.method, request.path, resp.status)
    return resp

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    # headers + corpo (tenta JSON, cai para RAW)
    headers = {k: v for k, v in request.headers.items()}
    json_payload = request.get_json(silent=True)
    raw = request.get_data(as_text=True)

    app.logger.info("HEADERS: %r", headers)
    if json_payload is not None:
        app.logger.info("JSON: %r", json_payload)
    else:
        app.logger.info("RAW: %s", raw)

    return jsonify({"message": "Webhook recebido com sucesso do GitHub!"}), 200

if __name__ == '__main__':
    # importante para logs aparecerem no docker logs
    import os
    os.environ["PYTHONUNBUFFERED"] = "1"
    # ativa logs de app e werkzeug no stdout
    import logging, sys
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    app.logger.handlers.clear()
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    # também direciona o werkzeug para stdout
    logging.getLogger('werkzeug').handlers.clear()
    logging.getLogger('werkzeug').addHandler(handler)
    logging.getLogger('werkzeug').setLevel(logging.INFO)

    app.logger.info("== Flask webhook-server iniciado ==")
    app.run(host='0.0.0.0', port=5000)
