# 🧅 OnionGen – Générateur d'adresses .onion personnalisées par **trhacknon**

![tor](https://raw.githubusercontent.com/trh4ckn0n/onionme/main/static/tor.svg)

> Application Flask permettant de générer des services `.onion` personnalisés avec des préfixes spécifiques.

---

## 🚀 Fonctionnalités principales

- Génération d'adresses `.onion` avec préfixes personnalisés (ex: `trknabc123.onion`)
- Téléchargement direct des fichiers `hostname`, `public_key`, `secret_key`
- Interface stylée **hacker** 💻 avec logo Tor, favicon et illustrations SVG
- Usage local ou hébergeable (Render, Replit, etc.)
- Utilisation pédagogique uniquement 🧠

---

<details>
<summary><strong>🔧 Comment ça fonctionne ?</strong></summary>

### Étapes :

1. L’utilisateur entre un ou plusieurs préfixes souhaités dans le champ.
2. Le serveur utilise des outils (comme `scallion`, `vanitygen`, ou `mkp224o`) pour générer une ou plusieurs adresses `.onion` correspondant aux préfixes.
3. Les clés générées sont stockées dans un dossier temporaire.
4. L'utilisateur peut **télécharger** :
   - `hostname` – l’adresse `.onion`
   - `hs_ed25519_public_key` – clé publique
   - `hs_ed25519_secret_key` – clé secrète

</details>

---

<details>
<summary><strong>🖼️ Aperçu de l'interface</strong></summary>

### Page d’accueil :

![interface1](https://raw.githubusercontent.com/trh4ckn0n/onionme/main/static/torbirdy.svg)

### Page des résultats :

- Affichage des résultats avec style rétro/cyber
- Icônes & Emojis pour améliorer l’expérience

</details>

---

## 🛠️ Dépendance externe requise : `oniongen-go`

Ce projet utilise **[oniongen-go](https://github.com/trh4ckn0n/oniongen-go)** pour la génération rapide et efficace d'adresses `.onion` de type v3 avec préfixes personnalisés.

### 🔗 Installation

Assurez-vous d’avoir **Go** installé sur votre machine, puis exécutez :

```bash
git clone https://github.com/trh4ckn0n/oniongen-go.git
cd oniongen-go
go build -o oniongen
sudo mv oniongen /usr/local/bin/
```

> ✅ Le binaire oniongen doit être accessible globalement (dans votre $PATH) pour que l'application Flask puisse l'utiliser automatiquement.

---

## 📁 Arborescence du projet

```bash
oniongen/
├── static/
│   ├── tor.svg
│   ├── carml-logo.svg
│   └── torbirdy.svg
├── templates/
│   ├── index.html
│   └── result.html
├── app.py
├── README.md
└── requirements.txt
```

## ⚙️ Lancer le projet en local
 ```
git clone https://github.com/trh4ckn0n/onionme
cd onionme
pip install -r requirements.txt python app.py
 ```
 
💡 L'application sera accessible sur : [http://localhost:5000](http://localhost:5000)
 
  
## 💡 Exemple d’utilisation
 
Saisis dans le champ de texte :
 `trhacknon oniongen darkweb ` 
🔍 Le système va tenter de générer les adresses `.onion` suivantes :
 
 
- `trhacknon[...].onion`
 
- `oniongen[...].onion`
 
- `darkweb[...].onion`
 

 
📦 Résultat : un tableau avec les adresses générées et un bouton de téléchargement pour chaque fichier lié.
  
