from django.core.management.base import BaseCommand, CommandError

from subjects.models import Subject


class Command(BaseCommand):
    help = 'Delete all comments for the given post.'

    def add_arguments(self, parser):
        parser.add_argument('subject_codes', nargs='+', type=str)

    def handle(self, *args, **options):
        for subject_code in options['subject_codes']:
            try:
                subject = Subject.objects.get(code=subject_code)

            except Subject.DoesNotExist:
                raise CommandError(f'Post #{subject.code} does not exist')

            subject.comments.delete()

            self.stdout.write(
                self.style.SUCCESS('Successfully deleted all comments for post #{post.pk}')
            )
