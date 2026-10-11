"""Building Repair Centre site content (Australian English).

Business details and service scope come from the original WordPress site
(database roofcent_wp2). Claims about insurance cover, years of experience,
KPIs, job counts, 24/7 availability, licences and Aust Building are left out
on the owner's instructions until they are confirmed. See docs/MIGRATION-NOTES.md.
"""

SITE = {
    "name": "Building Repair Centre",
    "url": "https://www.buildingrepaircentre.com.au",
    "phone": "0431 848 619",
    "phone_href": "tel:+61431848619",
    "email": "info@buildingrepaircentre.com.au",
    "hours": "Monday to Friday, 9 am – 5 pm",
    "area": "Servicing Sydney-wide",
    "roofcentre": "https://www.roofcentre.com.au/",
}

ABOUT = [
    "Building Repair Centre carries out building works and maintenance across Sydney, including drywall "
    "and plastering, painting, plumbing, electrical work, carpentry and joinery, rendering and bricklaying.",
    "We work with strata and property managers, insurance building clients, builders and commercial "
    "property owners, as well as homeowners who need repairs, maintenance or renovation work.",
    "We are always looking to work with new clients and partners. If you think we can help you or your "
    "business, get in touch and we can talk about the job.",
]

# Sector service pages. "slug" is the URL. /commnercial/ (the old misspelt URL) 301s to /commercial/.
SERVICES = [
    {
        "slug": "insurance-building",
        "name": "Insurance Building",
        "short": "Insurance building",
        "icon": "shield",
        "hero": "storm-tree-roof",
        "card": "storm-tree-roof",
        "summary": "Make-safe work and building repairs for properties damaged by storms, fallen trees, water, fire or impact.",
        "seo_title": "Insurance Building Repairs Sydney | Building Repair Centre",
        "description": "Make-safe work and insurance building repairs across Sydney for storm, fallen-tree, water, fire and impact damage. Call 0431 848 619.",
        "lead": "Make-safe work and building repairs for properties damaged by storms, fallen trees, water, fire or impact, across Sydney.",
        "intro": [
            "When a property is damaged, the first job is to make it safe and stop further damage. After that, "
            "the damaged areas need to be repaired and the building returned to its original condition.",
            "Building Repair Centre provides building services for insurance work: from the initial make-safe "
            "through to the repairs, using the trades the job needs.",
        ],
        "includes": [
            ("Emergency make safe", "Securing and weatherproofing a damaged property, such as temporary covers, propping or boarding up, so it does not get worse while repairs are arranged."),
            ("Building maintenance", "Ongoing building maintenance for property owners and managers."),
            ("All repair jobs", "Repairs to roofs, ceilings, walls, floors, doors, windows, fences and finishes after damage."),
            ("All trade services", "Carpentry, plastering, painting, roofing, electrical, plumbing, tiling and the other trades a repair can need."),
        ],
        "gallery": ["storm-tree-roof", "storm-tree-yard", "tile-roof-skylights", "plastered-room"],
        "faqs": [
            ("What should I do straight after storm or tree damage?",
             "Make sure everyone is safe first. If life or property is at immediate risk, call the NSW SES on "
             "<a href=\"tel:132500\">132 500</a> (or 000 in a life-threatening emergency). Take photos of the damage "
             "for your insurer, then call us on <a href=\"tel:+61431848619\">0431 848 619</a> during business hours to arrange make-safe work and repairs."),
            ("Do I need to contact my insurer first?",
             "If you are making an insurance claim, contact your insurer as early as possible and follow their "
             "instructions. They may need photos, a report or a quote before repairs start."),
        ],
    },
    {
        "slug": "strata-real-estate-maintenance",
        "name": "Strata & Real Estate Maintenance",
        "short": "Strata & real estate",
        "icon": "building",
        "hero": "redfern-apartments",
        "card": "redfern-apartments",
        "summary": "Repairs and maintenance for strata managers, real estate agencies, landlords and owners corporations.",
        "seo_title": "Strata & Real Estate Maintenance Sydney | Building Repair Centre",
        "description": "Building repairs and maintenance for strata managers, real estate agencies and landlords across Sydney. Interior and exterior work. Call 0431 848 619.",
        "lead": "Interior and exterior building repairs and maintenance for strata managers, real estate agencies, landlords and owners corporations.",
        "intro": [
            "We provide exterior and interior building services for strata and real estate management companies. "
            "That includes common property in apartment buildings and townhouse complexes, and repairs and "
            "maintenance in tenanted homes.",
            "We deal directly with tenants, landlords and the strata community to arrange the work, and we "
            "provide reasonable quotes for building work of all sizes.",
        ],
        "includes": [
            ("Emergency make safe", "Making a damaged property safe and weatherproof so residents are protected while repairs are organised."),
            ("Building maintenance", "Planned and reactive maintenance for common property, units and rental homes."),
            ("Repair jobs, small to big", "From a sticking door or damaged plasterboard to larger repairs across a building."),
            ("All trade services", "One contact for carpentry, painting, plastering, tiling, waterproofing, fencing and more."),
        ],
        "gallery": ["redfern-apartments", "redfern-1", "redfern-2", "redfern-3", "redfern-4", "apartment-block"],
        "faqs": [
            ("Can you arrange access with tenants or residents?",
             "Yes. Tell us who the contact is for access, such as the tenant, building manager or owner, and we will "
             "arrange a time that suits them."),
            ("Do you quote for strata and agency work?",
             "Yes. Send us the work order or a description of the job, the address and any photos, and we will provide a quote."),
        ],
    },
    {
        "slug": "commercial",
        "name": "Commercial",
        "short": "Commercial",
        "icon": "briefcase",
        "hero": "cafe-fitout",
        "card": "cafe-fitout",
        "summary": "Fit-outs, refurbishments and building maintenance for shops, offices, colleges and other commercial sites.",
        "seo_title": "Commercial Fit-outs & Maintenance | Building Repair Centre",
        "description": "Commercial building work in Sydney: office and shop fit-outs, refurbishments, project management and building maintenance. Call 0431 848 619.",
        "lead": "Large or small commercial works covering all parts of the building scope, from fit-outs to ongoing maintenance.",
        "intro": [
            "Building Repair Centre takes on large or small commercial works involving all parts of the building "
            "scope, including fit-outs, refurbishments and ongoing maintenance of commercial premises.",
            "We know choosing a builder is not easy, so we keep the process simple: tell us about the job, we "
            "provide a quote, and we coordinate the trades once you go ahead.",
            "Please contact us to talk about starting a commercial project.",
        ],
        "includes": [
            ("Project management", "Coordinating the trades, materials and schedule for your project."),
            ("Building maintenance", "Repairs and upkeep for offices, shops, schools, colleges and other commercial buildings."),
            ("Office fit-out", "Partitions, plasterboard, ceilings, joinery, painting and finishes for offices and retail spaces."),
            ("Development & subdivision", "Building work for development and subdivision projects."),
            ("All trade services", "Every trade the job needs, from electrical and plumbing to flooring and concreting."),
        ],
        "gallery": ["cafe-fitout", "camperdown-stairs", "camperdown-1", "camperdown-3", "camperdown-4", "camperdown-6", "college-1", "college-2"],
        "faqs": [
            ("Can you work around a business that is still trading?",
             "Tell us your trading hours and any restrictions when you request a quote, and we will plan the work around them where possible."),
            ("Do you take on small commercial jobs?",
             "Yes. We take on large and small commercial works, including one-off repairs and ongoing maintenance."),
        ],
    },
    {
        "slug": "residential",
        "name": "Residential",
        "short": "Residential",
        "icon": "home",
        "hero": "deck-pergola-cn",
        "card": "deck-pergola-cn",
        "summary": "Repairs, renovations, extensions, decks, pergolas, granny flats and new homes across Sydney.",
        "seo_title": "Residential Building & Renovations | Building Repair Centre",
        "description": "Home repairs, renovations, extensions, decks, pergolas, granny flats and new homes across Sydney. Request a quote or call 0431 848 619.",
        "lead": "Efficient solutions for your home, from repairs and maintenance to renovations, extensions, decks, granny flats and new homes.",
        "intro": [
            "Building Repair Centre can take on works and provide efficient solutions for your property. We restore "
            "damaged areas to their original state, or carry out temporary repairs, depending on what you need.",
            "We also handle full home renovations, home extensions, decks and pergolas, granny flats and new homes, "
            "as well as handyman services.",
        ],
        "includes": [
            ("Project management", "Planning and coordinating the trades on your renovation or build."),
            ("Building maintenance", "Repairs and upkeep to keep your home in good condition."),
            ("Bathroom renovation", "Strip-out, waterproofing, tiling, fixtures and finishes."),
            ("House renovation", "Updating rooms or the whole house, inside and out."),
            ("New homes", "New home construction."),
            ("Decks & pergolas", "Timber decks, pergolas and outdoor areas."),
            ("Development & subdivision", "Building work for development and subdivision projects."),
            ("Granny flats", "Secondary dwellings built on your property."),
            ("Trade services", "Individual trades, from carpentry and painting to plumbing and electrical."),
        ],
        "gallery": ["deck-pergola-cn", "deck-frame-cn", "pergola-5", "pergola-7", "pergola-3", "hallway-doors", "plastered-room", "pergola-12"],
        "faqs": [
            ("Can you do a temporary repair first?",
             "Yes. Depending on what you need, we can carry out a temporary repair to make the area safe, or restore it to its original state."),
            ("Do you build decks and pergolas?",
             "Yes. Decks and pergolas are part of our residential work. See the <a href=\"/projects/\">projects page</a> for photos of deck and pergola builds."),
        ],
    },
    {
        "slug": "tradie-services",
        "name": "Tradie Services",
        "short": "Trade services",
        "icon": "tools",
        "hero": "camperdown-3",
        "card": "plastered-room",
        "summary": "Carpentry, painting, electrical, plastering, plumbing, tiling, roofing and more: 21 trades from one contact.",
        "seo_title": "Trade Services in Sydney | Building Repair Centre",
        "description": "Trade services across Sydney: carpentry, painting, electrical, plastering, plumbing, tiling, roofing, rendering, fencing and more. Call 0431 848 619.",
        "lead": "Carpentry, painting, electrical, plastering, plumbing, tiling, roofing and more, organised through one contact.",
        "intro": [],
        "includes": [],
        "gallery": ["camperdown-1", "plastered-room", "concrete-courtyard", "fence-walkway", "aluminium-frame", "tile-roof-skylights"],
        "faqs": [
            ("Do you accept trades and suppliers?",
             "Yes. We accept trades, suppliers and individual tradespeople. Email "
             "<a href=\"mailto:info@buildingrepaircentre.com.au\">info@buildingrepaircentre.com.au</a> with your trade and contact details."),
        ],
    },
]

