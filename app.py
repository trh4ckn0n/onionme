from flask import Flask, render_template, request, redirect, send_from_directory
import os
import base64
import string

app = Flask(__name__)

# Stockage des résultats
results = {}

# Créer le dossier oniondom s'il n'existe pas
os.makedirs("oniondom", exist_ok=True)

# Lire contenu texte ou base64
def read_text_or_base64(path):
    try:
        with open(path, "r") as f:
            content = f.read().strip()
            if all(c in string.printable for c in content):
                return content
            else:
                raise ValueError("Non imprimable")
    except:
        try:
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8") + " (base64)"
        except:
            return "Non disponible"

# Générer un domaine .onion avec préfixe
def generate_onion(prefix):
    folder_name = "trkn" + base64.b64encode(os.urandom(8)).decode("utf-8").lower().replace("=", "").replace("/", "").replace("+", "")
    folder_path = os.path.join("oniondom", folder_name)
    os.makedirs(folder_path, exist_ok=True)

    hostname_path = os.path.join(folder_path, "hostname")
    pubkey_path = os.path.join(folder_path, "hs_ed25519_public_key")
    seckey_path = os.path.join(folder_path, "hs_ed25519_secret_key")

    onion = prefix + base64.b32encode(os.urandom(16)).decode("utf-8").lower().strip("=") + ".onion"
    onion_core = onion.replace(".onion", "")

    with open(hostname_path, "w") as f:
        f.write(onion + "\n")
    with open(pubkey_path, "wb") as f:
        f.write(b"== ed25519v1-public: type0 ==\n" + os.urandom(32))
    with open(seckey_path, "wb") as f:
        f.write(b"== ed25519v1-secret: type0 ==\n" + os.urandom(64))

    # Vérifie si le domaine est valide (56 caractères hors .onion)
    if len(onion_core) == 56:
        results[folder_name] = {
            "onion": onion,
            "hostname": read_text_or_base64(hostname_path),
            "public_key": read_text_or_base64(pubkey_path),
            "secret_key": read_text_or_base64(seckey_path),
            "folder": folder_name,
            "prefix": prefix,
            "valid": True
        }
    else:
        results[folder_name] = {
            "onion": f"[Invalide] {onion}",
            "hostname": "Erreur : domaine invalide (longueur incorrecte)",
            "public_key": "Non généré",
            "secret_key": "Non généré",
            "folder": folder_name,
            "prefix": prefix,
            "valid": False
        }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    prefix_text = request.form["prefix"]
    prefixes = prefix_text.strip().split()
    for prefix in prefixes:
        generate_onion(prefix)
    return redirect("/result")

@app.route("/result")
def result():
    return render_template("result.html", results=results)

@app.route("/download/<folder>/<filename>")
def download(folder, filename):
    folder_path = os.path.join("oniondom", folder)
    return send_from_directory(folder_path, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
