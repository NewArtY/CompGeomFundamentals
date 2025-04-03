class TimedSpawner:
    def __init__(self, interval, max_count):
        self.interval = interval  # Интервал между спавном (в кадрах)
        self.max_count = max_count  # Максимальное количество объектов
        self.current_frame = 0
        self.is_active = True

    def update(self, current_count):
        if not self.is_active:
            return False

        self.current_frame += 1
        if self.current_frame >= self.interval:
            self.current_frame = 0
            if current_count < self.max_count:
                return True
            else:
                self.is_active = False  # Отключаем спавнер
        return False
