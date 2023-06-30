from application import *


def main():
    controller = Controller(Application, ComplexCalculator)
    controller.master.run_view()


if __name__ == '__main__':
    main()