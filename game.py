import random
import pygame
import sys

# Initialisierung von Pygame
pygame.init()

# Fenstergröße
BREITE, HÖHE = 800, 600

# Farben
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
BRAUN = (139, 69, 19)
GRÜN = (0, 255, 0)
ROT = (255, 0, 0)
BLAU = (0, 0, 255)

# Initialisierung des Bildschirms
bildschirm = pygame.display.set_mode((BREITE, HÖHE))
pygame.display.set_caption("Rechtecksteuerung")

# Spieler- und Objektgrößen
SPIELER_GROESSE = 50
OBJEKT_GROESSE = 30

# Textschriftart
schrift = pygame.font.SysFont(None, 24)

# Spielerposition und Eigenschaften
spieler_x = 400
spieler_y = 300
spieler_geschwindigkeit = 1
spieler_energie = 100
gesammelte_objekte = 0
abgelegte_objekte = []

# Computer-Position und Eigenschaften
computer_x = 100
computer_y = 100
computer_geschwindigkeit = 0.5

# Spielobjekte initialisieren
energiegeber_x, energiegeber_y = 700, 500
sammel_objekt_x, sammel_objekt_y = 600, 400
ablageplatz_x, ablageplatz_y = 100, 100

# Spielstatusvariablen
läuft = True

