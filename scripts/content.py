# -*- coding: utf-8 -*-
"""
Copy and data used by build.py that isn't tied to one page template:
service groups, outcomes, free offers, city profiles and industries.
Written in British English. Text may contain basic HTML entities.
"""

# ---------------------------------------------------------------------------
# CTAs (keep these two phrases identical everywhere)
# ---------------------------------------------------------------------------
CTA_PRIMARY = "Let’s talk about your business"
CTA_SECONDARY = "Explore our services"
CASE_BY_CASE = ("We start by understanding what you want to achieve, then recommend the right solution for your "
                "business, situation and budget, case by case. We never use a one-size-fits-all package.")

# ---------------------------------------------------------------------------
# Services, grouped for the menu and the Services hub page
# ---------------------------------------------------------------------------
SERVICE_GROUPS = [
    ("Search & Advertising", ["seo-services", "aeo-ai-search", "local-seo", "ppc-digital-advertising", "google-ads"]),
    ("Websites & Apps", ["website-design", "e-commerce-websites-design", "app-development", "custom-software"]),
    ("Marketing", ["social-media", "content-marketing", "email-marketing", "lead-generation"]),
    ("Branding & Creative", ["branding", "graphic-design", "video-photography", "copywriting"]),
    ("Automation & Security", ["ai-automation", "crm", "cyber-security", "website-maintenance"]),
    ("Digital Consulting", ["digital-consulting"]),
]

SERVICE_BLURB = {
    "seo-services": "Better rankings, more visibility and more of the right customers finding you on Google.",
    "aeo-ai-search": "Be the business that ChatGPT and Google’s AI answers recommend.",
    "local-seo": "Show up on Google Maps so nearby customers find you first.",
    "ppc-digital-advertising": "Paid ads that reach the right audience and bring in leads, without wasting budget.",
    "google-ads": "Google Ads that appear at the moment customers search, tracked through to enquiries.",
    "website-design": "A fast, credible website that turns visitors into real enquiries.",
    "e-commerce-websites-design": "An online shop that’s simple for you to run and easy for people to buy from.",
    "app-development": "An app for your customers or your team, on iPhone, Android and the web.",
    "custom-software": "Tools built around the way you already work, so your team saves time.",
    "social-media": "Posts and paid social that build visibility, engagement and a loyal audience.",
    "content-marketing": "Useful blogs, guides and video that bring in customers for years, not days.",
    "email-marketing": "Stay in touch with past enquiries and turn them into repeat sales.",
    "lead-generation": "Campaigns and landing pages designed to fill your enquiry inbox.",
    "branding": "A logo and look that make your business feel established and trustworthy.",
    "graphic-design": "Brochures, property packs and social graphics that always look on brand.",
    "video-photography": "Photos and video that show your property, product or team at its best.",
    "copywriting": "Clear words that explain what you do and persuade people to get in touch.",
    "ai-automation": "Let AI answer common questions and follow up leads while you sleep.",
    "crm": "One place to track every enquiry, so no customer slips through the cracks.",
    "cyber-security": "Protect your website and customer data from hackers and downtime.",
    "website-maintenance": "We keep your site fast, updated, backed up and online, so you don’t have to.",
    "digital-consulting": "Not sure what you need? We tell you plainly where your money is best spent.",
}

