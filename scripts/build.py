# -*- coding: utf-8 -*-
"""
Static site generator for Pinky Brain Digital.
Reads the two CSVs + the content data below and writes:
  - index.html (homepage, wrapped with header/footer)
  - <service-slug>/index.html  for every service in Links.csv
  - <location-slug>/index.html for every row in Location.csv

Run: python scripts/build.py   (from the project root, or anywhere - paths are resolved relative to this file)
"""
import csv
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SITE_NAME = "Pinky Brain Digital"
SITE_EMAIL = "hello@pinkybraindigital.com"
SITE_ADDRESS = "International House, 109–111 Fulham Palace Road, London, W6 8JA"

# Cities featured in the header's Website Design / SEO Services dropdowns.
CURATED_NAV_CITIES = ["New York", "Los Angeles", "London", "Toronto", "Chicago", "Manchester", "Miami"]

# Populated once in main() from the Location CSV; read by header_html().
ALL_LOCATIONS = []

# ---------------------------------------------------------------------------
# ICONS (reused from the homepage's own icon vocabulary, for visual consistency)
# ---------------------------------------------------------------------------
ICONS = {
    'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.5 3.2-5.5 6.5-5.5s5.9 2 6.5 5.5M16 4.8a3.5 3.5 0 0 1 0 6.4M18.5 14.8c1.7.8 2.8 2.6 3 5.2"/>',
    'shield': '<path d="m12 3 8 3v6c0 4.8-3.4 8.2-8 9-4.6-.8-8-4.2-8-9V6z"/><path d="m8.8 12 2.2 2.2 4.2-4.4"/>',
    'chart': '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    'target': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r=".5"/>',
    'search': '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/>',
    'growth': '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    'doc': '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/>',
    'mail': '<path d="M4 6h16v12H4z"/><path d="m4 7 8 6 8-6"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'bolt': '<path d="M13 2 4 14h6l-1 8 9-12h-6z"/>',
    'check': '<path d="M4 12l5 5L20 6"/>',
}
def icon(name, cls="pb-i"):
    return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % (cls, ICONS[name])

WHY_ICONS = ['users', 'shield', 'chart', 'target']
CORE_ICONS = ['bolt', 'search', 'doc', 'chart']
STEP_ICONS = ['target', 'users', 'shield', 'chart']
FINAL_ICONS = ['growth', 'globe', 'check', 'arrow']

