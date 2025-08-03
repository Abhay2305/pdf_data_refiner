# import pdfplumber
# import pandas as pd
# from fpdf import FPDF

# # === STEP 1: Extract tables from all pages ===
# pdf_path = "Hr_Contacts_two.pdf"  # Change this to your actual PDF file path
# all_tables = []

# with pdfplumber.open(pdf_path) as pdf:
#     for page in pdf.pages:
#         tables = page.extract_tables()
#         for table in tables:
#             df = pd.DataFrame(table[1:], columns=table[0])  # Skip header duplication
#             all_tables.append(df)

# # === STEP 2: Combine and keep only 'Name' and 'Email' columns ===
# full_df = pd.concat(all_tables, ignore_index=True)

# # Confirm detected column names
# print("Detected columns:", full_df.columns.tolist())

# # Keep only Name and Email
# columns_to_keep = ['Name', 'Email']
# clean_df = full_df[columns_to_keep]

# # === STEP 3: Create PDF ===

# class PDF(FPDF):
#     def header(self):
#         self.set_font("Arial", "B", 10)
#         self.set_fill_color(255, 255, 0)  # Yellow background for header
#         for col in clean_df.columns:
#             self.cell(95, 8, str(col), border=1, fill=True)
#         self.ln()

#     def row(self, row_data):
#         self.set_font("Arial", size=9)
#         for item in row_data:
#             # Clean encoding for special characters
#             text = str(item).encode('latin-1', 'replace').decode('latin-1')
#             self.cell(95, 7, text, border=1)
#         self.ln()

# pdf = PDF()
# pdf.set_auto_page_break(auto=True, margin=15)
# pdf.add_page()

# # === STEP 4: Add rows to the PDF ===
# for idx, row in clean_df.iterrows():
#     pdf.row(row)

# # === STEP 5: Save PDF ===
# pdf.output("updated_Hr_Contacts_two.pdf")

# print("Done! Saved as 'name_email_only.pdf'")


import pdfplumber
import pandas as pd
from fpdf import FPDF

pdf_path = "Hr_Contacts.pdf"
all_rows = []
standard_header = None

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        tables = page.extract_tables()
        for table in tables:
            # Use first table header as reference
            if not standard_header:
                standard_header = table[0]
            for row in table[1:]:
                # Only include rows with matching column count
                if len(row) == len(standard_header):
                    row_dict = dict(zip(standard_header, row))
                    all_rows.append(row_dict)
                else:
                    print(f"Skipping row on page {page_num} due to mismatch: {row}")

# Convert to DataFrame
df = pd.DataFrame(all_rows)

# Clean column names
df.columns = [col.strip() for col in df.columns]

# Show available columns
print("Detected columns:", df.columns.tolist())

# Select only Name and Email (handle slight header variations)
name_col = next((c for c in df.columns if "name" in c.lower()), "Name")
email_col = next((c for c in df.columns if "email" in c.lower()), "Email")

df_clean = df[[name_col, email_col]]

# === Export to PDF ===

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 10)
        self.set_fill_color(255, 255, 0)
        for col in df_clean.columns:
            self.cell(95, 8, col, border=1, fill=True)
        self.ln()

    def row(self, row_data):
        self.set_font("Arial", size=9)
        for item in row_data:
            text = str(item).encode('latin-1', 'replace').decode('latin-1')
            self.cell(95, 7, text, border=1)
        self.ln()

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

for _, row in df_clean.iterrows():
    pdf.row(row)

pdf.output("updated_list.pdf")
print("Finished: name_email_fixed.pdf")
