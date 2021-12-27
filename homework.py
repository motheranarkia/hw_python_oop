class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    T_IN_MIN = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    RUN_CAL_1 = 18
    RUN_CAL_2 = 20

    def get_spent_calories(self) -> float:
        return (
            (self.RUN_CAL_1 * self.get_mean_speed()
             - self.RUN_CAL_2) * self.weight / self.M_IN_KM
            * self.duration * self.T_IN_MIN
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALK_CAL_1 = 0.035
    WALK_CAL_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (self.WALK_CAL_1 * self.weight
             + (self.get_mean_speed()**2 // self.height)
             * self.WALK_CAL_2 * self.weight)
            * (self.duration * self.T_IN_MIN)
        )


class Swimming(Training):
    """Тренировка: плавание."""
    SWIM_CAL_1 = 1.1
    SWIM_CAL_2 = 2
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP) / Training.M_IN_KM

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / Training.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.SWIM_CAL_1)
            * self.SWIM_CAL_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_and_class = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    if workout_type not in workout_type_and_class:
        raise ValueError('Ошибка данных')
    else:
        training = workout_type_and_class.get(workout_type)(*data)
        return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

for workout_type, data in packages:
    training = read_package(workout_type, data)
    main(training)
