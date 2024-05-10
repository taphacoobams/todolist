import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


#tester la creation d'un compte avec succes puis l'effacer apres le test
def test_create_account_success(cleanup):
    response = client.post("/auth/signup", json={"email": "test_adama@example.com", "password": "testpassword"})
    assert response.status_code == 201
    assert "message" in response.json()
    assert "id" in response.json()["message"]


# Tester si un compte existe déja
def test_create_account_conflict(cleanup):
    response = client.post("/auth/signup", json={"email": "adama@example.com", "password": "testpassword"})
    assert response.status_code == 409  # Conflict

#tester la connexion avec un user existant
def test_login(cleanup):
    response_create = client.post("/auth/signup", json={"email": "test_test@example.com", "password": "testpassword"})
    assert response_create.status_code == 201

    response_login = client.post("/auth/login", data={"username": "test_test@example.com", "password": "testpassword"})
    assert response_login.status_code == 200
    assert "access_token" in response_login.json()

#tester la connexion avec un user inexistant
def test_login_user_not_exists():
    response = client.post("/auth/login", data={"username": "utilisateur_inconnu@example.com", "password": "mot_de_passe_incorrect"})

    #code d'état est 401 (Non autorisé)
    assert response.status_code == 401
    assert "Invalid Credentials" in response.json()["detail"]


















'''
1. Identification des Cas de Test :
    Test d'ajout de salle de réunion (POST)
    Test de récupération de toutes les salles de réunion (GET)
    Test de récupération d'une salle de réunion spécifique (GET/{meeting_id})
    Test de mise à jour d'une salle de réunion (PATCH/{meeting_id})
    Test de suppression d'une salle de réunion (DELETE/{meeting_id}) 
    
2. Création des Scénarios de Test :
    Scénario 1 - Ajout de Salle de Réunion :
        Créez une nouvelle salle de réunion et vérifiez si elle est correctement ajoutée.
    Scénario 2 - Récupération de Toutes les Salles de Réunion :
        Ajoutez plusieurs salles de réunion, puis récupérez-les toutes et vérifiez si la liste correspond aux salles ajoutées.
    Scénario 3 - Récupération d'une Salle de Réunion Spécifique :
        Ajoutez une salle de réunion, récupérez-la par ID et vérifiez si les données correspondent.
    Scénario 4 - Mise à Jour d'une Salle de Réunion :
        Ajoutez une salle de réunion, effectuez une mise à jour et vérifiez si les modifications sont correctement enregistrées.
    Scénario 5 - Suppression d'une Salle de Réunion :
        Ajoutez une salle de réunion, supprimez-la et assurez-vous qu'elle n'est plus présente dans la liste.
    Scénario 6 - Tester le cas où une salle n'existe pas :
        Essayer teste le cas ou recuper une salle qui n'existe pas


'''