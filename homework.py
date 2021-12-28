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
    TIME_IN_MIN = 60

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
    RUN_MULTIPLICATION = 18
    RUN_DEDUCTION = 20

    def get_spent_calories(self) -> float:
        return (
            (self.RUN_MULTIPLICATION * self.get_mean_speed()
             - self.RUN_DEDUCTION) * self.weight / self.M_IN_KM
            * self.duration * self.TIME_IN_MIN
        )
        # все мои длинные строки перенесены так же, как и те,
        #         # что приводятся в пример, разве нет?
        # Вот, четыре отступа, все в одну линию. Не понимаю, что править.


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    HEIGHT_MULTIPLICATION = 0.029
    WEIGHT_MULTIPLICATION = 0.035

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
            (self.WEIGHT_MULTIPLICATION * self.weight
             + (self.get_mean_speed()**2 // self.height)
             * self.HEIGHT_MULTIPLICATION * self.weight)
            * (self.duration * self.TIME_IN_MIN)
        )


class Swimming(Training):
    """Тренировка: плавание."""
    ADD_CAL_FACTOR = 1.1
    CAL_MULTIPLIER = 2
    LEN_STEP = 1.38

    def __init__(
            self, action: int, duration: float, weight: float,
            length_pool: float, count_pool: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self):
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.ADD_CAL_FACTOR)
            * self.CAL_MULTIPLIER * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_and_class = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }

    if workout_type in workout_type_and_class:
        training = workout_type_and_class.get(workout_type)(*data)
        return training
    else:
        raise ValueError('Неожиданный тип тренировки')


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
        training: Training = read_package(workout_type, data)
        main(training)
