class KalmanFilter:
    """
    Простая реализация 1D Калман-фильтра для сглаживания ADC значений.
    """

    def __init__(self, process_variance, measurement_variance):
        self.process_variance = process_variance  # Q: насколько быстро может меняться значение
        self.measurement_variance = measurement_variance  # R: насколько шумный сигнал
        self.estimated_value = 0.0  # начальное значение
        self.error_covariance = 1.0  # P: ошибка оценки

    def update(self, measurement: float) -> float:
        """
        Обновляет внутреннее состояние фильтра и возвращает сглаженное значение.

        Args:
            measurement (float): Сырое значение с АЦП (0–255).

        Returns:
            float: Сглаженное значение.
        """
        # Prediction update
        self.error_covariance += self.process_variance

        # Measurement update
        kalman_gain = self.error_covariance / (self.error_covariance + self.measurement_variance)
        self.estimated_value += kalman_gain * (measurement - self.estimated_value)
        self.error_covariance *= (1 - kalman_gain)

        return self.estimated_value