# The 21 trades listed on the original Tradie Services page.
TRADES = [
    ("Carpentry works", "hammer", "Framing, doors, skirting, architraves and general carpentry repairs."),
    ("Painting", "roller", "Interior and exterior painting and repainting after repairs."),
    ("Electrical works", "bolt", "Electrical repairs and installations."),
    ("Plastering", "trowel", "Plasterboard installation, patching and setting."),
    ("Rubbish removal", "trash", "Clearing building waste and rubbish from the site."),
    ("Plumbing & drainage works", "pipe", "Plumbing and drainage repairs and installations."),
    ("Concreting works", "layers", "Paths, slabs, driveways and concrete repairs."),
    ("Waterproofing", "drop", "Waterproofing for bathrooms, balconies and wet areas."),
    ("Landscaping", "leaf", "Landscaping and outdoor works."),
    ("Guttering", "gutter", "Gutter and downpipe repairs and replacement."),
    ("Tiling", "grid", "Wall and floor tiling, including bathrooms and kitchens."),
    ("Roofing", "roof", "Roof repairs and maintenance."),
    ("Joinery", "joinery", "Cabinetry and joinery work."),
    ("Scaffolding", "scaffold", "Scaffolding for access to work at height."),
    ("Cleaning", "sparkle", "Cleaning during and after building work."),
    ("Flooring", "floor", "Floor installation and repairs."),
    ("Bricklaying", "brick", "Brickwork, repairs and new walls."),
    ("Aluminium windows & doors", "window", "Aluminium window and door installation and repairs."),
    ("Rendering", "render", "Rendering and render repairs."),
    ("Fencing", "fence", "New fences and fence repairs."),
    ("Handyman services", "tools", "Smaller jobs and odd jobs around the property."),
]

