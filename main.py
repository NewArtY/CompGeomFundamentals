from core.engine import Engine


def main():
    engine = Engine()
    engine.scene_manager.init_scenes()
    engine.run()


if __name__ == '__main__':
    main()
