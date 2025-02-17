User manual:
- Choose the LPI value (lens per inch), of your foil you baught.
- Choose the exact dimensions of the printed image. Make a test print and measure.
- Choose the PPI value (pixels per inch). The image should also be saved in this PPI later when it is output in another program. The PPI value should also correspond to the DPI value (dots per inch) of the printer you are using.
- Check the information field which values ​​are actually used, as not all combinations are physically possible.
  

A Python project created using ChatGPT. Here is the prompt (english translation):

Properties:
- Vertical or horizontal stripe direction  
- Support for any number of images (PNG, JPG, JPEG, BMP)  
- Freely selectable LPI and PPI values (with LPI value feedback)  
- Calculations depending on the PPI value  

User-friendliness:  
- Clear user interface (UI)  
- Simultaneous addition of multiple images  
- Only numerical inputs allowed (automatic validation)  
- Automatic conversion between cm and inches as well as recalculation of parameters  
- Feedback and error messages directly in the main window (no pop-ups)  

UI structure (resizable window):  

1. Image management:  
- `self.geometry("340x470")`  
- `self.minsize(200, 200)`  
- Top: "Add images" button, next to it "Remove image" button.  
- Below: Scrollable list of image names for added image paths (only file names left-aligned) and image dimensions in pixels (right-aligned, visually above the image name) in a 75% to 25% ratio.  
- The text "optional" before image height or width should be managed as a separate text element in the code.  
- Image name list starts with 5 rows (never smaller than 3) and dynamically adjusts in width and height according to window size.  

2. Parameter settings:  
- Directly below the image list: Selection of stripe direction "vertical" (default) or "horizontal".  
- One row below: Input field for the LPI value (default: 100).  
One row below:  
- Row for image width: Two input fields – one for cm (default: empty) and one for inches (default: 1).  
- Next row for image height: Two input fields – cm (default: empty) and inches (default: empty).  
- Below: Input field for "Pixels per inch" (PPI, default: 600).  

3. Info area:  
- Below appears an info area displaying calculated values and (if necessary) error messages (initially 9 empty lines).  
- Only one error message (in red) is displayed at a time.  
- Displayed in the following order: Number of images, final image width (px), final image height (px), true image width (inch), "true image height (inch)", stretching (active/hidden), stripe width (px), and the "true LPI value".  

Generation:  
- Always at the bottom of the window is the "Generate image" button (visually at a higher level than other elements when resizing the window).  

Internal program flow, structured by process:  
- "Optional" text hint appears before "image width" in horizontal stripe direction, before "image height" in vertical stripe direction.  
- Note: All mentioned input fields must have a value greater than zero; otherwise, an error message is displayed.  
- Only numbers and at most one dot or comma are allowed in all input fields; a comma is automatically converted to a dot.  
- Conversion from cm to inches occurs with each new number input.  
- If a new value is entered in the "inch" input field, the corresponding "cm" input field is cleared.  
- Information is displayed only when at least two images are present.  
- Only if vertical is active = "Image width (inch) must not be empty".  
- Only if horizontal is active = "Image height (inch) must not be empty".  
- Inputs (changes to image count, values, stripe direction) initially clear the current error message.  

Calculations (if no error messages are present):  
1. `(PPI / (Number of images * LPI))` rounded but at least 1 = Stripe width  
2. `PPI / (Number of images * Stripe width) = True LPI value`  

For "vertical" stripe direction:  
3. `(PPI * Image width (inch))` rounded = Final image width px  
5. `Final image width px / PPI = True image width (inch)`  
6. `(Final image width px / Number of images)` rounded up = Q-value  
7. If image height is empty: `Final image height px (rounded) = (Final image width px * Image height px from first image in list) / Image width px from first image`  
8. If height is set (= stretching active): `Final image height px (rounded) = (Final image width px * Image height (inch)) / Image width (inch)`  
10. `True image height (inch) = Final image height px (rounded) / PPI`  

For "horizontal" stripe direction:  
3. `(PPI * Image height (inch))` rounded = Final image height px  
5. `Final image height px / PPI = True image height (inch)`  
6. `(Final image height px / Number of images)` rounded up = Y-value  
7. If image width is empty: `Final image width px (rounded) = (Final image height px * Image width px from first image in list) / Image height px from first image`  
8. If width is set (= stretching active): `Final image width px (rounded) = (Final image height px * Image width (inch)) / Image height (inch)`  
10. `True image width (inch) = Final image width px (rounded) / PPI`  

Image generation process (after pressing the "Generate image" button), structured by process:  
1. Storage location is selected.  
2. Images are loaded into the program.  

For "vertical" stripe direction:  
3. All images are distorted to the dimensions Q-value to final image height.  
4. All images are cut into strips (value: stripe width), arranged alternately from left to right, and assembled into an image until final image width is reached. The strips should be taken alternately from each image, without skipping strips in the images.  

For "horizontal" stripe direction:  
3. All images are distorted to the dimensions final image width to Y-value.  
4. All images are cut into strips (value: stripe width), arranged alternately from top to bottom, and assembled into an image until final image height is reached. The strips should be taken alternately from each image, without skipping strips in the images.  

