
# Buscador de Financiación Climática (MVP)

Este MVP conecta proyectos de sostenibilidad con fondos europeos que trabajan en mercados emergentes.

## Ejecutar localmente
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Estructura
- app/: lógica y frontend Streamlit
- data/: dataset de actores (JSON)
- tests/: pruebas unitarias
