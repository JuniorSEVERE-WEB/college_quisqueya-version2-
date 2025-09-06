from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Program, Classroom

DEFAULT_CLASS_MAP = {
    Program.KINDERGARTEN: ["1e A Kinder", "2e A Kinder", "3e A Kinder"],
    Program.PRIMAIRE: ["1e AF", "2e AF", "3e AF", "4e AF", "5e AF", "6e AF"],
    Program.SECONDAIRE: ["7e AF", "8e AF", "9e AF", "NS1", "NS2", "NS3", "NS4"],
}

@receiver(post_save, sender=Program)
def create_default_classrooms(sender, instance, created, **kwargs):
    """
    À la création d'un Program, on crée automatiquement ses classrooms par défaut
    si elles n'existent pas encore pour ce programme+année.
    """
    if created:
        names = DEFAULT_CLASS_MAP.get(instance.name, [])
        for n in names:
            Classroom.objects.get_or_create(program=instance, name=n)
