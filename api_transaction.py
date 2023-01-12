from flask import Flask, jsonify, request
import json

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


@app.route('/print-transactions', methods=['GET'])
def print_transactions():
    if request.method == 'GET':
        return jsonify([{'P1': person1.to_json(), 'P2': person2.to_json(), 't': t, 's': s} for person1, person2, t, s in transactions])

# curl -X "GET" http://localhost:5000/print-transactions

@app.route("/do-transaction", methods=['POST'])
def do_transaction():
    if request.method == 'POST':
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
        
        t = data['t']
        s = data['s']
        
        person1.transaction(person2, s)
        transactions.append((person1, person2, t, s))
        transactions_json = {'P1': person1.to_json(), 'P2': person2.to_json(), 't': t, 's': s}
        return jsonify(transactions_json)

# curl -X POST -H "Content-Type: application/json" -d '{"P1": {"nom": "Dupont", "prenom": "Jean", "solde": 100}, "P2": {"nom": "Titou", "prenom": "Jean", "solde": 200}, "t": "12-01-2023 15:04", "s": 50}' http://localhost:5000/do-transaction
# curl -X POST -H "Content-Type: application/json" -d '{"P1": {"nom": "Titou", "prenom": "Jean"}, "P2": {"nom": "Dupont", "prenom": "Jean"}, "t": "12-01-2023 15:04", "s": 20}' http://localhost:5000/do-transaction

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
	app.run()