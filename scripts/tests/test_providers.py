#!/usr/bin/env python

from hawkeyapi.models import TeamModel
from hawkeyapi.objects import Team
from hawkeyapi.TestData import seasons


s = seasons[1]

#teams = TeamModel.scan(is_women__eq=True)
teams = TeamModel.conference_index.query('NCHC', is_women__eq=False)
#teams = TeamModel.conference_index.query('WCHA', is_women__eq=False, name__begins_with='Northern')

for e in teams:
    try:
        t = Team(
            e.name,
            e.mascot,
            e.is_women,
            e.home_conference,
            e.social_media,
            e.web_site,
            e.web_provider,
        )

        team_provider = t.get_provider()
    except Exception as ex:
        print "Totally blew up on %s" % e.name
        print "  Specific error: %s" % ex
        continue

    print ""
    print "%s - %s" % (t.institution_name, s.id)


#    sched_entries = team_provider.get_schedule(s)
#    print "%s Parsed %i entries" % (t.provider, len(sched_entries))


    try:
        sched_entries = team_provider.get_schedule(s)
        print "%s Parsed %i entries" % (t.provider, len(sched_entries))
    except Exception as e:
        print "FAILED"
        print "  Specific error: %s" % e
        continue

    print "SUCCESS"
