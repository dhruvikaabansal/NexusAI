import google.generativeai as genai
import traceback

GEMINI_API_KEY = "AIzaSyCE5vVXwMaXGcMjYqalQsY9iWxsKuHuPYw"
genai.configure(api_key=GEMINI_API_KEY)

try:
    print("Attempting to generate content with gemini-1.5-flash...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content('Hello')
    print("Success!")
    print(response.text)
except Exception:
    print("Failed!")
    traceback.print_exc()
