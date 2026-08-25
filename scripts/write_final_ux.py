import os

def generate():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "src", "components", "single-page-app.tsx"))
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix any :,.0f or Python formatting in the JS code
    fixed_content = content.replace("currentRoom.tariff:,.0f", "currentRoom.tariff.toLocaleString('en-IN')")
    fixed_content = fixed_content.replace(":,.0f", ".toLocaleString('en-IN')")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(fixed_content)
        
    print("Fixed formatting in:", path)

if __name__ == "__main__":
    generate()
