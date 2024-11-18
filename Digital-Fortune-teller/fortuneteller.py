import random
import time

# ASCII art voor de kristallen bol
crystal_ball = """
    *    .  *       .   
  .    *        .      
     .-"-.    .     
    /     \      
   |       |     
    \     /   .  
     '-.-'       
"""

# Lijst met voorspellingen
voorspellingen = [
    "Er staat een aangename verrassing te wachten",
    "Nieuwe kansen komen binnenkort op je pad",
    "Een oude vriend zal contact met je opnemen",
    "Wees voorzichtig met belangrijke beslissingen deze week",
    "Geluk staat aan jouw kant",
    "Een langgekoesterde wens zal uitkomen",
    "Reis plannen staan in de sterren geschreven",
    "Een financiële meevaller is onderweg",
    "Nieuwe vriendschappen zullen zich vormen",
    "Volg je intuïtie in de komende dagen"
]

def toon_waarzegger():
    print("\n=== 🔮 Welkom bij de Digitale Waarzegger 🔮 ===")
    print(crystal_ball)
    
    input("Druk op Enter om je fortuin te lezen...")
    print("\nDe kristallen bol wordt helder...")
    time.sleep(1)
    print("De geesten fluisteren...")
    time.sleep(1)
    
    voorspelling = random.choice(voorspellingen)
    print(f"\n🌟 Jouw voorspelling: {voorspelling} 🌟\n")

def main():
    while True:
        toon_waarzegger()
        opnieuw = input("Wil je nog een voorspelling? (ja/nee): ").lower()
        if opnieuw != 'ja':
            print("\nBedankt voor je bezoek aan de digitale waarzegger! Tot ziens! ✨")
            break

if __name__ == "__main__":
    main()