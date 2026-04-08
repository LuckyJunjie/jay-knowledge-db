"""ArXiv paper collector."""
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
import urllib.parse

import requests

logger = logging.getLogger(__name__)

# ArXiv API endpoint
ARXIV_API_URL = "http://export.arxiv.org/api/query"


class ArxivCollector:
    """Collector for ArXiv papers."""

    def __init__(self):
        self.data: List[Dict[str, Any]] = []
        self.last_fetch: Optional[datetime] = None

    def search(
        self,
        query: str,
        max_results: int = 10,
        sort_by: str = "relevance",
        sort_order: str = "descending",
        categories: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Search ArXiv for papers matching query.
        
        Args:
            query: Search query string
            max_results: Maximum number of results (max 30000)
            sort_by: Sort by 'relevance', 'lastUpdatedDate', 'submittedDate'
            sort_order: Sort order 'ascending' or 'descending'
            categories: ArXiv categories to filter (e.g., ['cs.AI', 'stat.ML'])
        
        Returns:
            List of paper metadata dictionaries
        """
        # Build search query
        search_query = query
        if categories:
            cat_query = " OR ".join([f"cat:{c}" for c in categories])
            search_query = f"({query}) AND ({cat_query})"
        
        # URL encode
        encoded_query = urllib.parse.quote(search_query)
        
        # Build API URL
        url = (
            f"{ARXIV_API_URL}?search_query={encoded_query}"
            f"&max_results={max_results}"
            f"&sortBy={sort_by}"
            f"&sortOrder={sort_order}"
        )
        
        logger.info(f"Searching ArXiv: {url[:100]}...")
        
        papers = []
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse XML response (ArXiv returns Atom feed)
            import xml.etree.ElementTree as ET
            
            root = ET.fromstring(response.content)
            
            # Namespace for ArXiv Atom feed
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            entries = root.findall('.//atom:entry', ns)
            
            for entry in entries:
                paper = self._parse_entry(entry)
                papers.append(paper)
            
            logger.info(f"Found {len(papers)} papers")
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch from ArXiv: {e}")
        except ET.ParseError as e:
            logger.error(f"Failed to parse ArXiv response: {e}")
        
        self.data = papers
        self.last_fetch = datetime.now()
        return papers

    def _parse_entry(self, entry) -> Dict[str, Any]:
        """Parse an ArXiv Atom entry."""
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        def get_text(element, path: str) -> str:
            el = element.find(f"atom:{path}", ns)
            return el.text if el is not None else ""
        
        # Extract categories
        categories = [
            cat.text for cat in entry.findall('atom:category', ns)
        ]
        
        # Extract authors
        authors = [
            author.find('atom:name', ns).text
            for author in entry.findall('atom:author', ns)
            if author.find('atom:name', ns) is not None
        ]
        
        # Extract PDF link
        pdf_link = ""
        for link in entry.findall('atom:link', ns):
            if link.get('title') == 'pdf':
                pdf_link = link.get('href', '')
                break
        
        return {
            'id': get_text(entry, 'id'),
            'title': get_text(entry, 'title').replace('\n', ' ').strip(),
            'summary': get_text(entry, 'summary').replace('\n', ' ').strip(),
            'authors': authors,
            'published': get_text(entry, 'published'),
            'updated': get_text(entry, 'updated'),
            'categories': categories,
            'pdf_link': pdf_link,
            'comment': get_text(entry, 'arxiv:comment'),
            'journal_ref': get_text(entry, 'arxiv:journal_ref')
        }

    def fetch_by_category(
        self,
        category: str,
        max_results: int = 10,
        date_from: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Fetch papers from specific ArXiv category.
        
        Args:
            category: ArXiv category (e.g., 'cs.AI', 'stat.ML', 'physics.gen-ph')
            max_results: Maximum number of results
            date_from: Filter by submission date (YYYYMMDD format)
        """
        query = f"cat:{category}"
        if date_from:
            query += f" AND submittedDate:[{date_from} TO 99991231]"
        
        return self.search(query, max_results, sort_by='submittedDate')

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of collected data."""
        return {
            'count': len(self.data),
            'last_fetch': self.last_fetch.isoformat() if self.last_fetch else None,
            'categories': list(set(
                cat for paper in self.data for cat in paper.get('categories', [])
            )) if self.data else []
        }


if __name__ == "__main__":
    collector = ArxivCollector()
    
    # Example: Search for machine learning papers
    papers = collector.search("machine learning", max_results=5)
    
    print(f"Found {len(papers)} papers:")
    for p in papers[:3]:
        print(f"  - {p['title'][:60]}...")
        print(f"    Authors: {', '.join(p['authors'][:2])}...")
        print(f"    Categories: {p['categories']}")
        print()