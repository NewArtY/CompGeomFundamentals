from core.engine import Engine
from core.scene_manager import SceneManager


def main():
    engine = Engine()
    engine.scene_manager.init_scenes()
    engine.run()


if __name__ == '__main__':
    main()
