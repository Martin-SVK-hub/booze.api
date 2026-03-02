import requests
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    try:
        # Načítanie dát z API
        response = requests.get("https://boozeapi.com/api/v1/cocktails")
        if response.status_code != 200:
            return f"Chyba pri načítaní API: {response.status_code}"

        data = response.json()

        # Počítadlo podľa typu alkoholu
        pocitadlo = {
            "Vodka": 0,
            "Gin": 0,
            "Rum": 0
        }

        # Začiatok HTML s dizajnom
        html = """
        <!DOCTYPE html>
        <html lang="sk">
        <head>
        <meta charset="UTF-8">
        <title>Zoznam drinkov</title>
        <style>
            body {
                background-color: #1e1e2f;
                color: #f0f0f0;
                font-family: 'Arial', sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
            }
            h1 {
                margin-top: 20px;
                font-size: 3em;
                background: linear-gradient(to right, #ff6ec4, #7873f5);
                -webkit-background-clip: text;
                color: transparent;
            }
            .drink-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                padding: 20px;
            }
            .drink-card {
                background-color: #2b2b44;
                border-radius: 15px;
                padding: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.5);
                transition: transform 0.3s;
            }
            .drink-card:hover {
                transform: scale(1.05);
            }
            .drink-card img {
                width: 100%;
                border-radius: 10px;
            }
            .stats {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin: 30px 0;
            }
            .stat-box {
                background-color: #3c3c5c;
                padding: 20px;
                border-radius: 10px;
                width: 150px;
            }
        </style>
        </head>
        <body>
        <h1>Zoznam drinkov</h1>
        <div class="drink-grid">
        """

        # Pridanie drinkov do gridu
        for cocktail in data.get("data", []):
            nazov = cocktail.get("name", "Neznámy drink")
            obrazok = cocktail.get("image", "")
            html += f"""
            <div class="drink-card">
                <img src="{obrazok}" alt="{nazov}">
                <h3>{nazov}</h3>
            </div>
            """

            # Počítanie podľa alkoholu
            for ingredient in cocktail.get("ingredients", []):
                typ = ingredient.get("type")
                if typ in pocitadlo:
                    pocitadlo[typ] += 1

        html += "</div><div class='stats'>"
        for alkohol, pocet in pocitadlo.items():
            html += f"<div class='stat-box'><h3>{alkohol}</h3><p>{pocet}</p></div>"
        html += "</div></body></html>"

        return html

    except Exception as e:
        return f"Nastala chyba: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)