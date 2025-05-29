from flask import Flask, render_template, request
import subprocess
import threading
import os

app = Flask(__name__)

# Dictionnaire pour stocker les résultats
results = {}

# Fonction pour générer une adresse .onion personnalisée
def generate_onion(prefix):
    try:
        result = subprocess.run(["oniongen", f"^{prefix}", "5"], capture_output=True)
        output = result.stdout.decode().strip()

        if output:
            onion_address = output.split("\n")[0]
            onion_dir = onion_address  # Nom du dossier = adresse .onion

            # Chemins vers les fichiers clés
            hostname_path = os.path.join(onion_dir, "hostname")
            pubkey_path = os.path.join(onion_dir, "hs_ed25519_public_key")
            seckey_path = os.path.join(onion_dir, "hs_ed25519_secret_key")

            # Lecture des fichiers si disponibles
            hostname = open(hostname_path).read().strip() if os.path.exists(hostname_path) else "Non trouvé"
            pubkey = open(pubkey_path).read().strip() if os.path.exists(pubkey_path) else "Non trouvé"
            seckey = open(seckey_path).read().strip() if os.path.exists(seckey_path) else "Non trouvé"

            # Stockage du résultat dans le dictionnaire
            results[prefix] = {
                "onion": onion_address,
                "hostname": hostname,
                "public_key": pubkey,
                "secret_key": seckey
            }
        else:
            results[prefix] = {"error": "Aucune adresse générée"}
    except Exception as e:
        results[prefix] = {"error": str(e)}

# Page d'accueil avec formulaire
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prefixes = request.form['prefixes'].split()
        copy_choice = request.form.get('copy')

        threads = []
        results.clear()

        # Génération multithreadée des adresses
        for prefix in prefixes:
            thread = threading.Thread(target=generate_onion, args=(prefix,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        # Lancement de cpkey.py si option cochée
        if copy_choice == 'yes':
            subprocess.run(["python3", "cpkey.py"])

        return render_template('result.html', results=results)

    return render_template('index.html')

# Lancement de l'application Flask
def main():
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
