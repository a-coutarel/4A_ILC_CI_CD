# 4A_ILC_CI_CD - ESIREM

Groupe :
--------
**COUTAREL Allan**    
**DEVOUCOUX Maxime**


## Sujet

L'API est réalisée en langage Python.

Ce projet utilise Flask pour créer une application Web qui permet de gérer des transactions bancaires. Il utilise également BytesIO, TextIOWrapper, datetime, sys, hashlib et csv pour des fonctionnalités supplémentaires.

Nous avons choisi ce sujet car nous l'avons trouvé pertient pour implémenter les solutions demandées.

## Fonctionnalités

* Initialisation de l'application Flask
* Création d'une classe Personne qui permet de créer des objets Personne avec un nom, un prénom et un compte bancaire. Les objets Personne peuvent être converties en objets JSON, avoir des méthodes pour débiter ou créditer un compte, effectuer une transaction entre deux personnes et vérifier si l'identité d'une personne correspond à une entrée de nom et de prénom
* Création d'une liste vide pour stocker les transactions et les personnes
* Définition d'une fonction pour trouver une personne dans la liste de personnes en utilisant un nom et un prénom
* Route pour afficher toutes les personnes et les transactions
* Route pour importer un fichier CSV de personnes
* Route pour afficher toutes les transactions triées par date
* Route pour afficher toutes les transactions liées à une personne triées par date
* Route pour effectuer une transaction entre 2 personnes
* Route pour afficher le solde du compte d'une personne
* Route pour vérifier l’intégrité des données envoyées en recalculant les hashs à partir des données envoyées et en les comparant avec les hashs stockés dans l'API.
* Route pour ajouter une personne
* Route pour supprimer une personne

⚠️ Veuillez importer un fichier CSV de personnes avant d'utiliser d'autres routes : si les personnes n'existent pas, il est impossible d'effectuer des transactions. Il faut d'abord importer des personnes pour effectuer des transactions entre elles.

*Note : Depuis la version v2.2.0, il est possible d'ajouter ou de supprimer une personne avec des routes. Quand une personne est supprimée, toutes les transactions liées à cette personne restent.*

## Utilisation

* Démarrez l'application Flask localement : 
    ```bash
    pip install flask
    export FLASK_APP=api_transaction.py
    export FLASK_ENV=development
    flask run
    ```

* Démarrez l'application à partir d'une image docker de l'API ( build and run - utilisation du Dockerfile ) : 
    ```bash
    docker build -t api_transaction .
    docker run -p 5000:5000 api_transaction
    ```

* Utilisez la route '/' pour afficher toutes les personnes et les transactions.
    - *Dans un navigateur :*
        ```bash
        http://localhost:5000/
        ```
    - *Avec une commande curl :*
        ```bash
        curl -X GET "http://localhost:5000/"
        ```

* Utilisez la route '/import' pour importer un fichier CSV de personnes en utilisant la commande curl ou en envoyant le fichier via une requête POST.
    - *Avec une commande curl :*
        ```bash
        curl -X POST -F 'file=@persons.csv' http://localhost:5000/import
        ```

* Utilisez la route '/print-transactions' pour afficher toutes les transactions triées par date.
    - *Dans un navigateur :*
        ```bash
        http://localhost:5000/print-transactions
        ```
    - *Avec une commande curl :*
        ```bash
        curl -X GET "http://localhost:5000/print-transactions"
        ```

* Utilisez la route '/print-person-transactions' pour afficher toutes les transactions liées à une personne triées par date.
    - *Dans un navigateur :*
        ```bash
        http://localhost:5000/print-person-transactions?lastname=Dupont&firstname=Jean
        ```
    - *Avec une commande curl :*
        ```bash
        curl -X GET "http://localhost:5000/print-person-transactions?lastname=Dupont&firstname=Jean"
        ```

* Utilisez la route '/do-transaction' pour effectuer une transaction entre 2 personnes.
    - *Avec une commande curl :*
        ```bash
        curl -X PUT -H "Content-Type: application/json" -d '{"P1": {"lastname": "Dupont", "firstname": "Jean"}, "P2": {"lastname": "Burger", "firstname": "Dylan"}, "t": "2023-01-12 15:04:22", "s": 50}' http://localhost:5000/do-transaction
        curl -X PUT -H "Content-Type: application/json" -d '{"P1": {"lastname": "Burger", "firstname": "Dylan"}, "P2": {"lastname": "Dupont", "firstname": "Jean"}, "t": "2023-01-12 17:10:52", "s": 20}' http://localhost:5000/do-transaction
        ```

