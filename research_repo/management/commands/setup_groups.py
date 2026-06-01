from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Set up user groups and permissions for the research repository'

    def handle(self, *args, **options):
        groups_permissions = {
            'Faculty': ['add_publication', 'change_publication', 'delete_publication', 'view_publication'],
            'Peer Reviewer': ['view_publication'],
            'Guest': []
        }

        for group_name, perms in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {group_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Group already exists: {group_name}'))

            # Clear existing permissions
            group.permissions.clear()

            # Add new permissions
            for perm_codename in perms:
                try:
                    perm = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(perm)
                    self.stdout.write(self.style.SUCCESS(f'Added permission "{perm_codename}" to group "{group_name}"'))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permission not found: {perm_codename}'))