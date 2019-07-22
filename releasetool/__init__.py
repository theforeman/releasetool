import os
import obal

from pkg_resources import resource_filename


def _get_data_path():
    """
    Return the data path. Houses playbooks and configs.
    """
    return os.environ.get('OBAL_DATA', resource_filename(__name__, 'data'))


def get_inventory_path():
    """
    Return the inventory path
    """
    return os.environ.get('OBAL_INVENTORY', os.path.join(os.getcwd(), 'package_manifest.yaml'))


def main():
    obal._get_data_path = _get_data_path
    obal.get_inventory_path = get_inventory_path
    obal.main()


if __name__ == '__main__':
    main()
