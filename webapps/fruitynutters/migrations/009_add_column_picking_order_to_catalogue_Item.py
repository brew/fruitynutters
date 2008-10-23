from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('catalogue', 'Item', 'picking_order', 'integer NOT NULL')
