from django.core.management.base import BaseCommand, CommandError

from newsportal.models import Post, Category


class Command(BaseCommand):
    help= 'Удаление новостей категории'
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = False

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('category', nargs='+', type=str)


    def handle(self, *args, **options):

        self.stdout.readable()
        self.stdout.write(f'Вы уверены что желаете удалить посты категорий {", ".join(options["category"])} ? ДА/НЕТ')

        answer = input()

        if answer == 'ДА':

            for category in options['category']:

                category_obj = Category.objects.get(category=category)

                posts = Post.objects.filter(category=category_obj)

                if posts:
                    posts.delete()
                    print(f'Были удалены посты категории {category}')
                else:
                    print(f'Постов категории {category} нет в базе')

        elif answer == 'НЕТ':
            print('ответ нет')
        else:
            print('ответ не ясен')