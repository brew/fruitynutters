from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('cart', 'cart', 'cart_username', 'varchar(60) NULL')