# ---------------------------------------------------------------------------
# SERVICES DATA  (sourced from the business's own live service pages)
# ---------------------------------------------------------------------------
SERVICES = {
    "website-design": {
        "slug": "website-design",
        "nav_label": "Website Design",
        "name": "Website Design & Development",
        "eyebrow": "Services · Website Design",
        "h1": "Websites that turn visitors into enquiries",
        "lead": "a fast, modern website built around your customers &mdash; mobile-first, easy for you to update, and designed to convert visitors into real enquiries.",
        "meta": "Fast, mobile-first website design and development that turns visitors into enquiries. Built around your customers, SEO-ready from day one.",
        "ticks": ["Mobile-first design", "SEO-ready from day one", "Launch support included"],
        "badge": ("Page speed", "96 / 100", "Mobile &middot; Desktop &middot; Tablet"),
        "hero_img": "website-design-service-hero.jpg",
        "hero_alt": "Website design and development mock-up for a business homepage",
        "split_img": "website-design-development-process.webp",
        "split_alt": "Website design and development process shown on a laptop screen",
        "why_title": "You don&rsquo;t need another website supplier. You need a digital partner.",
        "why_cards": [
            ("One team. One clear direction.", "From the first conversation to post-launch support, you work with one connected team. No passing your project between multiple suppliers and hoping nothing gets missed."),
            ("Strategy before decoration.", "We don&rsquo;t start by choosing colours and moving boxes around a screen. We first understand your audience, goals and customer journey &mdash; then design around them."),
            ("Clear costs. Clear communication.", "You get a straightforward quote based on the agreed scope before work begins. No confusing packages. No unexpected invoices for work you didn&rsquo;t ask for."),
            ("A site that grows with you.", "Your website is built to expand &mdash; new pages, features and integrations can be added later without a rebuild."),
        ],
        "core_title": "Everything you need to turn clicks into customers.",
        "core_sub": "A beautiful website gets attention. A well-built website gets results.",
        "core_intro": "We bring design, performance, SEO and conversion thinking together to create a website that looks credible, feels effortless to use and gives visitors a clear reason to get in touch.",
        "core_cards": [
            ("Custom website design", "Every website starts with your brand, audience and objectives. We create a visual experience that feels distinctive, professional and genuinely yours."),
            ("Mobile-first development", "Your website is designed for smaller screens first, then refined across tablets and desktops &mdash; so every interaction feels smooth wherever your customers find you."),
            ("SEO-ready foundations", "We build your pages with clean structure, relevant headings, optimised content and technical SEO foundations to give your website a strong starting point in search."),
            ("Performance that keeps people moving", "From image optimisation to efficient code and a streamlined page structure, we focus on creating a fast experience that doesn&rsquo;t make visitors wait around."),
        ],
        "g3_numbered": False,
        "g3_title": "Website Design That Works",
        "g3_sub": "Designed to attract attention, build trust and drive action.",
        "g3_intro": "A website should do more than look good. We combine thoughtful website design, user experience and search-friendly foundations to create a digital presence that helps your business make a stronger impression and generate more opportunities.",
        "g3_cards": [
            ("Clear Brand Positioning", "We structure your website so visitors quickly understand who you are, what you offer and why they should choose your business."),
            ("Conversion-Focused Layouts", "Strategic content sections, navigation and calls-to-action guide visitors naturally towards making an enquiry, booking a call or contacting your business."),
            ("Search-Ready Structure", "We build pages with clear headings, logical content structure, internal linking and SEO-friendly foundations to help search engines."),
            ("Experience That Builds Trust", "From polished layouts and consistent branding to clear messaging and intuitive navigation, every detail is designed to create confidence."),
        ],
        "g4_title": "A website built around what your customers need",
        "g4_intro": "Your website should do more than look good. We create clear, purposeful experiences that help visitors understand your business, trust your brand and take the next step.",
        "g4_cards": [
            ("Clear Messaging", "Make your services easy to understand with focused content and simple customer journeys."),
            ("Mobile-First Design", "Give customers a smooth experience across phones, tablets and desktop screens."),
            ("Built For Conversions", "Strategic calls-to-action, layouts and enquiry points help turn visitors into potential customers."),
            ("Ready To Grow", "Create a flexible website that can evolve as your business, services and online presence grow."),
        ],
        "faq": [
            ("How long does it take to build a website?", "Most Starter and Growth websites take around 3&ndash;6 weeks from approved design to launch. More complex or bespoke projects can take longer depending on functionality, integrations and the amount of content required."),
            ("Will you design the website around our existing branding?", "Absolutely. We&rsquo;ll work with your existing logo, colours, typography and brand guidelines. If your branding needs refinement, we can also discuss additional brand and design support."),
            ("Do I own my website after the project?", "Yes. Once the project has been paid in full, the website, design and supplied content belong to you."),
            ("Will I be able to edit the website myself?", "Yes. We build websites with practical content management in mind, so you can make everyday changes to text, images and pages. We&rsquo;ll also show you how everything works."),
            ("Can you help with website content?", "Yes. We can help structure, refine or create website content so your pages communicate your offer clearly and support your SEO and conversion goals."),
        ],
        "cta_intro": "get in touch and we&rsquo;ll reply within one business day with real next steps &mdash; not a scripted sales call.",
        "cta_points": [
            ("We reply within 1 business day", "No auto-reply chains &mdash; a real person from the team gets back to you."),
            ("A short, no-obligation call", "15&ndash;20 minutes to understand your business and what you actually need."),
            ("A clear, fixed-price proposal", "You&rsquo;ll know the scope and the cost upfront &mdash; no surprises later."),
        ],
    },
    "e-commerce-websites-design": {
        "slug": "e-commerce-websites-design",
        "nav_label": "E-commerce Websites",
        "name": "E-commerce Websites",
        "eyebrow": "Services · E-commerce Websites",
        "h1": "Online stores built to turn browsers into buyers",
        "lead": "an online shop that loads fast, works beautifully on a phone and makes checkout simple &mdash; so more of your visitors become paying customers.",
        "meta": "E-commerce website design for WooCommerce and Shopify. Mobile-first stores with fast checkout, built to sell across the USA, Canada, UK and Europe.",
        "ticks": ["Mobile-first shopping experience", "SEO-ready product pages", "Selling across USA, Canada, UK & Europe"],
        "badge": ("Secure checkout", "3 steps", "Cart &middot; Details &middot; Pay"),
        "hero_img": "ecommerce-website-design-hero.jpg",
        "hero_alt": "E-commerce website design showing a product catalogue and checkout",
        "split_img": "ecommerce-store-design-detail.webp",
        "split_alt": "Online store product and checkout page design detail",
        "why_title": "A store is a sales process, not a brochure.",
        "why_cards": [
            ("A store is a sales process, not a brochure.", "Every page has to move someone closer to paying. We design the whole journey &mdash; from first product view to order confirmation &mdash; not just how it looks."),
            ("Your customers decide in seconds.", "Shoppers judge a store in moments. Speed, clear pricing and visible trust signals do more for sales than fancy animation ever will."),
            ("You should run it, not fight it.", "We build the store so you can add products, change prices and process orders yourself, without calling a developer for every small change."),
            ("Built to be found, not just built.", "Product pages and categories are structured for search from day one, so your store isn&rsquo;t invisible after launch."),
        ],
        "core_title": "Everything a store needs to sell and keep selling.",
        "core_sub": "Design, speed, search visibility and checkout thinking, working together.",
        "core_intro": "A good online store does more than list products. We bring together design, speed, search visibility and checkout thinking to build a shop that feels trustworthy, is easy to run and gives customers every reason to complete their order &mdash; whether they&rsquo;re in New York, Toronto, London or Berlin.",
        "core_cards": [
            ("Custom store design", "Your store looks like your brand, not a template &mdash; with a homepage, collections and product pages designed to guide shoppers to what they came for."),
            ("Mobile-first shopping", "Most people browse on their phone, so we design the small screen first &mdash; easy-to-tap buttons, quick filters and a checkout that works with one thumb."),
            ("Checkout that converts", "We remove the steps and surprises that make people abandon their basket: clear delivery costs, guest checkout, trusted payment options and short forms."),
            ("Built for speed and search", "Fast pages and clean product and category structure help your products get found on Google, and stop slow loading from costing you sales."),
        ],
        "g3_numbered": False,
        "g3_title": "What Makes an Online Store Convert",
        "g3_sub": "Four things shoppers look for before they click &ldquo;Buy&rdquo;.",
        "g3_intro": "A store should do more than display products. We combine thoughtful design, clear product information and search-friendly foundations to create an online shop that earns trust quickly and makes buying feel easy.",
        "g3_cards": [
            ("Clear Product Presentation", "Strong images, clear descriptions, sizing, delivery information and reviews placed where shoppers need them, so they can decide with confidence."),
            ("Frictionless Checkout", "A short, simple path from basket to payment, with guest checkout and the payment methods customers in each country expect."),
            ("Search-Ready Catalogue", "Sensible categories, clean URLs, product schema and internal linking help search engines understand and rank your products."),
            ("Ready for Multiple Markets", "Currencies, shipping zones and tax settings can be set up for selling across the USA, Canada, the UK and Europe as you grow."),
        ],
        "g4_title": "Designed Around How People Actually Shop Online",
        "g4_intro": "Your customers don&rsquo;t want to hunt for information or guess what happens after they click &ldquo;Buy&rdquo;. We build stores that answer their questions early and make every next step obvious.",
        "g4_cards": [
            ("Answers Before the Basket", "Sizes, materials, delivery times and returns are visible before checkout, not after."),
            ("Comfortable on Any Screen", "Smooth browsing and checkout across phones, tablets and desktops."),
            ("Confidence at Every Step", "Secure payment options, reviews and clear policies help first-time buyers feel safe."),
            ("Room for More Products", "Add products, collections and new markets later without rebuilding the store."),
        ],
        "faq": [
            ("How long does it take to build an e-commerce website?", "Most online stores take around 6&ndash;10 weeks from approved design to launch, depending on the number of products, integrations (payments, shipping, stock) and how much content is ready. You&rsquo;ll get a clear timeline in your proposal."),
            ("Which platform do you build on &mdash; WooCommerce or Shopify?", "We recommend the platform that fits your products, budget and how you want to manage the store. WooCommerce suits businesses that want full control on WordPress; Shopify suits those who want a simple, hosted setup. We&rsquo;ll explain the trade-offs in plain English before you decide."),
            ("Can my store sell to customers in the USA, Canada, the UK and Europe?", "Yes. We can set up multiple currencies, shipping zones, tax and VAT options and the payment methods customers expect in each market. Tax rules vary by country, so we&rsquo;ll always suggest confirming the details with your accountant."),
            ("Will I be able to manage products and orders myself?", "Yes. We build the store so you can add products, change prices, manage stock and process orders without a developer, and we&rsquo;ll show you how during a handover session."),
            ("Can you help with product photos and descriptions?", "We can guide you on the images and descriptions that sell best, and help write or edit product copy. If you&rsquo;d like us to handle it, we&rsquo;ll include it in your quote."),
        ],
        "cta_intro": "tell us what you sell and where, and we&rsquo;ll reply within one business day with a clear view of what your store needs &mdash; no scripted sales call.",
        "cta_points": [
            ("We learn what you sell", "A real person replies within one business day with a few questions about your products, customers and markets."),
            ("A short store-planning call", "15&ndash;20 minutes on your goals, platform options and budget &mdash; with no obligation."),
            ("A clear, tailored quote", "You&rsquo;ll know the platform, timeline and cost before you commit."),
        ],
    },
    "seo-services": {
        "slug": "seo-services",
        "nav_label": "SEO Services",
        "name": "SEO Services",
        "eyebrow": "Services · SEO Services",
        "h1": "SEO that puts your business in front of customers ready to buy",
        "lead": "we help your website appear on Google when people search for what you sell &mdash; so you get more of the right visitors, not just more visitors.",
        "meta": "SEO services covering technical, content and local SEO. Plain-English monthly reporting, ranking businesses across the USA, Canada, UK and Europe.",
        "ticks": ["Technical, local & content SEO", "Plain-English monthly reports", "Ranking in USA, Canada, UK & Europe"],
        "badge": ("What we improve", "Technical &middot; Content &middot; Local", ""),
        "hero_img": "seo-services-hero.webp",
        "hero_alt": "SEO services dashboard showing search rankings improving",
        "split_img": "ecommerce-store-design-detail.webp",
        "split_alt": "SEO content and keyword strategy being planned on screen",
        "why_title": "Rankings aren&rsquo;t the goal. Customers are.",
        "why_cards": [
            ("Rankings aren&rsquo;t the goal. Customers are.", "We measure success by enquiries, calls and sales, not by how many keywords we can list in a report."),
            ("We tell you what&rsquo;s realistic.", "Some searches can be won in months, others take a year or more. We show you which is which before you commit."),
            ("No secret tricks.", "We don&rsquo;t buy spammy links or hide behind jargon. Everything we do follows Google&rsquo;s guidelines, and we explain it in plain English."),
            ("Reports you&rsquo;ll actually read.", "A short monthly summary of what we did, what changed and what happens next &mdash; no 40-page data dumps."),
        ],
        "core_title": "Four things that decide whether Google sends you customers.",
        "core_sub": "Technical health, useful content, local presence and trusted links.",
        "core_intro": "SEO isn&rsquo;t one trick. It&rsquo;s technical health, useful content, local presence and trusted links working together. We look after all four for businesses across the USA, Canada, the UK and Europe, so search engines understand your website and customers can find it.",
        "core_cards": [
            ("Technical SEO", "We fix the behind-the-scenes issues &mdash; speed, crawl errors, mobile usability and site structure &mdash; that stop Google reading your website properly."),
            ("Content and on-page SEO", "We plan and optimise pages around the words your customers actually search, so each page has a clear job and a clear reason to rank."),
            ("Local SEO", "We optimise your Google Business Profile, local listings and location pages so people nearby &mdash; in every city you serve &mdash; can find you."),
            ("Authority and link building", "We earn relevant, quality links and mentions that show search engines your business is trusted &mdash; no spammy shortcuts."),
        ],
        "g3_numbered": True,
        "g3_title": "How We Build Your Search Visibility",
        "g3_sub": "A clear process, from first audit to monthly reporting.",
        "g3_intro": "Good SEO is a long-term asset. We combine technical fixes, useful content and local visibility to build search performance that keeps working month after month, not a short-lived spike.",
        "g3_cards": [
            ("Audit and Opportunity Research", "We review your website, competitors and search demand to find the quickest wins and the biggest long-term opportunities."),
            ("Keyword and Content Strategy", "Each page is planned around what customers search for and what they need to know before they get in touch."),
            ("Technical and On-Page Fixes", "Speed, structure, headings, internal links and structured data are improved so search engines can crawl and understand your pages."),
            ("Tracking and Reporting", "We track rankings, traffic and &mdash; most importantly &mdash; enquiries, so you can see what SEO is doing for your business."),
        ],
        "g4_title": "SEO Shaped Around the Way Your Customers Search",
        "g4_intro": "Your customers don&rsquo;t want to hunt for information or guess what to do next. We build pages that answer their questions and make every next step obvious.",
        "g4_cards": [
            ("Every Page Has a Search Purpose", "Every page gives the searcher what they want, whether that&rsquo;s information, comparison or a ready-to-buy enquiry."),
            ("Local and International Reach", "Target the cities and countries you serve, with the right language, spelling and location signals."),
            ("Pages That Convert", "Visitors from Google land on pages with a clear next step &mdash; call, book or enquire."),
            ("Room for New Services", "A strong foundation that supports new services, locations and content as you expand."),
        ],
        "faq": [
            ("How long does SEO take to work?", "SEO is a long-term investment. Many businesses see early movement within 3&ndash;4 months, with stronger results building over 6&ndash;12 months, depending on competition, your website and your starting point. We&rsquo;ll set realistic expectations before we begin."),
            ("Can you guarantee first-page rankings?", "No &mdash; and be cautious of any agency that does. Nobody outside Google controls its results. What we can do is follow best practice, focus on the searches most likely to bring customers and report honestly on progress."),
            ("Can you help my business rank in more than one country?", "Yes. We work with businesses across the USA, Canada, the UK and Europe, and adapt keywords, spelling, local listings and location pages for each market you want to reach."),
            ("What&rsquo;s the difference between SEO and local SEO?", "SEO helps your website rank for searches anywhere. Local SEO focuses on &ldquo;near me&rdquo; and city-based searches and your Google Business Profile, which matters most if customers visit you or you serve a specific area."),
            ("Will I get reports I can understand?", "Yes. Every month you&rsquo;ll receive a plain-English report covering what we did, how your visibility and enquiries changed and what&rsquo;s planned next."),
        ],
        "cta_intro": "tell us about your website and who you want to reach, and we&rsquo;ll reply within one business day with honest next steps.",
        "cta_points": [
            ("We read your message", "A real person from the team replies within one business day with a few questions about your business and goals."),
            ("A short SEO discovery call", "15&ndash;20 minutes about your customers, your competitors and where you want to be found."),
            ("A clear plan and price", "You&rsquo;ll see what we&rsquo;d do, in what order and what it costs &mdash; before you commit to anything."),
        ],
    },
    "aeo-ai-search": {
        "slug": "aeo-ai-search",
        "nav_label": "AEO (AI Search)",
        "name": "AEO (AI Search)",
        "eyebrow": "Services · AEO (AI Search)",
        "h1": "Be the answer when your customers ask AI",
        "lead": "AEO &mdash; answer engine optimisation &mdash; helps AI tools like ChatGPT, Google AI Overviews and Perplexity understand your business, so they&rsquo;re more likely to mention you when people ask questions.",
        "meta": "AEO (Answer Engine Optimisation) to help ChatGPT, Google AI Overviews and Perplexity understand and recommend your business across the USA, Canada, UK and Europe.",
        "ticks": ["Built for AI and traditional search", "Clear, answer-ready content", "Visible in USA, Canada, UK & Europe"],
        "badge": ("Customers ask AI", "&ldquo;Who can help grow my business online?&rdquo;", "We make your answer easy to find"),
        "hero_img": "aeo-ai-search-hero.webp",
        "hero_alt": "AI chat interface showing an answer engine recommending a business",
        "split_img": "aeo-ai-search-detail.jpg",
        "split_alt": "Structured content and schema markup being reviewed for AI search",
        "why_title": "Customers are asking AI, not just searching.",
        "why_cards": [
            ("Customers are asking AI, not just searching.", "More people now ask AI tools for recommendations instead of scrolling through results. If AI doesn&rsquo;t understand your business, it can&rsquo;t suggest it."),
            ("This is SEO&rsquo;s next chapter, not a replacement.", "AEO builds on solid SEO. We strengthen both, so you&rsquo;re visible in Google&rsquo;s results and in the answers AI tools give."),
            ("Clarity beats cleverness.", "AI tools favour clear, factual, well-structured information. We make your content easy to understand, quote and trust."),
            ("We&rsquo;re honest about what&rsquo;s possible.", "Nobody can guarantee an AI tool will mention you. We focus on what improves your chances, and we track it openly."),
        ],
        "core_title": "How we get your business into AI answers.",
        "core_sub": "Preparing your website and content to be clear, credible and easy to cite.",
        "core_intro": "AI search tools pull answers from websites they can understand and trust. We prepare your website, content and online presence so your business is clear, credible and easy to cite &mdash; for customers across the USA, Canada, the UK and Europe.",
        "core_cards": [
            ("Answer-ready content", "We rewrite and structure your pages to answer the questions customers really ask, in clear, direct language that AI tools can quote."),
            ("Structured data and schema", "We add behind-the-scenes markup that tells search engines and AI tools exactly who you are, what you offer and where you operate."),
            ("Brand and entity consistency", "We make sure your business name, services, locations and details match across your website, profiles and directories, so AI tools describe you correctly."),
            ("AI visibility tracking", "We check how your brand appears in AI answers for the questions that matter, and report changes in plain English."),
        ],
        "g3_numbered": True,
        "g3_title": "How We Make Your Brand AI-Ready",
        "g3_sub": "Helping AI tools understand, trust and mention your business.",
        "g3_intro": "AEO isn&rsquo;t a trick. It&rsquo;s the discipline of making your business easy to understand &mdash; for people and for machines. Clear answers, trustworthy signals and well-structured pages give you a stronger chance of being included.",
        "g3_cards": [
            ("Question Research", "We find the real questions your customers ask AI tools and search engines, from &ldquo;who is the best&hellip;&rdquo; to &ldquo;how much does it cost&rdquo;."),
            ("FAQ and Answer Content", "Dedicated pages and sections give clear, direct answers, written for customers first and machines second."),
            ("Trust and Authority Signals", "Reviews, credentials, author details, citations and consistent listings strengthen why you should be trusted."),
            ("Schema and Technical Readiness", "Structured data, clean site architecture and fast pages help AI and search systems read your website."),
        ],
        "g4_title": "Content Written for the Way People Ask AI",
        "g4_intro": "People ask AI tools full questions, in natural language, and expect a straight answer. We build your content around those conversations, so your business is part of the answer.",
        "g4_cards": [
            ("Natural-Language Answers", "Content written the way customers actually ask and speak."),
            ("Built for Every AI Tool", "Designed to support visibility across Google AI Overviews, ChatGPT, Perplexity, Gemini and Microsoft Copilot."),
            ("Clear About Where You Operate", "Precise location and service details for customers in the USA, Canada, the UK and Europe."),
            ("Kept Current as AI Changes", "AI search is evolving fast, so your content and data stay structured, up to date and adaptable."),
        ],
        "faq": [
            ("What is AEO?", "AEO stands for Answer Engine Optimisation. It&rsquo;s the practice of structuring your website and content so AI tools and answer engines &mdash; such as ChatGPT, Google AI Overviews, Perplexity and Microsoft Copilot &mdash; can understand your business and include it in their answers."),
            ("How is AEO different from SEO?", "SEO helps your pages rank in a list of search results. AEO helps your business be understood and referenced inside a direct answer. They share the same foundations &mdash; quality content, clear structure and trust &mdash; so we treat them as one joined-up strategy."),
            ("Can you guarantee ChatGPT or Google AI will mention my business?", "No. AI tools decide their own answers and nobody outside them can control that. What we can do is improve your clarity, structure and credibility so you&rsquo;re more likely to be included, and measure how that changes."),
            ("Does AEO work for businesses outside the USA?", "Yes. AI tools answer questions in every market, so we help businesses in the USA, Canada, the UK and Europe make their locations, services and language clear for the customers they want to reach."),
            ("How long does AEO take to show results?", "Some improvements, such as better-structured content, can be picked up within weeks, but changes in AI answers usually build over several months. We agree how we&rsquo;ll measure progress at the start."),
        ],
        "cta_intro": "tell us what you do and who you serve, and we&rsquo;ll reply within one business day with a straight-talking view on where to start.",
        "cta_points": [
            ("We reply within 1 business day", "A real person reads your message and comes back with a few questions about your business and customers."),
            ("A short AI search call", "15&ndash;20 minutes on the questions your customers ask and where you&rsquo;d like to appear."),
            ("A plain-English plan", "What we&rsquo;d change, in what order, and how we&rsquo;d measure whether it&rsquo;s working."),
        ],
    },
    "ppc-digital-advertising": {
        "slug": "ppc-digital-advertising",
        "nav_label": "PPC & Digital Advertising",
        "name": "PPC & Digital Advertising",
        "eyebrow": "Services · PPC & Digital Advertising",
        "h1": "Advertising that brings customers, not just clicks",
        "lead": "we plan, run and improve your paid ads across the platforms your customers use, and track your results &mdash; so you can see what your budget is actually bringing in.",
        "meta": "PPC and digital advertising management across Google Ads, Meta and LinkedIn, tracked to enquiries and sales for businesses in the USA, Canada, UK and Europe.",
        "ticks": ["Google, Meta & LinkedIn campaigns", "Tracked to enquiries and sales", "Advertising in USA, Canada, UK & Europe"],
        "badge": ("Where we advertise", "Google &middot; Meta &middot; LinkedIn", ""),
        "hero_img": "ppc-digital-advertising-hero.webp",
        "hero_alt": "Paid advertising campaign dashboard showing clicks and conversions",
        "split_img": "ppc-digital-advertising-detail.webp",
        "split_alt": "Digital advertising creative and targeting being planned on screen",
        "why_title": "Clicks aren&rsquo;t customers.",
        "why_cards": [
            ("Clicks aren&rsquo;t customers.", "Cheap traffic that never buys drains budget. We target people who are looking for what you sell, and cut spend on those who aren&rsquo;t."),
            ("Every channel plays a different role.", "Search catches people ready to buy, social finds people who don&rsquo;t know you yet and retargeting brings back those who nearly did. We plan them as one system."),
            ("We agree the plan before the spend.", "Goals, audiences and a budget are settled first, then we launch &mdash; no guessing and no throwing money at every platform."),
            ("You see every dollar.", "Ad spend, our fee and your results sit side by side in one report &mdash; nothing hidden and nothing rounded away."),
        ],
        "core_title": "Where your ad budget goes &mdash; and what comes back.",
        "core_sub": "Strategy, setup, creative, tracking and ongoing optimisation.",
        "core_intro": "Paid advertising can grow a business quickly &mdash; or drain a budget just as fast. We manage the whole process: strategy, setup, creative, tracking and ongoing optimisation, for businesses advertising across the USA, Canada, the UK and Europe.",
        "core_cards": [
            ("Search and display advertising", "We put your business in front of people actively searching for your services, and remind others as they browse."),
            ("Paid social advertising", "We run targeted campaigns on Meta (Facebook and Instagram), LinkedIn and other platforms to reach the right audience where they spend their time."),
            ("Retargeting", "We bring back people who visited your website but didn&rsquo;t get in touch, with reminders that feel relevant rather than annoying."),
            ("Conversion tracking and reporting", "We set up tracking so you can see which ads lead to calls, forms and sales &mdash; not just clicks."),
        ],
        "g3_numbered": True,
        "g3_title": "How We Run Your Campaigns",
        "g3_sub": "From first plan to ongoing optimisation.",
        "g3_intro": "Great campaigns aren&rsquo;t about the biggest budget. They combine the right audience, a clear message and a landing page that makes the next step easy &mdash; then we test and improve continuously.",
        "g3_cards": [
            ("Audience and Channel Planning", "We choose platforms and audiences based on where your customers are and what they&rsquo;re ready to do."),
            ("Creative That Gets Attention", "Clear ad copy and visuals built around one message and one action, tested against alternatives."),
            ("Landing Pages That Convert", "Ads send people to pages built for one job &mdash; enquiry, booking or purchase &mdash; so every click counts."),
            ("Ongoing Optimisation", "We review results regularly, pause what isn&rsquo;t working and put more budget behind what is."),
        ],
        "g4_title": "Ads Shaped Around Real Customer Intent",
        "g4_intro": "Your customers see hundreds of ads a day. We focus on being useful and relevant at the moment they&rsquo;re ready to act, with messages that speak to real needs in each market you serve.",
        "g4_cards": [
            ("Say It Clearly", "Ads that state what you do, who it&rsquo;s for and what to do next."),
            ("Right Person, Right Place", "Reach customers by location, interest, intent and behaviour across the USA, Canada, the UK and Europe."),
            ("Every Campaign Has a Goal", "Each one is tied to a measurable result &mdash; enquiries, bookings or sales."),
            ("Scale Only What Works", "Budgets rise gradually, and only behind campaigns that have proved themselves."),
        ],
        "faq": [
            ("How much should I spend on advertising?", "It depends on your industry, competition and goals. We&rsquo;ll recommend a starting budget based on realistic costs and expected enquiries, and you stay in control of what you spend. Ad spend is paid to the advertising platforms and is separate from our management fee."),
            ("How quickly will I see results?", "Ads can start bringing traffic within days of launch, but the first few weeks are for learning what works. Most campaigns become more efficient after 6&ndash;8 weeks of testing and optimisation."),
            ("Which platforms do you advertise on?", "We typically use Google Ads, Microsoft Advertising, Meta (Facebook and Instagram) and LinkedIn, and recommend only the ones that fit your customers and budget."),
            ("Can you run one campaign across several countries?", "Yes. We set up location targeting, language and currency for the USA, Canada, the UK and Europe, and can advise on regional requirements such as cookie consent, so each market sees the right message."),
            ("How will I know if my ads are working?", "We track calls, form submissions and sales &mdash; not just clicks &mdash; and send a clear report showing spend, results and what we&rsquo;ll do next."),
        ],
        "cta_intro": "tell us your goals and a rough budget, and we&rsquo;ll reply within one business day with a sensible starting plan.",
        "cta_points": [
            ("We review your goals", "A real person replies within one business day with a few questions about your customers and what you want ads to achieve."),
            ("A short ad strategy call", "15&ndash;20 minutes on channels, budget and how we&rsquo;d measure success &mdash; with no obligation."),
            ("A campaign plan with clear costs", "You&rsquo;ll see the channels, the budget split and our management fee before anything launches."),
        ],
    },
    "social-media": {
        "slug": "social-media",
        "nav_label": "Social Media Marketing",
        "name": "Social Media Marketing",
        "eyebrow": "Services · Social Media Marketing",
        "h1": "Social media that builds trust and brings enquiries",
        "lead": "we plan, create and manage your social media so your business shows up consistently, looks professional and gives followers a reason to get in touch.",
        "meta": "Social media marketing and management &mdash; content planning, on-brand posting and community replies for businesses in the USA, Canada, UK and Europe.",
        "ticks": ["Content planned around your goals", "Consistent, on-brand posting", "Content for USA, Canada, UK & Europe"],
        "badge": ("What we handle", "Planning &middot; Posting &middot; Replies", ""),
        "hero_img": "social-media-marketing-hero.webp",
        "hero_alt": "Social media content calendar and posts being planned",
        "split_img": "social-media-marketing-detail.webp",
        "split_alt": "Social media graphics and captions being designed",
        "why_title": "Nobody has time to do it well.",
        "why_cards": [
            ("Nobody has time to do it well.", "Posting slips down the list when you&rsquo;re busy running a business. We make it someone&rsquo;s actual job, so your channels stay active."),
            ("Random posts don&rsquo;t build trust.", "Customers notice when a page is patchy or off-brand. A clear voice and steady rhythm make your business look established."),
            ("Followers aren&rsquo;t the finish line.", "A big following that never enquires doesn&rsquo;t pay the bills. We plan every post around what you want people to do next."),
            ("You stay in control.", "You approve the content plan before anything goes live, and we always explain what we&rsquo;re posting and why."),
        ],
        "core_title": "Your social media, handled from plan to post.",
        "core_sub": "Strategy, content and day-to-day management, all in one place.",
        "core_intro": "Social media works when it&rsquo;s consistent, on-brand and built around your customers. We handle the strategy, content and day-to-day management for businesses across the USA, Canada, the UK and Europe, so you can focus on running your business.",
        "core_cards": [
            ("Social strategy and planning", "We choose the right platforms, topics and posting rhythm for your audience, so your effort goes where it counts."),
            ("Content creation", "We design graphics, write captions and plan short-form video ideas that look professional and sound like you."),
            ("Community management", "We respond to comments and messages and flag genuine enquiries to you quickly, so no potential customer is left waiting."),
            ("Reporting and improvement", "We review what works each month and adjust the plan, so your content keeps getting better."),
        ],
        "g3_numbered": True,
        "g3_title": "The Four Habits That Make Social Media Work",
        "g3_sub": "Small, consistent things that add up to trust.",
        "g3_intro": "Social media isn&rsquo;t just about followers. Done well, it helps people get to know your business, trust it and take the next step. We combine consistent content with clear calls to action so activity turns into real conversations.",
        "g3_cards": [
            ("A Clear Brand Voice", "A tone and style that feel like your business, so people recognise you at a glance."),
            ("A Consistent Content Calendar", "Planned posts and campaigns keep your channels active without last-minute scrambling."),
            ("Engagement That Builds Trust", "Timely replies and helpful content show that real people are behind the brand."),
            ("Social That Supports Sales", "Links, offers and calls to action connect your posts to your website and your enquiries."),
        ],
        "g4_title": "Content Your Audience Actually Wants to See",
        "g4_intro": "Your audience follows brands that are useful, relevant and human. We research what your customers respond to in each market and build content that fits.",
        "g4_cards": [
            ("Based on Real Questions", "Posts built from what customers actually ask, care about and struggle with."),
            ("On the Right Platforms", "Focus on the channels &mdash; Instagram, Facebook, LinkedIn, TikTok or others &mdash; where your customers actually are."),
            ("Every Post Has a Purpose", "Clear calls to action that turn attention into conversations."),
            ("Ready for Paid Social", "When you want faster reach, we can add paid social campaigns to what&rsquo;s already working."),
        ],
        "faq": [
            ("Which social media platforms should my business be on?", "It depends on where your customers spend time. Service businesses often do well on Facebook, Instagram and LinkedIn, while product brands may add TikTok or Pinterest. We&rsquo;ll recommend the few that make sense rather than spreading you thin."),
            ("How often will you post?", "We agree a posting schedule that fits your goals and budget &mdash; typically a few high-quality posts a week rather than daily filler. You&rsquo;ll see the plan in advance."),
            ("Will I approve content before it&rsquo;s published?", "Yes. You&rsquo;ll receive the content calendar for approval before anything goes live, so nothing is posted without your say-so."),
            ("Should my content be different for the USA, UK and Europe?", "Often, yes. Spelling, humour, timing and references vary between markets. For businesses in the USA, Canada, the UK and Europe we adapt the tone and schedule for each audience rather than posting the same thing everywhere."),
            ("Can social media generate enquiries, or is it only for awareness?", "Both. Organic social builds trust and awareness, and with clear calls to action it can also generate enquiries. If you want faster results, we can add paid social ads to the mix."),
        ],
        "cta_intro": "tell us about your business and your audience, and we&rsquo;ll reply within one business day with ideas for where to start.",
        "cta_points": [
            ("We get to know your brand", "A real person replies within one business day with a few questions about your business, audience and current channels."),
            ("A short social media call", "15&ndash;20 minutes on platforms, content ideas and posting rhythm &mdash; with no obligation."),
            ("A content plan and quote", "You&rsquo;ll see what we&rsquo;d post, how often and what it costs before you commit."),
        ],
    },
    "google-ads": {
        "slug": "google-ads",
        "nav_label": "Google Ads",
        "name": "Google Ads",
        "eyebrow": "Services · Google Ads",
        "h1": "Google Ads that put you in front of customers the moment they search",
        "lead": "we set up and manage your Google Ads so your business appears when people search for what you offer &mdash; and we track every click through to real enquiries and sales.",
        "meta": "Google Ads management &mdash; Search, Shopping and Performance Max campaigns with conversion tracking, for businesses across the USA, Canada, UK and Europe.",
        "ticks": ["Search, Shopping and Performance Max", "Conversion tracking set up", "Campaigns in USA, Canada, UK & Europe"],
        "badge": ("What we manage", "Search &middot; Shopping &middot; Tracking", ""),
        "hero_img": "google-ads-hero.webp",
        "hero_alt": "Google Ads campaign dashboard showing search results performance",
        "split_img": "google-ads-detail.webp",
        "split_alt": "Google Ads keyword and bid management being reviewed",
        "why_title": "Google&rsquo;s defaults aren&rsquo;t built around you.",
        "why_cards": [
            ("Google&rsquo;s defaults aren&rsquo;t built around you.", "Automated suggestions often push you to spend more. We manage the account around your goals, not the platform&rsquo;s default settings."),
            ("Every click is accounted for.", "We set up tracking first, so you know which keywords, ads and campaigns lead to enquiries &mdash; and which just cost money."),
            ("Intent matters more than volume.", "We target searches from people ready to act and block irrelevant ones, so your budget goes to customers rather than curiosity."),
            ("Honest fees, honest reporting.", "You&rsquo;ll see your ad spend, our fee and your results in one plain-English report &mdash; no hidden charges, no jargon."),
        ],
        "core_title": "What we set up, fix and manage in your account.",
        "core_sub": "Account structure, keywords, landing pages and tracking, all handled.",
        "core_intro": "Google Ads is powerful, but it&rsquo;s easy to overspend without expert setup. We handle everything &mdash; account structure, keyword research, ad copy, landing pages, tracking and ongoing optimisation &mdash; for businesses advertising across the USA, Canada, the UK and Europe.",
        "core_cards": [
            ("Google Search campaigns", "We show your ads to people actively searching for your services, in the cities and countries you want to reach."),
            ("Shopping and Performance Max", "For online stores, we set up product ads and automated campaigns that can appear across Google Search, Shopping, YouTube and more."),
            ("Landing pages and conversion tracking", "We make sure each ad lands on a page built to convert, and set up tracking for calls, forms and purchases."),
            ("Ongoing optimisation", "We monitor search terms, bids and budgets regularly, cutting waste and putting more behind what works."),
        ],
        "g3_numbered": True,
        "g3_title": "How We Manage Your Google Ads",
        "g3_sub": "From account audit to steadily lower cost per enquiry.",
        "g3_intro": "Successful Google Ads campaigns combine the right keywords, clear ads and pages that convert. We build each element around your goals, then test and refine so your budget works harder.",
        "g3_cards": [
            ("Account Audit and Setup", "A clean account structure with the right settings, so money isn&rsquo;t wasted from day one."),
            ("Keywords and Ad Copy", "Intent-led keywords and clear ad copy that speaks to what customers are searching for."),
            ("Conversion Tracking", "Calls, forms and sales tracked accurately, so decisions are based on real results."),
            ("Budget and Bid Management", "Regular adjustments to bids, budgets and targeting to lower your cost per enquiry over time."),
        ],
        "g4_title": "Campaigns Built on What People Search For",
        "g4_intro": "Every search is a customer telling you what they want. We build campaigns around those searches &mdash; by location, device and intent &mdash; so your ads are relevant, helpful and hard to ignore.",
        "g4_cards": [
            ("Matched to Search Intent", "Ads that fit what people want at the moment they search."),
            ("Targeted to Where You Work", "Show your ads in the countries, regions and cities where you can serve customers."),
            ("Every Ad Leads Somewhere", "Ads, landing pages and tracking all lead to one measurable action."),
            ("Grow the Winners", "As results prove out, budgets grow and you expand into new services and markets."),
        ],
        "faq": [
            ("How much does Google Ads cost?", "You pay Google for clicks (your ad spend) and a management fee to us. Ad spend depends on your industry, competition and location &mdash; we&rsquo;ll recommend a starting budget based on realistic costs before you commit."),
            ("How long before I see results from Google Ads?", "Ads can generate traffic almost immediately, but it usually takes a few weeks of data to optimise properly. We review results regularly and share what we learn."),
            ("Can you run Google Ads in several countries at once?", "Yes. We set up location, language and currency targeting for the USA, Canada, the UK and Europe, and can run separate campaigns for each country so the message and budget suit each market."),
            ("What&rsquo;s the difference between Google Ads and SEO?", "Google Ads gives you paid placement, so you can appear straight away and pay for each click. SEO builds organic rankings that take longer but keep working without paying per click. Many businesses use both."),
            ("Will I own my Google Ads account?", "Yes. Your ad account is set up in your name and you keep full access to it and your data."),
        ],
        "cta_intro": "tell us what you sell and where, and we&rsquo;ll reply within one business day with a clear idea of how we&rsquo;d set up your campaigns.",
        "cta_points": [
            ("We look at your goals", "A real person replies within one business day with a few questions about your services, locations and budget."),
            ("A short Google Ads call", "15&ndash;20 minutes on keywords, budget and tracking &mdash; with no obligation."),
            ("A setup plan with clear fees", "You&rsquo;ll see how we&rsquo;d structure the account and what our management fee is before you commit."),
        ],
    },
}

