import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QPainter


# Константы для игры
GRID_SIZE = 50  # Размер сетки (количество клеток по горизонтали и вертикали)
CELL_SIZE = 10  # Размер клетки в пикселях
DELAY = 100  # Задержка между поколениями в миллисекундах


class GameOfLife(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Игра Жизнь - PyQt5")
        self.setFixedSize(GRID_SIZE * CELL_SIZE + 200, GRID_SIZE * CELL_SIZE + 20)

        # Статус игры
        self.running = False

        # Сетка для игры
        self.grid = self.create_random_grid()

        # Таймер для обновления игры
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)

        # Основной макет
        main_layout = QHBoxLayout()

        # Поле для игры
        self.canvas = GameCanvas(self.grid)
        main_layout.addWidget(self.canvas)

        # Панель управления
        control_panel = QVBoxLayout()
        self.start_button = QPushButton("Старт")
        self.start_button.clicked.connect(self.start_game)
        
        self.stop_button = QPushButton("Стоп")
        self.stop_button.clicked.connect(self.stop_game)
        
        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_grid)
        
        self.random_button = QPushButton("Случайно")
        self.random_button.clicked.connect(self.randomize_grid)
        
        control_panel.addWidget(self.start_button)
        control_panel.addWidget(self.stop_button)
        control_panel.addWidget(self.clear_button)
        control_panel.addWidget(self.random_button)
        control_panel.addStretch()
        
        main_layout.addLayout(control_panel)
        self.setLayout(main_layout)

    def create_random_grid(self):
        """Создаёт случайную сетку."""
        return [[random.choice([0, 1]) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def clear_grid(self):
        """Очищает сетку."""
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.canvas.update_grid(self.grid)

    def randomize_grid(self):
        """Заполняет сетку случайными значениями."""
        self.grid = self.create_random_grid()
        self.canvas.update_grid(self.grid)

    def get_neighbors(self, row, col):
        """Считает количество живых соседей для клетки."""
        neighbors = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:  # Пропустить саму клетку
                    continue
                r = (row + dr) % GRID_SIZE  # Обход границ
                c = (col + dc) % GRID_SIZE
                neighbors += self.grid[r][c]
        return neighbors

    def update_grid(self):
        """Обновляет сетку по правилам игры."""
        new_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                alive = self.grid[row][col]
                neighbors = self.get_neighbors(row, col)

                if alive == 1 and (neighbors == 2 or neighbors == 3):  # Клетка выживает
                    new_grid[row][col] = 1
                elif alive == 0 and neighbors == 3:  # Новая клетка рождается
                    new_grid[row][col] = 1
                # В противном случае клетка остаётся мёртвой
        self.grid = new_grid

    def step(self):
        """Шаг симуляции игры."""
        if self.running:
            self.update_grid()
            self.canvas.update_grid(self.grid)

    def start_game(self):
        """Запускает игру."""
        if not self.running:
            self.running = True
            self.timer.start(DELAY)

    def stop_game(self):
        """Останавливает игру."""
        self.running = False
        self.timer.stop()


class GameCanvas(QWidget):
    """Поле для отрисовки клеток."""
    def __init__(self, grid):
        super().__init__()
        self.grid = grid
        self.setFixedSize(GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)

    def update_grid(self, grid):
        """Обновляет внутреннюю сетку и перерисовывает холст."""
        self.grid = grid
        self.update()

    def paintEvent(self, event):
        """Отрисовка всех живых клеток."""
        painter = QPainter(self)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] == 1:  # Живая клетка
                    x = col * CELL_SIZE
                    y = row * CELL_SIZE
                    painter.fillRect(x, y, CELL_SIZE, CELL_SIZE, QColor(0, 128, 0))  # Зелёный цвет для живых клеток
                    painter.setPen(QColor(0, 0, 0))
                    painter.drawRect(x, y, CELL_SIZE, CELL_SIZE)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameOfLife()
    window.show()
    sys.exit(app.exec_())
