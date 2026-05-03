from core.di_container import DiContainer
from ui.app import App


def main() -> None:
    di_container = DiContainer()
    di_container.database.initialize_tables()
    di_container.logger.info("Starting sccli...")

    app = App(di_container=di_container)
    app.run()


if __name__ == "__main__":
    main()
