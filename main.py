from core.engine import Engine
from core.scenes.static_scene import StaticABScene
from core.scenes.t_scene import MovingPointScene


def main():
    engine = Engine()

    # Добавляем первую сцену
    engine.add_scene("main", StaticABScene())
    # Добавляем вторую сцену
    engine.add_scene("trajectories", MovingPointScene())
    # Устанавливаем начальную сцену
    engine.set_scene("main")

    engine.run()


if __name__ == '__main__':
    main()
