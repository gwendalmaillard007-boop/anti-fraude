import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

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
            liens.append(autre["id"])

        if dossier["tel"] == autre["tel"]:
            score += 30
            liens.append(autre["id"])

        if dossier["adresse"] == autre["adresse"]:
            score += 10
            liens.append(autre["id"])

        if dossier["garage"] == autre["garage"]:
            score += 15
            liens.append(autre["id"])

    return score, list(set(liens))

# --- Création du graphe ---

def afficher_graphe(df):
    G = nx.Graph()

    for _, row in df.iterrows():
        G.add_node(row["id"], label=row["nom"])

    for i, dossier1 in df.iterrows():
        for j, dossier2 in df.iterrows():
            if i >= j:
                continue

            if (
                dossier1["iban"] == dossier2["iban"] or
                dossier1["tel"] == dossier2["tel"] or
                dossier1["adresse"] == dossier2["adresse"] or
                dossier1["garage"] == dossier2["garage"]
            ):
                G.add_edge(dossier1["id"], dossier2["id"])

    net = Network(height="500px", width="100%", notebook=False)
    net.from_nx(G)

    net.save_graph("graph.html")
    with open("graph.html", "r", encoding="utf-8") as f:
        components.html(f.read(), height=500)

# --- Affichage ---

st.subheader("📊 Graphique des connexions")
afficher_graphe(df)

st.markdown("---")

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
            with st.expander("🔗 Voir les connexions"):
                st.write("Dossiers liés :", liens)

    st.markdown("---")
