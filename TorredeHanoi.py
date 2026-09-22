"""

Simulação 3D da Torre de Hanói (N-Discos, K-Pinos)

Instituição: Universidade Federal do Rio de Janeiro (UFRJ)
Curso: Engenharia Eletrônica e de Computação
Autor: Arthur Correa Cunningham Neves

Descrição:
Renderiza uma visualização 3D generalizada para k-pinos utilizando o algoritmo de Frame-Stewart.
Implementa objetos compostos (compound) para visualização precisa da rotação e controles
de interface para manipulação da velocidade em tempo real.

"""

import math
import time
import colorsys
import sys
from typing import List, Tuple
from vpython import canvas, color, vector, box, cylinder, compound, rate, slider, wtext, cross, norm

# ==========================================
# 1. PARÂMETROS DO USUÁRIO
# ==========================================
NUM_DISKS: int = 5
NUM_PEGS: int = 3
ANIMATION_SPEED: float = 15.0

try:
    assert isinstance(NUM_DISKS, int) and NUM_DISKS >= 1, "Discos devem ser um inteiro >= 1."
    assert isinstance(NUM_PEGS, int) and NUM_PEGS >= 3, "Pinos devem ser um inteiro >= 3."
except AssertionError as erro:
    print(f"[ERRO DE CONFIGURAÇÃO] {erro}")
    sys.exit(1)

# ==========================================
# 2. CONSTANTES GEOMÉTRICAS ADAPTATIVAS
# ==========================================
MAX_DISK_RADIUS: float = 2.0
MIN_DISK_RADIUS: float = 0.5
DISK_HEIGHT: float = 0.5
PEG_SPACING: float = MAX_DISK_RADIUS * 2.2

# Variável global para rastrear teclas pressionadas (WASD)
pressed_keys = set()

# ==========================================
# 3. NÚCLEO MATEMÁTICO
# ==========================================
def solve_hanoi(n: int, source: int, target: int, aux_pegs: List[int]) -> List[Tuple[int, int]]:
    if n == 0: return []
    if n == 1: return [(source, target)]
    k = len(aux_pegs) + 2 #quantidade de pinos atualmente utilizáveis naquele nível específico da recursão

    if k == 3:
        return (solve_hanoi(n - 1, source, aux_pegs[0], [target]) +
                [(source, target)] +
                solve_hanoi(n - 1, aux_pegs[0], target, [source]))

    if k == 4:
        m = n - round(math.sqrt(2 * n + 1)) + 1
    else:
        m = n // 2

    m = max(1, min(m, n - 1))
    moves = solve_hanoi(m, source, aux_pegs[0], aux_pegs[1:] + [target])
    moves += solve_hanoi(n - m, source, target, aux_pegs[1:])
    moves += solve_hanoi(m, aux_pegs[0], target, aux_pegs[1:] + [source])
    return moves

# ==========================================
# 4. CONTROLO DE CÂMARA LIVRE (WASD + C)
# ==========================================
def update_camera(scene_obj):
    """Lê as teclas ativas e move a câmara no espaço 3D usando vetores."""
    if not pressed_keys:
        return

    # --- INÍCIO DO SNIPPET (Centralização) ---
    if 'c' in pressed_keys:
        # Recalcula os centros geométricos globais
        center_x = (NUM_PEGS - 1) * PEG_SPACING / 2
        peg_height = NUM_DISKS * DISK_HEIGHT + 3

        # Restaura o foco (center) e a posição (pos) originais da câmara
        scene_obj.center = vector(center_x, peg_height / 2.5, 0)
        scene_obj.camera.pos = vector(center_x, peg_height * 0.8, (NUM_PEGS * PEG_SPACING) * 0.8 + 6)

        # Remove a tecla do set para libertar a câmara no frame seguinte
        pressed_keys.discard('c')
        return
    # --- FIM DO SNIPPET ---

    # Extrai a direção para onde a câmara está a olhar e o vetor lateral
    cam_axis = norm(scene_obj.camera.axis)
    cam_right = norm(cross(cam_axis, vector(0, 1, 0)))

    cam_speed = 0.3
    move_vec = vector(0, 0, 0)

    if 'w' in pressed_keys: move_vec += cam_axis * cam_speed
    if 's' in pressed_keys: move_vec -= cam_axis * cam_speed
    if 'a' in pressed_keys: move_vec -= cam_right * cam_speed
    if 'd' in pressed_keys: move_vec += cam_right * cam_speed
    if ' ' in pressed_keys: move_vec.y += cam_speed
    if 'shift' in pressed_keys: move_vec.y -= cam_speed
    scene_obj.camera.pos += move_vec
    scene_obj.center += move_vec

