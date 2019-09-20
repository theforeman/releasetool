import os
import obal

from pkg_resources import resource_filename


class ApplicationConfig(obal.ApplicationConfig):
    """
    A class describing the where to find various files
    """

    @staticmethod
    def name():
        """
        Return the name as shown to the user in the ArgumentParser
        """
        return 'releasetool'

    @staticmethod
    def data_path():
        """
        Return the data path. Houses playbooks and configs.
        """
        return os.environ.get('OBAL_DATA', resource_filename(__name__, 'data'))

    @staticmethod
    def inventory_path():
        """
        Return the inventory path
        """
        return os.environ.get('OBAL_INVENTORY', os.path.join(os.getcwd(), 'releasetool.yaml'))


def main():
    obal.main(application_config=ApplicationConfig)


if __name__ == '__main__':
    main()
