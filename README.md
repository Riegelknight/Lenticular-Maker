----!!!!!---- currently there is an image processing error when selecting the horizontal stripe direction ----!!!!!!-----

A Python project created using ChatGPT. Here is the prompt (english translation):

Properties:
- Vertical or horizontal stripe direction
- Support for any number of images (as PNG, JPG, JPEG, BMP)
- Freely selectable LPI and PPI values (with LPI value feedback)
- Calculations based on the PPI value

User-friendliness:
- Clear user interface (UI)
- Ability to add multiple images at the same time
- Only numeric inputs allowed (automatic validation)
- Automatic conversion between cm and inch as well as recalculation of the parameters
- Feedback and error messages displayed directly in the main window (no pop-ups)

UI structure (resizable window):
1. Image management:
   - At the top: "Add Images" button, next to it the "Remove Image" button.
   - Below: A scrollable list of image names from the added image paths (file names only, left-aligned) and image dimensions in pixels (right-aligned, displayed above the file name).
   - The image name list starts with 5 rows (never fewer than 3) and adjusts dynamically in width and height proportionally with the window size.
2. Parameter settings:
   - Directly below the image list: selection of stripe direction "vertical" (default) or "horizontal".
   - One row below: input field for the LPI value (default: 100).
   - One row further down:
     - Row for image width: two input fields – one for cm (default: empty) and one for inch (default: 1).
     - Next row for image height: two input fields – one for cm (default: empty) and one for inch (default: empty).
   - Below that: input field for "Pixels per inch" (PPI, default: 600).
3. Info area:
   - Below, an info area appears that displays calculated values and (if necessary) error messages (initially 9 rows are empty).
   - Only one error message is shown at a time (in red).
   - The displayed information, in order, is: number of images, image width (px), image height (px), true image width (inch), "true image height (inch)", stretching (active/hidden), stripe width (px) and the "true LPI value".

Generation:
- Always at the very bottom at the edge of the window is the "Generate Image" button (visually positioned above other elements when resizing the window).

Internal program flow, structured by process:
- An "Optional" text hint appears with horizontal stripe direction before "Image Width" and with vertical before "Image Height".
- Note: In all specified input fields the entered value must be greater than zero; otherwise, an error message is displayed.
- In all input fields only numbers and at most one dot or comma are allowed; any entered comma is automatically converted into a dot.
- Conversion from cm to inch occurs with every new numeric input.
- After further user inputs in the "inch" input field, any entries in the cm field should be cleared so that its corresponding input field is empty.
- Information is displayed only when there are at least two images.
- Only when vertical is active: "Image width (inch) must not be empty."
- Only when horizontal is active: "Image height (inch) must not be empty."
- Any input changes (number of images, values, stripe direction) initially clear the current error message.

Calculations (provided no error messages are present):
1. (PPI / (number of images * LPI)) rounded but at least 1 = stripe width
2. PPI / (number of images * stripe width) = "true LPI value"

For vertical stripe direction:

3. (PPI * image width (inch)) rounded = image width in px
4. image width in px / PPI = "true image width (inch)"
5. (image width in px / number of images) rounded up = Q value
6. If image height is empty: image height in px (rounded) = (image width in px * image height in px from the first image) / image width in px of the first image
7. If height is set (i.e. stretching active): image height in px (rounded) = (image width in px * image height (inch)) / image width (inch)
8. K value = image height in px (rounded)
9. true image height (inch) = image height in px (rounded) / PPI

For horizontal stripe direction:

3. (PPI * image height (inch)) rounded = image height in px
4. image height in px / PPI = "true image height (inch)"
5. (image height in px / number of images) rounded up = Q value
6. If image width is empty: image width in px (rounded) = (image height in px * image width in px from the first image) / image height in px of the first image
7. If width is set (i.e. stretching active): image width in px (rounded) = (image height in px * image width (inch)) / image height (inch)
8. K value = image width in px (rounded)
9. true image width (inch) = image width in px (rounded) / PPI

Process of image generation (after pressing the "Generate Image" button), structured by sequence:
1. Choose the storage location.
2. Load the images into the program.
3. If "horizontal" is selected, rotate all images by 90°.
4. Distort all images: adjust their width to the Q value and their height to the K value.
5. Cut the images into stripes (alternating arrangement from left to right) and assemble them into one image until the target image width in px is reached. The stripes should be taken alternately from each image without skipping any stripes.
6. If "horizontal" is active, rotate the final image back by 90°.
7. Save the final image.


Ein mit ChatGPT erstelltes Python-Projekt. Hier der Orginale prompt:

Eigenschaften:
- Vertikale oder horizontale Streifenrichtung
- Unterstützung beliebig vieler Bilder (als PNG, JPG, JPEG, BMP)
- Frei wählbare LPI- und PPI-Werte (mit LPI-Wert-Feedback)
- Berechnungen in Abhängigkeit vom PPI-Wert

Benutzerfreundlichkeit:
- Übersichtliche Benutzeroberfläche (UI)
- Gleichzeitiges Hinzufügen mehrerer Bilder
- Nur numerische Eingaben möglich (automatische Validierung)
- Automatische Umrechnung zwischen cm und inch sowie Neuberechnung der Parameter
- Feedback und Fehlermeldungen direkt im Hauptfenster (keine Pop-ups)

