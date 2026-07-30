import random
from datetime import datetime

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Reto GuateCome",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


APP_CSS = """
<style>
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(33, 150, 243, .11), transparent 30%),
            radial-gradient(circle at 90% 5%, rgba(0, 200, 150, .10), transparent 28%);
    }
    .block-container {max-width: 1180px; padding-top: 2rem;}
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1f33 0%, #102d46 100%);
    }
    [data-testid="stSidebar"] * {color: #f7fbff;}
    [data-testid="stMetric"] {
        background: rgba(255,255,255,.06);
        border: 1px solid rgba(120,150,180,.22);
        border-radius: 16px;
        padding: 14px 16px;
        box-shadow: 0 8px 24px rgba(10,30,50,.07);
    }
    .hero {
        padding: 2.1rem;
        border-radius: 24px;
        color: white;
        background: linear-gradient(135deg, #0d3a5c 0%, #076b69 100%);
        box-shadow: 0 18px 45px rgba(7, 50, 80, .22);
        margin-bottom: 1.3rem;
    }
    .hero h1 {margin: 0 0 .4rem 0; font-size: 2.35rem;}
    .hero p {font-size: 1.08rem; opacity: .94; margin-bottom: 0;}
    .case-card, .event-card, .result-card {
        border-radius: 18px;
        padding: 1.25rem 1.4rem;
        margin: .5rem 0 1rem 0;
        border: 1px solid rgba(120,150,180,.24);
        background: rgba(255,255,255,.72);
        color: #142b3a;
        box-shadow: 0 8px 26px rgba(10,40,70,.08);
    }
    .event-card {border-left: 6px solid #f39c35;}
    .result-card {border-left: 6px solid #00a884;}
    .role-pill {
        display: inline-block;
        padding: .32rem .72rem;
        border-radius: 999px;
        color: white;
        background: #315f85;
        font-weight: 700;
        font-size: .84rem;
        margin-bottom: .65rem;
    }
    .small-note {font-size: .9rem; opacity: .78;}
    .stButton > button, [data-testid="stFormSubmitButton"] button {
        border-radius: 12px;
        font-weight: 750;
        min-height: 2.8rem;
        transition: transform .15s ease, box-shadow .15s ease;
    }
    .stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(90deg, #087f79, #0a9b83);
        border-color: #087f79;
        color: white;
    }
    .stButton > button:hover, [data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(20,70,100,.16);
    }
</style>
"""
st.markdown(APP_CSS, unsafe_allow_html=True)


PRODUCT_BACKLOG = [
    {"id": "REG", "name": "Registro de usuarios con correo y DPI", "points": 8, "value": 10, "mandatory": True, "type": "Seguridad"},
    {"id": "CAT", "name": "Catálogo de restaurantes por zona", "points": 13, "value": 10, "mandatory": True, "type": "Core"},
    {"id": "CART", "name": "Carrito de compras", "points": 8, "value": 9, "mandatory": True, "type": "Core"},
    {"id": "PAY", "name": "Pago con tarjeta y banco local", "points": 13, "value": 10, "mandatory": True, "type": "Seguridad"},
    {"id": "LOGIN", "name": "Inicio de sesión", "points": 5, "value": 8, "mandatory": False, "type": "Core"},
    {"id": "SEARCH", "name": "Búsqueda de platos", "points": 8, "value": 8, "mandatory": False, "type": "Funcionalidad"},
    {"id": "PROFILE", "name": "Perfil del usuario", "points": 5, "value": 5, "mandatory": False, "type": "Funcionalidad"},
    {"id": "RATING", "name": "Calificaciones y reseñas", "points": 8, "value": 6, "mandatory": False, "type": "Marketing"},
    {"id": "WA", "name": "Notificaciones por WhatsApp", "points": 8, "value": 7, "mandatory": False, "type": "Marketing"},
    {"id": "RESET", "name": "Recuperación de contraseña", "points": 5, "value": 6, "mandatory": False, "type": "Seguridad"},
    {"id": "ADMIN", "name": "Panel para restaurantes", "points": 13, "value": 7, "mandatory": False, "type": "Administración"},
    {"id": "TRACK", "name": "Seguimiento del pedido", "points": 13, "value": 9, "mandatory": False, "type": "Core"},
]