# ---------------------------------------------------------------------------
# Outcomes: what each service should deliver (intro sentence + four results)
# ---------------------------------------------------------------------------
OUTCOMES = {
    "seo-services": ("SEO should be judged on the whole result, not just a ranking report.", [
        ("Better rankings", "Higher positions for the searches that matter to your business, not vanity keywords."),
        ("More visibility", "Your business seen more often on Google, in Maps and in AI-generated answers."),
        ("Relevant traffic", "More visitors who are genuinely looking for what you offer."),
        ("Enquiries and growth", "More calls, forms and bookings that turn into customers and, ultimately, business growth."),
    ]),
    "aeo-ai-search": ("The aim is simple: when people ask AI about what you do, your business is part of the answer.", [
        ("Visibility in AI answers", "More chances of being mentioned in ChatGPT, Google AI Overviews and similar tools."),
        ("A clearer brand", "Search engines and AI tools understand who you are, what you offer and where."),
        ("Better-informed visitors", "People arriving from AI recommendations who already know what you do."),
        ("A future-ready presence", "A website and content structured for how people search now and next."),
    ]),
    "local-seo": ("Local SEO is about being the obvious choice for people nearby.", [
        ("Maps visibility", "A place in the local results when nearby customers search for your services."),
        ("More calls and visits", "Phone calls, direction requests and walk-ins from people close to you."),
        ("A stronger reputation", "A steady flow of genuine reviews, answered professionally."),
        ("A consistent local presence", "Accurate business details everywhere you are listed."),
    ]),
    "ppc-digital-advertising": ("Advertising should be measured by what it brings in, not by clicks.", [
        ("The right audience", "Your ads in front of people chosen by location, interest and intent."),
        ("More leads", "Campaigns and landing pages built to bring in enquiries, bookings or sales."),
        ("Better return on spend", "Budget moved towards what works and away from what doesn’t."),
        ("Clear reporting", "Spend, results and next steps in one plain-English report."),
    ]),
    "google-ads": ("Google Ads works best when every click can be traced to a result.", [
        ("Found at the moment of intent", "Your ads appear when customers search for what you offer."),
        ("More qualified leads", "Calls, forms and purchases from people ready to act."),
        ("A lower cost per enquiry", "Regular optimisation to make every part of your budget work harder."),
        ("Full tracking", "Every click followed through to enquiries and sales."),
    ]),
    "website-design": ("A website should look good, but it also has to work hard for your business.", [
        ("A better user experience", "Clear navigation and fast, mobile-friendly pages that make it easy to find what people need."),
        ("Greater credibility", "A professional, consistent site that builds trust before anyone gets in touch."),
        ("More conversions", "Clear calls to action and enquiry points that turn more visitors into leads or sales."),
        ("A site that grows with you", "A flexible build you can update yourself and extend as your business changes."),
    ]),
    "e-commerce-websites-design": ("A good store makes buying easy and gives customers every reason to complete the order.", [
        ("A smoother shopping experience", "Easy browsing, clear product information and a checkout that works well on a phone."),
        ("Trust at every step", "Secure payments, clear delivery and returns information, and visible reviews."),
        ("More completed orders", "Fewer abandoned baskets and a higher share of visitors becoming customers."),
        ("A store ready to grow", "New products, collections and markets added without rebuilding."),
    ]),
    "app-development": ("The best apps make something genuinely easier for the people who use them.", [
        ("Convenience for users", "Everyday tasks completed in minutes, on the device people already use."),
        ("Higher engagement", "Features that bring people back, not just a one-off download."),
        ("Efficiency for your team", "Internal apps that replace paperwork and chasing."),
        ("Insight into usage", "Data on what people actually do, so you know what to improve next."),
    ]),
    "custom-software": ("Custom software should give time back to your team from the first week.", [
        ("Hours saved every week", "Manual and repeated tasks automated away."),
        ("Fewer errors", "One source of truth instead of copied spreadsheets."),
        ("A tool that fits", "Built around your workflow, not the other way round."),
        ("Room to scale", "Features and users added as your business grows."),
    ]),
    "social-media": ("Social media should support your wider business goals, not just collect likes.", [
        ("More visibility", "A consistent presence that keeps your business in front of the right people."),
        ("Real engagement", "Content that earns comments, shares and conversations."),
        ("Audience growth", "A growing community of followers who are relevant to your business."),
        ("Support for wider goals", "Social that backs up your enquiries, recruitment, reputation and events."),
    ]),
    "content-marketing": ("Good content keeps working long after the work of writing it is done.", [
        ("Authority in your field", "Content that shows you know your subject."),
        ("Steady organic traffic", "Pages that keep attracting visitors month after month."),
        ("Trust before first contact", "Prospects who have already learned from you."),
        ("Leads over time", "Enquiries that build steadily rather than spiking and fading."),
    ]),
    "email-marketing": ("Email turns the people who already know you into repeat customers.", [
        ("Repeat sales", "Past customers and enquiries brought back at the right moment."),
        ("Stronger relationships", "Useful, relevant emails that people are glad to receive."),
        ("Time saved", "Automated flows that follow up for you."),
        ("Measurable results", "Opens, clicks and revenue tied back to each campaign."),
    ]),
    "lead-generation": ("The goal is a steady flow of the right enquiries, not just more traffic.", [
        ("More enquiries", "A reliable stream of people asking to talk."),
        ("Better-quality leads", "Messaging and forms that attract the right fit."),
        ("A clearer cost per lead", "You know what each enquiry costs and where it came from."),
        ("A joined-up pipeline", "Leads captured and followed up, never lost."),
    ]),
    "branding": ("A strong brand makes every other piece of marketing work harder.", [
        ("Credibility", "A business that looks as established as it is."),
        ("Consistency", "One look and feel across every touchpoint."),
        ("A distinctive identity", "A brand that stands out from competitors rather than blending in."),
        ("Confidence", "An identity you and your team are proud to use."),
    ]),
    "graphic-design": ("Good design makes your message clearer and your business look as good as your work.", [
        ("A professional impression", "Materials that match the quality of what you deliver."),
        ("Clear communication", "Layouts that get the message across quickly."),
        ("Brand consistency", "Every piece unmistakably yours."),
        ("Faster turnaround", "Templates and systems that speed up future projects."),
    ]),
    "video-photography": ("Strong visuals do much of the persuading before anyone reads a word.", [
        ("Stronger first impressions", "Imagery that makes people stop and look."),
        ("Higher engagement", "Video and photography that perform on your website and social channels."),
        ("Content you can reuse", "One shoot supporting your website, social, ads and print."),
        ("Greater trust", "Authentic visuals of your property, product or team."),
    ]),
    "copywriting": ("Clear writing helps people understand you quickly and act.", [
        ("Clarity", "Visitors understand what you do within seconds."),
        ("Persuasion", "Words that guide readers towards getting in touch."),
        ("Search visibility", "Copy structured to support SEO as well as readers."),
        ("A consistent voice", "Your business sounding like itself everywhere."),
    ]),
    "ai-automation": ("AI automation should save your team time without losing the personal touch.", [
        ("Faster responses", "Customers answered straight away, day or night."),
        ("Fewer missed leads", "Every enquiry followed up automatically."),
        ("Time back for your team", "Repetitive questions and admin handled for them."),
        ("A consistent experience", "The same helpful answers every time."),
    ]),
    "crm": ("A good CRM means no enquiry slips through the cracks and every follow-up happens.", [
        ("No lost enquiries", "Every lead captured in one place."),
        ("Better follow-up", "Reminders and automations that keep opportunities moving."),
        ("Clearer reporting", "See where enquiries come from and how many convert."),
        ("Better teamwork", "Everyone working from the same customer history."),
    ]),
    "cyber-security": ("The aim is a site that stays online, stays safe and keeps customers’ trust.", [
        ("Reduced risk", "Common attack routes closed before they are used."),
        ("Less downtime", "Problems caught early, with tested backups ready."),
        ("Customer trust", "Protected data and a secure site visitors can rely on."),
        ("Peace of mind", "Clear, jargon-free reporting on your security."),
    ]),
    "website-maintenance": ("A well-cared-for website quietly keeps working in the background.", [
        ("A reliable website", "Monitored and kept online, so it is there when customers visit."),
        ("A faster website", "Ongoing performance checks keep pages quick."),
        ("A more secure website", "Updates and backups applied on schedule."),
        ("Time back for you", "The technical upkeep handled by someone else."),
    ]),
    "digital-consulting": ("A consultation should leave you clearer, not more confused.", [
        ("Clarity", "A plain-English view of where you stand."),
        ("Clear priorities", "What to do first, what can wait and what to skip."),
        ("Money well spent", "Budget directed to what will actually move your business forward."),
        ("Confidence", "A plan you can act on with us, your own team or anyone else."),
    ]),
}

