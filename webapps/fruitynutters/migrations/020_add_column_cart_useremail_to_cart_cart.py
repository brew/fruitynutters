from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('cart', 'cart', 'cart_useremail', 'varchar(60) NULL')
