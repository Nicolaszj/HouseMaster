import csv
from decimal import Decimal # Importamos Decimal para manejar el precio
from django.core.management.base import BaseCommand
from property.models import Property # Correcto # Asegúrate que esta sea la ruta correcta a tu app

class Command(BaseCommand):
    help = 'Importa propiedades desde un archivo CSV a nuestro modelo real'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='La ruta del archivo CSV a importar.')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']
        self.stdout.write(self.style.SUCCESS(f'Iniciando importación desde "{csv_file_path}"...'))
        
        # Para que `update_or_create` funcione de manera fiable, te recomiendo
        # añadir `unique=True` al campo 'address' en tu `models.py` y correr migraciones.
        
        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Opcional: Limpia la tabla antes de importar
                # Property.objects.all().delete()
                # self.stdout.write(self.style.WARNING('Se han eliminado las propiedades existentes.'))

                for row in reader:
                    # Usamos update_or_create para evitar duplicados. Requiere un campo único como `address`.
                    propiedad, created = Property.objects.update_or_create(
                        address=row['address'],
                        defaults={
                            'title': row['title'],
                            'description': row['description'],
                            # Cambio clave: Convertimos el precio a Decimal
                            'price': Decimal(row['price']), 
                            'type': row['type'],
                            'area': float(row['area']),
                            'rooms': int(row['rooms']),
                            'bathrooms': int(row['bathrooms']),
                            'status': row['status'],
                            'city': row['city'],
                            'department': row['department'],
                            # El campo 'image' se omite intencionalmente, ya que es un ImageField
                            # y no se puede llenar directamente con un texto de ruta desde el CSV.
                        }
                    )
                    
                    if created:
                        self.stdout.write(f"  - Creada: '{propiedad.title}'")
                    else:
                        self.stdout.write(f"  - Actualizada: '{propiedad.title}'")

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Error: El archivo "{csv_file_path}" no fue encontrado.'))
            return
        
        self.stdout.write(self.style.SUCCESS('¡Importación completada exitosamente!'))