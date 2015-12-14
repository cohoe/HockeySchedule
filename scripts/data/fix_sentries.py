#!/usr/bin/env python

from hawkeyapi.database import Teams, ScheduleEntries, Seasons, TeamAltnames, Locations, LocationAltnames
from hawkeyapi.factories import TeamFactory, SeasonFactory, ScheduleEntryFactory, LocationFactory
import traceback

team_entries = [
    #Teams.get_item(id='NCAA-Harvard-W'),
    Teams.get_item(id='NCAA-BC-W'),
    #Teams.get_item(id='NCAA-UConn-W'),
]

#team_entries = Teams.scan(is_women__eq=True, league__eq='NCAA')
team_entries = Teams.query_2(
    index='ConferenceIndex',
    home_conference__eq='CHA',
    is_women__eq=True,
)

s_db = Seasons.get_item(id='NCAA-1415-W')
s_obj = SeasonFactory.objectify(s_db)


for t_db in team_entries:
    t_obj = TeamFactory.objectify(t_db)

    try:
        entries = ScheduleEntries.query_2(
            index='TeamSeasonIndex',
            team_id__eq=t_obj.id,
            season__eq=s_obj.id,
        )
        counter = 0
        for e_item in entries:
            e = ScheduleEntryFactory.objectify(e_item)

            # Attempt to overwrite the opponent with a team_id
            if e.normal_opp is False:
                try:
                    opponent_team_items = TeamAltnames.query_2(
                        index='AltnamesGenderIndex',
                        altname__eq=e.opponent,
                        is_women__eq=e.is_women,
                    )
                    # Really need a helper function for this.
                    results_list = list(opponent_team_items)
                    num_results = len(results_list)
                    if num_results == 0:
                        raise Exception("No opponent altname found (%s)" % e.opponent)
                    elif num_results > 1:
                        raise Exception("Too many opponent altnames found (%s)" % e.opponent)
                    else:
                        e.opponent = results_list[0]['team_id']
                        e.normal_opp = True

                    print "**SUCESS: Rewrote opponent to '%s'" % e.opponent
                except Exception as ex:
                    print "**FAILED to rewrite oppponent '%s'" % e.opponent
                    #print ex
                    e.normal_opp = False

            # Attempt to overwrite the location with a location_id
            if e.normal_loc is False:
                try:
                    if e.site == 'home':
                        affiliation = t_obj.id
                    elif e.site == 'away':
                        affiliation = e.opponent
                    else:
                        # @TODO Need to figure out without affiliation
                        print "**ERROR: No idea what site this is"
                        pass
                    location_items = LocationAltnames.query_2(
                        index='AffiliationIndex',
                        affiliation__eq=affiliation,
                        altname__eq=e.location
                    )
                    # Really need a helper function for this.
                    results_list = list(location_items)
                    num_results = len(results_list)
                    if num_results == 0:
                        raise Exception("No location altname found (%s)" % e.location)
                    elif num_results > 1:
                        raise Exception("Too many location altnames found (%s)" % e.location)
                    else:
                        e.normal_loc = True
                        e.location = results_list[0]['location_id']

                    print "**SUCESS: Rewrote location to '%s'" % e.location
                except Exception as ex:
                    print "**FAILED to rewrite location '%s' for opponent '%s'" % (e.location, e.opponent)
                    #print ex
                    e.normal_loc = False

            sched_entry = ScheduleEntryFactory.itemify(ScheduleEntries, e)
            sched_entry.save(overwrite=True)
            counter += 1

        print "SUCCESS on %s (%i entries)" % (t_obj.id, counter)

    except Exception as e:
        print "FAILED on %s" % t_obj.id
        print e
        traceback.print_exc()