UI-Aufbau (resizable window):
1. Bildverwaltung:
- Oben: „Bilder hinzufügen“-Button, daneben „Bild entfernen“-Button.
- Darunter: Scrollbare Bildnamenliste der hinzugefügten Bilderpfade (nur Dateinamen linksbündig) und Bildabmessungen in Pixeln (rechtsbündig, visuell über den Bildnamen.).
- Bildnamenliste, startet mit 5 Zeilen (wird nie kleiner 3) und ändert sich dynamisch mit den Fensterabmessungen in der Breite und in der Höhe proportional.
2. Parameter-Einstellungen:
- Direkt unter der Bilderliste: Auswahl der Streifenrichtung „vertikal“ (Standard) oder „horizontal“.
- Eine Zeile darunter: Eingabefeld für den LPI-Wert (Standard: 100).
Eine Zeile darunter:
- Zeile für Bildbreite: Zwei Eingabefelder – eines für cm (Standard: leer) und eines für inch (Standard: 1).
- Nächste Zeile für Bildhöhe: Zwei Eingabefelder – cm (Standard: leer) und inch (Standard: leer).
 - Darunter: Eingabefeld für „Pixel per inch“ (PPI, Standard: 600).

3. Infobereich:
- Darunter erscheint ein Infobereich, der berechnete Werte und (falls nötig) Fehlermeldungen anzeigt (initial 9 Zeilen leer).
- Es wird immer nur eine Fehlermeldung (in roter Farbe) angezeigt.
- Angezeigt werden in dieser Reihenfolge: Anzahl der Bilder, Bildendbreite (px), Bildendhöhe (px), wahre Bildbreite (inch), "wahreBildhöhe (inch)", Streckung (aktiv/ ausgeblendet), Streifenbreite (px) und der "wahrerLPI-Wert".

Generierung:
- Immer ganz unten zum Fensterrand, befindet sich der „Bild generieren“-Button (visuell auf einer höheren ebene als andere Elemente, beim resizen des windows).

Interner Programmablauf, strukturiert nach Ablauf:
-"Optional"-Texthinweis erscheint bei horizontaler Streifenrichtung vor "Bildbreite", bei vertikaler vor "Bildhöhe"
- Hinweis: In allen genannten Eingabefeldern muss der eingegebene Wert größer null sein; sonst wird eine Fehlermeldung ausgegeben.
- In allen Eingabefeldern sind nur Zahlen sowie maximal ein Punkt oder Komma zulässig; ein eingegebenes Komma wird automatisch in einen Punkt umgewandelt.
- Umrechnung von cm in inch erfolgt mit jeder neuen Zahleneingabe
- Aachdem erneute eingaben vom user in "inch" Eingabefeld, sollen "eingaben in cm" löschen so das dessen zugehöriges Eingabefeld leer wird.
- Informationen erscheinen erst bei mindestens zwei Bildern
- Nur wenn vertikal aktiv = "Bildbreite (inch) darf nicht leer sein"
- Nur wenn horizontal aktiv = "Bildhöhe (inch) darf nicht leer sein"
- Eingaben (Änderung von: Bildanzahl, Werten, Streifenrichtung) löschen zunächst die Aktelle Fehlermeldung.

Berechnungen (sofern keine Fehlermeldungen vorliegen):
1. (PPI / (Anzahl Bilder * LPI)) gerundet aber mindestens 1 = Streifenbreite
2. PPI / (Anzahl Bilder * Streifenbreite) = "wahrerLPI-Wert"

bei Vertikale Streifenrichtung:

3. (PPI * Bildbreite (inch)) gerundet  = Bildendbreite px
4. Bildendbreite px / PPI = "wahreBildbreite (inch)"
5. (Bildendbreite px / Anzahl Bilder) aufgerundet = Q-Wert
6. Falls Bildhöhe leer: Bildendhöhe px (gerundet) =  (Bildendbreite px * Bildhöhe px aus Liste erstes Bild) / Bildbreite px erstes Bild
7. Falls Höhe gesetzt (= Streckung aktiv): Bildendhöhe px (gerundet) = (Bildendbreite px * Bildhöhe (inch))/ Bildbreite (inch)
8. K-Wert = Bildendhöhe px (gerundet)
9. wahre Bildhöhe (inch) = Bildendhöhe px (gerundet) / PPI

bei Horizontale Streifenrichtung:

3. (PPI * Bildhöhe (inch)) gerundet = Bildendhöhe px
4. Bildendhöhe px / PPI = "wahreBildhöhe (inch)"
5. (Bildendhöhe px / Anzahl Bilder) aufgerundet = Q-Wert
6. Falls Bildbreite leer: Bildendbreite px (gerundet) = (Bildendhöhe px * Bildbreite px aus Liste erstes Bild) / Bildhöhe px erstes Bild
7. Falls Breite gesetzt (= Streckung aktiv): Bildendbreite px 	(gerundet) = 	(Bildendhöhe px * Bildbreite (inch)) / Bildhöhe (inch)
8. K-Wert = Bildendbreite px (gerundet)	
9. wahre Bildbreite (inch) = Bildendbreite px (gerundet) / PPI

Ablauf der Bildgenerierung (nach Drücken des "Bild generieren"-Buttons), strukturiert nach Ablauf:
1. Speicherort wird gewählt
2. Bilder werden ins Programm geladen
3. Falls "horizontal" gewählt, werden alle Bilder um 90° gedreht
4. Alle Bilder werden in ihrer breite auf Q-Wert und in ihrer Höhe auf den K-Wert verzerrt.
5. Bilder werden in Streifen geschnitten (abwechselnde Anordnung von links nach rechts) und zu einem Bild zusammengesetzt, solange bis die Bildendbreite px erreicht ist. Die Streifen sollen von jedem Bild abwechselt genommen werden, ohne Streifen in den Bildern zu überspringen.
6. Falls "horizontal" aktiv, wird das Bild um 90° zurückgedreht.
7. Speicherung des finalen Bildes.
