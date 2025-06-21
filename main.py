import base64
import json
import os
import random
import subprocess


def lambda_handler(event, context):
    try:
        # NOTE: Set up basic input paths
        binary_path = os.path.join(os.sep, "var", "task", "typst")
        # TODO: Make this name unique so there's no risk of conflict
        output_pdf_path = os.path.join(os.sep, "tmp", "output.pdf")
        input_pdf_path = os.path.join(os.sep, "var", "task", "input.typ")
        # TODO: We currently have to set this to allow us to download the suiji library, should we pre-cache this?
        typst_storage_path = os.path.join(os.sep, "tmp")

        # TODO: Support input so that these aren't hardcoded
        question_count = 100
        max_question_length = 10

        command = [
            binary_path,
            "compile",
            input_pdf_path,
            output_pdf_path,
            "--input",
            f"count_seed={random.randint(0, 1000)}",
            "--input",
            f"length_seed={random.randint(0, 1000)}",
            "--input",
            f"questions={question_count}",
            "--input",
            f"question_length={max_question_length}",
            "--package-path",
            typst_storage_path,
            "--package-cache-path",
            typst_storage_path,
        ]

        result = subprocess.run(command, check=True, capture_output=True, text=True)

        if result.stdout:
            print(f"Binary stdout: {result.stdout}")
        if result.stderr:
            print(f"Binary stderr: {result.stderr}")

        with open(output_pdf_path, "rb") as f:
            pdf_content = f.read()

        pdf_base64 = base64.b64encode(pdf_content).decode("utf-8")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/pdf",
                "Content-Disposition": 'attachment; filename="output.pdf"',  # TODO: Add a nicer output name
            },
            "body": pdf_base64,
            "isBase64Encoded": True,
        }

    except subprocess.CalledProcessError as e:
        print(f"Binary execution failed: {e.cmd}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error running binary: {e.stderr}"),
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Internal server error: {str(e)}"),
        }