SERVICE_ORDER = ["website-design", "e-commerce-websites-design", "seo-services", "aeo-ai-search",
                  "ppc-digital-advertising", "social-media", "google-ads"]

# A numbered "how we work" process for the two services whose page doesn't
# already carry one (the rest have this baked into their g3 section).
PROCESS_CONTENT = {
    "website-design": {
        "title": "How We Build Your Website",
        "sub": "From first conversation to launch day.",
        "intro": "Every website follows the same clear process, so you always know what happens next and when.",
        "steps": [
            ("Discovery &amp; Strategy", "We learn about your business, audience and goals, and agree the scope, sitemap and timeline before any design starts."),
            ("Design", "We design your key pages around your brand and customer journey, and refine them with your feedback until they&rsquo;re ready to build."),
            ("Build &amp; Content", "Pages are built, tested across devices, and populated with your content, images and tracking."),
            ("Launch &amp; Handover", "We launch your site, show you how to make everyday edits, and stay on hand for launch support."),
        ],
    },
    "e-commerce-websites-design": {
        "title": "How We Build Your Online Store",
        "sub": "From first conversation to your first sale.",
        "intro": "Every store follows the same clear process, so you always know what happens next and when.",
        "steps": [
            ("Discovery &amp; Platform Choice", "We learn what you sell and who to, then recommend WooCommerce or Shopify based on your products and budget."),
            ("Store Design", "We design your homepage, collections and product pages around your brand and how customers shop."),
            ("Build, Payments &amp; Shipping", "We build the store, connect payment methods, shipping and tax settings, and load your products."),
            ("Launch &amp; Handover", "We launch your store, show you how to manage products and orders, and stay on hand after go-live."),
        ],
    },
}

