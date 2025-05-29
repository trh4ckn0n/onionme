from flask import Flask, render_template, request
import subprocess
import threading

app = Flask(__name__)

results = {}

def generate_onion(prefix):
    try:
        result = subprocess.run(["oniongen", f"^{prefix}", "5"], capture_output=True)
        output = result.stdout.decode().strip()
        if output:
            results[prefix] = output.split("\n")[0]
        else:
            results[prefix] = "Erreur ou aucun résultat"
    except Exception as e:
        results[prefix] = f"Erreur : {str(e)}"

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

        # Exécuter cpkey.py si option "copier" cochée
        if copy_choice == 'yes':
            subprocess.run(["python3", "cpkey.py"])

        return render_template('result.html', results=results)

    return render_template('index.html')
