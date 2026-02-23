class Paper:
    def __init__(self, title, authors, year, publisher, doi):
        self.title = title
        self.authors = authors
        self.year = year
        self.publisher = publisher
        self.doi = doi
        self.objective = {"content": "", "page": ""}
        self.methodology = {"content": "", "page": ""}
        self.conclusion = {"content": "", "page": ""}
        self.tags = []
    
    def to_dict(self):
        return {
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "publisher": self.publisher,
            "doi": self.doi,
            "objective": self.objective,
            "methodology": self.methodology,
            "conclusion": self.conclusion,
            "tags": self.tags
        }
    
    @staticmethod
    def from_dict(data):
        paper = Paper(
            data["title"],
            data["authors"],
            data["year"],
            data["publisher"],
            data["doi"]
        )
        paper.objective = data.get("objective", {"content": "", "page": ""})
        paper.methodology = data.get("methodology", {"content": "", "page": ""})
        paper.conclusion = data.get("conclusion", {"content": "", "page": ""})
        paper.tags = data.get("tags", [])
        return paper
    
    def get_short_title(self):
        author_last = self.authors.split(",")[0].strip() if self.authors else "Unknown"
        return f"{author_last} {self.year}"
    
    def is_section_filled(self, section):
        return bool(getattr(self, section)["content"])
