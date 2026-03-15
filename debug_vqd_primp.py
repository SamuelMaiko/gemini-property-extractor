import primp

def test_vqd():
    client = primp.Client(impersonate="chrome_127")
    
    headers = {
        "x-vqd-accept": "1",
        "Referer": "https://duck.ai/",
        "Origin": "https://duck.ai",
    }
    
    print("Trying duck.ai/duckchat/v1/status with primp...")
    try:
        # First visit main page
        client.get("https://duck.ai/")
        
        # Then get status
        response = client.get("https://duck.ai/duckchat/v1/status", headers=headers)
        print(f"Status code: {response.status_code}")
        print("Headers:")
        for k, v in response.headers.items():
            print(f"  {k}: {v}")
            
        vqd_4 = response.headers.get("x-vqd-4")
        vqd_hash = response.headers.get("x-vqd-hash-1")
        
        if vqd_4:
            print(f"FOUND x-vqd-4: {vqd_4}")
        if vqd_hash:
            print(f"FOUND x-vqd-hash-1: {vqd_hash}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_vqd()
