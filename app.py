from flask import Flask, render_template, request, send_from_directory
import subprocess
import threading
import os
import base64

app = Flask(__name__)
results = {}

def read_file_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode('ascii')
    else:
        return "Non trouvé"

def generate_onion(prefix):
    try:
        result = subprocess.run(["oniongen", f"^{prefix}", "5"], capture_output=True)
        output = result.stdout.decode('utf-8', errors='replace').strip()

        if output:
            folder_name = output.split("\n")[0].strip()

            hostname_path = os.path.join(folder_name, "hostname")
            pubkey_path = os.path.join(folder_name, "hs_ed25519_public_key")
            seckey_path = os.path.join(folder_name, "hs_ed25519_secret_key")

            # Lire l'adresse .onion
            if os.path.exists(hostname_path):
                with open(hostname_path, "r") as f:
                    onion_domain = f.read().strip()
            else:
                onion_domain = "non trouvé"

            results[prefix] = {
                "onion": onion_domain,
                "hostname_b64": read_file_base64(hostname_path),
                "public_key_b64": read_file_base64(pubkey_path),
                "secret_key_b64": read_file_base64(seckey_path),
                "folder": folder_name
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

@app.route('/download/<onion>/<filename>')
def download_key(onion, filename):
    directory = os.path.join(os.getcwd(), onion)
    return send_from_directory(directory, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
