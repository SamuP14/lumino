from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Delete all comments for the given post.'

    def add_arguments(self, parser):
        parser.add_argument('subject_codes', nargs='+', type=str)

    def handle(self, *args, **options):
        for subject_code in options['subject_codes']:
            try:
                pass
            except:
                raise CommandError()
