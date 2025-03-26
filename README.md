# PDF Basic Metadata Editor

A simple Python script to edit **basic metadata** in PDF files. It’s not perfect (yet!), but I whipped it up out of boredom, and it gets the job done for now.

I’m planning to expand it to support more file formats and metadata types beyond the basics I’ve implemented so far. If it’s useful to you, I’m glad! :)

## Features
- **View Metadata:** Load and display basic PDF metadata (e.g., Title, Author, Creation Date).
- **Edit Metadata:** Modify metadata fields directly in a sleek GUI.
- **Remove Metadata:** Clear all metadata with a single click.
- **In-Place Editing:** Changes are saved directly to the original PDF file.
- **Cool UI:** Pitch-black theme with purple accents and a custom icon for a futuristic vibe.

Currently supports the following metadata fields:
- `/Title`
- `/Author`
- `/Subject`
- `/Keywords`
- `/Creator`
- `/Producer`
- `/CreationDate`
- `/ModDate`
- `/Trapped`

## Installation
1. **Clone or Download:**
   - Grab the script from this repository (e.g., `pdf_metadata_handler.py`).
   - Optionally, download the `requirements.txt` file too.

2. **Install Dependencies:**
   - You’ll need Python 3.x installed.
   - Run this command in your terminal to install the required library:
     ```bash
     pip install -r requirements.txt
     ```
   - Or, if you just have the script:
     ```bash
     pip install PyPDF2
     ```

3. **Custom Icon (Optional):**
   - Place a `icon.png` file (e.g., 32x32 or 64x64 pixels) in the same directory as the script to customize the window icon. If it’s missing, the script will still run fine.

## Usage
1. **Run the Script:**
   ```bash
   python pdf_metadata_handler.py