def get_process_content(key):
    """Returns (title, sub, intro, steps) for a service's numbered process,
    whether it's a dedicated PROCESS_CONTENT entry or the service's own
    built-in g3 process section. Returns (None, None, None, None) if the
    service has no process content at all."""
    if key in PROCESS_CONTENT:
        p = PROCESS_CONTENT[key]
        return p["title"], p["sub"], p["intro"], p["steps"]
    s = SERVICES[key]
    if s.get("g3_numbered"):
        return s["g3_title"], s["g3_sub"], s["g3_intro"], s["g3_cards"]
    return None, None, None, None

# Which services get location (city) landing pages, and the local copy for each.
LOCATION_SERVICE_KEY = {
    "Website Design": "website-design",
    "SEO Services": "seo-services",
}
LOCAL_COPY = {
    "website-design": {
        "reasons": [
            "Local market knowledge of {city} and the wider {region_full}",
            "Mobile-first, fast-loading websites that turn local visitors into enquiries",
            "One team for design, SEO and everything else digital, so nothing gets lost between suppliers",
        ],
        "faq": [
            ("Do you build websites for businesses in {city}?", "Yes. We design and build websites for businesses across {city} and the wider {region_full}, using the same process we use everywhere &mdash; mobile-first, SEO-ready and built around your customers."),
            ("How long does a website for a {city} business take to launch?", "Most Starter and Growth websites take around 3&ndash;6 weeks from approved design to launch, whether you&rsquo;re based in {city} or anywhere else we work."),
        ],
    },
    "seo-services": {
        "reasons": [
            "Local SEO for {city} &mdash; Google Business Profile, maps and location pages, not just national rankings",
            "Technical and content SEO that helps {city} customers find you first",
            "Plain-English monthly reporting so you can see real progress, not just jargon",
        ],
        "faq": [
            ("Can you help my {city} business rank locally?", "Yes. Alongside national SEO, we optimise your Google Business Profile, local listings and location pages so people searching in {city} find you first."),
            ("Do you work with businesses outside {city} too?", "Yes. We work with businesses across {region_full} and internationally, adapting keywords, spelling and local listings for each market."),
        ],
    },
}
INTRO_TEMPLATES = [
    "Businesses in {city} need more than a generic {service_lower} &mdash; they need a team that understands the local market and delivers real results. {lead_cap}",
    "If you run a business in {city}, {region_full}, your {service_lower} should work as hard as you do. {lead_cap}",
    "{city} is a competitive market, and a strong {service_lower} strategy helps you stand out from nearby competitors. {lead_cap}",
]
REGION_FULL = {"USA": "the United States", "Canada": "Canada", "UK": "the United Kingdom", "Europe": "Europe"}
CITY_COUNTRY_OVERRIDE = {"Berlin": "Germany"}

