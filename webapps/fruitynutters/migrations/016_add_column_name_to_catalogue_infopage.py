from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('catalogue', 'page', 'name', 'varchar(30) NOT NULL UNIQUE')
