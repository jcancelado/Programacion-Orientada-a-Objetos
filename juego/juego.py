import pygame
import sys
import random
import math
import threading
import time

# ============================================================
# CONFIGURACIÓN Y CONSTANTES
# ============================================================
ANCHO = 1080
ALTO = 720
FPS = 60

# Colores (R, G, B)
BLANCO = (255, 255, 255)
NEGRO = (10, 10, 15)
ROJO = (230, 50, 50)
VERDE = (50, 200, 80)
AZUL = (50, 100, 230)
CIAN = (0, 255, 255)  # Para mensajes de defensa
GRIS = (50, 50, 50)
GRIS_CLARO = (180, 180, 180)
AMARILLO = (255, 215, 0)
PURPURA = (140, 50, 200)

# Rutas (Puedes editar estas rutas. Si fallan, el juego usará cuadros de colores)
RUTAS_IMAGENES = {
    "Lux": r"C:/Users/Estudiante/Documents/Programacion Orientada a Objetos/juego/img/lux.png",
    "Yasuo": r"C:/Users/Estudiante/Documents/Programacion Orientada a Objetos/juego/img/yasuo.png",
    "Ezreal": r"C:/Users/Estudiante/Documents/Programacion Orientada a Objetos/juego/img/Ezreal.png",
    "Jinx": r"C:/Users/Estudiante/Documents/Programacion Orientada a Objetos/juego/img/jinx.png",
    "Poppy": r"C:/Users/Estudiante/Documents/Programacion Orientada a Objetos/juego/img/poppy.png",
    "Caitlyn": r"C:/Users/Estudiante/Documents/Programacion Orientada a Objetos/juego/img/caytlin.png"
}

# Inicializar Pygame
pygame.init()
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("League of Pygame - Duelo por Turnos (Con Threads)")
RELOJ = pygame.time.Clock()

# Fuentes
FUENTE_GRANDE = pygame.font.SysFont("Arial", 50, bold=True)
FUENTE_MEDIANA = pygame.font.SysFont("Arial", 30, bold=True)
FUENTE_PEQUENA = pygame.font.SysFont("Arial", 18)

# ============================================================
# THREADING: SISTEMA DE AMBIENTE EN SEGUNDO PLANO
# ============================================================
# Usamos un Lock para evitar que el hilo escriba en la lista 
# al mismo tiempo que el juego intenta leerla para dibujar.
LOCK_PARTICULAS = threading.Lock()

class HiloAmbiente(threading.Thread):
    """
    Hilo que calcula posiciones de particulas de ambiente (lucérnagas/magia)
    en segundo plano para no cargar el bucle principal.
    """
    def __init__(self):
        super().__init__()
        self.daemon = True  # El hilo muere cuando se cierra el juego
        self.particulas = []
        self.activo = True

    def run(self):
        while self.activo:
            with LOCK_PARTICULAS:
                # 1. Generar nuevas partículas aleatoriamente
                if len(self.particulas) < 50:
                    self.particulas.append({
                        'x': random.randint(0, ANCHO),
                        'y': random.randint(0, ALTO),
                        'vx': random.uniform(-0.5, 0.5),
                        'vy': random.uniform(-0.5, -1.5), # Flotan hacia arriba
                        'radio': random.randint(1, 3),
                        'color': (random.randint(100, 200), random.randint(200, 255), 255),
                        'alpha': random.randint(100, 255)
                    })

                # 2. Actualizar posiciones
                for p in self.particulas[:]:
                    p['x'] += p['vx']
                    p['y'] += p['vy']
                    p['alpha'] -= 1 # Desvanecer
                    
                    if p['y'] < 0 or p['alpha'] <= 0:
                        self.particulas.remove(p)
            
            # Simular carga de trabajo o espera para no saturar CPU
            time.sleep(0.02) 

# Instancia global del generador de ambiente
ambiente_bg = HiloAmbiente()

