from flask import Flask, jsonify, request
import json
import sys
from datetime import datetime

app = Flask(__name__)

transactions = []
persons = [] 

class Person:
    def __init__(self, nom, prenom, solde):
        self.nom = nom
        self.prenom = prenom
        self.solde = solde
    
    def to_json(self):
        return {'nom': self.nom, 'prenom': self.prenom, 'solde': self.solde}

    def to_json_identity(self):
        return {'nom': self.nom, 'prenom': self.prenom}
        
    def debit(self, sum):
        self.solde -= sum
        
    def credit(self, sum):
        self.solde += sum
        
    def transaction(self, P2, sum):
        self.debit(sum)
        P2.credit(sum)
    
    def equals(self, nom, prenom):
        return nom == self.nom and prenom == self.prenom

def find(nom, prenom):
    for personne in persons:
        if(personne.equals(nom, prenom)):
            return personne
    return False

@app.route("/")
def print():
    res = "<h1>Liste des personnes :</h1><ul>"
    for person in persons:
        res += "<li>NOM : " + person.nom + " / PRENOM : " + person.prenom + " / SOLDE COMPTE : " + str(person.solde) + "</li>"
    res += "</ul><h1>Liste des transactions :</h1><ul>"
    for transaction in transactions:
        res += "<li>P1 : " + transaction[0].nom + " " + transaction[0].prenom + " / P2 : " + transaction[1].nom + " " + transaction[1].prenom + " / DATE : " + transaction[2].strftime("%Y-%m-%d %H:%M:%S") + " / SOMME : " + str(transaction[3]) + "</li>"
    return res+"</ul>"

@app.route('/print-transactions', methods=['GET'])
def print_transactions():
    if request.method == 'GET':
        sorted_transactions = sorted(transactions, key=lambda transaction: transaction[2])
        return jsonify([{'P1': person1.to_json_identity(), 'P2': person2.to_json_identity(), 't': t, 's': s} for person1, person2, t, s in sorted_transactions])

# curl -X "GET" http://localhost:5000/print-transactions


@app.route('/print-person-transactions', methods=['GET'])
def print_person_transactions(): 
    if request.method == 'GET':
        person_transactions = []
        nom = request.form['nom']
        prenom = request.form['prenom']
        
        person1 = find(nom, prenom)
        
        for transaction in transactions:
            if transaction[0].nom == person1.nom and transaction[0].prenom == person1.prenom:
                person_transactions.append(transaction)
            elif transaction[1].nom == person1.nom and transaction[1].prenom == person1.prenom:
                person_transactions.append(transaction)
            
        sorted_person_transactions = sorted(person_transactions, key=lambda transaction: transaction[2])
        return jsonify([{'P1': person1.to_json_identity(), 'P2': person2.to_json_identity(), 't': t, 's': s} for person1, person2, t, s in sorted_person_transactions])

# curl -X "GET" -d "nom=Dupont&prenom=Jean" http://localhost:5000/print-person-transactions


@app.route("/do-transaction", methods=['PUT'])
def do_transaction():
    if request.method == 'PUT':
        data = request.get_json()
        
        P1 = data['P1']
        person1 = find(P1['nom'], P1['prenom'])
        if(person1 == False):
            person1 = Person(P1['nom'], P1['prenom'], P1['solde'])
            persons.append(person1)
            
        P2 = data['P2']
        person2 = find(P2['nom'], P2['prenom'])
        if(person2 == False):
            person2 = Person(P2['nom'], P2['prenom'], P2['solde'])
            persons.append(person2)
        
        t = datetime.strptime(data['t'], "%Y-%m-%d %H:%M:%S")
        s = data['s']
        
        transactions.append((person1, person2, t, s))
        transactions_json = {'P1': person1.to_json(), 'P2': person2.to_json(), 't': t, 's': s}
        person1.transaction(person2, s)

        return jsonify(transactions_json)

# curl -X PUT -H "Content-Type: application/json" -d '{"P1": {"nom": "Dupont", "prenom": "Jean", "solde": 100}, "P2": {"nom": "Titou", "prenom": "Dylan", "solde": 200}, "t": "2023-01-12 15:04:22", "s": 50}' http://localhost:5000/do-transaction
# curl -X PUT -H "Content-Type: application/json" -d '{"P1": {"nom": "Titou", "prenom": "Dylan"}, "P2": {"nom": "Dupont", "prenom": "Jean"}, "t": "2023-01-12 17:10:52", "s": 20}' http://localhost:5000/do-transaction

@app.route('/affiche-solde', methods=['GET'])
def affiche_solde():
    if request.method == 'GET':
        nom = request.form['nom']
        prenom = request.form['prenom']
        
        person = find(nom, prenom)
        if(person == False):
            solde = "This person doesn't exist"
        else:
            solde = person.solde

        return jsonify("solde : " + str(solde))

# curl -X "GET" -d "nom=Dupont&prenom=Jean" http://localhost:5000/affiche-solde

if __name__ == "__main__":
    if len(sys.argv) > 1 :
        if sys.argv[1] == "check_syntax":
            print("Build [ OK ]")
            exit(0)
        else:
            print("Passed argument not supported ! Supported argument : check_syntax")
    app.run(debug=True)