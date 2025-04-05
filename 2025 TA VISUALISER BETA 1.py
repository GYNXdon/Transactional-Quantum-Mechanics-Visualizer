import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QCheckBox
from PyQt5.QtCore import Qt
import numpy as np
import pygame
import random

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

class QuantumSystem:
    def __init__(self, emitters, absorbers, use_probabilistic_selection=False):
        self.emitters = emitters
        self.absorbers = absorbers
        self.transactions = []
        self.state = None
        self.time = 0
        self.transaction_count = 0
        self.particles = []
        self.transaction_log = []
        self.use_probabilistic_selection = use_probabilistic_selection  # Store the toggle state

    def generate_offer_waves(self):
        for emitter in self.emitters:
            offer_wave = emitter.emit_offer_wave()
            self.transactions.append(offer_wave)

    def generate_confirmation_waves(self):
        for transaction in self.transactions:
            for absorber in self.absorbers:
                confirmation_wave = absorber.confirm(transaction)
                transaction.add_confirmation_wave(confirmation_wave)

    def select_transaction(self):
        unselected = [t for t in self.transactions if not t.selected]
        if unselected:
            weights = [t.weight for t in unselected]
            if sum(weights) == 0:
                return

            # Use probabilistic selection if enabled
            if self.use_probabilistic_selection:
                selected_transaction = random.choices(unselected, weights=weights, k=1)[0]
            else:
                selected_transaction = max(unselected, key=lambda t: t.weight)

            self.update_state(selected_transaction)
            self.spawn_particle(selected_transaction.emitter.position)
            selected_transaction.selected = True
            self.transaction_log.append((selected_transaction.emitter.position, selected_transaction.weight))
            self.transaction_count += 1

    def update_state(self, transaction):
        self.state = transaction.result_state

    def update_positions(self):
        for emitter in self.emitters:
            emitter.update_position(self.time)
        for absorber in self.absorbers:
            absorber.update_position(self.time, self.emitters)

    def calculate_total_energy(self):
        total_energy = sum(0.5 * np.linalg.norm(emitter.velocity) ** 2 for emitter in self.emitters)
        total_energy += sum(0.5 * np.linalg.norm(absorber.velocity) ** 2 for absorber in self.absorbers)
        return total_energy

    def spawn_particle(self, position):
        self.particles.append(Particle(position))

    def reset_simulation(self):
        self.transactions.clear()
        self.state = None
        self.time = 0
        self.transaction_count = 0
        self.particles.clear()
        self.transaction_log.clear()
        for emitter in self.emitters:
            emitter.reset()
        for absorber in self.absorbers:
            absorber.reset()

    def visualize(self, speed_multiplier):
        pygame.init()
        screen_width = 800
        screen_height = 600
        screen = pygame.display.set_mode((screen_width + 200, screen_height))
        pygame.display.set_caption("Transactional Interpretation of Quantum Mechanics")

        font = pygame.font.Font(None, 24)

        clock = pygame.time.Clock()
        running = True
        frame_count = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(WHITE)
            self.update_positions()
            self.generate_offer_waves()
            self.generate_confirmation_waves()

            if frame_count % 60 == 0:
                self.select_transaction()

            # Draw emitters
            for emitter in self.emitters:
                pygame.draw.circle(screen, BLUE, (int(emitter.position[0]), int(emitter.position[1])), 5)

            # Draw absorbers
            for absorber in self.absorbers:
                pygame.draw.circle(screen, RED, (int(absorber.position[0]), int(absorber.position[1])), 5)

            for transaction in self.transactions:
                if transaction.confirmation_waves:
                    pygame.draw.line(screen, GREEN, 
                                     (int(transaction.emitter.position[0]), int(transaction.emitter.position[1])),
                                     (int(transaction.confirmation_waves[0].absorber.position[0]), int(transaction.confirmation_waves[0].absorber.position[1])),
                                     1)
                    for confirmation in transaction.confirmation_waves:
                        pygame.draw.line(screen, RED, 
                                         (int(confirmation.absorber.position[0]), int(confirmation.absorber.position[1])),
                                         (int(transaction.emitter.position[0]), int(transaction.emitter.position[1])),
                                         1)

            transaction_count_text = font.render(f"Transaction Count: {self.transaction_count}", True, BLACK)
            screen.blit(transaction_count_text, (10, 10))

            total_energy_text = font.render(f"Total Energy: {self.calculate_total_energy():.2f}", True, BLACK)
            screen.blit(total_energy_text, (10, 40))

            for particle in self.particles[:]:
                particle.age += 1
                if particle.age > particle.lifespan:
                    self.particles.remove(particle)
                    continue
                pygame.draw.circle(screen, YELLOW, (int(particle.position[0]), int(particle.position[1])), 5)

            # Timeline log on the side
            pygame.draw.rect(screen, (230, 230, 230), (800, 0, 200, 600))
            screen.blit(font.render("Transaction Log", True, BLACK), (810, 10))
            for i, (pos, weight) in enumerate(self.transaction_log[-25:]):
                log_text = f"{i+1}: w={weight:.1f}"
                screen.blit(font.render(log_text, True, BLACK), (810, 30 + i * 20))

            pygame.display.flip()
            clock.tick(int(60 * speed_multiplier))
            frame_count += 1

        pygame.quit()

