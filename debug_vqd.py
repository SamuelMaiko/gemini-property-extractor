import requests

def test_vqd():
    session = requests.Session()
    # Modern Chrome User Agent
    ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    
    session.headers.update({
        "User-Agent": ua,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://duck.ai/",
        "Origin": "https://duck.ai",
    })
    
    print("Step 1: Getting main page (duck.ai)...")
    try:
        r1 = session.get("https://duck.ai/")
        print(f"Main page status: {r1.status_code}")
        
        print("\nStep 2: Getting VQD token from status endpoint (duck.ai)...")
        headers = {"x-vqd-accept": "1"}
        response = session.get("https://duck.ai/duckchat/v1/status", headers=headers)
        print(f"VQD response status: {response.status_code}")
        
        vqd = response.headers.get("x-vqd-4")
        if vqd:
            print(f"SUCCESS! x-vqd-4: {vqd}")
        else:
            print("x-vqd-4 not found.")
            print("Headers found:")
            for k, v in response.headers.items():
                print(f"  {k}: {v}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_vqd()