# ---------------------------------------------------------------------------
# Free audits and reviews
# ---------------------------------------------------------------------------
FREE_OFFERS = [
    ("digital-health-check", "Free Digital Health Check", "growth",
     "A quick, honest look at your website, search visibility and marketing, with a clear list of what to fix first."),
    ("seo-ai-search-audit", "Free SEO & AI Search Audit", "search",
     "See how you appear on Google and in AI answers such as ChatGPT, and where the biggest opportunities are."),
    ("website-review", "Free Website Review", "doc",
     "We look at speed, mobile experience, credibility and how well your site turns visitors into enquiries."),
    ("google-ads-ppc-audit", "Free Google Ads/PPC Audit", "chart",
     "We review your campaigns, spend and tracking, and show you where budget could work harder."),
    ("social-media-audit", "Free Social Media Audit", "users",
     "A review of your profiles, content and engagement, with practical ideas to grow your audience."),
    ("free-consultation", "Free 20-minute Consultation", "target",
     "Talk through your goals with one of the team. No pressure and no jargon."),
]
SERVICE_OFFER = {
    "seo-services": "seo-ai-search-audit", "aeo-ai-search": "seo-ai-search-audit", "local-seo": "seo-ai-search-audit",
    "content-marketing": "seo-ai-search-audit", "copywriting": "seo-ai-search-audit",
    "website-design": "website-review", "e-commerce-websites-design": "website-review", "app-development": "website-review",
    "custom-software": "free-consultation", "website-maintenance": "website-review", "cyber-security": "website-review",
    "ppc-digital-advertising": "google-ads-ppc-audit", "google-ads": "google-ads-ppc-audit", "lead-generation": "google-ads-ppc-audit",
    "social-media": "social-media-audit", "video-photography": "social-media-audit", "graphic-design": "social-media-audit",
    "branding": "digital-health-check", "email-marketing": "digital-health-check", "crm": "digital-health-check",
    "ai-automation": "digital-health-check", "digital-consulting": "free-consultation",
}

