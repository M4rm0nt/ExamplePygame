# Importieren der benötigten Module
import random  # Modul für Zufallszahlen
import pygame  # Pygame-Bibliothek für die Spieleentwicklung
import sys  # Modul für Systemfunktionalitäten

# Initialisierung von Pygame
pygame.init()

# Festlegen der Fenstergröße
BREITE, HÖHE = 800, 600

# Definition von Farben
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
BRAUN = (139, 69, 19)
GRÜN = (0, 255, 0)
ROT = (255, 0, 0)
BLAU = (0, 0, 255)

# Initialisierung des Bildschirms
bildschirm = pygame.display.set_mode((BREITE, HÖHE))  # Erstellen des Fensters
pygame.display.set_caption("Rechtecksteuerung")  # Titel des Fensters setzen

# Festlegen der Größe für Spieler und Objekte
SPIELER_GROESSE = 50
OBJEKT_GROESSE = 30

# Festlegen der Textschriftart
schrift = pygame.font.SysFont(None, 24)

# Festlegen der Spielerposition und -eigenschaften
spieler_x = 400  # x-Position des Spielers
spieler_y = 300  # y-Position des Spielers
spieler_geschwindigkeit = 1  # Geschwindigkeit, mit der sich der Spieler bewegt
spieler_energie = 100  # Energie des Spielers
gesammelte_objekte = 0  # Anzahl der vom Spieler gesammelten Objekte
abgelegte_objekte = []  # Liste der abgelegten Objekte des Spielers

# Festlegen der Computerposition und -eigenschaften
computer_start_x = 100  # Start-X-Position des Computers
computer_start_y = 500  # Start-Y-Position des Computers
computer_x = computer_start_x  # x-Position des Computers
computer_y = computer_start_y  # y-Position des Computers
computer_geschwindigkeit = 0.5  # Geschwindigkeit, mit der sich der Computer bewegt
computer_objekt = None  # Objekt, das der Computer gestohlen hat
computer_ablageplatz_x = 100  # Ablage-X-Position des Computers
computer_ablageplatz_y = 500  # Ablage-Y-Position des Computers
computer_abgelegte_objekte = []  # Liste der abgelegten Objekte des Computers

# Festlegen der Anfangspositionen der Spielobjekte
energiegeber_x, energiegeber_y = 700, 500  # Position des Energiegebers
sammel_objekt_x, sammel_objekt_y = 600, 400  # Position des Sammelobjekts
ablageplatz_x, ablageplatz_y = 100, 100  # Position des Ablageplatzes

# Variable zur Verfolgung des Spielstatus
läuft = True  # Solange das Spiel läuft, ist diese Variable True