5. Saving of the final image.



Benutzerhandbuch:
- Wähle den LPI-Wert (Lens per Inch), den Du von Deiner gekauften Folie erhältst.
- Wähle die genauen Maße des ausgedruckten Bildes. Mache einen Probedruck und messe nach.
- Wähle den PPI-Wert (Pixel per Inch). Das Bild sollte später auch in diesem PPI gespeichert werden, wenn es in einem anderen Programm ausgegeben wird. Der PPI-Wert sollte auch dem DPI-Wert (Dots per Inch) des von Dir verwendeten Druckers entsprechen.
- Prüfe im Infofeld, welche Werte tatsächlich verwendet werden, da nicht alle Kombinationen physikalisch möglich sind.

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
- self.geometry("340x470")
- self.minsize(200, 200)
- Oben: „Bilder hinzufügen“-Button, daneben „Bild entfernen“-Button.
- Darunter: Scrollbare Bildnamenliste der hinzugefügten Bilderpfade (nur Dateinamen linksbündig) und Bildabmessungen in Pixeln (rechtsbündig, visuell über den Bildnamen), im Verhältnis 75% zu 25%.
- Der Text „optional“, vor Bildhöhe oder Bildbreite, sollte als eigenständiger Text im Code verwaltet werden
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
- Nachdem erneute eingaben vom user in "inch" Eingabefeld, sollen "eingaben in cm" löschen so das dessen zugehöriges Eingabefeld leer wird.
- Informationen erscheinen erst bei mindestens zwei Bildern
- Nur wenn vertikal aktiv = "Bildbreite (inch) darf nicht leer sein"
- Nur wenn horizontal aktiv = "Bildhöhe (inch) darf nicht leer sein"
- Eingaben (Änderung von: Bildanzahl, Werten, Streifenrichtung) löschen zunächst die Aktelle Fehlermeldung.

Berechnungen (sofern keine Fehlermeldungen vorliegen):
1. (PPI / (Anzahl Bilder * LPI)) gerundet aber mindestens 1 = Streifenbreite
2. PPI / (Anzahl Bilder * Streifenbreite) = "wahrerLPI-Wert"

bei "vertikal" Streifenrichtung:

3. (PPI * Bildbreite (inch)) gerundet  = Bildendbreite px
5. Bildendbreite px / PPI = "wahreBildbreite (inch)"
6. (Bildendbreite px / Anzahl Bilder) aufgerundet = Q-Wert
7. Falls Bildhöhe leer: Bildendhöhe px (gerundet) =  (Bildendbreite px * Bildhöhe px aus Liste erstes Bild) / Bildbreite px erstes Bild
8. Falls Höhe gesetzt (= Streckung aktiv): Bildendhöhe px (gerundet) = (Bildendbreite px * Bildhöhe (inch))/ Bildbreite (inch)
10. wahre Bildhöhe (inch) = Bildendhöhe px (gerundet) / PPI

bei "horizontal" Streifenrichtung:

3. (PPI * Bildhöhe (inch)) gerundet = Bildendhöhe px
5. Bildendhöhe px / PPI = "wahreBildhöhe (inch)"	
6. (Bildendhöhe px / Anzahl Bilder) aufgerundet = Y-Wert
7. Falls Bildbreite leer: Bildendbreite px (gerundet) = (Bildendhöhe px * Bildbreite px aus Liste erstes Bild) / Bildhöhe px erstes Bild
8. Falls Breite gesetzt (= Streckung aktiv): Bildendbreite px (gerundet) = 	(Bildendhöhe px * Bildbreite (inch)) / Bildhöhe (inch)
10. wahre Bildbreite (inch) = Bildendbreite px (gerundet) / PPI

Ablauf der Bildgenerierung (nach Drücken des "Bild generieren"-Buttons), strukturiert nach Ablauf:
1. Speicherort wird gewählt
2. Bilder werden ins Programm geladen

bei "vertikal" Streifenrichtung:

3. Alle Bilder werden auf die Abmessungen Q-wert zu Bildendhöhe verzerrt.
4. Alle Bilder werden in Streifen (wert Streifenbreite) geschnitten (abwechselnde Anordnung von links nach rechts) und zu einem Bild zusammengesetzt, solange bis Bildendbreite ist. Die Streifen sollen von jedem Bild abwechselt genommen werden, ohne Streifen in den Bildern zu überspringen.

bei "horizontal" Streifenrichtung:

3. Alle Bilder werden auf die Abmessungen Bildendbreite zu Y-Wert verzerrt.
4. Alle Bilder werden in Streifen (wert Streifenbreite) geschnitten (abwechselnde Anordnung von oben nach unten) und zu einem Bild zusammengesetzt, solange bis Bildendhöhe erreicht ist. Die Streifen sollen von jedem Bild abwechselt genommen werden, ohne Streifen in den Bildern zu überspringen.

5. Speicherung des finalen Bildes.
