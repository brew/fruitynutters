from dmigrations.mysql import migrations as m
import datetime
migration = m.Migration(sql_up=["""
    CREATE TABLE `cart_cart` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `date_created` date NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    CREATE TABLE `cart_cartitem` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `cart_id` integer NOT NULL,
        `product_id` integer NOT NULL,
        `quantity` integer NOT NULL,
        `cart_bundle_id` integer NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    ALTER TABLE `cart_cartitem` ADD CONSTRAINT cart_id_refs_id_c970e5a FOREIGN KEY (`cart_id`) REFERENCES `cart_cart` (`id`);
""", """
    ALTER TABLE `cart_cartitem` ADD CONSTRAINT product_id_refs_id_73a2a46b FOREIGN KEY (`product_id`) REFERENCES `catalogue_item` (`id`);
""", """
    CREATE TABLE `cart_cartbundle` (
        `cart_ptr_id` integer NOT NULL PRIMARY KEY
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    ALTER TABLE `cart_cartbundle` ADD CONSTRAINT cart_ptr_id_refs_id_5231f7f FOREIGN KEY (`cart_ptr_id`) REFERENCES `cart_cart` (`id`);
""", """
    ALTER TABLE `cart_cartitem` ADD CONSTRAINT cart_bundle_id_refs_cart_ptr_id_7caeda34 FOREIGN KEY (`cart_bundle_id`) REFERENCES `cart_cartbundle` (`cart_ptr_id`);
"""], sql_down=["""
    ALTER TABLE `cart_cartitem` DROP FOREIGN KEY cart_bundle_id_refs_cart_ptr_id_7caeda34;
""", """
    DROP TABLE `cart_cartbundle`;
""", """
    DROP TABLE `cart_cartitem`;
""", """
    DROP TABLE `cart_cart`;
"""])
