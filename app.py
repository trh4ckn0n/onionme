from flask import Flask, render_template, request, redirect, send_from_directory
import os
import subprocess
import base64
import string
import shutil

app = Flask(__name__)

# Stocker tous les résultats
results = {}

# Création du dossier oniongen si n'existe pas
os.makedirs("oniongen", exist_ok=True)

# Fonction pour lire le fichier en texte brut ou base64 si nécessaire
def read_text_or_base64(path):
    try:
        with open(path, "r") as f:
            content = f.read().strip()
            if all(c in string.printable for c in content):
                return content  # Texte brut lisible
            else:
                raise ValueError("Contenu non imprimable")
    except:
        try:
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8") + " (base64)"
        except:
            return "Non disponible"

# Fonction pour lire en base64 uniquement
def read_file_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8") + " (base64)"
    except:
        return "Non disponible"

# Générer un domaine .onion avec un préfixe
def generate_onion(prefix):
    folder_name = "trkn" + base64.b64encode(os.urandom(8)).decode("utf-8").lower().replace("=", "").replace("/", "").replace("+", "")
    folder_path = os.path.join("oniongen", folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Simule la génération Tor (exemple seulement)
    hostname_path = os.path.join(folder_path, "hostname")
    pubkey_path = os.path.join(folder_path, "hs_ed25519_public_key")
    seckey_path = os.path.join(folder_path, "hs_ed25519_secret_key")

    onion = prefix + base64.b32encode(os.urandom(16)).decode("utf-8").lower().strip("=") + ".onion"

    with open(hostname_path, "w") as f:
        f.write(onion + "\n")

    with open(pubkey_path, "wb") as f:
        f.write(b"== ed25519v1-public: type0 ==\n" + os.urandom(32))

    with open(seckey_path, "wb") as f:
        f.write(b"== ed25519v1-secret: type0 ==\n" + os.urandom(64))

    results[folder_name] = {
        "onion": onion,
        "hostname": read_text_or_base64(hostname_path),
        "public_key": read_text_or_base64(pubkey_path),
        "secret_key": read_text_or_base64(seckey_path),
        "folder": folder_name,
        "prefix": prefix
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    prefix = request.form["prefix"]
    generate_onion(prefix)
    return redirect("/result")

@app.route("/result")
def result():
    return render_template("result.html", results=results)

@app.route("/download/<path:folder>/<filename>")
def download(folder, filename):
    folder_path = os.path.join("oniongen", folder)
    return send_from_directory(folder_path, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
