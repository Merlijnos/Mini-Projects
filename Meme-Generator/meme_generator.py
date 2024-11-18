from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple

class MemeGenerator:
    def __init__(self):
        self.beschikbare_stijlen = {
            "klassiek": {
                "font": "impact.ttf",
                "font_size": 60,
                "font_color": "white",
                "stroke_color": "black",
                "stroke_width": 2
            },
            "modern": {
                "font": "arial.ttf",
                "font_size": 50,
                "font_color": "white",
                "stroke_color": "black",
                "stroke_width": 1
            },
            "komisch": {
                "font": "comic.ttf",
                "font_size": 55,
                "font_color": "yellow",
                "stroke_color": "black",
                "stroke_width": 2
            }
        }
        self.huidige_stijl = self.beschikbare_stijlen["klassiek"]

    def pas_stijl_aan(self, stijl: str) -> None:
        if stijl in self.beschikbare_stijlen:
            self.huidige_stijl = self.beschikbare_stijlen[stijl]

    def pas_lettergrootte_aan(self, grootte: int) -> None:
        self.huidige_stijl["font_size"] = grootte

    def pas_kleuren_aan(self, tekst_kleur: str, outline_kleur: str) -> None:
        self.huidige_stijl["font_color"] = tekst_kleur
        self.huidige_stijl["stroke_color"] = outline_kleur

    def maak_meme(self, afbeelding_pad: str, bovenste_tekst: str = "", onderste_tekst: str = "", 
                  tekst_positie: Tuple[float, float] = None) -> Image:
        with Image.open(afbeelding_pad) as img:
            img = img.copy()
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype(self.huidige_stijl["font"], self.huidige_stijl["font_size"])
            except:
                font = ImageFont.load_default()
            
            img_w, img_h = img.size
            
            if bovenste_tekst:
                bbox = draw.textbbox((0, 0), bovenste_tekst.upper(), font=font)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                x = (img_w - w) / 2
                y = 10 if not tekst_positie else tekst_positie[1]
                self._teken_tekst_met_outline(draw, (x, y), bovenste_tekst.upper(), font)
            
            if onderste_tekst:
                bbox = draw.textbbox((0, 0), onderste_tekst.upper(), font=font)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                x = (img_w - w) / 2
                y = img_h - h - 10 if not tekst_positie else tekst_positie[1]
                self._teken_tekst_met_outline(draw, (x, y), onderste_tekst.upper(), font)
            
            return img

    def _teken_tekst_met_outline(self, draw, positie, tekst, font):
        x, y = positie
        stroke_width = self.huidige_stijl["stroke_width"]
        
        # Verbeterde outline voor betere leesbaarheid
        for adj in range(-stroke_width, stroke_width + 1):
            for adj2 in range(-stroke_width, stroke_width + 1):
                draw.text((x+adj, y+adj2), tekst, font=font, fill=self.huidige_stijl["stroke_color"])
        
        draw.text((x, y), tekst, font=font, fill=self.huidige_stijl["font_color"])

def toon_menu():
    print("\n=== Meme Generator Menu ===")
    print("1. Maak een nieuwe meme")
    print("2. Verander meme stijl")
    print("3. Pas lettergrootte aan")
    print("4. Pas kleuren aan")
    print("5. Afsluiten")
    return input("Kies een optie (1-5): ")

def main():
    generator = MemeGenerator()
    
    while True:
        keuze = toon_menu()
        
        if keuze == "1":
            print("\n=== Nieuwe Meme Maken ===")
            afbeelding_pad = input("Geef het pad naar je afbeelding: ").strip('"').strip("'")
            bovenste_tekst = input("Voer de bovenste tekst in (of druk enter voor geen tekst): ")
            onderste_tekst = input("Voer de onderste tekst in (of druk enter voor geen tekst): ")
            
            try:
                meme = generator.maak_meme(afbeelding_pad, bovenste_tekst, onderste_tekst)
                output_naam = "meme_" + os.path.basename(afbeelding_pad)
                meme.save(output_naam)
                print(f"\nMeme opgeslagen als: {output_naam}")
            except Exception as e:
                print(f"Er is een fout opgetreden: {str(e)}")
        
        elif keuze == "2":
            print("\nBeschikbare stijlen:")
            for stijl in generator.beschikbare_stijlen.keys():
                print(f"- {stijl}")
            nieuwe_stijl = input("Kies een stijl: ").lower()
            generator.pas_stijl_aan(nieuwe_stijl)
        
        elif keuze == "3":
            try:
                nieuwe_grootte = int(input("Voer nieuwe lettergrootte in (20-100): "))
                generator.pas_lettergrootte_aan(nieuwe_grootte)
            except ValueError:
                print("Ongeldige invoer. Voer een nummer in.")
        
        elif keuze == "4":
            tekst_kleur = input("Voer tekstkleur in (bijv. white, yellow, red): ")
            outline_kleur = input("Voer outline kleur in (bijv. black, blue): ")
            generator.pas_kleuren_aan(tekst_kleur, outline_kleur)
        
        elif keuze == "5":
            print("Bedankt voor het gebruiken van de Meme Generator!")
            break

if __name__ == "__main__":
    main()