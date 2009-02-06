from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('cart', 'cart', 'cart_comment', 'longtext NULL')
