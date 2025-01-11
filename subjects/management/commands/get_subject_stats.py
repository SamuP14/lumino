from django.core.management.base import BaseCommand
from django.db.models import Avg

from subjects.models import Enrollment, Subject


class Command(BaseCommand):
    help = 'Displays the average grades of all subjects'

    def handle(self, *args, **kwargs):
        subjects = Subject.objects.all()
        for subject in subjects:
            enrollments = Enrollment.objects.filter(subject=subject).exclude(mark__isnull=True)

            if enrollments.exists():
                average = enrollments.aggregate(Avg('mark'))['mark__avg']
            else:
                average = 0

            self.stdout.write(f'{subject.code}: {average:.2f}')
