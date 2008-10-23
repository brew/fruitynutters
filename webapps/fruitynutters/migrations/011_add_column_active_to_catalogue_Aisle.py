from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('catalogue', 'Aisle', 'active', 'bool NOT NULL')
