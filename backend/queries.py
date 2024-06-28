from aiohttp import web
from utils import pre_serialize, serialize_decimal, likely_missed
from typing import Tuple
import json
import copy


class ProductReader:

    def __init__(self, query):
        self.query = query

    async def __call__(self, request):
        pool = request.app['pool']
        product = request.match_info.get('product', None)
        if product is None:
            return web.json_response(
                {'status': 202,
                 'results': []}
            )
        # init connection from the pool
        async with pool.acquire() as conn:
            # start transaction
            async with conn.transaction():
                product = product.lower()
                result = await conn.fetch(
                    self.query,
                    '%'+product+'%'
                )
                if not product.endswith('.ico') \
                        and not bool(result)\
                        and not likely_missed(product):
                    # пополняем базу продуктов для клаулера
                    await conn.execute(
                        f"""INSERT INTO coming_products(name) VALUES('{product}')
                        ON CONFLICT DO NOTHING
                        """
                    )

                return web.Response(
                    text=json.dumps(await pre_serialize(result),
                                    ensure_ascii=False,
                                    default=serialize_decimal,
                                    indent=4)
                )


get_product_info = ProductReader(
    """
    WITH chosen AS (
        SELECT
        *
        FROM
        products
        WHERE
        name LIKE $1
        OR
        description LIKE $1
    )
    SELECT
    name,
    MAX(price) AS max_price,
    (
        SELECT
        ARRAY_AGG(DISTINCT(shop))
        FROM
        chosen
        WHERE
        price = (
            SELECT MAX(price) FROM chosen
        )
    ) AS max_price_shop,
    MIN(price) AS min_price,
    (
        SELECT
        ARRAY_AGG(DISTINCT(shop))
        FROM 
        chosen
        WHERE
        price = (
            SELECT MIN(price) FROM chosen
        )
    ) AS min_price_shop,
    AVG(price) AS avg_price,
    MIN(img) AS img,
    MAX(description) AS desc
    FROM 
    chosen
    GROUP BY
    name
    """
)  # !!! важно， что один и тот же продукт может присутствовать в разных объемах и единицах - это надо как-то детектить


# get_product_info = ProductReader(
#     """
#     WITH chosen AS (
#         SELECT
#         *
#         FROM products
#         WHERE
#         name LIKE $1
#         OR
#         description LIKE $1
#     )
#     SELECT
#     name,
#     JSON_AGG(
#         JSON_BUILD_OBJECT(
#             'shop', shop,
#             'price', price,
#             'price_unit', price_unit,
#             'volume', volume,
#             'volume_unit', volume_unit,
#             'description', description,
#             'img', img
#         )
#     ),
#     MAX(price) AS max_price,
#     (SELECT shop FROM chosen WHERE price = (SELECT MAX(price) FROM chosen)) AS max_price_shop,
#     MIN(price) AS min_price,
#     AVG(price) AS avg_price,
#     MIN(img) AS img
#     FROM chosen
#     GROUP BY
#     name
#     ;
#     """
# )

# get_product_info = ProductReader(
#     """
#     SELECT
#     name,
#     JSON_AGG(
#     JSON_BUILD_OBJECT(
#     'shop', shop,
#     'price', price,
#     'price_unit', price_unit,
#     'volume', volume,
#     'volume_unit', volume_unit,
#     'description', description,
#     'img', img
#     )
#     ) AS values,
#     MAX(price) AS max_price,
#     (SELECT shop FROM chosen WHERE price = max_price) AS max_price_shop,
#     MIN(price) AS min_price,
#     AVG(price) AS avg_price,
#     MIN(img) AS img
#     FROM
#     (
#     SELECT *
#     FROM products
#     WHERE
#     name LIKE $1
#     OR
#     description LIKE $1
#     ) AS chosen
#     GROUP BY name
#     ;"""
# )
# https://stackoverflow.com/questions/34163209/postgres-aggregate-two-columns-into-one-item