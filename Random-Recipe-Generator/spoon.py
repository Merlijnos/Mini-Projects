import requests
import random
import os
import json
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from datetime import datetime

load_dotenv()
console = Console()

class ReceptenManager:
    def __init__(self):
        self.api_key = os.getenv('SPOONACULAR_API_KEY')
        self.favorieten_bestand = 'favoriete_recepten.json'
        self.favorieten = self.laad_favorieten()

    def laad_favorieten(self):
        try:
            with open(self.favorieten_bestand, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def sla_favorieten_op(self):
        with open(self.favorieten_bestand, 'w') as f:
            json.dump(self.favorieten, f, indent=4)

    def haal_willekeurig_recept(self, dieet=None, keuken=None, max_tijd=None):
        params = {
            'apiKey': self.api_key,
            'number': 1,
            'tags': [],
        }
        
        if dieet:
            params['tags'].append(dieet)
        if keuken:
            params['tags'].append(keuken)
        if max_tijd:
            params['maxReadyTime'] = max_tijd
            
        params['tags'] = ','.join(params['tags']) if params['tags'] else None

        try:
            response = requests.get(
                "https://api.spoonacular.com/recipes/random",
                params=params
            )
            response.raise_for_status()
            return response.json()['recipes'][0]
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error bij ophalen recept: {e}[/red]")
            return None

    def toon_recept(self, recept):
        if not recept:
            return

        # Hoofdpanel met recepttitel
        console.print(Panel(
            f"[bold yellow]{recept['title']}[/bold yellow]",
            style="blue"
        ))

        # Basis informatie tabel
        info_table = Table(show_header=False)
        info_table.add_column("Kenmerk", style="cyan")
        info_table.add_column("Waarde", style="green")
        
        info_table.add_row("Bereidingstijd", f"{recept['readyInMinutes']} minuten")
        info_table.add_row("Porties", str(recept['servings']))
        info_table.add_row("Gezondheidscore", f"{recept.get('healthScore', 'N/A')}/100")
        info_table.add_row("Prijs per portie", f"${recept.get('pricePerServing', 0)/100:.2f}")
        
        console.print(info_table)

        # Ingrediënten
        console.print("\n[bold cyan]Ingrediënten:[/bold cyan]")
        ingredienten_table = Table(show_header=False, box=None)
        for ingredient in recept['extendedIngredients']:
            ingredienten_table.add_row(
                f"• {ingredient['amount']} {ingredient['unit']} {ingredient['name']}"
            )
        console.print(ingredienten_table)

        # Instructies
        console.print("\n[bold cyan]Bereidingswijze:[/bold cyan]")
        if recept.get('analyzedInstructions'):
            for idx, stap in enumerate(recept['analyzedInstructions'][0]['steps'], 1):
                console.print(f"[green]{idx}.[/green] {stap['step']}")
        else:
            console.print(Markdown(recept.get('instructions', 'Geen instructies beschikbaar.')))

    def voeg_toe_aan_favorieten(self, recept):
        favoriete_info = {
            'id': recept['id'],
            'titel': recept['title'],
            'datum_toegevoegd': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'url': recept.get('sourceUrl', ''),
            'bereidingstijd': recept['readyInMinutes']
        }
        self.favorieten.append(favoriete_info)
        self.sla_favorieten_op()
        console.print("[green]Recept toegevoegd aan favorieten![/green]")

    def toon_favorieten(self):
        if not self.favorieten:
            console.print("[yellow]Nog geen favoriete recepten opgeslagen.[/yellow]")
            return

        table = Table(title="Favoriete Recepten")
        table.add_column("Titel", style="cyan")
        table.add_column("Toegevoegd op", style="green")
        table.add_column("Bereidingstijd", style="yellow")
        table.add_column("URL", style="blue")

        for recept in self.favorieten:
            table.add_row(
                recept['titel'],
                recept['datum_toegevoegd'],
                f"{recept['bereidingstijd']} min",
                recept['url']
            )
        console.print(table)

def hoofdmenu():
    manager = ReceptenManager()
    
    while True:
        console.print("\n[bold cyan]🍳 Recepten Generator[/bold cyan]")
        console.print("[1] Zoek willekeurig recept")
        console.print("[2] Bekijk favorieten")
        console.print("[3] Afsluiten")
        
        keuze = Prompt.ask("Maak je keuze", choices=["1", "2", "3"])
        
        if keuze == "1":
            # Filter opties
            dieet = Prompt.ask(
                "Dieet filter (optioneel)", 
                choices=["", "vegetarian", "vegan", "gluten-free"],
                default=""
            )
            keuken = Prompt.ask(
                "Keuken filter (optioneel)", 
                choices=["", "italian", "mexican", "asian", "french"],
                default=""
            )
            max_tijd = Prompt.ask(
                "Maximum bereidingstijd in minuten (optioneel)", 
                default=""
            )
            
            recept = manager.haal_willekeurig_recept(
                dieet if dieet else None,
                keuken if keuken else None,
                int(max_tijd) if max_tijd.isdigit() else None
            )
            
            if recept:
                manager.toon_recept(recept)
                if Confirm.ask("Toevoegen aan favorieten?"):
                    manager.voeg_toe_aan_favorieten(recept)
                    
        elif keuze == "2":
            manager.toon_favorieten()
        else:
            console.print("[yellow]Tot ziens![/yellow]")
            break

if __name__ == "__main__":
    hoofdmenu()