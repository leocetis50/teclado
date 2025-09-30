import flet as ft
from flet_audio import Audio
import threading

# --Normalizar teclas--
def normalizar_tecla(k: str) -> str:
    k = (k or "").lower()
    if k == "space":
        return " "
    return k.replace(" ","").replace("-","")

#---Mostrar nota--

def mostrar_nota_visual(pagina, teclado, label,nombre_nota, texto_mostrar, recursos, teclado_bace):
    img_url = recursos.get(nombre_nota, {}).get("img")
    if not img_url:
        return
    teclado.str = img_url
    label.value = f"🎶🎵{texto_mostrar}🎵🎶"
    label.visible = True
    pagina.update()

    def resetear():
        teclado.str = teclado_bace
        label.visible = False
        pagina.update()
    threading.Timer(1.5, resetear).start()

#---Recursos y configuracon---

Recursos = {
    "Do":  {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Do.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Do.wav"},
    "Re":  {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Re.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Re.wav"},
    "Mi":  {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Mi.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Mi.wav"},
    "Fa":  {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Fa.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Fa.wav"},
    "Sol": {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Sol.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Sol.wav"},
    "La":  {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/La.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/La.wav"},
    "Si":  {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Si.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Si.wav"},
    "Do2": {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Do2.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Do2.wav"},
}

TECLADO_BACE = "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Teclado.png"

NOTAS = [
    {"nombre":"Do",  "mostrar": "Do",  "teclas": ["z"]},
    {"nombre":"Re",  "mostrar": "Re",  "teclas": ["x"]},
    {"nombre":"Mi",  "mostrar": "Mi",  "teclas": ["c"]},
    {"nombre":"Fa",  "mostrar": "Fa",  "teclas": ["v"]},
    {"nombre":"Sol", "mostrar": "Sol", "teclas": ["b"]},
    {"nombre":"La",  "mostrar": "La",  "teclas": ["n"]},
    {"nombre":"Si",  "mostrar": "Si",  "teclas": ["","m"]},
    {"nombre":"Do2", "mostrar": "Do2", "teclas": ["arrowright","arrow right", "arrow-right"]},
    
]

def main(page: ft.Page):
    #--Ventana--
    page.title = "Piano Virtual"
    page.bgcolor = ft.Colors.PURPLE_ACCENT_700
    page.window_width = 800
    page.window_height = 600
    page.window_resizable = False
    page.padding = 0
    page.spacing = 0

    #--Controles back--
    teclado = ft.Image(src=TECLADO_BACE, width=800, height=400)
    nota_label = ft.Text(
        value="",
        size=50,
        color="yellow",
        weight="bold",
        text_align="center",
        visible=False,
    )

    #--Layout: label arriba, teclado abajo--
    page.add(
        ft.Column(
            [
                ft.Container(
                    content=nota_label,alignment=ft.alignment.center,height=200,),
                    teclado,
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=10,
        )

    )    
    #--Mapa tecla-normalizada -> {nombre, mostrar}--
    tecla_a_nota = {}
    for n in NOTAS:
        for t in n["teclas"]:
            tecla_a_nota[normalizar_tecla(t)] = {"nombre": n["nombre"],"mostrar": n["mostrar"],}

    #Un reporductor de audio por nota, agregado al overlay de la pagina
    nombre_a_audio = {}
    for nombre, urls in Recursos.items():
        reproductor = Audio(src=urls["wav"])
        nombre_a_audio[nombre] = reproductor
        page.overlay.append(reproductor)

    #--Evento presionar tecla--
    def la_precionar_tecla(evento: ft.KeyboardEvent):
        tecla_norm = normalizar_tecla(evento.key)
        nota_info = tecla_a_nota.get(tecla_norm)
        if not nota_info:
            return
        nombre_nota = nota_info["nombre"]
        texto_mostrar = nota_info["mostrar"]

        reproductor = nombre_a_audio.get(nombre_nota)
        if reproductor:
            reproductor.play()
            mostrar_nota_visual(
                page, teclado, nota_label,
                nombre_nota, texto_mostrar,
                  Recursos, TECLADO_BACE
            )

    page.on_keyboard_event = la_precionar_tecla
    page.update()

ft.app(target=main,)