# ---------------------------------------------------------------------------
# Locations
# ---------------------------------------------------------------------------
SECTOR_NOTES = {
    "Professional services": ("credibility-led sites that explain your expertise and make it easy to book a call.",
                              "ranking for the services and specialisms clients search for, and building authority through helpful content."),
    "Property": ("polished listings, fast galleries and valuation or viewing enquiry forms.",
                                 "neighbourhood-level search visibility, plus listing and area-guide content."),
    "Hospitality": ("mobile-first menus, booking links and photography that makes people want to visit.",
                                    "appearing in Maps and “near me” searches with accurate menus, hours and reviews."),
    "Retail": ("easy browsing, clear delivery information and a checkout that works on a phone.",
                              "category and product-page SEO, plus local visibility for shops with a physical presence."),
    "Healthcare": ("clear treatment pages, reassuring design and simple online booking.",
                              "local visibility for the treatments and conditions people search for before booking."),
    "Home services": ("click-to-call buttons, clear service areas and reviews that win trust quickly.",
                                 "Google Maps rankings and “near me” searches when people need help fast."),
    "Creative industries": ("portfolio-led sites that show your work at its best and load quickly.",
                           "ranking for the niches you specialise in and attracting the right clients."),
    "Technology": ("scalable sites that explain a complex product simply and convert interest into demos.",
                                 "technical SEO plus comparison and use-case content that educates buyers."),
    "Finance": ("trust-first design with clear services, team profiles and compliant enquiry forms.",
                          "high-trust content and local visibility for the specialisms you offer."),
    "Manufacturing": ("clear capability pages, product catalogues and quote request forms.",
                                    "ranking for the specific products, materials and capabilities that B2B buyers search for."),
    "Tourism": ("inspiring imagery, clear itineraries and booking-ready pages.",
                            "seasonal, destination and experience searches, plus a strong Maps presence."),
    "Education": ("course pages, easy enrolment and answers to the questions students and parents ask.",
                               "course and programme searches, structured clearly for students and parents."),
    "Luxury brands": ("refined design and imagery that reflect a premium brand.",
                             "ranking for considered, high-intent searches while protecting a premium tone."),
    "Construction": ("project galleries, proof of past work and simple quote requests.",
                                          "local project and service searches, backed by proof of past work."),
    "Wellness": ("calm, welcoming design and straightforward booking.",
                            "local searches for classes, treatments and practitioners."),
}

