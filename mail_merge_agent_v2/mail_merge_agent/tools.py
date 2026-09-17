from pathlib import Path
import re
import zipfile

import pandas as pd


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Generated certificates will be saved here
OUTPUT_DIR = BASE_DIR / "output"


def read_docx_xml(docx_path: Path) -> str:
    """
    Read XML content from a DOCX file.
    """

    with zipfile.ZipFile(docx_path, "r") as zip_file:

        xml_parts = []

        for file_name in zip_file.namelist():

            if file_name.endswith(".xml"):

                try:
                    xml_text = zip_file.read(
                        file_name
                    ).decode("utf-8")

                    xml_parts.append(xml_text)

                except UnicodeDecodeError:
                    pass

        return "\n".join(xml_parts)


def find_placeholders(template_path: str) -> list[str]:
    """
    Find placeholders in the form:

        {{FIELD_NAME}}

    from the uploaded DOCX template.
    """

    path = Path(template_path)

    if not path.exists():
        return []

    try:
        xml_text = read_docx_xml(path)

    except Exception:
        return []

    # Find placeholders such as:
    # {{NAME}}
    # {{ROLL_NO}}
    # {{COURSE}}
    # {{DATE}}

    placeholders = re.findall(
        r"\{\{([A-Za-z0-9_ ]+)\}\}",
        xml_text
    )

    # Convert to complete placeholder format
    placeholders = [
        "{{" + placeholder + "}}"
        for placeholder in placeholders
    ]

    # Remove duplicates while preserving order
    unique_placeholders = list(
        dict.fromkeys(placeholders)
    )

    return unique_placeholders


def validate_certificate_template(
    template_path: str
) -> str:
    """
    Validate the uploaded certificate template.
    """

    path = Path(template_path)

    if not path.exists():

        return (
            f"Certificate template not found: {path}"
        )

    if path.suffix.lower() != ".docx":

        return (
            "Validation failed. "
            "The certificate template must be a .docx file."
        )

    try:

        placeholders = find_placeholders(
            str(path)
        )

    except Exception as e:

        return (
            "Could not read certificate template: "
            f"{e}"
        )

    if not placeholders:

        return (
            "Template validation failed.\n\n"
            "No placeholders were found in the "
            "certificate template.\n\n"
            "Please add placeholders using this format:\n"
            "{{FIELD_NAME}}\n\n"
            "For example:\n"
            "{{NAME}}\n"
            "{{ID}}\n"
            "{{COURSE}}"
        )

    return (
        "Template validation successful.\n\n"
        "Placeholders found:\n"
        + "\n".join(placeholders)
    )


def validate_excel_file(
    excel_path: str,
    required_columns: list[str]
) -> str:
    """
    Validate the uploaded Excel file.

    Only columns used by the certificate template
    are required.
    """

    path = Path(excel_path)

    if not path.exists():

        return (
            f"Excel file not found: {path}"
        )

    if path.suffix.lower() not in [
        ".xlsx",
        ".xls"
    ]:

        return (
            "Validation failed. "
            "The student data file must be an Excel file."
        )

    try:

        df = pd.read_excel(path)

    except Exception as e:

        return (
            f"Could not read Excel file: {e}"
        )

    # Check required columns
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        return (
            "Excel validation failed.\n\n"
            "The following columns are missing:\n"
            + "\n".join(missing_columns)
        )

    if df.empty:

        return (
            "Excel validation failed.\n\n"
            "The Excel file contains no records."
        )

    # Check blank values
    missing_values = []

    for index, row in df.iterrows():

        missing_fields = []

        for column in required_columns:

            value = row[column]

            if pd.isna(value) or not str(value).strip():

                missing_fields.append(column)

        if missing_fields:

            missing_values.append(
                f"Row {index + 2}: "
                + ", ".join(missing_fields)
            )

    if missing_values:

        return (
            "Excel validation failed.\n\n"
            "The following required values are missing:\n"
            + "\n".join(missing_values)
            + "\n\n"
            "No certificates should be generated."
        )

    return (
        "Excel validation successful.\n\n"
        f"Found {len(df)} records.\n"
        "All required values are filled."
    )