# Hauptschleife des Spiels
while läuft:
    for ereignis in pygame.event.get():  # Ereignisse abfragen
        if ereignis.type == pygame.QUIT:  # Wenn das Fenster geschlossen wird
            läuft = False  # Spiel beenden

    # Tasteneingaben verarbeiten
    tasten = pygame.key.get_pressed()

    # Spielerbewegungen verarbeiten und Energie abziehen
    if tasten[pygame.K_LEFT] and spieler_energie > 0 and len(abgelegte_objekte) != 5 and len(computer_abgelegte_objekte) != 5:
        spieler_x -= spieler_geschwindigkeit
        spieler_energie -= 0.010
    if tasten[pygame.K_RIGHT] and spieler_energie > 0 and len(abgelegte_objekte) != 5 and len(computer_abgelegte_objekte) != 5:
        spieler_x += spieler_geschwindigkeit
        spieler_energie -= 0.010
    if tasten[pygame.K_UP] and spieler_energie > 0 and len(abgelegte_objekte) != 5 and len(computer_abgelegte_objekte) != 5:
        spieler_y -= spieler_geschwindigkeit
        spieler_energie -= 0.010
    if tasten[pygame.K_DOWN] and spieler_energie > 0 and len(abgelegte_objekte) != 5 and len(computer_abgelegte_objekte) != 5:
        spieler_y += spieler_geschwindigkeit
        spieler_energie -= 0.010

    # Spielerposition einschränken, um innerhalb des Bildschirms zu bleiben
    spieler_x = max(0, min(spieler_x, BREITE - SPIELER_GROESSE))
    spieler_y = max(0, min(spieler_y, HÖHE - SPIELER_GROESSE))

    # Computer folgt dem Spieler oder liefert gestohlene Objekte ab
    if computer_objekt is None:
        if computer_x < spieler_x:
            computer_x += computer_geschwindigkeit
        elif computer_x > spieler_x:
            computer_x -= computer_geschwindigkeit
        if computer_y < spieler_y:
            computer_y += computer_geschwindigkeit
        elif computer_y > spieler_y:
            computer_y -= computer_geschwindigkeit
    else:
        target_x, target_y = computer_ablageplatz_x, computer_ablageplatz_y
        distance = ((computer_x - target_x) ** 2 + (computer_y - target_y) ** 2) ** 0.5
        if distance > 0.1:  # Schwellenwert für die Annäherung
            dx = target_x - computer_x
            dy = target_y - computer_y
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5
            if distance != 0:
                computer_x += computer_geschwindigkeit * (dx / distance)
                computer_y += computer_geschwindigkeit * (dy / distance)
        else:
            computer_abgelegte_objekte.append((computer_ablageplatz_x, computer_ablageplatz_y))
            computer_objekt = None

    # Anpassen der Bewegung des Computers nach dem Ablegen eines Objekts
    if computer_objekt is not None:
        target_x, target_y = computer_ablageplatz_x, computer_ablageplatz_y
        distance = ((computer_x - target_x) ** 2 + (computer_y - target_y) ** 2) ** 0.5
        if distance > 0.1:  # Schwellenwert für die Annäherung
            dx = target_x - computer_x
            dy = target_y - computer_y
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5
            if distance != 0:
                if distance < computer_geschwindigkeit:  # Falls die Entfernung kleiner ist als die Geschwindigkeit
                    computer_x = target_x
                    computer_y = target_y
                else:
                    computer_x += computer_geschwindigkeit * (dx / distance)
                    computer_y += computer_geschwindigkeit * (dy / distance)
        else:
            computer_abgelegte_objekte.append((computer_ablageplatz_x, computer_ablageplatz_y))
            computer_objekt = None
            # Computer nimmt die Verfolgung des Spielers wieder auf
            target_x, target_y = spieler_x, spieler_y

    # Rechtecke für Kollisionsprüfungen erstellen
    spieler_rechteck = pygame.Rect(spieler_x, spieler_y, SPIELER_GROESSE, SPIELER_GROESSE)
    energiegeber_rechteck = pygame.Rect(energiegeber_x, energiegeber_y, OBJEKT_GROESSE, OBJEKT_GROESSE)
    sammel_objekt_rechteck = pygame.Rect(sammel_objekt_x, sammel_objekt_y, OBJEKT_GROESSE, OBJEKT_GROESSE)
    ablageplatz_rechteck = pygame.Rect(ablageplatz_x, ablageplatz_y, OBJEKT_GROESSE, OBJEKT_GROESSE)
    computer_rechteck = pygame.Rect(computer_x, computer_y, SPIELER_GROESSE, SPIELER_GROESSE)
    computer_ablageplatz_rechteck = pygame.Rect(computer_ablageplatz_x, computer_ablageplatz_y, OBJEKT_GROESSE, OBJEKT_GROESSE)

    # Kollisionen mit den Objekten überprüfen und entsprechende Aktionen ausführen
    if spieler_rechteck.colliderect(energiegeber_rechteck):
        spieler_energie = 100

    if spieler_rechteck.colliderect(sammel_objekt_rechteck) and gesammelte_objekte < 5:
        gesammelte_objekte += 1
        sammel_objekt_x = -100

    if spieler_rechteck.colliderect(ablageplatz_rechteck) and gesammelte_objekte > 0:
        abgelegte_objekte.append((ablageplatz_x, ablageplatz_y))
        gesammelte_objekte -= 1
        sammel_objekt_x = random.randint(0, BREITE - OBJEKT_GROESSE)
        sammel_objekt_y = random.randint(0, HÖHE - OBJEKT_GROESSE)

    # Wenn der Computer kein Objekt hat und der Spieler eines hat und sie kollidieren, stiehlt der Computer es
    if computer_objekt is None and gesammelte_objekte > 0 and spieler_rechteck.colliderect(computer_rechteck):
        computer_objekt = (sammel_objekt_x, sammel_objekt_y)
        gesammelte_objekte -= 1
        sammel_objekt_x = random.randint(0, BREITE - OBJEKT_GROESSE)
        sammel_objekt_y = random.randint(0, HÖHE - OBJEKT_GROESSE)

    # Wenn der Computer ein gestohlenes Objekt hat, bringt er es zum Ablageplatz
    if computer_objekt is not None:
        target_x, target_y = computer_ablageplatz_x, computer_ablageplatz_y
        distance = ((computer_x - target_x) ** 2 + (computer_y - target_y) ** 2) ** 0.5
        if distance > 0.1:  # Schwellenwert für die Annäherung
            dx = target_x - computer_x
            dy = target_y - computer_y
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5
            if distance != 0:
                computer_x += computer_geschwindigkeit * (dx / distance)
                computer_y += computer_geschwindigkeit * (dy / distance)
        else:
            computer_abgelegte_objekte.append((computer_ablageplatz_x, computer_ablageplatz_y))
            computer_objekt = None
            # Computer nimmt die Verfolgung des Spielers wieder auf
            if computer_x < spieler_x:
                computer_x += computer_geschwindigkeit
            elif computer_x > spieler_x:
                computer_x -= computer_geschwindigkeit
            if computer_y < spieler_y:
                computer_y += computer_geschwindigkeit
            elif computer_y > spieler_y:
                computer_y -= computer_geschwindigkeit

    # Spielerenergie begrenzen, um sicherzustellen, dass sie zwischen 0 und 100 liegt
    spieler_energie = max(0, min(spieler_energie, 100))

    # Hintergrund zeichnen
    bildschirm.fill(WEISS)

    # Rechtecke für Spieler, Objekte und Ablageplatz zeichnen
    pygame.draw.rect(bildschirm, SCHWARZ, (spieler_x, spieler_y, SPIELER_GROESSE, SPIELER_GROESSE))
    pygame.draw.rect(bildschirm, ROT, (energiegeber_x, energiegeber_y, OBJEKT_GROESSE, OBJEKT_GROESSE))
    pygame.draw.rect(bildschirm, GRÜN, (sammel_objekt_x, sammel_objekt_y, OBJEKT_GROESSE, OBJEKT_GROESSE))
    pygame.draw.rect(bildschirm, BRAUN, (ablageplatz_x, ablageplatz_y, OBJEKT_GROESSE, OBJEKT_GROESSE))
    pygame.draw.rect(bildschirm, BLAU, (computer_x, computer_y, SPIELER_GROESSE, SPIELER_GROESSE))
    pygame.draw.rect(bildschirm, BLAU, (computer_ablageplatz_x, computer_ablageplatz_y, OBJEKT_GROESSE, OBJEKT_GROESSE))

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
    computer_abgelegte_objekte_text = schrift.render(f'Computer Abgelegte Objekte: {len(computer_abgelegte_objekte)}/5', True, SCHWARZ)
    bildschirm.blit(computer_abgelegte_objekte_text, (10, 70))
    gestohlene_objekte_text = schrift.render(f'Gestohlene Objekte: {len(computer_abgelegte_objekte)}', True, SCHWARZ)
    bildschirm.blit(gestohlene_objekte_text, (10, 90))

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
        gestohlene_objekte = []
        computer_objekt = None
        computer_abgelegte_objekte = []

    # Nachricht anzeigen, wenn alle Objekte gestohlen wurden und die R-Taste zum Neustart gedrückt wird
    if len(computer_abgelegte_objekte) == 5:
        nachricht_text = schrift.render("Der Computer hat alle Objekte gestohlen! R für restart", True, SCHWARZ)
        bildschirm.blit(nachricht_text, (200, 300))

    # Spiel zurücksetzen, wenn alle Objekte gestohlen wurden und R gedrückt wird
    if len(computer_abgelegte_objekte) == 5 and tasten[pygame.K_r]:
        spieler_x = 400
        spieler_y = 300
        spieler_energie = 100
        gesammelte_objekte = 0
        abgelegte_objekte = []
        gestohlene_objekte = []
        computer_objekt = None
        computer_abgelegte_objekte = []

    # Anzeigen, welches Objekt der Computer gestohlen hat
    if computer_objekt is not None:
        pygame.draw.rect(bildschirm, BLAU, (*computer_objekt, OBJEKT_GROESSE, OBJEKT_GROESSE))

    # Bildschirm aktualisieren
    pygame.display.flip()

# Pygame beenden
pygame.quit()
sys.exit()
