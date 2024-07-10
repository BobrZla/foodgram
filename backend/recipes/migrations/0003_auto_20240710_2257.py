# Generated by Django 3.2.3 on 2024-07-10 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(help_text='Картинка рецепта.', upload_to='recipes/', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RecipeIngredient', to='recipes.ingredient', verbose_name='Ингредиент из рецепта'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RecipeIngredient', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
