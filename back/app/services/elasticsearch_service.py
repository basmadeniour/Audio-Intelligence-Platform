from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import numpy as np

class ElasticsearchService:
    def __init__(self, host: str = "http://localhost:9200"):
        self.es = Elasticsearch(host)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index_name = "audio_transcripts"
        self._create_index()
    
    def _create_index(self):
        index_settings = {
            "mappings": {
                "properties": {
                    "text": {
                        "type": "text",
                        "analyzer": "standard"
                    },
                    "start_time": {"type": "float"},
                    "end_time": {"type": "float"},
                    "embedding": {
                        "type": "dense_vector",
                        "dims": 384,
                        "index": True,
                        "similarity": "cosine"
                    }
                }
            }
        }
        
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name, body=index_settings)
    
    def index_segments(self, segments: List[Dict[str, Any]]):
        for i, seg in enumerate(segments):
            text = seg.get("text", "")
            if not text:
                continue
            
            embedding = self.model.encode(text).tolist()
            
            doc = {
                "text": text,
                "start_time": seg.get("start", 0),
                "end_time": seg.get("end", 0),
                "embedding": embedding
            }
            
            self.es.index(index=self.index_name, id=f"seg_{i}", body=doc)
    
    def keyword_search(self, query: str, size: int = 5) -> List[Dict]:
        search_body = {
            "query": {
                "match": {
                    "text": query
                }
            },
            "size": size
        }
        
        response = self.es.search(index=self.index_name, body=search_body)
        
        results = []
        for hit in response["hits"]["hits"]:
            results.append({
                "text": hit["_source"]["text"],
                "start_time": hit["_source"]["start_time"],
                "end_time": hit["_source"]["end_time"],
                "score": hit["_score"]
            })
        
        return results
    
    def semantic_search(self, query: str, size: int = 5) -> List[Dict]:
        query_embedding = self.model.encode(query).tolist()
        
        search_body = {
            "size": size,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": query_embedding}
                    }
                }
            }
        }
        
        response = self.es.search(index=self.index_name, body=search_body)
        
        results = []
        for hit in response["hits"]["hits"]:
            results.append({
                "text": hit["_source"]["text"],
                "start_time": hit["_source"]["start_time"],
                "end_time": hit["_source"]["end_time"],
                "score": hit["_score"]
            })
        
        return results
    
    def hybrid_search(self, query: str, size: int = 5) -> List[Dict]:
        query_embedding = self.model.encode(query).tolist()
        
        search_body = {
            "size": size,
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "text": {
                                    "query": query,
                                    "boost": 1.0
                                }
                            }
                        },
                        {
                            "script_score": {
                                "query": {"match_all": {}},
                                "script": {
                                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                                    "params": {"query_vector": query_embedding},
                                    "boost": 1.0
                                }
                            }
                        }
                    ]
                }
            }
        }
        
        response = self.es.search(index=self.index_name, body=search_body)
        
        results = []
        for hit in response["hits"]["hits"]:
            results.append({
                "text": hit["_source"]["text"],
                "start_time": hit["_source"]["start_time"],
                "end_time": hit["_source"]["end_time"],
                "score": hit["_score"]
            })
        
        return results
    
    def delete_index(self):
        if self.es.indices.exists(index=self.index_name):
            self.es.indices.delete(index=self.index_name)
    
    def clear_index(self):
        self.delete_index()
        self._create_index()
    
    def get_stats(self) -> dict:
        if not self.es.indices.exists(index=self.index_name):
            return {"exists": False}
        
        stats = self.es.indices.stats(index=self.index_name)
        return {
            "exists": True,
            "document_count": stats["indices"][self.index_name]["total"]["docs"]["count"],
            "size_bytes": stats["indices"][self.index_name]["total"]["store"]["size_in_bytes"]
        }