# ==========================================
# 5. INICIALIZAÇÃO DA CENA 3D
# ==========================================
def init_scene() -> Tuple[List[vector], List[List[compound]], float, canvas]:
    # 1. Cálculos de dimensão primeiro
    center_x = (NUM_PEGS - 1) * PEG_SPACING / 2
    peg_height = NUM_DISKS * DISK_HEIGHT + 3

    # 2. Injeção do CSS para centralizar no navegador
    css_center = """<style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 2vh;
            font-family: sans-serif;
        }
        #glowscript { text-align: center; }
    </style>"""

    scene_title = css_center + f"<b>Torre de Hanói 3D</b><br>N={NUM_DISKS} | Pinos={NUM_PEGS} | <b>Movimento:</b> WASD + Mouse (Botao direito e Arraste) | <b>C:</b> Centrar"
    # 3. Criação da janela única
    scene = canvas(title=scene_title,
                   width=1280, height=720,
                   background=color.gray(0.1))

    # 4. Ajustes de Câmera
    scene.center = vector(center_x, peg_height / 2.5, 0)
    scene.camera.pos = vector(center_x, peg_height * 0.8, (NUM_PEGS * PEG_SPACING) * 0.8 + 6)

    # 5. Eventos de Teclado (WASD)
    def keydown(evt): pressed_keys.add(evt.key.lower())
    def keyup(evt): pressed_keys.discard(evt.key.lower())

    scene.bind('keydown', keydown)
    scene.bind('keyup', keyup)

    # 6. Controles de Interface (Slider)
    scene.append_to_caption('\n\n<b>Velocidade da Animação:</b> ')

    def on_slider_change(s):
        global ANIMATION_SPEED
        ANIMATION_SPEED = s.value
        speed_text.text = f" {ANIMATION_SPEED:.1f}x"

    slider(min=1, max=100, value=ANIMATION_SPEED, length=400, bind=on_slider_change)
    speed_text = wtext(text=f" {ANIMATION_SPEED:.1f}x")
    scene.append_to_caption('\n')

    # 7. Construção da Base e Pinos
    base_width = (NUM_PEGS - 1) * PEG_SPACING + MAX_DISK_RADIUS * 3
    box(pos=vector(center_x, -DISK_HEIGHT/2, 0),
        size=vector(base_width, DISK_HEIGHT, MAX_DISK_RADIUS * 3),
        color=vector(0.4, 0.2, 0.1))

    positions = [vector(i * PEG_SPACING, 0, 0) for i in range(NUM_PEGS)]
    state: List[List[compound]] = [[] for _ in range(NUM_PEGS)]

    for pos in positions:
        cylinder(pos=pos, axis=vector(0, peg_height, 0), radius=0.15, color=color.white)

    # 8. Construção dos Discos
    for i in range(NUM_DISKS):
        disk_index = NUM_DISKS - i - 1
        radius = MIN_DISK_RADIUS + (MAX_DISK_RADIUS - MIN_DISK_RADIUS) * (disk_index / (NUM_DISKS - 1)) if NUM_DISKS > 1 else MAX_DISK_RADIUS
        r, g, b = colorsys.hsv_to_rgb(i / NUM_DISKS, 1.0, 1.0)
        base_cyl = cylinder(pos=vector(0, -DISK_HEIGHT/2, 0), axis=vector(0, DISK_HEIGHT, 0),
                            radius=radius, color=vector(r, g, b))

        marker_thickness = 0.1
        m1 = box(pos=vector(radius - marker_thickness/2, 0, 0),
                 size=vector(marker_thickness, DISK_HEIGHT * 1.02, marker_thickness * 3), color=color.white)
        m2 = box(pos=vector(-radius + marker_thickness/2, 0, 0),
                 size=vector(marker_thickness, DISK_HEIGHT * 1.02, marker_thickness * 3), color=color.white)
        d = compound([base_cyl, m1, m2])
        d.pos = positions[0] + vector(0, i * DISK_HEIGHT + DISK_HEIGHT/2, 0)

        state[0].append(d)

    return positions, state, peg_height, scene