# ---------------------------------------------------------------------------
# HEADER / FOOTER
# ---------------------------------------------------------------------------
def curated_city_locations(service_key, limit=7):
    by_city = {l["city"]: l for l in ALL_LOCATIONS if l["service_key"] == service_key}
    picks = [by_city[c] for c in CURATED_NAV_CITIES if c in by_city][:limit]
    if len(picks) < limit:
        for l in ALL_LOCATIONS:
            if l["service_key"] == service_key and l not in picks:
                picks.append(l)
                if len(picks) >= limit:
                    break
    return picks

DIGITAL_MARKETING_KEYS = ["e-commerce-websites-design", "aeo-ai-search", "ppc-digital-advertising", "google-ads"]

def _city_dropdown(root, service_key, bare=True):
    # NOTE: bare <a> tags (no <li>) for the desktop dropdown - it sits inside
    # a <div> that is itself inside a <li>, and an <li> start tag auto-closes
    # any open ancestor <li> (even through a <div>), which would otherwise
    # hoist these links out of the dropdown and into the main nav row.
    locs = curated_city_locations(service_key)
    tag_open, tag_close = ("", "") if bare else ('<li class="pb-mobile-sub">', "</li>")
    links = "".join('%s<a href="%s%s.html">%s</a>%s' % (tag_open, root, l["folder"], l["city"], tag_close) for l in locs)
    more = '%s<a href="%ssitemap.html#%s">View all locations</a>%s' % (tag_open, root, service_key, tag_close)
    return links + more

