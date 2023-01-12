from flask import Flask, jsonify, request

class Person:
    def __init__(self, nom, prenom, solde):
        self._nom = nom
        self._prenom = prenom
        self._solde = solde