EVENTS = [
    {
        "title": "Deuda técnica inesperada",
        "icon": "🔥",
        "description": "Un módulo provisional está causando errores intermitentes en el carrito.",
        "role": "Development Team",
        "tags": ["technical_debt", "junior"],
        "choices": [
            {
                "text": "Refactorizar el módulo ahora",
                "reason": "El equipo corrige la raíz del problema, aunque pierde capacidad inmediata.",
                "effects": {"capacity": -4, "morale": 2, "debt": -4, "budget": -6000},
            },
            {
                "text": "Aplicar un parche rápido",
                "reason": "El sprint avanza, pero la solución temporal deja trabajo pendiente.",
                "effects": {"capacity": -1, "morale": -1, "debt": 5, "budget": -1500},
            },
            {
                "text": "Ignorar el error hasta el siguiente sprint",
                "reason": "El equipo conserva tiempo hoy, pero aumenta el riesgo y la frustración.",
                "effects": {"capacity": 1, "morale": -4, "debt": 8, "budget": 0},
            },
        ],
    },
    {
        "title": "Cambio urgente solicitado por Marketing",
        "icon": "📣",
        "description": "Marketing pide una landing page para una campaña que inicia en dos días.",
        "role": "Product Owner",
        "tags": ["interruption", "communication"],
        "choices": [
            {
                "text": "Proteger el objetivo del sprint",
                "reason": "El equipo mantiene el foco, aunque Marketing deberá esperar.",
                "effects": {"capacity": 0, "morale": 3, "debt": 0, "budget": 0},
            },
            {
                "text": "Negociar una versión mínima",
                "reason": "La negociación satisface parcialmente a Marketing y consume algo de capacidad.",
                "effects": {"capacity": -3, "morale": 0, "debt": 1, "budget": -3000},
            },
            {
                "text": "Aceptar la solicitud completa",
                "reason": "El cambio rompe el foco del sprint y obliga al equipo a trabajar bajo presión.",
                "effects": {"capacity": -7, "morale": -6, "debt": 4, "budget": -9000},
            },
        ],
    },
    {
        "title": "Desarrollador junior bloqueado",
        "icon": "🧑‍💻",
        "description": "Una persona nueva no logra completar una historia crítica.",
        "role": "Development Team",
        "tags": ["junior", "mentoring"],
        "choices": [
            {
                "text": "Hacer pair programming",
                "reason": "La historia avanza y el conocimiento queda compartido.",
                "effects": {"capacity": 2, "morale": 4, "debt": -1, "budget": 0},
            },
            {
                "text": "Reasignar la historia a una persona senior",
                "reason": "La tarea se resuelve, pero se pierde una oportunidad de aprendizaje.",
                "effects": {"capacity": 1, "morale": -2, "debt": 0, "budget": 0},
            },
            {
                "text": "Pedirle que continúe investigando solo",
                "reason": "La autonomía es valiosa, pero el bloqueo dura demasiado.",
                "effects": {"capacity": -3, "morale": -3, "debt": 2, "budget": 0},
            },
        ],
    },
    {
        "title": "Problema con la API de facturación",
        "icon": "🧾",
        "description": "La integración de facturación cambió sin previo aviso.",
        "role": "Scrum Master",
        "tags": ["external", "communication"],
        "choices": [
            {
                "text": "Escalar el bloqueo y reorganizar el trabajo",
                "reason": "El equipo mantiene el flujo mientras se gestiona la dependencia externa.",
                "effects": {"capacity": -1, "morale": 1, "debt": 0, "budget": -1000},
            },
            {
                "text": "Esperar una respuesta sin cambiar el plan",
                "reason": "Varias personas quedan bloqueadas durante buena parte del sprint.",
                "effects": {"capacity": -5, "morale": -3, "debt": 0, "budget": 0},
            },
            {
                "text": "Construir una solución temporal interna",
                "reason": "Se recupera algo de velocidad, pero se crea código que habrá que reemplazar.",
                "effects": {"capacity": -2, "morale": 0, "debt": 5, "budget": -4000},
            },
        ],
    },
    {
        "title": "Falla en las pruebas automatizadas",
        "icon": "🧪",
        "description": "Una actualización provoca resultados inconsistentes en la suite de pruebas.",
        "role": "Development Team",
        "tags": ["testing", "technical_debt"],
        "choices": [
            {
                "text": "Detenerse y estabilizar las pruebas",
                "reason": "Se pierde tiempo hoy, pero se protege la calidad del producto.",
                "effects": {"capacity": -3, "morale": 1, "debt": -3, "budget": -2500},
            },
            {
                "text": "Probar manualmente solo lo crítico",
                "reason": "El equipo entrega, aunque aumenta el riesgo para los siguientes sprints.",
                "effects": {"capacity": -1, "morale": -1, "debt": 4, "budget": -1000},
            },
            {
                "text": "Desactivar las pruebas para avanzar",
                "reason": "La velocidad aparente mejora, pero la deuda técnica crece rápidamente.",
                "effects": {"capacity": 2, "morale": -4, "debt": 9, "budget": 0},
            },
        ],
    },
    {
        "title": "Corte de energía en la oficina",
        "icon": "💡",
        "description": "La oficina se queda sin electricidad durante varias horas.",
        "role": "Scrum Master",
        "tags": ["external", "communication"],
        "choices": [
            {
                "text": "Activar trabajo remoto",
                "reason": "La coordinación cambia, pero el equipo conserva casi toda su capacidad.",
                "effects": {"capacity": -1, "morale": 1, "debt": 0, "budget": 0},
            },
            {
                "text": "Trabajar por turnos con la planta eléctrica",
                "reason": "Los cambios de turno interrumpen el ritmo del equipo.",
                "effects": {"capacity": -4, "morale": -2, "debt": 0, "budget": -2000},
            },
            {
                "text": "Mover al equipo a un espacio alternativo",
                "reason": "La empresa cubre el traslado y el equipo recupera el ritmo.",
                "effects": {"capacity": -2, "morale": 2, "debt": 0, "budget": -5000},
            },
        ],
    },
    {
        "title": "Nueva librería promete acelerar el desarrollo",
        "icon": "✨",
        "description": "El equipo encuentra una librería de código abierto que podría ahorrar varios días.",
        "role": "Development Team",
        "tags": ["innovation", "morale"],
        "choices": [
            {
                "text": "Crear una prueba de concepto primero",
                "reason": "La validación reduce el riesgo y confirma una ganancia moderada.",
                "effects": {"capacity": 3, "morale": 2, "debt": 0, "budget": -1000},
            },
            {
                "text": "Integrarla inmediatamente",
                "reason": "El equipo gana velocidad, pero introduce una dependencia poco conocida.",
                "effects": {"capacity": 6, "morale": 2, "debt": 4, "budget": 0},
            },
            {
                "text": "Descartarla por no ser el estándar",
                "reason": "Se evita el riesgo, aunque se pierde una oportunidad de aprendizaje.",
                "effects": {"capacity": 0, "morale": -2, "debt": 0, "budget": 0},
            },
        ],
    },
    {
        "title": "Conflicto sobre el diseño de la experiencia",
        "icon": "🎨",
        "description": "Diseño propone una interfaz atractiva pero costosa; desarrollo sugiere una versión simple.",
        "role": "Product Owner",
        "tags": ["communication", "interruption"],
        "choices": [
            {
                "text": "Acordar un diseño incremental",
                "reason": "El equipo encuentra un equilibrio entre experiencia y velocidad.",
                "effects": {"capacity": -2, "morale": 2, "debt": 0, "budget": -2500},
            },
            {
                "text": "Exigir el diseño completo",
                "reason": "La experiencia mejora, pero el cambio consume mucha capacidad.",
                "effects": {"capacity": -6, "morale": -3, "debt": 1, "budget": -7000},
            },
            {
                "text": "Usar la versión técnica más simple",
                "reason": "El equipo avanza rápido, pero se posterga trabajo de experiencia de usuario.",
                "effects": {"capacity": 1, "morale": 0, "debt": 3, "budget": 0},
            },
        ],
    },
]


