import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

DATA_FILE = notes.json

class SecondBrain
    def __init__(self)
        print(Loading AI model...)
        self.model = SentenceTransformer(all-MiniLM-L6-v2)
        self.notes = []
        self.load_notes()

    def load_notes(self)
        if os.path.exists(DATA_FILE)
            with open(DATA_FILE, r) as f
                self.notes = json.load(f)
        else
            self.notes = []

    def save_notes(self)
        with open(DATA_FILE, w) as f
            json.dump(self.notes, f, indent=4)

    def add_note(self, text)
        embedding = self.model.encode(text).tolist()

        self.notes.append({
            text text,
            embedding embedding
        })

        self.save_notes()
        print(✅ Note saved!)

    def search_notes(self, query)
        if not self.notes
            print(No notes found.)
            return

        query_embedding = self.model.encode(query)

        scores = []
        for note in self.notes
            emb = np.array(note[embedding])
            similarity = self.cosine_similarity(query_embedding, emb)
            scores.append((similarity, note[text]))

        scores.sort(reverse=True, key=lambda x x[0])

        print(n🔍 Top Matches)
        for score, text in scores[5]
            print(fnScore {score.3f})
            print(text)

    def cosine_similarity(self, a, b)
        return np.dot(a, b)  (np.linalg.norm(a)  np.linalg.norm(b))


def main()
    brain = SecondBrain()

    while True
        print(n=== Second Brain ===)
        print(1. Add Note)
        print(2. Search Notes)
        print(3. Exit)

        choice = input(Choose )

        if choice == 1
            text = input(nWrite your noten )
            brain.add_note(text)

        elif choice == 2
            query = input(nSearchn )
            brain.search_notes(query)

        elif choice == 3
            break

        else
            print(Invalid choice.)


if __name__ == __main__
    main()