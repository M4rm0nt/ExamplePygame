import random  # Importiere das random-Modul, um Zufallszahlen zu generieren
import pygame  # Importiere das Pygame-Modul für die Spielentwicklung
import sys  # Importiere das sys-Modul für Systemoperationen

# Initialisierung von Pygame
pygame.init()

# Fenstergröße
BREITE, HÖHE = 800, 600  # Definiere die Größe des Spielfensters

# Farben (als RGB-Tupel definiert)
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
BRAUN = (139, 69, 19)
GRÜN = (0, 255, 0)
ROT = (255, 0, 0)

# Initialisierung des Bildschirms
bildschirm = pygame.display.set_mode((BREITE, HÖHE))  # Erstelle den Spielfenster-Bildschirm
pygame.display.set_caption("Rechtecksteuerung")  # Setze den Titel des Spiels

# Spieler- und Objektgrößen
SPIELER_GROESSE = 50
OBJEKT_GROESSE = 30

# Textschriftart
schrift = pygame.font.SysFont(None, 24)  # Lade die Standard-Schriftart für den Text


# Spielerklasse definieren
class Spieler:
    def __init__(self):
        # Spielerposition und Eigenschaften
        self.x = BREITE // 2 - SPIELER_GROESSE // 2
        self.y = HÖHE // 2 - SPIELER_GROESSE // 2
        self.geschwindigkeit = 1
        self.energie = 100
        self.gesammelte_objekte = 0
        self.abgelegte_objekte = []  # Liste der abgelegten Objekte


# Objektklasse definieren
class Objekt:
    def __init__(self, x, y):
        # Objektposition
        self.x = x
        self.y = y

# Funktion für das Hauptspiel
def hauptspiel():
    # Spielobjekte initialisieren
    spieler = Spieler()
    energiegeber = Objekt(BREITE - 50, HÖHE - 50)
    objekt = Objekt(BREITE - 200, HÖHE - 200)
    ablageplatz = Objekt(100, 100)

    # Spielhauptschleife
    läuft = True
    spiel_gewonnen = False
    while läuft:
        # Eventhandling
        for ereignis in pygame.event.get():
            if ereignis.type == pygame.QUIT:
                läuft = False  # Beende das Spiel, wenn das Fenster geschlossen wird

        # Tastatureingaben abfragen
        tasten = pygame.key.get_pressed()
        spieler_bewegen(tasten, spieler)  # Funktion aufrufen, um den Spieler zu bewegen

        # Kollisionsüberprüfung
        kollisionen_prüfen(spieler, energiegeber, objekt, ablageplatz)

        # Spielfeld aktualisieren
        bildschirm_aktualisieren(spieler, energiegeber, objekt, ablageplatz)

        # Bildschirm aktualisieren
        pygame.display.flip()

        # Spiel zurücksetzen, wenn alle Objekte abgelegt wurden und R gedrückt wird
        if len(spieler.abgelegte_objekte) == 5 and tasten[pygame.K_r]:
            reset_spiel(spieler)
            läuft = False
            spiel_gewonnen = True

    # Wenn das Spiel gewonnen wurde, starte es erneut
    if spiel_gewonnen:
        hauptspiel()

    # Pygame beenden
    pygame.quit()
    sys.exit()


# Funktion zum Bewegen des Spielers
def spieler_bewegen(tasten, spieler):
    # Spielerbewegungen verarbeiten und Energie abziehen
    if tasten[pygame.K_LEFT] and spieler.energie > 0 and len(spieler.abgelegte_objekte) != 5:
        spieler.x -= spieler.geschwindigkeit
        spieler.energie -= 0.010
    if tasten[pygame.K_RIGHT] and spieler.energie > 0 and len(spieler.abgelegte_objekte) != 5:
        spieler.x += spieler.geschwindigkeit
        spieler.energie -= 0.010
    if tasten[pygame.K_UP] and spieler.energie > 0 and len(spieler.abgelegte_objekte) != 5:
        spieler.y -= spieler.geschwindigkeit
        spieler.energie -= 0.010
    if tasten[pygame.K_DOWN] and spieler.energie > 0 and len(spieler.abgelegte_objekte) != 5:
        spieler.y += spieler.geschwindigkeit
        spieler.energie -= 0.010

    # Spieler innerhalb der Bildschirmgrenzen halten
    spieler.x = max(0, min(spieler.x, BREITE - SPIELER_GROESSE))
    spieler.y = max(0, min(spieler.y, HÖHE - SPIELER_GROESSE))


