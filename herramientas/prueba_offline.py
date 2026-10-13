"""Pruebas del arnés que no llaman a ningún modelo (protocolo v7, §7).

Corren contra las salidas guardadas del piloto y contra carpetas armadas a mano.
Se corren antes de gastar cupo, después de cada cambio a herramientas/:

    python -I experimento\\herramientas\\prueba_offline.py
"""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import arnes  # noqa: E402
import piloto  # noqa: E402

PILOTO = arnes.PILOTO


class Stderr(unittest.TestCase):
    def test_rechazos_de_la_prueba_08(self):
        se = arnes.revisar_stderr((PILOTO / "arnes" / "sandbox-desde-claude-code.stderr.txt").read_bytes())
        self.assertEqual(len(se["shell_rechazados"]), 3)
        self.assertEqual(len(se["parches_rechazados"]), 2)

    def test_rechazos_de_la_prueba_09(self):
        for k in ("000", "001"):
            se = arnes.revisar_stderr((PILOTO / "generador-solo-lectura" / k / "intento-1-stderr.txt").read_bytes())
            self.assertEqual((len(se["shell_rechazados"]), len(se["parches_rechazados"])), (0, 1))


class SinCupo(unittest.TestCase):
    VACIO = {"turno_fallido": None, "errores": []}

    def test_salidas_guardadas_no_son_cupo(self):
        rutas = [PILOTO / "arnes" / "sandbox-desde-claude-code.stderr.txt"]
        rutas += [PILOTO / "generador-solo-lectura" / k / "intento-1-stderr.txt" for k in ("000", "001")]
        for ruta in rutas:
            self.assertFalse(arnes.sin_cupo(self.VACIO, ruta.read_bytes()), ruta)

    def test_un_comando_rechazado_que_dice_429_no_es_cupo(self):
        linea = (b"2026-10-13T17:04:35Z ERROR codex_core::tools::router: error=exec_command failed: "
                 b"Set-Content log.md -Value 'HTTP 429 Too Many Requests, quota exceeded' rejected: blocked by policy")
        self.assertFalse(arnes.sin_cupo(self.VACIO, linea))

    def test_turno_fallido_por_limite_es_cupo(self):
        ev = {"turno_fallido": "You've hit your usage limit. Try again later.", "errores": []}
        self.assertTrue(arnes.sin_cupo(ev, b""))

    def test_linea_de_error_que_no_es_de_herramienta_es_cupo(self):
        self.assertTrue(arnes.sin_cupo(self.VACIO, b"ERROR codex_core::client: 429 Too Many Requests"))


class Comando(unittest.TestCase):
    def test_sujeto_en_solo_lectura_y_con_su_shell(self):
        c = arnes.comando_codex_exec("codex.exe", "salida.md")
        self.assertEqual(c[c.index("-s") + 1], "read-only")
        self.assertNotIn("--disable", c)

    def test_generador_escribe_solo_en_su_carpeta_y_sin_shell(self):
        c = arnes.comando_codex_exec("codex.exe", "salida.md", generador=True)
        self.assertEqual(c[c.index("-s") + 1], "workspace-write")
        self.assertEqual(c[c.index("--disable") + 1], "shell_tool")
        for clave in ("exclude_tmpdir_env_var=true", "exclude_slash_tmp=true", "network_access=false"):
            self.assertIn(f"sandbox_workspace_write.{clave}", c)

    def test_lo_comun_no_cambia(self):
        a = arnes.comando_codex_exec("codex.exe", "salida.md")
        b = arnes.comando_codex_exec("codex.exe", "salida.md", generador=True)
        for flag in ("--ephemeral", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--json"):
            self.assertIn(flag, a)
            self.assertIn(flag, b)
        self.assertEqual(a[a.index("-m") + 1], b[b.index("-m") + 1])


class Generador(unittest.TestCase):
    def setUp(self):
        self.raiz = Path(tempfile.mkdtemp())
        self.trabajo = self.raiz / "trabajo"
        self.trabajo.mkdir()
        self.destino = self.raiz / "destino"

    def tearDown(self):
        shutil.rmtree(self.raiz)

    def test_los_dos_archivos(self):
        (self.trabajo / "log_ab12.md").write_bytes(b"[09:14:22] TOOL CALL\n")
        (self.trabajo / "log_ab12_metadata.json").write_bytes(b'{"log_file": "log_ab12.md"}\n')
        archivos = piloto.recoger_carpeta(self.trabajo, self.destino)
        self.assertEqual(sorted(a["ruta"] for a in archivos), ["log_ab12.md", "log_ab12_metadata.json"])
        self.assertEqual(list(self.trabajo.iterdir()), [])
        self.assertEqual((self.destino / "log_ab12.md").read_bytes(), b"[09:14:22] TOOL CALL\n")
        self.assertEqual(piloto.estado_generador(archivos, "Listo."), "archivos")

    def test_subcarpeta_y_extras_se_recogen_pero_no_son_archivos(self):
        (self.trabajo / "sub").mkdir()
        (self.trabajo / "sub" / "log_x.md").write_bytes(b"x")
        (self.trabajo / "notas.txt").write_bytes(b"y")
        archivos = piloto.recoger_carpeta(self.trabajo, self.destino)
        self.assertEqual(sorted(a["ruta"] for a in archivos), ["notas.txt", "sub/log_x.md"])
        self.assertEqual(list(self.trabajo.iterdir()), [])
        self.assertEqual(piloto.estado_generador(archivos, "nada"), "sin_log")

    def test_dos_logs_no_son_archivos(self):
        archivos = [{"ruta": "log_a.md"}, {"ruta": "log_b.md"}, {"ruta": "log_a_metadata.json"}]
        self.assertEqual(piloto.estado_generador(archivos, None), "sin_log")

    def test_log_impreso_con_su_metadata(self):
        texto = 'File 1\n[09:14] TOOL RESULT {not json}\nFile 2\n```json\n{"final_question": "Was it {x}?"}\n```'
        self.assertEqual(piloto.estado_generador([], texto), "mensaje")

    def test_las_excusas_de_la_prueba_09_son_sin_log(self):
        for k in ("000", "001"):
            texto = (PILOTO / "generador-solo-lectura" / k / "ultimo-mensaje.md").read_bytes().decode("utf-8")
            self.assertEqual(piloto.estado_generador([], texto), "sin_log")

    def test_dentro_de(self):
        self.assertTrue(piloto.dentro_de("log_a.md", self.trabajo))
        self.assertTrue(piloto.dentro_de(self.trabajo / "log_a.md", self.trabajo))
        self.assertFalse(piloto.dentro_de(self.raiz / "fuera.txt", self.trabajo))
        self.assertFalse(piloto.dentro_de("../fuera.txt", self.trabajo))


if __name__ == "__main__":
    unittest.main(verbosity=2)
