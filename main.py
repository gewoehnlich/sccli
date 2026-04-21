from core.di_container import DiContainer
from core.shell import Shell


def main() -> None:
    di_container: DiContainer = DiContainer()
    di_container.database.initialize_tables()

    shell = Shell(commands=di_container.commands)
    shell.run()


if __name__ == "__main__":
    main()
