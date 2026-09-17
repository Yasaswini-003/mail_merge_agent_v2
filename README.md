📜 Generic Mail Merge Agent — Version 2

Dynamic Document Generation using Google ADK + Python

The Generic Mail Merge Agent is an AI-powered document automation project that generates personalized DOCX documents using a user-provided DOCX template and an Excel data file.

Unlike Version 1, this version does not depend on predefined fields such as Student Name, Roll No, Coordinator, or HOD.

The fields are detected dynamically from the uploaded template.

✨ What Does It Do?
📄 DOCX Template
       │
       ▼
🔍 Detect Placeholders
       │
       ▼
📊 Read Excel File
       │
       ▼
🔎 Validate Required Columns
       │
       ▼
🔎 Validate Required Values
       │
       ▼
   ┌───┴────┐
   │        │
Invalid    Valid
   │        │
   ▼        ▼
🛑 Stop   🔄 Replace Placeholders
            │
            ▼
       📄 Generate Documents
            │
            ▼
       📁 Save in output/

The agent can:

✅ Detect placeholders dynamically
✅ Validate the DOCX template
✅ Identify required Excel columns automatically
✅ Validate missing Excel columns
✅ Validate blank required values
✅ Ignore extra Excel columns
✅ Generate one personalized DOCX per Excel row
✅ Replace placeholders automatically
✅ Keep the original template unchanged
✅ Save generated documents in the output folder
✅ Work with different document types
✅ Use Google ADK as the agent framework
🛠️ Technologies
Technology	Purpose
🐍 Python	Core implementation
🤖 Google ADK	AI agent framework
✨ Gemini	Agent model
📊 Pandas	Excel processing
📄 DOCX	Document template
📑 Excel	Input data
🗜️ ZIP / XML	DOCX processing

The project was tested using:

Google ADK 2.9.1
📌 Version 2

Version 2 is a generic implementation of the Mail Merge Agent.

Unlike Version 1, there are no predefined business fields.

For example, the template could contain:

{{Name}}
{{dept}}

or:

{{Employee}}
{{Company}}
{{JoiningDate}}

or any other supported field names.

The Excel columns are determined from the placeholders in the template.

🏷️ Dynamic Placeholders

For example, a DOCX template may contain:

This document is presented to

{{Name}}

from the

{{dept}}

department.

The system automatically detects:

{{Name}}
{{dept}}

Therefore, the Excel file must contain:

Name	dept
Ananya Reddy	CSE
Vikram Sharma	ECE
Sneha Patel	Civil
Arjun Verma	Mechanical
Kavya Nair	EEE

No fields are hardcoded into the application.

📊 Sample Excel Data

The current local test data contains:

Name	dept
Ananya Reddy	CSE
Vikram Sharma	ECE
Sneha Patel	Civil
Arjun Verma	Mechanical
Kavya Nair	EEE

➡️ 5 valid Excel records → 5 personalized DOCX documents

📂 Project Structure
mail_merge_agent_v2/
│
├── 📁 mail_merge_agent/
│   ├── 📄 __init__.py
│   ├── 🤖 agent.py
│   └── 🔧 tools.py
│
├── 📁 output/
│
├── 📄 .env
├── 📄 .env.example
├── 📄 .gitignore
├── 📄 requirements.txt
└── 📄 README.md

Temporary files used during local testing:

📄 sample_certificate.docx
📊 Data.xlsx

These are test files and are not required by the generic implementation.

⚙️ How It Works
1️⃣ Read the DOCX Template

The agent first checks the uploaded DOCX template.

It verifies:

✔ File exists
✔ File is a DOCX file
✔ Placeholders exist

Example:

{{Name}}
{{dept}}
2️⃣ Detect Placeholders

The system dynamically extracts the fields from the template.

For example:

{{Name}}
{{dept}}

becomes:

Name
dept

These fields are then used to determine the required Excel columns.

3️⃣ Validate Excel Columns

The Excel file is checked against the detected placeholders.

For example:

Template:

{{Name}}
{{dept}}

Excel:

Name
dept

✅ Validation passes.

If the Excel file contains only:

Name

the system reports:

Excel validation failed.

The following columns are missing:
dept

No documents are generated.

4️⃣ Validate Required Values

Every required field must contain a value.

Example:

Name	dept
Ananya Reddy	CSE
Vikram Sharma	ECE
Sneha Patel	Civil
Arjun Verma	

Kavya Nair	EEE

The system detects the missing value:

Excel validation failed.

The following required values are missing:
Row 5: dept

No certificates should be generated.

This prevents incomplete documents from being generated.

5️⃣ Ignore Extra Excel Columns

The Excel file can contain additional information.

For example:

Name	dept	Age	Phone
Ananya Reddy	CSE	21	9876543210

If the template only contains:

{{Name}}
{{dept}}

then:

Age
Phone

are ignored.

Only fields required by the template are used.

6️⃣ Replace Placeholders

For example:

{{Name}}

becomes:

Ananya Reddy

and:

{{dept}}

becomes:

CSE

The same process is performed for every Excel row.

7️⃣ Generate Documents

One personalized DOCX document is created for every valid Excel record.

For example:

📄 Record_1_1.docx
📄 Record_2_2.docx
📄 Record_3_3.docx
📄 Record_4_4.docx
📄 Record_5_5.docx

All generated files are stored inside:

output/

The original template remains unchanged.

🧩 Agent Components
🤖 agent.py

Defines the Google ADK agent:

generic_mail_merge_agent

The agent connects the following tools:

validate_certificate_template()
validate_excel_file()
generate_certificates()

The agent is responsible for coordinating the mail-merge workflow.

🔧 tools.py

Contains the main document-processing functionality.

read_docx_xml()

Reads XML content from the DOCX file.

find_placeholders()

Detects dynamic placeholders from the DOCX template.

validate_certificate_template()

Validates the uploaded DOCX template.

validate_excel_file()

Validates the Excel file against the required fields.

replace_in_docx_xml()

Replaces placeholders inside the DOCX XML.

generate_certificates()

Performs the complete validation and document-generation workflow.

📄 __init__.py

The package exposes the ADK root agent:

from .agent import root_agent

__all__ = ["root_agent"]

This allows Google ADK to discover the agent.

🧪 Local Testing

The document-processing tools can be tested without using the ADK interface.

Test 1 — Detect Placeholders

Run:

python -c "from mail_merge_agent.tools import find_placeholders; print(find_placeholders('sample_certificate.docx'))"

Example result:

['{{dept}}', '{{Name}}']
Test 2 — Validate Excel

Run:

python -c "from mail_merge_agent.tools import validate_certificate_template, find_placeholders, validate_excel_file; p=find_placeholders('sample_certificate.docx'); print('Placeholders:', p); print(); print(validate_excel_file('Data.xlsx',[x[2:-2] for x in p]))"
🧪 Validation Tests Completed
✅ Successful Validation

A valid Excel file containing:

Name
dept

was successfully validated against:

{{Name}}
{{dept}}
❌ Missing Value Test

A blank dept value was introduced.

The system correctly stopped generation and reported:

Excel validation failed.

The following required values are missing:
Row 5: dept

No certificates should be generated.
❌ Missing Column Test

The dept column was removed.

The system correctly reported:

Excel validation failed.

The following columns are missing:
dept

No documents were generated.

✅ Successful Generation Test

After restoring the missing column and filling all required values, the system successfully generated documents for all five Excel records.

5 Excel records
        ↓
5 DOCX documents
🔒 Original Template Protection

The original DOCX template is never overwritten.

The workflow is:

📄 Original Template
       │
       ├──────────────┐
       │              │
       ▼              ▼
   Read Only      Generate Copies
                      │
                      ▼
                  📁 output/

This ensures that the original template remains available for future mail-merge operations.

🚀 Installation & Setup
Step 1 — Open the Project
cd C:\Users\arema\Downloads\mail_merge_agent_v2
Step 2 — Create Virtual Environment
python -m venv .venv
Step 3 — Activate Virtual Environment
.venv\Scripts\Activate

You should see:

(.venv)

at the beginning of the command prompt.

Step 4 — Install Dependencies
pip install -r requirements.txt
Step 5 — Verify Google ADK
pip show google-adk

Expected version:

2.9.1
🔑 Environment Configuration

Create a .env file in the project root:

GOOGLE_API_KEY=your_google_api_key

Never upload the actual API key to GitHub.

The .env.example file can contain:

GOOGLE_API_KEY=your_google_api_key

The .gitignore file should contain:

.env
.venv/
__pycache__/
output/
▶️ Run the Agent

The project can be tested through the Google ADK Web interface.

Step 1 — Activate the Environment
.venv\Scripts\Activate
Step 2 — Start ADK Web
adk web

The local ADK server will start.

Step 3 — Open the ADK Interface

Open the local ADK Web interface provided by the server.

Select:

generic_mail_merge_agent
Step 4 — Interact with the Agent

The agent can be asked to perform a mail-merge task.

For uploaded files, a test prompt used during development was:

I have uploaded a DOCX template and an Excel data file. Please process both uploaded files as a single mail-merge task. First inspect the DOCX template and identify all placeholders dynamically. Then inspect the Excel file and verify that every placeholder has a matching Excel column and that all required values are present for every record. Do not assume or hardcode any field names. If there is any missing placeholder column or blank required value, stop and report all validation errors without generating any documents. If validation passes, generate one personalized DOCX document for every Excel row using the uploaded template, without modifying the original template. Finally, report the total number of documents generated and the output file names. Do not ask me for file paths because the required files have already been uploaded.
🌐 ADK Web Workflow
💬 User
   │
   │ Upload DOCX
   │ Upload Excel
   ▼
