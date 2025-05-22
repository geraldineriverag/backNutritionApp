FORM_SCHEMA = [
    {
        "title": "Paso 1: Medidas Corporales",
        "fields": [
            {"key": "height", "label": "Altura (cm)", "type": "numeric"},
            {"key": "current_weight", "label": "Peso actual (kg)", "type": "numeric"},
            {"key": "waist_circumference", "label": "Cintura (cm)", "type": "numeric"},
            {"key": "hip_circumference", "label": "Cadera (cm)", "type": "numeric"},
        ],
    },
    {
        "title": "Paso 2: Objetivos Nutricionales",
        "fields": [
            {
                "key": "goal_type",
                "label": "Objetivo principal",
                "type": "select",
                "options": [
                    "Pérdida de peso",
                    "Ganar masa muscular",
                    "Mantenimiento",
                    "Mejorar hábitos",
                    "Tratar condición médica",
                ],
            },
            {"key": "medical_condition", "label": "Condición médica", "type": "text"},
            {"key": "allergies", "label": "Alergias", "type": "textarea"},
            {"key": "medications", "label": "Medicamentos", "type": "textarea"},
        ],
    },
    {
        "title": "Paso 3: Condiciones y Salud",
        "fields": [
            {"key": "preexisting_condition", "label": "Condiciones preexistentes", "type": "textarea"},
            {"key": "digestive_issues", "label": "Problemas digestivos", "type": "textarea"},
            {"key": "past_surgeries", "label": "Cirugías previas", "type": "textarea"},
            {"key": "fitness_level", "label": "Nivel de condición física", "type": "select", "options": ["Bajo", "Moderado", "Alto"]},
        ],
    },
    {
        "title": "Paso 4: Actividad Física",
        "fields": [
            {
                "key": "work_activity",
                "label": "Actividad laboral",
                "type": "select",
                "options": ["Sedentario", "Activo", "Muy activo"],
            },
            {
                "key": "exercise_frequency",
                "label": "Frecuencia de ejercicio (veces por semana)",
                "type": "numeric",
            },
            {"key": "exercise_type", "label": "Tipo de ejercicio", "type": "text"},
        ],
    },
    {
        "title": "Paso 5: Hábitos Alimenticios",
        "fields": [
            {"key": "meals_per_day", "label": "Comidas por día", "type": "numeric"},
            {"key": "meal_schedule", "label": "Horario de comidas", "type": "textarea"},
            {"key": "dietary_preferences", "label": "Preferencias dietéticas", "type": "text"},
            {"key": "favorite_foods", "label": "Comidas favoritas", "type": "textarea"},
        ],
    },
    {
        "title": "Paso 6: Alimentación y Salud",
        "fields": [
            {"key": "avoided_foods", "label": "Comidas evitadas", "type": "textarea"},
            {"key": "water_intake", "label": "Ingesta de agua (litros)", "type": "numeric"},
            {"key": "alcohol_caffeine_consumption", "label": "Consumo de alcohol o cafeína", "type": "textarea"},
        ],
    },
    {
        "title": "Paso 7: Cocina y Presupuesto",
        "fields": [
            {"key": "budget", "label": "Presupuesto disponible", "type": "numeric"},
            {
                "key": "cooking_time",
                "label": "Tiempo disponible para cocinar",
                "type": "select",
                "options": ["Poco tiempo", "Tiempo medio", "Mucho tiempo"],
            },
        ],
    },
]
