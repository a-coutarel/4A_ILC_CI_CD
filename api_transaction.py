# Import necessary modules from Flask, BytesIO, TextIOWrapper, datetime, sys and csv
from flask import Flask, jsonify, request
from io import BytesIO, TextIOWrapper
from datetime import datetime
import sys
import csv
import hashlib

# Initialize the Flask app
app = Flask(__name__)

# Create empty lists to store transactions and persons
transactions = []
persons = [] 


# Define Person class
class Person:
    # Initialize a person with last name, first name, and account
    def __init__(self, lastname, firstname, account):
        self.lastname = lastname
        self.firstname = firstname
        self.account = account
    
    # Create a JSON object of the person
    def to_json(self):
        return {'lastname': self.lastname, 'firstname': self.firstname, 'account': self.account}

    # Create a JSON object of the person's identity
    def to_json_identity(self):
        return {'lastname': self.lastname, 'firstname': self.firstname}
        
    # Method to debit an account
    def debit(self, sum):
        self.account -= sum
        
    # Method to credit an account
    def credit(self, sum):
        self.account += sum
    
    # Perform a transaction between two persons
    def transaction(self, P2, sum):
        self.debit(sum)
        P2.credit(sum)
    
    # Check if the person's identity matches the input lastname and firstname
    def equals(self, lastname, firstname):
        return lastname == self.lastname and firstname == self.firstname


# Function to find a person in the persons list by last name and first name
def find(lastname, firstname):
    for person in persons:
        if(person.equals(lastname, firstname)):
            return person
    return False


# Route to print all persons and transactions
# Request example : http://localhost:5000/
@app.route("/", methods=['GET'])
def printAll():
    if request.method == 'GET':
        res = "<h1>Liste des personnes :</h1><ul>"
        for person in persons:
            res += "<li>NOM : " + person.lastname + " / PRENOM : " + person.firstname + " / SOLDE COMPTE : " + '%.2f' % person.account + "€</li>"
        res += "</ul><h1>Liste des transactions :</h1><ul>"
        for transaction in transactions:
            res += "<li>P1 : " + transaction[0].lastname + " " + transaction[0].firstname + " / P2 : " + transaction[1].lastname + " " + transaction[1].firstname + " / DATE : " + transaction[2].strftime("%Y-%m-%d %H:%M:%S") + " / SOMME : " + '%.2f' % transaction[3] + "€ / HASH : " + transaction[4] +"</li>"
        return res+"</ul>"
    else:
        return "Invalid request method"


# Route to import a csv file of persons
# Request example : curl -X POST -F 'file=@persons.csv' http://localhost:5000/import
@app.route('/import', methods=['POST'])
def import_data():
    if request.method == 'POST':
        file = request.files['file']
        file_bytes = file.read()
        f = BytesIO(file_bytes)
        f = TextIOWrapper(f)
        reader = csv.reader(f, delimiter=';')
        
        for row in reader:
            persons.append(Person(row[0], row[1], float(row[2])))
        
        return jsonify("CSV file imported with success !")
    else:
        return "Invalid request method"


# Route to add a person
# Request example : curl -X POST -H "Content-Type: application/json" -d '{"P": {"lastname": "Delarue", "firstname": "Marc", "account": 700}}' http://localhost:5000/add-person
@app.route('/add-person', methods=['POST'])
def add_person():
    if request.method == 'POST':
        data = request.get_json()
        P = data['P']
        persons.append(Person(P['lastname'], P['firstname'], P['account']))
        return jsonify("Person added with success !")
    else:
        return "Invalid request method"


# Route to delete a person
# Request example : curl -X DELETE -H "Content-Type: application/json" -d '{"P": {"lastname": "Coutarel", "firstname": "Allan", "account": 800}}' http://localhost:5000/delete-person
@app.route('/delete-person', methods=['DELETE'])
def delete_person():
    if request.method == 'DELETE':
        data = request.get_json()
        P = data['P']
        for idx, person in enumerate(persons):
            if person.lastname == P['lastname'] and person.firstname == P['firstname'] and person.account == P['account']:
                persons.pop(idx)
                return jsonify("Person deleted with success !")
        return jsonify("Person not found !")
    else:
        return "Invalid request method"


# Route to print all transactions sorted by date
# Request example : curl -X GET "http://localhost:5000/print-transactions"
# In navigator : http://localhost:5000/print-transactions
@app.route('/print-transactions', methods=['GET'])
def print_transactions():
    if request.method == 'GET':
        sorted_transactions = sorted(transactions, key=lambda transaction: transaction[2])
        res = "<h1>Liste des transactions triées par odre chronologique :</h1><ul>"
        for transaction in sorted_transactions:
            res += "<li>P1 : " + transaction[0].lastname + " " + transaction[0].firstname + " / P2 : " + transaction[1].lastname + " " + transaction[1].firstname + " / DATE : " + transaction[2].strftime("%Y-%m-%d %H:%M:%S") + " / SOMME : " + '%.2f' % transaction[3] + "€ / HASH : " + transaction[4] +"</li>"
        return res+"</ul>"
    else:
        return "Invalid request method"


