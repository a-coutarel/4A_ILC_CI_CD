# 4A_ILC_CI_CD - ESIREM

Groupe :
--------
**COUTAREL Allan**    
**DEVOUCOUX Maxime**


## Sujet

L'API est réalisée en langage Python.

Ce projet utilise Flask pour créer une application Web qui permet de gérer des transactions bancaires. Il utilise également BytesIO, TextIOWrapper, datetime, sys, hashlib et csv pour des fonctionnalités supplémentaires.

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

⚠️ Veuillez importer un fichier CSV de personnes avant d'utiliser d'autres routes

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

## Badges 

![Status_actions](https://github.com/a-coutarel/4A_ILC_CI_CD/actions/workflows/app_build.yml/badge.svg) ![Status_actions](https://github.com/a-coutarel/4A_ILC_CI_CD/actions/workflows/build_image.yml/badge.svg) ![Status_actions](https://github.com/a-coutarel/4A_ILC_CI_CD/actions/workflows/build_and_push.yml/badge.svg)