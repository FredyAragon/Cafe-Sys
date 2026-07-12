from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_promotions_imageurl_alter_promotions_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='order',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.CASCADE,
                related_name='reviews',
                to='core.orders',
                db_column='order_id',
            ),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='product',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.CASCADE,
                related_name='reviews',
                to='core.products',
                db_column='product_id',
            ),
        ),
    ]