# intro: local context; web/seo: one city-specific sentence for each service
CITY_PROFILES = {
    "London": {
        "intro": "London is one of the most competitive business markets in the world, with professional services, creative and tech firms and independent businesses in every borough.",
        "areas": ["Shoreditch", "Canary Wharf", "Westminster", "Kensington", "Croydon"],
        "sectors": ["Professional services", "Property", "Hospitality", "Technology"],
        "web": "With so many competitors a short journey away, a London website has to load quickly on a phone and make its value clear in seconds.",
        "seo": "London searches are fiercely contested, so we focus on the borough, neighbourhood and service combinations where you can realistically win.",
        "more": "Customers here compare several providers in minutes, often on the move, and many search by borough or by the nearest station. A site that makes your location, services and contact details obvious is a real advantage.",
    },
    "Manchester": {
        "intro": "Manchester combines a fast-growing digital and creative scene with a large base of independent businesses, from the Northern Quarter to Salford’s MediaCity.",
        "areas": ["the Northern Quarter", "Salford", "Trafford", "Didsbury", "Stockport"],
        "sectors": ["Creative industries", "Professional services", "Hospitality", "Retail"],
        "web": "Manchester customers are digitally savvy, so your website needs to feel as polished as the city’s best-known brands.",
        "seo": "We target the searches Greater Manchester customers actually use, from city-centre queries to those in the surrounding towns.",
        "more": "The city’s mix of start-ups, established firms and a lively independent scene means standing out takes more than a pretty design. Clear messaging and strong local signals make the difference.",
    },
    "Birmingham": {
        "intro": "Birmingham is the UK’s second city and a major centre for professional services, manufacturing and retail, with a diverse mix of local businesses.",
        "areas": ["the Jewellery Quarter", "Digbeth", "Edgbaston", "Solihull", "Sutton Coldfield"],
        "sectors": ["Professional services", "Manufacturing", "Retail", "Healthcare"],
        "web": "Birmingham’s business base is diverse, so we design around your specific customers rather than a generic West Midlands audience.",
        "seo": "We build visibility across Birmingham and the wider West Midlands, including the neighbourhood searches that bring in local customers.",
        "more": "Birmingham is large enough that customers in Edgbaston, Digbeth or Solihull all search slightly differently. Good local pages speak to each area rather than treating the whole region as one audience.",
    },
    "Leeds": {
        "intro": "Leeds is a major centre for financial, legal and professional services, with a growing digital sector and a busy independent scene.",
        "areas": ["the city centre", "Headingley", "Chapel Allerton", "Horsforth", "Roundhay"],
        "sectors": ["Finance", "Professional services", "Retail", "Technology"],
        "web": "Leeds businesses range from city-centre professional firms to growing independents, and your website should reflect where you sit in that mix.",
        "seo": "We focus on the Leeds and West Yorkshire searches that matter, helping you stand out in a busy professional and retail market.",
        "more": "Leeds draws customers from right across West Yorkshire, so businesses often need to be found well beyond the city centre. Pages for the districts you serve help you appear where your customers actually are.",
    },
    "Bradford": {
        "intro": "Bradford has a diverse, entrepreneurial business community, from independent retailers and restaurants to manufacturers and growing service firms.",
        "areas": ["the city centre", "Saltaire", "Shipley", "Bingley", "Ilkley"],
        "sectors": ["Hospitality", "Retail", "Manufacturing", "Professional services"],
        "web": "Bradford’s independent businesses often compete with larger names in nearby Leeds, so a sharp, trustworthy website helps you hold your own.",
        "seo": "Strong local SEO helps Bradford businesses be found first by customers in the city, Saltaire and the surrounding district.",
        "more": "Many Bradford businesses win work through word of mouth. A good website and strong reviews turn that reputation into enquiries from people who have not heard of you yet.",
    },
    "Newcastle": {
        "intro": "Newcastle has a thriving mix of professional services, tech start-ups and hospitality across the city centre, the Quayside and Ouseburn.",
        "areas": ["the Quayside", "Jesmond", "Gosforth", "Ouseburn", "Gateshead"],
        "sectors": ["Professional services", "Technology", "Hospitality", "Healthcare"],
        "web": "Newcastle customers appreciate a straightforward, friendly approach, so we build websites that sound like the business behind them.",
        "seo": "We help Tyneside businesses appear in the searches that matter across Newcastle, Gateshead and the wider North East.",
        "more": "Customers across Tyneside often search by area, from Jesmond and Gosforth to the Quayside. Pages that reflect where you work help you show up for them.",
    },
    "Liverpool": {
        "intro": "Liverpool’s economy blends a strong visitor and hospitality scene with growing creative, digital and professional services sectors.",
        "areas": ["the Baltic Triangle", "the Georgian Quarter", "Albert Dock", "Wavertree", "the Waterfront"],
        "sectors": ["Tourism", "Creative industries", "Hospitality", "Professional services"],
        "web": "Liverpool’s visitor and creative economy means plenty of people research businesses on their phone, so mobile performance matters.",
        "seo": "From Baltic Triangle start-ups to long-established firms, we help Liverpool businesses appear for the local and visitor searches that matter.",
        "more": "Visitors and locals alike search for businesses on their phones, often while they are out and about. Accurate opening hours, clear directions and quick-loading pages make a real difference.",
    },
    "Berlin": {
        "intro": "Berlin is one of Europe’s leading start-up and creative cities, with a multilingual, international audience that expects polished websites.",
        "areas": ["Mitte", "Kreuzberg", "Prenzlauer Berg", "Charlottenburg", "Friedrichshain"],
        "sectors": ["Technology", "Creative industries", "Hospitality", "Tourism"],
        "web": "German websites need more than good design: requirements such as an Impressum and careful data-protection handling are part of doing it properly.",
        "seo": "Berlin is a multilingual, international search market, so we plan German- and English-language visibility together.",
        "more": "Many Berlin businesses serve German- and English-speaking customers alike, so clear language options and well-structured content help both audiences find and trust you.",
    },
    "New York": {
        "intro": "New York is one of the most competitive markets in the world, where businesses across all five boroughs compete for attention against well-funded rivals.",
        "areas": ["Manhattan", "Brooklyn", "Queens", "the Bronx", "Staten Island"],
        "sectors": ["Finance", "Professional services", "Hospitality", "Retail"],
        "web": "In a city where customers compare options in seconds, your website needs to earn trust on first view and load fast on a phone.",
        "seo": "New York is among the most competitive search markets anywhere, so we focus on the borough, neighbourhood and service searches you can realistically win.",
        "more": "Competition is intense even at street level, and customers often search for a service plus a neighbourhood. Specific, well-optimised pages for each area you serve help you stand out.",
    },
    "Los Angeles": {
        "intro": "Los Angeles is a sprawling, image-conscious market where entertainment, creative, property and lifestyle businesses compete for attention.",
        "areas": ["Santa Monica", "Beverly Hills", "Downtown LA", "Pasadena", "Culver City"],
        "sectors": ["Creative industries", "Property", "Wellness", "Luxury brands"],
        "web": "Los Angeles customers expect polished visuals, so your website should reflect the quality of your work from the first scroll.",
        "seo": "Los Angeles is spread across many distinct areas, so local search strategy works best neighbourhood by neighbourhood.",
        "more": "Customers rarely travel across the whole metro area, so businesses do best when they are clear about which neighbourhoods they serve and show proof of their work.",
    },
    "Chicago": {
        "intro": "Chicago has a broad, resilient economy spanning finance, manufacturing, logistics and professional services, with strong competition at neighbourhood level.",
        "areas": ["the Loop", "River North", "Lincoln Park", "Wicker Park", "Evanston"],
        "sectors": ["Professional services", "Manufacturing", "Healthcare", "Hospitality"],
        "web": "Chicago businesses often serve distinct neighbourhoods, so we build clear service-area pages that speak to each one.",
        "seo": "We target the Chicago-area searches your customers actually make, from the Loop to the surrounding suburbs.",
        "more": "Chicagoans often search by neighbourhood, and the seasons shape demand for many services. A site that reflects both helps you capture the right searches at the right time.",
    },
    "Houston": {
        "intro": "Houston is a major hub for energy, healthcare and logistics, with a large base of service businesses covering a wide metropolitan area.",
        "areas": ["Downtown", "the Heights", "Montrose", "Sugar Land", "The Woodlands"],
        "sectors": ["Construction", "Healthcare", "Home services", "Property"],
        "web": "Houston’s metro area is huge, so your website should make your service area obvious and your phone number impossible to miss.",
        "seo": "We help Houston businesses appear in the right parts of the metro area, where customers search by suburb as much as by city.",
        "more": "Because the metro area is so large, customers want to know quickly whether you serve their part of town. Clear service-area information is often what turns a visit into a call.",
    },
    "Miami": {
        "intro": "Miami is an international, bilingual market where hospitality, property, tourism and luxury lifestyle brands compete for local and overseas customers.",
        "areas": ["Brickell", "Wynwood", "Coral Gables", "Miami Beach", "Coconut Grove"],
        "sectors": ["Property", "Hospitality", "Luxury brands", "Tourism"],
        "web": "Miami’s mix of local and international customers means your website may need to work smoothly in more than one language.",
        "seo": "Miami searches are shaped by tourism, seasonality and bilingual behaviour, so we plan keywords and content with all three in mind.",
        "more": "Seasonal visitors, second-home owners and year-round residents all search differently, so it pays to be clear about who you serve and when.",
    },
    "Atlanta": {
        "intro": "Atlanta is a fast-growing business hub in the south-eastern US, with strong film, logistics, technology and professional services sectors.",
        "areas": ["Midtown", "Buckhead", "Decatur", "Sandy Springs", "Alpharetta"],
        "sectors": ["Professional services", "Technology", "Creative industries", "Manufacturing"],
        "web": "Atlanta’s sprawling metro area means customers often choose by convenience, so clear service areas and fast pages matter.",
        "seo": "We build visibility across Atlanta and its surrounding suburbs, where customers search by area as well as by service.",
        "more": "Traffic and distance shape how people choose in Atlanta, so customers favour businesses that are clearly close to them. Strong local pages and reviews help you look convenient.",
    },
    "Boston": {
        "intro": "Boston’s economy is driven by education, healthcare, life sciences and professional services, with a discerning, research-minded customer base.",
        "areas": ["Back Bay", "Cambridge", "the Seaport", "Somerville", "Brookline"],
        "sectors": ["Education", "Healthcare", "Professional services", "Technology"],
        "web": "Boston customers research carefully before they commit, so your website needs clear information and genuine proof of your expertise.",
        "seo": "We focus on the research-heavy searches Boston customers make, backed by content that demonstrates real expertise.",
        "more": "With so many universities, hospitals and professional firms nearby, Boston customers expect depth and proof. Detailed pages and genuine reviews build the confidence they look for.",
    },
    "Dallas": {
        "intro": "Dallas is a major corporate and business hub in Texas, with strong property, finance and professional services sectors across the wider metroplex.",
        "areas": ["Uptown", "Deep Ellum", "Plano", "Frisco", "Irving"],
        "sectors": ["Property", "Finance", "Professional services", "Construction"],
        "web": "Dallas–Fort Worth is a wide-reaching market, so we design websites that make your service area and credentials clear at a glance.",
        "seo": "Searches vary widely between areas of the metroplex, so we build location-specific visibility rather than one generic page.",
        "more": "Customers across the metroplex often look for someone near their own suburb, so it helps to have clear pages for the areas you cover rather than one general page.",
    },
    "Seattle": {
        "intro": "Seattle is a technology-led market with a digitally savvy customer base, alongside strong healthcare, outdoor retail and hospitality sectors.",
        "areas": ["Capitol Hill", "Bellevue", "Ballard", "South Lake Union", "Redmond"],
        "sectors": ["Technology", "Healthcare", "Retail", "Hospitality"],
        "web": "Seattle customers are comfortable online and quick to judge a slow site, so performance and clarity come first.",
        "seo": "Seattle’s tech-savvy audience compares options thoroughly, so we focus on detailed, trustworthy content that earns the click.",
        "more": "Seattle customers read reviews closely and value clear, honest information, so openness about your services, approach and results tends to pay off.",
    },
    "San Francisco": {
        "intro": "San Francisco is the heart of the Bay Area technology scene, where start-ups, scale-ups and professional services compete for attention online.",
        "areas": ["SoMa", "the Mission", "the Financial District", "Oakland", "Palo Alto"],
        "sectors": ["Technology", "Finance", "Creative industries", "Professional services"],
        "web": "San Francisco audiences are used to excellent digital products, so your website needs to feel fast, clear and modern.",
        "seo": "We help Bay Area businesses cut through a crowded, technical market with clear, authoritative search content.",
        "more": "Buyers in the Bay Area research thoroughly and compare quickly, so clear positioning and evidence of results matter more than clever slogans.",
    },
    "Denver": {
        "intro": "Denver is a growing market known for its outdoor lifestyle, technology and start-up scene, craft hospitality and fast-expanding service sector.",
        "areas": ["LoDo", "Cherry Creek", "RiNo", "Boulder", "Aurora"],
        "sectors": ["Technology", "Hospitality", "Wellness", "Construction"],
        "web": "Denver’s business community is growing quickly, so a clear, modern website helps you stand out.",
        "seo": "We build visibility across Denver and the Front Range, where customers search by neighbourhood and nearby town.",
        "more": "People in Denver often search by neighbourhood or nearby town, and demand can shift with the seasons, so flexible content and local pages help you keep up.",
    },
    "Phoenix": {
        "intro": "Phoenix is one of the fastest-growing metro areas in the US, with strong demand across property, healthcare, construction and home services.",
        "areas": ["Scottsdale", "Tempe", "Mesa", "Chandler", "Glendale"],
        "sectors": ["Home services", "Property", "Healthcare", "Construction"],
        "web": "Phoenix customers often search in a hurry, so quick-loading pages and click-to-call buttons can win the job.",
        "seo": "We help Phoenix-area businesses appear in the local searches that matter, from Scottsdale to Mesa and beyond.",
        "more": "Growth and the climate shape demand for many Phoenix services, and customers tend to want quick answers, so fast pages and clear contact options help you win the call.",
    },
    "Toronto": {
        "intro": "Toronto is Canada’s largest business centre, with a multicultural customer base and strong finance, technology and professional services sectors.",
        "areas": ["Downtown Toronto", "Mississauga", "North York", "Scarborough", "Etobicoke"],
        "sectors": ["Finance", "Technology", "Professional services", "Retail"],
        "web": "Toronto’s multicultural audience may search in several languages, so we plan content and structure with that in mind.",
        "seo": "We focus on Greater Toronto Area searches, where customers often search by neighbourhood or suburb.",
        "more": "Toronto’s neighbourhoods and suburbs each have their own character, so pages that speak to the areas you serve feel more relevant than a single generic page.",
    },
    "Vancouver": {
        "intro": "Vancouver combines a strong technology, film and tourism economy with a lifestyle-focused customer base that searches and shops heavily online.",
        "areas": ["Gastown", "Yaletown", "Burnaby", "Richmond", "North Vancouver"],
        "sectors": ["Technology", "Tourism", "Creative industries", "Wellness"],
        "web": "Vancouver customers are active online, so mobile-first design and fast pages are essential.",
        "seo": "We target Metro Vancouver searches across the city and nearby municipalities such as Burnaby and Richmond.",
        "more": "Lifestyle, the seasons and tourism all influence how Vancouver customers search, so fresh content and accurate local details help you stay visible all year.",
    },
}

