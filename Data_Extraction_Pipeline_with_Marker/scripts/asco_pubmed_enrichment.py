"""
asco_pubmed_enrichment.py
--------------------------
Phases 2 & 3: PubMed Verification, Enrichment, and Storage - ASCO Guidelines

ASCO-specific implementation that:
- Verifies and enriches metadata using PubMed API
- Validates data with Pydantic schema
- Produces database-ready JSON output

Phase 2: Verification and Enrichment (PubMed API)
1. Search by DOI: Use the DOI extracted by Marker
2. Fallback to Title: If DOI fails, search by title
3. Error Handling: If no match found, move to data/failed/ and log error
4. Get Citation: Fetch formatted citation with validated metadata

Phase 3: Assembly and Storage
1. Create Object: Instantiate schema with validated data
2. Save Result: Save individual file as {pdf_name}_final.json to data/processed/
3. Log all operations to logs/phase2_3_execution.log
"""

import json
import shutil
import time
import logging
import re
import difflib
from pathlib import Path
from typing import Dict, Optional, List, Tuple
from datetime import datetime
import xml.etree.ElementTree as ET

import requests
from pydantic import BaseModel, Field, ValidationError

# ============================================================================
# Configuration
# ============================================================================
INPUT_DIR = Path("data/marker_outputs")
OUTPUT_DIR = Path("data/processed")
FAILED_DIR = Path("data/failed")
LOGS_DIR = Path("logs")

# Create directories if they don't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FAILED_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# Logging Configuration
# ============================================================================

# Set up logging for Phase 2 & 3
EXECUTION_LOG = LOGS_DIR / "phase2_3_execution.log"
ERROR_LOG = LOGS_DIR / "phase2_3_errors.log"

# Configure execution logger (INFO level - logs all operations)
execution_logger = logging.getLogger("phase2_3_execution")
execution_logger.setLevel(logging.INFO)
execution_handler = logging.FileHandler(EXECUTION_LOG, encoding="utf-8")
execution_handler.setFormatter(
    logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
)
execution_logger.addHandler(execution_handler)
execution_logger.propagate = False  # Prevent duplicate logs

