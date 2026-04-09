import streamlit as st
import pandas as pd

st.set_page_config(page_title="Anti-Fraude", layout="wide")

st.title("🕵️‍♂️ Détection de fraude - Démo")

# Base de données de démonstration
data = [
    {"id": 1, "nom": "Dupont", "tel": "0600000001", "iban": "FR761111", "adresse": "Paris", "garage": "AutoGlass Pro"},
    {"id": 2, "nom": "Martin", "tel": "0600000002", "iban": "FR762222", "adresse": "Lyon", "garage": "Speed Repair"},
    {"id": 3, "nom": "Durand", "tel": "0600000001", "iban": "FR763333", "adresse": "Paris", "garage": "AutoGlass Pro"},
    {"id": 4, "nom": "Petit", "tel": "0600000004", "iban": "FR761111", "adresse": "Marseille", "garage": "Glass Expert"},
    {"id": 5, "nom": "Moreau", "tel": "0600000005", "iban": "FR765555", "adresse": "Lille", "garage": "Speed Repair"},
    {"id": 6, "nom": "Simon", "tel": "0600000006", "iban": "FR766666", "adresse": "Paris", "garage": "AutoGlass Pro"},
    {"id": 7, "nom": "Laurent", "tel": "0600000007", "iban": "FR767777", "adresse": "Paris", "garage": "AutoGlass Pro"},
    {"id": 8, "nom": "Michel", "tel": "0600000008", "iban": "FR768888", "adresse": "Nice", "garage": "Sud Pare-Brise"},
    {"id": 9, "nom": "Garcia", "tel": "0600000001", "iban": "FR769999", "adresse": "Paris", "garage": "AutoGlass Pro"},
    {"id": 10, "nom": "Roux", "tel": "0600000010", "iban": "FR761111", "adresse": "Paris", "garage": "AutoGlass Pro"},
]

df = pd.DataFrame(data)

st.sidebar.header("🔎 Analyse")

seuil = st.sidebar.slider("Seuil d'alerte", 0, 100, 50)

# Fonction de calcul du score
def calcul_score(dossier, df):
    score = 0
    liens = []

    for _, autre in df.iterrows():
        if dossier["id"] == autre["id"]:
            continue

        if dossier["iban"] == autre["iban"]:
            score += 50
            liens.append(f"IBAN commun avec dossier {autre['id']}")

        if dossier["tel"] == autre["tel"]:
            score += 30
            liens.append(f"Téléphone commun avec dossier {autre['id']}")

        if dossier["adresse"] == autre["adresse"]:
            score += 10
            liens.append(f"Adresse commune avec dossier {autre['id']}")

        if dossier["garage"] == autre["garage"]:
            score += 15
            liens.append(f"Garage commun avec dossier {autre['id']}")

    return score, liens

# Affichage des données
for _, row in df.iterrows():
    score, liens = calcul_score(row, df)

    with st.container():
        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader(f"📄 Dossier {row['id']} - {row['nom']}")
            st.write(f"📞 Téléphone : {row['tel']}")
            st.write(f"🏦 IBAN : {row['iban']}")
            st.write(f"🏠 Adresse : {row['adresse']}")
            st.write(f"🔧 Garage : {row['garage']}")

        with col2:
            st.metric("Score fraude", score)

            if score >= seuil:
                st.error("⚠️ DOSSIER SUSPECT")
            else:
                st.success("✅ OK")

        if liens:
            with st.expander("🔗 Voir les liens détectés"):
                for lien in liens:
                    st.write("-", lien)

    st.markdown("---")u\\0369+