🤖 Generic Mail-Merge Agent
   │
   ▼
🔍 Inspect Template
   │
   ▼
🏷️ Detect Placeholders
   │
   ▼
📊 Inspect Excel
   │
   ▼
🔎 Validate Columns
   │
   ▼
🔎 Validate Values
   │
   ├──── ❌ Invalid
   │       │
   │       ▼
   │     🛑 Stop
   │
   └──── ✅ Valid
           │
           ▼
      🔄 Replace Fields
           │
           ▼
      📄 Generate DOCX
           │
           ▼
      📁 Save Output
⚠️ Current ADK Web Limitation

During ADK Web testing, the Gemini API free-tier request quota was exhausted.

The error received was:

429 RESOURCE_EXHAUSTED

Because of this limitation, the local Python document-processing functionality was tested independently.

The ADK agent itself loads successfully, but the complete uploaded-file generation workflow requires available Gemini API quota.

🔍 Agent Verification

The ADK agent was successfully imported using:

python -c "from mail_merge_agent.agent import root_agent; print(root_agent.name)"

Result:

generic_mail_merge_agent

This confirms that the root agent is correctly configured and discoverable.

📋 Validation Rules
Condition	Result
📄 DOCX does not exist	🛑 Stop
❌ File is not DOCX	🛑 Stop
🏷️ No placeholders	🛑 Stop
📊 Excel does not exist	🛑 Stop
❌ File is not Excel	🛑 Stop
❌ Required Excel column missing	🛑 Stop
❌ Excel has no records	🛑 Stop
❌ Required value is blank	🛑 Stop
✅ All validation passes	📄 Generate documents
➕ Extra Excel columns	Ignore
📄 Original template	Never modify
📦 Output

Generated documents are stored inside:

output/

Example:

output/
│
├── 📄 Record_1_1.docx
├── 📄 Record_2_2.docx
├── 📄 Record_3_3.docx
├── 📄 Record_4_4.docx
└── 📄 Record_5_5.docx

The exact filename currently depends on the available optional filename logic.

The generated document contents are populated using the matching Excel values.

⚠️ Current Known Limitation

The current output filename logic checks specifically for an uppercase:

NAME

column.

Therefore, when the Excel file contains:

Name

the generated document may currently use a fallback filename such as:

Record_1_1.docx

instead of:

Ananya Reddy_1.docx

This does not affect the actual mail-merge replacement.

A future improvement will make filename detection for Name, name, and NAME case-insensitive while keeping the field optional.

🧩 Implementation Limitation

The current placeholder detection reads the DOCX XML and searches for placeholder text.

Microsoft Word can sometimes split visible text across multiple XML runs.

For example:

{{Name}}

may internally be stored as multiple XML fragments.

In such cases, the current implementation may not detect the placeholder correctly.

A future version can implement more robust Word paragraph/run-level placeholder detection.

💡 Example Use Cases

Because the fields are dynamic, the same agent can be used for:

📜 Certificates
💼 Appointment letters
📨 Offer letters
👨‍🎓 Student documents
👩‍💼 Employee documents
🎫 Event documents
🏆 Participation certificates
📚 Training completion documents
💌 Invitations
📢 Personalized notices
🏢 Office documents
📄 Bulk document generation

The template determines the fields for each task.

🔐 Security

The Google API key must not be committed to Git.

Use:

.env

for local configuration.

Make sure .gitignore contains:

.env

Generated documents can also be excluded from Git:

output/
📊 Version 2 Status
✅ Completed

Generic mail-merge design

Dynamic DOCX placeholder detection

Dynamic Excel column detection

DOCX validation

Excel validation

Missing-column validation

Blank-value validation

Extra-column handling

Multiple-record document generation

DOCX placeholder replacement

Original-template protection

Output directory handling

Google ADK agent integration

Root agent verification

Local successful-generation testing

Missing-column testing

Missing-value testing

ADK Web startup testing

ADK Web agent response testing

ADK Web upload workflow setup

Gemini quota limitation identified

🔄 Future Improvements

Complete ADK Web file-upload generation after API quota becomes available

Make output filename detection case-insensitive

Improve DOCX placeholder detection across Word XML runs

Add automated unit tests

Improve generated-file download handling

Add ZIP generation for multiple documents

Improve error reporting

Add support for more document formats

Improve special-character handling in filenames

👩‍💻 Project

Generic Mail Merge Agent — Version 2

Built with:

🐍 Python
🤖 Google ADK
✨ Gemini
📊 Pandas
📄 DOCX
📑 Excel

Automating repetitive document generation through a generic AI-powered mail-merge workflow.

Version 2 is the generic evolution of the original Mail Merge Certificate Agent.
