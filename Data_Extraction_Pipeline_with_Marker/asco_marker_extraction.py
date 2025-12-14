"""
asco_marker_extraction.py
--------------------------
Phase 1: Extraction and Conversion (Marker) - ASCO Guidelines
MIGRATED TO MARKER v1.0+

ASCO-specific implementation that extracts:
- Clean, structured Markdown corpus
- Tentative metadata (title, DOI) for PubMed enrichment

This script:
1. Loads Marker models using the new v1.0+ API
2. Converts PDFs using PdfConverter to extract clean, structured Markdown corpus
3. Extracts text (corpus) and tentative metadata (title, DOI) from PDF
4. Saves intermediate JSON files to data/marker_outputs/
5. Logs all operations to logs/phase1_execution.log

"""

import json
import re
import logging
import os
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

import torch  # For device detection

# Marker v1.0+ API imports
# Try different import strategies for compatibility
try:
    from marker.models import create_model_dict
    HAS_CREATE_MODEL_DICT = True
except ImportError:
    HAS_CREATE_MODEL_DICT = False
    # Fallback to old API if create_model_dict not available
    from marker.models import load_all_models

try:
    from marker.converters.pdf import PdfConverter
    HAS_PDF_CONVERTER = True
except ImportError:
    HAS_PDF_CONVERTER = False

try:
    from marker.convert import convert_single_pdf
    HAS_CONVERT_SINGLE_PDF = True
except ImportError:
    HAS_CONVERT_SINGLE_PDF = False

from marker.settings import settings
import pypdfium2 as pdfium

# ============================================================================
# BATCH CONFIGURATION (Template - Easy to Modify)
# ============================================================================
# 
# These values control Marker's batch processing for accuracy vs speed trade-off.
# 
# For Medical Data (Current - Recommended):
#   - BATCH_MULTIPLIER = 1      # Maximum accuracy (prevents "±" → "6" errors)
#   - SURYA_BATCH_SIZE = "1"    # Maximum OCR precision when needed
# 
# For Faster Processing (Not Recommended for Medical Data):
#   - BATCH_MULTIPLIER = 4      # ~2x faster but less accurate (may cause symbol errors)
#   - SURYA_BATCH_SIZE = "4"   # Faster OCR but less precise
# 
# WARNING: Changing these values may cause symbol misrecognition errors
# (e.g., "±" being interpreted as "6") which is critical for oncology data.
# ============================================================================

BATCH_MULTIPLIER = 1          # Change this value (1, 2, 4) to adjust batch size
SURYA_BATCH_SIZE = "1"        # Change this value ("1", "2", "4") to adjust OCR batch size

# ============================================================================
# Marker Configuration (Simplified for v1.0+)
# ============================================================================