# ============================================================
# SISTEMA DE CARGA DE RECURSOS (SEGURO)
# ============================================================
def cargar_imagen(nombre, color_reserva):
    """Intenta cargar la imagen, si falla, crea un cuadro con el nombre."""
    ruta = RUTAS_IMAGENES.get(nombre, "")
    try:
        img = pygame.image.load(ruta).convert_alpha()
        img = pygame.transform.scale(img, (150, 150)) # Estandarizar tamaño
        return img
    except (FileNotFoundError, pygame.error):
        # Crear imagen placeholder si falla
        surf = pygame.Surface((150, 150))
        surf.fill(color_reserva)
        pygame.draw.rect(surf, BLANCO, (0,0,150,150), 4)
        texto = FUENTE_PEQUENA.render(nombre, True, NEGRO)
        surf.blit(texto, (75 - texto.get_width()//2, 75 - texto.get_height()//2))
        return surf

# ============================================================
# CLASES DE EFECTOS VISUALES
# ============================================================
class TextoFlotante:
    def __init__(self, x, y, texto, color=ROJO, tamaño=30):
        self.x = x
        self.y = y
        self.texto = texto
        self.color = color
        self.alpha = 255
        self.font = pygame.font.SysFont("Arial", tamaño, bold=True)
        self.vida = 80  # frames

    def update(self):
        self.y -= 1.0  # Flotar hacia arriba lento
        self.vida -= 1
        if self.vida < 20:
            self.alpha -= 12  # Desvanecer

    def draw(self, surface):
        if self.vida > 0 and self.alpha > 0:
            text_surf = self.font.render(self.texto, True, self.color)
            text_surf.set_alpha(self.alpha)
            surface.blit(text_surf, (self.x, self.y))

class Particula:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.vida = random.randint(20, 40)
        self.color = color
        self.radio = random.randint(3, 6)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.radio *= 0.9  # Hacerse más pequeño
        self.vida -= 1

    def draw(self, surface):
        if self.vida > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radio))

# ============================================================
# CLASES DE UI (BOTONES)
# ============================================================
class Boton:
    def __init__(self, x, y, w, h, texto, color_base, color_hover, accion=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.color_base = color_base
        self.color_hover = color_hover
        self.accion = accion
        self.hovered = False

    def update(self, eventos):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.hovered and self.accion:
                    self.accion()

    def draw(self, surface):
        color = self.color_hover if self.hovered else self.color_base
        # Sombra
        pygame.draw.rect(surface, (20, 20, 20), (self.rect.x+3, self.rect.y+3, self.rect.w, self.rect.h), border_radius=8)
        # Botón
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, BLANCO, self.rect, 2, border_radius=8)
        
        txt = FUENTE_MEDIANA.render(self.texto, True, BLANCO)
        surface.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))

# ============================================================
# MODELO DE PERSONAJES
# ============================================================
class Personaje:
    def __init__(self, nombre, color_tema, max_vida, daño_base):
        self.nombre = nombre
        self.image = cargar_imagen(nombre, color_tema)
        self.max_vida = max_vida
        self.vida = max_vida
        self.daño_base = daño_base
        self.cooldowns = {}
        
        # Animación y Posición
        self.origen_x = 0
        self.origen_y = 0
        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(0, 0, 150, 150)
        self.anim_timer = 0
        self.estado_anim = "IDLE" # IDLE, ATAQUE, REGRESO

    def set_pos(self, x, y):
        self.origen_x = x
        self.origen_y = y
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def update(self):
        # Interpolación simple para animaciones
        if self.estado_anim == "ATAQUE":
            # Moverse hacia adelante
            direccion = 1 if self.origen_x < ANCHO/2 else -1
            objetivo = self.origen_x + (200 * direccion)
            self.x += (objetivo - self.x) * 0.2
            if abs(self.x - objetivo) < 5:
                self.estado_anim = "REGRESO"
        elif self.estado_anim == "REGRESO":
            self.x += (self.origen_x - self.x) * 0.1
            if abs(self.x - self.origen_x) < 2:
                self.x = self.origen_x
                self.estado_anim = "IDLE"
        
        self.rect.topleft = (self.x, self.y)

    def atacar(self, objetivo):
        self.estado_anim = "ATAQUE"
        spread = max(1, int(self.daño_base * 0.2))
        daño = random.randint(self.daño_base - spread, self.daño_base + spread)
        
        es_critico = False
        texto_especial = ""

        if random.random() < 0.15: # Crítico genérico
            daño = int(daño * 1.8)
            es_critico = True

        # Lógica polimórfica de ataque
        daño, texto_especial = self.habilidad_especial_ataque(daño)
        
        # Lógica polimórfica de defensa
        daño_final, razon_mitigacion = objetivo.defender(daño)
        
        objetivo.recibir_daño(daño_final)
        
        # Retornamos todo para que la UI lo muestre
        return daño_final, es_critico, texto_especial, razon_mitigacion

    def recibir_daño(self, cantidad):
        self.vida = max(0, self.vida - cantidad)

    def defender(self, daño):
        """Retorna (daño_final, texto_explicativo)"""
        return self.habilidad_especial_defensa(daño)

    # Métodos para sobreescribir
    def habilidad_especial_ataque(self, daño): 
        return daño, ""
    
    def habilidad_especial_defensa(self, daño): 
        return daño, ""

