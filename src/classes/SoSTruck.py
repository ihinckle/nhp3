from src.classes.SoSHashTable import SoSHashTable
from src.classes.SoSPackage import SoSPackage


class SoSTruck:
    def __init__(self):
        self._cargo = SoSHashTable(16)
        self._destinations = []

    def load(self, package: SoSPackage):
        self._cargo.insert(package.get_destination_id(), package.get_id())
        self._destinations.append(package.get_destination_id())
        package.set_delivery_status(package.DELIVERY_STATUS.EN_ROUTE.value)

    def debug(self):
        for item in self._cargo:
            print(item)