def _digital_marketing_dropdown(root, bare=True):
    tag_open, tag_close = ("", "") if bare else ('<li class="pb-mobile-sub">', "</li>")
    return "".join(
        '%s<a href="%s%s.html">%s</a>%s' % (tag_open, root, k, SERVICES[k]["nav_label"], tag_close)
        for k in DIGITAL_MARKETING_KEYS
    )

def header_html(root):
    wd_sub = _city_dropdown(root, "website-design")
    seo_sub = _city_dropdown(root, "seo-services")
    dm_sub = _digital_marketing_dropdown(root)
    wd_sub_m = _city_dropdown(root, "website-design", bare=False)
    seo_sub_m = _city_dropdown(root, "seo-services", bare=False)
    dm_sub_m = _digital_marketing_dropdown(root, bare=False)
    chevron = '<svg class="pb-i" viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
    return """
<header class="pb-header">
  <div class="pb-wrap pb-header__bar">
    <a class="pb-header__logo" href="%(root)sindex.html">
      <img src="%(root)simages/logo.png" alt="Pinky Brain Digital logo" width="192" height="64">
    </a>
    <nav class="pb-nav" aria-label="Primary">
      <ul class="pb-nav__list">
        <li class="pb-has-sub">
          <a href="%(root)swebsite-design.html">Website Design %(chevron)s</a>
          <div class="pb-nav__sub">%(wd_sub)s</div>
        </li>
        <li class="pb-has-sub">
          <a href="%(root)sseo-services.html">SEO Services %(chevron)s</a>
          <div class="pb-nav__sub">%(seo_sub)s</div>
        </li>
        <li><a href="%(root)ssocial-media.html">Social Media</a></li>
        <li class="pb-has-sub">
          <a href="%(root)sindex.html#pbs-services">Digital Marketing %(chevron)s</a>
          <div class="pb-nav__sub">%(dm_sub)s</div>
        </li>
        <li><a href="%(root)sindex.html#pbs-about-title">About Us</a></li>
        <li><a href="%(root)scontact-us.html">Contact</a></li>
      </ul>
      <a class="pb-btn pb-btn--dark pb-nav__cta" href="%(root)scontact-us.html">Book a free consultation</a>
      <button class="pb-burger" aria-label="Open menu"><svg class="pb-i" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </nav>
  </div>
</header>
<div class="pb-mobile-nav">
  <div class="pb-mobile-nav__top">
    <a href="%(root)sindex.html"><img src="%(root)simages/logo.png" alt="Pinky Brain Digital logo" width="138" height="46"></a>
    <button class="pb-mobile-nav__close" aria-label="Close menu"><svg class="pb-i" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
  </div>
  <ul>
    <li><a href="%(root)sindex.html">Home</a></li>
    <li><a href="%(root)swebsite-design.html">Website Design</a></li>
    %(wd_sub_m)s
    <li><a href="%(root)sseo-services.html">SEO Services</a></li>
    %(seo_sub_m)s
    <li><a href="%(root)ssocial-media.html">Social Media</a></li>
    <li><a href="%(root)sindex.html#pbs-services">Digital Marketing</a></li>
    %(dm_sub_m)s
    <li><a href="%(root)sindex.html#pbs-about-title">About Us</a></li>
    <li><a href="%(root)scontact-us.html">Contact</a></li>
  </ul>
  <a class="pb-btn pb-btn--dark" href="%(root)scontact-us.html">Book a free consultation</a>
</div>
""" % {"root": root, "wd_sub": wd_sub, "seo_sub": seo_sub, "dm_sub": dm_sub,
       "wd_sub_m": wd_sub_m, "seo_sub_m": seo_sub_m, "dm_sub_m": dm_sub_m, "chevron": chevron}

def footer_html(root):
    services_links = "".join(
        '<li><a href="%s%s.html">%s</a></li>' % (root, s, SERVICES[s]["nav_label"])
        for s in SERVICE_ORDER
    )
    return """
<footer class="pb-footer">
  <div class="pb-wrap">
    <div class="pb-footer__brand">
      <img src="%(root)simages/logo.png" alt="Pinky Brain Digital logo" width="174" height="58" style="filter:brightness(0) invert(1)">
      <p>Most businesses juggle a web designer, an SEO freelancer, a social media manager and an ads specialist, and nobody owns the results. We bring every digital discipline into one team.</p>
      <div class="pb-footer__social">
        <a href="#" aria-label="Facebook"><svg class="pb-i" viewBox="0 0 24 24" width="16" height="16"><path d="M14 9h3V6h-3c-1.7 0-3 1.3-3 3v2H9v3h2v7h3v-7h3l1-3h-4V9c0-.6.4-1 1-1z"/></svg></a>
        <a href="#" aria-label="X (Twitter)"><svg class="pb-i" viewBox="0 0 24 24" width="16" height="16"><path d="M4 4l16 16M20 4 4 20"/></svg></a>
        <a href="#" aria-label="YouTube"><svg class="pb-i" viewBox="0 0 24 24" width="16" height="16"><rect x="3" y="6" width="18" height="12" rx="3"/><path d="m10 9 5 3-5 3z"/></svg></a>
      </div>
    </div>
    <div>
      <h4>Services</h4>
      <ul>%(services_links)s</ul>
    </div>
    <div>
      <h4>Company</h4>
      <ul>
        <li><a href="%(root)sindex.html#pbs-about-title">About Us</a></li>
        <li><a href="%(root)sindex.html#pbs-industries">Industries</a></li>
        <li><a href="%(root)sindex.html#pbs-faq">FAQs</a></li>
        <li><a href="%(root)scontact-us.html">Contact Us</a></li>
        <li><a href="%(root)ssitemap.html">Sitemap</a></li>
      </ul>
    </div>
    <div>
      <h4>Get In Touch</h4>
      <ul>
        <li>%(address)s</li>
        <li><a href="mailto:%(email)s">%(email)s</a></li>
      </ul>
    </div>
  </div>
  <div class="pb-wrap pb-footer__bottom">
    <span>&copy; 2026 All Rights Reserved to Pinky Brain Digital</span>
  </div>
</footer>
<script src="%(root)sassets/js/site.js"></script>
""" % {"root": root, "services_links": services_links, "email": SITE_EMAIL, "address": SITE_ADDRESS}

def head_html(root, title, description, canonical_path):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s</title>
<meta name="description" content="%(description)s">
<link rel="canonical" href="https://pinkybraindigital.com%(canonical)s">
<link rel="icon" href="%(root)simages/favicon-32.png" sizes="32x32">
<link rel="icon" href="%(root)simages/favicon-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="%(root)simages/favicon-180.png">
<link rel="stylesheet" href="%(root)sassets/css/site.css">
</head>
<body>
""" % {"title": title, "description": description, "canonical": canonical_path, "root": root}

# ---------------------------------------------------------------------------
# COMPONENT RENDERERS
# ---------------------------------------------------------------------------
def render_hero(root, data, eyebrow, h1, lead, ticks, hero_img, hero_alt, badge, cta_label="Book a free consultation"):
    ticks_html = "".join("<li>%s</li>" % t for t in ticks)
    badge_html = ""
    if badge:
        b0, b1, b2 = badge
        badge_html = """<div class="pb-hero__badge"><div><b>%s</b><span>%s</span>%s</div></div>""" % (
            b1, b0, ("<div style='margin-top:4px;font-size:.72rem;color:#7A818D'>%s</div>" % b2) if b2 else "")
    return """
<section class="pb-hero">
  <div class="pb-wrap pb-hero__grid">
    <div>
      <p class="pb-eyebrow">%(eyebrow)s</p>
      <h1>%(h1)s</h1>
      <p class="pb-lead"><b>In a nutshell:</b> %(lead)s</p>
      <div class="pb-hero__actions">
        <a class="pb-btn pb-btn--dark" href="mailto:%(email)s">%(cta)s %(arrow)s</a>
        <a class="pb-btn pb-btn--line" href="#pb-faq">See FAQs</a>
      </div>
      <ul class="pb-hero__ticks">%(ticks)s</ul>
    </div>
    <div class="pb-hero__media">
      <img class="pb-hero__img" src="%(root)simages/%(img)s" alt="%(alt)s" width="900" height="792" loading="eager" decoding="async">
      %(badge)s
    </div>
  </div>
</section>
""" % {"eyebrow": eyebrow, "h1": h1, "lead": lead, "ticks": ticks_html, "root": root,
       "img": hero_img, "alt": hero_alt, "badge": badge_html, "email": SITE_EMAIL,
       "cta": cta_label, "arrow": icon("arrow")}

def render_cards(cards, icons_cycle, numbered=False):
    out = []
    for i, (title, text) in enumerate(cards):
        ic = icons_cycle[i % len(icons_cycle)]
        out.append("""<div class="pb-card"><span class="pb-card__ic">%s</span><h3>%s</h3><p>%s</p></div>""" % (icon(ic), title, text))
    return "".join(out)

def render_section(eyebrow, title, sub, intro, cards, icons_cycle, tint=False, numbered=False, extra_title_tag="h2"):
    cls = "pb-section pb-section--tint" if tint else "pb-section"
    grid_cls = "pb-grid-4 pb-process" if numbered else "pb-grid-4"
    return """
<section class="%(cls)s">
  <div class="pb-wrap">
    <div class="pb-section__head">
      <div><p class="pb-eyebrow">%(eyebrow)s</p><h2>%(title)s</h2></div>
      <p>%(intro)s</p>
    </div>
    <div class="%(grid_cls)s">%(cards)s</div>
  </div>