# ==========================================
# 6. MOTOR DE ANIMAÇÃO
# ==========================================
def animate_move(source_idx: int, target_idx: int,
                 positions: List[vector], state: List[List[compound]],
                 peg_height: float, scene_obj: canvas) -> None:
    global ANIMATION_SPEED
    try:
        disk = state[source_idx].pop()
    except IndexError:
        return

    target_x = positions[target_idx].x
    target_y = len(state[target_idx]) * DISK_HEIGHT + DISK_HEIGHT/2
    frame_rate = 60
    # Subida
    while disk.pos.y < peg_height + 1:
        rate(frame_rate)
        update_camera(scene_obj) # Checa o teclado em tempo real durante a animação
        step = 0.1 * ANIMATION_SPEED
        disk.pos.y += step
        disk.rotate(angle=step * 0.2, axis=vector(0, 1, 0), origin=disk.pos)

    # Movimento Lateral
    direction = 1 if target_x > disk.pos.x else -1
    while (target_x - disk.pos.x) * direction > 0:
        rate(frame_rate)
        update_camera(scene_obj)
        step = 0.1 * ANIMATION_SPEED
        disk.pos.x += step * direction
        disk.rotate(angle=step * 0.2, axis=vector(0, 1, 0), origin=disk.pos)

    disk.pos.x = target_x

    # Descida
    while disk.pos.y > target_y:
        rate(frame_rate)
        update_camera(scene_obj)
        step = 0.1 * ANIMATION_SPEED
        disk.pos.y -= step
        disk.rotate(angle=step * 0.2, axis=vector(0, 1, 0), origin=disk.pos)

    disk.pos.y = target_y
    state[target_idx].append(disk)

# ==========================================
# 7. EXECUÇÃO PRINCIPAL
# ==========================================
def main():
    print(f"[{time.strftime('%H:%M:%S')}] Calculando movimentação lógica...")
    pegs_indices = list(range(NUM_PEGS))
    moves = solve_hanoi(NUM_DISKS, 0, NUM_PEGS - 1, pegs_indices[1:-1])

    positions, state, peg_height, scene_obj = init_scene()
    print(f"[{time.strftime('%H:%M:%S')}] Pressione WASD na aba do navegador para voar pelo espaço!")

    # Loop não-bloqueante para substituir o time.sleep(2) e já permitir usar o WASD
    for _ in range(120): # ~2 segundos
        rate(60)
        update_camera(scene_obj)

    try:
        # Loop da resolução da torre
        for source, target in moves:
            animate_move(source, target, positions, state, peg_height, scene_obj)

        print(f"[{time.strftime('%H:%M:%S')}] Resolução concluída! Continue voando pelo cenário com WASD.")

        # Loop infinito ao fim da simulação para manter a câmera livre funcional
        while True:
            rate(60)
            update_camera(scene_obj)

    except KeyboardInterrupt:
        print("\n[AVISO] Simulação interrompida.")

if __name__ == "__main__":
    main()
