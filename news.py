import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model and tokenizer once
@st.cache_resource(show_spinner=True)


def show_front_page():
    st.markdown(
        """
        <style>
            body {
                background: linear-gradient(180deg, #0e1117 0%, #1b1f24 100%);
                animation: gradientShift 15s ease infinite;
                color: #dfe6e9;
                font-family: 'Helvetica Neue', sans-serif;
                margin: 0;
                padding: 0 15px;
            }
            @keyframes gradientShift {
                0% {background-position: 0% 50%;}
                50% {background-position: 100% 50%;}
                100% {background-position: 0% 50%;}
            }
            .main-title {
                text-align: center;
                font-size: 64px;
                color: #00adb5;
                margin-top: 30px;
                letter-spacing: 2px;
                font-weight: 700;
                text-shadow: 2px 2px 8px rgba(0,173,181,0.4);
            }
            .subtitle {
                text-align: center;
                font-size: 22px;
                color: #B3C3D1;
                margin-top: 15px;
                line-height: 1.6;
                max-width: 900px;
                margin-left: auto;
                margin-right: auto;
            }
            .feature-container {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                margin-top: 50px;
                gap: 20px;
            }
            .feature-card {
                background-color: #1b1f24;
                border: 1px solid rgba(0,173,181,0.3);
                border-radius: 12px;
                padding: 20px;
                width: 250px;
                text-align: center;
                transition: transform 0.3s, box-shadow 0.3s;
                color: #dfe6e9;
            }
            .feature-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 6px 20px rgba(0,173,181,0.5);
            }
            .feature-card h4 {
                color: #00adb5;
                font-size: 20px;
                margin-bottom: 10px;
                font-weight: 600;
            }
            .branding-img {
                display: block;
                margin: 20px auto 10px auto;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0,173,181,0.3);
            }
            .attribution {
                text-align: center;
                margin-top: 40px;
                color: #777;
                font-size: 14px;
            }
            @media (max-width: 768px) {
                .main-title {
                    font-size: 42px;
                }
                .subtitle {
                    font-size: 18px;
                }
                .feature-card {
                    width: 90%;
                }
            }
        </style>

        <div style="text-align:center;">
            <img src="https://www.currencytransfer.com/wp-content/uploads/2023/03/strongest-currencies-in-the-world-1.min_.jpg"
                 class="branding-img"
                 width="220"
                 alt="News App Image"/>
            <h1 class="main-title">Earth Times</h1>
            <p class="subtitle">
                         </p>
        </div>
        
        </div>
            <div class="attribution">
             Developed with ❤️  by CA. Ankit Kotriwala
        
        </div>

        
        """,
        unsafe_allow_html=True
    )


def display_news_from_sites(sites):
    max_items = 15
    min_words = 10

    base_html = """
    <html>
    <head>
      <style>
        body {
          font-family: 'Georgia', serif;
          background: #f9f9f9;
          margin: 0; padding: 20px;
          color: #555;
        }
        .news-source-card {
          background: white;
          border-radius: 10px;
          box-shadow: 0 2px 7px rgba(0,0,0,0.12);
          margin: 20px auto;
          max-width: 900px;
          padding: 20px 30px;
        }
        .news-source-title {
          font-size: 28px;
          font-weight: 700;
          margin-bottom: 25px;
          border-bottom: 3px solid #444;
          padding-bottom: 12px;
          color: #222;
        }
        .news-card {
          display: flex;
          flex-direction: row;
          margin-bottom: 18px;
          border-bottom: 1px solid #ddd;
          padding-bottom: 15px;
          cursor: pointer;
          transition: background 0.3s ease;
        }
        .news-card:hover {
          background: #fafafa;
        }
        .news-content h3 {
          margin: 0 0 6px 0;
          font-size: 1rem;
          font-weight: 500;
          line-height: 1.3;
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
          margin-bottom: 8px;
        }
        /* Responsive adjustments */
        @media (max-width: 600px) {
          .news-card {
            flex-direction: column;
          }
        }
        details {
          margin-top: 10px;
          font-size: 0.95rem;
        }
        summary {
          font-weight: 600;
          color: #333;
          cursor: pointer;
          outline: none;
        }
      </style>
    </head>
    <body>
    """

    html_content = base_html

    for site_name, site_url in sites:
        try:
            response = requests.get(site_url, timeout=10)
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
                        headlines.append((text, urljoin(site_url, link['href'])))

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
                headlines = [(link.text.strip(), urljoin(site_url, link['href'])) for link in valid_links]

            if not headlines:
                html_content += f'<div class="news-source-card"><div class="news-source-title">{site_name}</div><p>No relevant news found.</p></div>'
                continue

            html_content += f'<div class="news-source-card"><div class="news-source-title">{site_name}</div>'

            visible_count = 7
            for title, link in headlines[:visible_count]:
                html_content += f'''
                <div class="news-card" onclick="window.open('{link}', '_blank')">
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
                    <div class="news-card" onclick="window.open('{link}', '_blank')">
                      <div class="news-content">
                        <h3><a href="{link}" target="_blank" rel="noopener">{title}</a></h3>
                      </div>
                    </div>'''
                html_content += '</details>'

            html_content += '</div>'

        except requests.exceptions.RequestException as e:
            html_content += f'<div class="news-source-card"><div class="news-source-title">{site_name}</div><p>Error fetching news: {e}</p></div>'

    html_content += "</body></html>"

    components.html(html_content, height=22000)