def configure_marker_for_performance():
    """
    Configure Marker settings for ASCO PDF processing with dynamic hardware detection.
    
    UNIVERSAL SCRIPT: Automatically detects GPU (Colab/Azure) or CPU (MacBook) and configures accordingly.
    
    MEDICAL DATA MODE: Uses batch_multiplier=1 for maximum accuracy, preventing symbol
    misrecognition errors (e.g., "±" being interpreted as "6" in tables).
    
    CRITICAL OPTIMIZATIONS:
    1. TORCH_DEVICE: Dynamic detection (CUDA or CPU)
       - CUDA if available (GPU mode), otherwise CPU (safe mode)
    
    2. TORCH_DTYPE: float16 for GPU (saves 50% memory, ~2x faster), float32 for CPU
       - CPU float16 is slower, so we keep float32 for CPU
    
    3. SURYA_BATCH_SIZE: Environment variable for Marker's batch processing
       - Uses configured SURYA_BATCH_SIZE (default "1" for maximum accuracy)
       - Prevents symbol misrecognition in tables (e.g., "±" → "6")
    
    4. batch_multiplier: Used in convert_single_pdf calls
       - Uses configured BATCH_MULTIPLIER (default 1 for maximum accuracy)
       - Critical for oncology data where precision is essential
    
    Returns:
        batch_multiplier value for use in processing
    
    NOTE: OCR handling is now managed internally by Marker v1.0+
    The new API automatically handles "born digital" PDFs more efficiently.
    """
    # Dynamic hardware detection: CUDA or CPU
    is_gpu = torch.cuda.is_available()
    device = "cuda" if is_gpu else "cpu"
    
    # Configure Marker settings
    settings.TORCH_DEVICE = device
    
    # Configure precision and batch settings based on device
    # CRITICAL: For medical/oncology data, we prioritize ACCURACY over speed
    # Using batch_multiplier=1 and SURYA_BATCH_SIZE=1 ensures maximum precision
    if is_gpu:
        # GPU Mode: Precision-Optimized (Medical Data)
        try:
            settings.TORCH_DTYPE = torch.float16
            dtype_str = "float16"
            precision_info = "float16 (saves 50% memory, ~2x faster)"
        except (AttributeError, ValueError):
            dtype_str = "default"
            precision_info = "default"
        
        # Use configured batch settings (template: easy to modify)
        os.environ["SURYA_BATCH_SIZE"] = SURYA_BATCH_SIZE
        batch_multiplier = BATCH_MULTIPLIER
        
        mode_msg = "🎯 Running in Precision-Optimized GPU Mode (Medical Data)"
        print(f"\n{mode_msg}")
        print(f"⚙️  Marker Configuration (v1.0+):")
        print(f"  - Device: {device.upper()}")
        print(f"  ✅ GPU detected: Using CUDA acceleration")
        print(f"  - GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'}")
        print(f"  - Precision: {precision_info}")
        print(f"  - Batch Size (SURYA_BATCH_SIZE): {SURYA_BATCH_SIZE}")
        print(f"  - Batch Multiplier: {batch_multiplier}")
        if batch_multiplier == 1 and SURYA_BATCH_SIZE == "1":
            print(f"  ⚠️  Medical Data Mode: Prioritizing accuracy over speed")
        else:
            print(f"  ⚠️  WARNING: Using batch_multiplier={batch_multiplier} may reduce accuracy")
        print(f"  - API: Marker v1.0+ (PdfConverter)")
        print()
    else:
        # CPU Mode: Safe and Stable
        dtype_str = "float32"
        precision_info = "float32 (CPU)"
        
        # Use configured batch settings (template: easy to modify)
        os.environ["SURYA_BATCH_SIZE"] = SURYA_BATCH_SIZE
        batch_multiplier = BATCH_MULTIPLIER
        
        mode_msg = "🛡️ Running in Safe CPU Mode (Slow but stable)"
        print(f"\n{mode_msg}")
        print(f"⚙️  Marker Configuration (v1.0+):")
        print(f"  - Device: {device.upper()}")
        print(f"  ⚠️  Running on CPU. This will be slow.")
        print(f"  💡 For faster results, use the Google Colab notebook.")
        print(f"  - Precision: {precision_info}")
        print(f"  - Batch Size (SURYA_BATCH_SIZE): {SURYA_BATCH_SIZE}")
        print(f"  - Batch Multiplier: {batch_multiplier}")
        if batch_multiplier == 1 and SURYA_BATCH_SIZE == "1":
            print(f"  - Medical Data Mode: Prioritizing accuracy over speed")
        else:
            print(f"  ⚠️  WARNING: Using batch_multiplier={batch_multiplier} may reduce accuracy")
        print(f"  - API: Marker v1.0+ (PdfConverter)")
        print()
    
    # Log to file if logger is available (will be initialized later in main)
    try:
        execution_logger.info("=" * 80)
        execution_logger.info("MARKER PERFORMANCE CONFIGURATION (v1.0+) - UNIVERSAL SCRIPT")
        execution_logger.info("=" * 80)
        execution_logger.info(mode_msg)
        execution_logger.info(f"Device: {device}")
        if is_gpu:
            execution_logger.info(f"GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'}")
        execution_logger.info(f"Precision: {precision_info}")
        execution_logger.info(f"Batch Size (SURYA_BATCH_SIZE): {os.environ.get('SURYA_BATCH_SIZE', 'Not set')}")
        execution_logger.info(f"Batch Multiplier: {batch_multiplier}")
        execution_logger.info("MIGRATION NOTES:")
        execution_logger.info("  - Migrated from marker-pdf==0.2.6 to v1.0+")
        execution_logger.info("  - Using new API: PdfConverter, create_model_dict, text_from_rendered")
        execution_logger.info("  - Removed all compatibility patches")
        execution_logger.info("  - OCR handling managed internally by Marker")
        execution_logger.info("  - Universal script: Auto-detects GPU/CPU and configures dynamically")
        execution_logger.info(f"  - Batch Configuration: batch_multiplier={BATCH_MULTIPLIER}, SURYA_BATCH_SIZE={SURYA_BATCH_SIZE}")
        if BATCH_MULTIPLIER == 1 and SURYA_BATCH_SIZE == "1":
            execution_logger.info("  - MEDICAL DATA MODE: Using batch_multiplier=1 for maximum accuracy")
            execution_logger.info("    This prevents symbol misrecognition (e.g., '±' → '6') in medical tables")
        else:
            execution_logger.warning(f"  - WARNING: Using batch_multiplier={BATCH_MULTIPLIER} may reduce accuracy")
            execution_logger.warning("    Not recommended for medical/oncology data")
        if not is_gpu:
            execution_logger.warning("Running on CPU - processing will be slow. Consider using Google Colab for GPU acceleration.")
        execution_logger.info("=" * 80)
    except (NameError, AttributeError):
        # Logger not yet initialized, that's okay - we'll log it later
        pass
    
    return batch_multiplier