# ---------------------------------------------------------------------------
# Industries hub page
# ---------------------------------------------------------------------------
INDUSTRIES = [
    ("real-estate", "Real Estate Agencies",
     "Listing websites, property SEO and lead generation that win more instructions.",
     "Agents win business on trust and visibility. We build fast, polished property sites, strengthen local search so vendors find you first, and set up lead capture that turns valuation requests into instructions.",
     ["seo-services", "website-design", "local-seo", "lead-generation", "video-photography"]),
    ("property-developers", "Property Developers",
     "Launch campaigns, development microsites and international buyer leads.",
     "A development needs momentum from day one. We create standalone microsites and launch campaigns, with tracking that shows which markets and channels bring serious buyers.",
     ["website-design", "ppc-digital-advertising", "video-photography", "lead-generation", "crm"]),
    ("luxury-brands", "Luxury & Lifestyle Brands",
     "Refined identities, e-commerce and content that protect exclusivity.",
     "Premium brands can’t afford to look ordinary. We design identities, stores and content that feel considered at every touchpoint, without discounting your positioning.",
     ["branding", "e-commerce-websites-design", "video-photography", "content-marketing", "social-media"]),
    ("dental-clinics", "Dentists & Clinics",
     "Fill your appointment book from local searches.",
     "Patients choose clinics they can find and trust. We improve your local search presence, build clear treatment pages and make booking simple, so more enquiries become appointments.",
     ["local-seo", "website-design", "seo-services", "google-ads", "ai-automation"]),
    ("trades", "Plumbers & Electricians",
     "Turn local searches into booked jobs.",
     "When something breaks, people call the first trusted name they find. We help you show up in Maps and search, with fast pages and click-to-call buttons so more searches become jobs.",
     ["local-seo", "google-ads", "website-design", "crm", "seo-services"]),
    ("restaurants", "Restaurants & Cafés",
     "More bookings from Google, menus and social.",
     "Diners decide quickly. We keep your menus, photos and opening hours accurate everywhere, build booking-friendly pages and run social content that makes people want to visit.",
     ["local-seo", "website-design", "social-media", "video-photography"]),
    ("retail", "Retailers & Shops",
     "Bring more people through your door and online.",
     "High-street and online need to work together. We combine local visibility, a smooth online store and simple email campaigns to bring customers in and keep them coming back.",
     ["e-commerce-websites-design", "local-seo", "email-marketing", "social-media"]),
    ("online-businesses", "Online Businesses",
     "Sell more with a faster store and smarter ads.",
     "When every sale happens online, speed, trust and targeting matter. We improve your store, tighten your advertising and track results through to revenue.",
     ["e-commerce-websites-design", "google-ads", "ppc-digital-advertising", "email-marketing", "seo-services"]),
    ("professional-services", "Professional Services",
     "Win trust and steady enquiries from new clients.",
     "Clients choose advisers they trust. We build credible websites, publish helpful content and strengthen your search visibility, so the right clients find you and get in touch.",
     ["website-design", "seo-services", "content-marketing", "lead-generation", "copywriting"]),
]