* Utilisez la route '/print-account' pour afficher le solde du compte d'une personne.
    - *Dans un navigateur :*
        ```bash
        http://localhost:5000/print-account?lastname=Dupont&firstname=Jean
        ```
    - *Avec une commande curl :*
        ```bash
        curl -X GET "http://localhost:5000/print-account?lastname=Dupont&firstname=Jean"
        ```

* Utilisez la route '/verify-data' pour vérifier l’intégrité des données envoyées.
    - *Avec une commande curl :*
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"P1": {"lastname": "Burger", "firstname": "Dylan"}, "P2": {"lastname": "Dupont", "firstname": "Jean"}, "t": "2023-01-12 17:10:52", "s": 20}' http://localhost:5000/verify-data
        ```

* Utilisez la route '/add-person' pour ajouter une personne à la liste des personnes.
    - *Avec une commande curl :*
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"P": {"lastname": "Delarue", "firstname": "Marc", "account": 700}}' http://localhost:5000/add-person
        ```

* Utilisez la route '/delete-person' pour supprimer une personne de la liste des personnes.
    - *Avec une commande curl :*
        ```bash
        curl -X DELETE -H "Content-Type: application/json" -d '{"P": {"lastname": "Coutarel", "firstname": "Allan", "account": 800}}' http://localhost:5000/delete-person
        ```

## Précision sur l'importation d'un fichier csv

Pour un bon fonctionnement, le fichier csv doit respecter le format suivant : 
```
Nom1;Prenom1;solde1
Nom2;Prenom2;solde2
...
```

Lorsqu'un utilisateur effectue une requête POST à la route '/import', la fonction import_data sera exécutée. La fonction commence par vérifier si la méthode de requête est bien POST, sinon elle renvoie le message "Invalid request method".

Si la méthode de requête est POST, la fonction accède ensuite au fichier qui a été envoyé avec la requête en utilisant l'objet request.files. Le fichier est affecté à la variable file.

Le fichier est lu et le contenu est stocké dans une variable nommée file_bytes. Un objet BytesIO est créé à partir des octets du fichier et affecté à la variable f. La variable f est ensuite enveloppée dans un objet TextIOWrapper, qui permet de lire le fichier en tant que texte.

Un objet lecteur CSV est créé avec la variable f et le délimiteur ';' est passé à la fonction csv.reader(). L'objet lecteur est affecté à la variable reader.

La fonction parcourt ensuite les lignes dans le fichier CSV en utilisant une boucle for et l'objet reader. Pour chaque ligne, elle crée un nouvel objet Person et l'ajoute à la liste de personnes. L'objet Person est créé en passant les valeurs de la première, deuxième et troisième colonnes de la ligne en tant que paramètres à la classe Person. La troisième colonne est passée en tant que nombre réel.

Enfin, la fonction renvoie un objet JSON avec le message "CSV file imported with success !" indiquant que le fichier CSV a été importé avec succès.

## Précision sur la fonction de hachage

La fonction de hachage utilisée dans le code est SHA-256. Cette fonction de hachage est utilisée pour créer un jeton de hachage pour chaque transaction réalisée.

SHA-256 est une fonction de hachage cryptographique qui prend une entrée de n'importe quelle taille et la convertit en une sortie fixe de 256 bits. Cela signifie qu'une fois qu'une entrée est hachée en utilisant SHA-256, elle produira toujours la même sortie de 256 bits, quelle que soit la taille de l'entrée d'origine. De plus, la fonction de hachage est une opération à sens unique, ce qui signifie qu'il est très difficile, voire impossible, de déduire l'entrée d'origine à partir de la sortie de hachage.

Dans ce code, la fonction de hachage est utilisée pour créer un jeton de hachage pour chaque transaction qui est effectuée. Les données de transaction sont converties en chaîne (str(transaction_data)) et encodées en bytes (encode()). La fonction sha256() de la bibliothèque hashlib est utilisée pour créer le jeton de hachage. Enfin, la fonction hexdigest() est utilisée pour retourner le jeton de hachage sous forme de chaîne hexadécimale.

Le choix de SHA-256 est un bon choix car il est considéré comme sûr et est largement utilisé dans les applications de sécurité pour créer des jetons de hachage de manière fiable.

## Badges 

![Status_actions](https://github.com/a-coutarel/4A_ILC_CI_CD/actions/workflows/app_build.yml/badge.svg) ![Status_actions](https://github.com/a-coutarel/4A_ILC_CI_CD/actions/workflows/build_image.yml/badge.svg) ![Status_actions](https://github.com/a-coutarel/4A_ILC_CI_CD/actions/workflows/build_and_push.yml/badge.svg)

[![](https://img.shields.io/badge/PROJET_TERMINÉ_🚀-059142?style=for-the-badge&logoColor=white)](https://dev.to/envoy_/150-badges-for-github-pnk)