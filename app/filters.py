
def passes_hard_filters(actor, proyecto):
    # Simple filters: temas, regiones, org type, instrumentos
    if proyecto['temas'] and not set(proyecto['temas']) & set(actor.get('foco_tematico', [])):
        return False
    if proyecto['regiones_objetivo'] and not set(proyecto['regiones_objetivo']) & set(actor.get('mercados_objetivo', [])):
        return False
    if proyecto['org_type'] and not set(proyecto['org_type']) & set(actor.get('criterios_elegibilidad', {}).get('tipo_entidad', [])):
        return False
    if proyecto['instrumentos_preferidos'] and not set(proyecto['instrumentos_preferidos']) & set(actor.get('instrumentos', [])):
        return False
    return True
