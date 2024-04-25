import random
import pygame
import sys

# Initialisierung von Pygame
# Das musst du in deinem Code haben damit du Pygame verwenden kannst
pygame.init()

# Fenstergröße
# Das ist die Größe des Fensters, das geöffnet wird, wenn das Spiel gestartet wird
BREITE, HÖHE = 800, 600

# Farben
# Das sind die Farben, die im Spiel verwendet werden
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
BRAUN = (139, 69, 19)
GRÜN = (0, 255, 0)
ROT = (255, 0, 0)

# Initialisierung des Bildschirms
# Hier wird das Fenster erstellt, in dem das Spiel angezeigt wird
bildschirm = pygame.display.set_mode((BREITE, HÖHE))
pygame.display.set_caption("Rechtecksteuerung")

# Spieler- und Objektgrößen
# Das sind die Größen der Rechtecke, die im Spiel verwendet werden
SPIELER_GROESSE = 50
OBJEKT_GROESSE = 30

# Textschriftart
# Das ist die Schriftart, die im Spiel verwendet wird
schrift = pygame.font.SysFont(None, 24)

# Spielerposition und Eigenschaften
# Das sind die Startposition und Eigenschaften des Spielers
spieler_x = BREITE // 2 - SPIELER_GROESSE // 2
spieler_y = HÖHE // 2 - SPIELER_GROESSE // 2
spieler_geschwindigkeit = 1
spieler_energie = 100
gesammelte_objekte = 0
abgelegte_objekte = []

# Spielobjekte initialisieren
# Das sind die Startpositionen der Spielobjekte
energiegeber_x, energiegeber_y = BREITE - 50, HÖHE - 50
sammel_objekt_x, sammel_objekt_y = BREITE - 200, HÖHE - 200
ablageplatz_x, ablageplatz_y = 100, 100

# Spielstatusvariablen
# Das sind die Variablen, die den Spielstatus speichern
läuft = True
spiel_gewonnen = False

