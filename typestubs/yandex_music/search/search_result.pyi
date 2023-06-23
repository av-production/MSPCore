from typing import Generic, List, TypeVar

t1 = TypeVar("t1")

class SearchResult(Generic[t1]):
    results: List[t1]