RETROSPECTIVES = {
    "communication": {
        "name": "Mejorar la comunicación",
        "description": "Reduce en 2 puntos los impactos negativos de interrupciones o dependencias externas.",
    },
    "testing": {
        "name": "Automatizar pruebas",
        "description": "Reduce en 3 puntos la deuda generada por eventos técnicos o de pruebas.",
    },
    "mentoring": {
        "name": "Fomentar pair programming",
        "description": "Añade 2 puntos de capacidad ante eventos de mentoring o personas junior.",
    },
    "morale": {
        "name": "Cuidar la salud del equipo",
        "description": "Evita hasta 3 puntos de pérdida de moral en el siguiente sprint.",
    },
    "quality": {
        "name": "Fortalecer la Definition of Done",
        "description": "Reduce 2 puntos de deuda durante el sprint, pero inicia con 1 punto menos de capacidad.",
    },
}


def fresh_state():
    return {
        "screen": "intro",
        "team_name": "",
        "participants": "",
        "sprint": 1,
        "day": 1,
        "backlog": [item.copy() for item in PRODUCT_BACKLOG],
        "completed": [],
        "planned": [],
        "base_capacity": 30,
        "sprint_capacity": 30,
        "last_velocity": 0,
        "delivered_value": 0,
        "delivered_points": 0,
        "morale": 70,
        "debt": 0,
        "budget": 500_000,
        "retro_bonus": None,
        "sprint_events": [],
        "current_result": {},
        "event_log": [],
        "sprint_summaries": [],
        "sprint_outcome": {},
        "game_started_at": datetime.now().isoformat(timespec="seconds"),
    }


def init_game():
    st.session_state.clear()
    for key, value in fresh_state().items():
        st.session_state[key] = value


if "screen" not in st.session_state:
    init_game()


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def format_money(value):
    return f"Q{value:,.0f}"


def current_event():
    if not st.session_state.sprint_events:
        return None
    return st.session_state.sprint_events[st.session_state.day - 1]


