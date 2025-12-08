import os
from pypdf import PdfReader, PdfWriter

def split_pdf_manually():
    print("--- PDF Splitter Tool ---")

    # 1. Get the PDF file path
    pdf_filename = input("Enter the PDF filename (e.g., 'document.pdf'): ").strip()
    
    # Check if file exists
    if not os.path.exists(pdf_filename):
        print(f"Error: The file '{pdf_filename}' was not found.")
        return

    # 2. Open the PDF to read
    try:
        reader = PdfReader(pdf_filename)
        total_pages = len(reader.pages)
        print(f"Successfully loaded. Total pages: {total_pages}")
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return

    # 3. Get the split point
    try:
        split_point = int(input(f"Enter the page number to end Part 1 (1 - {total_pages}): "))
    except ValueError:
        print("Error: Please enter a valid whole number.")
        return

    # Validation to ensure split point is within range
    if split_point < 1 or split_point >= total_pages:
        print(f"Error: Please choose a number between 1 and {total_pages - 1}.")
        return

    print("Processing...")

    # 4. Create Writer Objects
    writer_part1 = PdfWriter()
    writer_part2 = PdfWriter()

    # 5. Add pages to respective writers
    # Python uses 0-based indexing. 
    # If split_point is 141, we want indices 0 to 140 (which is 141 pages).
    
    # Part 1: Page 1 to split_point
    for i in range(split_point):
        writer_part1.add_page(reader.pages[i])

    # Part 2: split_point + 1 to End
    for i in range(split_point, total_pages):
        writer_part2.add_page(reader.pages[i])

    # 6. Construct output filenames based on original name
    base_name = os.path.splitext(pdf_filename)[0]
    out1 = f"{base_name}_Part1.pdf"
    out2 = f"{base_name}_Part2.pdf"

    # 7. Save the files
    with open(out1, "wb") as f1:
        writer_part1.write(f1)
    
    with open(out2, "wb") as f2:
        writer_part2.write(f2)

    print("--- Success! ---")
    print(f"Created: {out1} (Pages 1-{split_point})")
    print(f"Created: {out2} (Pages {split_point + 1}-{total_pages})")

if __name__ == "__main__":
    split_pdf_manually()

