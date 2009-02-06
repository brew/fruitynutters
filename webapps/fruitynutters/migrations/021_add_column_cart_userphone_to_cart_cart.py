from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('cart', 'cart', 'cart_userphone', 'varchar(60) NULL')
