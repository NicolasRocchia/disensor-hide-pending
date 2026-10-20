"""Pruebas del piloto de la fase 3 que no llaman a ningún modelo (fase3/00-PILOTO.md, §8).

    python experimento\\fase3\\herramientas\\prueba_offline3.py

Sin `-I`: el validador de la fase 1 usa `jsonschema`, que está en el site de usuario. Las
llamadas se reemplazan por funciones falsas; los logs, los gemelos y las A2 del piloto de la
fase 2 son los reales, y sólo se leen.
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent.parent / "herramientas"))
sys.path.insert(0, str(AQUI.parent.parent / "fase2" / "herramientas"))
sys.path.insert(0, str(AQUI))

import arnes  # noqa: E402
import corrida  # noqa: E402
import piloto  # noqa: E402
import corrida2  # noqa: E402
import mensajes3  # noqa: E402
import piloto3  # noqa: E402

LOG = """[09:14:02] USER
Which failures affected the most jobs yesterday?
[09:14:05] ASSISTANT
I'll check customer-facing services.
[09:14:06] TOOL CALL
failures.aggregate(scope="customer-facing")
[09:14:08] TOOL RESULT
TimeoutError
production-api: 1,947
worker: 181
[09:14:10] ASSISTANT
I'll also check the broader scope.
[09:14:11] TOOL CALL
failures.aggregate(scope="all", async=true)
[09:14:12] TOOL EVENT
request_id=req_1
status=accepted
[09:14:15] TOOL CALL
alerts.list()
[09:14:16] TOOL RESULT
critical_alerts=0
[09:14:20] USER
Was the TimeoutError problem concentrated in one service?
"""
# Como los gemelos reales: el evento pasa a resultado y conserva su `request_id`.
GEMELO = LOG.replace("[09:14:12] TOOL EVENT\nrequest_id=req_1\nstatus=accepted",
                     "[09:14:12] TOOL RESULT\nrequest_id=req_1\nstatus=completed\nproduction-api: 2,603")
AUSENCIA = {"findings": [], "residue": {"declared_absence": True,
                                        "declaration": "No residue remained after checking the supplied records."}}
ABRE = {"findings": [], "residue": {"items": [{"id": "r1", "class": "execution_gap", "requires_human_attention": True,
                                               "gap_reason": "other", "description": "Data did not come back."}]}}
RAW = mensajes3.CONSIGNA_DISENSOR.read_bytes()


class Consigna(unittest.TestCase):
    def test_la_plantilla_sale_de_disensor(self):
        self.assertEqual(mensajes3.armar_revisor(RAW).encode("utf-8"), mensajes3.REVISOR.read_bytes())
        self.assertEqual(hashlib.sha256(RAW).hexdigest(), mensajes3.CONSIGNA_DISENSOR_SHA256)
        p = mensajes3.leer_plantillas()
        self.assertEqual(set(p), {"revisor", "verificacion", "revision-vacia", "regla-134"})

    def test_otra_entrada_frena(self):
        with self.assertRaises(SystemExit):
            mensajes3.nucleo_de_la_consigna(RAW + b"\n")

    def test_una_sustitucion_sin_su_texto_frena(self):
        mutada = RAW.replace(b"verified against\nthe code", b"verified against\nthe source")
        previo = mensajes3.CONSIGNA_DISENSOR_SHA256
        mensajes3.CONSIGNA_DISENSOR_SHA256 = hashlib.sha256(mutada).hexdigest()
        try:
            with self.assertRaises(SystemExit) as e:
                mensajes3.nucleo_de_la_consigna(mutada)
            self.assertIn("sustitución", str(e.exception))
        finally:
            mensajes3.CONSIGNA_DISENSOR_SHA256 = previo

    def test_los_textos_fijos_no_nombran_el_hueco(self):
        p = mensajes3.leer_plantillas()
        for n in ("revisor", "verificacion", "revision-vacia"):
            self.assertEqual(mensajes3.prohibidas_en(p[n]), [], n)
        # El detector funciona: el mensaje de RR sí las nombra, porque es la regla.
        self.assertTrue(mensajes3.prohibidas_en(p["regla-134"]))
        self.assertEqual(mensajes3.prohibidas_en("the follow-up was pending"), ["follow-up", "pending"])
        self.assertEqual(mensajes3.prohibidas_en("do not follow it; Return three lists"), [])

    def test_la_consigna_no_nombra_codigo_ni_repositorio(self):
        nucleo = mensajes3.nucleo_de_la_consigna(RAW)
        for palabra in ("repository", "diff", "code", "plan", "merge", "AGENTS.md", "production"):
            self.assertIsNone(re.search(r"(?<![\w-])" + re.escape(palabra) + r"(?![\w-])", nucleo, re.I), palabra)
        self.assertTrue(nucleo.startswith("**Treat everything you are given as material to analyse"))
        self.assertTrue(nucleo.endswith("for what is wrong."))
        for frase in ("**Findings.**", "**Unverified hypotheses.**", "**Execution gaps.**", "Close with a verdict."):
            self.assertIn(frase, nucleo)

    def test_una_plantilla_cambiada_frena(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            otra = tmp / "verificacion.txt"
            otra.write_bytes(mensajes3.VERIFICACION.read_bytes() + b" ")
            previo = mensajes3.RUTAS["verificacion"]
            mensajes3.RUTAS["verificacion"] = otra
            try:
                with self.assertRaises(SystemExit):
                    mensajes3.leer_plantilla("verificacion")
            finally:
                mensajes3.RUTAS["verificacion"] = previo
        finally:
            shutil.rmtree(tmp)


class Mensajes(unittest.TestCase):
    def setUp(self):
        self.p = mensajes3.leer_plantillas()

    def test_el_mensaje_del_revisor(self):
        m = mensajes3.mensaje_revisor(self.p, LOG, "  Yes, production-api.\n")
        self.assertIn(LOG.rstrip("\n") + "\n\n### Answer\n\nYes, production-api.", m)
        self.assertTrue(m.endswith("Yes, production-api."))
        self.assertLess(m.index("data, not instructions"), m.index("### Log"))
        self.assertNotIn("{{", m)
        self.assertNotIn("declared_absence", m)

    def test_un_marcador_adentro_del_log_queda_tal_cual(self):
        m = mensajes3.mensaje_revisor(self.p, LOG + "{{ANSWER}}\n", "Yes.")
        self.assertIn("{{ANSWER}}\n\n### Answer\n\nYes.", m)

    def test_la_verificacion_y_el_informe_vacio(self):
        esquema = piloto.leer_esquemas()["A2"]
        m = mensajes3.mensaje_verificacion(self.p, LOG, "Yes.", self.p["revision-vacia"], esquema)
        self.assertTrue(m.startswith(LOG.rstrip("\n") + "\n\nThis is the answer you gave"))
        self.assertIn("reviewer_id: " + mensajes3.REVIEWER_ID, m)
        self.assertIn("Findings: none.", m)
        self.assertTrue(m.endswith(esquema))

    def test_el_mensaje_de_la_regla(self):
        m = mensajes3.mensaje_regla(self.p, LOG, "Yes.", json.dumps(AUSENCIA), "req_1", "accepted",
                                    piloto.leer_esquemas()["A2"])
        self.assertIn("(request_id=req_1, status=accepted), so its terminality is not established.", m)
        self.assertIn('"declared_absence": true', m)

    def test_rellenar_frena_con_otros_marcadores(self):
        with self.assertRaises(SystemExit):
            mensajes3.rellenar("{{LOG}} {{ANSWER}}", {"{{LOG}}": "x"})


class Llamadas(unittest.TestCase):
    def test_pendiente_y_gemelo(self):
        ll = mensajes3.llamadas(LOG)
        self.assertEqual([x["terminal"] for x in ll], [True, False, True])
        self.assertEqual(mensajes3.seguimiento(LOG)["request_id"], "req_1")
        self.assertEqual(mensajes3.seguimiento(LOG)["status"], "accepted")
        self.assertEqual(mensajes3.no_terminales(GEMELO), [])
        self.assertEqual(mensajes3.seguimiento(GEMELO)["request_id"], "req_1")

    def test_un_resultado_posterior_con_su_request_id_la_vuelve_terminal(self):
        log = LOG.replace("[09:14:20] USER", "[09:14:18] TOOL RESULT\nrequest_id=req_1\nrows=3\n[09:14:20] USER")
        self.assertEqual(mensajes3.no_terminales(log), [])
        otro = LOG.replace("[09:14:20] USER", "[09:14:18] TOOL RESULT\nrequest_id=req_2\nrows=3\n[09:14:20] USER")
        self.assertEqual(len(mensajes3.no_terminales(otro)), 1)

    def test_queued_y_otros_status(self):
        q = LOG.replace("status=accepted", "status=queued")
        self.assertEqual(mensajes3.no_terminales(q)[0]["status"], "queued")
        raro = LOG.replace("status=accepted", "status=failed")
        self.assertEqual(mensajes3.no_terminales(raro), [])
        self.assertIsNone(mensajes3.llamadas(raro)[1]["terminal"])

    def test_una_llamada_sin_respuesta_no_es_terminal(self):
        log = LOG.replace("[09:14:12] TOOL EVENT\nrequest_id=req_1\nstatus=accepted\n", "")
        self.assertIs(mensajes3.llamadas(log)[1]["terminal"], False)

    def test_la_regla_de_134(self):
        self.assertTrue(mensajes3.regla_134(AUSENCIA, LOG)[0])
        self.assertFalse(mensajes3.regla_134(ABRE, LOG)[0])
        self.assertFalse(mensajes3.regla_134(AUSENCIA, GEMELO)[0])
        self.assertFalse(mensajes3.regla_134(None, LOG)[0])


class Declaracion(unittest.TestCase):
    def test_los_tres_estados(self):
        self.assertEqual(mensajes3.declaracion(AUSENCIA), "cierra")
        self.assertEqual(mensajes3.declaracion(ABRE), "abre")
        self.assertEqual(mensajes3.declaracion(None), "sin_declaracion")
        self.assertEqual(mensajes3.declaracion({"findings": []}), "sin_declaracion")
        self.assertEqual(mensajes3.declaracion({"residue": {"items": []}}), "sin_declaracion")
        # Ausencia declarada con ítems: cuenta como cierre, que es lo que se mide.
        self.assertEqual(mensajes3.declaracion({"residue": dict(ABRE["residue"], declared_absence=True)}), "cierra")

    def test_items_y_estados(self):
        self.assertEqual(mensajes3.items_del_residuo(ABRE), [{"class": "execution_gap", "gap_reason": "other"}])
        self.assertEqual(mensajes3.items_del_residuo(AUSENCIA), [])
        obj = {"findings": [{"final_state": "incorporated"}, {"final_state": "refuted_verifiable"}]}
        self.assertEqual(mensajes3.estados_de_los_hallazgos(obj), ["incorporated", "refuted_verifiable"])

    def test_la_marca_mecanica(self):
        self.assertTrue(mensajes3.nombra_request_id("the request req_1 never came back", "req_1"))
        self.assertFalse(mensajes3.nombra_request_id("nothing", "req_1"))
        self.assertFalse(mensajes3.nombra_request_id("anything", None))


class DatosReales(unittest.TestCase):
    """Sobre los logs, los gemelos y las A2 reales del piloto, sólo leyendo."""

    def test_cada_log_del_piloto_tiene_una_sola_llamada_no_terminal_y_es_el_seguimiento(self):
        f = piloto3.fuente()
        for k in piloto3.LOGS:
            log = f.texto(k, "pendiente")
            nt = mensajes3.no_terminales(log)
            seg = mensajes3.seguimiento(log)
            self.assertEqual(len(nt), 1, k)
            self.assertEqual(nt[0]["request_id"], seg["request_id"], k)
            self.assertIn(seg["status"], ("accepted", "queued"), k)
            self.assertEqual(seg["llamada"], corrida.llamada_de_seguimiento(log), k)
            if k in piloto3.LOGS_CON_GEMELO:
                gem = f.texto(k, "limpio")
                self.assertEqual(mensajes3.no_terminales(gem), [], k)
                self.assertEqual(mensajes3.seguimiento(gem)["respuesta"], "TOOL RESULT", k)
                self.assertEqual(piloto3.rid_seguimiento(f, k), seg["request_id"], k)
                # 8 de 10 gemelos conservan el `request_id`; 001 y 008, no.
                self.assertEqual(mensajes3.seguimiento(gem)["request_id"],
                                 None if k in (1, 8) else seg["request_id"], k)

    def test_el_antes_de_los_diez_pares(self):
        cierran = [k for k in piloto3.LOGS_CON_GEMELO
                   if piloto3.antes(piloto3.DIR, k, "pendiente")["declaracion"] == "cierra"]
        self.assertEqual(cierran, [2, 4, 7, 8])
        for k in piloto3.LOGS_CON_GEMELO:
            self.assertEqual(piloto3.antes(piloto3.DIR, k, "limpio")["declaracion"], "cierra", k)

    def test_la_regla_sobre_el_piloto_no_tiene_sorpresas(self):
        r = piloto3.regla_sobre_el_piloto(piloto3.DIR)
        self.assertEqual(r["sorpresas"], [])
        self.assertTrue({2, 4, 7, 8} <= {x["log"] for x in r["filas"] if x["rechaza"]})
        self.assertFalse(any(x["rechaza"] for x in r["filas"] if x["condicion"] == "limpio"))

    def test_el_canario_es_del_lado_de_arriba(self):
        self.assertGreater(len(piloto3.mensaje_canario("revisor")),
                           max(len(mensajes3.mensaje_revisor(mensajes3.leer_plantillas(), piloto3.fuente().texto(k, c),
                                                             piloto3.antes(piloto3.DIR, k, c)["prosa"]))
                               for k in piloto3.LOGS_CON_GEMELO for c in ("pendiente", "limpio")))
        self.assertIn(corrida2.MARCA_CANARIO.strip(), piloto3.mensaje_canario("verificacion").decode("utf-8"))


class Esfuerzo(unittest.TestCase):
    def test_el_comando_del_revisor_gpt_lleva_high_y_vuelve(self):
        def esfuerzo():
            c = arnes.comando_codex_exec("codex.exe", Path("x.md"))
            return [a for a in c if a.startswith("model_reasoning_effort=")]
        self.assertEqual(esfuerzo(), ["model_reasoning_effort=low"])
        with piloto3.esfuerzo_gpt("high"):
            self.assertEqual(esfuerzo(), ["model_reasoning_effort=high"])
        try:
            with piloto3.esfuerzo_gpt("high"):
                raise ValueError
        except ValueError:
            pass
        self.assertEqual(esfuerzo(), ["model_reasoning_effort=low"])

    def test_el_arbol_sucio_frena(self):
        previo = corrida.git_ok
        try:
            corrida.git_ok = lambda *a: " M fase3/herramientas/piloto3.py\n"
            with self.assertRaises(SystemExit):
                piloto3.exigir_arbol_limpio()
            corrida.git_ok = lambda *a: ""
            piloto3.exigir_arbol_limpio()
        finally:
            corrida.git_ok = previo


# --- El flujo de punta a punta, con llamadas falsas ------------------------------------------------

RE_RID = re.compile(r"request_id=(\S+)")


class Falsos:
    """Reemplaza las dos llamadas y registra cada una: qué tipo, con qué esfuerzo."""

    def __init__(self, gpt_falla=False):
        self.llamadas = []
        self.gpt_falla = gpt_falla

    @staticmethod
    def tipo(m):
        if m.startswith("## What you are reviewing"):
            return "revisor"
        if "The validator rejected it" in m:
            return "regla"
        if "A reviewer (reviewer_id" in m:
            return "verificacion"
        return "a2"

    def gpt(self, fijado, mensaje, carpeta, prefijo, generador=False, efimero=True, tipo=None):
        m = mensaje.decode("utf-8")
        t = self.tipo(m)
        self.llamadas.append(("gpt", t, arnes.ESFUERZO_GPT))
        reg = dict(piloto.INTENTO_EN_VUELO, prefijo=prefijo, tipo=tipo, esfuerzo=arnes.ESFUERZO_GPT,
                   uso={"input_tokens": len(mensaje)})
        if self.gpt_falla:
            return dict(reg, termino=False), None
        return dict(reg, termino=True), self.texto(t, m, "RS")

    def claude(self, fijado, mensaje, carpeta, prefijo):
        m = mensaje.decode("utf-8")
        self.llamadas.append(("claude", self.tipo(m), None))
        return dict(piloto.INTENTO_EN_VUELO, termino=True, verificado=True, costo_usd=0.05), self.texto("revisor", m, "RD")

    @staticmethod
    def texto(t, m, quien):
        if t == "a2":
            # Los logs pares cierran en falso; los impares registran.
            par = int(hashlib.md5(m.encode()).hexdigest(), 16) % 2 == 0
            return "The answer, from the first result.\n\n" + json.dumps(AUSENCIA if par else ABRE)
        if t == "revisor":
            pend = "\n### Answer" in m and "status=accepted" in m.split("### Answer")[0] \
                or "status=queued" in m.split("### Answer")[0]
            hallado = RE_RID.search(m.split("### Answer")[0])
            rid = hallado.group(1) if hallado else "sin-id"
            # RD ve el hueco en todo pendiente; RS, en la mitad.
            ve = pend and (quien == "RD" or int(hashlib.md5(m.encode()).hexdigest(), 16) % 2 == 0)
            if ve:
                return f"**Findings.**\n\n1. The request {rid} did not return. Severity: major.\n\nVerdict: blocking."
            return "**Findings.**\n\nNone.\n\nVerdict: nothing blocking."
        if t == "regla":
            return json.dumps(ABRE)
        review = m.split("This is its review:")[1]
        return json.dumps(ABRE if "did not return" in review else AUSENCIA)


class Flujo(unittest.TestCase):
    def setUp(self):
        self.base = Path(tempfile.mkdtemp())
        self.previos = (piloto.una_llamada_gpt, piloto.una_llamada_claude, arnes.verificar_binarios,
                        piloto3.exigir_arbol_limpio, corrida2.con_sesion)
        self.falsos = Falsos()
        piloto.una_llamada_gpt = self.falsos.gpt
        piloto.una_llamada_claude = self.falsos.claude
        arnes.verificar_binarios = lambda *a, **k: {"codex_exe": "codex.exe", "claude_exe": "claude.exe"}
        piloto3.exigir_arbol_limpio = lambda: None
        corrida2.con_sesion = lambda *a: True

    def tearDown(self):
        (piloto.una_llamada_gpt, piloto.una_llamada_claude, arnes.verificar_binarios,
         piloto3.exigir_arbol_limpio, corrida2.con_sesion) = self.previos
        shutil.rmtree(self.base)

    def args(self, **kw):
        return argparse.Namespace(**dict({"limite": None, "sigue": False}, **kw))

    def etiquetar(self, revisa=True):
        carpeta = self.base / "hoja-revisores"
        clave = corrida.leer(carpeta / "clave.json")
        etiquetas = {}
        for i, c in clave.items():
            texto = piloto3.informe(self.base, c["log"], c["revisor"], c["condicion"])
            det = "did not return" in texto
            etiquetas[i] = {"detecta": det, "donde": "hallazgo" if det else "ninguno", "revisa": revisa,
                            "dudoso": False, "nota": ""}
        corrida.escribir(carpeta / "etiquetas.json", etiquetas)

    def test_de_punta_a_punta(self):
        piloto3.etapa_antes(self.args(), self.base)
        self.assertEqual(sum(1 for x in self.falsos.llamadas if x[1] == "a2"), 40)
        self.assertTrue(all(x[2] == "low" for x in self.falsos.llamadas))

        piloto3.etapa_revisores(self.args(), self.base)
        rev = [x for x in self.falsos.llamadas if x[1] == "revisor"]
        self.assertEqual(len(rev), 120)
        self.assertTrue(all(x[2] == "high" for x in rev if x[0] == "gpt"))
        self.assertEqual(sum(1 for x in rev if x[0] == "claude"), 60)
        self.assertEqual(arnes.ESFUERZO_GPT, "low")
        # Por log, sus llamadas seguidas.
        plan = corrida.leer(self.base / "plan-revisores.json")["items"]
        vistos = []
        for k, _, _ in plan:
            if not vistos or vistos[-1] != k:
                self.assertNotIn(k, vistos)
                vistos.append(k)
        self.assertEqual(sorted(vistos), list(piloto3.LOGS))

        # Reanudar no vuelve a llamar.
        n = len(self.falsos.llamadas)
        piloto3.etapa_revisores(self.args(), self.base)
        self.assertEqual(len(self.falsos.llamadas), n)

        # Sin resumen de la etapa 1, la verificación no corre.
        with self.assertRaises(SystemExit):
            piloto3.etapa_verificacion(self.args(), self.base)

        piloto3.etapa_hoja_revisores(self.args(), self.base)
        hoja = (self.base / "hoja-revisores" / "PARA-CLASIFICAR.md").read_text(encoding="utf-8")
        for marca in ('"RS"', '"RD"', " RS ", " RD ", "claude", "gpt"):
            self.assertNotIn(marca, hoja)
        with self.assertRaises(SystemExit):
            piloto3.etapa_resumen_1(self.args(), self.base)  # etiquetas vacías
        self.etiquetar()
        piloto3.etapa_resumen_1(self.args(), self.base)
        r1 = corrida.leer(self.base / "resumen-etapa1.json")
        self.assertEqual(r1["por_revisor"]["RD"]["detecta_en_falsos_cierres"]["tasa"], 1.0)
        self.assertEqual(r1["por_revisor"]["RD"]["inventa_en_gemelos"]["k"], 0)
        self.assertEqual(r1["desacuerdos_con_la_marca"], [])
        self.assertTrue(r1["regla_6_1"]["pasa_a_etapa_2"])

        piloto3.etapa_verificacion(self.args(), self.base)
        ver = [x for x in self.falsos.llamadas if x[1] in ("verificacion", "regla")]
        self.assertTrue(all(x[2] == "low" for x in ver))
        n_fc = sum(1 for k in piloto3.LOGS if piloto3.es_falso_cierre(self.base, k))
        self.assertEqual(sum(1 for x in ver if x[1] == "regla"), n_fc)
        plan_v = corrida.leer(self.base / "plan-verificacion.json")["items"]
        self.assertEqual(sorted(k for k, b, _ in plan_v if b == "RR"),
                         sorted(k for k in piloto3.LOGS if piloto3.es_falso_cierre(self.base, k)))
        self.assertEqual(sum(1 for x in ver if x[1] == "verificacion"), 3 * 60)

        piloto3.etapa_hoja_verificacion(self.args(), self.base)
        piloto3.etapa_resumen_2(self.args(), self.base)
        r2 = corrida.leer(self.base / "resumen-etapa2.json")
        pb = r2["por_brazo"]
        self.assertEqual(pb["RD"]["abre_en_falsos_cierres"]["tasa"], 1.0)
        self.assertEqual(pb["R0"]["abre_en_falsos_cierres"]["tasa"], 0.0)
        self.assertEqual(pb["RR"]["abre_en_falsos_cierres"]["tasa"], 1.0)
        self.assertEqual(pb["RD"]["abre_en_gemelos"]["k"], 0)
        # El RD falso ve el hueco en todo pendiente y en ningún gemelo: abre en los 10 pares.
        self.assertEqual(r2["s_final"]["RD"]["suma"], 10)
        self.assertEqual(r2["s_final"]["R0"]["suma"], 0)
        self.assertNotIn("RR", r2["s_final"])
        self.assertFalse(r2["reglas_6_2"]["techo"])
        self.assertFalse(r2["reglas_6_2"]["segunda_pasada_sola"])
        self.assertEqual(r2["reglas_6_2"]["gemelos_con_residuo"], [])
        self.assertEqual(pb["RD"]["clases_del_residuo"].get("execution_gap/other"), pb["RD"]["abre_en_falsos_cierres"]["k"]
                         + pb["RD"]["abre_donde_ya_registraba"]["k"])

    def test_un_revisor_que_no_revisa_pide_la_decision_de_nico(self):
        piloto3.etapa_antes(self.args(), self.base)
        piloto3.etapa_revisores(self.args(), self.base)
        piloto3.etapa_hoja_revisores(self.args(), self.base)
        self.etiquetar(revisa=False)
        piloto3.etapa_resumen_1(self.args(), self.base)
        with self.assertRaises(SystemExit) as e:
            piloto3.etapa_verificacion(self.args(), self.base)
        self.assertIn("--sigue", str(e.exception))
        # Etiquetas cambiadas después del resumen: frena también.
        fe = self.base / "hoja-revisores" / "etiquetas.json"
        et = corrida.leer(fe)
        primero = sorted(et)[0]
        et[primero]["dudoso"] = True
        corrida.escribir(fe, et)
        with self.assertRaises(SystemExit) as e:
            piloto3.etapa_verificacion(self.args(sigue=True), self.base)
        self.assertIn("no coincide", str(e.exception))

    def test_una_etiqueta_incoherente_frena(self):
        piloto3.etapa_antes(self.args(), self.base)
        piloto3.etapa_revisores(self.args(), self.base)
        piloto3.etapa_hoja_revisores(self.args(), self.base)
        self.etiquetar()
        fe = self.base / "hoja-revisores" / "etiquetas.json"
        et = corrida.leer(fe)
        primero = sorted(et)[0]
        et[primero].update(detecta=True, donde="ninguno")
        corrida.escribir(fe, et)
        with self.assertRaises(SystemExit):
            piloto3.etapa_resumen_1(self.args(), self.base)

    def test_la_hoja_no_pisa_etiquetas(self):
        piloto3.etapa_antes(self.args(), self.base)
        piloto3.etapa_revisores(self.args(), self.base)
        piloto3.etapa_hoja_revisores(self.args(), self.base)
        self.etiquetar()
        antes_de_rehacer = corrida.leer(self.base / "hoja-revisores" / "etiquetas.json")
        piloto3.etapa_hoja_revisores(self.args(), self.base)
        self.assertEqual(corrida.leer(self.base / "hoja-revisores" / "etiquetas.json"), antes_de_rehacer)

    def test_las_plantillas_quedan_fijas_en_la_etapa(self):
        piloto3.etapa_antes(self.args(), self.base)
        piloto3.etapa_revisores(self.args(limite=1), self.base)
        previo = mensajes3.md5_de_las_plantillas
        try:
            mensajes3.md5_de_las_plantillas = lambda: dict(previo(), revisor="0" * 32)
            with self.assertRaises(SystemExit) as e:
                piloto3.etapa_revisores(self.args(), self.base)
            self.assertIn("cambiaron", str(e.exception))
        finally:
            mensajes3.md5_de_las_plantillas = previo

    def test_el_limite_cuenta_logs(self):
        piloto3.etapa_antes(self.args(), self.base)
        piloto3.etapa_revisores(self.args(limite=2), self.base)
        plan = corrida.leer(self.base / "plan-revisores.json")["items"]
        primeros = []
        for k, _, _ in plan:
            if k not in primeros:
                primeros.append(k)
        esperadas = sum(1 for k, _, _ in plan if k in primeros[:2])
        self.assertEqual(sum(1 for x in self.falsos.llamadas if x[1] == "revisor"), esperadas)

    def test_una_caida_del_servicio_no_gasta_el_item(self):
        piloto3.etapa_antes(self.args(), self.base)
        self.falsos.gpt_falla = True
        plan = piloto3.plan_revisores(self.base)
        k, _, c = next(x for x in plan if x[1] == "RS")
        f = piloto3.fuente()
        with self.assertRaises(SystemExit) as e:
            with piloto3.esfuerzo_gpt("high"):
                piloto3.correr_revision(self.base, {}, mensajes3.leer_plantillas(), f, k, "RS", c, {})
        self.assertIn("no contesta", str(e.exception))
        r = corrida.leer(self.base / "revisiones" / f"{k:03d}-RS-{c}" / "resumen.json")
        self.assertTrue(r["intentos"][-1]["caida"])
        self.assertTrue(r["intentos"][-1]["sin_cupo"])
        self.assertNotIn("estado", r)
        canarios = list((self.base / "canarios").glob("revisor-codex-*.json"))
        self.assertEqual(len(canarios), 1)
        # El canario corrió con el esfuerzo del revisor.
        self.assertEqual(self.falsos.llamadas[-1], ("gpt", "revisor", "high"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