# Funktion zur Überprüfung von Kollisionen zwischen Objekten
def kollisionen_prüfen(spieler, energiegeber, objekt, ablageplatz):
    # Rechtecke für Kollisionsprüfungen erstellen
    spieler_rechteck = pygame.Rect(spieler.x, spieler.y, SPIELER_GROESSE, SPIELER_GROESSE)
    energiegeber_rechteck = pygame.Rect(energiegeber.x, energiegeber.y, OBJEKT_GROESSE, OBJEKT_GROESSE)
    objekt_rechteck = pygame.Rect(objekt.x, objekt.y, OBJEKT_GROESSE, OBJEKT_GROESSE)
    ablageplatz_rechteck = pygame.Rect(ablageplatz.x, ablageplatz.y, OBJEKT_GROESSE, OBJEKT_GROESSE)

    # Kollisionen mit den Objekten überprüfen und entsprechende Aktionen ausführen
    if spieler_rechteck.colliderect(energiegeber_rechteck):
        spieler.energie = 100
        energiegeber.x = BREITE - 50
        energiegeber.y = HÖHE - 50

    if spieler_rechteck.colliderect(objekt_rechteck) and spieler.gesammelte_objekte < 5:
        spieler.gesammelte_objekte += 1
        objekt.x = -100

    if spieler_rechteck.colliderect(ablageplatz_rechteck) and spieler.gesammelte_objekte > 0:
        spieler.abgelegte_objekte.append((ablageplatz.x, ablageplatz.y))
        spieler.gesammelte_objekte -= 1
        objekt.x = random.randint(0, BREITE - OBJEKT_GROESSE)
        objekt.y = random.randint(0, HÖHE - OBJEKT_GROESSE)

    spieler.energie = max(0, min(spieler.energie, 100))


# Funktion zum Aktualisieren des Bildschirms
def bildschirm_aktualisieren(spieler, energiegeber, objekt, ablageplatz):
    # Hintergrund zeichnen
    bildschirm.fill(WEISS)

    # Rechtecke für Spieler, Objekte und Ablageplatz zeichnen
    pygame.draw.rect(bildschirm, SCHWARZ, (spieler.x, spieler.y, SPIELER_GROESSE, SPIELER_GROESSE))
    pygame.draw.rect(bildschirm, ROT, (energiegeber.x, energiegeber.y, OBJEKT_GROESSE, OBJEKT_GROESSE))
    pygame.draw.rect(bildschirm, GRÜN, (objekt.x, objekt.y, OBJEKT_GROESSE, OBJEKT_GROESSE))
    pygame.draw.rect(bildschirm, BRAUN, (ablageplatz.x, ablageplatz.y, OBJEKT_GROESSE, OBJEKT_GROESSE))  # Ablageplatz zeichnen

    # Abgelegte Objekte des Spielers zeichnen
    for objekt_pos in spieler.abgelegte_objekte:
        pygame.draw.rect(bildschirm, SCHWARZ, (*objekt_pos, OBJEKT_GROESSE, OBJEKT_GROESSE))

    # Balken für die Spielerenergie zeichnen
    energie_balken_breite = spieler.energie * SPIELER_GROESSE / 100
    energie_balken = pygame.Rect(spieler.x, spieler.y - 10, energie_balken_breite, 5)
    pygame.draw.rect(bildschirm, GRÜN, energie_balken)

    # Textinformationen zum Spielstatus anzeigen
    energie_text = schrift.render(f'Energie: {spieler.energie:.2f}', True, SCHWARZ)
    bildschirm.blit(energie_text, (10, 10))

    objekte_text = schrift.render(f'Gesammelte Objekte: {spieler.gesammelte_objekte}', True, SCHWARZ)
    bildschirm.blit(objekte_text, (10, 30))

    abgelegte_objekte_text = schrift.render(f'Abgelegte Objekte: {len(spieler.abgelegte_objekte)}/5', True, SCHWARZ)
    bildschirm.blit(abgelegte_objekte_text, (10, 50))


    # Nachricht anzeigen, wenn die Energie leer ist und die E-Taste zum Aufladen gedrückt wird
    if spieler.energie <= 0:
        nachricht_text = schrift.render("Deine Energie ist leer, drücke E um sie wieder aufzuladen", True, SCHWARZ)
        bildschirm.blit(nachricht_text, (BREITE // 2 - 200, HÖHE // 2))


    # Nachricht anzeigen, wenn alle Objekte abgelegt wurden und die R-Taste zum Neustart gedrückt wird
    if len(spieler.abgelegte_objekte) == 5:
        nachricht_text = schrift.render("Glückwunsch, du hast alle Objekte abgelegt! R für restart", True, SCHWARZ)
        bildschirm.blit(nachricht_text, (BREITE // 2 - 200, HÖHE // 2))


# Funktion zum Zurücksetzen des Spiels
def reset_spiel(spieler):
    # Setze den Spieler zurück
    spieler.x = BREITE // 2 - SPIELER_GROESSE // 2
    spieler.y = HÖHE // 2 - SPIELER_GROESSE // 2
    spieler.energie = 100
    spieler.gesammelte_objekte = 0
    spieler.abgelegte_objekte = []


# Hauptspiel starten
hauptspiel()