def prepare_sprint(planned_stories):
    st.session_state.planned = [story.copy() for story in planned_stories]
    st.session_state.day = 1
    expected = st.session_state.last_velocity or random.randint(27, 33)
    quality_cost = 1 if st.session_state.retro_bonus == "quality" else 0
    st.session_state.base_capacity = max(15, expected - quality_cost)
    st.session_state.sprint_capacity = st.session_state.base_capacity

    event_pool = random.sample(EVENTS, 4)
    event_pool.append(
        {
            "title": "Día de avance estable",
            "icon": "✅",
            "description": "No aparecen bloqueos importantes. El equipo puede concentrarse en el objetivo del sprint.",
            "role": "Equipo Scrum",
            "tags": ["calm"],
            "choices": [],
        }
    )
    random.shuffle(event_pool)
    st.session_state.sprint_events = event_pool


def adjusted_effects(event, choice):
    effects = choice["effects"].copy()
    bonus = st.session_state.retro_bonus
    bonus_note = ""

    if bonus == "communication" and set(event["tags"]) & {"interruption", "external", "communication"}:
        if effects["capacity"] < 0:
            recovered = min(2, abs(effects["capacity"]))
            effects["capacity"] += recovered
            bonus_note = f"La mejora de comunicación recuperó {recovered} puntos de capacidad."
    elif bonus == "testing" and set(event["tags"]) & {"testing", "technical_debt"}:
        if effects["debt"] > 0:
            reduced = min(3, effects["debt"])
            effects["debt"] -= reduced
            bonus_note = f"La automatización evitó {reduced} puntos de deuda técnica."
    elif bonus == "mentoring" and set(event["tags"]) & {"mentoring", "junior"}:
        effects["capacity"] += 2
        bonus_note = "El pair programming añadió 2 puntos de capacidad."
    elif bonus == "morale" and effects["morale"] < 0:
        protected = min(3, abs(effects["morale"]))
        effects["morale"] += protected
        bonus_note = f"Las medidas de bienestar evitaron {protected} puntos de pérdida de moral."

    if bonus == "quality":
        old_debt = effects["debt"]
        effects["debt"] = max(-10, effects["debt"] - 2)
        if old_debt != effects["debt"]:
            bonus_note = (bonus_note + " " if bonus_note else "") + "La Definition of Done redujo 2 puntos de deuda."

    return effects, bonus_note


def log_decision(event, choice_text, reason, effects):
    st.session_state.event_log.append(
        {
            "Equipo": st.session_state.team_name,
            "Participantes": st.session_state.participants,
            "Sprint": st.session_state.sprint,
            "Día": st.session_state.day,
            "Rol": event["role"],
            "Evento": event["title"],
            "Decisión": choice_text,
            "Resultado": reason,
            "Cambio capacidad": effects["capacity"],
            "Cambio moral": effects["morale"],
            "Cambio deuda técnica": effects["debt"],
            "Cambio presupuesto": effects["budget"],
            "Capacidad acumulada": st.session_state.sprint_capacity,
            "Moral acumulada": st.session_state.morale,
            "Deuda acumulada": st.session_state.debt,
            "Presupuesto restante": st.session_state.budget,
        }
    )


def resolve_choice(event, choice):
    effects, bonus_note = adjusted_effects(event, choice)
    st.session_state.sprint_capacity = max(0, st.session_state.sprint_capacity + effects["capacity"])
    st.session_state.morale = clamp(st.session_state.morale + effects["morale"], 0, 100)
    st.session_state.debt = clamp(st.session_state.debt + effects["debt"], 0, 100)
    st.session_state.budget = max(0, st.session_state.budget + effects["budget"])
    st.session_state.current_result = {
        "event": event,
        "choice": choice["text"],
        "reason": choice["reason"],
        "effects": effects,
        "bonus_note": bonus_note,
    }
    log_decision(event, choice["text"], choice["reason"], effects)
    st.session_state.screen = "consequence"


def resolve_calm_day(event):
    effects = {"capacity": 1, "morale": 1, "debt": 0, "budget": 0}
    st.session_state.sprint_capacity += 1
    st.session_state.morale = clamp(st.session_state.morale + 1, 0, 100)
    reason = "El foco sostenido permite recuperar un punto de capacidad y mejora ligeramente la moral."
    st.session_state.current_result = {
        "event": event,
        "choice": "Mantener el foco",
        "reason": reason,
        "effects": effects,
        "bonus_note": "",
    }
    log_decision(event, "Mantener el foco", reason, effects)
    st.session_state.screen = "consequence"


