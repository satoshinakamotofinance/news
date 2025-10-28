import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def display_news_from_sites(sites):
    max_items = 15
    min_words = 10

    base_html = """
    <html>
    <head>
      <style>
        body {
          font-family: 'Georgia', Georgia, serif;
          background: #f9f9f9;
          margin: 0; padding: 0;
          color: #555;
        }
        .news-source-card {
          background: white;
          border-radius: 10px;
          box-shadow: 0 2px 5px rgba(0,0,0,0.1);
          margin: 20px auto;
          max-width: 900px;
          padding: 15px 25px;
        }
        .news-source-title {
          font-size: 28px;
          font-weight: 700;
          margin-bottom: 20px;
          border-bottom: 3px solid #444;
          padding-bottom: 10px;
          color: #222;
        }
        .news-card {
          display: flex;
          flex-direction: row;
          margin-bottom: 18px;
          border-bottom: 1px solid #ddd;
          padding-bottom: 12px;
        }
        .news-content h3 {
          margin: 0 0 6px 0;
          font-size: 1.0rem;
          font-weight: 400;
        }
        .news-content h3 a {
          color: black;
          text-decoration: none;
        }
        .news-content h3 a:hover {
          text-decoration: underline;
        }
        .news-date {
          font-size: 0.85rem;
          color: #888;
          margin-bottom: 6px;
        }
        @media (max-width: 600px) {
          .news-card {
            flex-direction: column;
          }
        }
      </style>
    </head>
    <body>
    """

    html_content = base_html

    for website_name, website_url in sites:
        try:
            response = requests.get(website_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            news_items = soup.find_all('article')
            if not news_items:
                news_container = (soup.find('div', class_='news-list') or
                                  soup.find('ul', class_='news-items') or
                                  soup.find('div', class_='news-items'))
                if news_container:
                    news_items = news_container.find_all('li')

            headlines = []
            for item in news_items:
                if len(headlines) >= max_items:
                    break
                link = item.find('a', href=True)
                if link:
                    text = link.text.strip()
                    if len(text.split()) >= min_words:
                        headlines.append((text, urljoin(website_url, link['href'])))

            if not headlines:
                all_links = soup.find_all("a", href=True)
                header_links = soup.find_all("header")
                footer_links = soup.find_all("footer")

                valid_links = []
                for link in all_links:
                    if link in header_links or link in footer_links:
                        continue
                    text = link.text.strip()
                    if len(text.split()) >= min_words:
                        valid_links.append(link)
                    if len(valid_links) >= max_items:
                        break
                headlines = [(link.text.strip(), urljoin(website_url, link['href'])) for link in valid_links]

            if not headlines:
                html_content += f'<div class="news-source-card"><div class="news-source-title">{website_name}</div><p>No relevant news found.</p></div>'
                continue

            html_content += f'<div class="news-source-card"><div class="news-source-title">{website_name}</div>'

            visible_count = 7
            for title, link in headlines[:visible_count]:
                html_content += f'''
                <div class="news-card">
                  <div class="news-content">
                    <h3><a href="{link}" target="_blank" rel="noopener">{title}</a></h3>
                  </div>
                </div>'''

            if len(headlines) > visible_count:
                html_content += f'''
                <details>
                  <summary>Show {len(headlines) - visible_count} more...</summary>'''
                for title, link in headlines[visible_count:]:
                    html_content += f'''
                    <div class="news-card">
                      <div class="news-content">
                        <h3><a href="{link}" target="_blank" rel="noopener">{title}</a></h3>
                      </div>
                    </div>'''
                html_content += '</details>'

            html_content += '</div>'

        except requests.exceptions.RequestException as e:
            html_content += f'<div class="news-source-card"><div class="news-source-title">{website_name}</div><p>Error fetching news: {e}</p></div>'

    html_content += "</body></html>"

    components.html(html_content, height=22000)

def main():

    st.title("NEWS")
    tab_globe, tab_commnews, tab_gaap,tab_tax2 = st.tabs([
        "Global", "Commodities", "GAAP", "Tax"])

    with tab_tax2:

        tax_websites = [
            ("KPMG Tax Flash", "https://kpmg.com/in/en/services/tax/flash-news.html"),
            ("Tax Foundation (Tax)", "https://taxfoundation.org/"),
            ("Canada Revenue Agency (CRA) (Tax)", "https://www.canada.ca/en/revenue-agency.html"),
            ("H&R Block Canada (Tax)", "https://www.hrblock.ca/"),
            ("HMRC (Her Majesty’s Revenue and Customs) (Tax)", "https://www.gov.uk/government/organisations/hm-revenue-customs"),
            ("Taxation.co.uk (Tax)", "https://www.taxation.co.uk/"),
            ("Chartered Institute of Taxation (CIOT) (Tax)", "https://www.tax.org.uk/"),
            ("CPA Australia (Tax)", "https://www.cpaaustralia.com.au/"),
        ]
        display_news_from_sites(tax_websites)

    with tab_gaap:

        gaap_websites = [
            ("Financial Reporting Council (FRC)", "https://www.frc.org.uk/news-and-events/news/"),
            ("Canadian Public Accountability Board (CPAB)", "https://cpab-ccrc.ca/media/news-release"),
            ("Australian Accounting Standards Board (AASB)", "https://aasb.gov.au/news/"),
            ("Institute of Chartered Accountants of India (ICAI)", "https://www.icai.org/category/announcements"),
        ]
        display_news_from_sites(gaap_websites)



    with tab_commnews:

        html_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1.0" />
          <title>Global News Aggregator</title>
          <style>
            body {
              font-family: 'Georgia', Georgia, serif;
              background: #f9f9f9;
              margin: 0;
              padding: 0;
            }
            header {
              background: white;
              padding: 20px;
              text-align: center;
              font-size: 2rem;
              border-bottom: 1px solid #ddd;a
            }
            #category-buttons {
              display: flex;
              flex-wrap: wrap;
              justify-content: center;
              background: #fff;
              border-bottom: 1px solid #ddd;
            }
            .category-btn {
              margin: 10px;
              padding: 10px 20px;
              background: #eee;
              border: none;
              border-radius: 5px;
              cursor: pointer;
              font-size: 1rem;
              transition: background 0.3s;
            }
            .category-btn:hover {
              background: #ccc;
            }
            .news-section {
              padding: 20px;
              max-width: 1200px;
              margin: auto;
            }
            .category-header {
              font-size: 1.5rem;
              border-bottom: 2px solid #333;
              padding-bottom: 5px;
              margin-top: 40px;
            }
            .news-card {
              display: flex;
              flex-direction: row;
              background: white;
              border-radius: 10px;
              margin: 15px 0;
              box-shadow: 0 2px 5px rgba(0,0,0,0.1);
              overflow: hidden;
            }
            .news-content {
              padding: 15px;
              flex: 1;
            }
            .news-content h3 {
              margin: 0;
              font-size: 1.2rem;
            }
            .news-content a {
              color: #333;
              text-decoration: none;
            }
            .news-content a:hover {
              text-decoration: underline;
            }
            .news-date {
              color: #888;
              font-size: 0.9rem;
              margin: 5px 0;
            }
            .news-summary {
              font-size: 1rem;
              color: #555;
            }
            @media (max-width: 600px) {
              .news-card {
                flex-direction: column;
              }
            }
          </style>
        </head>
        <body>
        
        <div id="category-buttons"></div>
        
        <div id="news-container" class="news-section"></div>
        
        <script>
          const feedsByCategory = {
        
            "Commodities & Energy Markets": [
              "https://www.kitco.com/rss/news.xml",
              "https://www.mining.com/feed/",
              "https://www.marketwatch.com/rss/commodities",
              "https://goldseek.com/rss.xml",
              "https://www.bullionvault.com/rss.xml",
              "https://www.marketwatch.com/rss/gold",
              "https://www.investing.com/rss/news_1.rss",
              "https://www.fxstreet.com/rss/news",
              "https://www.silverdoctors.com/feed/",
              "https://www.gold-eagle.com/rss.xml",
              "https://www.marketwatch.com/rss/silver",
              "https://www.silverinstitute.org/feed/",
              "https://www.moneycontrol.com/rss/MCtopnews.xml",
              "https://www.rigzone.com/news/rss/",
              "https://feeds.marketwatch.com/marketwatch/energy",
              "https://www.energyvoice.com/feed/",
              "https://www.oilandgasonline.com/rss",
              "https://www.oilandgasiq.com/rss.xml",
              "https://www.reuters.com/business/energy/rss",
              "https://www.nasdaq.com/feed/rssoutbound?category=Energy",
              "https://www.naturalgasintel.com/feed/",
              "https://www.eia.gov/rss/news.xml",
              "https://www.ogj.com/rss",
              "https://oilprice.com/rss/main",
              "https://www.barchart.com/rss/news/energy",
              "https://www.marketwatch.com/rss/natural-gas",
              "https://copperinvestingnews.com/feed",
              "https://www.marketwatch.com/rss/copper",
              "https://www.metalbulletin.com/rss",
              "https://www.lme.com/en/rss",
              "https://www.graincentral.com/feed/",
              "https://www.marketwatch.com/rss/corn",
              "https://www.dtnpf.com/agriculture/web/ag/news/rss",
              "https://www.marketwatch.com/rss/wheat",
              "https://www.fxstreet.com/rss/news/wheat",
              "https://www.marketwatch.com/rss/soybeans",
              "https://www.barchart.com/rss/news/grains",
              "https://www.world-grain.com/rss",
              "https://www.foodnavigator.com/RSS/Processing-Packaging/Sugar",
              "https://www.agrimarketing.com/rss.xml",
              "https://www.marketwatch.com/rss/sugar",
              "https://www.dailycoffeenews.com/feed/",
              "https://www.nasdaq.com/feed/rssoutbound?category=Commodities",
              "https://www.financialexpress.com/market/commodities/feed/",
              "https://www.investing.com/rss/news_301.rss",
              "https://www.business-standard.com/rss/markets-commodities.rss",
              "https://www.marketwatch.com/rss/coffee",
              "https://www.foodnavigator.com/RSS/Commodities/Coffee",
              "https://www.agriculture.com/rss.xml",
              "https://www.agweb.com/rss/news",
              "https://www.kitco.com/rss/base-metals.xml",
              "https://www.agri-pulse.com/rss/topics/95-corn",
              "https://www.feednavigator.com/RSS/Feed-Grains/Corn",
              "https://www.feednavigator.com/RSS/Feed-Grains/Wheat",
              "https://www.reuters.com/rssFeed/wheatNews",
              "https://www.feednavigator.com/RSS/Feed-Grains/Soybeans",
              "https://www.reuters.com/rssFeed/soybeansNews",
              "https://www.reuters.com/rssFeed/sugarNews",
              "https://www.reuters.com/rssFeed/coffeeNews",
              "https://www.agriculture.com/rss/topic/89500",
              "https://www.agri-pulse.com/rss/topics/97-soybeans",
              "https://www.miningweekly.com/page/platinum/feed",
              "https://www.miningweekly.com/page/palladium/feed",
              "https://www.barchart.com/rss/news/softs"
            ]
          };
        
          const categoryButtonsDiv = document.getElementById('category-buttons');
          const newsContainer = document.getElementById('news-container');
        
          // Generate category buttons
          Object.keys(feedsByCategory).forEach(category => {
            const btn = document.createElement('button');
            btn.className = 'category-btn';
            btn.innerText = category;
            btn.onclick = () => filterCategory(category);
            categoryButtonsDiv.appendChild(btn);
          });
        
          // Render all categories initially
          Object.keys(feedsByCategory).forEach(category => renderCategory(category));
        
          function filterCategory(category) {
            const sections = document.querySelectorAll('.news-category');
            sections.forEach(section => {
              if (section.dataset.category === category) {
                section.style.display = 'block';
                section.scrollIntoView({ behavior: 'smooth' });
              } else {
                section.style.display = 'none';
              }
            });
          }
        
          function renderCategory(category) {
            const sectionDiv = document.createElement('div');
            sectionDiv.className = 'news-category';
            sectionDiv.dataset.category = category;
            sectionDiv.innerHTML = `<div class="category-header">${category}</div>`;
            newsContainer.appendChild(sectionDiv);
        
            feedsByCategory[category].forEach(feedUrl => {
              const apiUrl = `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(feedUrl)}`;
        
              fetch(apiUrl)
                .then(response => response.json())
                .then(data => {
                  if (data.status === "ok") {
                    const now = new Date();
                    const threeDaysAgo = new Date();
                    threeDaysAgo.setDate(now.getDate() - 2);
        
                    data.items.forEach(item => {
                      const pubDate = new Date(item.pubDate);
                      if (pubDate >= threeDaysAgo && pubDate <= now) {
                        const card = document.createElement('div');
                        card.className = 'news-card';
        
                        const summary = item.description ? item.description.replace(/(<([^>]+)>)/gi, "").slice(0, 150) + "..." : "";
                        const date = pubDate.toLocaleDateString();
        
                        let contentHTML = `
                          <div class="news-content">
                            <h3><a href="${item.link}" target="_blank">${item.title}</a></h3>
                            <div class="news-date">${date}</div>
                            <div class="news-summary">${summary}</div>
                          </div>
                        `;
        
                        const imgSrc = item.thumbnail || item.enclosure?.link;
                        if (imgSrc) {
                          card.innerHTML = `
                            <img src="${imgSrc}" alt="News Image" style="width:150px;object-fit:cover;" />
                            ${contentHTML}
                          `;
                        } else {
                          card.innerHTML = contentHTML;
                        }
        
                        sectionDiv.appendChild(card);
                      }
                    });
                  }
                })
                .catch(error => {
                  console.error("Error fetching feed:", feedUrl, error);
                });
            });
          }
        </script>
        
        </body>
        </html>
        """
        components.html(html_code, height=22000)

    with tab_globe:

        html_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1.0" />
          <title>Global News Aggregator</title>
          <style>
            body {
              font-family: 'Georgia', Georgia, serif;
              background: #f9f9f9;
              margin: 0;
              padding: 0;
            }
            header {
              background: white;
              padding: 20px;
              text-align: center;
              font-size: 2rem;
              border-bottom: 1px solid #ddd;
            }
            #category-buttons {
              display: flex;
              flex-wrap: wrap;
              justify-content: center;
              background: #fff;
              border-bottom: 1px solid #ddd;
            }
            .category-btn {
              margin: 10px;
              padding: 10px 20px;
              background: #eee;
              border: none;
              border-radius: 5px;
              cursor: pointer;
              font-size: 1rem;
              transition: background 0.3s;
            }
            .category-btn:hover {
              background: #ccc;
            }
            .news-section {
              padding: 20px;
              max-width: 1200px;
              margin: auto;
            }
            .category-header {
              font-size: 1.5rem;
              border-bottom: 2px solid #333;
              padding-bottom: 5px;
              margin-top: 40px;
            }
            .news-card {
              display: flex;
              flex-direction: row;
              background: white;
              border-radius: 10px;
              margin: 15px 0;
              box-shadow: 0 2px 5px rgba(0,0,0,0.1);
              overflow: hidden;
            }
            .news-content {
              padding: 15px;
              flex: 1;
            }
            .news-content h3 {
              margin: 0;
              font-size: 1.2rem;
            }
            .news-content a {
              color: #333;
              text-decoration: none;
            }
            .news-content a:hover {
              text-decoration: underline;
            }
            .news-date {
              color: #888;
              font-size: 0.9rem;
              margin: 5px 0;
            }
            .news-summary {
              font-size: 1rem;
              color: #555;
            }
            @media (max-width: 600px) {
              .news-card {
                flex-direction: column;
              }
            }
          </style>
        </head>
        <body>
        
        <header>Global News</header>
        
        <div id="category-buttons"></div>
        
        <div id="news-container" class="news-section"></div>
        
        <script>
          const feedsByCategory = {
            "Business & Markets": [
              "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
              "https://rss.cnn.com/rss/money_markets.rss",
              "https://www.cnbc.com/id/100003114/device/rss/rss.html",
              "https://www.ft.com/?format=rss",
              "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
              "https://www.thehindubusinessline.com/markets/?service=rss",
              "https://www.marketwatch.com/rss/topstories",
              "https://www.bloomberg.com/feed/podcast/bloomberg-businessweek.xml"
            ],
            "World News": [
              "https://rss.cnn.com/rss/edition_world.rss",
              "http://feeds.bbci.co.uk/news/world/rss.xml",
              "https://www.aljazeera.com/xml/rss/all.xml",
              "https://www.theguardian.com/world/rss",
              "https://www.reutersagency.com/feed/?best-topics=world&post_type=best",
              "https://www.npr.org/rss/rss.php?id=1004",
              "https://www.latimes.com/world/rss2.0.xml"
            ],
            "US News": [
              "http://rss.cnn.com/rss/edition_us.rss",
              "http://feeds.foxnews.com/foxnews/national",
              "https://www.npr.org/rss/rss.php?id=1001",
              "https://feeds.a.dj.com/rss/RSSUSNews.xml",
              "https://www.usnews.com/rss/news",
              "https://www.nbcnews.com/id/3032091/device/rss/rss.xml"
            ],
            "Europe News": [
              "https://www.euronews.com/rss?level=theme&name=news",
              "https://rss.dw.com/rdf/rss-en-europe",
              "http://feeds.bbci.co.uk/news/world/europe/rss.xml",
              "https://www.theguardian.com/world/europe-news/rss",
              "https://www.france24.com/en/rss",
              "https://www.economist.com/europe/rss.xml"
            ],
            "Asia News": [
              "https://www.thehindu.com/news/international/feeder/default.rss",
              "https://www.scmp.com/rss/91/feed",
              "https://www.japantimes.co.jp/news/feed/",
              "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
              "https://www.channelnewsasia.com/rssfeeds/8395986",
              "https://www.koreatimes.co.kr/www/rss/rss.xml"
            ],
            "Africa News": [
              "https://allafrica.com/tools/headlines/rdf/latest/headlines.rdf",
              "http://feeds.bbci.co.uk/news/world/africa/rss.xml",
              "https://www.aljazeera.com/xml/rss/all.xml?subsection=africa",
              "https://www.news24.com/rss",
              "https://www.africanews.com/feed/rss"
            ],
            "Latin America News": [
              "http://feeds.bbci.co.uk/news/world/latin_america/rss.xml",
              "https://www.telesurenglish.net/rss/news.xml",
              "https://www.buenosairesherald.com/feed",
              "https://www.reuters.com/rssFeed/topNews"
            ]
          };
        
          const categoryButtonsDiv = document.getElementById('category-buttons');
          const newsContainer = document.getElementById('news-container');
        
          // Generate category buttons
          Object.keys(feedsByCategory).forEach(category => {
            const btn = document.createElement('button');
            btn.className = 'category-btn';
            btn.innerText = category;
            btn.onclick = () => filterCategory(category);
            categoryButtonsDiv.appendChild(btn);
          });
        
          // Render all categories initially
          Object.keys(feedsByCategory).forEach(category => renderCategory(category));
        
          function filterCategory(category) {
            const sections = document.querySelectorAll('.news-category');
            sections.forEach(section => {
              if (section.dataset.category === category) {
                section.style.display = 'block';
                section.scrollIntoView({ behavior: 'smooth' });
              } else {
                section.style.display = 'none';
              }
            });
          }
        
          function renderCategory(category) {
            const sectionDiv = document.createElement('div');
            sectionDiv.className = 'news-category';
            sectionDiv.dataset.category = category;
            sectionDiv.innerHTML = `<div class="category-header">${category}</div>`;
            newsContainer.appendChild(sectionDiv);
        
            feedsByCategory[category].forEach(feedUrl => {
              const apiUrl = `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(feedUrl)}`;
        
              fetch(apiUrl)
                .then(response => response.json())
                .then(data => {
                  if (data.status === "ok") {
                    const now = new Date();
                    const threeDaysAgo = new Date();
                    threeDaysAgo.setDate(now.getDate() - 2);
        
                    data.items.forEach(item => {
                      const pubDate = new Date(item.pubDate);
                      if (pubDate >= threeDaysAgo && pubDate <= now) {
                        const card = document.createElement('div');
                        card.className = 'news-card';
        
                        const summary = item.description ? item.description.replace(/(<([^>]+)>)/gi, "").slice(0, 150) + "..." : "";
                        const date = pubDate.toLocaleDateString();
        
                        let contentHTML = `
                          <div class="news-content">
                            <h3><a href="${item.link}" target="_blank">${item.title}</a></h3>
                            <div class="news-date">${date}</div>
                            <div class="news-summary">${summary}</div>
                          </div>
                        `;
        
                        const imgSrc = item.thumbnail || item.enclosure?.link;
                        if (imgSrc) {
                          card.innerHTML = `
                            <img src="${imgSrc}" alt="News Image" style="width:150px;object-fit:cover;" />
                            ${contentHTML}
                          `;
                        } else {
                          card.innerHTML = contentHTML;
                        }
        
                        sectionDiv.appendChild(card);
                      }
                    });
                  }
                })
                .catch(error => {
                  console.error("Error fetching feed:", feedUrl, error);
                });
            });
          }
        </script>
        
        </body>
        </html>
        """
        components.html(html_code, height=52000)

if __name__ == "__main__":
    main()
