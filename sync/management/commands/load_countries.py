from django.core.management.base import BaseCommand
import logging

logger = logging.getLogger('logger')


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            logger.info("Verificando los estados de las cuentas")
            self.actualizador.actualizar_cuentas(self.manager.all())
        except Exception as e:
            logger.exception(e)