def calculate_review():
    capacity_left = max(0, int(round(st.session_state.sprint_capacity)))
    completed_now = []
    incomplete = []

    for story in st.session_state.planned:
        if story["points"] <= capacity_left:
            completed_now.append(story)
            capacity_left -= story["points"]
        else:
            incomplete.append(story)

    completed_ids = {story["id"] for story in completed_now}
    st.session_state.backlog = [
        story for story in st.session_state.backlog if story["id"] not in completed_ids
    ]
    st.session_state.completed.extend(completed_now)

    points_planned = sum(story["points"] for story in st.session_state.planned)
    points_done = sum(story["points"] for story in completed_now)
    value_done = sum(story["value"] for story in completed_now)
    predictability = round((points_done / points_planned) * 100) if points_planned else 0

    st.session_state.delivered_points += points_done
    st.session_state.delivered_value += value_done
    st.session_state.last_velocity = max(15, min(45, points_done or int(st.session_state.sprint_capacity)))
    outcome = {
        "Sprint": st.session_state.sprint,
        "Puntos planificados": points_planned,
        "Capacidad final": int(round(st.session_state.sprint_capacity)),
        "Puntos completados": points_done,
        "Valor entregado": value_done,
        "Predictibilidad (%)": predictability,
        "Historias completadas": ", ".join(story["name"] for story in completed_now) or "Ninguna",
        "Historias incompletas": ", ".join(story["name"] for story in incomplete) or "Ninguna",
        "Moral": st.session_state.morale,
        "Deuda técnica": st.session_state.debt,
        "Presupuesto restante": st.session_state.budget,
    }
    st.session_state.sprint_outcome = outcome
    st.session_state.sprint_summaries.append(
        {
            "Equipo": st.session_state.team_name,
            "Participantes": st.session_state.participants,
            **outcome,
        }
    )


def go_to_next_day():
    if st.session_state.day >= 5:
        calculate_review()
        st.session_state.screen = "review"
    else:
        st.session_state.day += 1
        st.session_state.screen = "daily"


def sidebar():
    with st.sidebar:
        st.title("🚀 GuateCome")
        if st.session_state.team_name:
            st.caption(f"Equipo: {st.session_state.team_name}")
        st.progress(min(st.session_state.sprint, 5) / 5, text=f"Sprint {min(st.session_state.sprint, 5)} de 5")
        st.metric("💎 Valor entregado", st.session_state.delivered_value)
        st.metric("😊 Moral", f"{st.session_state.morale}/100")
        st.metric("🧱 Deuda técnica", f"{st.session_state.debt}/100")
        st.metric("💰 Presupuesto", format_money(st.session_state.budget))
        if st.session_state.retro_bonus:
            bonus = RETROSPECTIVES[st.session_state.retro_bonus]
            st.success(f"Mejora activa: {bonus['name']}")
        st.divider()
        st.caption("El objetivo no es hacer más trabajo, sino entregar el MVP con alto valor y un equipo sostenible.")


