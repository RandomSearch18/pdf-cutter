import sys
from pathlib import Path
from sys import argv, stderr

DOCUMENTATION_URL = "https://github.com/RandomSearch18/pdf-cutter#readme"

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("Error: The pypdf package must be installed to use this program.", file=stderr)
    print(f"See program documentation for details: {DOCUMENTATION_URL}", file=stderr)
    sys.exit(1)

from pypdf.errors import PyPdfError, PdfStreamError

# 30 pages is the maximum that PaperCut will allow in a single print job
# Note that this should be even so that double-sided printing can carry forward
PAGES_PER_CHUNK = 30


def get_file_path():
    # Take file path from command-line arg if provided
    if len(argv) > 1:
        return Path(argv[1])

    raw_input = input("Enter PDF file path: ")
    # Allow quoted path, like you get if you drag and drop a file into the terminal
    if raw_input.startswith("'") and raw_input.endswith("'"):
        raw_input = raw_input[1:-1]
    return Path(raw_input)


def main():
    file_path = get_file_path()
    try:
        reader = PdfReader(file_path)
        print(f"Opened PDF {file_path}")
    except OSError as error:
        print(error, file=stderr)
        return
    except PdfStreamError:
        print(f"Error: Not a PDF file: {file_path}", file=stderr)
        return
    except PyPdfError:
        print(f"Error: Failed reading PDF file: {file_path}", file=stderr)
        return

    total_pages = len(reader.pages)
    print(f"Processing {total_pages} pages")

    # Prepare the target folder
    target_folder = file_path.parent / f"{file_path.stem} (PDF cutter)"
    target_folder.mkdir(exist_ok=True, parents=True)
    for file in target_folder.glob("*"):
        file.unlink()

    done = False
    chunk_number = 1
    pages = list(reader.pages)
    while not done:
        # Add pages to a PDF in-memory
        print(f"Creating chunk #{chunk_number}...")
        writer = PdfWriter()
        pages_added = 0
        while pages_added < PAGES_PER_CHUNK:
            if len(pages) == 0:
                break
            page = pages.pop(0)
            writer.add_page(page)
            pages_added += 1
        # Write the file
        output_path = target_folder / f"Part {chunk_number} - {file_path.stem}.pdf"
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
        # End the loop if we've gotten through the PDF
        chunk_number += 1
        if pages_added < PAGES_PER_CHUNK:
            done = True


if __name__ == "__main__":
    main()
