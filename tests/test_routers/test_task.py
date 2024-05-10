
import pytest
from fastapi.testclient import TestClient
from main import app
import httpx
from fastapi.testclient import TestClient
from firebase_admin import auth
from database.firebse import authUser


client = TestClient(app)


# Test pour faire un get all sur les tâches
def test_get_all_tasks(cleanup):
    client.post("/auth/signup", json={"email": "test_adama@example.com", "password": "testpassword"})
    
    auth_token = authUser.sign_in_with_email_and_password(email="test_adama@example.com", password="testpassword")['idToken']
    auth_headers= {"Authorization": f"Bearer {auth_token}"}

    response = client.get("/task/", headers=auth_headers)
    assert response.status_code == 200

def test_get_all_tasks_unauthorized(cleanup):
    # On n'effectue aucune inscription ni authentification
    
    response = client.get("/task/")
    
    # On vérifie que le code de status est 401 (non autorisé)
    assert response.status_code == 401

#Test pour ajout
def test_add_new_task(cleanup):
    client.post("/auth/signup", json={"email": "test_adama@example.com", "password": "testpassword"})
    
    # Création des données de la tâche
    auth_token = authUser.sign_in_with_email_and_password(email="test_adama@example.com", password="testpassword")['idToken']
    auth_headers = {"Authorization": f"Bearer {auth_token}"}
    
    task_data = {
        "title": "Test Task",
    }
    response = client.post("/task/", headers=auth_headers, json=task_data)
    assert response.status_code == 201
    # Vérifier que la tâche a été créée
    new_task = response.json()
    assert new_task["title"] == task_data["title"]

    # Suppression
    task_id = response.json()["id"]

    # Supprimer la tâche après
    response = client.delete(f"/task/{task_id}", headers=auth_headers)
    assert response.status_code == 200



def test_get_task_by_id(cleanup):
    # Créer un utilisateur de test
    client.post("/auth/signup", json={"email": "test_user@example.com", "password": "testpassword"})
    auth_token = authUser.sign_in_with_email_and_password(email="test_user@example.com", password="testpassword")['idToken']
    auth_headers = {"Authorization": f"Bearer {auth_token}"}
      
    # Créer une nouvelle tâche pour le test
    task_data = {
        "title": "Test Task"
    }

    # Envoyer la requête POST avec le paramètre json
    response = client.post("/task/", headers=auth_headers, json=task_data)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Appelez la fonction get_task_by_id pour obtenir les détails de la tâche
    response = client.get(f"/task/{task_id}", headers=auth_headers)
    # Requête réussie (code de statut 200)
    assert response.status_code == 200
    # Supprimer la tâche après
    response = client.delete(f"/task/{task_id}", headers=auth_headers)
    assert response.status_code == 200

def test_delete_task_by_id(cleanup):
    # Créer un utilisateur de test
    client.post("/auth/signup", json={"email": "test_user@example.com", "password": "testpassword"})
    auth_token = authUser.sign_in_with_email_and_password(email="test_user@example.com", password="testpassword")['idToken']
    auth_headers = {"Authorization": f"Bearer {auth_token}"}

    # Créer une nouvelle tâche pour le test
    task_data = {
        "title": "Test Task"
    }
    response = client.post("/task/", headers=auth_headers, json=task_data)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Supprimer la tâche avec le task_id
    response = client.delete(f"/task/{task_id}", headers=auth_headers)

    # Suppression avec succès (code de statut 200)
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted"}

def test_patch_task_by_id(cleanup):
    # Créer un utilisateur de test
    client.post("/auth/signup", json={"email": "test_user@example.com", "password": "testpassword"})
    auth_token = authUser.sign_in_with_email_and_password(email="test_user@example.com", password="testpassword")['idToken']
    auth_headers = {"Authorization": f"Bearer {auth_token}"}

    # Créer une nouvelle tâche pour le test
    task_data = {
        "title": "Test Task"
    }
    response = client.post("/task/", headers=auth_headers, json=task_data)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Mettre à jour partiellement la tâche avec le task_id
    updated_task_data = {
        "title": "Updated Test Task",
    }
    response = client.patch(f"/task/{task_id}", headers=auth_headers, json=updated_task_data)

    # Vérifier si la tâche a été mise à jour avec succès (code de statut 200)
    assert response.status_code == 200
    # Vérifier si les données de la tâche ont été mises à jour correctement
    updated_task = response.json()
    assert updated_task["title"] == updated_task_data["title"]
    # Supprimer la tâche après
    response = client.delete(f"/task/{task_id}", headers=auth_headers)
    assert response.status_code == 200