def screen_intro():
    st.markdown(
        """
        <div class="hero">
            <h1>🚀 Reto GuateCome</h1>
            <p>Una simulación Scrum sobre priorización, adaptación y entrega de valor.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="case-card">
            <h3>El caso</h3>
            <p><strong>GuateCome</strong> conectará a consumidores con restaurantes pequeños y de
            barrio que normalmente no aparecen en las grandes plataformas de delivery.</p>
            <p>La empresa recibió <strong>Q500,000</strong> y presentará el producto a inversionistas
            dentro de cinco semanas. El equipo dispone de <strong>5 sprints de 5 días</strong> para
            lanzar un MVP. No será posible construir todo.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("team_form"):
        col1, col2 = st.columns(2)
        team_name = col1.text_input("Nombre del equipo", placeholder="Ej. Los Quetzales Ágiles")
        participants = col2.text_input("Participantes", placeholder="Nombres separados por coma")
        accepted = st.form_submit_button("Aceptar el reto", type="primary", width="stretch")
    if accepted:
        st.session_state.team_name = team_name.strip() or "Equipo GuateCome"
        st.session_state.participants = participants.strip() or "Sin especificar"
        st.session_state.screen = "mission"
        st.rerun()


def screen_mission():
    st.title("🎯 Misión y reglas")
    st.info(
        "Lancen un MVP funcional antes de terminar el quinto sprint. "
        "Prioricen valor sin agotar al equipo ni acumular demasiada deuda técnica."
    )

    st.subheader("El MVP obligatorio")
    mandatory = [story for story in st.session_state.backlog if story["mandatory"]]
    cols = st.columns(4)
    for col, story in zip(cols, mandatory):
        col.metric(story["name"], f"{story['points']} pts", f"Valor {story['value']}")

    st.subheader("Cómo se juega")
    left, middle, right = st.columns(3)
    left.markdown("#### 1. Planning\nOrdenen y seleccionen historias según su valor y capacidad.")
    middle.markdown("#### 2. Sprint\nDurante cinco días tomarán decisiones desde distintos roles.")
    right.markdown("#### 3. Review y Retro\nRevisen lo entregado y elijan una mejora para el siguiente sprint.")

    with st.expander("¿Qué significa cada indicador?"):
        st.markdown(
            """
            - **Valor:** beneficio que recibe el negocio al completar historias.
            - **Moral:** salud y motivación del equipo.
            - **Deuda técnica:** costo futuro provocado por soluciones apresuradas.
            - **Presupuesto:** dinero disponible para responder a las necesidades del proyecto.
            - **Predictibilidad:** porcentaje del compromiso del sprint que realmente se completó.
            """
        )

    st.warning("Las consecuencias no se muestran antes de decidir. Conversen desde la perspectiva del rol indicado.")
    if st.button("Ir al primer Sprint Planning", type="primary", width="stretch"):
        st.session_state.screen = "planning"
        st.rerun()


def screen_planning():
    sprint = st.session_state.sprint
    st.title(f"📝 Sprint {sprint}: Planning")
    guide_capacity = st.session_state.last_velocity or 30
    st.markdown(
        f"""
        <div class="case-card">
            <span class="role-pill">Product Owner + Development Team</span>
            <h3>¿Qué construiremos ahora?</h3>
            <p>Asigne una prioridad y seleccione las historias del sprint.
            La capacidad orientativa es de <strong>{guide_capacity} puntos</strong>.</p>
            <p class="small-note">El Product Owner prioriza valor; el equipo decide cuánto puede completar con calidad.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.backlog:
        st.success("¡El equipo completó todo el Product Backlog antes del quinto sprint!")
        st.write("Ya no quedan historias por planificar. Pueden cerrar la simulación y revisar los resultados.")
        if st.button("Ver resultado final", type="primary", width="stretch"):
            st.session_state.screen = "end"
            st.rerun()
        return

    rows = []
    for index, story in enumerate(st.session_state.backlog, start=1):
        rows.append(
            {
                "Seleccionar": False,
                "Prioridad": index,
                "ID": story["id"],
                "Historia": story["name"],
                "Tipo": story["type"],
                "Obligatoria": "Sí" if story["mandatory"] else "",
                "Puntos": story["points"],
                "Valor": story["value"],
                "Valor/Punto": round(story["value"] / story["points"], 2),
            }
        )

    edited = st.data_editor(
        pd.DataFrame(rows),
        hide_index=True,
        width="stretch",
        disabled=["ID", "Historia", "Tipo", "Obligatoria", "Puntos", "Valor", "Valor/Punto"],
        column_config={
            "Seleccionar": st.column_config.CheckboxColumn("Incluir"),
            "Prioridad": st.column_config.NumberColumn("Prioridad", min_value=1, max_value=len(rows), step=1),
            "Valor/Punto": st.column_config.NumberColumn("Valor/Punto", format="%.2f"),
        },
        key=f"planning_editor_{sprint}",
    )

    selected_rows = edited[edited["Seleccionar"]].sort_values(["Prioridad", "Valor"], ascending=[True, False])
    planned_points = int(selected_rows["Puntos"].sum()) if not selected_rows.empty else 0
    planned_value = int(selected_rows["Valor"].sum()) if not selected_rows.empty else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Puntos seleccionados", planned_points, planned_points - guide_capacity, delta_color="inverse")
    col2.metric("Valor potencial", planned_value)
    risk = "Alto" if planned_points > guide_capacity * 1.2 else "Moderado" if planned_points > guide_capacity else "Controlado"
    col3.metric("Riesgo del compromiso", risk)

    submitted = st.button("Confirmar Sprint Backlog", type="primary", width="stretch")
    if submitted:
        if selected_rows.empty:
            st.error("Seleccionen al menos una historia para iniciar el sprint.")
        else:
            id_map = {story["id"]: story for story in st.session_state.backlog}
            selected = [id_map[row_id] for row_id in selected_rows["ID"].tolist()]
            prepare_sprint(selected)
            st.session_state.event_log.append(
                {
                    "Equipo": st.session_state.team_name,
                    "Participantes": st.session_state.participants,
                    "Sprint": sprint,
                    "Día": 0,
                    "Rol": "Equipo Scrum",
                    "Evento": "Sprint Planning",
                    "Decisión": " | ".join(story["name"] for story in selected),
                    "Resultado": f"Se comprometieron {planned_points} puntos con valor potencial {planned_value}.",
                    "Cambio capacidad": 0,
                    "Cambio moral": 0,
                    "Cambio deuda técnica": 0,
                    "Cambio presupuesto": 0,
                    "Capacidad acumulada": st.session_state.sprint_capacity,
                    "Moral acumulada": st.session_state.morale,
                    "Deuda acumulada": st.session_state.debt,
                    "Presupuesto restante": st.session_state.budget,
                }
            )
            st.session_state.screen = "daily"
            st.rerun()


def screen_daily():
    event = current_event()
    sprint = st.session_state.sprint
    day = st.session_state.day

    st.title(f"🏃 Sprint {sprint} · Día {day} de 5")
    col1, col2, col3 = st.columns(3)
    col1.metric("Capacidad actual", int(round(st.session_state.sprint_capacity)))
    col2.metric("Compromiso", sum(story["points"] for story in st.session_state.planned))
    col3.metric("Progreso temporal", f"{day * 20}%")
    st.progress(day / 5)

    st.markdown(
        f"""
        <div class="event-card">
            <span class="role-pill">{event['role']}</span>
            <h2>{event['icon']} {event['title']}</h2>
            <p>{event['description']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if event["choices"]:
        st.markdown("#### Conversen y elijan una respuesta")
        with st.form(f"decision_{sprint}_{day}"):
            selected_text = st.radio(
                "¿Qué decide el equipo?",
                [choice["text"] for choice in event["choices"]],
                index=None,
            )
            submit = st.form_submit_button("Tomar decisión", type="primary", width="stretch")
        if submit:
            if not selected_text:
                st.error("Seleccionen una alternativa antes de continuar.")
            else:
                choice = next(choice for choice in event["choices"] if choice["text"] == selected_text)
                resolve_choice(event, choice)
                st.rerun()
    else:
        st.success("Aprovechen este día para mantener el foco y revisar el objetivo del sprint.")
        if st.button("Cerrar el Daily Scrum", type="primary", width="stretch"):
            resolve_calm_day(event)
            st.rerun()


def delta_text(label, value, money=False):
    if value == 0:
        return f"{label}: sin cambio"
    prefix = "+" if value > 0 else ""
    shown = format_money(value) if money else f"{prefix}{value}"
    return f"{label}: {shown}"


def screen_consequence():
    result = st.session_state.current_result
    effects = result["effects"]
    event = result["event"]

    st.title("🔎 Resultado de la decisión")
    st.markdown(
        f"""
        <div class="result-card">
            <span class="role-pill">{event['role']}</span>
            <h3>{result['choice']}</h3>
            <p>{result['reason']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(4)
    cols[0].metric("Capacidad", int(round(st.session_state.sprint_capacity)), effects["capacity"])
    cols[1].metric("Moral", st.session_state.morale, effects["morale"])
    cols[2].metric("Deuda técnica", st.session_state.debt, effects["debt"], delta_color="inverse")
    cols[3].metric("Presupuesto", format_money(st.session_state.budget), delta_text("", effects["budget"], True).replace(": ", ""))

    if result["bonus_note"]:
        st.success(f"Mejora de retrospectiva aplicada: {result['bonus_note']}")

    st.info("Pregunta rápida: ¿qué principio de Scrum apoyó o puso en riesgo esta decisión?")
    label = "Ir al Sprint Review" if st.session_state.day >= 5 else "Continuar al siguiente día"
    if st.button(label, type="primary", width="stretch"):
        go_to_next_day()
        st.rerun()


def screen_review():
    outcome = st.session_state.sprint_outcome
    st.title(f"🔄 Sprint {st.session_state.sprint}: Review")
    cols = st.columns(4)
    cols[0].metric("Planificado", outcome["Puntos planificados"])
    cols[1].metric("Completado", outcome["Puntos completados"])
    cols[2].metric("Valor entregado", outcome["Valor entregado"])
    cols[3].metric("Predictibilidad", f"{outcome['Predictibilidad (%)']}%")

    left, right = st.columns(2)
    with left:
        st.success("**Historias completadas**")
        st.write(outcome["Historias completadas"])
    with right:
        if outcome["Historias incompletas"] == "Ninguna":
            st.success("**Historias incompletas:** Ninguna")
        else:
            st.warning("**Regresan al Product Backlog**")
            st.write(outcome["Historias incompletas"])

    if outcome["Predictibilidad (%)"] < 70:
        st.warning("El compromiso fue poco predecible. Consideren seleccionar menos trabajo en el próximo sprint.")
    elif outcome["Predictibilidad (%)"] >= 90:
        st.success("El equipo logró un compromiso altamente predecible.")

    if st.button("Ir a la Retrospectiva", type="primary", width="stretch"):
        st.session_state.screen = "retrospective"
        st.rerun()


def screen_retrospective():
    st.title(f"🙏 Sprint {st.session_state.sprint}: Retrospectiva")
    st.markdown(
        """
        <div class="case-card">
            <span class="role-pill">Scrum Master + Equipo</span>
            <h3>¿Qué mejora tendrá más impacto en el próximo sprint?</h3>
            <p>Revisen lo ocurrido y elijan una sola acción. Esta mejora tendrá un efecto real.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form(f"retro_{st.session_state.sprint}"):
        selected = st.radio(
            "Acción de mejora",
            list(RETROSPECTIVES.keys()),
            format_func=lambda key: f"{RETROSPECTIVES[key]['name']} — {RETROSPECTIVES[key]['description']}",
            index=None,
        )
        submit = st.form_submit_button("Adoptar mejora", type="primary", width="stretch")

    if submit:
        if not selected:
            st.error("Elijan una mejora antes de continuar.")
        else:
            st.session_state.retro_bonus = selected
            st.session_state.event_log.append(
                {
                    "Equipo": st.session_state.team_name,
                    "Participantes": st.session_state.participants,
                    "Sprint": st.session_state.sprint,
                    "Día": 6,
                    "Rol": "Scrum Master",
                    "Evento": "Sprint Retrospective",
                    "Decisión": RETROSPECTIVES[selected]["name"],
                    "Resultado": RETROSPECTIVES[selected]["description"],
                    "Cambio capacidad": 0,
                    "Cambio moral": 0,
                    "Cambio deuda técnica": 0,
                    "Cambio presupuesto": 0,
                    "Capacidad acumulada": st.session_state.sprint_capacity,
                    "Moral acumulada": st.session_state.morale,
                    "Deuda acumulada": st.session_state.debt,
                    "Presupuesto restante": st.session_state.budget,
                }
            )
            if st.session_state.sprint >= 5:
                st.session_state.screen = "end"
            else:
                st.session_state.sprint += 1
                st.session_state.screen = "planning"
            st.rerun()


def final_assessment():
    mandatory_ids = {story["id"] for story in PRODUCT_BACKLOG if story["mandatory"]}
    completed_ids = {story["id"] for story in st.session_state.completed}
    mandatory_complete = mandatory_ids.issubset(completed_ids)
    predictability_values = [row["Predictibilidad (%)"] for row in st.session_state.sprint_summaries]
    avg_predictability = round(sum(predictability_values) / len(predictability_values)) if predictability_values else 0
    score = (
        st.session_state.delivered_value * 8
        + st.session_state.morale
        - st.session_state.debt * 3
        + avg_predictability
        + (100 if mandatory_complete else -100)
    )
    if score >= 650 and mandatory_complete:
        level = "🏆 Agile Champion"
        message = "Entregaron un MVP valioso con buenas decisiones de adaptación."
    elif score >= 430 and mandatory_complete:
        level = "🌟 Equipo Ágil"
        message = "El MVP está listo y el equipo mostró una gestión sólida."
    elif mandatory_complete:
        level = "✅ MVP entregado"
        message = "Cumplieron el objetivo básico, aunque quedan oportunidades claras de mejora."
    else:
        level = "🧭 Equipo en aprendizaje"
        message = "El MVP quedó incompleto. Revisen la priorización y el tamaño de los compromisos."
    return mandatory_complete, avg_predictability, max(0, int(score)), level, message


def csv_bytes(records):
    return pd.DataFrame(records).to_csv(index=False).encode("utf-8-sig")


def screen_end():
    mandatory_complete, avg_predictability, score, level, message = final_assessment()
    if mandatory_complete:
        st.balloons()

    st.markdown(
        f"""
        <div class="hero">
            <h1>{level}</h1>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(5)
    cols[0].metric("Puntuación", score)
    cols[1].metric("Valor", st.session_state.delivered_value)
    cols[2].metric("Predictibilidad", f"{avg_predictability}%")
    cols[3].metric("Moral", st.session_state.morale)
    cols[4].metric("Deuda técnica", st.session_state.debt)

    if mandatory_complete:
        st.success("MVP obligatorio completado.")
    else:
        mandatory_ids = {story["id"] for story in PRODUCT_BACKLOG if story["mandatory"]}
        completed_ids = {story["id"] for story in st.session_state.completed}
        missing = [story["name"] for story in PRODUCT_BACKLOG if story["id"] in mandatory_ids - completed_ids]
        st.error("MVP incompleto. Faltaron: " + ", ".join(missing))

    st.subheader("Resultados por sprint")
    st.dataframe(pd.DataFrame(st.session_state.sprint_summaries), hide_index=True, width="stretch")

    st.subheader("📥 Exportar resultados")
    left, right = st.columns(2)
    left.download_button(
        "Descargar decisiones detalladas (CSV)",
        data=csv_bytes(st.session_state.event_log),
        file_name=f"guatecome_decisiones_{st.session_state.team_name.replace(' ', '_')}.csv",
        mime="text/csv",
        width="stretch",
    )
    right.download_button(
        "Descargar resumen por sprint (CSV)",
        data=csv_bytes(st.session_state.sprint_summaries),
        file_name=f"guatecome_resumen_{st.session_state.team_name.replace(' ', '_')}.csv",
        mime="text/csv",
        width="stretch",
    )

    with st.expander("Preguntas para la reflexión final", expanded=True):
        st.markdown(
            """
            1. ¿Qué diferencia encontraron entre completar puntos y entregar valor?
            2. ¿Cuándo protegieron el objetivo del sprint y cuándo lo pusieron en riesgo?
            3. ¿Qué costo tuvieron las soluciones rápidas?
            4. ¿Cómo influyeron las retrospectivas en los siguientes sprints?
            5. ¿Qué cambiarían si jugaran nuevamente?
            """
        )

    if st.button("🔄 Reiniciar simulación", width="stretch"):
        init_game()
        st.rerun()


sidebar()
SCREENS = {
    "intro": screen_intro,
    "mission": screen_mission,
    "planning": screen_planning,
    "daily": screen_daily,
    "consequence": screen_consequence,
    "review": screen_review,
    "retrospective": screen_retrospective,
    "end": screen_end,
}
SCREENS.get(st.session_state.screen, screen_intro)()