def main():
    st.set_page_config(page_title="Best News App of the Decade", layout="wide")

    show_front_page()

    tab_globe, tab_commnews, tab_technology, tab_pods, tab_blogs,tab_books,tab_aiknowledge,tab_travel,tab_music,tab_Radio,tab_sports,tab_trending,tab_food,tab_startups,tab_space,tab_gaming,tab_finance, tab_politics, tab_science, tab_health,tab_editorial = st.tabs([
        "Global", "Commodities", "Technology",   "Pods", "Blogs", "Books", "AiKnowledge","Travel","Music","Radio","Sports","Trending","Food","Startups","Space","Gaming","Finance", "Politics", "Science", "Health",   "Editorial"
    ])

    with tab_technology:
        html_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <!-- TradingView Widget BEGIN -->
            <div class="tradingview-widget-container">
              <div class="tradingview-widget-container__widget"></div>
              <div class="tradingview-widget-copyright">
                <a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank">
                  <span class="blue-text"></span>
                </a>
              </div>
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-tickers.js" async>
              {
              "symbols": [
                {
                  "description": "Apple",
                  "proName": "NASDAQ:AAPL"
                },
                {
                  "description": "Microsoft",
                  "proName": "NASDAQ:MSFT"
                },
                {
                  "description": "NVIDIA",
                  "proName": "NASDAQ:NVDA"
                },
                {
                  "description": "Alphabet Class A",
                  "proName": "NASDAQ:GOOGL"
                },
                {
                  "description": "Amazon",
                  "proName": "NASDAQ:AMZN"
                },
                {
                  "description": "Meta Platforms",
                  "proName": "NASDAQ:META"
                },
                {
                  "description": "Tesla",
                  "proName": "NASDAQ:TSLA"
                },
                {
                  "description": "Broadcom",
                  "proName": "NASDAQ:AVGO"
                },
                {
                  "description": "TSMC",
                  "proName": "NYSE:TSM"
                },
                {
                  "description": "Adobe",
                  "proName": "NASDAQ:ADBE"
                },
                {
                  "description": "Salesforce",
                  "proName": "NYSE:CRM"
                },
                {
                  "description": "ASML",
                  "proName": "NASDAQ:ASML"
                }
              ],
              "isTransparent": false,
              "showSymbolLogo": true,
              "colorTheme": "light",
              "locale": "en"
            }
              </script>
            </div>
            <!-- TradingView Widget END -->

          <meta charset="UTF-8"/>
          <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
          <title>Technology News</title>
          <style>
            body { font-family: 'Georgia', serif; background: #f9f9f9; margin: 0; padding: 0; }
            header { background: white; padding: 20px; text-align: center; font-size: 2rem; border-bottom: 1px solid #ddd; }
            #category-buttons { display: flex; flex-wrap: wrap; justify-content: center; background: #fff; border-bottom: 1px solid #ddd; }
            .category-btn {
              margin: 10px; padding: 10px 20px; background: #eee; border: none; border-radius: 5px;
              cursor: pointer; font-size: 1rem; transition: background 0.3s;
            }
            .category-btn:hover { background: #ccc; }
            .news-section { padding: 20px; max-width: 1200px; margin: auto; }
            .category-header {
              font-size: 1.5rem; border-bottom: 2px solid #333; padding-bottom: 5px; margin-top: 40px;
            }
            .news-card {
              display: flex; flex-direction: row; background: white; border-radius: 10px;
              margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); overflow: hidden;
            }
            .news-content { padding: 15px; flex: 1; }
            .news-content h3 { margin: 0; font-size: 1.2rem; line-height:1.2; }
            .news-content a { color: #333; text-decoration: none; }
            .news-content a:hover { text-decoration: underline; }
            .news-date { color: #888; font-size: 0.9rem; margin: 5px 0; }
            .news-summary { font-size: 1rem; color: #555; }
            @media (max-width: 600px) { .news-card { flex-direction: column; } }
          </style>
        </head>
        <body>
        <div id="category-buttons"></div>
        <div id="news-container" class="news-section"></div>
        <script>
          const feedsByCategory = {
            "Technology News": [

              "https://techcrunch.com/feed/",
              "https://www.theguardian.com/us/technology/rss",
              "https://feeds.arstechnica.com/arstechnica/technology-lab",
              "https://www.reutersagency.com/feed/?best-topics=tech&post_type=best",
              "https://feeds.a.dj.com/rss/RSSWSJD.xml",
              "https://www.ft.com/technology?format=rss",
              "https://www.wired.com/feed/rss",
              "https://www.engadget.com/rss.xml",
              "https://www.techmeme.com/feed.xml",
              "https://www.cnet.com/rss/news/",
              "https://www.gadgets360.com/rss",
              "https://www.techradar.com/rss",
              "https://www.computerweekly.com/rss",
              "https://www.zdnet.com/news/rss.xml",
              "https://venturebeat.com/feed/",
              "https://www.macrumors.com/macrumors.xml",
              "https://arstechnica.com/feed/",
              "https://mashable.com/feed/",
              "https://www.theverge.com/rss/index.xml",
              "https://feeds.feedburner.com/TechCrunch",
              "https://feeds.feedburner.com/Gizmodo/full",
              "https://feeds.feedburner.com/TheNextWeb",
              "https://www.digitaltrends.com/feed/",
              "https://www.linux.com/feed/",
              "https://www.androidcentral.com/feed",
              "https://9to5mac.com/feed/",
              "https://9to5google.com/feed/",
              "https://www.anandtech.com/rss/",
              "https://www.slashdot.org/rss/slashdot.rdf",
              "https://www.extremetech.com/feed",
              "https://www.techspot.com/backend.xml",
              "https://www.howtogeek.com/feed/",
              "https://gizmodo.com/rss",
              "https://lifehacker.com/rss",
              "https://feeds.feedburner.com/AndroidAuthority",
              "https://arstechnica.com/cars/feed/",
              "https://www.makeuseof.com/feed/",
              "https://www.technobuffalo.com/feed",
              "https://www.digitalcitizen.life/feed/",
              "https://www.windowscentral.com/rss.xml",
              "https://www.thewindowsclub.com/feed",
              "https://www.techradar.com/news/rss",
              "https://www.macworld.com/index.rss",
              "https://www.cnet.com/rss/news/",
              "https://thenextweb.com/feed/",
              "https://www.pcgamer.com/rss/",
              "https://www.technewsworld.com/perl/index.rss",
              "http://feeds.feedburner.com/TechRepublic",
              "https://www.techpowerup.com/news-feeds/",
              "https://www.theinformation.com/feed",
              "https://www.idg.com/tools-for-it-professionals/rss-feeds/",
              "https://www.infoq.com/feed/",
              "https://blog.cloudflare.com/feed/",
              "https://www.techspot.com/rss/",
              "https://feed.ethnews.com/",
              "https://www.wired.com/about/rss-feeds/",
              "https://www.pcworld.com/index.rss",
              "https://securityboulevard.com/feed",
              "https://securityledger.com/feed",
              "https://www.darkreading.com/rss.xml",
              "https://www.helpnetsecurity.com/feed/",
              "https://feeds.feedburner.com/TechCrunch/startups",
              "https://www.androidpolice.com/feed/",
              "https://9to5google.com/feed/",
              "https://www.zdnet.com/topic/security/rss.xml",
              "https://www.securityweek.com/rss",
              "https://www.techrepublic.com/rssfeeds/",
              "https://www.infoworld.com/index.rss",
              "https://www.csoonline.com/index.rss",
              "https://www.infosecurity-magazine.com/rss/news/",
              "https://www.databreachtoday.com/rss.xml",
              "https://securityintelligence.com/feed/",
              "https://thehackernews.com/feeds/posts/default",
              "https://www.cyberscoop.com/feed/",
              "https://krebsonsecurity.com/feed/",
              "https://www.techpowerup.com/news-feeds/",
              "https://www.techradar.com/rss",
              "https://www.techgenyz.com/feed/",
              "https://www.maketecheasier.com/feed/",
              "https://www.informationweek.com/rss_simple.asp",
              "https://feeds.feedburner.com/GSM-Argentina",
              "https://www.digitaltrends.com/feed/",
              "https://www.omgubuntu.co.uk/feed",
              "https://www.techspot.com/backend.xml",
              "https://www.extremetech.com/feed",
              "https://www.technewsworld.com/perl/index.rss",
              "https://slashdot.org/rss/slashdot.rdf",
              "https://www.techspot.com/backend.xml",
              "https://www.freecodecamp.org/news/feed/",
              "https://a16z.com/feed/",
              "https://spectrum.ieee.org/rss/fulltext",
              "https://www.inventiva.co.in/feed/",
              "https://www.technologyreview.com/feed/",
              "https://spectrum.ieee.org/robotics/feed",
              "https://bgr.com/feed/"

            ]
          };

          const categoryButtonsDiv = document.getElementById('category-buttons');
          const newsContainer = document.getElementById('news-container');

          Object.keys(feedsByCategory).forEach(category => {
            const btn = document.createElement('button');
            btn.className = 'category-btn';
            btn.innerText = category;
            btn.onclick = () => filterCategory(category);
            categoryButtonsDiv.appendChild(btn);
          });

          Object.keys(feedsByCategory).forEach(category => renderCategory(category));

          function filterCategory(category) {
            const sections = document.querySelectorAll('.news-category');
            sections.forEach(section => {
              section.style.display = (section.dataset.category === category) ? 'block' : 'none';
              if (section.style.display === 'block') section.scrollIntoView({behavior: 'smooth'});
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
                  if(data.status === "ok") {
                    const now = new Date();
                    const threeDaysAgo = new Date();
                    threeDaysAgo.setDate(now.getDate() - 2);

                    data.items.forEach(item => {
                      const pubDate = new Date(item.pubDate);
                      if(pubDate >= threeDaysAgo && pubDate <= now) {
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
                        if(imgSrc) {
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

    with tab_finance:
        html_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8"/>
          <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
          <title>Finance News</title>
          <style>
            body { font-family: 'Georgia', serif; background: #f9f9f9; margin: 0; padding: 0; }
            header { background: white; padding: 20px; text-align: center; font-size: 2rem; border-bottom: 1px solid #ddd; }
            #category-buttons { display: flex; flex-wrap: wrap; justify-content: center; background: #fff; border-bottom: 1px solid #ddd; }
            .category-btn {
              margin: 10px; padding: 10px 20px; background: #eee; border: none; border-radius: 5px;
              cursor: pointer; font-size: 1rem; transition: background 0.3s;
            }
            .category-btn:hover { background: #ccc; }
            .news-section { padding: 20px; max-width: 1200px; margin: auto; }
            .category-header {
              font-size: 1.5rem; border-bottom: 2px solid #333; padding-bottom: 5px; margin-top: 40px;
            }
            .news-card {
              display: flex; flex-direction: row; background: white; border-radius: 10px;
              margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); overflow: hidden;
            }
            .news-content { padding: 15px; flex: 1; }
            .news-content h3 { margin: 0; font-size: 1.2rem; line-height:1.2; }
            .news-content a { color: #333; text-decoration: none; }
            .news-content a:hover { text-decoration: underline; }
            .news-date { color: #888; font-size: 0.9rem; margin: 5px 0; }
            .news-summary { font-size: 1rem; color: #555; }
            @media (max-width: 600px) { .news-card { flex-direction: column; } }
          </style>
        </head>
        <body>
        <div id="category-buttons"></div>
        <div id="news-container" class="news-section"></div>
        <script>
          const feedsByCategory = {
            "Finance News": [
                "https://www.coindesk.com/feed/",
                "https://cointelegraph.com/rss",
                "https://bitcoinmagazine.com/feed",
                "https://decrypt.co/feed",
                "https://cryptoslate.com/feed",
                "https://www.theblockcrypto.com/feed",
                "https://cryptobriefing.com/feed/",
                "https://www.newsbtc.com/feed",
                "https://news.bitcoin.com/feed",
                "https://bitcoinist.com/feed",
                "https://cryptopotato.com/feed",
                "https://cryptonews.com/feed",
                "https://www.ccn.com/feed/",
                "https://www.financemagnates.com/cryptocurrency/feed/",
                "https://coinjournal.net/feed",
                "https://www.forbes.com/crypto-blockchain/feed2/",
                "https://www.investing.com/rss/news_25.rss",
                "https://www.reuters.com/finance/rss",
                "https://www.bloomberg.com/markets/rss",
                "https://www.marketwatch.com/rss/crypto",
                "https://www.ft.com/cryptocurrency?format=rss",
                "https://cryptoslate.com/feed",
                "https://www.economist.com/finance-and-economics/rss.xml",
                "https://federalreserve.gov/feeds/rss.htm",
                "https://www.sec.gov/rss/news/press.xml",
                "https://www.nasdaq.com/feed/rssoutbound?category=crypto",
                "https://www.nasdaq.com/feed/rssoutbound?category=finance",
                "https://www.investing.com/rss/crypto-news.rss",
                "https://cryptobriefing.com/feed",
                "https://cryptoslate.com/feed",
                "https://news.bitcoin.com/feed",
                "https://cointelegraph.com/rss",
                "https://crypto.news/feed",
                "https://crypto.slashdot.org/rss",
                "https://www.cryptoglobe.com/latest/feed",
                "https://blog.chain.link/rss/",
                "https://feeds.feedburner.com/EvangelismForBitcoin",
                "https://www.crypto-news-flash.com/feed/",
                "https://www.btcfork.com/feed/",
                "https://cryptoscan.io/feed/",
                "https://www.cryptoaltex.com/feed/",
                "https://cryptopotato.com/feed",
                "https://cryptonews.com/feed",
                "https://www.bitcoininsider.org/rss.xml",
                "https://www.coinspeaker.com/feed/",
                "https://dailyhodl.com/feed/",
                "https://bitcoinschannel.com/feed/",
                "https://www.newsbtc.com/feed",
                "https://cryptobriefing.com/feed",
                "https://www.finextra.com/rss/news.aspx?cat=cryptocurrency",
                "https://www.investing.com/rss/forex-news",
                "https://forexnews.nowfinance.com/feed",
                "https://www.dailyfx.com/feeds/market-news",
                "https://www.fxstreet.com/rss/news",
                "https://www.forexfactory.com/rss.php",
                "https://www.dailyforex.com/forex-rss",
                "https://www.fxstreet.com/rss/forex-news",
                "https://www.marketwatch.com/rss/markets",
                "https://www.bloomberg.com/markets/economics.rss",
                "https://www.cnbc.com/id/100003114/device/rss/rss.html",
                "https://www.reuters.com/finance/economy/rss.xml",
                "https://www.ft.com/markets?format=rss",
                "https://www.wsj.com/xml/rss/3_7031.xml",
                "https://www.wsj.com/xml/rss/3_7031.xml",
                "https://www.kiplinger.com/rss/posts.xml",
                "https://www.morningstar.com/rss/top-stories",
                "https://www.investopedia.com/feed/",
                "https://www.marketwatch.com/rss/topstories",
                "https://www.valuewalk.com/feed/",
                "https://www.thebalance.com/rss/all.xml",
                "https://www.barrons.com/feed",
                "https://www.msn.com/en-us/money/markets/rss",
                "https://money.cnn.com/rss/newsfeeds/topstories.rss",
                "https://www.nasdaq.com/feed/rssoutbound?category=markets",
                "https://www.ft.com/?format=rss",
                "https://www.reuters.com/rssFeed/marketsNews",
                "https://www.investing.com/rss/news_301.rss",
                "https://www.business-standard.com/rss/markets-commodities.rss",
                "https://www.nasdaq.com/feed/rssoutbound?category=technology",
                "https://www.fxstreet.com/rss/news",
                "https://www.marketwatch.com/rss/economy",
                "https://www.businesstimes.com.sg/rss/feed",
                "https://www.stlouisfed.org/rss",
                "https://www.newyorkfed.org/medialibrary/media/research/current_issues",
                "https://www.bis.org/statistics/index.htm?m=6%7C33%7C633",
                "https://cointelegraph.com/rss/tag/blockchain",
                "https://www.coindesk.com/tag/bitcoin/feed/",
                "https://www.ft.com/rss/technology"

              
            ]
          };

          const categoryButtonsDiv = document.getElementById('category-buttons');
          const newsContainer = document.getElementById('news-container');

          Object.keys(feedsByCategory).forEach(category => {
            const btn = document.createElement('button');
            btn.className = 'category-btn';
            btn.innerText = category;
            btn.onclick = () => filterCategory(category);
            categoryButtonsDiv.appendChild(btn);
          });

          Object.keys(feedsByCategory).forEach(category => renderCategory(category));

          function filterCategory(category) {
            const sections = document.querySelectorAll('.news-category');
            sections.forEach(section => {
              section.style.display = (section.dataset.category === category) ? 'block' : 'none';
              if (section.style.display === 'block') section.scrollIntoView({behavior: 'smooth'});
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
                  if(data.status === "ok") {
                    const now = new Date();
                    const threeDaysAgo = new Date();
                    threeDaysAgo.setDate(now.getDate() - 2);

                    data.items.forEach(item => {
                      const pubDate = new Date(item.pubDate);
                      if(pubDate >= threeDaysAgo && pubDate <= now) {
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
                        if(imgSrc) {
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

    with tab_politics:
        html_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8"/>
          <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
          <title>Political News</title>
          <style>
            body { font-family: 'Georgia', serif; background: #f9f9f9; margin: 0; padding: 0; }
            header { background: white; padding: 20px; text-align: center; font-size: 2rem; border-bottom: 1px solid #ddd; }
            #category-buttons { display: flex; flex-wrap: wrap; justify-content: center; background: #fff; border-bottom: 1px solid #ddd; }
            .category-btn {
              margin: 10px; padding: 10px 20px; background: #eee; border: none; border-radius: 5px;
              cursor: pointer; font-size: 1rem; transition: background 0.3s;
            }
            .category-btn:hover { background: #ccc; }
            .news-section { padding: 20px; max-width: 1200px; margin: auto; }
            .category-header {
              font-size: 1.5rem; border-bottom: 2px solid #333; padding-bottom: 5px; margin-top: 40px;
            }
            .news-card {
              display: flex; flex-direction: row; background: white; border-radius: 10px;
              margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); overflow: hidden;
            }
            .news-content { padding: 15px; flex: 1; }
            .news-content h3 { margin: 0; font-size: 1.2rem; line-height:1.2; }
            .news-content a { color: #333; text-decoration: none; }
            .news-content a:hover { text-decoration: underline; }
            .news-date { color: #888; font-size: 0.9rem; margin: 5px 0; }
            .news-summary { font-size: 1rem; color: #555; }
            @media (max-width: 600px) { .news-card { flex-direction: column; } }
          </style>
        </head>
        <body>
        <div id="category-buttons"></div>
        <div id="news-container" class="news-section"></div>
        <script>
          const feedsByCategory = {
            "Politics": [

                "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
                "https://www.politico.com/rss/politics08.xml",
                "https://feeds.a.dj.com/rss/RSSPolitics.xml",
                "https://www.cnn.com/services/rss/",
                "https://www.bbc.com/news/politics/rss.xml",
                "https://www.theguardian.com/politics/rss",
                "https://www.reuters.com/rssFeed/PoliticsNews",
                "https://www.npr.org/rss/rss.php?id=1014",
                "https://www.aljazeera.com/xml/rss/all.xml",
                "https://rss.cnn.com/rss/edition_politics.rss",
                "https://www.foxnews.com/about/rss/",
                "https://www.huffpost.com/section/politics/feed",
                "https://www.usatoday.com/rss/topic/Politics/",
                "https://feeds.washingtonpost.com/rss/politics",
                "https://www.nbcnews.com/id/3032091/device/rss/rss.xml",
                "https://www.realclearpolitics.com/rss.xml",
                "https://www.axios.com/feed.xml",
                "https://www.c-span.org/rss/all/",
                "https://www.bloomberg.com/politics/rss",
                "https://www.cbsnews.com/latest/rss/politics",
                "https://www.pbs.org/newshour/politics/feed/",
                "https://www.nationalreview.com/feed/",
                "https://newrepublic.com/rss.xml",
                "https://www.thedailybeast.com/feeds/rss",
                "https://www.theatlantic.com/feed/channel/politics/",
                "https://www.foreignaffairs.com/rss",
                "https://www.economist.com/united-states/rss.xml",
                "http://www.pbs.org/wnet/rss/news/",
                "https://www.vice.com/en_us/rss/topic/politics",
                "https://www.politifact.com/rss/feed.xml",
                "https://www.thediplomat.com/feed/",
                "https://www.nationaljournal.com/feed/",
                "https://www.politico.eu/rss",
                "https://www.france24.com/en/rss",
                "https://www.dw.com/en/top-stories/s-9097",
                "https://feeds.feedburner.com/ForeignPolicy",
                "https://www.scmp.com/rss/91/feed",
                "https://www.lemonde.fr/politique/rss_full.xml",
                "https://www.spiegel.de/international/index.rss",
                "https://www.abc.net.au/news/feed/51120/rss.xml",
                "https://feeds.skynews.com/feeds/rss/politics.xml",
                "https://www.nytimes.com/section/world/feed",
                "https://www.reutersagency.com/feed/?best-topics=politics&post_type=best",
                "https://www.cnn.com/specials/politics/rss",
                "https://www.politico.com/newsletters/rss.xml",
                "https://www.latimes.com/politics/rss2.0.xml",
                "https://www.theglobeandmail.com/politics/rss/",
                "https://www.cbc.ca/cmlink/rss-politics",
                "https://www.independent.co.uk/news/politics/rss",
                "https://www.nationalpost.com/feed",
                "https://www.npr.org/sections/politics/feed",
                "https://www.usnews.com/rss/politics",
                "https://www.thenation.com/feed/",
                "https://www.newyorker.com/feed/news",
                "https://abcnews.go.com/abcnews/politicsheadlines",
                "https://www.voanews.com/rss?pid=1373",
                "https://www.washingtontimes.com/rss/headlines/politics/",
                "https://www.euronews.com/rss?level=theme&name=politics",
                "https://www.politics.co.uk/feed/",
                "https://www.thedailynews.sc/rss/politics",
                "https://www.hrw.org/rss/news.xml",
                "https://www.csmonitor.com/USA/Politics/Politics-Feed",
                "https://www.nationalreview.com/feed/",
                "https://www.thedailybeast.com/feeds/rss",
                "https://www.propublica.org/feed",
                "https://www.c-span.org/rss/series/C-SPAN13.rss",
                "https://www.nbcnews.com/politics/rss",
                "https://www.dissentmagazine.org/feed",
                "https://www.revolution-news.com/feed/",
                "https://thehill.com/rss/syndicator/19110",
                "https://fivethirtyeight.com/politics/feed",
                "https://theintercept.com/feed",
                "https://www.rollingstone.com/politics/feed/",
                "https://www.salon.com/feed/",
                "https://www.politico.com/newsletters/rss/",
                "https://www.buzzfeednews.com/feeds/politics",
                "https://www.c-span.org/rss/feed/",
                "https://www.washingtonexaminer.com/rss/topics/politics",
                "https://www.thedailybeast.com/feeds/rss",
                "https://www.realclearpolitics.com/rss_feeds/index.xml",
                "https://www.belfasttelegraph.co.uk/news/politics/rss",
                "https://www.thenewhumanitarian.org/rss.xml",
                "https://www.pressherald.com/category/politics/feed/",
                "https://www.heraldscotland.com/news/politics/feed/",
                "https://www.politifact.com/rss/feed.xml",
                "https://www.nationaljournal.com/feed/",
                "https://www.chicagotribune.com/news/politics/rss2.0.xml",
                "https://www.rollingstone.com/politics/feed/",
                "https://www.pbs.org/newshour/politics/feed/",
                "https://www.abc.net.au/news/feed/51120/rss.xml",
                "https://www.irishtimes.com/news/politics/rss",
                "https://www.politics.co.uk/feed/",
                "https://www.thecanary.co/feed/",
                "https://www.democracynow.org/feeds/podcast/rss",
                "https://www.washingtontimes.com/rss/headlines/politics/",
                "https://www.voanews.com/rss?pid=1373",
                "https://www.propublica.org/feed",
                "https://www.csmonitor.com/USA/Politics/Politics-Feed",
                "https://www.wsj.com/xml/rss/3_7031.xml"

            ]
          };

          const categoryButtonsDiv = document.getElementById('category-buttons');
          const newsContainer = document.getElementById('news-container');

          Object.keys(feedsByCategory).forEach(category => {
            const btn = document.createElement('button');
            btn.className = 'category-btn';
            btn.innerText = category;
            btn.onclick = () => filterCategory(category);
            categoryButtonsDiv.appendChild(btn);
          });

          Object.keys(feedsByCategory).forEach(category => renderCategory(category));

          function filterCategory(category) {
            const sections = document.querySelectorAll('.news-category');
            sections.forEach(section => {
              section.style.display = (section.dataset.category === category) ? 'block' : 'none';
              if (section.style.display === 'block') section.scrollIntoView({behavior: 'smooth'});
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
                  if(data.status === "ok") {
                    const now = new Date();
                    const threeDaysAgo = new Date();
                    threeDaysAgo.setDate(now.getDate() - 2);

                    data.items.forEach(item => {
                      const pubDate = new Date(item.pubDate);
                      if(pubDate >= threeDaysAgo && pubDate <= now) {
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
                        if(imgSrc) {
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

    with tab_science:
        html_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8"/>
          <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
          <title>Scientific News</title>
          <style>
            body { font-family: 'Georgia', serif; background: #f9f9f9; margin: 0; padding: 0; }
            header { background: white; padding: 20px; text-align: center; font-size: 2rem; border-bottom: 1px solid #ddd; }
            #category-buttons { display: flex; flex-wrap: wrap; justify-content: center; background: #fff; border-bottom: 1px solid #ddd; }
            .category-btn {
              margin: 10px; padding: 10px 20px; background: #eee; border: none; border-radius: 5px;
              cursor: pointer; font-size: 1rem; transition: background 0.3s;
            }
            .category-btn:hover { background: #ccc; }
            .news-section { padding: 20px; max-width: 1200px; margin: auto; }
            .category-header {
              font-size: 1.5rem; border-bottom: 2px solid #333; padding-bottom: 5px; margin-top: 40px;
            }
            .news-card {
              display: flex; flex-direction: row; background: white; border-radius: 10px;
              margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); overflow: hidden;
            }
            .news-content { padding: 15px; flex: 1; }
            .news-content h3 { margin: 0; font-size: 1.2rem; line-height:1.2; }
            .news-content a { color: #333; text-decoration: none; }
            .news-content a:hover { text-decoration: underline; }
            .news-date { color: #888; font-size: 0.9rem; margin: 5px 0; }
            .news-summary { font-size: 1rem; color: #555; }
            @media (max-width: 600px) { .news-card { flex-direction: column; } }
          </style>
        </head>
        <body>
        <div id="category-buttons"></div>
        <div id="news-container" class="news-section"></div>
        <script>
          const feedsByCategory = {
            "Science": [
            "https://www.newscientist.com/feed/home/",
            "https://rss.sciam.com/ScientificAmerican-Global",
            "https://www.sciencenews.org/feed",
            "https://scienceblogs.com/rss.xml",
            "https://medium.com/feed/starts-with-a-bang",
            "https://www.livescience.com/feeds/all",
            "https://www.sciencedaily.com/rss/all.xml",
            "https://www.scitechdaily.com/feed/",
            "https://zmescience.com/feed/",
            "https://www.nature.com/nature.rss",
            "https://academic.oup.com/rss/site_5230/595.xml",
            "https://phys.org/rss-feed/",
            "https://www.nasa.gov/rss/dyn/breaking_news.rss",
            "https://www.nsf.gov/rss/rss.xml",
            "https://www.the-scientist.com/rss",
            "https://journals.plos.org/plosone/article/feed",
            "https://feeds.feedburner.com/sciencemagazine-news",
            "https://feeds.npr.org/1007/rss.xml",
            "https://www.pnas.org/rss/current.xml",
            "https://www.frontiersin.org/rss",
            "https://www.eurekalert.org/rss.xml",
            "https://www.esa.int/rssfeed",
            "https://www.cell.com/cell/current.rss",
            "https://feeds.nature.com/nature/rss/current",
            "https://www.nature.com/subjects/biology.rss",
            "https://www.nature.com/subjects/neuroscience.rss",
            "https://www.nature.com/subjects/environmental-sciences.rss",
            "https://www.nature.com/subjects/physics.rss",
            "https://www.nature.com/subjects/medicine.rss",
            "https://www.britannica.com/rss/event",
            "https://news.nationalgeographic.com/content/news/news.rss",
            "https://www.genengnews.com/feed/",
            "https://www.nih.gov/news-events/rss.xml",
            "https://www.genome.gov/about-genomics/rss",
            "https://www.ncbi.nlm.nih.gov/research/rss/",
            "https://feeds.sciencedaily.com/sciencedaily/top_news/top_physics.xml",
            "https://feeds.sciencedaily.com/sciencedaily/top_news/top_health.xml",
            "https://feeds.sciencedaily.com/sciencedaily/top_news/top_technology.xml",
            "https://www.nasa.gov/rss/dyn/solar_system.rss",
            "https://www.nasa.gov/rss/dyn/earth.rss",
            "https://www.nasa.gov/rss/dyn/space_weather.rss",
            "https://www.researchgate.net/feed/rss/all",
            "https://www.sciencealert.com/rss-feed/all",
            "https://www.livescience.com/space/index.rss",
            "https://scitechdaily.com/feed/space/",
            "https://www.bbc.co.uk/news/science_and_environment/rss.xml",
            "https://www.abc.net.au/science/feed/51120/rss.xml",
            "https://phys.org/rss-feed/space-news/",
            "https://phys.org/rss-feed/health-news/",
            "https://phys.org/rss-feed/technology-news/",
            "https://www.techradar.com/rss/news/science",
            "https://www.wired.com/feed/category/science/latest/rss",
            "https://www.sciencenews.org/feed/science-news",
            "https://www.statnews.com/feed/",
            "https://www.theguardian.com/science/rss",
            "https://www.forbes.com/science/rss/",
            "https://feeds.feedburner.com/ScienceDaily?format=xml",
            "https://sciencenewsnet.in/feed/",
            "https://www.cnet.com/rss/science/",
            "https://www.scientificamerican.com/feed/feedrss.cfm",
            "https://www.chemistryworld.com/rss",
            "https://www.biospace.com/rss/allnews/",
            "https://www.nature.com/naturecommunications.rss",
            "https://www.scientificamerican.com/feed/science-news/",
            "https://www.nature.com/feeds/rss",
            "https://www.medicalnewstoday.com/rss",
            "https://www.sciencefriday.com/feed/podcast/",
            "https://www.nextbigfuture.com/feed",
            "https://www.nih.gov/about-nih/what-we-do/science-health-public-trust/podcast/rss.xml",
            "https://www.eurekalert.org/rss/release.xml",
            "https://feeds.feedburner.com/earthsky",
            "https://feeds.feedburner.com/philsci-archive",
            "https://feeds.feedburner.com/technologyreview/feeds/rss2",
            "https://www.nature.com/sdata.rss",
            "https://www.chemistryworld.com/rss",
            "https://www.bbc.co.uk/news/health/rss.xml",
            "https://www.esa.int/rssfeed/all",
            "https://scopeblog.stanford.edu/feed/",
            "https://www.cell.com/cell-reports/current.rss",
            "https://news.mit.edu/rss/topic/biology",
            "https://www.smithsonianmag.com/feed/science-nature/",
            "https://www.npr.org/rss/rss.php?id=1007",
            "https://www.technologyreview.com/feed/",
            "https://futurism.com/feed",
            "https://feeds.nationalgeographic.com/ng/News/Science/rss/",
            "https://journalnewsnetwork.com/feed/",
            "https://www.aaas.org/rss/news",
            "https://www.weforum.org/agenda/archive/science/rss/index.xml",
            "https://www.nature.com/nphys.rss",
            "https://www.scientificamerican.com/scicasts/feed/",
            "https://news.sciencemag.org/rss/news_current.xml",
            "https://journals.plos.org/plosbiology/feed",
            "https://news.mit.edu/rss/topic/science",
            "https://www.genengnews.com/rss/",
            "https://www.medicalnewstoday.com/rss/daily-health-news.xml",
            "https://www.researchgate.net/rss/",
            "https://www.sciencedaily.com/rss/computers.xml",
            "https://www.ncbi.nlm.nih.gov/pmc/pmc_rss.xml",
            "https://www.frontiersin.org/rss",
            "https://www.sciencedaily.com/rss/mind-matters.xml"

              
            ]
          };

          const categoryButtonsDiv = document.getElementById('category-buttons');
          const newsContainer = document.getElementById('news-container');

          Object.keys(feedsByCategory).forEach(category => {
            const btn = document.createElement('button');
            btn.className = 'category-btn';
            btn.innerText = category;
            btn.onclick = () => filterCategory(category);
            categoryButtonsDiv.appendChild(btn);
          });

          Object.keys(feedsByCategory).forEach(category => renderCategory(category));

          function filterCategory(category) {
            const sections = document.querySelectorAll('.news-category');
            sections.forEach(section => {
              section.style.display = (section.dataset.category === category) ? 'block' : 'none';
              if (section.style.display === 'block') section.scrollIntoView({behavior: 'smooth'});
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
                  if(data.status === "ok") {
                    const now = new Date();
                    const threeDaysAgo = new Date();
                    threeDaysAgo.setDate(now.getDate() - 2);

                    data.items.forEach(item => {
                      const pubDate = new Date(item.pubDate);
                      if(pubDate >= threeDaysAgo && pubDate <= now) {
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
                        if(imgSrc) {
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
    with tab_health:
        html_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8"/>
          <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
          <title>Health News</title>
          <style>
            body { font-family: 'Georgia', serif; background: #f9f9f9; margin: 0; padding: 0; }
            header { background: white; padding: 20px; text-align: center; font-size: 2rem; border-bottom: 1px solid #ddd; }
            #category-buttons { display: flex; flex-wrap: wrap; justify-content: center; background: #fff; border-bottom: 1px solid #ddd; }
            .category-btn {
              margin: 10px; padding: 10px 20px; background: #eee; border: none; border-radius: 5px;
              cursor: pointer; font-size: 1rem; transition: background 0.3s;
            }
            .category-btn:hover { background: #ccc; }
            .news-section { padding: 20px; max-width: 1200px; margin: auto; }
            .category-header {
              font-size: 1.5rem; border-bottom: 2px solid #333; padding-bottom: 5px; margin-top: 40px;
            }
            .news-card {
              display: flex; flex-direction: row; background: white; border-radius: 10px;
              margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); overflow: hidden;
            }
            .news-content { padding: 15px; flex: 1; }
            .news-content h3 { margin: 0; font-size: 1.2rem; line-height:1.2; }
            .news-content a { color: #333; text-decoration: none; }
            .news-content a:hover { text-decoration: underline; }
            .news-date { color: #888; font-size: 0.9rem; margin: 5px 0; }
            .news-summary { font-size: 1rem; color: #555; }
            @media (max-width: 600px) { .news-card { flex-direction: column; } }
          </style>
        </head>
        <body>
        <div id="category-buttons"></div>
        <div id="news-container" class="news-section"></div>
        <script>
          const feedsByCategory = {
            "Health": [
            

            "https://www.medicalnewstoday.com/rss",
            "https://www.sciencedaily.com/rss/health.xml",
            "https://www.nih.gov/rss.xml",
            "https://kffhealthnews.org/feed",
            "https://www.fiercehealthcare.com/fiercehealthcarecom/rss-feeds",
            "https://www.healthline.com/rss",
            "https://www.who.int/feeds/entity/mediacentre/news/en/rss.xml",
            "https://www.webmd.com/rss/rss.aspx?type=health",
            "https://www.cdc.gov/rss/rss.xml",
            "https://www.health.com/feed",
            "https://www.mayoclinic.org/rss-feed/rss",
            "https://www.npr.org/rss/rss.php?id=1128",
            "https://www.statnews.com/feed/",
            "https://www.nih.gov/news-events/rss.xml",
            "https://www.nytimes.com/section/health/feed.xml",
            "https://www.usatoday.com/rss/topic/Health",
            "https://feeds.a.dj.com/rss/RSSHealth.xml",
            "https://www.theguardian.com/society/health/rss",
            "https://www.scientificamerican.com/feed/feedrss.cfm?category=health",
            "https://www.health.gov/rss.xml",
            "https://rss.medicalnewstoday.com/health-news.xml",
            "https://www.nhs.uk/rss",
            "https://www.topmastersinhealthcare.com/feed/",
            "https://www.thehealthcareblog.com/feed",
            "https://healthitanalytics.com/rss.xml",
            "https://www.nejm.org/rss",
            "https://www.ama-assn.org/rss/site_1/featured.rss",
            "https://www.psychologytoday.com/us/rss",
            "https://www.bmj.com/rss/current.xml",
            "https://feeds.feedburner.com/Euronews-Health",
            "https://www.ahrq.gov/rss.xml",
            "https://www.healthaffairs.org/do/10.1377/hblog/rss.xml",
            "https://health.usnews.com/rss/themes/health-wellness",
            "https://meduza.io/rss/feature/health",
            "https://www.medpagetoday.com/rss",
            "https://jamanetwork.com/rss/site_3181/4636.xml",
            "https://www.nih.gov/news-events/news-releases/rss-feed",
            "https://www.washingtonpost.com/health/rss",
            "https://www.reuters.com/rssFeed/healthNews",
            "https://www.aafp.org/rss.xml",
            "https://blogs.cdc.gov/publichealthmatters/feed",
            "https://feeds.feedburner.com/HarvardHealth",
            "https://onlinelibrary.wiley.com/feed/rss/10970258",
            "https://alkamelsystems.com/feed.xml",
            "https://www.medscape.com/viewarticle/rss",
            "https://www.eurekalert.org/rss.xml",
            "https://www.globalhealthnow.org/rss",
            "https://www.medicalnewstoday.com/rss/diseases-and-conditions.xml",
            "https://www.mobilehealthnews.com/rss",
            "https://www.hhs.gov/about/news/rss/index.xml",
            "https://www.healthcareitnews.com/rss.xml",
            "https://www.medicaleconomics.com/rss.xml",
            "https://www.cancer.gov/rss.xml",
            "https://www.cdc.gov/features/fair-information/rss.rss",
            "https://www.who.int/feed/entity/mediacentre/news/en/rss.xml",
            "https://www.patient.info/rss.xml",
            "https://www.health.harvard.edu/blog/feed",
            "https://www.health.org.uk/blog/rss.xml",
            "https://www.kff.org/feed/",
            "https://www.ncbi.nlm.nih.gov/research/rss/",
            "https://www.physiciansweekly.com/feed/",
            "https://feeds.feedburner.com/healthnewsfrom-nida",
            "https://www.womenshealth.gov/rss.xml",
            "https://scienceblog.com/feed",
            "https://www.publichealthlawcenter.org/rss-feeds",
            "https://www.cdc.gov/nchs/dataaccess/restricteddata.htm",
            "https://www.mja.com.au/rss.xml",
            "https://www.acc.org/rss.xml",
            "https://www.nejm.org/rss",
            "https://www.ama-assn.org/rss/site_1/featured.rss",
            "https://www.cdc.gov/media/rss/pressfeeds.xml",
            "https://www.who.int/rss-feeds/news-english.xml",
            "https://www.gov.uk/government/rss",
            "https://www.livescience.com/health/feed",
            "https://www.cdc.gov/healthyschools/bam/documents/accelerate-bam-fs-rss-feed.xml",
            "https://www.healthline.com/rss/all-health-topics",
            "https://www.statnews.com/feed/",
            "https://www.medicalnewstoday.com/rss/daily-health-news.xml",
            "https://www.medicalxpress.com/rss-feed/",
            "https://www.cdc.gov/diabetes/rss/rss-press.xml",
            "https://www.healthypeople.gov/2020/topics-objectives/topic/health-communication-and-health-information-technology",
            "https://www.niams.nih.gov/rss",
            "https://www.aidsmap.com/rss.xml",
            "https://www.yalemedicine.org/rss",
            "https://www.hopkinsmedicine.org/rss/index.xml",
            "https://www.randomustmeso.com/rss-feed.xml",
            "https://www.who.int/rss-feeds/news-english.xml",
            "https://feeds.feedburner.com/eurekalert/TopHealthNews",
            "https://www.psychologytoday.com/us/rss",
            "https://health.economictimes.indiatimes.com/rss",
            "https://www.fastcompany.com/section/health/rss",
            "https://rss.medicalxpress.com/rss/health.xml",
            "https://www.nih.gov/health-information/news-events/news-releases/rss-feed",
            "https://www.healthinformaticsforum.com/feed/"

              
            ]
          };

          const categoryButtonsDiv = document.getElementById('category-buttons');
          const newsContainer = document.getElementById('news-container');

          Object.keys(feedsByCategory).forEach(category => {
            const btn = document.createElement('button');
            btn.className = 'category-btn';
            btn.innerText = category;
            btn.onclick = () => filterCategory(category);
            categoryButtonsDiv.appendChild(btn);
          });

          Object.keys(feedsByCategory).forEach(category => renderCategory(category));

          function filterCategory(category) {
            const sections = document.querySelectorAll('.news-category');
            sections.forEach(section => {
              section.style.display = (section.dataset.category === category) ? 'block' : 'none';
              if (section.style.display === 'block') section.scrollIntoView({behavior: 'smooth'});
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
                  if(data.status === "ok") {
                    const now = new Date();
                    const threeDaysAgo = new Date();
                    threeDaysAgo.setDate(now.getDate() - 2);

                    data.items.forEach(item => {
                      const pubDate = new Date(item.pubDate);
                      if(pubDate >= threeDaysAgo && pubDate <= now) {
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
                        if(imgSrc) {
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
    with tab_sports:

        st.set_page_config(page_title="Game on ", layout="wide")

        st.markdown("""
            <style>
            body, .css-18e3th9 {
                font-family: Georgia, Georgia;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("Game on")

        # Sports blogs dictionary with 15 URLs per sport (example URLs, verify or replace with updated links)

        sports_blogs = {
            "Soccer": [
                {"title": "FotMob", "url": "https://www.fotmob.com/"},
                {"title": "Football365", "url": "https://www.football365.com/"},
                {"title": "Transfermarkt", "url": "https://www.transfermarkt.com/"},

                {"title": "Bleacher Report Soccer", "url": "https://bleacherreport.com/world-soccer"},
                {"title": "MLS Soccer", "url": "https://www.mlssoccer.com/"},
                {"title": "SoccerNews", "url": "https://www.soccernews.com/"},


            ],

            "Cricket": [
                {"title": "The Cricket Monthly", "url": "https://www.thecricketmonthly.com/"},
                {"title": "ICC Cricket", "url": "https://www.icc-cricket.com/"},
                {"title": "Cricket Country", "url": "https://www.cricketcountry.com/"},
                {"title": "NDTV Sports Cricket", "url": "https://sports.ndtv.com/cricket"},
                {"title": "FOX Cricket", "url": "https://www.foxsports.com.au/cricket"},

            ],

            "Basketball": [

                {"title": "Basketball Insiders", "url": "https://www.basketballinsiders.com/"},
                {"title": "Bleacher Report NBA", "url": "https://bleacherreport.com/nba"},
                {"title": "Sports Illustrated NBA", "url": "https://www.si.com/nba"},
                {"title": "RealGM", "url": "https://basketball.realgm.com/"},
                {"title": "Basketball Reference", "url": "https://www.basketball-reference.com/"},
               
                {"title": "The Athletic NBA", "url": "https://theathletic.com/nba/"},
            ],

            "Hockey": [
                {"title": "NHL.com", "url": "https://www.nhl.com/news"},
                {"title": "The Hockey News", "url": "https://thehockeynews.com/"},
                {"title": "SB Nation NHL", "url": "https://www.sbnation.com/nhl"},
                {"title": "ESPN NHL", "url": "https://www.espn.com/nhl/"},
                {"title": "TSN Hockey", "url": "https://www.tsn.ca/nhl"},
                {"title": "Hockey Reference", "url": "https://www.hockey-reference.com/"},
                {"title": "CBS Sports NHL", "url": "https://www.cbssports.com/nhl/"},
                {"title": "Sportsnet NHL", "url": "https://www.sportsnet.ca/nhl/"},
                {"title": "Yahoo Sports NHL", "url": "https://sports.yahoo.com/nhl/"},
                {"title": "TheScore NHL", "url": "https://www.thescore.com/nhl"},
                {"title": "Hockey Wilderness", "url": "https://hockeywilderness.com/"},
                {"title": "Boston Hockey Now", "url": "https://www.bostonhockeynow.com/"},
                {"title": "The Hockey Writers", "url": "https://thehockeywriters.com/"},
                {"title": "The Ice Garden", "url": "https://theicegarden.com/"},
                {"title": "Rink Royalty", "url": "https://rinkroyalty.com/"},
            ],

            "Tennis": [

                {"title": "Tennis.com", "url": "https://www.tennis.com/"},
                {"title": "Tennis Now", "url": "https://www.tennisnow.com/"},
                {"title": "Tennis Magazine", "url": "https://www.tennis.com/magazine/"},
                {"title": "FlashScore Tennis", "url": "https://www.flashscore.com/tennis/"},
                {"title": "Tennis365", "url": "https://www.tennis365.com/"},
                {"title": "Tennis World", "url": "https://www.tennisworldusa.org/"},
                {"title": "Inside Tennis", "url": "https://www.insidetennis.com/"},

            ],

            "Volleyball": [

                {"title": "Volleyball World", "url": "https://en.volleyballworld.com/"},
                {"title": "Volleywood", "url": "https://volleywood.net/"},
                {"title": "USA Volleyball", "url": "https://usavolleyball.org/"},
                {"title": "Volleyball USA", "url": "https://www.volleyusa.com/"},
                {"title": "VolleyCountry", "url": "https://volleycountry.com/"},


            ],



            "Baseball": [

                {"title": "Baseball-Reference", "url": "https://www.baseball-reference.com/"},
                {"title": "MLB Trade Rumors", "url": "https://www.mlbtraderumors.com/"},

                {"title": "Baseball Savant", "url": "https://baseballsavant.mlb.com/"},
                {"title": "The Athletic MLB", "url": "https://theathletic.com/mlb/"},

                {"title": "RotoWire Baseball", "url": "https://www.rotowire.com/baseball/"},
            ],

            "Rugby": [
                {"title": "Planetrugby", "url": "https://www.planetrugby.com/"},
                {"title": "Rugby World", "url": "https://www.rugbyworld.com/"},
                {"title": "The42", "url": "https://www.the42.ie/rugby/"},
                {"title": "ItsRugby", "url": "https://www.itsrugby.co.uk/"},
                {"title": "Fiji Rugby", "url": "https://www.fijirugby.com/"},

            ],

            "Golf": [
                {"title": "PGA Tour", "url": "https://www.pgatour.com/"},
                {"title": "Golf Channel", "url": "https://www.golfchannel.com/"},
                {"title": "Golf Channel News", "url": "https://www.golfchannel.com/news"},
                {"title": "Golf Australia", "url": "https://www.golf.org.au/"},

            ],

            "MMA": [

                {"title": "Sherdog", "url": "https://www.sherdog.com/"},
                {"title": "MMA News", "url": "https://www.mmanews.com/"},
                {"title": "LowKick MMA", "url": "https://www.lowkickmma.com/"},
                {"title": "Fightful", "url": "https://www.fightful.com/"},
                {"title": "MMA Oddsbreaker", "url": "https://mmaoddsbreaker.com/"},
                {"title": "MiddleEasy", "url": "https://middleeasy.com/"},

            ],

            "Formula 1": [

                {"title": "PlanetF1", "url": "https://www.planetf1.com/"},
                {"title": "Autosport F1", "url": "https://www.autosport.com/f1/"},
                {"title": "Motorsport.com F1", "url": "https://www.motorsport.com/f1/"},
                {"title": "The Race", "url": "https://the-race.com/"},
                {"title": "GP Blog", "url": "https://www.gpblog.com/en"},
                {"title": "Motorsport Stats", "url": "https://www.motorsportstats.com/series/formula-1"},
                {"title": "F1 Fans Forum", "url": "https://www.f1fansite.com/forums/"},
                
            ],
        }
        tab_labels = list(sports_blogs.keys())
        tabs = st.tabs(tab_labels)

        @st.cache_data(show_spinner=False)
        def get_url_from_title(blogs_list, title):
            for blog in blogs_list:
                if blog["title"] == title:
                    return blog["url"]
            return None

        for tab, sport in zip(tabs, tab_labels):
            with tab:
                st.subheader(f"{sport} ")
                blogs = sports_blogs[sport]
                blog_titles = [blog["title"] for blog in blogs]

                state_key = f"selected_blog_{sport}"
                if state_key not in st.session_state:
                    st.session_state[state_key] = blog_titles[0]

                selected_blog = st.segmented_control(
                    "Select to explore",
                    blog_titles,
                    key=state_key,
                )

                selected_url = get_url_from_title(blogs, selected_blog)
                if selected_url:
                    iframe_html = f"""
                    <div style="position: relative; width: 100%; height: 2000px;">
                        <iframe src="{selected_url}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border:none;" allowfullscreen></iframe>
                    </div>
                    """
                    components.html(iframe_html, height=2000)
                else:
                    st.warning("Selected blog URL could not be found.")


    with tab_editorial:
        html_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8"/>
          <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
          <title>Editorial Select</title>
          <style>
            body { font-family: 'Georgia', serif; background: #f9f9f9; margin: 0; padding: 0; }
            header { background: white; padding: 20px; text-align: center; font-size: 2rem; border-bottom: 1px solid #ddd; }
            #category-buttons { display: flex; flex-wrap: wrap; justify-content: center; background: #fff; border-bottom: 1px solid #ddd; }
            .category-btn {
              margin: 10px; padding: 10px 20px; background: #eee; border: none; border-radius: 5px;
              cursor: pointer; font-size: 1rem; transition: background 0.3s;
            }
            .category-btn:hover { background: #ccc; }
            .news-section { padding: 20px; max-width: 1200px; margin: auto; }
            .category-header {
              font-size: 1.5rem; border-bottom: 2px solid #333; padding-bottom: 5px; margin-top: 40px;
            }
            .news-card {
              display: flex; flex-direction: row; background: white; border-radius: 10px;
              margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); overflow: hidden;
            }
            .news-content { padding: 15px; flex: 1; }
            .news-content h3 { margin: 0; font-size: 1.2rem; line-height:1.2; }
            .news-content a { color: #333; text-decoration: none; }
            .news-content a:hover { text-decoration: underline; }
            .news-date { color: #888; font-size: 0.9rem; margin: 5px 0; }
            .news-summary { font-size: 1rem; color: #555; }
            @media (max-width: 600px) { .news-card { flex-direction: column; } }
          </style>
        </head>
        <body>
        <div id="category-buttons"></div>
        <div id="news-container" class="news-section"></div>
        <script>
          const feedsByCategory = {
            "Editorial News": [

            "https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/opinion/rss.xml",
            "https://www.theguardian.com/us/commentisfree/rss",
            "https://www.washingtonpost.com/opinions/rss.xml",
            "https://www.latimes.com/opinion/rss2.0.xml",
            "https://www.huffpost.com/section/opinion/feed",
            "https://timesofindia.indiatimes.com/rss.cms",
            "https://indianexpress.com/section/opinion/feed/",
            "https://www.firstpost.com/opinion/feed",
            "https://www.thehindubusinessline.com/opinion/?service=rss",
            "https://www.telegraphindia.com/rss/opinion.xml",
            "https://www.deccanherald.com/opinion/feed",
            "https://www.dailyo.in/rss/all.xml",
            "https://www.bbc.com/news/opinion/rss.xml",
            "https://www.aljazeera.com/xml/rss/opinion.xml",
            "https://www.economist.com/united-states/rss.xml",
            "https://www.project-syndicate.org/rss/analysis",
            "https://www.reuters.com/rssFeed/editorialNews",
            "https://www.forbes.com/opinion/feed/",
            "https://www.npr.org/rss/rss.php?id=1019",
            "https://www.cbc.ca/cmlink/rss-opinion",
            "https://www.etstreams.com/opinion/rss.xml",
            "https://www.livemint.com/rss/opinion",
            "https://www.business-standard.com/rss/opinion-10313.rss",
            "https://www.scmp.com/rss/263/feed",
            "https://www.jpost.com/Rss/RssFeed?feedName=opinion",
            "https://www.nationalreview.com/feed/",
            "https://www.bloombergquint.com/author/rss/journalists",
            "https://www.buzzfeednews.com/rss",
            "https://www.thenation.com/feed/",
            "https://newrepublic.com/rss.xml",
            "https://thehill.com/rss/syndicator/19110",
            "https://www.salon.com/feed/",
            "https://www.democracynow.org/feeds/rss",
            "https://www.fpif.org/feed/",
            "https://www.truthdig.com/feed/",
            "https://www.counterpunch.org/feed/",
            "https://www.truthout.org/feed/",
            "https://www.insidesources.com/rss/",
            "https://www.propublica.org/feed",
            "https://www.dissentmagazine.org/feed",
            "https://www.commonwealmagazine.org/feed",
            "https://www.thedailybeast.com/feeds/rss/opinion",
            "https://www.nationaljournal.com/feed/",
            "https://www.realclearpolitics.com/rss_feeds/index.xml",
            "https://www.newyorker.com/feed/news",
            "https://www.vox.com/rss/index.xml",
            "https://www.euronews.com/rss?level=theme&name=opinion",
            "https://www.hrw.org/rss/news.xml",
            "https://www.c-span.org/rss/series/C-SPAN13.rss",
            "https://www.washingtontimes.com/rss/headlines/opinion/",
            "https://www.opendemocracy.net/en/feed/",
            "https://www.spectator.co.uk/rss",
            "https://www.americanthinker.com/rss.xml",
            "https://www.commentarymagazine.com/feed/",
            "https://www.weeklystandard.com/rss/arts.xml",
            "https://www.newstatesman.com/politics/rss.xml",
            "https://www.christianitytoday.com/rss/opinion.xml",
            "https://www.insidehighered.com/rss/feed",
            "https://www.insideelections.com/feed",
            "https://www.bipartisanalliance.com/feed",
            "https://www.overthinkgroup.com/rss.xml",
            "https://www.economist.com/rss",
            "https://www.pewresearch.org/feed/",
            "https://www.cato.org/rss.xml",
            "https://www.fpri.org/rss",
            "https://www.heritage.org/feed/rss",
            "https://www.rand.org/news/rss",
            "https://foreignpolicy.com/feed/",
            "https://www.foreignaffairs.com/rss",
            "https://www.cfr.org/rss",
            "https://blogs.lse.ac.uk/feed/",
            "https://www.globalpolicyjournal.com/rss.xml",
            "https://www.project-syndicate.org/rss/opinion",
            "https://www.juancole.com/feed",
            "https://www.oxfordmartin.ox.ac.uk/feed/",
            "https://www.lowyinstitute.org/rss",
            "https://www.usip.org/rss",
            "https://www.americanprogress.org/feed/",
            "https://www.washingtonmonthly.com/rss/all.php"

            ]
          };

          const categoryButtonsDiv = document.getElementById('category-buttons');
          const newsContainer = document.getElementById('news-container');

          Object.keys(feedsByCategory).forEach(category => {
            const btn = document.createElement('button');
            btn.className = 'category-btn';
            btn.innerText = category;
            btn.onclick = () => filterCategory(category);
            categoryButtonsDiv.appendChild(btn);
          });

          Object.keys(feedsByCategory).forEach(category => renderCategory(category));

          function filterCategory(category) {
            const sections = document.querySelectorAll('.news-category');
            sections.forEach(section => {
              section.style.display = (section.dataset.category === category) ? 'block' : 'none';
              if (section.style.display === 'block') section.scrollIntoView({behavior: 'smooth'});
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
                  if(data.status === "ok") {
                    const now = new Date();
                    const threeDaysAgo = new Date();
                    threeDaysAgo.setDate(now.getDate() - 2);

                    data.items.forEach(item => {
                      const pubDate = new Date(item.pubDate);
                      if(pubDate >= threeDaysAgo && pubDate <= now) {
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
                        if(imgSrc) {
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
    with tab_trending:
        html_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8"/>
          <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
          <title>Trending News</title>
          <style>
            body { font-family: 'Georgia', serif; background: #f9f9f9; margin: 0; padding: 0; }
            header { background: white; padding: 20px; text-align: center; font-size: 2rem; border-bottom: 1px solid #ddd; }
            #category-buttons { display: flex; flex-wrap: wrap; justify-content: center; background: #fff; border-bottom: 1px solid #ddd; }
            .category-btn {
              margin: 10px; padding: 10px 20px; background: #eee; border: none; border-radius: 5px;
              cursor: pointer; font-size: 1rem; transition: background 0.3s;
            }
            .category-btn:hover { background: #ccc; }
            .news-section { padding: 20px; max-width: 1200px; margin: auto; }
            .category-header {
              font-size: 1.5rem; border-bottom: 2px solid #333; padding-bottom: 5px; margin-top: 40px;
            }
            .news-card {
              display: flex; flex-direction: row; background: white; border-radius: 10px;
              margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); overflow: hidden;
            }
            .news-content { padding: 15px; flex: 1; }
            .news-content h3 { margin: 0; font-size: 1.2rem; line-height:1.2; }
            .news-content a { color: #333; text-decoration: none; }
            .news-content a:hover { text-decoration: underline; }
            .news-date { color: #888; font-size: 0.9rem; margin: 5px 0; }
            .news-summary { font-size: 1rem; color: #555; }
            @media (max-width: 600px) { .news-card { flex-direction: column; } }
          </style>
        </head>
        <body>
        <div id="category-buttons"></div>
        <div id="news-container" class="news-section"></div>
        <script>
          const feedsByCategory = {
            "Trending": [

            "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
            "https://www.cnn.com/services/rss/",
            "https://feeds.bbci.co.uk/news/rss.xml",
            "https://feeds.reuters.com/reuters/topNews",
            "https://www.aljazeera.com/xml/rss/all.xml",
            "https://rss.cnn.com/rss/cnn_topstories.rss",
            "https://www.npr.org/rss/rss.php?id=1001",
            "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
            "https://www.theguardian.com/world/rss",
            "https://feeds.foxnews.com/foxnews/latest",
            "https://timesofindia.indiatimes.com/rss.cms",
            "https://www.hindustantimes.com/rss/topnews/rssfeed.xml",
            "https://indianexpress.com/section/india/feed/",
            "https://www.washingtonpost.com/rss/world",
            "https://www.wsj.com/xml/rss/3_7085.xml",
            "https://www.usatoday.com/rss/news",
            "https://www.buzzfeed.com/world.xml",
            "https://feeds.feedburner.com/TechCrunch/",
            "https://www.engadget.com/rss.xml",
            "https://www.techradar.com/rss",
            "https://www.mashable.com/feed/",
            "https://feeds.feedburner.com/Gizmodo/full",
            "https://www.cnet.com/rss/news/",
            "https://www.reddit.com/r/news/.rss",
            "https://news.ycombinator.com/rss",
            "https://www.nbcnews.com/id/3032091/device/rss/rss.xml",
            "https://www.axios.com/feed.xml",
            "https://www.npr.org/rss/rss.php?id=1019",
            "https://feeds.skynews.com/feeds/rss/home.xml",
            "https://www.nationalgeographic.com/content/nationalgeographic/en_us/news.rss",
            "https://feeds.abcnews.com/abcnews/topstories",
            "https://globalnews.ca/feed/",
            "https://www.euronews.com/rss",
            "https://www.cbc.ca/cmlink/rss-topstories",
            "https://www.voanews.com/rss",
            "https://www.nbcnews.com/news/rss",
            "https://www.kpbs.org/news/rss",
            "https://www.vox.com/rss/index.xml",
            "https://www.politico.com/rss",
            "https://www.nbcnews.com/id/3032091/device/rss/rss.xml",
            "https://news.google.com/news/rss",
            "https://www.techspot.com/rss/",
            "https://feeds.feedburner.com/ScienceNewsHeadlines",
            "https://feeds.feedburner.com/HealthNewsHeadlines",
            "https://feeds.feedburner.com/EntertainmentNewsHeadlines",
            "https://rss.nytimes.com/services/xml/rss/nyt/FrontPage.xml",
            "https://www.independent.co.uk/news/rss",
            "https://www.latimes.com/nation/rss2.0.xml",
            "https://www.wsj.com/xml/rss/3_7011.xml",
            "https://www.cbsnews.com/latest/rss/national",
            "https://feeds.feedburner.com/TheAtlantic",
            "https://feeds.feedburner.com/foreignpolicy/HPJQ",
            "https://www.sciencedaily.com/rss/top_news/top_technology.xml",
            "https://www.sciencedaily.com/rss/top_news/top_health.xml",
            "https://www.sciencedaily.com/rss/top_news/top_science.xml",
            "https://feeds.feedburner.com/TechCrunch/startups",
            "https://feeds.feedburner.com/Engadget",
            "https://feeds.feedburner.com/TheNextWeb",
            "https://feeds.feedburner.com/CultOfMac",
            "https://feeds.feedburner.com/LifeHacker",
            "https://www.pcgamer.com/rss",
            "https://www.gamespot.com/feeds/mashup/",
            "https://feeds.gawker.com/gizmodo/full",
            "https://www.polygon.com/rss/index.xml",
            "https://uproxx.com/feed",
            "https://www.sfgate.com/rss/feed/News-504.php",
            "https://www.sfchronicle.com/rss/feed/All-News-102.php",
            "https://www.npr.org/rss/rss.php?id=1008",
            "https://www.npr.org/rss/rss.php?id=1005",
            "https://www.npr.org/rss/rss.php?id=1007",
            "https://www.npr.org/rss/rss.php?id=1013"

            ]
          };

          const categoryButtonsDiv = document.getElementById('category-buttons');
          const newsContainer = document.getElementById('news-container');

          Object.keys(feedsByCategory).forEach(category => {
            const btn = document.createElement('button');
            btn.className = 'category-btn';
            btn.innerText = category;
            btn.onclick = () => filterCategory(category);
            categoryButtonsDiv.appendChild(btn);
          });

          Object.keys(feedsByCategory).forEach(category => renderCategory(category));

          function filterCategory(category) {
            const sections = document.querySelectorAll('.news-category');
            sections.forEach(section => {
              section.style.display = (section.dataset.category === category) ? 'block' : 'none';
              if (section.style.display === 'block') section.scrollIntoView({behavior: 'smooth'});
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
                  if(data.status === "ok") {
                    const now = new Date();
                    const threeDaysAgo = new Date();
                    threeDaysAgo.setDate(now.getDate() - 2);

                    data.items.forEach(item => {
                      const pubDate = new Date(item.pubDate);
                      if(pubDate >= threeDaysAgo && pubDate <= now) {
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
                        if(imgSrc) {
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

    with tab_pods:


        st.set_page_config(page_title="Podcast Browser", layout="wide")

        st.markdown("""
            <style>
            body, .css-18e3th9 {
                font-family: Georgia, Georgia;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("Podcast")


        podcasts = [
            {"title": "NPR News Now", "url": "https://www.npr.org/sections/news/"},
            {"title": "Radiolab", "url": "https://www.wnycstudios.org/podcasts/radiolab"},
            {"title": "Stuff You Should Know", "url": "https://www.iheart.com/podcast/105-stuff-you-should-know-26940277/"},
            {"title": "All-In with Chamath, Jason, Sacks & Friedberg", "url": "https://allin.com/episodes"},
            {"title": "TED Talks Daily", "url": "https://www.ted.com/podcasts/ted-talks-daily"},
            {"title": "Planet Money", "url": "https://www.npr.org/sections/money/"},
            {"title": "Armchair Expert with Dax Shepard", "url": "https://armchairexpertpod.com/"},
            {"title": "Wait Wait... Don't Tell Me!", "url": "https://www.npr.org/programs/wait-wait-dont-tell-me/"},
            {"title": "The Moth", "url": "https://themoth.org/podcast"},
            {"title": "Lore", "url": "https://www.lorepodcast.com/"},
            {"title": "Pod Save America", "url": "https://crooked.com/podcast-series/pod-save-america/"},
            {"title": "Song Exploder", "url": "https://songexploder.net/"},
            {"title": "99% Invisible", "url": "https://99percentinvisible.org/"},
            {"title": "The Happiness Lab", "url": "https://www.happinesslab.fm/"},
            {"title": "No Such Thing As A Fish", "url": "https://www.nosuchthingasafish.com/"},
            {"title": "Revisionist History", "url": "https://revisionisthistory.com/"},
            {"title": "The Tony Robbins Podcast", "url": "https://www.tonyrobbins.com/podcast/"},
            {"title": "Philosophize This!", "url": "https://www.philosophizethis.org/"},
            {"title": "Code Switch", "url": "https://www.npr.org/sections/codeswitch/"},
            {"title": "On Being with Krista Tippett", "url": "https://onbeing.org/series/podcast/"},
            {"title": "Science Friday", "url": "https://www.sciencefriday.com/"},
            {"title": "The Adventure Zone", "url": "https://www.maximumfun.org/shows/adventure-zone"},
            {"title": "Judge John Hodgman", "url": "https://maximumfun.org/shows/judge-john-hodgman/"},
            {"title": "The Magnus Archives", "url": "https://rustyquill.com/show/the-magnus-archives/"},
        ]
        tab_titles = [pod["title"] for pod in podcasts]

        if "selected_podcast" not in st.session_state:
            st.session_state.selected_podcast = tab_titles[0]

        selected_tab = st.segmented_control("Select a podcast", tab_titles, key="selected_podcast")

        @st.cache_data(show_spinner=False)
        def get_url_from_title(title):
            for pod in podcasts:
                if pod["title"] == title:
                    return pod["url"]
            return None

        selected_url = get_url_from_title(selected_tab)

        if selected_url:
            iframe_html = f"""
            <div style="position: relative; width: 100%; height: 2000px;">
                <iframe src="{selected_url}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border:none;" allowfullscreen></iframe>
            </div>
            """
            components.html(iframe_html, height =2000)
        else:
            st.warning("Selected podcast URL could not be found.")


    with tab_commnews:

        html_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>    
        <!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text"></span></a></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-tickers.js" async>
          {
          "symbols": [
            {
              "description": "Gold",
              "proName": "TVC:GOLD"
            },
            {
              "description": "Silver",
              "proName": "TVC:SILVER"
            },
            {
              "description": "Oil",
              "proName": "TVC:USOIL"
            },
            {
              "description": "Brent",
              "proName": "TVC:UKOIL"
            },
            {
              "description": "Natural gas",
              "proName": "CAPITALCOM:NATURALGAS"
            },
            {
              "description": "Copper",
              "proName": "CAPITALCOM:COPPER"
            },
            {
              "description": "Platinum",
              "proName": "TVC:PLATINUM"
            },
            {
              "description": "Palladium",
              "proName": "TVC:PALLADIUM"
            },
            {
              "description": "Corn",
              "proName": "CAPITALCOM:CORN"
            },
            {
              "description": "Wheat",
              "proName": "CAPITALCOM:WHEAT"
            },
            {
              "description": "Soybean",
              "proName": "CAPITALCOM:SOYBEAN"
            },
            {
              "description": "Coffee",
              "proName": "SPARKS:COFFEE"
            },
            {
              "description": "Cocoa",
              "proName": "NYMEX:CJ1!"
            },
            {
              "description": "Cotton",
              "proName": "NYMEX:TT1!"
            },
            {
              "description": "Sugar",
              "proName": "NYMEX:YO1!"
            },
            {
              "description": "Lean hogs",
              "proName": "CME:HE1!"
            },
            {
              "description": "Live cattle",
              "proName": "CME:LE1!"
            },
            {
              "description": "Feeder cattle",
              "proName": "CME:GF1!"
            },
            {
              "description": "Orange juice",
              "proName": "CMCMARKETS:ORANGEJUICEN2025"
            },
            {
              "description": "Rough rice",
              "proName": "CBOT:ZR1!"
            },
            {
              "description": "Milk",
              "proName": "CME:GDK1!"
            },
            {
              "description": "Heating oil",
              "proName": "ICEEUR:UHO1!"
            },
            {
              "description": "Gasoline",
              "proName": "NYMEX:RB1!"
            },
            {
              "description": "Aluminium",
              "proName": "COMEX:ALI1!"
            },
            {
              "description": "Soybean",
              "proName": "CBOT:ZM1!"
            }
          ],
          "isTransparent": false,
          "showSymbolLogo": true,
          "colorTheme": "light",
          "locale": "en"
        }
          </script>
        </div>
        <!-- TradingView Widget END -->
          <meta charset="UTF-8"/>
          <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
          <title>Commodities News</title>
          <style>
            body { font-family: 'Georgia', serif; background: #f9f9f9; margin: 0; padding: 0; }
            header { background: white; padding: 20px; text-align: center; font-size: 2rem; border-bottom: 1px solid #ddd; }
            #category-buttons { display: flex; flex-wrap: wrap; justify-content: center; background: #fff; border-bottom: 1px solid #ddd; }
            .category-btn {
              margin: 10px; padding: 10px 20px; background: #eee; border: none; border-radius: 5px;
              cursor: pointer; font-size: 1rem; transition: background 0.3s;
            }
            .category-btn:hover { background: #ccc; }
            .news-section { padding: 20px; max-width: 1200px; margin: auto; }
            .category-header {
              font-size: 1.5rem; border-bottom: 2px solid #333; padding-bottom: 5px; margin-top: 40px;
            }
            .news-card {
              display: flex; flex-direction: row; background: white; border-radius: 10px;
              margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); overflow: hidden;
            }
            .news-content { padding: 15px; flex: 1; }
            .news-content h3 { margin: 0; font-size: 1.2rem; line-height:1.2; }
            .news-content a { color: #333; text-decoration: none; }
            .news-content a:hover { text-decoration: underline; }
            .news-date { color: #888; font-size: 0.9rem; margin: 5px 0; }
            .news-summary { font-size: 1rem; color: #555; }
            @media (max-width: 600px) { .news-card { flex-direction: column; } }
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

          Object.keys(feedsByCategory).forEach(category => {
            const btn = document.createElement('button');
            btn.className = 'category-btn';
            btn.innerText = category;
            btn.onclick = () => filterCategory(category);
            categoryButtonsDiv.appendChild(btn);
          });

          Object.keys(feedsByCategory).forEach(category => renderCategory(category));

          function filterCategory(category) {
            const sections = document.querySelectorAll('.news-category');
            sections.forEach(section => {
              section.style.display = (section.dataset.category === category) ? 'block' : 'none';
              if (section.style.display === 'block') section.scrollIntoView({behavior: 'smooth'});
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
                  if(data.status === "ok") {
                    const now = new Date();
                    const threeDaysAgo = new Date();
                    threeDaysAgo.setDate(now.getDate() - 2);

                    data.items.forEach(item => {
                      const pubDate = new Date(item.pubDate);
                      if(pubDate >= threeDaysAgo && pubDate <= now) {
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
                        if(imgSrc) {
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
            <!-- TradingView Widget BEGIN -->
            <div class="tradingview-widget-container">
              <div class="tradingview-widget-container__widget"></div>
              <div class="tradingview-widget-copyright">
                <a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank">
                  <span class="blue-text"></span>
                </a>
              </div>
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-tickers.js" async>
              {
              "symbols": [
               
                {
                  "description": "Nasdaq 100",
                  "proName": "NASDAQ:NDX"
                },
                {
                  "description": "FTSE 100",
                  "proName": "OANDA:UK100GBP"
                },
                {
                  "description": "DAX 40",
                  "proName": "XETR:DAX"
                },
                
                {
                  "description": "Nikkei 225",
                  "proName": "INDEX:NKY"
                },
                {
                  "description": "Hang Seng",
                  "proName": "HSI:HSI"
                },
               
                {
                  "description": "BSE Sensex",
                  "proName": "INDEX:SENSEX"
                },
                {
                  "description": "MSCI World",
                  "proName": "TVC:WORLD"
                },
                {
                  "description": "Euro Stoxx 50",
                  "proName": "INDEX:STOXX50E"
                }
              ],
              "isTransparent": false,
              "showSymbolLogo": true,
              "colorTheme": "light",
              "locale": "en"
            }
              </script>
            </div>
            <!-- TradingView Widget END -->

          <meta charset="UTF-8"/>
          <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
          <title>Global News</title>
          <style>
            body { font-family: 'Georgia', serif; background: #f9f9f9; margin: 0; padding: 0; }
            header { background: white; padding: 20px; text-align: center; font-size: 2rem; border-bottom: 1px solid #ddd; }
            #category-buttons { display: flex; flex-wrap: wrap; justify-content: center; background: #fff; border-bottom: 1px solid #ddd; }
            .category-btn {
              margin: 10px; padding: 10px 20px; background: #eee; border: none; border-radius: 5px;
              cursor: pointer; font-size: 1rem; transition: background 0.3s;
            }
            .category-btn:hover { background: #ccc; }
            .news-section { padding: 20px; max-width: 1200px; margin: auto; }
            .category-header {
              font-size: 1.5rem; border-bottom: 2px solid #333; padding-bottom: 5px; margin-top: 40px;
            }
            .news-card {
              display: flex; flex-direction: row; background: white; border-radius: 10px;
              margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); overflow: hidden;
            }
            .news-content { padding: 15px; flex: 1; }
            .news-content h3 { margin: 0; font-size: 1.2rem; line-height:1.2; }
            .news-content a { color: #333; text-decoration: none; }
            .news-content a:hover { text-decoration: underline; }
            .news-date { color: #888; font-size: 0.9rem; margin: 5px 0; }
            .news-summary { font-size: 1rem; color: #555; }
            @media (max-width: 600px) { .news-card { flex-direction: column; } }
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

          Object.keys(feedsByCategory).forEach(category => {
            const btn = document.createElement('button');
            btn.className = 'category-btn';
            btn.innerText = category;
            btn.onclick = () => filterCategory(category);
            categoryButtonsDiv.appendChild(btn);
          });

          Object.keys(feedsByCategory).forEach(category => renderCategory(category));

          function filterCategory(category) {
            const sections = document.querySelectorAll('.news-category');
            sections.forEach(section => {
              section.style.display = (section.dataset.category === category) ? 'block' : 'none';
              if(section.style.display === 'block') section.scrollIntoView({behavior:'smooth'});
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
                  if(data.status === "ok") {
                    const now = new Date();
                    const threeDaysAgo = new Date();
                    threeDaysAgo.setDate(now.getDate() - 2);

                    data.items.forEach(item => {
                      const pubDate = new Date(item.pubDate);
                      if(pubDate >= threeDaysAgo && pubDate <= now) {
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
                        if(imgSrc) {
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

    with tab_blogs:


        st.set_page_config(page_title="Top Blogs Browser", layout="wide")

        st.markdown("""
            <style>
            body, .css-18e3th9 {
                font-family: Georgia, Georgia;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("Top Blogs")

        blogs = [
            {"title": "Lifehacker", "url": "https://lifehacker.com/"},
            {"title": "Wired", "url": "https://www.wired.com/"},
            {"title": "VentureBeat", "url": "https://venturebeat.com/"},
            {"title": "Copyblogger", "url": "https://copyblogger.com/"},
            {"title": "Neil Patel Blog", "url": "https://neilpatel.com/blog/"},
            {"title": "Moz Blog", "url": "https://moz.com/blog"},
            {"title": "Social Media Examiner", "url": "https://www.socialmediaexaminer.com/"},
            {"title": "The Next Web", "url": "https://thenextweb.com/"},
            {"title": "Vogue", "url": "https://www.vogue.com/"},
            {"title": "GQ", "url": "https://www.gq.com/"},
            {"title": "Pitchfork", "url": "https://pitchfork.com/"},
            {"title": "CNET", "url": "https://www.cnet.com/"},
            {"title": "Shopify Blog", "url": "https://www.shopify.com/blog"},
            {"title": "Smart Passive Income", "url": "https://www.smartpassiveincome.com/blog/"},
            {"title": "Copyhackers", "url": "https://copyhackers.com/blog/"},
        ]

        blog_titles = [blog["title"] for blog in blogs]

        if "selected_blog" not in st.session_state:
            st.session_state.selected_blog = blog_titles[0]

        selected_blog = st.segmented_control("Select a blog to read", blog_titles, key="selected_blog")

        @st.cache_data(show_spinner=False)
        def get_url_from_title(title):
            for blog in blogs:
                if blog["title"] == title:
                    return blog["url"]
            return None

        selected_url = get_url_from_title(selected_blog)

        if selected_url:
            iframe_html = f"""
            <div style="position: relative; width: 100%; height: 2000px;">
                <iframe src="{selected_url}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border:none;" allowfullscreen></iframe>
            </div>
            """
            components.html(iframe_html, height=2000)
        else:
            st.warning("Selected blog URL could not be found.")

    with tab_books:

        st.set_page_config(page_title="Free Books Browser", layout="wide")

        st.markdown("""
            <style>
            body, .css-18e3th9 {
                font-family: Georgia, Georgia;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("Free Books")

        books_sources = [
            {"title": "Project Gutenberg", "url": "https://www.gutenberg.org/"},
            {"title": "Open Library", "url": "https://openlibrary.org/"},
            {"title": "LibriVox (Audiobooks)", "url": "https://librivox.org/"},
            {"title": "Internet Archive - eBooks", "url": "https://archive.org/details/texts"},
            {"title": "Free-EBooks.net", "url": "https://www.free-ebooks.net/"},
            {"title": "Obooko", "url": "https://www.obooko.com/"},
            {"title": "Classicly", "url": "https://classicly.com/"},
            {"title": "GetFreeEBooks", "url": "https://www.getfreeebooks.com/"},
            {"title": "BookRix", "url": "https://www.bookrix.com/"},
            {"title": "FreeComputerBooks", "url": "https://freecomputerbooks.com/"},
            {"title": "Planet eBook", "url": "https://www.planetebook.com/"},
            {"title": "PDF Books World", "url": "https://www.pdfbooksworld.com/"},
            {"title": "Open Culture", "url": "https://www.openculture.com/free_ebooks"},
            {"title": "PublicBookshelf", "url": "https://www.publicbookshelf.com/"},
            {"title": "WikiSource", "url": "https://en.wikisource.org/wiki/Main_Page"},
            {"title": "International Children's Digital Library", "url": "http://en.childrenslibrary.org/"},
            {"title": "HathiTrust Digital Library", "url": "https://www.hathitrust.org/"},
            {"title": "Project Muse", "url": "https://muse.jhu.edu/"},
            {"title": "Literature Project", "url": "https://www.literatureproject.com/"},
            {"title": "Classic Bookshelf", "url": "http://www.classicbookshelf.com/"},
            {"title": "WikiBooks", "url": "https://www.wikibooks.org/"},
            {"title": "Authorama", "url": "http://www.authorama.com/"},

        ]

        titles = [source["title"] for source in books_sources]

        # Initialize session_state key if not present
        if "selected_source" not in st.session_state:
            st.session_state.selected_source = titles[0]

        selected_source = st.segmented_control("Select a free book source", titles, key="selected_source")

        @st.cache_data(show_spinner=False)
        def get_url_from_title(title):
            # Cache the lookup by title
            for source in books_sources:
                if source["title"] == title:
                    return source["url"]
            return None

        selected_url = get_url_from_title(selected_source)

        if selected_url:
            iframe_html = f"""
            <div style="position: relative; width: 100%; height: 2000px;">
                <iframe src="{selected_url}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border:none;" allowfullscreen></iframe>
            </div>
            """
            components.html(iframe_html, height=2000)
        else:
            st.warning("Selected book source URL could not be found.")

    with tab_aiknowledge:

        st.set_page_config(page_title="AI Search Engines Browser", layout="wide")

        st.markdown("""
            <style>
            body, .css-18e3th9 {
                font-family: Georgia, Georgia;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("AI Tools and Search engines")

        ai_search_sources = [

            {"title": "Exa AI", "url": "https://exa.ai"},
            {"title": "Anthropic Claude", "url": "https://www.anthropic.com/"},
            {"title": "Komo AI", "url": "https://komo.ai/"},
            {"title": "DeepSeek AI", "url": "https://deepseek.ai/"},
            {"title": "Consensus AI", "url": "https://consensus.app/search"},
            {"title": "SearXNG", "url": "https://searxng.org/"},
            {"title": "Toolify AI Tools Directory", "url": "https://www.toolify.ai"},
            {"title": "Futurepedia AI Tools Directory", "url": "https://www.futurepedia.io"},
            {"title": "There's An AI For That", "url": "https://theresanaiforthat.com"},
            {"title": "Vercel AI Search", "url": "https://vercel.com/ai"},
            {"title": "Cogram AI Search", "url": "https://cogram.com/"},
            {"title": "Genei AI", "url": "https://genei.io/"},
            {"title": "Elicit AI Research Assistant", "url": "https://elicit.org/"},
            {"title": "Research Rabbit", "url": "https://researchrabbitapp.com/"},
            {"title": "TopBots AI Search Directory", "url": "https://www.topbots.com/ai-tools/"},
            {"title": "Learn Prompting", "url": "https://learnprompting.org/"},
            {"title": "GPT Index", "url": "https://gpt-index.readthedocs.io/"},
            {"title": "AI Tools List", "url": "https://aitoolsdirectory.com/"},
            {"title": "AI Tool Tracker", "url": "https://www.aitooltracker.com/"},
            {"title": "AI Radar", "url": "https://airadar.io/"},
            {"title": "AI Landscape", "url": "https://landscape.lfai.foundation/"},
            {"title": "Lambda Labs AI Tools", "url": "https://lambdalabs.com/"},
            {"title": "AI Dungeon", "url": "https://play.aidungeon.io/"},
            {"title": "AI Experiments by Google", "url": "https://experiments.withgoogle.com/collection/ai"},
            {"title": "Chromebot AI", "url": "https://chromebot.ai/"},
            {"title": "Microsoft Cognitive Services", "url": "https://azure.microsoft.com/en-us/services/cognitive-services/"},
            {"title": "OpenAI Codex", "url": "https://openai.com/blog/openai-codex/"},
            {"title": "Pictory AI", "url": "https://pictory.ai/"},
            {"title": "Reviewshake AI", "url": "https://reviewshake.com/"},
            {"title": "Beautiful AI", "url": "https://www.beautiful.ai/"},
            {"title": "ContentBot AI", "url": "https://contentbot.ai/"},
            {"title": "GrowthBar AI", "url": "https://www.growthbarseo.com/"},
            {"title": "TextCortex AI", "url": "https://textcortex.com/"},
            {"title": "Lately AI", "url": "https://www.lately.ai/"},
            {"title": "Surfer SEO AI", "url": "https://surferseo.com/"},
            {"title": "MarketMuse AI", "url": "https://marketmuse.com/"},
            {"title": "Outranking AI", "url": "https://www.outranking.io/"},
            {"title": "Text Blaze AI", "url": "https://blaze.today/"},
            {"title": "Smartwriter AI", "url": "https://www.smartwriter.ai/"},

        ]

        titles = [source["title"] for source in ai_search_sources]

        # Initialize session_state key if not present
        if "selected_ai_source" not in st.session_state:
            st.session_state.selected_ai_source = titles[0]

        selected_source = st.segmented_control("Select an AI search engine", titles, key="selected_ai_source")

        @st.cache_data(show_spinner=False)
        def get_url_from_title(title):
            for source in ai_search_sources:
                if source["title"] == title:
                    return source["url"]
            return None

        selected_url = get_url_from_title(selected_source)

        if selected_url:
            iframe_html = f"""
            <div style="position: relative; width: 100%; height: 1200px;">
                <iframe src="{selected_url}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border:none;" allowfullscreen></iframe>
            </div>
            """
            components.html(iframe_html, height=1200)
        else:
            st.warning("Selected AI search engine URL could not be found.")





    with tab_travel:


        st.set_page_config(page_title="Travel Browser", layout="wide")

        st.markdown("""
            <style>
            body, .css-18e3th9 {
                font-family: Georgia, Georgia;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("Travel Resources")

        travel_sites = [
            {"title": "Lonely Planet", "url": "https://www.lonelyplanet.com/"},
            {"title": "National Geographic Travel", "url": "https://www.nationalgeographic.com/travel/"},
            {"title": "The Points Guy", "url": "https://thepointsguy.com/"},
            {"title": "Rough Guides", "url": "https://www.roughguides.com/"},
            {"title": "Jetsetter", "url": "https://www.jetsetter.com/"},

            {"title": "Travel Noire", "url": "https://travelnoire.com/"},


            {"title": "Adventurous Kate", "url": "https://www.adventurouskate.com/"},

            {"title": "Hand Luggage Only", "url": "https://www.handluggageonly.co.uk/"},

            {"title": "Travelling King", "url": "https://travellingking.com/"},

            {"title": "Travel Awaits", "url": "https://www.travelawaits.com/"},

            {"title": "BootsnAll", "url": "https://www.bootsnall.com/"},
            {"title": "Atlas & Boots", "url": "https://atlasandboots.com/"},

            {"title": "Road Affair", "url": "https://www.roadaffair.com/"},
            {"title": "Roads & Kingdoms", "url": "https://roadsandkingdoms.com/"},
            {"title": "The Travel Tester", "url": "https://thetraveltester.com/"},
            {"title": "Where’s Sharon", "url": "https://wheressharon.com/"},

        ]

        titles = [site["title"] for site in travel_sites]

        if "selected_travel_site" not in st.session_state:
            st.session_state.selected_travel_site = titles[0]

        selected_site = st.segmented_control("Select a travel site", titles, key="selected_travel_site")

        @st.cache_data(show_spinner=False)
        def get_url_from_title(title):
            for site in travel_sites:
                if site["title"] == title:
                    return site["url"]
            return None

        selected_url = get_url_from_title(selected_site)

        if selected_url:
            iframe_html = f"""
            <div style="position: relative; width: 100%; height: 2000px;">
                <iframe src="{selected_url}" style="position: absolute; top:0; left:0; width:100%; height:100%; border:none;" allowfullscreen></iframe>
            </div>
            """
            components.html(iframe_html,height=2000)
        else:
            st.warning("Selected travel site URL could not be found.")
    
    with tab_music :


        st.set_page_config(page_title="Free Music Browser", layout="wide")

        st.markdown("""
            <style>
            body, .css-18e3th9 {
                font-family: Georgia, Georgia;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("Free Music Sources")


        music_sources = [
            {"title": "Freefy", "url": "https://freefy.app/"},
            {"title": "Soundstripe", "url": "https://www.soundstripe.com/"},
            {"title": "Littlive", "url": "https://littlive.com/genres"},
            {"title": "Freeplay Music", "url": "https://freeplaymusic.com/"},
            {"title": "iHeartRadio", "url": "https://www.iheart.com/"},
            {"title": "Bandcamp", "url": "https://bandcamp.com/"},
            {"title": "Internet Archive Audio", "url": "https://archive.org/details/audio/"},
            {"title": "JamPlay", "url": "https://www.jamplay.com/"},
            {"title": "Spinrilla", "url": "https://www.spinrilla.com/"},
            {"title": "DatPiff", "url": "https://www.datpiff.com/"},

            {"title": "Radio Garden", "url": "http://radio.garden/"},
            {"title": "TeknoAXE", "url": "https://teknoaxe.com/Home.php"},
            {"title": "PureVolume", "url": "https://purevolume.com/"},
            {"title": "LiveOne", "url": "https://www.liveone.com/"},



        # Add up to 100+ with more genre-specific, classical, podcast sources, radio stations, and new independent music hubs...
        ]
        titles = [source["title"] for source in music_sources]

        if "selected_music_source" not in st.session_state:
            st.session_state.selected_music_source = titles[0]

        selected_source = st.segmented_control("Select a free music source", titles, key="selected_music_source")

        @st.cache_data(show_spinner=False)
        def get_url_from_title(title):
            for source in music_sources:
                if source["title"] == title:
                    return source["url"]
            return None

        selected_url = get_url_from_title(selected_source)

        if selected_url:
            iframe_html = f"""
            <div style="position: relative; width: 100%; height: 1200px;">
                <iframe src="{selected_url}" style="position: absolute; top: 0; left: 0; 
                width: 100%; height: 100%; border:none;" allowfullscreen></iframe>
            </div>
            """
            components.html(iframe_html, height=1200)
        else:
            st.warning("Selected music source URL could not be found.")

    with tab_Radio:
        import random
        import requests

        from streamlit_extras.switch_page_button import switch_page  # Optional for multi-page
        import time

        # Custom CSS for modern radio UI
        st.markdown("""
        <style>
            .main-header {
                font-size: 3rem !important;
                font-weight: 800 !important;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                margin-bottom: 2rem;
            }
            .now-playing {
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
                padding: 1.5rem;
                border-radius: 20px;
                margin: 1rem 0;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            .station-card {
                background: rgba(255,255,255,0.95);
                padding: 1.5rem;
                border-radius: 15px;
                margin: 1rem 0;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
            }
            .favorite-btn {
                background: linear-gradient(45deg, #ffd700, #ffed4e);
                border: none;
                border-radius: 50px;
                padding: 0.8rem 1.5rem;
                font-weight: bold;
                font-size: 1.1rem;
                transition: all 0.3s ease;
            }
            .favorite-btn:hover {
                transform: scale(1.05);
                box-shadow: 0 5px 15px rgba(255,215,0,0.4);
            }
            .surprise-btn {
                background: linear-gradient(45deg, #ff9a9e, #fecfef);
                border-radius: 50px;
                padding: 1rem 2rem;
                font-size: 1.2rem;
                font-weight: bold;
            }
            .metric-container {
                background: rgba(0,0,0,0.1);
                padding: 1rem;
                border-radius: 10px;
            }
        </style>
        """, unsafe_allow_html=True)

        st.set_page_config(
            page_title="🌐 World Radio Hub",
            layout="wide",
            page_icon="🎵",
            initial_sidebar_state="collapsed"
        )

        # Enhanced theme config
        st.markdown("""
        <style>
        [theme]
        primaryColor="#667eea"
        backgroundColor="#0f0f23"
        secondaryBackgroundColor="#1a1a2e"
        textColor="#e0e0e0"
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<h1 class="main-header">🌐 World Radio Hub</h1>', unsafe_allow_html=True)

        API_BASE = "https://de1.api.radio-browser.info/json"

        # ---------- Enhanced caching with better error handling ----------
        @st.cache_data(ttl=1800, show_spinner=False)
        def get_top_stations(limit=300):
            try:
                url = f"{API_BASE}/stations/topclick"
                resp = requests.get(url, params={"limit": limit, "hidebroken": True}, timeout=15)
                resp.raise_for_status()
                return resp.json()
            except:
                return []

        @st.cache_data(ttl=3600)
        def get_countries():
            try:
                url = f"{API_BASE}/countries"
                resp = requests.get(url, timeout=10)
                return resp.json()
            except:
                return []

        @st.cache_data(ttl=3600)
        def get_languages():
            try:
                url = f"{API_BASE}/languages"
                resp = requests.get(url, timeout=10)
                return resp.json()
            except:
                return []

        @st.cache_data(ttl=3600)
        def search_stations_advanced(filters, limit=200):
            url = f"{API_BASE}/stations/search"
            params = {
                "limit": limit,
                "hidebroken": True,
                "has_geo": True,
            }
            for key, value in filters.items():
                if value:
                    params[key] = value
            try:
                resp = requests.get(url, params=params, timeout=15)
                resp.raise_for_status()
                return resp.json()
            except:
                return []

        def enhanced_station_display(s):
            name = s.get("name", "Unknown")[:50]
            country = s.get("country", "🌍")
            bitrate = s.get("bitrate", 0)
            codec = s.get("codec", "?")
            quality = "🔴" if bitrate < 64 else "🟡" if bitrate < 128 else "🟢"
            return f"{name} {quality} [{country}]"

        def create_station_card(station, is_playing=False):
            col1, col2, col3 = st.columns([1, 3, 1])

            with col1:
                st.markdown(f"**{station.get('name', 'Unknown')}**")
                st.caption(f"🇸🇽 {station.get('country', 'N/A')} | {station.get('language', 'N/A')}")

            with col2:
                bitrate = station.get("bitrate", 0)
                quality = "🔴 Poor" if bitrate < 64 else "🟡 Good" if bitrate < 128 else "🟢 HQ"
                st.metric("Quality", f"{bitrate}kbps", quality)
                tags = station.get("tags", "")
                if tags:
                    st.caption(f"🎯 {tags}")

            with col3:
                favicon = station.get("favicon")
                if favicon:
                    st.image(favicon, width=50, use_column_width=None)

        # ---------- Global session state ----------
        if "current_station" not in st.session_state:
            st.session_state.current_station = None
        if "favorites" not in st.session_state:
            st.session_state.favorites = set()
        if "history" not in st.session_state:
            st.session_state.history = []
        if "player_state" not in st.session_state:
            st.session_state.player_state = "stopped"

        # ---------- Main layout ----------
        header_col1, header_col2 = st.columns([4, 1])

        with header_col2:
            if st.button("🎲 Surprise Me!", key="global_surprise", help="Random station from top 200"):
                top_stations = get_top_stations()
                if top_stations:
                    st.session_state.current_station = random.choice(top_stations)
                    st.session_state.player_state = "playing"
                    st.rerun()

        # Now playing section (sticky)
        if st.session_state.current_station:
            with st.container():
                st.markdown('<div class="now-playing">', unsafe_allow_html=True)
                st.markdown("### 🎵 Now Playing")
                create_station_card(st.session_state.current_station)

                col_btn1, col_audio, col_btn2 = st.columns([1, 4, 1])

                with col_btn1:
                    if st.button("★" if st.session_state.current_station.get("stationuuid") not in st.session_state.favorites else "⭐",
                                 key="toggle_fav_global", help="Add to favorites"):
                        uuid = st.session_state.current_station.get("stationuuid")
                        if uuid:
                            if uuid in st.session_state.favorites:
                                st.session_state.favorites.discard(uuid)
                            else:
                                st.session_state.favorites.add(uuid)
                            st.rerun()

                with col_audio:
                    stream_url = st.session_state.current_station.get("url_resolved") or st.session_state.current_station.get("url")
                    if stream_url:
                        st.audio(stream_url, autoplay=True, sample_rate=44100)
                    else:
                        st.error("❌ No stream available")

                with col_btn2:
                    if st.button("⏹️ Stop", key="stop_global"):
                        st.session_state.current_station = None
                        st.session_state.player_state = "stopped"
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("👆 Select a station from tabs below to start listening!")

        # ---------- Enhanced sidebar ----------
        with st.sidebar:
            st.markdown("### 🎛️ Quick Controls")

            # Load filter data
            countries = get_countries()
            languages = get_languages()

            st.markdown("#### 🌍 Filters")
            country = st.selectbox("Country", [""] + [c["name"] for c in countries[:250]])
            language = st.selectbox("Language", [""] + [l["name"] for l in languages[:250]])
            min_bitrate = st.slider("Min Quality", 0, 320, 64)

            st.markdown("---")

            st.markdown("#### ⭐ Favorites")
            if st.session_state.favorites:
                st.success(f"{len(st.session_state.favorites)} saved")
            else:
                st.info("No favorites yet")

            if st.button("🗑️ Clear All", key="clear_all"):
                st.session_state.favorites.clear()
                st.session_state.history.clear()
                st.session_state.current_station = None
                st.rerun()

        # ---------- Main tabs ----------
        tab1, tab2, tab3, tab4 = st.tabs(["🎯 Top Hits", "🔍 Discover", "⭐ Favorites", "📜 History"])

        with tab1:
            st.header("🌟 Top 300 Global Stations")
            stations = [s for s in get_top_stations(300) if (s.get("bitrate", 0) >= min_bitrate)]

            if stations:
                labels = [enhanced_station_display(s) for s in stations]
                selected = st.selectbox("Pick your station:", labels, key="top_select")
                station = stations[labels.index(selected)]

                if st.button("▶️ Play", key="play_top"):
                    st.session_state.current_station = station
                    if station.get("stationuuid") not in st.session_state.history:
                        st.session_state.history.append(station)
                        if len(st.session_state.history) > 20:
                            st.session_state.history.pop(0)
                    st.rerun()

        with tab2:
            st.header("🧭 Discover New Stations")
            filters = {"country": country, "language": language}
            stations = [s for s in search_stations_advanced(filters, 200) if (s.get("bitrate", 0) >= min_bitrate)]

            if stations:
                labels = [enhanced_station_display(s) for s in stations]
                selected = st.selectbox("Found stations:", labels, key="disc_select")
                station = stations[labels.index(selected)]

                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"[🌐 {station.get('homepage', '#')}]({station.get('homepage', '#')})")
                with col2:
                    if st.button("▶️ Play", key="play_disc"):
                        st.session_state.current_station = station
                        st.session_state.history.append(station)
                        st.rerun()

        with tab3:
            st.header("⭐ Your Favorites")
            fav_stations = []
            all_stations = get_top_stations(500) + search_stations_advanced({}, 500)

            for uuid in st.session_state.favorites:
                for s in all_stations:
                    if s.get("stationuuid") == uuid:
                        fav_stations.append(s)
                        break

            if fav_stations:
                labels = [enhanced_station_display(s) for s in fav_stations]
                selected = st.selectbox("Play favorite:", labels, key="fav_select")
                station = fav_stations[labels.index(selected)]

                if st.button("▶️ Play", key="play_fav"):
                    st.session_state.current_station = station
                    st.rerun()

        with tab4:
            st.header("📜 Recently Played")
            recent = st.session_state.history[-10:][::-1]
            for i, station in enumerate(recent, 1):
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{i}.** {enhanced_station_display(station)}")
                    with col2:
                        if st.button("▶️", key=f"play_hist_{i}"):
                            st.session_state.current_station = station
                            st.rerun()

        # Footer
        st.markdown("---")
        st.markdown("*Built for music lovers worldwide. Data from [Radio Browser API](https://www.radio-browser.info/)* 🎵✨")




if __name__ == "__main__":
    main()
