import abc


class GameObject(abc.ABC):

    @abc.abstractmethod
    def update(self):
        """
        обновляет внутреннее состояние объекта
        запускается на каждом шаге игрового цикла (но это не точно, может быть в draw засунем)
        """
        pass

    @abc.abstractmethod
    def draw(self):
        """
        отображает объект на экране
        запускается на каждом шаге игрового цикла
        """
        pass
