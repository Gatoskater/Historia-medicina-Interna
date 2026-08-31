"""
Convierte los sub-campos estructurados de cada motivo de consulta
(asistente de Enfermedad Actual) en una frase narrativa lista para
insertarse en el relato libre, con redacción semiológica natural.
"""


def _v(datos, key):
    """Devuelve el valor si el campo fue realmente llenado. 0 es válido
    (p. ej. intensidad 0/10); None y cadenas vacías/solo-espacios no lo son."""
    val = datos.get(key)
    if val is None:
        return None
    if isinstance(val, str) and not val.strip():
        return None
    return val


def _slider_valido(datos, key):
    # Un slider en 0 puede ser "no lo llenó" o "dolor 0/10"; solo lo
    # incluimos si el usuario tocó explícitamente otro campo del bloque,
    # lo cual se resuelve a nivel de "¿hay algo más lleno?" en app.py.
    return datos.get(key)


def _minuscula_inicial(s):
    """Pone en minúscula solo la primera letra, para insertar texto libre
    del usuario a mitad de una frase sin romper la gramática."""
    if not s:
        return s
    return s[0].lower() + s[1:]


def _compose_generic(label_motivo, campos_def, datos):
    """Fallback genérico: enumera 'Campo: valor' para motivos sin plantilla dedicada."""
    partes = []
    for c in campos_def:
        v = _v(datos, c["key"])
        if v is not None:
            partes.append(f"{c['label'].lower()}: {v}")
    if not partes:
        return ""
    return f"Refiere {label_motivo.lower()} — " + "; ".join(partes) + "."


def _dolor(datos):
    d = lambda k: _v(datos, k)
    piezas = []
    inicio = "Refiere dolor"
    if d("localizacion"):
        inicio += f" localizado en {d('localizacion')}"
    piezas.append(inicio)

    if d("aparicion"):
        piezas.append(f"de aparición {_minuscula_inicial(d('aparicion'))}")
    if d("caracter"):
        piezas.append(f"de carácter {d('caracter').lower()}")
    if d("irradiacion"):
        piezas.append(f"que se irradia {d('irradiacion').lower()}" if "no" not in d("irradiacion").lower() else d("irradiacion"))
    if d("intensidad") is not None:
        piezas.append(f"de intensidad {int(d('intensidad'))}/10 según EVA")
    if d("periodicidad"):
        piezas.append(f"de curso {d('periodicidad').lower()}")
    if d("horario"):
        piezas.append(f"con {_minuscula_inicial(d('horario'))}")
    if d("duracion"):
        piezas.append(f"con una duración de {d('duracion').lower()}")

    frase = ", ".join(piezas) + "."
    extra = []
    if d("atenuantes"):
        extra.append(f"Como atenuante/agravante {d('atenuantes').lower()}.")
    if d("concomitantes"):
        extra.append(f"Concomitante con {d('concomitantes').lower()}.")
    return " ".join([frase] + extra)


def _fiebre(datos):
    d = lambda k: _v(datos, k)
    piezas = ["Refiere fiebre"]
    if d("aparicion"):
        piezas.append(f"de aparición {d('aparicion').lower()}")
    if d("cuantificacion"):
        piezas.append(f"cuantificada en {d('cuantificacion')}")
    frase = ", ".join(piezas) + "."
    extra = []
    if d("escalofrios"):
        extra.append(f"{'Precedida' if d('escalofrios')=='Sí' else 'No precedida'} de escalofríos.")
    if d("periodicidad") or d("horario"):
        s = "De curso"
        if d("periodicidad"):
            s += f" {d('periodicidad').lower()}"
        if d("horario"):
            s += f", con {d('horario').lower()}"
        extra.append(s + ".")
    if d("atenuantes"):
        extra.append(f"{d('atenuantes')}.")
    if d("concomitantes"):
        extra.append(f"Concomitante con {d('concomitantes').lower()}.")
    return " ".join([frase] + extra)


def _tos(datos):
    d = lambda k: _v(datos, k)
    piezas = ["Refiere tos"]
    if d("tipo"):
        piezas.append(d("tipo").lower())
    if d("evolucion"):
        piezas.append(f"con {d('evolucion').lower()} de evolución")
    frase = ", ".join(piezas) + "."
    extra = []
    if d("esputo"):
        extra.append(f"Esputo: {d('esputo').lower()}.")
    if d("horario"):
        extra.append(f"{d('horario')}.")
    if d("desencadenantes"):
        extra.append(f"Se desencadena con {d('desencadenantes').lower()}.")
    if d("concomitantes"):
        extra.append(f"Concomitante con {d('concomitantes').lower()}.")
    return " ".join([frase] + extra)


def _disnea(datos):
    d = lambda k: _v(datos, k)
    piezas = ["Refiere disnea"]
    if d("relacion_esfuerzo"):
        piezas.append(d("relacion_esfuerzo").lower())
    if d("evolucion"):
        piezas.append(f"de evolución {d('evolucion').lower()}")
    frase = ", ".join(piezas) + "."
    extra = []
    if d("clase_funcional"):
        extra.append(f"Clase funcional {d('clase_funcional').split('—')[0].strip()} de la NYHA.")
    if d("desencadenantes"):
        extra.append(f"Desencadenada por {d('desencadenantes').lower()}.")
    if d("concomitantes"):
        extra.append(f"Concomitante con {d('concomitantes').lower()}.")
    return " ".join([frase] + extra)


