import json
import os
from paper import Paper

class Storage:
    def __init__(self, filename="papers.json"):
        self.filename = filename
        self.papers = []
        self.load()
    
    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.papers = [Paper.from_dict(p) for p in data]
    
    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.papers], f, indent=2, ensure_ascii=False)
    
    def add_paper(self, paper):
        self.papers.append(paper)
        self.save()
    
    def delete_paper(self, index):
        if 0 <= index < len(self.papers):
            self.papers.pop(index)
            self.save()
    
    def update_paper(self, index, paper):
        if 0 <= index < len(self.papers):
            self.papers[index] = paper
            self.save()
    
    def get_papers(self):
        return self.papers
