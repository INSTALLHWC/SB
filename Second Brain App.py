import os
import sys
import json
import subprocess
import importlib.util
from pathlib import Path

# ----------------------------
# Auto-install dependencies if missing
# ----------------------------
def install_if_missing(package):
    if importlib.util.find_spec(package) is None:
        print(f"Installing missing package: {package}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except Exception as e:
            print(f"⚠️ Could not install {package}: {e}")

# Try installing core dependencies
for pkg in ["numpy", "sentence-transformers"]:
    install_if_missing(pkg)

# Import safely
try:
    import numpy as np
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("\n❌ Required packages missing and couldn't be installed. Exiting.")
    sys.exit(1)

# ----------------------------
# Safe Data Directory
# ----------------------------
def get_data_file():
    home = Path.home()
    data_dir = home / ".second_brain"
    data_dir.mkdir(exist_ok=True)
    return data_dir / "notes.json"

DATA_FILE = get_data_file()

# ----------------------------
# Second Brain Class
# ----------------------------
class SecondBrain:
    def __init__(self):
        print("Loading AI model (first run may take a moment)...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.notes = []
        self.load_notes()

    def load_notes(self):
        if DATA_FILE.exists():
            with open(DATA_FILE, "r") as f:
                self.notes = json.load(f)
        else:
            self.notes = []

    def save_notes(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.notes, f, indent=4)

    def add_note(self, text):
        embedding = self.model.encode(text).tolist()
        self.notes.append({
            "text": text,
            "embedding": embedding
        })
        self.save_notes()
        print("✅ Note saved!")  # emoji in quotes

    def search_notes(self, query):
        if not self.notes:
            print("No notes found.")
            return

        query_emb = self.model.encode(query)
        scores = []
        for note in self.notes:
            emb = np.array(note["embedding"])
            similarity = self.cosine_similarity(query_emb, emb)
            scores.append((similarity, note["text"]))

        scores.sort(reverse=True, key=lambda x: x[0])

        print("\n🔍 Top Matches:")
        for score, text in scores[:5]:
            print(f"\nScore: {score:.3f}")
            print(text)

    @staticmethod
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ----------------------------
# Main CLI
# ----------------------------
def main():
    brain = SecondBrain()

    while True:
        print("\n=== Second Brain ===")
        print("1. Add Note")
        print("2. Search Notes")
        print("3. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            text = input("\nWrite your note:\n> ")
            brain.add_note(text)

        elif choice == "2":
            query = input("\nSearch:\n> ")
            brain.search_notes(query)

        elif choice == "3":
            print("Exiting Second Brain...")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
