import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from property.models import Property, PropertyImage

class Command(BaseCommand):
    help = 'Importa propiedades desde un archivo CSV, incluyendo agente e imágenes.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='La ruta del archivo CSV a importar.')
        parser.add_argument(
            '--agent', type=str, help='Username del agente al que se asignarán las propiedades.', required=True
        )

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']
        agent_username = options['agent']

        try:
            agent_user = User.objects.get(username=agent_username)
            self.stdout.write(f"Propiedades se asignarán al agente: '{agent_user.username}'")
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Error: El usuario agente '{agent_username}' no fue encontrado. Créalo primero."))
            return

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                propiedad, created = Property.objects.update_or_create(
                    address=row['address'],
                    defaults={ 'agent': agent_user, 'title': row['title'], 'description': row['description'], 'price': Decimal(row['price']), 'type': row['type'], 'area': float(row['area']), 'rooms': int(row['rooms']), 'bathrooms': int(row['bathrooms']), 'status': row['status'], 'city': row['city'], 'department': row['department'], }
                )

                image_files = [img.strip() for img in row['image'].split(',') if img.strip()]
                if image_files:
                    propiedad.image = f'{image_files[0]}'
                    propiedad.save()
                    propiedad.images.all().delete()
                    is_first = True
                    for image_name in image_files:
                        PropertyImage.objects.create( property=propiedad, image=f'{image_name}', is_cover=is_first )
                        is_first = False
                if created: self.stdout.write(f"  - CREADA: '{propiedad.title}'")
        self.stdout.write(self.style.SUCCESS('¡Importación completada!'))