# Who we work for (from the original FAQ answer about the business).
CLIENTS = [
    "Insurance builders and insurance companies",
    "Strata building management",
    "Real estate property management",
    "Builders' projects",
    "Building management maintenance",
    "Colleges, schools and universities",
    "Commercial and residential owners",
    "Private and government projects",
]

FAQS = [
    ("What services do you offer?",
     "We offer <a href=\"/insurance-building/\">insurance building</a>, <a href=\"/strata-real-estate-maintenance/\">strata and real "
     "estate maintenance</a>, <a href=\"/commercial/\">commercial</a> and <a href=\"/residential/\">residential</a> building work, "
     "plus <a href=\"/tradie-services/\">trade services</a> such as carpentry, painting, plastering, electrical, plumbing and tiling."),
    ("What do you specialise in?",
     "We specialise in insurance and renovation repair work. We also take on residential and commercial building work."),
    ("What are your business hours?",
     "We are open Monday to Friday, 9 am to 5 pm."),
    ("Which areas do you service?",
     "We service the Sydney region. Tell us the suburb when you request a quote."),
    ("Who do you work for?",
     "We provide services to insurance builders, strata and building managers, real estate property managers, builders, colleges, "
     "schools and universities, and commercial and residential property owners, on private and government projects."),
    ("How do I get a quote?",
     "Call us on <a href=\"tel:+61431848619\">0431 848 619</a> or <a href=\"/contact-us/#quote\">send an enquiry</a>. Include the "
     "address or suburb, a description of the work and, if you can, a few photos."),
    ("Do you charge for quotes?",
     "No. Quotes are free. For some jobs we will need to inspect the property before we can quote."),
    ("Can you help after storm or tree damage?",
     "Yes. We carry out make-safe work and repairs. If life or property is at immediate risk, call the NSW SES on "
     "<a href=\"tel:132500\">132 500</a>, or 000 in a life-threatening emergency."),
    ("Do you accept trades and suppliers?",
     "Yes. We accept trades, suppliers and individual tradespeople. Email "
     "<a href=\"mailto:info@buildingrepaircentre.com.au\">info@buildingrepaircentre.com.au</a> with your details."),
]