# Route to print all transactions of a person, sorted by date
# Request example : curl -X GET "http://localhost:5000/print-person-transactions?lastname=Dupont&firstname=Jean"
# In navigator : http://localhost:5000/print-person-transactions?lastname=Dupont&firstname=Jean
@app.route('/print-person-transactions', methods=['GET'])
def print_person_transactions():
    if request.method == 'GET':
        lastname = request.args.get('lastname')
        firstname = request.args.get('firstname')
        
        person = find(lastname, firstname)
        
        if person != False:
            person_transactions = []
            
            for transaction in transactions:
                if transaction[0].lastname == person.lastname and transaction[0].firstname == person.firstname:
                    person_transactions.append(transaction)
                elif transaction[1].lastname == person.lastname and transaction[1].firstname == person.firstname:
                    person_transactions.append(transaction)
            
            sorted_person_transactions = sorted(person_transactions, key=lambda transaction: transaction[2])
            res = "<h1>Liste des transactions triées par odre chronologique liées à " + person.lastname + " " + person.firstname + " :</h1><ul>"
            for transaction in sorted_person_transactions:
                res += "<li>P1 : " + transaction[0].lastname + " " + transaction[0].firstname + " / P2 : " + transaction[1].lastname + " " + transaction[1].firstname + " / DATE : " + transaction[2].strftime("%Y-%m-%d %H:%M:%S") + " / SOMME : " + '%.2f' % transaction[3] + "€ / HASH : " + transaction[4] +"</li>"
            return res+"</ul>"
        else:
            return "Invalid request, need valid lastname and firstname"
    else:
        return "Invalid request method"


# Route to perform a transaction between 2 persons
# Request example : curl -X PUT -H "Content-Type: application/json" -d '{"P1": {"lastname": "Dupont", "firstname": "Jean"}, "P2": {"lastname": "Burger", "firstname": "Dylan"}, "t": "2023-01-12 15:04:22", "s": 50}' http://localhost:5000/do-transaction
# curl -X PUT -H "Content-Type: application/json" -d '{"P1": {"lastname": "Burger", "firstname": "Dylan"}, "P2": {"lastname": "Dupont", "firstname": "Jean"}, "t": "2023-01-12 17:10:52", "s": 20}' http://localhost:5000/do-transaction
@app.route("/do-transaction", methods=['PUT'])
def do_transaction():
    if request.method == 'PUT':
        data = request.get_json()
        
        P1 = data['P1']
        person1 = find(P1['lastname'], P1['firstname'])
            
        P2 = data['P2']
        person2 = find(P2['lastname'], P2['firstname'])
        
        if person1 != False and person2 != False:
        
            t = datetime.strptime(data['t'], "%Y-%m-%d %H:%M:%S")
            s = data['s']
            
            transaction_data = (person1, person2, t, s)
            h = hashlib.sha256(str(transaction_data).encode()).hexdigest()
            transactions.append((person1, person2, t, s, h))
            transactions_json = {'P1': person1.to_json(), 'P2': person2.to_json(), 't': t, 's': s, 'h': h}
            person1.transaction(person2, s)
            return jsonify(transactions_json)
        else:
            return "Invalid request, need valid persons"
    else:
        return "Invalid request method"


# Route to print the account of a person
# Request example : curl -X GET "http://localhost:5000/print-account?lastname=Dupont&firstname=Jean"
# In navigator : http://localhost:5000/print-account?lastname=Dupont&firstname=Jean
@app.route('/print-account', methods=['GET'])
def print_account():
    if request.method == 'GET':
        lastname = request.args.get('lastname')
        firstname = request.args.get('firstname')
        
        person = find(lastname, firstname)
        
        if person != False:
            account = person.account
            return "<p>Solde de " + person.lastname + " " + person.firstname + " : " + '%.2f' % account + "€</p>"
        else:
            return "Invalid request, need valid lastname and firstname"
    else:
        return "Invalid request method"

    
# Route to verify the integrity of data
# curl -X POST -H "Content-Type: application/json" -d '{"P1": {"lastname": "Burger", "firstname": "Dylan"}, "P2": {"lastname": "Dupont", "firstname": "Jean"}, "t": "2023-01-12 17:10:52", "s": 20}' http://localhost:5000/verify-data
@app.route("/verify-data", methods=['POST'])
def verify_data():
    if request.method == 'POST':
        data = request.get_json()
        
        P1 = data['P1']
        person1 = find(P1['lastname'], P1['firstname'])
        
        P2 = data['P2']
        person2 = find(P2['lastname'], P2['firstname'])
        
        if person1 != False and person2 != False:
        
            t = datetime.strptime(data['t'], "%Y-%m-%d %H:%M:%S")
            s = data['s']
            
            transaction_data = (person1, person2, t, s)
            h = hashlib.sha256(str(transaction_data).encode()).hexdigest()
            
            for transaction in transactions : 
                if transaction[0].lastname == person1.lastname and transaction[0].firstname == person1.firstname and transaction[1].lastname == person2.lastname and transaction[1].firstname == person2.firstname and transaction[3] == s and transaction[4] == h:
                    return "Data are valid"
            return "Data are not valid"
        
        else:
            return "Invalid request, need valid persons"
    else:
        return "Invalid request method"

    
# Main function that run the flask app; can also check syntax of the app with check_syntax argument
if __name__ == "__main__":
    if len(sys.argv) > 1 :
        if sys.argv[1] == "check_syntax":
            print("Build [ OK ]")
            exit(0)
        else:
            print("Passed argument not supported ! Supported argument : check_syntax")
            exit(1)
    app.run(debug=True)
