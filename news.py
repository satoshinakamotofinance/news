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

    tab_globe, tab_commnews, tab_technology, tab_pods, tab_blogs,tab_books,tab_aiknowledge,tab_travel,tab_music,tab_sports,tab_food,tab_startups,tab_space,tab_gaming,tab_finance,  tab_science, tab_health,tab_editorial = st.tabs([
        "Global", "Commodities", "Technology",   "Pods", "Blogs", "Books", "AiKnowledge","Travel","Music","Sports","Food","Startups","Space","Gaming","Finance",  "Science", "Health",   "Editorial"
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



    with tab_food:
        st.set_page_config(page_title="Food & Recipe Browser", layout="wide")

        st.markdown("""
            <style>
            body, .css-18e3th9 {
                font-family: Georgia, Georgia;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("Food & Recipe Sites")

        food_sources = [
            # Global recipe portals

            {"title": "Epicurious", "url": "https://www.epicurious.com/"},
            {"title": "Food52", "url": "https://food52.com/"},

            # Popular food blogs
            {"title": "Pinch of Yum", "url": "https://pinchofyum.com/"},
            {"title": "Minimalist Baker", "url": "https://minimalistbaker.com/"},
            {"title": "Smitten Kitchen", "url": "https://smittenkitchen.com/"},

            {"title": "Hebbars Kitchen", "url": "https://hebbarskitchen.com/"},

            {"title": "Archana's Kitchen", "url": "https://www.archanaskitchen.com/"},




            # Restaurant discovery / guides




        ]

        titles = [source["title"] for source in food_sources]

        if "selected_food_source" not in st.session_state:
            st.session_state.selected_food_source = titles[0]

        selected_source = st.segmented_control(
            "Select a food or recipe site",
            titles,
            key="selected_food_source"
        )

        @st.cache_data(show_spinner=False)
        def get_url_from_title(title):
            for source in food_sources:
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
            st.warning("Selected food site URL could not be found.")

    with tab_startups:
        st.set_page_config(page_title="Startup Browser", layout="wide")

        st.markdown("""
            <style>
            body, .css-18e3th9 {
                font-family: Georgia, Georgia;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("Startup Resources & News")

        startup_sources = [
            # Global startup news

            {"title": "VentureBeat – Startups", "url": "https://venturebeat.com/category/startups/"},

            {"title": "The Next Web – Growth Quarters", "url": "https://thenextweb.com/growth-quarters"},
            {"title": "StartupBlink – Startup News", "url": "https://www.startupblink.com/blog/top-startup-news-outlets-to-follow-for-entrepreneurs-founders/"},

            # Indian startup ecosystem

            {"title": "VidSaga – Indian Startup Media Portals", "url": "https://www.vidsaga.com/startup-media-portals/"},

            # Product discovery & launches

            {"title": "Indie Hackers – Product Listings", "url": "https://www.indiehackers.com/products"},

            {"title": "Startup Stash – Tools Directory", "url": "https://startupstash.com/"},
            {"title": "Bizplanr – Startup Resources List", "url": "https://bizplanr.ai/blog/startup-resources"},

            {"title": "SaaStr – SaaS & Startups", "url": "https://www.saastr.com/"},
            {"title": "First Round Review", "url": "https://review.firstround.com/"},
        ]

        titles = [source["title"] for source in startup_sources]

        if "selected_startup_source" not in st.session_state:
            st.session_state.selected_startup_source = titles[0]

        selected_source = st.segmented_control(
            "Select a startup site",
            titles,
            key="selected_startup_source"
        )

        @st.cache_data(show_spinner=False)
        def get_url_from_title(title):
            for source in startup_sources:
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
            st.warning("Selected startup site URL could not be found.")



    with tab_space:
        st.markdown("""
            <style>
            body, .css-18e3th9 {
                font-family: Georgia, Georgia;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("Space Resources & News")

        space_sources = [
            # Global space news

            {"title": "SpaceNews", "url": "https://spacenews.com/"},

            # SpaceX and commercial space

            # Astronomy & missions
            {"title": "Universe Today", "url": "https://www.universetoday.com/"},

            {"title": "ESA News", "url": "https://www.esa.int/News"},

        ]

        titles = [source["title"] for source in space_sources]

        if "selected_space_source" not in st.session_state:
            st.session_state.selected_space_source = titles[0]

        selected_source = st.segmented_control(
            "Select a space site",
            titles,
            key="selected_space_source"
        )

        @st.cache_data(show_spinner=False)
        def get_url_from_title(title):
            for source in space_sources:
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
            st.warning("Selected space site URL could not be found.")



    with tab_gaming:
        st.markdown("""
            <style>
            body, .css-18e3th9 {
                font-family: Georgia, Georgia;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("Gaming Resources & News")

        gaming_sources = [

            {"title": "Shacknews", "url": "https://www.shacknews.com/"},             # ✅ Works

            {"title": "Gematsu", "url": "https://www.gematsu.com/"},                 # ✅ Works (Japanese games focus)

        ]

        titles = [source["title"] for source in gaming_sources]
        if "selected_gaming_source" not in st.session_state:
            st.session_state.selected_gaming_source = titles[0]

        selected_source = st.segmented_control("Select gaming site", titles, key="selected_gaming_source")

        @st.cache_data(show_spinner=False)
        def get_url_from_title(title):
            for source in gaming_sources:
                if source["title"] == title:
                    return source["url"]
            return None

        selected_url = get_url_from_title(selected_source)
        if selected_url:
            components.html(f'<iframe src="{selected_url}" style="width:100%;height:1200px;border:none;" allowfullscreen></iframe>', height=1200)
        else:
            st.warning("Selected site URL could not be found.")



    with tab_finance:
        st.markdown("""
            <style>
            body, .css-18e3th9 {
                font-family: Georgia, Georgia;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("Finance Resources & News")

        finance_sources = [


            {"title": "Investing.com", "url": "https://www.investing.com/"},

            {"title": "MoneyControl", "url": "https://www.moneycontrol.com/"},

            {"title": "Zee Business", "url": "https://zeebiz.com/"},
            {"title": "NDTV Profit", "url": "https://www.ndtv.com/profit"},
            {"title": "CNBC TV18", "url": "https://www.cnbctv18.com/"},             # ✅ Indian business news
            {"title": "StockTwits", "url": "https://stocktwits.com/"},               # ✅ Social trading

        ]

        titles = [source["title"] for source in finance_sources]
        if "selected_finance_source" not in st.session_state:
            st.session_state.selected_finance_source = titles[0]

        selected_source = st.segmented_control("Select finance site", titles, key="selected_finance_source")

        @st.cache_data(show_spinner=False)
        def get_url_from_title(title):
            for source in finance_sources:
                if source["title"] == title:
                    return source["url"]
            return None

        selected_url = get_url_from_title(selected_source)
        if selected_url:
            components.html(f'<iframe src="{selected_url}" style="width:100%;height:1200px;border:none;" allowfullscreen></iframe>', height=1200)
        else:
            st.warning("Selected site URL could not be found.")






    with tab_science:
        st.markdown("""
            <style>
            body, .css-18e3th9 {
                font-family: Georgia, Georgia;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("Science Resources & News")

        science_sources = [
            {"title": "ScienceDaily", "url": "https://www.sciencedaily.com/"},
            {"title": "Phys.org", "url": "https://phys.org/"},
            {"title": "Science News", "url": "https://www.sciencenews.org/"},

            {"title": "Universe Today", "url": "https://www.universetoday.com/"},

        ]

        titles = [source["title"] for source in science_sources]
        if "selected_science_source" not in st.session_state:
            st.session_state.selected_science_source = titles[0]

        selected_source = st.segmented_control("Select science site", titles, key="selected_science_source")

        @st.cache_data(show_spinner=False)
        def get_url_from_title(title):
            for source in science_sources:
                if source["title"] == title:
                    return source["url"]
            return None

        selected_url = get_url_from_title(selected_source)
        if selected_url:
            components.html(f'<iframe src="{selected_url}" style="width:100%;height:1200px;border:none;" allowfullscreen></iframe>', height=1200)
        else:
            st.warning("Selected site URL could not be found.")


    with tab_health:
        st.markdown("""
            <style>
            body, .css-18e3th9 {
                font-family: Georgia, Georgia;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("Health Resources & News")

        health_sources = [
            {"title": "WebMD", "url": "https://www.webmd.com/"},
            {"title": "Healthline", "url": "https://www.healthline.com/"},
            {"title": "Medical News Today", "url": "https://www.medicalnewstoday.com/"},

            {"title": "Cleveland Clinic Health", "url": "https://health.clevelandclinic.org/"},

        ]

        titles = [source["title"] for source in health_sources]
        if "selected_health_source" not in st.session_state:
            st.session_state.selected_health_source = titles[0]

        selected_source = st.segmented_control("Select health site", titles, key="selected_health_source")

        @st.cache_data(show_spinner=False)
        def get_url_from_title(title):
            for source in health_sources:
                if source["title"] == title:
                    return source["url"]
            return None

        selected_url = get_url_from_title(selected_source)
        if selected_url:
            components.html(f'<iframe src="{selected_url}" style="width:100%;height:1200px;border:none;" allowfullscreen></iframe>', height=1200)
        else:
            st.warning("Selected site URL could not be found.")



    with tab_editorial:
        st.markdown("""
            <style>
            body, .css-18e3th9 {
                font-family: Georgia, Georgia;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("Editorial & Opinion Resources")

        editorial_sources = [
            {"title": "NY Times Opinion", "url": "https://www.nytimes.com/section/opinion"},



            {"title": "The Atlantic Ideas", "url": "https://www.theatlantic.com/ideas/"},

        ]

        titles = [source["title"] for source in editorial_sources]
        if "selected_editorial_source" not in st.session_state:
            st.session_state.selected_editorial_source = titles[0]

        selected_source = st.segmented_control("Select editorial site", titles, key="selected_editorial_source")

        @st.cache_data(show_spinner=False)
        def get_url_from_title(title):
            for source in editorial_sources:
                if source["title"] == title:
                    return source["url"]
            return None

        selected_url = get_url_from_title(selected_source)
        if selected_url:
            components.html(f'<iframe src="{selected_url}" style="width:100%;height:1200px;border:none;" allowfullscreen></iframe>', height=1200)
        else:
            st.warning("Selected site URL could not be found.")





if __name__ == "__main__":
    main()