def _diarrea(datos):
    d = lambda k: _v(datos, k)
    piezas = ["Refiere diarrea"]
    if d("evolucion"):
        piezas.append(f"de {d('evolucion').lower()} de evolución")
    if d("num_evacuaciones"):
        piezas.append(f"con {d('num_evacuaciones').lower()}")
    if d("consistencia"):
        piezas.append(f"de consistencia {d('consistencia').lower()}")
    frase = ", ".join(piezas) + "."
    extra = []
    if d("color"):
        extra.append(f"{d('color')}.")
    if d("moco_sangre") and d("moco_sangre") != "No":
        extra.append(f"Con presencia de {d('moco_sangre').lower()}.")
    if d("desencadenante"):
        extra.append(f"Como posible desencadenante: {d('desencadenante').lower()}.")
    if d("concomitantes"):
        extra.append(f"Concomitante con {d('concomitantes').lower()}.")
    return " ".join([frase] + extra)


def _vomitos(datos):
    d = lambda k: _v(datos, k)
    piezas = ["Presenta vómitos"]
    if d("num_episodios"):
        piezas.append(f"en {d('num_episodios').lower()}")
    if d("contenido"):
        piezas.append(f"de contenido {d('contenido').lower()}")
    frase = ", ".join(piezas) + "."
    extra = []
    if d("nauseas_previas"):
        extra.append(f"{'Precedidos' if d('nauseas_previas')=='Sí' else 'No precedidos'} de náuseas.")
    if d("cantidad"):
        extra.append(f"Cantidad: {d('cantidad').lower()}.")
    if d("horario"):
        extra.append(f"{d('horario')}.")
    if d("concomitantes"):
        extra.append(f"Concomitante con {d('concomitantes').lower()}.")
    return " ".join([frase] + extra)


def _cefalea(datos):
    d = lambda k: _v(datos, k)
    piezas = ["Refiere cefalea"]
    if d("localizacion"):
        piezas.append(d("localizacion").lower())
    if d("caracter"):
        piezas.append(f"de carácter {d('caracter').lower()}")
    if d("intensidad") is not None:
        piezas.append(f"de intensidad {int(d('intensidad'))}/10")
    frase = ", ".join(piezas) + "."
    extra = []
    if d("duracion"):
        extra.append(f"{d('duracion')}.")
    if d("asociados"):
        extra.append(f"Asociada a {d('asociados').lower()}.")
    if d("desencadenantes"):
        extra.append(f"Desencadenada por {d('desencadenantes').lower()}.")
    return " ".join([frase] + extra)


def _edema(datos):
    d = lambda k: _v(datos, k)
    piezas = ["Refiere edema"]
    if d("localizacion"):
        piezas.append(f"en {d('localizacion').lower()}")
    frase = ", ".join(piezas) + "."
    extra = []
    if d("fovea"):
        extra.append(f"Godet: {d('fovea').lower()}.")
    if d("horario"):
        extra.append(f"De predominio {d('horario').lower()}.")
    if d("concomitantes"):
        extra.append(f"Concomitante con {d('concomitantes').lower()}.")
    return " ".join([frase] + extra)


def _sincope(datos):
    d = lambda k: _v(datos, k)
    frase = "Refiere episodio de pérdida de conciencia."
    extra = []
    if d("prodromo"):
        extra.append(f"Precedido de {d('prodromo').lower()}.")
    if d("duracion"):
        extra.append(f"Duración aproximada de {d('duracion').lower()}.")
    if d("esfinteres"):
        extra.append(f"{'Con' if d('esfinteres')=='Sí' else 'Sin'} relajación de esfínteres.")
    if d("movimientos"):
        extra.append(f"Movimientos anormales: {d('movimientos').lower()}.")
    if d("recuperacion"):
        extra.append(f"{d('recuperacion')}.")
    if d("desencadenante"):
        extra.append(f"Desencadenado por {d('desencadenante').lower()}.")
    return " ".join([frase] + extra)


def _palpitaciones(datos):
    d = lambda k: _v(datos, k)
    piezas = ["Refiere palpitaciones"]
    if d("inicio_termino"):
        piezas.append(f"de inicio y término {d('inicio_termino').lower()}")
    if d("ritmo"):
        piezas.append(f"de ritmo {d('ritmo').lower()}")
    frase = ", ".join(piezas) + "."
    extra = []
    if d("duracion"):
        extra.append(f"{d('duracion')}.")
    if d("desencadenantes"):
        extra.append(f"Desencadenadas por {d('desencadenantes').lower()}.")
    if d("concomitantes"):
        extra.append(f"Concomitante con {d('concomitantes').lower()}.")
    return " ".join([frase] + extra)


_COMPOSERS = {
    "dolor": _dolor, "fiebre": _fiebre, "tos": _tos, "disnea": _disnea,
    "diarrea": _diarrea, "vomitos": _vomitos, "cefalea": _cefalea,
    "edema": _edema, "sincope": _sincope, "palpitaciones": _palpitaciones,
}


def componer_narrativa(motivo_key, motivo_label, campos_def, datos):
    """Devuelve la frase narrativa para un motivo dado, o cadena vacía si no hay datos."""
    if not any(_v(datos, c["key"]) is not None for c in campos_def):
        return ""
    fn = _COMPOSERS.get(motivo_key)
    if fn:
        texto = fn(datos)
        # Si el composer específico no encontró nada útil, cae al genérico.
        if texto and texto.strip() not in ("", "."):
            return texto
    return _compose_generic(motivo_label, campos_def, datos)
