
import pytest
from app import scoring

def test_scoring_basic():
    actor = {
        'mercados_objetivo':['África'],
        'evidencias':[{'fecha':'2024-01-01'}],
        'pruebas_alineacion_EM':['Proyecto'],
        'foco_tematico':['clima'],
        'criterios_elegibilidad':{'TRL_min':'4','impacto_minimo':'100 tCO2e','exclusiones':['armas']},
        'ticket_min_eur':50000,'ticket_max_eur':2000000,'fase':['pilot/TRL4-6'],
        'instrumentos':['grant'],'contacto_o_call':'http://test','confiabilidad_fuentes':0.8
    }
    proyecto = {'regiones_objetivo':['África'],'temas':['clima'],'TRL':5,'ticket_solicitado':100000,'fase':'pilot/TRL4-6','instrumentos_preferidos':['grant']}
    score = scoring.calculate_final_score(actor, proyecto)
    assert 0 <= score <= 100