# ============================================================================
# Configuration
# ============================================================================
RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/marker_outputs")
LOGS_DIR = Path("logs")

# Create directories if they don't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# Logging Configuration
# ============================================================================

# Set up logging for Phase 1
EXECUTION_LOG = LOGS_DIR / "phase1_execution.log"
ERROR_LOG = LOGS_DIR / "phase1_errors.log"

# Configure execution logger (INFO level - logs all operations)
execution_logger = logging.getLogger("phase1_execution")
execution_logger.setLevel(logging.INFO)
execution_handler = logging.FileHandler(EXECUTION_LOG, encoding="utf-8")
execution_handler.setFormatter(
    logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
)
execution_logger.addHandler(execution_handler)
execution_logger.propagate = False  # Prevent duplicate logs

# Configure error logger (ERROR level - logs only errors)
error_logger = logging.getLogger("phase1_errors")
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(ERROR_LOG, encoding="utf-8")
error_handler.setFormatter(
    logging.Formatter("%(asctime)s - [ERROR] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
)
error_logger.addHandler(error_handler)
error_logger.propagate = False

# ============================================================================
# Metadata extraction (ASCO-specific)
# ============================================================================

def extract_pdf_metadata(pdf_path: str, corpus: Optional[str] = None) -> Dict[str, Optional[str]]:
    """
    Extract tentative metadata (title, DOI) from PDF.
    
    ASCO-specific: Extracts title and DOI for PubMed enrichment in Phase 2.
    
    IMPROVED DOI EXTRACTION:
    - Uses Marker corpus (if available) for better OCR quality
    - Handles DOIs split across multiple lines in multi-column layouts
    - Reconstructs fragmented DOIs by searching continuation in nearby lines
    - Prioritizes early pages to avoid DOI references from bibliography
    
    Args:
        pdf_path: Path to PDF file
        corpus: Optional Marker-extracted corpus (better quality than pypdfium2)
    
    Returns:
        Dictionary with 'title' and 'doi' keys (values may be None if not found)
    """
    try:
        doc = pdfium.PdfDocument(pdf_path)
        pdf_metadata = doc.get_metadata_dict(skip_empty=True)
        
        # Extract title from PDF metadata
        title = pdf_metadata.get("Title", "").strip() if pdf_metadata else None
        if not title:
            title = None
        
        # Improved DOI extraction strategy:
        # 1. Find DOI start pattern (10.XXXX/) - more reliable than trying to match complete DOI
        # 2. Then aggressively search for continuation, handling line breaks and fragmentation
        # Pattern to find DOI start: 10.XXXX/ (where XXXX is 4+ digits)
        doi_start_pattern = r'(?:https?://(?:dx\.)?doi\.org/)?(?:DOI[:\s]+)?(10\.\d{4,}/)'
        
        doi = None
        
        # PRIORITY 1: Search in Marker corpus (best quality, handles fragmentation)
        if corpus:
            try:
                # Focus on first 3000 characters (first 1-2 pages) to avoid references
                early_text = corpus[:3000]
                
                # Find all potential DOI starts
                start_matches = list(re.finditer(doi_start_pattern, early_text, re.IGNORECASE))
                
                for match in start_matches:
                    doi_start = match.group(1)  # The "10.XXXX/" part
                    start_pos = match.start()
                    end_pos = match.end()
                    
                    # Check context to avoid references
                    context_start = max(0, start_pos - 200)
                    context_end = min(len(early_text), end_pos + 300)
                    context = early_text[context_start:context_end].lower()
                    
                    if any(keyword in context for keyword in ['references', 'bibliography', 'cited']):
                        continue
                    
                    # Extract text after DOI start (up to 300 chars to handle fragmentation)
                    continuation_text = early_text[end_pos:end_pos + 300]
                    
                    # Strategy: Remove line breaks and spaces, then find longest valid DOI continuation
                    # This handles cases where DOI is split across lines
                    continuation_clean = re.sub(r'[\n\r]+', ' ', continuation_text)  # Replace line breaks with space
                    continuation_clean = re.sub(r'\s+', ' ', continuation_clean)  # Normalize spaces
                    
                    # Find continuation: alphanumeric, dots, hyphens, underscores, slashes
                    # Stop at: spaces, parentheses, brackets, commas, semicolons, or end of reasonable DOI
                    # DOI suffix can be quite long, so we're more permissive
                    continuation_match = re.search(r'^([a-zA-Z0-9.\-/_]+)', continuation_clean)
                    
                    if continuation_match:
                        continuation = continuation_match.group(1).strip()
                        
                        # Remove trailing punctuation that likely doesn't belong to DOI
                        # But be careful - some DOIs end with dots (e.g., "suppl.")
                        # Remove only if followed by space or end of text
                        continuation = re.sub(r'([.,;)\]]+)(?:\s|$)', r'\1', continuation)
                        # Actually, let's be more conservative - only remove if it's clearly trailing punctuation
                        # after a space or at end
                        continuation = re.sub(r'\s+[.,;)\]]+$', '', continuation)
                        
                        # Reconstruct full DOI
                        reconstructed_doi = doi_start + continuation
                        
                        # Clean up: remove any trailing punctuation that's clearly not part of DOI
                        # But keep dots/hyphens that might be part of the DOI
                        reconstructed_doi = re.sub(r'[.,;)\]]+$', '', reconstructed_doi)
                        
                        # Validate: DOI should be reasonable length and format
                        # Typical DOIs are 20-150 characters
                        if 15 <= len(reconstructed_doi) <= 150:
                            # Check if it looks like a valid DOI format
                            # After the slash, we allow alphanumeric, dots, hyphens, underscores, slashes
                            if re.match(r'^10\.\d{4,}/[a-zA-Z0-9.\-/_]+$', reconstructed_doi):
                                # Additional check: DOI suffix should have at least 3 characters
                                suffix = reconstructed_doi.split('/', 1)[1] if '/' in reconstructed_doi else ''
                                if len(suffix) >= 3:
                                    doi = reconstructed_doi
                                    execution_logger.info(f"  Found DOI in Marker corpus: {doi}")
                                    break
                
                # If still no DOI found, try a more aggressive search in larger window
                if not doi:
                    # Expand search to 5000 characters
                    expanded_text = corpus[:5000]
                    start_matches = list(re.finditer(doi_start_pattern, expanded_text, re.IGNORECASE))
                    
                    for match in start_matches:
                        doi_start = match.group(1)
                        start_pos = match.start()
                        end_pos = match.end()
                        
                        # Check context
                        context_start = max(0, start_pos - 200)
                        context_end = min(len(expanded_text), end_pos + 300)
                        context = expanded_text[context_start:context_end].lower()
                        
                        if any(keyword in context for keyword in ['references', 'bibliography', 'cited']):
                            continue
                        
                        continuation_text = expanded_text[end_pos:end_pos + 300]
                        continuation_clean = re.sub(r'[\n\r]+', ' ', continuation_text)
                        continuation_clean = re.sub(r'\s+', ' ', continuation_clean)
                        
                        continuation_match = re.search(r'^([a-zA-Z0-9.\-/_]+)', continuation_clean)
                        if continuation_match:
                            continuation = continuation_match.group(1).strip()
                            continuation = re.sub(r'\s+[.,;)\]]+$', '', continuation)
                            
                            reconstructed_doi = doi_start + continuation
                            reconstructed_doi = re.sub(r'[.,;)\]]+$', '', reconstructed_doi)
                            
                            if 15 <= len(reconstructed_doi) <= 150:
                                if re.match(r'^10\.\d{4,}/[a-zA-Z0-9.\-/_]+$', reconstructed_doi):
                                    suffix = reconstructed_doi.split('/', 1)[1] if '/' in reconstructed_doi else ''
                                    if len(suffix) >= 3:
                                        doi = reconstructed_doi
                                        execution_logger.info(f"  Found DOI in Marker corpus (expanded search): {doi}")
                                        break
                
            except Exception as e:
                execution_logger.warning(f"  Error extracting DOI from Marker corpus: {e}")
        
        # PRIORITY 2: Search in PDF metadata fields (fallback)
        # Metadata fields are usually short, so DOIs should be complete
        if not doi and pdf_metadata:
            # Check Subject field (often contains DOI)
            subject = pdf_metadata.get("Subject", "")
            if subject:
                # Use same strategy: find start, then continuation
                start_match = re.search(doi_start_pattern, subject, re.IGNORECASE)
                if start_match:
                    doi_start = start_match.group(1)
                    end_pos = start_match.end()
                    continuation_text = subject[end_pos:end_pos + 200]
                    continuation_clean = re.sub(r'[\n\r\s]+', '', continuation_text)
                    continuation_match = re.search(r'^([a-zA-Z0-9.\-/_]+)', continuation_clean)
                    if continuation_match:
                        continuation = continuation_match.group(1)
                        continuation = re.sub(r'[.,;)\]]+$', '', continuation)
                        reconstructed_doi = doi_start + continuation
                        reconstructed_doi = re.sub(r'[.,;)\]]+$', '', reconstructed_doi)
                        if 15 <= len(reconstructed_doi) <= 150 and re.match(r'^10\.\d{4,}/[a-zA-Z0-9.\-/_]+$', reconstructed_doi):
                            suffix = reconstructed_doi.split('/', 1)[1] if '/' in reconstructed_doi else ''
                            if len(suffix) >= 3:
                                doi = reconstructed_doi
                                execution_logger.info(f"  Found DOI in PDF metadata (Subject): {doi}")
            
            # Check Keywords field
            if not doi:
                keywords = pdf_metadata.get("Keywords", "")
                if keywords:
                    start_match = re.search(doi_start_pattern, keywords, re.IGNORECASE)
                    if start_match:
                        doi_start = start_match.group(1)
                        end_pos = start_match.end()
                        continuation_text = keywords[end_pos:end_pos + 200]
                        continuation_clean = re.sub(r'[\n\r\s]+', '', continuation_text)
                        continuation_match = re.search(r'^([a-zA-Z0-9.\-/_]+)', continuation_clean)
                        if continuation_match:
                            continuation = continuation_match.group(1)
                            continuation = re.sub(r'[.,;)\]]+$', '', continuation)
                            reconstructed_doi = doi_start + continuation
                            reconstructed_doi = re.sub(r'[.,;)\]]+$', '', reconstructed_doi)
                            if 15 <= len(reconstructed_doi) <= 150 and re.match(r'^10\.\d{4,}/[a-zA-Z0-9.\-/_]+$', reconstructed_doi):
                                suffix = reconstructed_doi.split('/', 1)[1] if '/' in reconstructed_doi else ''
                                if len(suffix) >= 3:
                                    doi = reconstructed_doi
                                    execution_logger.info(f"  Found DOI in PDF metadata (Keywords): {doi}")
        
        # PRIORITY 3: Search in first 3 pages using pypdfium2 (fallback if corpus failed)
        if not doi and len(doc) > 0:
            try:
                max_pages_to_check = min(3, len(doc))
                for page_idx in range(max_pages_to_check):
                    page = doc[page_idx]
                    text_page = page.get_textpage()
                    page_text = text_page.get_text_bounded()
                    
                    # Use same strategy: find start, then continuation
                    start_matches = list(re.finditer(doi_start_pattern, page_text, re.IGNORECASE))
                    for match in start_matches:
                        doi_start = match.group(1)
                        start_pos = match.start()
                        end_pos = match.end()
                        
                        # Check context
                        context_start = max(0, start_pos - 200)
                        context_end = min(len(page_text), end_pos + 300)
                        context = page_text[context_start:context_end].lower()
                        
                        if any(keyword in context for keyword in ['references', 'bibliography', 'cited']):
                            continue
                        
                        continuation_text = page_text[end_pos:end_pos + 300]
                        continuation_clean = re.sub(r'[\n\r]+', ' ', continuation_text)
                        continuation_clean = re.sub(r'\s+', ' ', continuation_clean)
                        continuation_match = re.search(r'^([a-zA-Z0-9.\-/_]+)', continuation_clean)
                        if continuation_match:
                            continuation = continuation_match.group(1).strip()
                            continuation = re.sub(r'\s+[.,;)\]]+$', '', continuation)
                            reconstructed_doi = doi_start + continuation
                            reconstructed_doi = re.sub(r'[.,;)\]]+$', '', reconstructed_doi)
                            if 15 <= len(reconstructed_doi) <= 150:
                                if re.match(r'^10\.\d{4,}/[a-zA-Z0-9.\-/_]+$', reconstructed_doi):
                                    suffix = reconstructed_doi.split('/', 1)[1] if '/' in reconstructed_doi else ''
                                    if len(suffix) >= 3:
                                        doi = reconstructed_doi
                                        execution_logger.info(f"  Found DOI in pypdfium2 extraction (page {page_idx + 1}): {doi}")
                                        break
                        
                        if doi:
                            break
                    
                    if doi:
                        break
            except Exception as e:
                execution_logger.warning(f"  Error extracting DOI from pypdfium2: {e}")
        
        doc.close()
        
        return {
            "title": title if title else None,
            "doi": doi if doi else None
        }
    
    except Exception as e:
        warning_msg = f"Could not extract metadata from {Path(pdf_path).name}: {e}"
        print(f"Warning: {warning_msg}")
        execution_logger.warning(warning_msg)
        return {"title": None, "doi": None}

# ============================================================================
# Main function
# ============================================================================
def main():
    """
    Phase 1: Extract text and tentative metadata from PDFs using Marker v1.0+.
    
    MIGRATED TO MARKER v1.0+:
    - Simple binary device detection: CUDA or CPU (no MPS)
    - Using new Marker v1.0+ API (PdfConverter)
    - GPU acceleration with float16 precision (when CUDA available)
    - OCR handling managed internally by Marker
    - Removed all compatibility patches
    
    For each PDF:
    1. Configure Marker for optimal performance (GPU detection)
    2. Load Marker models using create_model_dict (once at start)
    3. Convert PDF to Markdown using PdfConverter
    4. Extract tentative metadata (title, DOI) from PDF
    5. Save intermediate JSON file with text and metadata
    6. Log all operations to logs/phase1_execution.log
    """
    start_time = datetime.now()
    
    # Initialize logging first (needed for configure_marker_for_performance logging)
    execution_logger.info("=" * 80)
    execution_logger.info("PHASE 1: ASCO PDF EXTRACTION STARTED (MARKER v1.0+)")
    execution_logger.info(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    execution_logger.info("=" * 80)
    
    # Step 0: Configure Marker for optimal performance BEFORE loading models
    # This must be done before model loading to ensure correct device/dtype
    # Returns batch_multiplier for use in processing
    print("Configuring Marker for optimal performance...")
    batch_multiplier = configure_marker_for_performance()
    
    pdf_files = list(RAW_DIR.glob("*.pdf"))
    if not pdf_files:
        msg = f"No PDF files found in {RAW_DIR.resolve()}"
        print(msg)
        execution_logger.warning(msg)
        return
    
    execution_logger.info(f"Found {len(pdf_files)} PDF file(s) to process")
    print(f"Found {len(pdf_files)} PDF(s). Starting extraction...\n")
    
    # Step 1: Load Marker models using new v1.0+ API (once at start)
    print("Loading Marker models (this may take a while)...")
    execution_logger.info("Loading Marker models using create_model_dict (v1.0+ API)...")
    model_load_start = datetime.now()
    
    # Step 1: Load models - try both old and new API
    models = None
    model_dict = None
    converter = None
    
    try:
        if HAS_CREATE_MODEL_DICT:
            # New v1.0+ API: create_model_dict
            execution_logger.info("Using Marker v1.0+ API (create_model_dict)")
            model_dict = create_model_dict()
            model_load_time = (datetime.now() - model_load_start).total_seconds()
            execution_logger.info(f"Models loaded successfully in {model_load_time:.2f} seconds")
            print("Models loaded.\n")
            
            # Initialize PdfConverter if available
            if HAS_PDF_CONVERTER:
                print("Initializing PdfConverter...")
                execution_logger.info("Initializing PdfConverter (v1.0+ API)...")
                try:
                    converter = PdfConverter(model_dict)
                    execution_logger.info("PdfConverter initialized successfully")
                    print("PdfConverter ready.\n")
                except Exception as e:
                    execution_logger.warning(f"Could not initialize PdfConverter: {e}. Will try alternative method.")
                    converter = None
        else:
            # Fallback to old API: load_all_models
            execution_logger.info("Using Marker 0.2.6 API (load_all_models) - fallback mode")
            models = load_all_models()
            model_load_time = (datetime.now() - model_load_start).total_seconds()
            execution_logger.info(f"Models loaded successfully in {model_load_time:.2f} seconds")
            print("Models loaded.\n")
    except Exception as e:
        error_msg = f"Failed to load Marker models: {e}"
        print(f"✗ {error_msg}")
        execution_logger.error(error_msg)
        error_logger.error(error_msg, exc_info=True)
        return
    
    # Process each PDF
    success_count = 0
    failed_count = 0
    
    for pdf_path in pdf_files:
        pdf_start_time = datetime.now()
        pdf_name = pdf_path.name
        execution_logger.info(f"Processing: {pdf_name}")
        print(f"→ Processing: {pdf_name}")
        
        try:
            # Step 2: Convert PDF to Markdown using Marker v1.0+ API
            execution_logger.info(f"  Converting PDF to Markdown: {pdf_name}")
            print(f"  Converting to Markdown...")
            
            # Try different APIs based on what's available (multi-strategy fallback)
            corpus = None
            
            # Strategy 1: Use PdfConverter (v1.0+ API) if available
            if converter is not None:
                try:
                    execution_logger.info("  Trying PdfConverter (v1.0+ API)")
                    
                    # Try different method names for PdfConverter
                    full_pdf = None
                    if hasattr(converter, 'convert_pdf'):
                        full_pdf = converter.convert_pdf(str(pdf_path))
                    elif hasattr(converter, 'convert'):
                        full_pdf = converter.convert(str(pdf_path))
                    elif hasattr(converter, '__call__'):
                        full_pdf = converter(str(pdf_path))
                    
                    if full_pdf is not None:
                        # Extract text from result - check what type of object we got
                        if isinstance(full_pdf, str):
                            corpus = full_pdf.strip()
                        elif hasattr(full_pdf, 'text_from_rendered'):
                            corpus = full_pdf.text_from_rendered().strip()
                        elif hasattr(full_pdf, 'get_markdown'):
                            corpus = full_pdf.get_markdown().strip()
                        elif hasattr(full_pdf, 'text'):
                            corpus = full_pdf.text.strip()
                        elif hasattr(full_pdf, 'full_text'):
                            corpus = full_pdf.full_text.strip()
                        else:
                            corpus = str(full_pdf).strip()
                        
                        if corpus:
                            execution_logger.info("  ✓ Successfully used PdfConverter API")
                except Exception as e:
                    execution_logger.warning(f"  PdfConverter method failed: {e}. Trying fallback.")
                    corpus = None
            
            # Strategy 2: Use convert_single_pdf with model_dict (v1.0+ API fallback)
            if corpus is None and model_dict is not None and HAS_CONVERT_SINGLE_PDF:
                try:
                    execution_logger.info(f"  Trying convert_single_pdf with model_dict (batch_multiplier={batch_multiplier})")
                    text, images, marker_metadata = convert_single_pdf(
                        str(pdf_path),
                        model_dict,
                        batch_multiplier=batch_multiplier
                    )
                    corpus = text.strip() if text else ""
                    if corpus:
                        execution_logger.info("  ✓ Successfully used convert_single_pdf with model_dict")
                except Exception as e:
                    execution_logger.warning(f"  convert_single_pdf with model_dict failed: {e}")
                    corpus = None
            
            # Strategy 3: Use convert_single_pdf with old models list (legacy fallback)
            if corpus is None and HAS_CONVERT_SINGLE_PDF and models is not None:
                try:
                    execution_logger.info(f"  Trying convert_single_pdf with models list (legacy, batch_multiplier={batch_multiplier})")
                    text, images, marker_metadata = convert_single_pdf(
                        str(pdf_path),
                        models,
                        batch_multiplier=batch_multiplier
                    )
                    corpus = text.strip() if text else ""
                    if corpus:
                        execution_logger.info("  ✓ Successfully used convert_single_pdf (legacy)")
                except Exception as e:
                    execution_logger.warning(f"  convert_single_pdf failed: {e}")
                    corpus = None
            
            # Strategy 4: Fallback error with detailed information
            if corpus is None:
                error_details = (
                    f"Could not convert PDF with any available API.\n"
                    f"  - PdfConverter available: {converter is not None}\n"
                    f"  - HAS_CONVERT_SINGLE_PDF: {HAS_CONVERT_SINGLE_PDF}\n"
                    f"  - model_dict available: {model_dict is not None}\n"
                    f"  - models available: {models is not None}\n"
                )
                raise RuntimeError(error_details)
            
            # Clean and structure the corpus (text from Marker)
            corpus = corpus.strip()
            
            # Step 3: Extract tentative metadata (title, DOI) from PDF
            # Pass corpus to function for improved DOI extraction (handles fragmented DOIs)
            execution_logger.info(f"  Extracting metadata: {pdf_name}")
            pdf_metadata = extract_pdf_metadata(str(pdf_path), corpus=corpus)
            
            # Combine metadata
            # Prefer PDF metadata title over Marker's (Marker may not extract it)
            title = pdf_metadata.get("title")
            doi = pdf_metadata.get("doi")
            
            if not corpus:
                warning_msg = f"  Warning: Empty corpus extracted from {pdf_name}"
                execution_logger.warning(warning_msg)
                print(f"  ⚠ {warning_msg}")
            
            # Create output structure
            output_data = {
                "text": corpus,  # Clean, structured Markdown representation
                "metadata": {
                    "title": title,  # Tentative title from PDF metadata
                    "doi": doi       # Tentative DOI from PDF metadata or text
                }
            }
            
            # Step 4: Save intermediate JSON file
            json_file = OUTPUT_DIR / f"{pdf_path.stem}.json"
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            processing_time = (datetime.now() - pdf_start_time).total_seconds()
            success_count += 1
            
            execution_logger.info(f"  ✓ Successfully processed: {pdf_name}")
            execution_logger.info(f"    - Output: {json_file.name}")
            execution_logger.info(f"    - Title: {title if title else 'Not found'}")
            execution_logger.info(f"    - DOI: {doi if doi else 'Not found'}")
            execution_logger.info(f"    - Corpus length: {len(corpus):,} characters")
            execution_logger.info(f"    - Processing time: {processing_time:.2f} seconds")
            
            print(f"  ✓ Saved: {json_file.name}")
            print(f"  - Title: {title if title else 'Not found'}")
            print(f"  - DOI: {doi if doi else 'Not found'}")
            print(f"  - Corpus length: {len(corpus)} characters\n")
        
        except Exception as e:
            failed_count += 1
            processing_time = (datetime.now() - pdf_start_time).total_seconds()
            error_msg = f"Failed to process {pdf_name}: {e}"
            error_details = f"  ✗ {error_msg} (after {processing_time:.2f} seconds)"
            
            print(error_details)
            execution_logger.error(error_msg)
            execution_logger.error(f"  Processing time before failure: {processing_time:.2f} seconds")
            error_logger.error(error_msg, exc_info=True)
            print()  # Empty line for readability
    
    # Final summary
    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    
    execution_logger.info("=" * 80)
    execution_logger.info("PHASE 1: ASCO PDF EXTRACTION COMPLETED")
    execution_logger.info(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    execution_logger.info(f"Total execution time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
    execution_logger.info(f"Successfully processed: {success_count} PDF(s)")
    execution_logger.info(f"Failed: {failed_count} PDF(s)")
    execution_logger.info(f"Output directory: {OUTPUT_DIR.resolve()}")
    execution_logger.info(f"Execution log: {EXECUTION_LOG.resolve()}")
    if failed_count > 0:
        execution_logger.info(f"Error log: {ERROR_LOG.resolve()}")
    execution_logger.info("=" * 80)
    
    print(f"\nPhase 1 complete! Intermediate files saved in {OUTPUT_DIR.resolve()}")
    print(f"  - Successfully processed: {success_count} PDF(s)")
    print(f"  - Failed: {failed_count} PDF(s)")
    print(f"  - Total time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
    print(f"  - Execution log: {EXECUTION_LOG.resolve()}")
    if failed_count > 0:
        print(f"  - Error log: {ERROR_LOG.resolve()}")

if __name__ == "__main__":
    main()
