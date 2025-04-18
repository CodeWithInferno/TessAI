from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from core.llm import llm
from langchain.prompts import PromptTemplate

def perform_search(query, max_results=3):
    print("🌐 Searching...")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"https://www.bing.com/search?q={query.replace(' ', '+')}", timeout=15000)

            # Wait for search result links
            try:
                page.wait_for_selector("li.b_algo h2 a", timeout=7000)
            except:
                print("⚠️ Results may not have loaded properly.")
                return []

            links = page.query_selector_all("li.b_algo h2 a")[:max_results]
            contents = []

            for link in links:
                try:
                    href = link.get_attribute("href")
                    if not href:
                        continue
                    page.goto(href, timeout=10000)
                    page.wait_for_timeout(2000)
                    soup = BeautifulSoup(page.content(), "html.parser")
                    text = soup.get_text(separator="\n")
                    contents.append(text[:2000])
                except:
                    continue

            browser.close()
            return contents if contents else ["No useful results found."]

    except Exception as e:
        print(f"❌ Search failed: {e}")
        return []
    print("🌐 Searching...")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            search_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
            page.goto(search_url, timeout=10000)
            page.wait_for_selector("li.b_algo h2 a", timeout=7000)

            links = page.query_selector_all("li.b_algo h2 a")[:max_results]
            contents = []

            for link in links:
                try:
                    href = link.get_attribute("href")
                    if not href:
                        continue
                    page.goto(href, timeout=10000)
                    page.wait_for_timeout(3000)
                    soup = BeautifulSoup(page.content(), "html.parser")
                    text = soup.get_text(separator="\n")
                    contents.append(text[:2000])
                except:
                    continue

            browser.close()
            return contents

    except Exception as e:
        print("❌ Search failed:", str(e))
        return []
    print("🌐 Searching...")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"https://duckduckgo.com/?q={query.replace(' ', '+')}", timeout=10000)
            page.wait_for_selector("a.result__a", timeout=7000)

            links = page.query_selector_all("a.result__a")[:max_results]
            contents = []

            for link in links:
                try:
                    href = link.get_attribute("href")
                    if not href:
                        continue
                    page.goto(href, timeout=10000)
                    page.wait_for_timeout(3000)
                    soup = BeautifulSoup(page.content(), "html.parser")
                    text = soup.get_text(separator="\n")
                    contents.append(text[:2000])
                except:
                    continue

            browser.close()
            return contents

    except Exception as e:
        print("❌ Search failed:", str(e))
        return []

    print("🌐 Searching...")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.google.com", timeout=10000)
            page.fill("input[name='q']", query)
            page.keyboard.press("Enter")
            page.wait_for_selector("h3", timeout=7000)

            results = page.query_selector_all("h3")[:max_results]
            contents = []

            for h3 in results:
                try:
                    link = h3.evaluate("el => el.parentElement.href")
                    page.goto(link, timeout=10000)
                    page.wait_for_timeout(3000)
                    soup = BeautifulSoup(page.content(), "html.parser")
                    text = soup.get_text(separator="\n")
                    contents.append(text[:2000])
                except:
                    continue

            browser.close()
            return contents

    except Exception as e:
        print("❌ Search failed:", str(e))
        return []

def search_and_summarize(query):
    docs = perform_search(query)
    if not docs:
        return "Couldn't retrieve results. Try again later."

    print("🤖 Summarizing...\n")
    joined = "\n\n".join(docs)
    summary_prompt = PromptTemplate.from_template("Summarize key useful info:\n\n{docs}")
    chain = summary_prompt | llm
    return chain.invoke({"docs": joined}).strip()
