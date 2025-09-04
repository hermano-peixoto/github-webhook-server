
from flask import Flask, request, jsonify
import logging, sys, os

app = Flask(__name__)
app.url_map.strict_slashes = False  # aceita /github-webhook e /github-webhook/

# ===== Logging enxuto =====
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
app.logger.handlers.clear()
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Silenciar access log do Werkzeug (mostra só nossa linha)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

VERBOSE = os.getenv("WEBHOOK_VERBOSE", "0") == "1"  # ligue com WEBHOOK_VERBOSE=1

@app.route("/github-webhook", methods=["POST"])
def github_webhook():
    payload = request.get_json(silent=True) or {}
    # Extrai campos úteis com defaults seguros
    repo = (payload.get("repository") or {}).get("full_name", "?")
    ref = payload.get("ref", "?")                     # ex: refs/heads/main
    branch = ref.split("/")[-1] if ref else "?"
    pusher = (payload.get("pusher") or {}).get("name", "?")
    head = (payload.get("head_commit") or {}).get("id", "")[:7]
    msg  = (payload.get("head_commit") or {}).get("message", "").splitlines()[0]

    # Uma linha enxuta por evento
    app.logger.info("GitHub push: repo=%s branch=%s by=%s head=%s msg=%r",
                    repo, branch, pusher, head, msg)

    # (Opcional) modo detalhado
    if VERBOSE:
        app.logger.info("Headers: %r", dict(request.headers))
        # cuidado: pode ser grande
        # import json; app.logger.info("JSON: %s", json.dumps(payload, indent=2))

    return jsonify({"ok": True}), 200

if __name__ == "__main__":
    os.environ["PYTHONUNBUFFERED"] = "1"
    app.logger.info("== Flask webhook-server iniciado ==")
    app.run(host="0.0.0.0", port=5000)