def replace_in_docx_xml(
    input_file: Path,
    output_file: Path,
    replacements: dict[str, str]
):
    """
    Replace placeholders inside DOCX XML.
    """

    with zipfile.ZipFile(
        input_file,
        "r"
    ) as zin:

        with zipfile.ZipFile(
            output_file,
            "w",
            zipfile.ZIP_DEFLATED
        ) as zout:

            for item in zin.infolist():

                data = zin.read(
                    item.filename
                )

                if item.filename.endswith(".xml"):

                    try:

                        text = data.decode(
                            "utf-8"
                        )

                        for old_text, new_text in replacements.items():

                            text = text.replace(
                                old_text,
                                new_text
                            )

                        data = text.encode(
                            "utf-8"
                        )

                    except UnicodeDecodeError:
                        pass

                zout.writestr(
                    item,
                    data
                )


def generate_certificates(
    template_path: str,
    excel_path: str
) -> str:
    """
    Generate certificates using a DOCX template
    and an Excel file.

    Placeholders in the DOCX must match Excel
    column names.

    Example:

        {{NAME}}  -> NAME
        {{ID}}    -> ID
    """

    template = Path(template_path)
    excel = Path(excel_path)

    # ------------------------------------------
    # 1. Validate template
    # ------------------------------------------

    template_result = validate_certificate_template(
        str(template)
    )

    if not template_result.startswith(
        "Template validation successful"
    ):

        return (
            "Certificate generation stopped.\n\n"
            + template_result
        )

    # ------------------------------------------
    # 2. Find placeholders
    # ------------------------------------------

    placeholders = find_placeholders(
        str(template)
    )

    # Convert:
    # {{NAME}} -> NAME
    # {{ROLL_NO}} -> ROLL_NO

    required_columns = [
        placeholder[2:-2]
        for placeholder in placeholders
    ]

    # ------------------------------------------
    # 3. Validate Excel
    # ------------------------------------------

    excel_result = validate_excel_file(
        str(excel),
        required_columns
    )

    if not excel_result.startswith(
        "Excel validation successful"
    ):

        return (
            "Certificate generation stopped.\n\n"
            + excel_result
        )

    # ------------------------------------------
    # 4. Read Excel
    # ------------------------------------------

    try:

        df = pd.read_excel(
            excel
        )

    except Exception as e:

        return (
            "Could not read Excel file: "
            f"{e}"
        )

    # ------------------------------------------
    # 5. Create output directory
    # ------------------------------------------

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    generated_files = []

    # ------------------------------------------
    # 6. Generate certificates
    # ------------------------------------------

    for index, row in df.iterrows():

        replacements = {}

        for placeholder in placeholders:

            column_name = placeholder[2:-2]

            value = str(
                row[column_name]
            ).strip()

            replacements[
                placeholder
            ] = value

        # Use NAME if available for filename.
        # Otherwise use row number.

                # Use a Name column for the filename if available.
        # The column check is case-insensitive.
        # This does not affect placeholder matching.

        name_column = next(
            (
                column
                for column in df.columns
                if str(column).strip().lower() == "name"
            ),
            None
        )

        if name_column:

            name = str(
                row[name_column]
            ).strip()

            if not name or name.lower() == "nan":

                name = f"Record_{index + 1}"

        else:

            name = f"Record_{index + 1}"

        # Make filename safe

        safe_name = "".join(
            character
            if character.isalnum()
            or character in " _-"
            else "_"
            for character in name
        ).strip()

        output_file = (
            OUTPUT_DIR
            / f"{safe_name}_{index + 1}.docx"
        )

        replace_in_docx_xml(
            template,
            output_file,
            replacements
        )

        generated_files.append(
            str(output_file)
        )

    # ------------------------------------------
    # 7. Final response
    # ------------------------------------------

    if not generated_files:

        return (
            "No certificates were generated."
        )

    return (
        f"Successfully generated "
        f"{len(generated_files)} certificates.\n\n"
        + "\n".join(generated_files)
    )
