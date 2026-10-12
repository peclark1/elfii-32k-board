# PCBWay — engineering CAM feasibility and quotation request (NOT an order)

Project: Netronics ELF II 32 KiB SRAM expansion card, early-original 86-contact 2-sided edge interface.

We have a complete, KiCad-DRC-clean two-layer review board. Before submitting any manufacturing order, would your fabrication engineering/CAM team please confirm whether you can preserve the original *electrical and mechanical* card-edge geometry:

- FR-4, nominal 1.6 mm finished thickness (please state allowed production tolerance at connector); outline extrema 177.800 x 127.127 mm, stepped insertion tongue/shoulders preserved.
- **86 contacts, 43 on each face, 2.540 mm pitch, contact copper 1.397 mm wide x 8.890 mm long**. Tip copper stops **only 0.1016 mm from the leading board edge**. This is the historical connector geometry and must NOT be moved, shortened or changed by default CAM normalization.
- Prefer hard gold over nickel *selectively on the 86 contacts*, quote 10 microinch Au / 120 microinch Ni or your recommended connector-grade durable option. Please state required plating-rail or current-feed provisions and whether/how they would be removed.
- We recognize standard 30/45 degree bevel depths would intersect the copper. **Could you offer an intentionally unbeveled or custom very shallow edge-finishing/deburring operation** without modifying this copper? Alternatively, can you plate/finish in another sequence that leaves correct copper, contact wipe and an acceptable insertion lead-in? Please provide a cross-section/dimensioned drawing showing the finished leading edge, residual tip thickness, proposed relief and tolerances. If impossible, please describe the minimum *dimensioned* changes you would require; do not implement them.
- Two layers, 1 oz nominal finished copper, 0.15 mm minimum signal traces (only short sections), 0.20 mm supply traces, 0.60 mm via lands/0.30 mm nominal drills, mask openings on all finger copper on both faces, green mask/white silkscreen. PCBWay guidance suggests extending the solder-mask opening fully to the cut edge; can CAM remove the approximately 0.1016 mm residual mask strip at the tip without touching copper? Please identify any required mask-only edit for explicit approval. Please confirm trace-to-trace and drill-to-copper capability, final annular ring tolerances, mask registration and plating clearance.
- All contact-facing copper ends are away from ground pours; GND pours stop short of the tongue. The edge carries no vias or plated through holes. Please confirm electrical test, routed outline and absence of residual panel tabs on the insertion edge.

Please quote **five** unassembled prototype PCBs, separately listing board cost, selective plating/finishing, setup/CAM surcharges, shipping to US/Minnesota, production lead time and any minimum lot requirement. As a fallback, please quote *unbeveled ENIG for limited-insertion engineering test use*, clearly identified as lower wear resistance than hard gold, if you can manufacture that geometry.

Please explicitly state whether you require artwork adjustment and provide a marked-up CAM image BEFORE we authorize a change. Our supplied Gerbers are design-review artifacts only and must not be released to manufacturing or treated as authorization to modify the connector. No order is authorized.

Reference documentation: docs/design/prototype-fabrication-readiness-2026-10-12.md and docs/reference/hyperboard-rev2-gerber-geometry.md.
