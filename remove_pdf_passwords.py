from typing import Optional
import argparse
import getpass
from pathlib import Path
from pypdf import PdfReader, PdfWriter


def remove_passwords(input_dir: str, output_dir: Optional[str] = None) -> None:
    input_path = Path(input_dir).expanduser().resolve()
    output_path = Path(output_dir).expanduser().resolve() if output_dir else input_path
    output_path.mkdir(parents=True, exist_ok=True)

    password = getpass.getpass("PDF password (won't echo): ")

    pdf_files = sorted(input_path.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {input_path}")
        return

    for pdf in pdf_files:
        print(f"Processing: {pdf.name}")
        try:
            reader = PdfReader(str(pdf))
            if reader.is_encrypted and not reader.decrypt(password):
                print(f"  ! Wrong password for {pdf.name}, skipping.")
                continue

            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            out_file = (output_path / pdf.name).with_name(pdf.stem + "_nopw.pdf")
            with open(out_file, "wb") as f:
                writer.write(f)

            print(f"  -> Saved: {out_file}")
        except Exception as e:
            print(f"  ! Error processing {pdf.name}: {e}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove password protection from all PDFs in a folder."
    )
    parser.add_argument(
        "input_dir",
        help="Folder containing password-protected PDFs",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        default=None,
        help="Folder to save unlocked PDFs (default: same as input)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    remove_passwords(input_dir=args.input_dir, output_dir=args.output_dir)
