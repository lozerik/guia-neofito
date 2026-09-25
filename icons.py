"""Emblemas heráldicos originales, uno por facción.

No son los logos oficiales de Games Workshop: son insignias propias,
compuestas desde cero (marca central + aro doble + almenas), pensadas para
tener el aire de una insignia de capítulo o de casa sin copiar ningún
diseño registrado.

ICONS[slug] es el contenido interno de un <svg viewBox="0 0 64 64">, en
trazo (stroke="currentColor"), listo para heredar el color de la facción.
"""

_STROKE = 'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'

# Marca central de cada facción, ya pensada para caber en un círculo de
# radio ~19 centrado en (32,32) — el aro y las almenas se añaden aparte.
_MARKS = {
    # ---------------------------------------------------------------- Imperio
    # Astartes: espada alada, laureles de una legión veterana.
    "astartes": f'''<g {_STROKE}>
        <path d="M32 15v26M27 41h10M32 41l-4 8M32 41l4 8"/>
        <path d="M32 18c-5 1-9 5-10 10 4 0 8-1 10-4"/>
        <path d="M32 18c5 1 9 5 10 10-4 0-8-1-10-4"/>
    </g>''',

    # Astra Militarum: águila de infantería sobre bayonetas cruzadas.
    "militarum": f'''<g {_STROKE}>
        <path d="M20 44L32 17l12 27"/>
        <path d="M24 36h16"/>
        <circle cx="32" cy="27" r="3"/>
    </g>''',

    # Adeptus Mechanicus: engranaje con un ojo central, el Omnissiah que todo lo ve.
    "mechanicus": f'''<g {_STROKE}>
        <circle cx="32" cy="32" r="9"/>
        <circle cx="32" cy="32" r="3"/>
        <path d="M32 16v5M32 43v5M16 32h5M43 32h5
                 M21 21l3.4 3.4M39.6 39.6L43 43M43 21l-3.4 3.4M24.4 39.6L21 43"/>
    </g>''',

    # Sororitas: llama dentro de una gota, la fe que arde.
    "sororitas": f'''<g {_STROKE}>
        <path d="M32 15c7 10 10 16 10 21a10 10 0 1 1-20 0c0-5 3-11 10-21z"/>
        <path d="M32 28c3 4 4 7 4 10a4 4 0 1 1-8 0c0-3 1-6 4-10z"/>
    </g>''',

    # Custodes: sol radiante, la guardia dorada del trono.
    "custodes": f'''<g {_STROKE}>
        <circle cx="32" cy="32" r="7"/>
        <path d="M32 15v6M32 43v6M15 32h6M43 32h6
                 M20 20l4.2 4.2M39.8 39.8L44 44M44 20l-4.2 4.2M24.2 39.8L20 44"/>
    </g>''',

    # ------------------------------------------------------------------ Caos
    # Marines del Caos: estrella de ocho puntas rota, el juramento traicionado.
    "chaos-marines": f'''<g {_STROKE}>
        <path d="M32 14l3.4 10 10-5-5 10 10 3.4-10 3.4 5 10-10-5-3.4 10-3.4-10-10 5 5-10-10-3.4 10-3.4-5-10 10 5z"/>
    </g>''',

    # Guardia de la Muerte: gota de plaga sobre un anillo agrietado.
    "death-guard": f'''<g {_STROKE}>
        <circle cx="32" cy="33" r="11"/>
        <path d="M32 18c3 4 4.5 6.5 4.5 9.5a4.5 4.5 0 1 1-9 0c0-3 1.5-5.5 4.5-9.5z"/>
        <path d="M23 39l2.5 2.5M41 39l-2.5 2.5"/>
    </g>''',

    # Mil Hijos: ojo dentro de una pirámide de llamas, el conocimiento prohibido.
    "thousand-sons": f'''<g {_STROKE}>
        <path d="M32 16l13 24H19z"/>
        <ellipse cx="32" cy="35" rx="6" ry="3.4"/>
        <circle cx="32" cy="35" r="1.3"/>
    </g>''',

    # Devoradores de Mundos: hacha partiendo una cadena.
    "world-eaters": f'''<g {_STROKE}>
        <path d="M21 21l10 10M43 21L33 31"/>
        <path d="M21 21l-3 3 5 5 3-3zM43 21l3 3-5 5-3-3z"/>
        <circle cx="27" cy="38" r="3.4"/><circle cx="37" cy="44" r="3.4"/>
    </g>''',

    # Demonios: estrella de cuatro puntas irregulares, la disformidad hecha forma.
    "daemons": f'''<g {_STROKE}>
        <path d="M32 14c1.5 8 4.5 13.5 12 15.5-7.5 2-10.5 7.5-12 15.5-1.5-8-4.5-13.5-12-15.5 7.5-2 10.5-7.5 12-15.5z"/>
    </g>''',

    # ---------------------------------------------------------------- Xenos
    # Aeldari: lágrima-rúnica en espiral, el duelo de un pueblo antiguo.
    "aeldari": f'''<g {_STROKE}>
        <path d="M32 15c9 7 10.5 15 6 22a7.5 7.5 0 1 1-12 0c-4.5-7-3-15 6-22z"/>
        <path d="M32 31a4.4 4.4 0 1 0 0 8.8"/>
    </g>''',

    # Drukhari: media luna espinada, el placer que corta.
    "drukhari": f'''<g {_STROKE}>
        <path d="M39 17a16 16 0 1 0 0 30 19 19 0 0 1 0-30z"/>
        <path d="M18 24l-4.5-1.5M17 32h-4.5M18 40l-4.5 1.5"/>
    </g>''',

    # Orkos: colmillo mellado, la fuerza bruta.
    "orks": f'''<g {_STROKE}>
        <path d="M25 15l4.5 25-7.5 10 15-7.5-4.5-27.5z"/>
        <path d="M25 24l-6-1.5M26.5 31.5l-6.5.7M28 39l-6 3"/>
    </g>''',

    # T'au: tres puntas orbitando un centro, las castas unidas en el Bien Mayor.
    "tau": f'''<g {_STROKE}>
        <circle cx="32" cy="32" r="3"/>
        <path d="M32 20v7M32 20l-4.4 3M32 20l4.4 3"/>
        <path d="M42.5 38.5l-6.6-3M42.5 38.5l-1.4 5M42.5 38.5l-6 1.4"/>
        <path d="M21.5 38.5l6.6-3M21.5 38.5l1.4 5M21.5 38.5l6-1.4"/>
    </g>''',

    # Tiránidos: tres garras convergiendo, el enjambre que devora.
    "tyranids": f'''<g {_STROKE}>
        <path d="M32 47V24M32 24c-4.4-5.8-4.4-8.8-1.4-11.6M32 24c4.4-5.8 4.4-8.8 1.4-11.6
                 M32 24c-7.3-1.4-11.7 0-14.6 4.4M32 24c7.3-1.4 11.7 0 14.6 4.4"/>
    </g>''',

    # Necrones: ojo dentro de un obelisco quebrado, reyes que despiertan.
    # -------------------------------------------------- Legiones leales
    # Ángeles Oscuros: capucha y cáliz, la orden que guarda un secreto.
    "dark-angels": f'''<g {_STROKE}>
        <path d="M32 15c-6 3-9 8-9 15v9a9 9 0 0 0 18 0v-9c0-7-3-12-9-15z"/>
        <path d="M27 33h10M32 28v10"/>
    </g>''',

    # Estirpe Blanca: media luna y un rayo, la velocidad de la estepa.
    "white-scars": f'''<g {_STROKE}>
        <path d="M37 16a15 15 0 1 0 0 30 18 18 0 0 1 0-30z"/>
        <path d="M20 44l6-9-4-1 8-10-3 8 4 1-6 9"/>
    </g>''',

    # Lobos Espaciales: cabeza de lobo triangular, colmillos al frente.
    "space-wolves": f'''<g {_STROKE}>
        <path d="M32 15l11 13-3 14-8-6-8 6-3-14z"/>
        <path d="M24 27l-4-5M40 27l4-5M28 38l-1.5 5M36 38l1.5 5"/>
    </g>''',

    # Puños Imperiales: puño cerrado sobre una almena, la muralla que no cede.
    "imperial-fists": f'''<g {_STROKE}>
        <path d="M22 46V26h4v-5h4v5h4v-6h4v6h4v-5h4v5h4v20z"/>
        <path d="M24 46v-9h16v9"/>
    </g>''',

    # Ultramarines: escudo con laurel y un cheurón, el ideal del Codex.
    "ultramarines": f'''<g {_STROKE}>
        <path d="M32 15c-3 3-6 5-10 6 0 12 3 19 10 21 7-2 10-9 10-21-4-1-7-3-10-6z"/>
        <path d="M25 32l7 4 7-4"/>
    </g>''',

    # Ángeles Sangrientos: gota alada, la nobleza y la maldición de Sanguinius.
    "blood-angels": f'''<g {_STROKE}>
        <path d="M32 18c5 8 8 13 8 18a8 8 0 1 1-16 0c0-5 3-10 8-18z"/>
        <path d="M24 30c-5 1-8 4-9 8M40 30c5 1 8 4 9 8"/>
    </g>''',

    # Manos de Hierro: garra mecánica de tres dedos, la carne sustituida.
    "iron-hands": f'''<g {_STROKE}>
        <path d="M32 44V22M32 22l-7-8M32 22l7-8M24 30l-8-3M40 30l8-3"/>
        <circle cx="32" cy="44" r="3"/>
    </g>''',

    # Salamandras: llama sobre un yunque, artesanos del fuego.
    "salamanders": f'''<g {_STROKE}>
        <path d="M32 15c5 7 7 11 7 15a7 7 0 1 1-14 0c0-4 2-8 7-15z"/>
        <path d="M20 44h24M24 44v4h16v-4"/>
    </g>''',

    # Guardia Cuervo: ala de cuervo angular, el golpe desde la sombra.
    "raven-guard": f'''<g {_STROKE}>
        <path d="M18 40c6-14 10-20 18-22-2 6-2 10 0 14-7 1-12 4-18 8z"/>
        <path d="M22 34l-6 8"/>
    </g>''',

    # -------------------------------------------------- Legiones traidoras
    # Hijos del Emperador: pluma-ojo, la perfección vuelta exceso.
    "emperors-children": f'''<g {_STROKE}>
        <path d="M32 16c8 4 12 11 12 19-4 6-8 9-12 9s-8-3-12-9c0-8 4-15 12-19z"/>
        <circle cx="32" cy="34" r="3.4"/>
    </g>''',

    # Guerreros de Hierro: torre almenada partida por un rayo de asedio.
    "iron-warriors": f'''<g {_STROKE}>
        <path d="M23 46V22h4v-4h4v4h2v-6h2v6h2v-4h4v4h4v24z"/>
        <path d="M28 46V33l4-5 4 5v13"/>
    </g>''',

    # Señores de la Noche: garra-rayo, el terror antes que la fuerza.
    "night-lords": f'''<g {_STROKE}>
        <path d="M32 15l-4 12 5-2-5 12 12-16-6 1z"/>
        <path d="M20 44l6-8M44 44l-6-8"/>
    </g>''',

    # Portadores de la Palabra: libro abierto en llamas, la fe primera.
    "word-bearers": f'''<g {_STROKE}>
        <path d="M14 22c6-2 12-2 18 2 6-4 12-4 18-2v20c-6-2-12-2-18 2-6-4-12-4-18-2z"/>
        <path d="M32 24v18"/>
    </g>''',

    # Legión Alfa: hidra de dos cabezas, nadie sabe de qué lado están.
    "alpha-legion": f'''<g {_STROKE}>
        <path d="M32 46V24c0-6-4-9-9-9M32 24c0-6 4-9 9-9"/>
        <circle cx="21" cy="14" r="2.6"/><circle cx="43" cy="14" r="2.6"/>
    </g>''',

    # -------------------------------------------------- Xenos nuevos
    # Liga de Votann: piedra rúnica con una chispa, la memoria de los ancestros.
    "votann": f'''<g {_STROKE}>
        <path d="M20 44V26l12-10 12 10v18z"/>
        <path d="M32 24v8M28 28h8"/>
    </g>''',

        "necrons": f'''<g {_STROKE}>
        <path d="M24 47V25l8-11 8 11v22z"/>
        <ellipse cx="32" cy="33" rx="5" ry="2.8"/>
        <circle cx="32" cy="33" r="1.1" fill="currentColor" stroke="none"/>
    </g>''',
}

# Ocho almenas cortas en torno al aro exterior, como en una insignia de casa.
_BATTLEMENTS = "".join(
    f'<path d="M{32 + 27.5 * __import__("math").cos(__import__("math").radians(a)):.2f} '
    f'{32 + 27.5 * __import__("math").sin(__import__("math").radians(a)):.2f} '
    f'L{32 + 30.5 * __import__("math").cos(__import__("math").radians(a)):.2f} '
    f'{32 + 30.5 * __import__("math").sin(__import__("math").radians(a)):.2f}"/>'
    for a in range(0, 360, 45)
)

_FRAME = f'''<g fill="none" stroke="currentColor">
    <circle cx="32" cy="32" r="30" stroke-width="1.6"/>
    <circle cx="32" cy="32" r="25.5" stroke-width="1"/>
    <g stroke-width="2" stroke-linecap="round">{_BATTLEMENTS}</g>
</g>'''

ICONS = {slug: _FRAME + mark for slug, mark in _MARKS.items()}