</section>
""" % {"cls": cls, "eyebrow": eyebrow, "title": title, "intro": intro,
       "grid_cls": grid_cls, "cards": render_cards(cards, icons_cycle)}

def render_split(img_root, img, alt, title, intro, reasons):
    items = "".join("<li>%s</li>" % r for r in reasons)
    return """
<section class="pb-section">
  <div class="pb-wrap pb-split">
    <img class="pb-split__img" src="%(root)simages/%(img)s" alt="%(alt)s" loading="lazy" decoding="async">
    <div>
      <p class="pb-eyebrow">Why it matters</p>
      <h2>%(title)s</h2>
      <p>%(intro)s</p>
      <ul class="pb-mini-list">%(items)s</ul>
    </div>
  </div>
</section>
""" % {"root": img_root, "img": img, "alt": alt, "title": title, "intro": intro, "items": items}

def render_faq(faq_items, faq_id="pb-faq"):
    items = []
    for i, (q, a) in enumerate(faq_items):
        items.append('<details%s><summary><h3>%s</h3></summary><p>%s</p></details>' % (" open" if i == 0 else "", q, a))
    return """
<section id="%(id)s" class="pb-section pb-section--tint pb-faq">
  <div class="pb-wrap">
    <div class="pb-section__head">
      <div><p class="pb-eyebrow">FAQs</p><h2>Frequently asked questions</h2></div>
      <p>Straight answers to the questions businesses ask us most.</p>
    </div>
    <div class="pb-faq__list">%(items)s</div>
  </div>
</section>
""" % {"id": faq_id, "items": "".join(items)}

def faq_jsonld(faq_items):
    def esc(s):
        s = re.sub(r"&mdash;", "—", s)
        s = re.sub(r"&ndash;", "–", s)
        s = re.sub(r"&rsquo;", "’", s)
        s = re.sub(r"&ldquo;", "“", s)
        s = re.sub(r"&rdquo;", "”", s)
        s = re.sub(r"&hellip;", "…", s)
        s = re.sub(r"&middot;", "·", s)
        s = s.replace('"', '\\"')
        return s
    entities = ",\n    ".join(
        '{"@type": "Question", "name": "%s", "acceptedAnswer": {"@type": "Answer", "text": "%s"}}' % (esc(q), esc(a))
        for q, a in faq_items
    )
    return """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    %s
  ]
}
</script>
""" % entities

def render_cta(intro, root="", extra_note=""):
    return """
<section class="pb-section">
  <div class="pb-wrap">
    <div class="pb-cta">
      <div class="pb-cta__solo">
        <h2>Get in touch</h2>
        <p><b>In a nutshell:</b> %(intro)s</p>
        <div class="pb-cta__actions">
          <a class="pb-btn pb-btn--pink" href="%(root)scontact-us.html">Contact us %(arrow)s</a>
          <a class="pb-cta__mail" href="mailto:%(email)s">or email %(email)s directly</a>
        </div>
      </div>
    </div>
  </div>
</section>
""" % {"intro": intro, "email": SITE_EMAIL, "arrow": icon("arrow"), "root": root}

def render_breadcrumb(root, trail):
    parts = []
    for i, (label, href) in enumerate(trail):
        if href:
            parts.append('<a href="%s">%s</a>' % (href, label))
        else:
            parts.append('<span style="color:var(--pb-dark);font-weight:600">%s</span>' % label)
    return '<div class="pb-wrap pb-crumb">' + '<span>/</span>'.join(parts) + '</div>'

# ---------------------------------------------------------------------------
# BUILD: SERVICE PAGES
# ---------------------------------------------------------------------------
def build_service_page(key, all_locations):
    s = SERVICES[key]
    root = ""
    out = []
    out.append(head_html(root, "%s | Pinky Brain Digital" % s["name"], s["meta"], "/%s/" % s["slug"]))
    out.append(header_html(root))
    out.append(render_breadcrumb(root, [("Home", root + "index.html"), ("Services", root + "index.html#pbs-services"), (s["nav_label"], None)]))
    out.append(render_hero(root, s, s["eyebrow"], s["h1"], s["lead"], s["ticks"], s["hero_img"], s["hero_alt"], s["badge"]))
    out.append(render_section("Why choose us", s["why_title"], "", "", s["why_cards"], WHY_ICONS))
    out.append(render_section("What we do", s["core_title"], s["core_sub"], s["core_intro"], s["core_cards"], CORE_ICONS, tint=True))
    out.append(render_section("How we help" if s["g3_numbered"] else "Our approach", s["g3_title"], s["g3_sub"], s["g3_intro"], s["g3_cards"], STEP_ICONS, numbered=s["g3_numbered"]))
    if key in PROCESS_CONTENT:
        pt, psub, pintro, psteps = get_process_content(key)
        out.append(render_section("How we work", pt, psub, pintro, psteps, STEP_ICONS, tint=True, numbered=True))
    out.append(render_split(root, s["split_img"], s["split_alt"], s["g4_title"], s["g4_intro"], [c[0] + " &mdash; " + c[1] for c in s["g4_cards"]]))
    out.append(render_faq(s["faq"]))
    out.append(render_cta(s["cta_intro"], root=root))
    out.append(footer_html(root))
    out.append(faq_jsonld(s["faq"]))
    out.append("</body></html>")
    path = os.path.join(ROOT, s["slug"] + ".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(out))
    return path

# ---------------------------------------------------------------------------
# BUILD: LOCATION PAGES
# ---------------------------------------------------------------------------
def read_locations():
    path = os.path.join(ROOT, "Pinky Brain Digital - Location.csv")
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = (row.get("URL") or "").strip()
            city = (row.get("City") or "").strip()
            service = (row.get("Service") or "").strip()
            region = (row.get("Region") or "").strip()
            title = (row.get("Page title") or "").strip()
            if not url or not city or service not in LOCATION_SERVICE_KEY:
                continue
            folder = url.strip("/")
            rows.append({
                "no": row.get("No", "").strip(),
                "region": region,
                "city": city,
                "service": service,
                "service_key": LOCATION_SERVICE_KEY[service],
                "title": title,
                "url": url,
                "folder": folder,
            })
    return rows

def build_location_page(loc, idx, all_locations):
    s = SERVICES[loc["service_key"]]
    root = ""
    city = loc["city"]
    region = loc["region"]
    region_full = REGION_FULL.get(region, region)
    country = CITY_COUNTRY_OVERRIDE.get(city, region_full)
    service_lower = s["name"].lower()

    lead_plain = re.sub(r"&mdash;", "-", s["lead"])
    lead_plain = re.sub(r"&rsquo;", "'", lead_plain)
    lead_plain = re.sub(r"&ldquo;|&rdquo;", '"', lead_plain)
    lead_cap = lead_plain[0].upper() + lead_plain[1:]

    tmpl = INTRO_TEMPLATES[idx % len(INTRO_TEMPLATES)]
    intro_para = tmpl.format(city=city, region_full=country, service_lower=service_lower, lead_cap=lead_cap)

    local = LOCAL_COPY[loc["service_key"]]
    reasons = [r.format(city=city, region_full=country) for r in local["reasons"]]
    local_faq = [(q.format(city=city), a.format(city=city, region_full=country)) for q, a in local["faq"]]

    h1 = loc["title"]
    eyebrow = "%s &middot; %s" % (region, city)
    ticks = list(s["ticks"])
    if ticks:
        ticks[-1] = "Serving %s and %s" % (city, region_full)

    title_tag = "%s | Pinky Brain Digital" % h1
    meta_desc = "%s in %s. %s" % (s["name"], city, s["meta"])
    if len(meta_desc) > 300:
        meta_desc = meta_desc[:297] + "..."

    out = []
    out.append(head_html(root, title_tag, meta_desc, "/%s" % loc["url"]))
    out.append(header_html(root))
    out.append(render_breadcrumb(root, [("Home", root + "index.html"), (s["nav_label"], root + s["slug"] + ".html"), (city, None)]))
    out.append(render_hero(root, s, eyebrow, h1, lead_cap.rstrip("."), ticks, s["hero_img"], s["hero_alt"], None, cta_label="Book a free consultation"))
    out.append("""
<section class="pb-section">
  <div class="pb-wrap">
    <div class="pb-section__head">
      <div><p class="pb-eyebrow">%(city)s</p><h2>%(service)s built for businesses in %(city)s</h2></div>
      <p>%(intro)s</p>
    </div>
    <div class="pb-grid-4">%(cards)s</div>
  </div>
