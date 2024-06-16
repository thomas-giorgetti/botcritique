# Installation

## Générer l'environnement virtuel

python -m venv venv
source venv/bin/activate

## Installation des pré-requis

Avec l'environnement virtuel activé

pip install -r requirements.txt

## Créer le .env
```
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=8000
FLASK_APP=run.py
FLASK_DEBUG=1
DISCORD_BOT_TOKEN=token_bot_discord
```

## Initialiser la base sqlite3

Avec l'environnement virtuel activé

python init_db

## Lancement de l'application

Avec l'environnement virtuel activé

flask run

## Lancement du bot

Avec l'environnement virtuel activé

python bot.py

## Création des services

nano /etc/systemd/system/flask_app.service

```
[Unit]
Description=Flask Application
After=network.target

[Service]
User=user_service
WorkingDirectory=/chemin/vers/botcritique
ExecStart=/chemin/vers/botcritique/venv/bin/flask run --host=0.0.0.0 --port=8000
Restart=always

[Install]
WantedBy=multi-user.target
```

nano /etc/systemd/system/discord_bot.service

```
[Unit]
Description=Discord Bot
After=network.target

[Service]
User=user_service
WorkingDirectory=/chemin/vers/botcritique
ExecStart=/chemin/vers/botcritique/venv/bin/python3 /chemin/vers/botcritique/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

systemctl daemon-reload

systemctl enable flask_app

systemctl start flask_app

systemctl enable discord_bot

systemctl start discord_bot

# Utilisation

## Commandes

### !critique url_imdb note critique

La note doit se trouver entre 1 et 10

La critique doit faire 500 signes ou moins

La commande met à jour une critique existante si une ancienne est trouvée

### !list url_imdb

Liste les notes et le nom de l'utilisateur qui l'a publiée.

Retourne l'id_critique

### !hasard url_imdb

Retourne une critique au hasard

### !del id_critique

Supprime la critique de la base de donnée

## /infos

http://ip_host:8000/infos
