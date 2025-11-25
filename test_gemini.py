import google.generativeai as genai

# Test Gemini API
GEMINI_API_KEY = "AIzaSyCE5vVXwMaXGcMjYqalQsY9iWxsKuHuPYw"
genai.configure(api_key=GEMINI_API_KEY)

try:
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    response = model.generate_content("Say hello in one word")
    print(f"✅ Gemini API Working!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Gemini API Error: {e}")
    print("\nTrying alternative model...")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say hello in one word")
        print(f"✅ Alternative model works!")
        print(f"Response: {response.text}")
    except Exception as e2:
        print(f"❌ Alternative also failed: {e2}")