class Jinx(Personaje):
    def habilidad_especial_ataque(self, daño):
        if random.random() < 0.25:
            return int(daño * 1.5), "¡COHETE!"
        return daño, ""

class Yasuo(Personaje):
    def habilidad_especial_defensa(self, daño):
        # Yasuo tiene probabilidad de bloquear TODO el daño
        if random.random() < 0.15:
            return 0, "¡MURO DE VIENTO!"
        return daño, ""

class Lux(Personaje):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.escudo_cd = 0

    def habilidad_especial_defensa(self, daño):
        if self.escudo_cd == 0:
            self.escudo_cd = 3
            absorb = int(daño * 0.5)
            return daño - absorb, f"¡ESCUDO! (-{absorb})"
        if self.escudo_cd > 0: self.escudo_cd -= 1
        return daño, ""

class Ezreal(Personaje):
    def habilidad_especial_ataque(self, daño):
        if random.random() < 0.2:
            return 0, "¡Falla Skillshot!"
        return daño + 10, ""

class Poppy(Personaje):
    def habilidad_especial_defensa(self, daño):
        # Poppy siempre reduce daño un poco por ser tanque
        reducido = int(daño * 0.2)
        return daño - reducido, "¡PIEL DE HIERRO!"

class Caitlyn(Personaje):
    def habilidad_especial_ataque(self, daño):
        if random.random() < 0.4:
            return int(daño * 1.7), "¡Headshot!"
        return daño, ""