# Hauptschleife des Spiels
while läuft:
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            läuft = False

    # Tasteneingaben verarbeiten
    tasten = pygame.key.get_pressed()

    # Spielerbewegungen verarbeiten und Energie abziehen
    if tasten[pygame.K_LEFT] and spieler_energie > 0 and len(abgelegte_objekte) != 5:
        spieler_x -= spieler_geschwindigkeit
        spieler_energie -= 0.010
    if tasten[pygame.K_RIGHT] and spieler_energie > 0 and len(abgelegte_objekte) != 5:
        spieler_x += spieler_geschwindigkeit
        spieler_energie -= 0.010
    if tasten[pygame.K_UP] and spieler_energie > 0 and len(abgelegte_objekte) != 5:
        spieler_y -= spieler_geschwindigkeit
        spieler_energie -= 0.010
    if tasten[pygame.K_DOWN] and spieler_energie > 0 and len(abgelegte_objekte) != 5:
        spieler_y += spieler_geschwindigkeit
        spieler_energie -= 0.010

    # Spielerposition einschränken
    spieler_x = max(0, min(spieler_x, BREITE - SPIELER_GROESSE))
    spieler_y = max(0, min(spieler_y, HÖHE - SPIELER_GROESSE))

    # Computer folgt dem Spieler
    if computer_x < spieler_x:
        computer_x += computer_geschwindigkeit
    elif computer_x > spieler_x:
        computer_x -= computer_geschwindigkeit

    if computer_y < spieler_y:
        computer_y += computer_geschwindigkeit
    elif computer_y > spieler_y:
        computer_y -= computer_geschwindigkeit

    # Rechtecke für Kollisionsprüfungen erstellen
    spieler_rechteck = pygame.Rect(spieler_x, spieler_y, SPIELER_GROESSE, SPIELER_GROESSE)
    energiegeber_rechteck = pygame.Rect(energiegeber_x, energiegeber_y, OBJEKT_GROESSE, OBJEKT_GROESSE)
    sammel_objekt_rechteck = pygame.Rect(sammel_objekt_x, sammel_objekt_y, OBJEKT_GROESSE, OBJEKT_GROESSE)
    ablageplatz_rechteck = pygame.Rect(ablageplatz_x, ablageplatz_y, OBJEKT_GROESSE, OBJEKT_GROESSE)
    computer_rechteck = pygame.Rect(computer_x, computer_y, SPIELER_GROESSE, SPIELER_GROESSE)

    # Kollisionen mit den Objekten überprüfen und entsprechende Aktionen ausführen
    if spieler_rechteck.colliderect(energiegeber_rechteck):
        spieler_energie = 100
        energiegeber_x = BREITE - 50
        energiegeber_y = HÖHE - 50

    if spieler_rechteck.colliderect(sammel_objekt_rechteck) and gesammelte_objekte < 5:
        gesammelte_objekte += 1
        sammel_objekt_x = -100

    if spieler_rechteck.colliderect(ablageplatz_rechteck) and gesammelte_objekte > 0:
        abgelegte_objekte.append((ablageplatz_x, ablageplatz_y))
        gesammelte_objekte -= 1
        sammel_objekt_x = random.randint(0, BREITE - OBJEKT_GROESSE)
        sammel_objekt_y = random.randint(0, HÖHE - OBJEKT_GROESSE)

    # Spielerenergie begrenzen
    spieler_energie = max(0, min(spieler_energie, 100))

    # Hintergrund zeichnen
    bildschirm.fill(WEISS)

    # Rechtecke für Spieler, Objekte und Ablageplatz zeichnen
    pygame.draw.rect(bildschirm, SCHWARZ, (spieler_x, spieler_y, SPIELER_GROESSE, SPIELER_GROESSE))
    pygame.draw.rect(bildschirm, ROT, (energiegeber_x, energiegeber_y, OBJEKT_GROESSE, OBJEKT_GROESSE))
    pygame.draw.rect(bildschirm, GRÜN, (sammel_objekt_x, sammel_objekt_y, OBJEKT_GROESSE, OBJEKT_GROESSE))
    pygame.draw.rect(bildschirm, BRAUN, (ablageplatz_x, ablageplatz_y, OBJEKT_GROESSE, OBJEKT_GROESSE))
    pygame.draw.rect(bildschirm, BLAU, (computer_x, computer_y, SPIELER_GROESSE, SPIELER_GROESSE))

    # Abgelegte Objekte des Spielers zeichnen
    for objekt_pos in abgelegte_objekte:
        pygame.draw.rect(bildschirm, SCHWARZ, (*objekt_pos, OBJEKT_GROESSE, OBJEKT_GROESSE))

    # Textinformationen zum Spielstatus anzeigen
    energie_text = schrift.render(f'Energie: {spieler_energie:.2f}', True, SCHWARZ)
    bildschirm.blit(energie_text, (10, 10))

    objekte_text = schrift.render(f'Gesammelte Objekte: {gesammelte_objekte}', True, SCHWARZ)
    bildschirm.blit(objekte_text, (10, 30))

    abgelegte_objekte_text = schrift.render(f'Abgelegte Objekte: {len(abgelegte_objekte)}/5', True, SCHWARZ)
    bildschirm.blit(abgelegte_objekte_text, (10, 50))

    # Nachricht anzeigen, wenn die Energie leer ist und die E-Taste zum Aufladen gedrückt wird
    if spieler_energie <= 0:
        nachricht_text = schrift.render("Deine Energie ist leer, drücke E um sie wieder aufzuladen", True, SCHWARZ)
        bildschirm.blit(nachricht_text, (200, 300))

    # Spiel zurücksetzen, wenn die Energie leer ist und E gedrückt wird
    if spieler_energie <= 0 and tasten[pygame.K_e]:
        spieler_energie = 100
        spieler_x = 400
        spieler_y = 300

    # Nachricht anzeigen, wenn alle Objekte abgelegt wurden und die R-Taste zum Neustart gedrückt wird
    if len(abgelegte_objekte) == 5:
        nachricht_text = schrift.render("Glückwunsch, du hast alle Objekte abgelegt! R für restart", True, SCHWARZ)
        bildschirm.blit(nachricht_text, (200, 300))

    # Spiel zurücksetzen, wenn alle Objekte abgelegt wurden und R gedrückt wird
    if len(abgelegte_objekte) == 5 and tasten[pygame.K_r]:
        spieler_x = 400
        spieler_y = 300
        spieler_energie = 100
        gesammelte_objekte = 0
        abgelegte_objekte = []

    pygame.display.flip()

# Pygame beenden
pygame.quit()
sys.exit()
