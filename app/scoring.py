
from datetime import datetime

def score_alineacion_EM(actor, proyecto):
    score = 0
    proyecto_regiones = set(proyecto.get('regiones_objetivo', []))
    actor_regiones = set(actor.get('mercados_objetivo', []))

    intersection = proyecto_regiones & actor_regiones
    if intersection:
        score += min(40, len(intersection) * 15)
    elif 'global EM' in actor_regiones and proyecto_regiones:
        score += 25

    evidencias = actor.get('evidencias', [])
    recent_evidence = 0
    for ev in evidencias:
        try:
            fecha = datetime.strptime(ev['fecha'], '%Y-%m-%d')
            months_old = (datetime.now() - fecha).days / 30
            if months_old <= 24:
                recent_evidence += 1
        except:
            continue

    if recent_evidence >= 2:
        score += 30
    elif recent_evidence == 1:
        score += 20
    else:
        score += 10

    if actor.get('pruebas_alineacion_EM'):
        score += min(30, len(actor['pruebas_alineacion_EM']) * 15)

    return min(100, score)

def score_foco_climatico(actor, proyecto):
    score = 0
    proyecto_temas = set(proyecto.get('temas', []))
    actor_temas = set(actor.get('foco_tematico', []))

    high_impact = {'clima','energía','energía renovable'}
    medium_impact = {'economía circular','resiliencia','agricultura regenerativa'}

    matches = proyecto_temas & actor_temas
    for match in matches:
        if match in high_impact:
            score += 20
        elif match in medium_impact:
            score += 15
        else:
            score += 10

    score = min(50, score)

    impacto_minimo = actor.get('criterios_elegibilidad', {}).get('impacto_minimo', '')
    if 'tCO2e' in impacto_minimo:
        try:
            tons = int(''.join(filter(str.isdigit, impacto_minimo.split('tCO2e')[0])))
            if tons >= 1000:
                score += 30
            elif tons >= 100:
                score += 20
            elif tons >= 50:
                score += 15
        except:
            score += 10

    exclusions = actor.get('criterios_elegibilidad', {}).get('exclusiones', [])
    if exclusions:
        score += min(20, len(exclusions) * 10)

    return min(100, score)

def score_ticket_fase(actor, proyecto):
    score = 0
    proyecto_ticket = proyecto.get('ticket_solicitado', 500000)
    actor_min = actor.get('ticket_min_eur', 0)
    actor_max = actor.get('ticket_max_eur', float('inf'))

    if actor_min <= proyecto_ticket <= actor_max:
        score += 50
    elif proyecto_ticket < actor_min:
        ratio = proyecto_ticket / actor_min
        score += max(0, 50 * ratio - 10)
    elif proyecto_ticket > actor_max:
        ratio = actor_max / proyecto_ticket
        score += max(0, 50 * ratio - 20)

    proyecto_trl = proyecto.get('TRL', 5)
    try:
        actor_trl_min = int(actor.get('criterios_elegibilidad', {}).get('TRL_min', '1'))
    except:
        actor_trl_min = 1

    if proyecto_trl >= actor_trl_min:
        score += 30
    else:
        score += max(0, 30 - (actor_trl_min - proyecto_trl) * 10)

    proyecto_fase = proyecto.get('fase', 'pilot/TRL4-6')
    actor_fases = actor.get('fase', [])
    if proyecto_fase in actor_fases:
        score += 20
    elif any(fase in proyecto_fase for fase in actor_fases):
        score += 10

    return min(100, score)

def score_claridad(actor, proyecto):
    score = 0
    proyecto_instrumentos = set(proyecto.get('instrumentos_preferidos', ['grant']))
    actor_instrumentos = set(actor.get('instrumentos', []))

    if proyecto_instrumentos & actor_instrumentos:
        score += 30
    elif not proyecto_instrumentos:
        score += 20

    if actor.get('contacto_o_call'):
        score += 15
    if actor.get('criterios_elegibilidad'):
        completeness = len([k for k,v in actor['criterios_elegibilidad'].items() if v])
        score += min(10, completeness * 2)

    confiabilidad = actor.get('confiabilidad_fuentes', 0.5)
    score += int(confiabilidad * 25)

    evidencias = actor.get('evidencias', [])
    all_old = True
    for ev in evidencias:
        try:
            fecha = datetime.strptime(ev['fecha'], '%Y-%m-%d')
            months_old = (datetime.now() - fecha).days / 30
            if months_old <= 24:
                all_old = False
                break
        except:
            continue

    if not all_old:
        score += 20
    else:
        score -= 20

    return max(0, min(100, score))

def calculate_final_score(actor, proyecto):
    weights = {'alineacion_EM':0.40,'foco_climatico':0.25,'ticket_fase':0.20,'claridad':0.15}
    scores = {
        'alineacion_EM': score_alineacion_EM(actor, proyecto),
        'foco_climatico': score_foco_climatico(actor, proyecto),
        'ticket_fase': score_ticket_fase(actor, proyecto),
        'claridad': score_claridad(actor, proyecto)
    }
    actor['puntuacion_componentes'] = scores
    final_score = sum(scores[comp] * weights[comp] for comp in weights)
    return round(final_score,1)
