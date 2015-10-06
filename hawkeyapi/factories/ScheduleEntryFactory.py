#!/usr/bin/env python
from hawkeyapi.objects import ScheduleEntry
from boto.dynamodb2.items import Item
from datetime import date
from dateutil import parser as dateparser

class ScheduleEntryFactory():
    """
    A factory for creating and manipulating things.
    """

    @classmethod
    def objectify(cls, e_db):
        """
        Turn an item into an object.
        """
        isconf = None
        if e_db['is_conference'] is not None:
            isconf = bool(e_db['is_conference'])

        return ScheduleEntry(
            str(e_db['entry_id']),
            date.fromordinal(e_db['date']),
            dateparser.parse(e_db['start_time']).time(),
            e_db['opponent'],
            e_db['site'],
            e_db['location'],
            e_db['links'],
            isconf,
            e_db['league'],
            e_db['season'],
            e_db['team_id'],
            bool(e_db['is_women']),
            bool(e_db['normal_opp']),
            bool(e_db['normal_loc']),
        )

    @classmethod
    def itemify(cls, db_table, obj):
        """
        Turn an object into an item.
        """
        return Item(
            db_table,
            data = {
                'team_id': obj.team_id,
                'entry_id': str(obj.id),
                'date': obj.date.toordinal(),
                'start_time': obj.start_time.isoformat(),
                'opponent': obj.opponent,
                'site': obj.site,
                'location': obj.location,
                'links': obj.links,
                'is_conference': obj.is_conference,
                'season': obj.season,
                'league': obj.league,
                'is_women': obj.is_women,
                'normal_loc': obj.normal_loc,
                'normal_opp': obj.normal_opp,
            },
        )
