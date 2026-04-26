from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

REGISTER_URL = "/api/auth/register/abonne/"


class AbonneRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    # ── CAS SUCCÈS ──────────────────────────────────────────────────────────

    def test_inscription_reussie(self):
        """Inscription correcte : compte créé, rôle abonné, actif immédiatement."""
        res = self.client.post(REGISTER_URL, {
            "username": "jean_test",
            "email": "jean@test.ht",
            "password1": "MonMotDePasse!1",
            "password2": "MonMotDePasse!1",
        }, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("detail", res.data)

        user = User.objects.get(username="jean_test")
        self.assertEqual(user.role, "abonne")
        self.assertTrue(user.is_active, "Un abonné doit être actif immédiatement")
        self.assertTrue(user.check_password("MonMotDePasse!1"))

    def test_inscription_reussie_avec_champs_optionnels(self):
        """Inscription avec téléphone et sexe optionnels."""
        res = self.client.post(REGISTER_URL, {
            "username": "marie_test",
            "email": "marie@test.ht",
            "password1": "Secret123!",
            "password2": "Secret123!",
            "phone": "+50934567890",
            "sexe": "femme",
        }, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="marie_test")
        self.assertEqual(user.phone, "+50934567890")
        self.assertEqual(user.sexe, "femme")

    # ── CAS ERREUR — MOTS DE PASSE ──────────────────────────────────────────

    def test_mots_de_passe_differents(self):
        """password1 ≠ password2 doit retourner une erreur 400."""
        res = self.client.post(REGISTER_URL, {
            "username": "paul_test",
            "email": "paul@test.ht",
            "password1": "MotDePasse1!",
            "password2": "MotDePasse2!",
        }, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="paul_test").exists())

    def test_password2_vide(self):
        """password2 absent doit retourner une erreur 400."""
        res = self.client.post(REGISTER_URL, {
            "username": "pierre_test",
            "email": "pierre@test.ht",
            "password1": "MotDePasse1!",
            "password2": "",
        }, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="pierre_test").exists())

    # ── CAS ERREUR — DOUBLONS ───────────────────────────────────────────────

    def test_username_deja_utilise(self):
        """Deux comptes avec le même username : erreur 400."""
        User.objects.create_user(
            username="doublon_user",
            email="original@test.ht",
            password="qqchose123",
            role="abonne",
        )
        res = self.client.post(REGISTER_URL, {
            "username": "doublon_user",
            "email": "nouveau@test.ht",
            "password1": "Autre123!",
            "password2": "Autre123!",
        }, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # Un seul compte avec ce username doit exister
        self.assertEqual(User.objects.filter(username="doublon_user").count(), 1)

    def test_email_deja_utilise(self):
        """Deux comptes avec le même email : erreur 400."""
        User.objects.create_user(
            username="user_original",
            email="partage@test.ht",
            password="qqchose123",
            role="abonne",
        )
        res = self.client.post(REGISTER_URL, {
            "username": "user_nouveau",
            "email": "partage@test.ht",
            "password1": "Autre123!",
            "password2": "Autre123!",
        }, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="user_nouveau").exists())

    # ── CAS ERREUR — CHAMPS OBLIGATOIRES ────────────────────────────────────

    def test_sans_username(self):
        """Sans username : erreur 400."""
        res = self.client.post(REGISTER_URL, {
            "email": "sans_user@test.ht",
            "password1": "Abc12345!",
            "password2": "Abc12345!",
        }, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sans_email(self):
        """Sans email : erreur 400."""
        res = self.client.post(REGISTER_URL, {
            "username": "sans_email",
            "password1": "Abc12345!",
            "password2": "Abc12345!",
        }, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_invalide(self):
        """Email mal formaté : erreur 400."""
        res = self.client.post(REGISTER_URL, {
            "username": "email_invalide",
            "email": "pas-un-email",
            "password1": "Abc12345!",
            "password2": "Abc12345!",
        }, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # ── CAS ERREUR — CONNEXION APRÈS INSCRIPTION ────────────────────────────

    def test_connexion_apres_inscription(self):
        """Après inscription, le compte peut se connecter via l'endpoint JWT."""
        self.client.post(REGISTER_URL, {
            "username": "login_test",
            "email": "login@test.ht",
            "password1": "Login123!",
            "password2": "Login123!",
        }, format="json")

        token_url = "/api/auth/token/"
        res = self.client.post(token_url, {
            "username": "login_test",
            "password": "Login123!",
        }, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)
