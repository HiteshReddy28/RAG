from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
from bs4.element import Tag

def uscis_extract(html_content: str) -> str:
    """Extract readable text from a USCIS HTML page.

    This function tries to find a <main> element (or element with id="main-content").
    If none is found it falls back to the document <body> or the full soup. It
    also guards against None and non-Tag descendants.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find("main") or soup.find(id="main-content")

    # Fall back to <body> or the full soup if main content isn't present
    if main_content is None:
        main_content = soup.body or soup

    def extract_table(table_tag: Tag) -> str:
        rows = []
        for tr in table_tag.find_all("tr"):
            cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            rows.append(" | ".join(cells))
        return "\n".join(rows)

    content = []

    # iterate only over Tag descendants to avoid text/node attributes without .name
    for element in main_content.descendants:
        if not isinstance(element, Tag):
            continue

        if element.name in ["h1", "h2", "h3"]:
            text = element.get_text(strip=True)
            if text:
                content.append(f"{element.name.upper()}: {text}")
        elif element.name == "p":
            text = element.get_text(strip=True)
            if text:
                content.append(text)
        elif element.name in ["ul", "ol"]:
            for li in element.find_all("li"):
                li_text = li.get_text(strip=True)
                if li_text:
                    content.append(f"- {li_text}")
        elif element.name == "table":
            table_text = extract_table(element)
            if table_text:
                content.append(f"TABLE:\n{table_text}")

    all_text = "\n\n".join(content)

    return all_text