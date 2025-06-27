import shutil
import sys
from pathlib import Path

from convert import markdown_to_html_node


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    src = Path("static")
    dest = Path("docs")
    content_dir = Path("content")
    template_path = Path("template.html")

    if dest.exists() and dest.is_dir():
        shutil.rmtree(dest)

    copy_static_to_public(src, dest)

    generate_pages_recursive(content_dir, dest, template_path, basepath)


def copy_static_to_public(src_dir, dest_dir):
    if dest_dir.exists() and dest_dir.is_dir():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    for item in src_dir.iterdir():
        src_item = item
        dest_item = dest_dir / item.name
        if item.is_dir():
            copy_static_to_public(src_item, dest_item)
        else:
            shutil.copy2(src_item, dest_item)


def extract_title(markdown):
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 title found")


def generate_pages_recursive(content_dir, dest_dir, template_path, basepath):
    for md_path in content_dir.rglob("*.md"):
        rel_path = md_path.relative_to(content_dir)
        html_path = dest_dir / rel_path.with_suffix(".html")
        generate_page(
            from_path=md_path,
            template_path=template_path,
            dest_path=html_path,
            basepath=basepath,
        )


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    with open(template_path, "r", encoding="utf-8") as file:
        template_content = file.read()

    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    page_content = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_content
    )

    page_content = page_content.replace('href="/', f'href="{basepath}')
    page_content = page_content.replace('src="/', f'src="{basepath}')

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(page_content)


if __name__ == "__main__":
    main()
