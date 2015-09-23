#!/usr/bin/env python
from hawkeyapi.objects import Season
from boto.dynamodb2.items import Item

class SeasonFactory():
    """
    A factory for creating and manipulating things.
    """

    @classmethod
    def objectify(cls, e_db):
        """
        Turn an item into an object.
        """
        return Season(
            e_db['id'],
            e_db['league'],
            int(e_db['start']),
            int(e_db['end']),
            bool(e_db['is_women']),
        )

    @classmethod
    def itemify(cls, db_table, obj):
        """
        Turn an object into an item.
        """
        return Item(
            db_table,
            data = {
                'id': obj.id,
                'league': obj.league,
                'start': obj.start_year,
                'end': obj.end_year,
                'is_women': obj.is_women,
            },
        )