# Project gallery groups (photos from the original Projects page and media library).
# Suburb names are as captioned on the original site.
PROJECTS = [
    {"id": "camperdown", "title": "Camperdown", "type": "commercial", "label": "Commercial fit-out",
     "text": "Fit-out of a commercial building in Camperdown, from the open shell to plasterboard walls and finished floors.",
     "photos": ["camperdown-stairs", "camperdown-1", "camperdown-3", "camperdown-4", "camperdown-6"]},
    {"id": "college", "title": "College building", "type": "commercial", "label": "Commercial",
     "text": "Work inside a large steel-framed college building, using scissor lifts for access at height.",
     "photos": ["college-frame", "college-1", "college-2", "college-3", "college-4"]},
    {"id": "cafe", "title": "Café fit-out", "type": "commercial", "label": "Commercial fit-out",
     "text": "A completed café fit-out with timber counter, display cabinet and lighting.",
     "photos": ["cafe-fitout"]},
    {"id": "redfern", "title": "Redfern", "type": "strata", "label": "Strata & apartments",
     "text": "Work on a multi-storey apartment building in Redfern.",
     "photos": ["redfern-apartments", "redfern-1", "redfern-2", "redfern-3", "redfern-4", "apartment-block"]},
    {"id": "chipping-norton", "title": "Chipping Norton", "type": "residential", "label": "Deck & pergola",
     "text": "A new timber deck and pergola at the back of a brick home in Chipping Norton, plus internal plastering.",
     "photos": ["deck-pergola-cn", "deck-frame-cn", "plastered-room"]},
    {"id": "deck-roof", "title": "Deck, pergola and roof build", "type": "residential", "label": "Deck & pergola",
     "text": "Building a raised deck and a roofed pergola: from the subfloor and framing to the finished metal roof.",
     "photos": ["pergola-5", "pergola-1", "pergola-8", "pergola-10", "pergola-3", "pergola-6", "pergola-7", "pergola-9", "pergola-2", "pergola-4", "pergola-11", "pergola-12"]},
    {"id": "lindfield", "title": "Lindfield", "type": "residential", "label": "Residential",
     "text": "A steel-framed structure under construction on a sloping bush block in Lindfield.",
     "photos": ["lindfield-frame"]},
    {"id": "storm", "title": "Storm and tree damage", "type": "insurance", "label": "Insurance repairs",
     "text": "Properties damaged by fallen trees, before make-safe and repair work.",
     "photos": ["storm-tree-roof", "storm-tree-yard"]},
    {"id": "more", "title": "More of our work", "type": "trades", "label": "Trade services",
     "text": "Roofing, concreting, fencing, joinery and finishing work from other jobs.",
     "photos": ["tile-roof-skylights", "concrete-courtyard", "fence-walkway", "aluminium-frame", "hallway-doors"]},
]

PROJECT_FILTERS = [("all", "All projects"), ("commercial", "Commercial"), ("strata", "Strata & apartments"),
                   ("residential", "Residential"), ("insurance", "Insurance repairs"), ("trades", "Trade services")]
