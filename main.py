from core.engine import Engine
from core.scenes.static_scene import StaticABScene
from core.scenes.t_scene import MovingPointScene
from core.scenes.test_scene import TestScene
from core.scenes.transformation_scene import TransformationScene


def main():
    engine = Engine()

    # Добавляем первую сцену
    engine.add_scene("main", StaticABScene())
    # Добавляем последующие сцены (потребуется менеджер сцен)
    engine.add_scene("trajectories", MovingPointScene())
    engine.add_scene("transformation", TransformationScene())
    engine.add_scene("test", TestScene())
    # Устанавливаем начальную сцену
    engine.set_scene("main")

    engine.run()


if __name__ == '__main__':
    main()
