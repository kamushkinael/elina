import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog
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
        
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_grid_to_file)
        
        self.load_button = QPushButton("Загрузить")
        self.load_button.clicked.connect(self.load_grid_from_file)
        
        control_panel.addWidget(self.start_button)
        control_panel.addWidget(self.stop_button)
        control_panel.addWidget(self.clear_button)
        control_panel.addWidget(self.random_button)
        control_panel.addWidget(self.save_button)
        control_panel.addWidget(self.load_button)
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

    def save_grid_to_file(self):
        """Сохраняет текущее состояние сетки в файл."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить сетку", "", "Текстовые файлы (*.txt)")
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    for row in self.grid:
                        file.write(''.join(map(str, row)) + '\n')
            except Exception as e:
                print(f"Ошибка при сохранении файла: {e}")

    def load_grid_from_file(self):
        """Загружает состояние сетки из файла."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Загрузить сетку", "", "Текстовые файлы (*.txt)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    new_grid = [list(map(int, list(line.strip()))) for line in file if line.strip()]
                if len(new_grid) == GRID_SIZE and all(len(row) == GRID_SIZE for row in new_grid):
                    self.grid = new_grid
                    self.canvas.update_grid(self.grid)
            except Exception as e:
                print(f"Ошибка при загрузке файла: {e}")


class GameCanvas(QWidget):
    """Поле для отрисовки клеток."""
    def __init__(self, grid):
        super().__init__()
        self.grid = grid
        self.setFixedSize(GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
        self.is_drawing = False

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
                    painter.fillRect(x, y, CELL_SIZE, CELL_SIZE, QColor(0, 128, 0))
                    painter.setPen(QColor(0, 0, 0))
                    painter.drawRect(x, y, CELL_SIZE, CELL_SIZE)

    def mouseMoveEvent(self, event):
        """Рисование или стирание клеток при движении мыши."""
        x = event.x() // CELL_SIZE
        y = event.y() // CELL_SIZE
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            if event.buttons() & Qt.LeftButton:  # ЛКМ — рисование
                self.grid[y][x] = 1
            elif event.buttons() & Qt.RightButton:  # ПКМ — стирание
                self.grid[y][x] = 0
            self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameOfLife()
    window.show()
    sys.exit(app.exec_())