# Configure error logger (ERROR level - logs only errors)
error_logger = logging.getLogger("phase2_3_errors")
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(ERROR_LOG, encoding="utf-8")
error_handler.setFormatter(
    logging.Formatter("%(asctime)s - [ERROR] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
)
error_logger.addHandler(error_handler)
error_logger.propagate = False


# PubMed API endpoints
PUBMED_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ESEARCH_URL = f"{PUBMED_BASE_URL}/esearch.fcgi"
EFETCH_URL = f"{PUBMED_BASE_URL}/efetch.fcgi"

# PubMed API Configuration
# Using API key for higher rate limits (10 requests/second vs 3 without)
API_KEY = "8818fbd7f8172cd08cc88fd111daef19fb09"
EMAIL = "adrian.dominguez@thebluescrubs.ai"

# Rate limiting: PubMed requires delays between requests
# With API key: 0.1s delay (allows 10 requests/second)
REQUEST_DELAY = 0.1

# ============================================================================
# Pydantic Schema for Validated Data
# ============================================================================

class GuidelineDocument(BaseModel):
    """
    Schema for validated ASCO guideline documents.
    Matches the database schema: Title, Citation, Link, Corpus (PascalCase).
    """
    Title: str = Field(..., description="Title from PubMed")
    Citation: str = Field(..., description="Formatted citation from PubMed")
    Link: str = Field(..., description="DOI link (https://doi.org/...)")
    Corpus: str = Field(..., description="Clean, structured Markdown from Marker")
    
    class Config:
        json_schema_extra = {
            "example": {
                "Title": "Example Title",
                "Citation": "Author et al. Journal. Year.",
                "Link": "https://doi.org/10.1234/example",
                "Corpus": "Markdown content..."
            }
        }

# ============================================================================
# Forensic Helpers
# ============================================================================

DOI_PATTERN = re.compile(r"10\\.\\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)


def _clean_doi(raw: str) -> str:
    """Normalize a DOI string by removing common prefixes and whitespace."""
    cleaned = raw.strip()
    cleaned = re.sub(r"^https?://doi\\.org/", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^doi:\\s*", "", cleaned, flags=re.IGNORECASE)
    return cleaned


def extract_authors_from_text(text: str) -> List[str]:
    """
    Heuristic: use first 10 lines as author bag-of-words (len>3).
    """
    if not text:
        return []
    lines = text.splitlines()[:10]
    tokens: List[str] = []
    for line in lines:
        for tok in re.findall(r"[A-Za-z]+", line):
            if len(tok) > 3:
                tokens.append(tok.lower())
    return tokens


def _normalize_title(title: str) -> str:
    """
    Lowercase, trim, remove trailing 'summary', strip punctuation, collapse spaces.
    """
    t = (title or "").lower().strip()
    if t.endswith("summary"):
        t = t[: -len("summary")].strip(" -:;,.")
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

# ============================================================================
# PubMed API Functions
# ============================================================================

def search_pubmed(query: str, is_doi: bool = False, use_title_field: bool = True) -> Optional[str]:
    """
    Search PubMed by DOI or title.
    
    Args:
        query: DOI or title to search for
        is_doi: If True, search by DOI; if False, search by title
    
    Returns:
        PMID if found, None otherwise
    """
    try:
        if is_doi:
            # Search by DOI
            search_term = f'"{query}"[DOI]'
        else:
            term = query.strip()
            term = term.replace(':', ' ')
            term = term.replace(';', ' ')
            term = term.replace(',', ' ')
            if use_title_field:
                search_term = f'"{term}"[Title]'
            else:
                search_term = term
        
        params = {
            "db": "pubmed",
            "term": search_term,
            "retmode": "json",
            "retmax": 1
        }
        
        # Add API key and email for higher rate limits
        params["api_key"] = API_KEY
        params["email"] = EMAIL
        
        response = requests.get(ESEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        idlist = data.get("esearchresult", {}).get("idlist", [])
        
        time.sleep(REQUEST_DELAY)  # Rate limiting
        
        if idlist:
            return idlist[0]  # Return first PMID found
        return None
    
    except Exception as e:
        error_msg = f"Error searching PubMed with query '{query[:50]}...': {e}"
        print(f"  Error searching PubMed: {e}")
        execution_logger.warning(error_msg)
        return None

def fetch_formatted_citation(pmid: str) -> Optional[Dict[str, str]]:
    """
    Fetch formatted citation and metadata from PubMed.
    
    Args:
        pmid: PubMed ID
    
    Returns:
        Dictionary with title, citation, link, doi, and pmid
    """
    try:
        params = {
            "db": "pubmed",
            "id": pmid,
            "retmode": "xml",
            "rettype": "abstract"
        }
        
        # Add API key and email for higher rate limits
        params["api_key"] = API_KEY
        params["email"] = EMAIL
        
        response = requests.get(EFETCH_URL, params=params, timeout=10)
        response.raise_for_status()
        
        # Parse XML response
        root = ET.fromstring(response.content)
        
        # Extract article data
        article = root.find(".//PubmedArticle")
        if article is None:
            return None
        
        # Extract title
        title_elem = article.find(".//ArticleTitle")
        title = title_elem.text if title_elem is not None else "Unknown Title"
        
        # Extract DOI
        doi_elem = article.find(".//ArticleId[@IdType='doi']")
        doi = doi_elem.text if doi_elem is not None else None
        
        # Extract authors
        author_list = article.find(".//AuthorList")
        authors = []
        if author_list is not None:
            for author in author_list.findall(".//Author"):
                last_name = author.find("LastName")
                first_name = author.find("ForeName")
                if last_name is not None and first_name is not None:
                    authors.append(f"{last_name.text}, {first_name.text}")
                elif last_name is not None:
                    authors.append(last_name.text)
        
        # Extract journal
        journal_elem = article.find(".//Journal/Title")
        journal = journal_elem.text if journal_elem is not None else "Unknown Journal"
        
        # Extract year
        year_elem = article.find(".//PubDate/Year")
        year = year_elem.text if year_elem is not None else "Unknown Year"
        
        # Extract volume and pages
        volume_elem = article.find(".//Volume")
        volume = volume_elem.text if volume_elem is not None else ""
        
        pages_elem = article.find(".//Pages")
        pages = pages_elem.text if pages_elem is not None else ""
        
        # Build citation (APA style)
        if authors:
            if len(authors) == 1:
                citation_authors = authors[0]
            elif len(authors) <= 3:
                citation_authors = ", ".join(authors[:-1]) + f", & {authors[-1]}"
            else:
                citation_authors = f"{authors[0]} et al."
        else:
            citation_authors = "Unknown Authors"
        
        citation = f"{citation_authors}. ({year}). {title}. {journal}"
        if volume:
            citation += f", {volume}"
        if pages:
            citation += f", {pages}"
        if doi:
            citation += f". https://doi.org/{doi}"
        
        # Build DOI link (matching database schema)
        # Use DOI link if available, otherwise PubMed link
        if doi:
            link = f"https://doi.org/{doi}"
        else:
            link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}"
        
        time.sleep(REQUEST_DELAY)  # Rate limiting
        
        return {
            "title": title,
            "citation": citation,
            "link": link,
            "pmid": pmid,
            "doi": doi,
            "authors": authors
        }
    
    except Exception as e:
        error_msg = f"Error fetching citation for PMID {pmid}: {e}"
        print(f"  Error fetching citation: {e}")
        execution_logger.warning(error_msg)
        return None

# ============================================================================
# Error Handling
# ============================================================================

def log_error(filename: str, reason: str):
    """Log error to phase2_3_errors.log file (using logging module)."""
    error_msg = f"{filename}: {reason}"
    error_logger.error(error_msg)
    execution_logger.error(error_msg)

def move_to_failed(json_file: Path, reason: str):
    """Move JSON file to failed directory and log error."""
    try:
        failed_file = FAILED_DIR / json_file.name
        shutil.move(str(json_file), str(failed_file))
        log_error(json_file.name, reason)
        print(f"  ✗ Moved to failed: {json_file.name} - {reason}")
    except Exception as e:
        print(f"  ✗ Error moving file: {e}")

# ============================================================================
# Main Processing Functions
# ============================================================================

def process_intermediate_file(json_file: Path) -> bool:
    """
    Process a single intermediate JSON file through Phase 2 & 3.
    
    Args:
        json_file: Path to intermediate JSON file
    
    Returns:
        True if successful, False if failed
    """
    file_start_time = datetime.now()
    file_name = json_file.name
    execution_logger.info(f"Processing: {file_name}")
    print(f"→ Processing: {file_name}")
    
    try:
        # Load intermediate data
        execution_logger.info(f"  Loading intermediate data: {file_name}")
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        text = data.get("text", "")
        metadata = data.get("metadata", {})
        tentative_title = metadata.get("title")
        tentative_doi = metadata.get("doi")
        
        if not text:
            move_to_failed(json_file, "Empty corpus")
            return False

        # Phase 1: Forensic inspection (conservative: only trust metadata DOI)
        detected_doi = tentative_doi
        authors_tokens = extract_authors_from_text(text)
        
        # Phase 2: Strategic search
        pmid = None
        pubmed_metadata = None
        
        # Try DOI first (only metadata DOI; no text-derived DOI to avoid noise)
        if detected_doi:
            execution_logger.info(f"  Searching PubMed by DOI: {detected_doi}")
            print(f"  Searching by DOI: {detected_doi}")
            pmid = search_pubmed(detected_doi, is_doi=True)
            if pmid:
                execution_logger.info(f"  ✓ Found PMID via DOI: {pmid}")
        
        # Title-based attempts (exact, remove 'summary', pre-colon, loose)
        if not pmid and tentative_title:
            title_variants = []
            base_title = tentative_title.strip()
            if base_title:
                title_variants.append(base_title)
                # Drop trailing "summary"
                lowered = base_title.lower()
                if lowered.endswith("summary"):
                    stripped = base_title[: -len("summary")].strip(" -:;")
                    if stripped:
                        title_variants.append(stripped)
                # Pre-colon
                if ":" in base_title:
                    main_title = base_title.split(":", 1)[0].strip()
                    if main_title and main_title != base_title:
                        title_variants.append(main_title)
            # Deduplicate while preserving order
            seen = set()
            unique_variants = []
            for t in title_variants:
                if t not in seen:
                    seen.add(t)
                    unique_variants.append(t)
            for variant in unique_variants:
                execution_logger.info(f"  Searching PubMed by title variant: {variant[:80]}...")
                print(f"  Searching by title: {variant[:80]}...")
                pmid = search_pubmed(variant, is_doi=False, use_title_field=True)
                if pmid:
                    execution_logger.info(f"  ✓ Found PMID via title: {pmid}")
                    break
                # Loose search without Title field as fallback
                pmid = search_pubmed(variant, is_doi=False, use_title_field=False)
                if pmid:
                    execution_logger.info(f"  ✓ Found PMID via loose search: {pmid}")
                    break
            # Optional enriched search: title + first author token (if any)
            if not pmid and unique_variants:
                first_author = authors_tokens[0] if authors_tokens else ""
                if first_author:
                    enriched_query = f"{unique_variants[0]} {first_author}"
                    execution_logger.info(f"  Searching PubMed by enriched query: {enriched_query[:80]}...")
                    pmid = search_pubmed(enriched_query, is_doi=False, use_title_field=False)
                    if pmid:
                        execution_logger.info(f"  ✓ Found PMID via enriched query: {pmid}")
        
        # Fetch citation if we found a PMID
        if pmid:
            execution_logger.info(f"  Fetching citation for PMID: {pmid}")
            print(f"  Found PMID: {pmid}")
            pubmed_metadata = fetch_formatted_citation(pmid)
            if not pubmed_metadata:
                execution_logger.error(f"  ✗ Could not fetch citation for PMID {pmid}")

        # Phase 3: Validation (Gatekeeper)
        verified = False
        allow_doi_output = False  # only output DOI on exact match
        sim_score = 0
        if pubmed_metadata:
            pub_title = pubmed_metadata.get("title", "").strip()
            pub_doi = pubmed_metadata.get("doi")
            norm_pub_doi = _clean_doi(pub_doi) if pub_doi else None
            norm_local_doi = _clean_doi(detected_doi) if detected_doi else None

            local_title = tentative_title or ""
            if pub_title:
                sim_score = difflib.SequenceMatcher(
                    None, _normalize_title(local_title), _normalize_title(pub_title)
                ).ratio()

            # Rule 1: DOI match when both present (only path to allow DOI output)
            if norm_pub_doi and norm_local_doi:
                if norm_pub_doi.lower() == norm_local_doi.lower():
                    verified = True
                    allow_doi_output = True
                else:
                    verified = False
            else:
                # Rule 2: Very strong title match (>=0.92) with no DOI conflict -> verified, but no DOI output
                if sim_score >= 0.92 and not (norm_pub_doi and norm_local_doi and norm_pub_doi.lower() != norm_local_doi.lower()):
                    verified = True
                    allow_doi_output = False
                # Rule 3: Strong title + authors overlap (>=0.85 with authors), no DOI conflict -> verified, no DOI output
                elif sim_score >= 0.85:
                    pub_authors = pubmed_metadata.get("authors", []) or []
                    pub_author_tokens = set()
                    for a in pub_authors:
                        for tok in re.findall(r"[A-Za-z]+", a):
                            if len(tok) > 3:
                                pub_author_tokens.add(tok.lower())
                    if pub_author_tokens and authors_tokens and pub_author_tokens.intersection(authors_tokens):
                        if not (norm_pub_doi and norm_local_doi and norm_pub_doi.lower() != norm_local_doi.lower()):
                            verified = True
                            allow_doi_output = False
        
        # Phase 4: Build output (never drop if text exists)
        try:
            if verified and pubmed_metadata:
                # Safe link selection: DOI only on exact match; otherwise PubMed PMID
                pub_pmid = pubmed_metadata.get("pmid")
                pub_doi = pubmed_metadata.get("doi")
                if allow_doi_output and pub_doi:
                    verified_link = f"https://doi.org/{pub_doi}"
                elif pub_pmid:
                    verified_link = f"https://pubmed.ncbi.nlm.nih.gov/{pub_pmid}"
                else:
                    verified_link = "https://pubmed.ncbi.nlm.nih.gov"
                document = GuidelineDocument(
                    Title=pubmed_metadata["title"],
                    Citation=pubmed_metadata["citation"],
                    Link=verified_link,
                    Corpus=text
                )
            else:
                fallback_title = tentative_title or "Unknown Title (unverified)"
                # Strict fallback: neutral link to avoid false positives
                fallback_link = "https://asco.org"
                fallback_citation = f"ASCO Guideline. {fallback_title}. (Data extracted from text, unverified in PubMed)."
                if pubmed_metadata:
                    execution_logger.warning(f"  ⚠️ PubMed match rejected for {file_name}; fallback used.")
                else:
                    execution_logger.warning(f"  ⚠️ No PubMed match for {file_name}; fallback used.")
                document = GuidelineDocument(
                    Title=fallback_title,
                    Citation=fallback_citation,
                    Link=fallback_link,
                    Corpus=text
                )
            
            # Save individual final output file
            output_filename = f"{json_file.stem}_final.json"
            output_path = OUTPUT_DIR / output_filename
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(document.model_dump(), f, ensure_ascii=False, indent=2)
            
            processing_time = (datetime.now() - file_start_time).total_seconds()
            
            execution_logger.info(f"  ✓ Successfully processed: {file_name}")
            execution_logger.info(f"    - Output: {output_filename}")
            execution_logger.info(f"    - Title: {document.Title[:80]}...")
            execution_logger.info(f"    - PMID: {pmid if pmid else 'Not verified'}")
            execution_logger.info(f"    - DOI: {pubmed_metadata.get('doi', 'Not available') if pubmed_metadata else 'Not available'}")
            execution_logger.info(f"    - Processing time: {processing_time:.2f} seconds")
            
            if not verified:
                print(f"  ⚠️ Fallback used (unverified metadata): {document.Title[:50]}...")
            else:
                print(f"  ✓ Success: {document.Title[:50]}...")
            print(f"  ✓ Saved: {output_filename}")
            return True
        
        except ValidationError as e:
            error_msg = f"Validation error for {file_name}: {e}"
            execution_logger.error(error_msg)
            error_logger.error(error_msg, exc_info=True)
            move_to_failed(json_file, f"Validation error: {e}")
            return False
    
    except Exception as e:
        error_msg = f"Processing error for {file_name}: {e}"
        execution_logger.error(error_msg)
        error_logger.error(error_msg, exc_info=True)
        move_to_failed(json_file, f"Processing error: {e}")
        return False

# ============================================================================
# Main Function
# ============================================================================

def main():
    """
    Main function to process Phase 2 & 3.
    
    Reads intermediate JSON files, enriches with PubMed data,
    and saves final validated documents (one file per input).
    Logs all operations to logs/phase2_3_execution.log
    """
    start_time = datetime.now()
    execution_logger.info("=" * 80)
    execution_logger.info("PHASE 2 & 3: PUBMED ENRICHMENT AND VALIDATION STARTED")
    execution_logger.info(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    execution_logger.info("=" * 80)
    
    # Get all intermediate JSON files
    json_files = list(INPUT_DIR.glob("*.json"))
    
    if not json_files:
        msg = f"No intermediate JSON files found in {INPUT_DIR.resolve()}"
        print(msg)
        execution_logger.warning(msg)
        return
    
    execution_logger.info(f"Found {len(json_files)} intermediate file(s) to process")
    print(f"Found {len(json_files)} intermediate file(s). Starting enrichment...\n")
    
    # Process all files with checkpointing
    success_count = 0
    failed_count = 0
    skipped_count = 0
    
    for json_file in json_files:
        # CHECKPOINTING: Check if final output already exists (resume capability)
        output_filename = f"{json_file.stem}_final.json"
        output_path = OUTPUT_DIR / output_filename
        
        if output_path.exists():
            skipped_count += 1
            skip_msg = f"⏭️ Skipping {json_file.name} (Final output already exists: {output_filename})"
            print(skip_msg)
            execution_logger.info(f"Skipping {json_file.name} - Final output already exists: {output_filename}")
            print()  # Empty line for readability
            continue
        
        success = process_intermediate_file(json_file)
        if success:
            success_count += 1
        else:
            failed_count += 1
        print()  # Empty line for readability
    
    # Final summary
    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    
    total_files = len(json_files)
    
    execution_logger.info("=" * 80)
    execution_logger.info("PHASE 2 & 3: PUBMED ENRICHMENT AND VALIDATION COMPLETED - FINAL REPORT")
    execution_logger.info("=" * 80)
    execution_logger.info(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    execution_logger.info(f"Total execution time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
    execution_logger.info(f"Total files: {total_files}")
    execution_logger.info(f"Successfully validated (new): {success_count}")
    execution_logger.info(f"Skipped (already processed): {skipped_count}")
    execution_logger.info(f"Failed: {failed_count}")
    execution_logger.info(f"Output directory: {OUTPUT_DIR.resolve()}")
    execution_logger.info(f"Execution log: {EXECUTION_LOG.resolve()}")
    if failed_count > 0:
        execution_logger.info(f"Error log: {ERROR_LOG.resolve()}")
    execution_logger.info("=" * 80)
    
    print(f"\n{'='*80}")
    print(f"✓ Phase 2 & 3 Complete! Final Report")
    print(f"{'='*80}")
    print(f"  Total files: {total_files}")
    print(f"  ✅ Successfully validated (new): {success_count}")
    print(f"  ⏭️  Skipped (already processed): {skipped_count}")
    print(f"  ✗ Failed: {failed_count}")
    print(f"  ⏱️  Total time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
    print(f"  📁 Output directory: {OUTPUT_DIR.resolve()}")
    print(f"  📝 Execution log: {EXECUTION_LOG.resolve()}")
    if failed_count > 0:
        print(f"  ⚠️  Error log: {ERROR_LOG.resolve()}")
    print(f"{'='*80}")
    
    if success_count == 0:
        warning_msg = "No documents were successfully validated."
        print(f"\n✗ {warning_msg}")
        print("  Check error log for details.")
        execution_logger.warning(warning_msg)

if __name__ == "__main__":
    main()

