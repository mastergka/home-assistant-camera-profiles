# Camera Profiles for Home Assistant

Globale, dauerhaft gespeicherte Kameraauswahl-Profile für Home Assistant.

## Funktionen

- aktuelle `input_boolean.kamera_anzeigen_*`-Auswahl unter frei wählbarem Namen speichern
- Profile über `select.kameraprofil` auswählen und anwenden
- Profile laden und löschen
- unbegrenzte Speicherung in Home Assistants `.storage`
- gemeinsame Nutzung in mehreren Dashboards und durch alle Benutzer

## Installation

Dieses Repository in HACS als benutzerdefiniertes Repository der Kategorie **Integration** hinzufügen. Danach **Camera Profiles** herunterladen, Home Assistant neu starten und unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** einrichten.

## Entitäten

- `select.kameraprofil`
- `text.neues_kameraprofil`
- `button.kameraprofil_speichern`
- `button.kameraprofil_laden`
- `button.kameraprofil_loschen`

