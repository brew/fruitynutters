from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('catalogue', 'item', 'order_name', 'varchar(60) NOT NULL')
