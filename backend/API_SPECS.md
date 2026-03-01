# API Specifications

## Base URL
```
http://localhost:8000
```

## Endpoints

### GET /search

Search for research papers on arXiv.

**Query Parameters:**
- `query` (string, required) - Search keywords
- `max_results` (integer, optional) - Maximum number of results (default: 10)

**Request Example:**
```
GET http://localhost:8000/search?query=RAG&max_results=5
```

**Response:**
```json
{
  "results": [
    {
      "id": "2504.04915",
      "title": "Collab-RAG: Boosting Retrieval-Augmented Generation...",
      "summary": "Retrieval-Augmented Generation (RAG) systems...",
      "entry_id": "http://arxiv.org/abs/2504.04915v1",
      "year": 2025,
      "authors": ["Ran Xu", "Wenqi Shi", "Yuchen Zhuang"],
      "published": "2025-04-07T10:52:22+00:00"
    }
  ]
}
```

**Response Fields:**
- `id` (string) - Short arXiv ID
- `title` (string) - Paper title
- `summary` (string) - Paper abstract/summary
- `entry_id` (string) - Full arXiv URL
- `year` (integer) - Publication year
- `authors` (array of strings) - List of author names
- `published` (string) - ISO format publication date

**Status Codes:**
- `200` - Success
- `422` - Validation error (missing query parameter)
