def check_live_google_rank(keyword):
    try:
        query = urllib.parse.quote(keyword)
        # Google search URL with India (gl=in) and English (hl=en)
        url = f"https://www.google.com/search?q={query}&gl=in&hl=en"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        resp = requests.get(url, headers=headers, timeout=6)
        
        if resp.status_code != 200:
            return "Google Blocked (Captcha / 403)"
            
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Google ke standard organic search result blocks (`div.g`) ko scan karein
        search_results = soup.select("div.g")
        
        for idx, result in enumerate(search_results, start=1):
            result_text = result.get_text().lower()
            if BUSINESS_NAME.lower() in result_text:
                return f"Rank #{idx} 🎯"
                
        # Agar div.g mein nahi mila, toh poore page text mein check karein
        page_text = soup.get_text().lower()
        if BUSINESS_NAME.lower() in page_text:
            return "Indexed in Top 20 (Exact position structure changed)"
            
        return "Not in Top 20"
        
    except Exception as e:
        return f"Scan Error"
