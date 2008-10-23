from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('cart', 'Cart', 'date_updated', 'date NOT NULL')
