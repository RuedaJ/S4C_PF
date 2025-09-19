
def why_fit(actor, proyecto):
    temas = set(proyecto.get('temas', [])) & set(actor.get('foco_tematico', []))
    regiones = set(proyecto.get('regiones_objetivo', [])) & set(actor.get('mercados_objetivo', []))
    ticket = proyecto.get('ticket_solicitado', 0)
    actor_min, actor_max = actor.get('ticket_min_eur',0), actor.get('ticket_max_eur',0)
    frases = []
    if temas:
        frases.append(f"Alineación temática en {', '.join(temas)}")
    if regiones:
        frases.append(f"Presencia en {', '.join(regiones)}")
    if actor_min <= ticket <= actor_max:
        frases.append("Ticket dentro del rango permitido")
    return "; ".join(frases) or "Coincidencia parcial"
