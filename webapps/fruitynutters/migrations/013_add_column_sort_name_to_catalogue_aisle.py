from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('catalogue', 'aisle', 'sort_name', 'varchar(60) NOT NULL')