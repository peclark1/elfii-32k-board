# Experimental full 19-net congested-group reroute

This branch is an **experimental candidate only**. It is not approved for merge or fabrication.

The candidate selectively rips up the existing congested connector-area routes for:

- MA0-MA7
- D0-D7
- TPA
- NMRD
- NMWR

The router models **all 86 edge fingers as physical copper obstacles**, including unassigned contacts. The candidate then routes all 19 nets in one coordinated pass using a 0.3175 mm search grid and 0.254 mm tracks.

Candidate changes:
- removed 307 old target-net segments and 32 old target-net vias;
- added 643 routed segments and 103 vias;
- preserves all non-target copper, component placement, edge geometry, power pours and schematic net assignments;
- completes every targeted logical connection in the routing model.

The normal track-quality check is allowed to warn on this branch so the candidate can reach real KiCad 9 DRC. **Main remains strict**. Accept/reject this route based on:
1. no new shorts, track crossings, solder-mask bridges, clearance violations, or thermal errors;
2. reduction of the signal airwire count;
3. visual/layout quality review, including via count and serviceability.

Even a DRC-clean result would still require cleanup before fabrication because 103 vias is higher than desired and the known card-edge/footprint issues remain.
