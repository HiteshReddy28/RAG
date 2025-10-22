from bs4 import BeautifulSoup
import requests

def uscis_extract(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find("main") or soup.find(id="main-content")

    for tag in main_content(["script", "style", "noscript", "header", "footer"]):
        tag.extract()

    def extract_table(table_tag):
        rows = []
        for tr in table_tag.find_all("tr"):
            cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            rows.append(" | ".join(cells))  
        return "\n".join(rows)

    content = []
    for element in main_content.descendants:
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