from flask import Flask
from rutas.rutas_bebidas import bp_bebidas

app = Flask(__name__)

app.register_blueprint(bp_bebidas)

if __name__ == "__main__":
    app.run(debug=True)