</section>
""" % {"city": city, "service": s["name"], "intro": intro_para, "cards": render_cards(s["core_cards"], CORE_ICONS)})
    pt, psub, pintro, psteps = get_process_content(loc["service_key"])
    if pt:
        local_title = pt if city in pt else "%s in %s" % (pt, city)
        out.append(render_section("Our process", local_title, psub, pintro, psteps, STEP_ICONS, tint=True, numbered=True))
    out.append(render_split(root, s["split_img"], s["split_alt"],
                             "Why %s businesses choose Pinky Brain Digital" % city,
                             "%s does more for your %s than a one-size-fits-all package." % (s["name"], "website" if loc["service_key"] == "website-design" else "search visibility"),
                             reasons))
    out.append(render_faq(s["faq"][:3] + local_faq, faq_id="pb-faq"))
    cta_intro = "tell us about your %s business and we&rsquo;ll reply within one business day with real next steps." % city
    out.append(render_cta(cta_intro, root=root))
    out.append(footer_html(root))
    out.append(faq_jsonld(s["faq"][:3] + local_faq))
    out.append("</body></html>")

    path = os.path.join(ROOT, loc["folder"] + ".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(out))
    return path

# ---------------------------------------------------------------------------
# BUILD: HOMEPAGE (wrap existing fragment)
# ---------------------------------------------------------------------------
IMG_REMAP = {
    "2149273705.webp": "homepage-hero-digital-agency-team.webp",
    "10539.webp": "about-pinky-brain-digital-team.webp",
    "2149241210.jpg": "luxury-real-estate-interior.jpg",
    "favii.png": "pinky-brain-digital-badge-icon.png",
    "photo-1600585154526-990dced4db0d.webp": "luxury-property-marketing.webp",
    "Modern-dental-clinic-treatment-room.avif": "dental-clinic-marketing.avif",
    "plumber.avif": "plumbers-electricians-marketing.avif",
    "cafe.avif": "restaurant-cafe-marketing.avif",
    "shop.avif": "retail-shop-marketing.avif",
    "online.avif": "ecommerce-online-business-marketing.avif",
    "service.avif": "professional-services-marketing.avif",
}

def build_homepage():
    frag_source = os.path.join(ROOT, "_ref", "index.homepage-fragment.html")
    frag_path = os.path.join(ROOT, "index.html")
    with open(frag_source, encoding="utf-8") as f:
        frag = f.read()
    for old, new in IMG_REMAP.items():
        frag = frag.replace(
            "https://pinkybraindigital.com/wp-content/uploads/2026/09/%s" % old,
            "images/%s" % new,
        )
    # fix internal links that pointed to non-existent WP pages, to real local pages
    link_fix = {
        "/services/website-design/": "website-design.html",
        "/services/ecommerce/": "e-commerce-websites-design.html",
        "/services/seo/": "seo-services.html",
        "/services/aeo/": "aeo-ai-search.html",
        "/services/ppc-management/": "ppc-digital-advertising.html",
        "/services/social-media-marketing/": "social-media.html",
        "/website-design-packages/": "website-design.html",
        "/contact/": "mailto:%s" % SITE_EMAIL,
    }
    for old, new in link_fix.items():
        frag = frag.replace('href="%s"' % old, 'href="%s"' % new)

    root = ""
    title = "Pinky Brain Digital | Full-Service Digital Agency &mdash; Websites, SEO, AEO & Marketing"
    desc = "Pinky Brain Digital is a full-service digital agency for the UK, Europe, USA and Canada &mdash; websites, e-commerce, SEO & AEO, social media, advertising, branding and AI automation."
    out = []
    out.append(head_html(root, title, desc, "/"))
    out.append(header_html(root))
    out.append(frag)
    out.append(footer_html(root))
    out.append("</body></html>")
    with open(frag_path, "w", encoding="utf-8") as f:
        f.write("".join(out))
    return frag_path

# ---------------------------------------------------------------------------
# BUILD: CONTACT US PAGE
# ---------------------------------------------------------------------------
def build_contact_page():
    root = ""
    title = "Contact Us | Pinky Brain Digital"
    desc = "Get in touch with Pinky Brain Digital. Email, call or send a message and we'll reply within one business day."
    service_options = "".join('<option value="%s">%s</option>' % (SERVICES[k]["name"], SERVICES[k]["name"]) for k in SERVICE_ORDER)

    out = []
    out.append(head_html(root, title, desc, "/contact-us/"))
    out.append(header_html(root))
    out.append(render_breadcrumb(root, [("Home", root + "index.html"), ("Contact", None)]))
    out.append("""
<section class="pb-hero">
  <div class="pb-wrap pb-hero__grid">
    <div>
      <p class="pb-eyebrow">Get in touch</p>
      <h1>Let&rsquo;s talk about your business</h1>
      <p class="pb-lead"><b>In a nutshell:</b> tell us what you need and we&rsquo;ll reply within one business day with real next steps &mdash; not a scripted sales call.</p>
      <ul class="pb-hero__ticks">
        <li>Real replies, no chatbots</li>
        <li>Free 15&ndash;20 minute call</li>
        <li>No obligation</li>
      </ul>
    </div>
    <div class="pb-card" style="padding:32px">
      <h3 style="margin-bottom:16px">Head Office</h3>
      <p style="font-size:.98rem;color:var(--pb-body)">%(address)s</p>
      <p style="margin-top:20px"><a class="pb-link" href="mailto:%(email)s">%(email)s</a></p>
    </div>
  </div>
</section>
<section class="pb-section">
  <div class="pb-wrap" style="max-width:820px">
    <div class="pb-section__head" style="display:block">
      <p class="pb-eyebrow">Send a message</p>
      <h2>Tell us about your project</h2>
    </div>
    <form class="pb-form" id="pb-contact-form">
      <div>
        <label for="pb-name">Your name*</label>
        <input id="pb-name" name="name" type="text" required>
      </div>
      <div>
        <label for="pb-email">Email address*</label>
        <input id="pb-email" name="email" type="email" required>
      </div>
      <div>
        <label for="pb-phone">Phone number</label>
        <input id="pb-phone" name="phone" type="tel">
      </div>
      <div>
        <label for="pb-service">Service you&rsquo;re interested in</label>
        <select id="pb-service" name="service">
          <option value="">Not sure yet</option>
          %(service_options)s
        </select>
      </div>
      <div class="pb-field--full">
        <label for="pb-message">Your message*</label>
        <textarea id="pb-message" name="message" required></textarea>
      </div>
      <div class="pb-form__actions">
        <button type="submit" class="pb-btn pb-btn--dark">Send message %(arrow)s</button>
        <span class="pb-form__note" style="margin:0">We reply within one business day.</span>
      </div>
    </form>
  </div>
</section>
<script>
document.getElementById('pb-contact-form').addEventListener('submit', function (e) {
  e.preventDefault();
  var f = e.target;
  var subject = 'Website enquiry' + (f.service.value ? ' - ' + f.service.value : '');
  var body = 'Name: ' + f.name.value + '%%0D%%0AEmail: ' + f.email.value + '%%0D%%0APhone: ' + f.phone.value + '%%0D%%0A%%0D%%0A' + f.message.value;
  window.location.href = 'mailto:%(email)s?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body).replace(/%%250D%%250A/g, '%%0D%%0A');
});
</script>
""" % {"address": SITE_ADDRESS, "email": SITE_EMAIL, "service_options": service_options, "arrow": icon("arrow")})
    out.append(footer_html(root))
    out.append("</body></html>")

    path = os.path.join(ROOT, "contact-us.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(out))
    return path

# ---------------------------------------------------------------------------
# BUILD: SITEMAP PAGE + sitemap.xml
# ---------------------------------------------------------------------------
def build_sitemap_page(locations):
    root = ""
    title = "Sitemap | Pinky Brain Digital"
    desc = "A complete list of every page on the Pinky Brain Digital website."

    def col(heading, links, anchor_id=""):
        items = "".join('<li><a href="%s">%s</a></li>' % (href, label) for label, href in links)
        anchor = ' id="%s"' % anchor_id if anchor_id else ""
        return '<div%s><h3>%s</h3><ul>%s</ul></div>' % (anchor, heading, items)

    company_links = [
        ("Home", "index.html"), ("About Us", "index.html#pbs-about-title"),
        ("Industries", "index.html#pbs-industries"), ("FAQs", "index.html#pbs-faq"),
        ("Contact Us", "contact-us.html"), ("Sitemap", "sitemap.html"),
    ]
    service_links = [(SERVICES[k]["name"], "%s.html" % k) for k in SERVICE_ORDER]
    wd_links = [(l["city"], "%s.html" % l["folder"]) for l in locations if l["service_key"] == "website-design"]
    seo_links = [(l["city"], "%s.html" % l["folder"]) for l in locations if l["service_key"] == "seo-services"]

    cols = (
        col("Company", company_links)
        + col("Services", service_links)
        + col("Website Design &mdash; Locations", wd_links, anchor_id="website-design")
        + col("SEO Services &mdash; Locations", seo_links, anchor_id="seo-services")
    )

    out = []
    out.append(head_html(root, title, desc, "/sitemap/"))
    out.append(header_html(root))
    out.append(render_breadcrumb(root, [("Home", root + "index.html"), ("Sitemap", None)]))
    out.append("""
<section class="pb-section">
  <div class="pb-wrap">
    <div class="pb-section__head" style="display:block">
      <p class="pb-eyebrow">Every page</p>
      <h2>Sitemap</h2>
    </div>
    <div class="pb-sitemap-grid">%s</div>
  </div>
</section>
""" % cols)
    out.append(footer_html(root))
    out.append("</body></html>")

    path = os.path.join(ROOT, "sitemap.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(out))
    return path

def build_sitemap_xml(locations):
    base = "https://pinkybraindigital.com"
    urls = ["/"] + ["/%s/" % k for k in SERVICE_ORDER] + ["/contact-us/", "/sitemap/"] + [l["url"] for l in locations]
    body = "".join('  <url><loc>%s%s</loc></url>\n' % (base, u) for u in urls)
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % body
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)
    return path

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    global ALL_LOCATIONS
    locations = read_locations()
    ALL_LOCATIONS = locations
    print("Loaded %d location rows" % len(locations))

    built = []
    built.append(build_homepage())
    print("Built homepage")

    for key in SERVICE_ORDER:
        built.append(build_service_page(key, locations))
    print("Built %d service pages" % len(SERVICE_ORDER))

    for i, loc in enumerate(locations):
        built.append(build_location_page(loc, i, locations))
    print("Built %d location pages" % len(locations))

    built.append(build_contact_page())
    built.append(build_sitemap_page(locations))
    built.append(build_sitemap_xml(locations))
    print("Built contact page + sitemap")

    print("Total files written: %d" % len(built))

if __name__ == "__main__":
    main()
