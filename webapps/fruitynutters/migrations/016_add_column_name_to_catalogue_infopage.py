from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('catalogue', 'infopage', 'name', 'varchar(30) NOT NULL UNIQUE')