# Hauptschleife des Spiels
# Das ist die Hauptschleife des Spiels, die das Spiel steuert
while läuft:
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            läuft = False

    # Tasteneingaben verarbeiten
    # Hier werden die Tasteneingaben des Spielers verarbeitet
    tasten = pygame.key.get_pressed()

    # Spielerbewegungen verarbeiten und Energie abziehen
    # Hier wird die Bewegung des Spielers verarbeitet und die Energie abgezogen
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
    # Hier wird die Position des Spielers eingeschränkt, damit er nicht aus dem Bildschirm läuft
    spieler_x = max(0, min(spieler_x, BREITE - SPIELER_GROESSE))
    spieler_y = max(0, min(spieler_y, HÖHE - SPIELER_GROESSE))

    # Rechtecke für Kollisionsprüfungen erstellen
    # Das brauchst du um zu überprüfen ob sich die Rechtecke berühren
    spieler_rechteck = pygame.Rect(spieler_x, spieler_y, SPIELER_GROESSE, SPIELER_GROESSE)
    energiegeber_rechteck = pygame.Rect(energiegeber_x, energiegeber_y, OBJEKT_GROESSE, OBJEKT_GROESSE)
    sammel_objekt_rechteck = pygame.Rect(sammel_objekt_x, sammel_objekt_y, OBJEKT_GROESSE, OBJEKT_GROESSE)
    ablageplatz_rechteck = pygame.Rect(ablageplatz_x, ablageplatz_y, OBJEKT_GROESSE, OBJEKT_GROESSE)

    # Kollisionen mit den Objekten überprüfen und entsprechende Aktionen ausführen
    # Hier wird überprüft ob sich die Rechtecke berühren und entsprechende Aktionen ausgeführt
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
    # Hier wird die Spielerenergie begrenzt, damit sie nicht über 100 oder unter 0 fällt
    spieler_energie = max(0, min(spieler_energie, 100))

    # Hintergrund zeichnen
    # Hier wird der Hintergrund des Spiels gezeichnet
    bildschirm.fill(WEISS)

    # Rechtecke für Spieler, Objekte und Ablageplatz zeichnen
    # Hier werden die Rechtecke für den Spieler, die Objekte und den Ablageplatz gezeichnet
    pygame.draw.rect(bildschirm, SCHWARZ, (spieler_x, spieler_y, SPIELER_GROESSE, SPIELER_GROESSE))
    pygame.draw.rect(bildschirm, ROT, (energiegeber_x, energiegeber_y, OBJEKT_GROESSE, OBJEKT_GROESSE))
    pygame.draw.rect(bildschirm, GRÜN, (sammel_objekt_x, sammel_objekt_y, OBJEKT_GROESSE, OBJEKT_GROESSE))
    pygame.draw.rect(bildschirm, BRAUN, (ablageplatz_x, ablageplatz_y, OBJEKT_GROESSE, OBJEKT_GROESSE))

    # Abgelegte Objekte des Spielers zeichnen
    # Hier werden die abgelegten Objekte des Spielers gezeichnet
    for objekt_pos in abgelegte_objekte:
        pygame.draw.rect(bildschirm, SCHWARZ, (*objekt_pos, OBJEKT_GROESSE, OBJEKT_GROESSE))

    # Balken für die Spielerenergie zeichnen
    # Hier wird der Balken für die Spielerenergie gezeichnet
    energie_balken_breite = spieler_energie * SPIELER_GROESSE / 100
    energie_balken = pygame.Rect(spieler_x, spieler_y - 10, energie_balken_breite, 5)
    pygame.draw.rect(bildschirm, GRÜN, energie_balken)

    # Textinformationen zum Spielstatus anzeigen
    # Hier werden die Textinformationen zum Spielstatus angezeigt
    energie_text = schrift.render(f'Energie: {spieler_energie:.2f}', True, SCHWARZ)
    bildschirm.blit(energie_text, (10, 10))

    objekte_text = schrift.render(f'Gesammelte Objekte: {gesammelte_objekte}', True, SCHWARZ)
    bildschirm.blit(objekte_text, (10, 30))

    abgelegte_objekte_text = schrift.render(f'Abgelegte Objekte: {len(abgelegte_objekte)}/5', True, SCHWARZ)
    bildschirm.blit(abgelegte_objekte_text, (10, 50))

    # Nachricht anzeigen, wenn die Energie leer ist und die E-Taste zum Aufladen gedrückt wird
    # Hier wird eine Nachricht angezeigt, wenn die Energie leer ist und die E-Taste zum Aufladen gedrückt wird
    if spieler_energie <= 0:
        nachricht_text = schrift.render("Deine Energie ist leer, drücke E um sie wieder aufzuladen", True, SCHWARZ)
        bildschirm.blit(nachricht_text, (BREITE // 2 - 200, HÖHE // 2))

    # Nachricht anzeigen, wenn alle Objekte abgelegt wurden und die R-Taste zum Neustart gedrückt wird
    # Hier wird eine Nachricht angezeigt, wenn alle Objekte abgelegt wurden und die R-Taste zum Neustart gedrückt wird
    if len(abgelegte_objekte) == 5:
        nachricht_text = schrift.render("Glückwunsch, du hast alle Objekte abgelegt! R für restart", True, SCHWARZ)
        bildschirm.blit(nachricht_text, (BREITE // 2 - 200, HÖHE // 2))

    # display.flip() wird verwendet um die Änderungen auf dem Bildschirm anzuzeigen
    # Das musst du am Ende deiner Schleife haben damit die Änderungen auf dem Bildschirm angezeigt werden
    pygame.display.flip()

    # Spiel zurücksetzen, wenn alle Objekte abgelegt wurden und R gedrückt wird
    # Hier wird das Spiel zurückgesetzt, wenn alle Objekte abgelegt wurden und die R-Taste gedrückt wird
    if len(abgelegte_objekte) == 5 and tasten[pygame.K_r]:
        spieler_x = BREITE // 2 - SPIELER_GROESSE // 2
        spieler_y = HÖHE // 2 - SPIELER_GROESSE // 2
        spieler_energie = 100
        gesammelte_objekte = 0
        abgelegte_objekte = []

# Pygame beenden
pygame.quit()
sys.exit()