class Emitter:
    def __init__(self, position, velocity):
        self.initial_position = np.array(position, dtype=float)
        self.initial_velocity = np.array(velocity, dtype=float)
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.offer_wave = None

    def emit_offer_wave(self):
        self.offer_wave = OfferWave(self)
        return self.offer_wave

    def update_position(self, time):
        self.position += self.velocity
        if self.position[0] < 0 or self.position[0] > 800:
            self.velocity[0] *= -1
        if self.position[1] < 0 or self.position[1] > 600:
            self.velocity[1] *= -1

    def reset(self):
        self.position = self.initial_position.copy()
        self.velocity = self.initial_velocity.copy()

class Absorber:
    def __init__(self, position, velocity):
        self.initial_position = np.array(position, dtype=float)
        self.initial_velocity = np.array(velocity, dtype=float)
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)

    def confirm(self, offer_wave):
        return ConfirmationWave(self, offer_wave)

    def update_position(self, time, emitters):
        self.position += self.velocity
        if self.position[0] < 0 or self.position[0] > 800:
            self.velocity[0] *= -1
        if self.position[1] < 0 or self.position[1] > 600:
            self.velocity[1] *= -1

    def reset(self):
        self.position = self.initial_position.copy()
        self.velocity = self.initial_velocity.copy()

class OfferWave:
    def __init__(self, emitter):
        self.emitter = emitter
        self.confirmation_waves = []
        self.weight = 0
        self.result_state = None
        self.selected = False

    def add_confirmation_wave(self, confirmation_wave):
        self.confirmation_waves.append(confirmation_wave)
        self.calculate_weight()
        self.result_state = self.determine_result_state()

    def calculate_weight(self):
        self.weight = sum(cw.weight for cw in self.confirmation_waves)

    def determine_result_state(self):
        return f"Result from {self.emitter}"

class ConfirmationWave:
    def __init__(self, absorber, offer_wave):
        self.absorber = absorber
        self.offer_wave = offer_wave
        self.weight = self.calculate_weight()

    def calculate_weight(self):
        return 1

class Particle:
    def __init__(self, position):
        self.position = np.array(position, dtype=float)
        self.age = 0
        self.lifespan = 180

class SimulationGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Quantum Simulation Control Panel")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Adjust Simulation Parameters"))

        layout.addWidget(QLabel("Emitter Velocity"))
        self.emitter_velocity_slider = QSlider(Qt.Horizontal)
        self.emitter_velocity_slider.setMinimum(1)
        self.emitter_velocity_slider.setMaximum(10)
        self.emitter_velocity_slider.setValue(5)
        layout.addWidget(self.emitter_velocity_slider)

        layout.addWidget(QLabel("Absorber Velocity"))
        self.absorber_velocity_slider = QSlider(Qt.Horizontal)
        self.absorber_velocity_slider.setMinimum(1)
        self.absorber_velocity_slider.setMaximum(10)
        self.absorber_velocity_slider.setValue(5)
        layout.addWidget(self.absorber_velocity_slider)

        self.probabilistic_checkbox = QCheckBox("Use Probabilistic Transaction Selection")
        layout.addWidget(self.probabilistic_checkbox)

        self.start_button = QPushButton("Start Simulation")
        self.start_button.clicked.connect(self.start_simulation)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def start_simulation(self):
        emitter_velocity = self.emitter_velocity_slider.value()
        absorber_velocity = self.absorber_velocity_slider.value()
        use_probabilistic_selection = self.probabilistic_checkbox.isChecked()

        emitters = [Emitter((np.random.rand() * 800, np.random.rand() * 600),
                            ((np.random.rand() - 0.5) * emitter_velocity, (np.random.rand() - 0.5) * emitter_velocity))
                    for _ in range(5)]
        absorbers = [Absorber((np.random.rand() * 800, np.random.rand() * 600),
                              ((np.random.rand() - 0.5) * absorber_velocity, (np.random.rand() - 0.5) * absorber_velocity))
                     for _ in range(5)]

        system = QuantumSystem(emitters, absorbers, use_probabilistic_selection)
        system.visualize(speed_multiplier=1.0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = SimulationGUI()
    gui.show()
    sys.exit(app.exec_())
