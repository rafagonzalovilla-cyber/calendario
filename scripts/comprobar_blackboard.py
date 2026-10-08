#!/usr/bin/env python3
"""Diagnóstico seguro de acceso a Blackboard y validez del calendario publicado."""
import datetime as dt
import os
import pathlib
import urllib.error
import urllib.request
from urllib.parse import urlparse

BLACKBOARD_URL = "https://ceu.blackboard.com/ultra/courses/_363043_1/document/_4726501_1?view=content&state=view"
ROOT = pathlib.Path(__file__).resolve().parents[1]
calendar = ROOT / "calendario-ceu.ics"
summary = pathlib.Path(os.environ["GITHUB_STEP_SUMMARY"]) if os.getenv("GITHUB_STEP_SUMMARY") else None

def report(message):
    print(message)
    if summary:
        with summary.open("a", encoding="utf-8") as f:
            f.write(message + "\n\n")

def main():
    if not calendar.is_file():
        raise SystemExit("FALTA calendario-ceu.ics")
    data = calendar.read_text(encoding="utf-8-sig")
    count = data.count("BEGIN:VEVENT")
    if "BEGIN:VCALENDAR" not in data or "END:VCALENDAR" not in data or count == 0:
        raise SystemExit("El archivo ICS no parece válido")
    report(f"## Calendario CEU: {count} eventos\nArchivo válido estructuralmente. Esta prueba no equivale a verificar cada evento.")
    request = urllib.request.Request(BLACKBOARD_URL, headers={"User-Agent": "CEU-calendar-checker/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=25) as resp:
            final_url = resp.url
            content_type = resp.headers.get("Content-Type", "")
            body = resp.read(20000)
        looks_like_pdf = body.startswith(b"%PDF")
        login_indicator = any(x in final_url.lower() for x in ("login", "saml", "oauth", "microsoftonline"))
        report(f"### Acceso desde GitHub\nURL final: `{urlparse(final_url).netloc}`  
Tipo: `{content_type}`")
        if looks_like_pdf:
            report("Se ha recibido un PDF, pero aún falta validar su formato y generar eventos. No se modifica el calendario.")
        elif login_indicator or "text/html" in content_type.lower():
            report("**Acceso automático no confirmado:** GitHub recibe HTML o redirección de autenticación, no el PDF. Se necesita una integración autorizada o descarga desde el ordenador.")
        else:
            report("Respuesta recibida, pero no es un PDF directamente interpretable. No se modifica el calendario.")
    except (urllib.error.URLError, TimeoutError) as e:
        report(f"**Acceso a Blackboard no disponible desde GitHub:** {type(e).__name__}. El calendario permanece intacto.")
    report(f"Última ejecución UTC: {dt.datetime.now(dt.timezone.utc).isoformat()}")
if __name__ == "__main__":
    main()
