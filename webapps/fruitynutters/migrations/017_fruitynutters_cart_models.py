from dmigrations.mysql import migrations as m
import datetime
migration = m.Migration(sql_up=["""
    CREATE TABLE `cart_cartwriteinitem` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `cart_id` integer NOT NULL,
        `name` varchar(140) NOT NULL,
        `code` varchar(20) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
"""], sql_down=["""
    DROP TABLE `cart_cartwriteinitem`;
"""])
