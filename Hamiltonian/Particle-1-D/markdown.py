import json
import sys

def generate_markdown(data: dict) -> str:
    """
    Convert the JSON data into a formatted markdown string.
    """

    md_lines = []

    for account, engines in data.items():
        md_lines.append(f"# Account: {account}\n")

        for engine_name, categories in engines.items():
            md_lines.append(f"## Scan Engine: {engine_name}\n")

            for category, items in sorted(categories.items()):
                # items is a dict → count keys
                count = len(items) if isinstance(items, dict) else 0

                # category label formatting
                label = category.replace("_", " ").title()

                # special renames from your HTML example
                SPECIAL = {
                    "scanerror": "Failed to fetch scan",
                    "tolerated-unsupported": "Tolerated Unsupported"
                }
                if category in SPECIAL:
                    label = SPECIAL[category]

                md_lines.append(f"- **{label}** - {count}")

            md_lines.append("")  # spacing after each scan engine

        md_lines.append("\n---\n")  # separator between accounts

    return "\n".join(md_lines)


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_scan_report.py <input.json> <output.md>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r") as f:
        data = json.load(f)

    md_text = generate_markdown(data)

    with open(output_file, "w") as f:
        f.write(md_text)

    print(f"Markdown file generated: {output_file}")


if __name__ == "__main__":
    main()