# ============================================================
# GESTOR DEL JUEGO (Game Loop principal)
# ============================================================
class Juego:
    def __init__(self):
        self.escena = "SELECCION" # SELECCION, PELEA, VICTORIA
        self.jugador1 = None
        self.jugador2 = None
        self.turno = 1
        self.efectos = [] # Textos y partículas
        self.botones = []
        
        # Iniciar el Hilo de Ambiente (Background)
        if not ambiente_bg.is_alive():
            ambiente_bg.start()
        
        # Crear plantilla de personajes
        self.roster = [
            Lux("Lux", AMARILLO, 100, 15),
            Yasuo("Yasuo", GRIS_CLARO, 120, 14),
            Ezreal("Ezreal", AZUL, 105, 16),
            Jinx("Jinx", PURPURA, 95, 18),
            Poppy("Poppy", VERDE, 150, 10),
            Caitlyn("Caitlyn", ROJO, 100, 15)
        ]
        
        self.crear_interfaz_seleccion()
        self.shake_timer = 0

    def crear_interfaz_seleccion(self):
        self.botones = []
        x_inicial = 150
        y_inicial = 200
        col = 0
        row = 0
        
        for i, pj in enumerate(self.roster):
            if i > 0 and i % 3 == 0:
                row += 1
                col = 0
            
            x = x_inicial + col * 280
            y = y_inicial + row * 220
            
            # Crear un botón invisible sobre la imagen para detectar clics
            b = Boton(x, y + 160, 150, 40, "Elegir", GRIS, AZUL, 
                     accion=lambda idx=i: self.seleccionar_personaje(idx))
            self.botones.append(b)
            col += 1

    def seleccionar_personaje(self, indice):
        clase = self.roster[indice]
        # Clonar personaje
        nuevo = type(clase)(clase.nombre, (100,100,100), clase.max_vida, clase.daño_base)
        # Reasignar imagen (se pierde al clonar con type)
        nuevo.image = clase.image 
        
        if not self.jugador1:
            self.jugador1 = nuevo
        elif not self.jugador2:
            self.jugador2 = nuevo
            self.iniciar_pelea()

    def iniciar_pelea(self):
        self.escena = "PELEA"
        self.botones = []
        
        # Posicionar jugadores
        self.jugador1.set_pos(150, 350)
        self.jugador2.set_pos(ANCHO - 300, 350)
        
        # Botones de acción
        btn_atk = Boton(ANCHO//2 - 100, 600, 200, 60, "¡ATACAR!", ROJO, (255, 100, 100), self.accion_atacar)
        btn_reset = Boton(ANCHO - 150, 20, 130, 40, "Reiniciar", GRIS, GRIS_CLARO, self.reset_game)
        self.botones = [btn_atk, btn_reset]

    def accion_atacar(self):
        if self.jugador1.estado_anim != "IDLE" or self.jugador2.estado_anim != "IDLE":
            return # Esperar animaciones

        atacante = self.jugador1 if self.turno == 1 else self.jugador2
        defensor = self.jugador2 if self.turno == 1 else self.jugador1
        
        # Calcular daño y lógica (Ahora recibe la razón de mitigación)
        daño, crit, special, mitigacion = atacante.atacar(defensor)
        
        # Generar efectos visuales
        pos_txt_x = defensor.x + 75
        pos_txt_y = defensor.y
        
        # 1. Mostrar texto de mitigación si existe (ej: "Muro de viento")
        if mitigacion:
            self.efectos.append(TextoFlotante(pos_txt_x, pos_txt_y - 50, mitigacion, CIAN, 25))

        # 2. Mostrar Daño
        if daño == 0 and not mitigacion:
            # Caso especial: falla ataque (ezreal) sin defensa activa
            pass 
        else:
            if daño == 0:
                pass # Ya mostramos mitigacion arriba
            else:
                color_dmg = AMARILLO if crit else BLANCO
                tam_dmg = 60 if crit else 40
                self.efectos.append(TextoFlotante(pos_txt_x, pos_txt_y, f"-{daño}", color_dmg, tam_dmg))
                
                # Sangre/Chispas
                for _ in range(15):
                    self.efectos.append(Particula(defensor.x + 75, defensor.y + 75, ROJO))

                if crit:
                    self.shake_timer = 10 # Vibrar pantalla

        # 3. Mostrar texto de habilidad ofensiva (ej: "Cohete")
        if special:
            self.efectos.append(TextoFlotante(pos_txt_x - 50, pos_txt_y - 80, special, PURPURA, 25))

        # Verificar victoria
        if defensor.vida <= 0:
            self.escena = "VICTORIA"
            self.botones = [Boton(ANCHO//2 - 100, 500, 200, 50, "Jugar de nuevo", VERDE, AZUL, self.reset_game)]
        else:
            self.turno = 2 if self.turno == 1 else 1

    def reset_game(self):
        self.jugador1 = None
        self.jugador2 = None
        self.turno = 1
        self.escena = "SELECCION"
        self.efectos = []
        self.crear_interfaz_seleccion()

    def draw_health_bar(self, surface, x, y, actual, maximo, color):
        ancho_barra = 250
        alto_barra = 25
        ratio = actual / maximo
        
        # Fondo gris
        pygame.draw.rect(surface, (40, 40, 40), (x, y, ancho_barra, alto_barra))
        # Vida actual
        pygame.draw.rect(surface, color, (x, y, ancho_barra * ratio, alto_barra))
        # Borde
        pygame.draw.rect(surface, BLANCO, (x, y, ancho_barra, alto_barra), 2)
        
        txt = FUENTE_PEQUENA.render(f"{actual}/{maximo}", True, BLANCO)
        surface.blit(txt, (x + ancho_barra//2 - txt.get_width()//2, y + 2))

    def run(self):
        while True:
            eventos = pygame.event.get()
            for event in eventos:
                if event.type == pygame.QUIT:
                    ambiente_bg.activo = False # Apagar hilo
                    pygame.quit()
                    sys.exit()

            # Update logic
            for btn in self.botones:
                btn.update(eventos)
            
            for fx in self.efectos[:]:
                fx.update()
                if hasattr(fx, 'vida') and fx.vida <= 0:
                    self.efectos.remove(fx)

            if self.shake_timer > 0:
                self.shake_timer -= 1
                shake_x = random.randint(-5, 5)
                shake_y = random.randint(-5, 5)
            else:
                shake_x, shake_y = 0, 0

            # Dibujado
            PANTALLA.fill(NEGRO) # Limpiar pantalla
            
            # Fondo genérico degradado
            for i in range(ALTO):
                color = (20, 20 + (i//15), 40)
                pygame.draw.line(PANTALLA, color, (0, i), (ANCHO, i))

            surface_juego = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

            # --- DIBUJAR HILO DE AMBIENTE ---
            # Adquirimos el lock para leer la lista de particulas segura
            with LOCK_PARTICULAS:
                for p in ambiente_bg.particulas:
                    color_con_alpha = (*p['color'], int(p['alpha']))
                    # Dibujar circulo con alpha (requiere surface especial en pygame, simplificamos)
                    # Pygame draw circle no soporta alpha directo facil, usamos circle sólido pequeño
                    pygame.draw.circle(surface_juego, p['color'], (int(p['x']), int(p['y'])), p['radio'])
            # --------------------------------

            if self.escena == "SELECCION":
                titulo = FUENTE_GRANDE.render("SELECCIONA TUS CAMPEONES", True, BLANCO)
                surface_juego.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
                
                if self.jugador1:
                    info = FUENTE_MEDIANA.render(f"Jugador 1: {self.jugador1.nombre}", True, AZUL)
                    surface_juego.blit(info, (50, 120))
                else:
                    info = FUENTE_MEDIANA.render("Jugador 1: Eligiendo...", True, GRIS_CLARO)
                    surface_juego.blit(info, (50, 120))
                
                # Dibujar parrilla de personajes
                x_inicial = 150
                y_inicial = 200
                col = 0
                row = 0
                for i, pj in enumerate(self.roster):
                    if i > 0 and i % 3 == 0:
                        row += 1
                        col = 0
                    x = x_inicial + col * 280
                    y = y_inicial + row * 220
                    
                    surface_juego.blit(pj.image, (x, y))
                    nombre = FUENTE_MEDIANA.render(pj.nombre, True, BLANCO)
                    surface_juego.blit(nombre, (x + 75 - nombre.get_width()//2, y - 30))
                    
                    stats = FUENTE_PEQUENA.render(f"HP:{pj.max_vida} ATK:{pj.daño_base}", True, GRIS_CLARO)
                    surface_juego.blit(stats, (x + 75 - stats.get_width()//2, y + 155))
                    col += 1

            elif self.escena == "PELEA" or self.escena == "VICTORIA":
                # Actualizar y Dibujar personajes
                self.jugador1.update()
                self.jugador2.update()
                
                surface_juego.blit(self.jugador1.image, self.jugador1.rect)
                # Jugador 2 invertido (mirando a izquierda)
                img_j2 = pygame.transform.flip(self.jugador2.image, True, False)
                surface_juego.blit(img_j2, self.jugador2.rect)
                
                # UI Barras
                self.draw_health_bar(surface_juego, 50, 50, self.jugador1.vida, self.jugador1.max_vida, VERDE)
                self.draw_health_bar(surface_juego, ANCHO - 300, 50, self.jugador2.vida, self.jugador2.max_vida, ROJO)
                
                nombre1 = FUENTE_MEDIANA.render(self.jugador1.nombre, True, BLANCO)
                nombre2 = FUENTE_MEDIANA.render(self.jugador2.nombre, True, BLANCO)
                surface_juego.blit(nombre1, (50, 20))
                surface_juego.blit(nombre2, (ANCHO - 300, 20))
                
                # Indicador de turno
                if self.escena == "PELEA":
                    txt_turno = f"TURNO: {'JUGADOR 1' if self.turno == 1 else 'JUGADOR 2'}"
                    col_turno = AZUL if self.turno == 1 else ROJO
                    lbl = FUENTE_GRANDE.render(txt_turno, True, col_turno)
                    surface_juego.blit(lbl, (ANCHO//2 - lbl.get_width()//2, 100))

            if self.escena == "VICTORIA":
                ganador = self.jugador1.nombre if self.jugador1.vida > 0 else self.jugador2.nombre
                overlay = pygame.Surface((ANCHO, ALTO))
                overlay.set_alpha(150)
                overlay.fill(NEGRO)
                surface_juego.blit(overlay, (0,0))
                
                txt_vic = FUENTE_GRANDE.render(f"¡VICTORIA PARA {ganador}!", True, AMARILLO)
                surface_juego.blit(txt_vic, (ANCHO//2 - txt_vic.get_width()//2, ALTO//2 - 100))

            # Dibujar botones
            for btn in self.botones:
                btn.draw(surface_juego)

            # Dibujar efectos (sobre todo lo demas)
            for fx in self.efectos:
                fx.draw(surface_juego)

            # Aplicar shake y dibujar en pantalla final
            PANTALLA.blit(surface_juego, (shake_x, shake_y))
            
            pygame.display.flip()
            RELOJ.tick(FPS)

if __name__ == "__main__":
    juego = Juego()
    juego.run()