from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            title = line[1:].strip()
            return title
    raise ValueError("Could not extract title")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as markdown_file:
       markdown = markdown_file.read()

    with open(template_path, "r") as template_file:
       template = template_file.read()

    node = markdown_to_html_node(markdown)
    html = node.to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    with open(dest_path, "w") as dest_file:
        dest_file.write(template)
