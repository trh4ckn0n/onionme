from flask import Flask, render_template, request, send_from_directory
import subprocess
import threading
import os

app = Flask(__name__)
results = {}

def generate_onion(prefix):
    try:
        result = subprocess.run(["oniongen", f"^{prefix}", "5"], capture_output=True)
        output = result.stdout.decode('utf-8', errors='replace').strip()

        if output:
            onion_address = output.split("\n")[0]
            onion_dir = onion_address

            # Fichiers générés
            hostname_path = os.path.join(onion_dir, "hostname")
            pubkey_path = os.path.join(onion_dir, "hs_ed25519_public_key")
            seckey_path = os.path.join(onion_dir, "hs_ed25519_secret_key")

            hostname = open(hostname_path).read().strip() if os.path.exists(hostname_path) else "Non trouvé"
            pubkey = open(pubkey_path).read().strip() if os.path.exists(pubkey_path) else "Non trouvé"
            seckey = open(seckey_path).read().strip() if os.path.exists(seckey_path) else "Non trouvé"

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prefixes = request.form['prefixes'].split()
        copy_choice = request.form.get('copy')

        threads = []
        results.clear()

        for prefix in prefixes:
            thread = threading.Thread(target=generate_onion, args=(prefix,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        if copy_choice == 'yes':
            subprocess.run(["python3", "cpkey.py"])

        return render_template('result.html', results=results)

    return render_template('index.html')

# Route pour télécharger un fichier de clé
@app.route('/download/<onion>/<filename>')
def download_key(onion, filename):
    directory = os.path.join(os.getcwd(), onion)
    return send_from_directory(directory, filename, as_attachment=True)

# Lancement
def main():
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
