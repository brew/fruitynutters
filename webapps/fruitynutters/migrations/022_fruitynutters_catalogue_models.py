from dmigrations.mysql import migrations as m
import datetime
migration = m.Migration(sql_up=["""
    CREATE TABLE `catalogue_virtualshoppage` (
        `page_ptr_id` integer NOT NULL PRIMARY KEY,
        `shopPdf` varchar(100) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
"""], sql_down=["""
    DROP TABLE `catalogue_virtualshoppage`;
"""])
