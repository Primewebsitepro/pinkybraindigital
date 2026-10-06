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
import html
import json
import os
import re

from content import (
    CTA_PRIMARY, CTA_SECONDARY, CASE_BY_CASE, SERVICE_GROUPS, SERVICE_BLURB, OUTCOMES,
    FREE_OFFERS, SERVICE_OFFER, SECTOR_NOTES, CITY_PROFILES, INDUSTRIES,
)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SITE_NAME = "Pinky Brain Digital"
SITE_URL = "https://pinkybraindigital.com"
SITE_EMAIL = "hello@pinkybraindigital.com"
SITE_ADDRESS = "International House, 109–111 Fulham Palace Road, London, W6 8JA"



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
        "lead": "we design fast, modern websites built around your customers: mobile-first, easy for you to update and designed to turn visitors into real enquiries.",
        "meta": "Fast, mobile-first website design and development that turns visitors into enquiries. Built around your customers, SEO-ready from day one.",
        "ticks": ["Mobile-first design", "SEO-ready from day one", "Launch support included"],
        "badge": ("Page speed", "96 / 100", "Mobile &middot; Desktop &middot; Tablet"),
        "hero_img": "website-design-service-hero.webp",
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
        "lead": "we build online shops that load quickly, work beautifully on a phone and make checkout simple, so more of your visitors become paying customers.",
        "meta": "E-commerce website design for WooCommerce and Shopify. Mobile-first stores with fast checkout, built to sell across the UK, Europe, the USA and Canada.",
        "ticks": ["Mobile-first shopping experience", "SEO-ready product pages", "Selling across UK, Europe, USA & Canada"],
        "badge": ("Secure checkout", "3 steps", "Cart &middot; Details &middot; Pay"),
        "hero_img": "ecommerce-website-design-hero.webp",
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
            ("Ready for Multiple Markets", "Currencies, shipping zones and tax settings can be set up for selling across the UK, Europe, the USA and Canada as you grow."),
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
            ("Which platform do you build on &mdash; WooCommerce or Shopify?", "We recommend the platform that fits your products, budget and how you want to manage the store. WooCommerce suits businesses that want full control on WordPress; Shopify suits those who want a simple, hosted setup. We&rsquo;ll walk you through the trade-offs before you decide."),
            ("Can my store sell to customers in the UK, Europe, the USA and Canada?", "Yes. We can set up multiple currencies, shipping zones, tax and VAT options and the payment methods customers expect in each market. Tax rules vary by country, so we&rsquo;ll always suggest confirming the details with your accountant."),
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
        "lead": "we help your business rank higher, get seen by the right people and turn that visibility into enquiries, customers and growth.",
        "meta": "SEO services for better rankings, more visibility, relevant traffic and more enquiries. Technical, content and local SEO with comprehensive reporting.",
        "ticks": ["Technical, local & content SEO", "Comprehensive monthly reports", "Ranking in UK, Europe, USA & Canada"],
        "badge": ("What we improve", "Technical &middot; Content &middot; Local", ""),
        "hero_img": "seo-services-hero.webp",
        "hero_alt": "SEO services dashboard showing search rankings improving",
        "split_img": "ecommerce-store-design-detail.webp",
        "split_alt": "SEO content and keyword strategy being planned on screen",
        "why_title": "Better rankings. More visibility. More opportunities to grow.",
        "why_cards": [
            ("Better rankings. More visibility. More opportunities to grow.", "We care about the complete result: higher rankings and visibility, relevant traffic, enquiries, customers and, ultimately, growth for your business. We report on all of it, not just a list of keywords."),
            ("We tell you what&rsquo;s realistic.", "Some searches can be won in months, others take a year or more. We show you which is which before you commit."),
            ("No secret tricks.", "We don&rsquo;t buy spammy links or hide behind jargon. Everything we do follows Google&rsquo;s guidelines, and we explain it clearly."),
            ("Reports you&rsquo;ll actually read.", "A short monthly summary of what we did, what changed and what happens next &mdash; no 40-page data dumps."),
        ],
        "core_title": "Four things that decide whether Google sends you customers.",
        "core_sub": "Technical health, useful content, local presence and trusted links.",
        "core_intro": "SEO isn&rsquo;t one trick. It&rsquo;s technical health, useful content, local presence and trusted links working together. We look after all four for businesses across the UK, Europe, the USA and Canada, so search engines understand your website and customers can find it.",
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
            ("Can you help my business rank in more than one country?", "Yes. We work with businesses across the UK, Europe, the USA and Canada, and adapt keywords, spelling, local listings and location pages for each market you want to reach."),
            ("What&rsquo;s the difference between SEO and local SEO?", "SEO helps your website rank for searches anywhere. Local SEO focuses on &ldquo;near me&rdquo; and city-based searches and your Google Business Profile, which matters most if customers visit you or you serve a specific area."),
            ("Will I get reports I can understand?", "Yes. Every month you&rsquo;ll receive a comprehensive report covering what we did, how your visibility and enquiries changed and what&rsquo;s planned next."),
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
        "lead": "AEO (answer engine optimisation) helps AI tools such as ChatGPT, Google AI Overviews and Perplexity understand your business, so they are more likely to mention you when people ask questions.",
        "meta": "AEO (Answer Engine Optimisation) helps ChatGPT, Google AI Overviews and Perplexity understand and recommend your business.",
        "ticks": ["Built for AI and traditional search", "Clear, answer-ready content", "Visible in UK, Europe, USA & Canada"],
        "badge": ("Customers ask AI", "&ldquo;Who can help grow my business online?&rdquo;", "We make your answer easy to find"),
        "hero_img": "aeo-ai-search-hero.webp",
        "hero_alt": "AI chat interface showing an answer engine recommending a business",
        "split_img": "aeo-ai-search-detail.webp",
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
        "core_intro": "AI search tools pull answers from websites they can understand and trust. We prepare your website, content and online presence so your business is clear, credible and easy to cite &mdash; for customers across the UK, Europe, the USA and Canada.",
        "core_cards": [
            ("Answer-ready content", "We rewrite and structure your pages to answer the questions customers really ask, in clear, direct language that AI tools can quote."),
            ("Structured data and schema", "We add behind-the-scenes markup that tells search engines and AI tools exactly who you are, what you offer and where you operate."),
            ("Brand and entity consistency", "We make sure your business name, services, locations and details match across your website, profiles and directories, so AI tools describe you correctly."),
            ("AI visibility tracking", "We check how your brand appears in AI answers for the questions that matter, and report every change in full."),
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
            ("Clear About Where You Operate", "Precise location and service details for customers in the UK, Europe, the USA and Canada."),
            ("Kept Current as AI Changes", "AI search is evolving fast, so your content and data stay structured, up to date and adaptable."),
        ],
        "faq": [
            ("What is AEO?", "AEO stands for Answer Engine Optimisation. It&rsquo;s the practice of structuring your website and content so AI tools and answer engines &mdash; such as ChatGPT, Google AI Overviews, Perplexity and Microsoft Copilot &mdash; can understand your business and include it in their answers."),
            ("How is AEO different from SEO?", "SEO helps your pages rank in a list of search results. AEO helps your business be understood and referenced inside a direct answer. They share the same foundations &mdash; quality content, clear structure and trust &mdash; so we treat them as one joined-up strategy."),
            ("Can you guarantee ChatGPT or Google AI will mention my business?", "No. AI tools decide their own answers and nobody outside them can control that. What we can do is improve your clarity, structure and credibility so you&rsquo;re more likely to be included, and measure how that changes."),
            ("Does AEO work for businesses outside the USA?", "Yes. AI tools answer questions in every market, so we help businesses in the UK, Europe, the USA and Canada make their locations, services and language clear for the customers they want to reach."),
            ("How long does AEO take to show results?", "Some improvements, such as better-structured content, can be picked up within weeks, but changes in AI answers usually build over several months. We agree how we&rsquo;ll measure progress at the start."),
        ],
        "cta_intro": "tell us what you do and who you serve, and we&rsquo;ll reply within one business day with a straight-talking view on where to start.",
        "cta_points": [
            ("We reply within 1 business day", "A real person reads your message and comes back with a few questions about your business and customers."),
            ("A short AI search call", "15&ndash;20 minutes on the questions your customers ask and where you&rsquo;d like to appear."),
            ("A comprehensive plan", "What we&rsquo;d change, in what order, and how we&rsquo;d measure whether it&rsquo;s working."),
        ],
    },
    "ppc-digital-advertising": {
        "slug": "ppc-digital-advertising",
        "nav_label": "PPC & Digital Advertising",
        "name": "PPC & Digital Advertising",
        "eyebrow": "Services · PPC & Digital Advertising",
        "h1": "Advertising that brings customers, not just clicks",
        "lead": "we plan, run and improve your paid ads across the platforms your customers use, and track the results, so you can see what your budget is actually bringing in.",
        "meta": "PPC and digital advertising management across Google Ads, Meta and LinkedIn, tracked to enquiries and sales for businesses in the UK, Europe, the USA and Canada.",
        "ticks": ["Google, Meta & LinkedIn campaigns", "Tracked to enquiries and sales", "Advertising in UK, Europe, USA & Canada"],
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
        "core_intro": "Paid advertising can grow a business quickly &mdash; or drain a budget just as fast. We manage the whole process: strategy, setup, creative, tracking and ongoing optimisation, for businesses advertising across the UK, Europe, the USA and Canada.",
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
            ("Right Person, Right Place", "Reach customers by location, interest, intent and behaviour across the UK, Europe, the USA and Canada."),
            ("Every Campaign Has a Goal", "Each one is tied to a measurable result &mdash; enquiries, bookings or sales."),
            ("Scale Only What Works", "Budgets rise gradually, and only behind campaigns that have proved themselves."),
        ],
        "faq": [
            ("How much should I spend on advertising?", "It depends on your industry, competition and goals. We&rsquo;ll recommend a starting budget based on realistic costs and expected enquiries, and you stay in control of what you spend. Ad spend is paid to the advertising platforms and is separate from our management fee."),
            ("How quickly will I see results?", "Ads can start bringing traffic within days of launch, but the first few weeks are for learning what works. Most campaigns become more efficient after 6&ndash;8 weeks of testing and optimisation."),
            ("Which platforms do you advertise on?", "We typically use Google Ads, Microsoft Advertising, Meta (Facebook and Instagram) and LinkedIn, and recommend only the ones that fit your customers and budget."),
            ("Can you run one campaign across several countries?", "Yes. We set up location targeting, language and currency for the UK, Europe, the USA and Canada, and can advise on regional requirements such as cookie consent, so each market sees the right message."),
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
        "meta": "Social media marketing and management &mdash; content planning, on-brand posting and community replies for businesses in the UK, Europe, the USA and Canada.",
        "ticks": ["Content planned around your goals", "Consistent, on-brand posting", "Content for UK, Europe, USA & Canada"],
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
        "core_intro": "Social media works when it&rsquo;s consistent, on-brand and built around your customers. We handle the strategy, content and day-to-day management for businesses across the UK, Europe, the USA and Canada, so you can focus on running your business.",
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
            ("Should my content be different for the USA, UK and Europe?", "Often, yes. Spelling, humour, timing and references vary between markets. For businesses in the UK, Europe, the USA and Canada we adapt the tone and schedule for each audience rather than posting the same thing everywhere."),
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
        "lead": "we set up and manage your Google Ads so your business appears when people search for what you offer, then track every click through to real enquiries and sales.",
        "meta": "Google Ads management &mdash; Search, Shopping and Performance Max campaigns with conversion tracking, for businesses across the UK, Europe, the USA and Canada.",
        "ticks": ["Search, Shopping and Performance Max", "Conversion tracking set up", "Campaigns in UK, Europe, USA & Canada"],
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
            ("Honest fees, honest reporting.", "You&rsquo;ll see your ad spend, our fee and your results in one comprehensive report &mdash; no hidden charges, no jargon."),
        ],
        "core_title": "What we set up, fix and manage in your account.",
        "core_sub": "Account structure, keywords, landing pages and tracking, all handled.",
        "core_intro": "Google Ads is powerful, but it&rsquo;s easy to overspend without expert setup. We handle everything &mdash; account structure, keyword research, ad copy, landing pages, tracking and ongoing optimisation &mdash; for businesses advertising across the UK, Europe, the USA and Canada.",
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
            ("Can you run Google Ads in several countries at once?", "Yes. We set up location, language and currency targeting for the UK, Europe, the USA and Canada, and can run separate campaigns for each country so the message and budget suit each market."),
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

# ---------------------------------------------------------------------------
# EXTRA SERVICES — the rest of the 20-service homepage grid. These don't sit
# in the primary nav (that would be 21 nav items), but every one gets a real
# page instead of a dead /services/... link.
# ---------------------------------------------------------------------------
EXTRA_SERVICES = {
    "app-development": {
        "slug": "app-development", "nav_label": "Web & Mobile Apps", "name": "Web & Mobile Apps",
        "eyebrow": "Services · Web & Mobile Apps",
        "h1": "Apps that make life easier for your customers and your team",
        "lead": "we build apps for your customers or your team, on iPhone, Android and the web, shaped around the job each one needs to do.",
        "meta": "Web and mobile app development for iOS, Android and the web, built around real workflows rather than trends.",
        "ticks": ["iOS, Android &amp; web", "Built around real workflows", "Ongoing support included"],
        "badge": ("Built for", "iOS &middot; Android &middot; Web", ""),
        "hero_img": "homepage-hero-digital-agency-team.webp", "hero_alt": "Team planning a mobile app on a laptop and tablet",
        "split_img": "website-design-development-process.webp", "split_alt": "App interface design being reviewed on screen",
        "why_title": "An app is a commitment, not a trend.",
        "why_cards": [
            ("An app is a commitment, not a trend.", "We only recommend an app when it genuinely solves a problem a website can&rsquo;t &mdash; not because it sounds impressive."),
            ("Useful beats flashy.", "The best apps are the ones people open again. We design around real, repeat tasks, not novelty."),
            ("One codebase where possible.", "Cross-platform frameworks mean lower cost and faster updates across iPhone, Android and web."),
            ("Support doesn&rsquo;t stop at launch.", "App stores and phones keep changing, so we stay on as your ongoing maintenance partner."),
        ],
        "core_title": "Everything your app needs.", "core_sub": "From first sketch to the app store.",
        "core_intro": "We combine research, design and solid engineering to build apps that people actually keep on their phone.",
        "core_cards": [
            ("Discovery &amp; UX mapping", "We map the exact screens and actions your users need, before any design work starts."),
            ("Native &amp; cross-platform builds", "We build for iPhone, Android and web using whichever approach fits your budget and timeline."),
            ("Secure data &amp; logins", "User accounts, payments and personal data are handled with proper security from day one."),
            ("App store submission", "We handle submission to the Apple App Store and Google Play, so launch is one less thing to manage."),
        ],
        "g3_numbered": True, "g3_title": "How We Build Your App", "g3_sub": "From first conversation to app store listing.",
        "g3_intro": "A clear, staged process keeps the project predictable and the budget under control.",
        "g3_cards": [
            ("Discovery &amp; Planning", "We map user journeys, features and technical requirements before design begins."),
            ("Design &amp; Prototyping", "Key screens are designed and tested as a clickable prototype, so you can try it before we build."),
            ("Build &amp; Testing", "The app is built and tested across real devices for bugs, performance and usability."),
            ("Launch &amp; Support", "We submit to the app stores, then stay on for updates, fixes and new features."),
        ],
        "g4_title": "An App People Actually Use", "g4_intro": "Downloads don&rsquo;t matter if nobody opens the app twice. We design for return visits.",
        "g4_cards": [
            ("Clear Onboarding", "New users understand what to do in the first 30 seconds."),
            ("Fast &amp; Reliable", "Built to load quickly and work smoothly, even on a patchy connection."),
            ("Built to Scale", "Your app can grow from your first 100 users to your next 100,000."),
            ("Data You Can Act On", "Usage data shows you what people actually do, so you know what to improve next."),
        ],
        "faq": [
            ("Should I build an app or a mobile-friendly website?", "Many businesses don&rsquo;t need an app at all &mdash; a fast, mobile-first website does the job. We&rsquo;ll tell you honestly which fits your goals before recommending an app."),
            ("How much does an app cost?", "It depends on complexity, platforms and integrations. We&rsquo;ll give you a clear, fixed-scope quote once we understand what the app needs to do."),
            ("Do you build for both iPhone and Android?", "Yes, usually from a single cross-platform codebase to keep costs down and updates simple."),
            ("Will I own the app afterwards?", "Yes. Once the project is paid in full, the app, its code and your app store listings belong to you."),
            ("What happens after launch?", "We offer ongoing support plans covering OS updates, bug fixes and new features as phones and platforms change."),
        ],
        "cta_intro": "tell us what you want your app to do, and we&rsquo;ll reply within one business day with honest advice on whether an app is even the right move.",
    },
    "custom-software": {
        "slug": "custom-software", "nav_label": "Custom Software", "name": "Custom Software",
        "eyebrow": "Services · Custom Software",
        "h1": "Software built around the way your team already works",
        "lead": "we build tools around the way you already work, so your team saves time instead of fighting a system that doesn’t fit.",
        "meta": "Custom software and internal tools built around your team's real workflow, replacing spreadsheets and disconnected systems.",
        "ticks": ["Built around your workflow", "Replaces spreadsheets &amp; email chains", "Grows as you grow"],
        "badge": ("Built for", "Your exact workflow", ""),
        "hero_img": "website-design-development-process.webp", "hero_alt": "Custom software dashboard being reviewed on screen",
        "split_img": "homepage-hero-digital-agency-team.webp", "split_alt": "Team mapping a software workflow together",
        "why_title": "Off-the-shelf software makes you adapt. Custom software adapts to you.",
        "why_cards": [
            ("Off-the-shelf makes you adapt. Custom adapts to you.", "Generic tools force your team into someone else&rsquo;s process. We build around your actual workflow instead."),
            ("We start with the bottleneck, not the tech.", "We find where time is really being lost &mdash; double entry, manual reports, disconnected tools &mdash; and solve that first."),
            ("Simple, maintainable builds.", "We favour proven, well-documented technology over anything clever just for the sake of it."),
            ("You&rsquo;re not locked in.", "You own the code and the data. There&rsquo;s no vendor holding your business hostage."),
        ],
        "core_title": "What we build.", "core_sub": "Practical tools for real business problems.",
        "core_intro": "From internal dashboards to systems that connect your existing tools, we build software that removes manual work.",
        "core_cards": [
            ("Internal tools &amp; dashboards", "Purpose-built tools that replace messy spreadsheets and give your team one clear source of truth."),
            ("System integrations", "We connect the software you already use, so data moves automatically instead of being re-typed."),
            ("Workflow automation", "Repetitive admin tasks are automated, freeing your team to focus on higher-value work."),
            ("Secure, scalable builds", "Software built to handle real usage and grow as your business and data grow."),
        ],
        "g3_numbered": True, "g3_title": "How We Build Your Software", "g3_sub": "From process audit to a tool your team actually uses.",
        "g3_intro": "We start by understanding the real problem, not by writing code.",
        "g3_cards": [
            ("Process Audit", "We map your current workflow and find where time and accuracy are being lost."),
            ("Solution Design", "We design the simplest tool that solves the problem, and agree scope and cost before building."),
            ("Build &amp; Test", "The software is built in stages, with regular check-ins so nothing drifts from what you asked for."),
            ("Rollout &amp; Training", "We launch the tool with your team, with training so everyone knows how to use it from day one."),
        ],
        "g4_title": "Software That Fits the Way You Work", "g4_intro": "The right custom tool feels obvious once it&rsquo;s there &mdash; like it should have always existed.",
        "g4_cards": [
            ("Built Around Real Tasks", "Every screen is designed around what your team actually does each day."),
            ("Less Manual Work", "Automation removes the repetitive admin that eats up hours every week."),
            ("One Source of Truth", "No more conflicting spreadsheets &mdash; everyone works from the same accurate data."),
            ("Room to Grow", "New features and integrations can be added later without starting over."),
        ],
        "faq": [
            ("How is this different from buying off-the-shelf software?", "Off-the-shelf tools are built for everyone, so you compromise. Custom software is built around your exact process, with nothing you don&rsquo;t need."),
            ("How much does custom software cost?", "It depends entirely on scope. We start with a process audit and give you a clear, fixed quote before any build work begins."),
            ("How long does a project take?", "Small internal tools can take a few weeks; larger systems take longer. We&rsquo;ll give you a realistic timeline in the proposal."),
            ("Will you maintain the software after launch?", "Yes. We offer ongoing support and development so the tool keeps working as your business changes."),
            ("Do we own the software?", "Yes. Once paid in full, the code and everything built for you belongs to your business outright."),
        ],
        "cta_intro": "tell us what&rsquo;s slowing your team down, and we&rsquo;ll reply within one business day with honest thoughts on whether custom software is worth it.",
    },
    "local-seo": {
        "slug": "local-seo", "nav_label": "Local SEO & Google Profile", "name": "Local SEO & Google Profile",
        "eyebrow": "Services · Local SEO",
        "h1": "Show up on Google Maps when nearby customers search",
        "lead": "we help your business show up on Google Maps and in local searches, so nearby customers find you first, ahead of the competition down the road.",
        "meta": "Local SEO and Google Business Profile management to help nearby customers find and choose your business first.",
        "ticks": ["Google Business Profile setup", "Maps &amp; “near me” visibility", "Local reviews &amp; citations"],
        "badge": ("Local pack", "Top 3 on Maps", ""),
        "hero_img": "seo-services-hero.webp", "hero_alt": "Google Maps local search results shown on screen",
        "split_img": "ecommerce-store-design-detail.webp", "split_alt": "Local business Google profile being optimised",
        "why_title": "Most local searches never scroll past the map.",
        "why_cards": [
            ("Most local searches never scroll past the map.", "If you&rsquo;re not in the top 3 map results, most nearby customers never see you at all."),
            ("Your profile is doing more selling than you think.", "Photos, reviews, hours and posts on your Google Business Profile shape a decision before anyone visits your website."),
            ("Consistency builds trust with Google.", "Matching name, address and phone details across the web help Google trust that your business is legitimate."),
            ("Reviews compound over time.", "A steady flow of genuine reviews, handled well, becomes one of your strongest local ranking signals."),
        ],
        "core_title": "What we manage.", "core_sub": "Everything that decides your local visibility.",
        "core_intro": "Local SEO is part profile, part website, part reputation. We look after all three.",
        "core_cards": [
            ("Google Business Profile optimisation", "We complete, verify and actively manage your profile so it works as hard as possible."),
            ("Local citations &amp; listings", "We fix inconsistent business details across directories that quietly hurt your rankings."),
            ("Review strategy", "We help you collect genuine reviews and respond to them in a way that builds trust."),
            ("Location-specific content", "We build pages and content that speak directly to the areas you serve."),
        ],
        "g3_numbered": True, "g3_title": "How We Boost Your Local Visibility", "g3_sub": "From audit to consistent map rankings.",
        "g3_intro": "We fix the technical and reputation signals that decide who Google shows first.",
        "g3_cards": [
            ("Local Audit", "We check your current Maps ranking, profile completeness and citation consistency."),
            ("Profile &amp; Citation Fixes", "We complete your Google Business Profile and correct listings across key directories."),
            ("Review &amp; Content Plan", "We put a simple system in place for gathering reviews and publishing local content."),
            ("Ongoing Monitoring", "We track your local rankings and keep your profile active month after month."),
        ],
        "g4_title": "Built for the Way People Search Locally", "g4_intro": "&ldquo;Near me&rdquo; searches convert fast &mdash; the person is often ready to buy or visit today.",
        "g4_cards": [
            ("Found on Maps First", "Show up in the local pack before customers even reach the full search results."),
            ("Trusted at a Glance", "Reviews, photos and accurate hours help people choose you with confidence."),
            ("One Business, One Story", "Consistent details everywhere stop Google &mdash; and customers &mdash; getting confused."),
            ("Works Alongside National SEO", "Local SEO strengthens, rather than replaces, your wider search visibility."),
        ],
        "faq": [
            ("What&rsquo;s the difference between SEO and local SEO?", "SEO helps you rank for searches anywhere. Local SEO focuses on &ldquo;near me&rdquo; searches and your Google Business Profile, which matters most if customers visit you or you serve a specific area."),
            ("How long does local SEO take to work?", "Profile fixes can show movement within weeks; strong map rankings usually build over a few months, depending on competition."),
            ("Can you help with negative reviews?", "We can&rsquo;t remove genuine reviews, but we help you respond professionally and build a steady flow of new positive ones."),
            ("Do I need a website for local SEO to work?", "It helps, but your Google Business Profile can drive calls and visits even before your website is fully optimised."),
            ("Can you manage multiple locations?", "Yes. We manage Google Business Profiles and local pages for businesses with several branches or service areas."),
        ],
        "cta_intro": "tell us where you&rsquo;re based and who you want to reach, and we&rsquo;ll reply within one business day with a clear view of your current local visibility.",
    },
    "content-marketing": {
        "slug": "content-marketing", "nav_label": "Content Marketing", "name": "Content Marketing",
        "eyebrow": "Services · Content Marketing",
        "h1": "Content that brings in customers for years, not days",
        "lead": "we create useful blogs, guides and video that bring in customers for years, not days, and support your SEO at the same time.",
        "meta": "Content marketing - blogs, guides and video built to attract, inform and convert customers over the long term.",
        "ticks": ["Built to support SEO", "Written for real customers", "Blogs, guides &amp; video"],
        "badge": ("Built to last", "Years, not days", ""),
        "hero_img": "social-media-marketing-detail.webp", "hero_alt": "Content calendar and blog article being planned",
        "split_img": "aeo-ai-search-detail.webp", "split_alt": "Long-form article being written and structured",
        "why_title": "Most content is written once and forgotten.",
        "why_cards": [
            ("Most content is written once and forgotten.", "We plan content as an asset that keeps earning attention months and years after it&rsquo;s published."),
            ("Every piece has a job.", "Awareness, education or conversion &mdash; each piece of content is planned around what it needs to achieve."),
            ("Written for people, structured for search.", "Clear, useful writing that also follows the structure search engines and AI tools reward."),
            ("Quality over volume.", "One genuinely useful guide outperforms ten thin articles. We&rsquo;d rather do less, well."),
        ],
        "core_title": "What we create.", "core_sub": "Content built around what your customers actually ask.",
        "core_intro": "We plan, write and publish content that answers real questions and moves people toward getting in touch.",
        "core_cards": [
            ("Content strategy", "We plan topics around what your customers search for and where they are in their decision."),
            ("Blogs &amp; guides", "In-depth, useful articles that build authority and support your SEO."),
            ("Video &amp; short-form content", "Video content planned for your website and social channels."),
            ("Distribution &amp; repurposing", "One piece of content is reshaped into social posts, email and more, so nothing is wasted."),
        ],
        "g3_numbered": True, "g3_title": "How We Build Your Content Engine", "g3_sub": "From topic research to publishing rhythm.",
        "g3_intro": "Good content marketing is a system, not a one-off article.",
        "g3_cards": [
            ("Topic &amp; Keyword Research", "We find the questions your customers actually ask, and the gaps competitors haven&rsquo;t filled."),
            ("Content Planning", "A realistic content calendar built around your goals and capacity."),
            ("Writing &amp; Production", "Content is written, reviewed and optimised before it goes anywhere near your site."),
            ("Publish &amp; Promote", "We publish, distribute and track what works, then do more of it."),
        ],
        "g4_title": "Content Built to Compound", "g4_intro": "Good content keeps bringing in visitors long after the work of writing it is done.",
        "g4_cards": [
            ("Answers Real Questions", "Every piece solves a genuine problem your customers have."),
            ("Supports SEO &amp; AEO", "Structured so it helps you rank on Google and get quoted by AI tools."),
            ("Consistent Brand Voice", "Content sounds like your business, not a generic template."),
            ("Tracked &amp; Improved", "We see what performs and refine the plan every month."),
        ],
        "faq": [
            ("How is content marketing different from copywriting?", "Copywriting covers your core website pages. Content marketing is the ongoing blogs, guides and video that keep bringing in new visitors over time."),
            ("How often should we publish?", "Consistency matters more than frequency. We agree a realistic rhythm &mdash; often a few strong pieces a month rather than daily filler."),
            ("Will content marketing help my SEO?", "Yes. Well-structured, useful content is one of the strongest long-term ranking signals, alongside technical SEO and links."),
            ("Can you write in our brand voice?", "Yes. We learn how your business communicates and write to match, then you review everything before it&rsquo;s published."),
            ("How long until content marketing shows results?", "Early pieces can bring traffic within weeks, but content marketing is a compounding, long-term investment that builds over 6&ndash;12 months."),
        ],
        "cta_intro": "tell us about your business and your customers, and we&rsquo;ll reply within one business day with content ideas worth pursuing.",
    },
    "email-marketing": {
        "slug": "email-marketing", "nav_label": "Email Marketing", "name": "Email Marketing",
        "eyebrow": "Services · Email Marketing",
        "h1": "Stay in touch with past enquiries and turn them into repeat sales",
        "lead": "we help you stay in touch with past enquiries and customers and turn them into repeat sales, without spamming your list into unsubscribing.",
        "meta": "Email marketing campaigns and automated flows that turn past enquiries and customers into repeat business.",
        "ticks": ["Automated welcome &amp; follow-up flows", "Segmented, relevant sending", "Clear open &amp; click reporting"],
        "badge": ("Automated flows", "Welcome &middot; Follow-up &middot; Repeat", ""),
        "hero_img": "ppc-digital-advertising-detail.webp", "hero_alt": "Email campaign performance dashboard on screen",
        "split_img": "google-ads-detail.webp", "split_alt": "Email automation flow being mapped out",
        "why_title": "Your list is the audience you already have.",
        "why_cards": [
            ("Your list is the audience you already have.", "Past customers and enquiries are cheaper to sell to than strangers &mdash; email keeps you front of mind."),
            ("Automation does the remembering for you.", "Welcome and follow-up emails go out the moment they&rsquo;re needed, without anyone having to remember to send them."),
            ("Relevance beats frequency.", "Segmented, well-timed emails perform better than blasting your whole list with everything."),
            ("We watch deliverability, not just design.", "A beautiful email that lands in spam is worthless. We keep your sending reputation healthy."),
        ],
        "core_title": "What we set up.", "core_sub": "Campaigns and automations that keep working in the background.",
        "core_intro": "We build the flows and campaigns that turn your list into a genuine sales channel.",
        "core_cards": [
            ("Welcome &amp; nurture flows", "Automated sequences that introduce new subscribers to your business and guide them toward buying."),
            ("Newsletter &amp; campaigns", "Regular, useful email that keeps your business in customers&rsquo; inboxes without being annoying."),
            ("Abandoned enquiry follow-up", "Automated reminders for people who showed interest but didn&rsquo;t convert."),
            ("List segmentation &amp; targeting", "Emails sent to the right group of people, based on what they&rsquo;ve actually shown interest in."),
        ],
        "g3_numbered": True, "g3_title": "How We Build Your Email Marketing", "g3_sub": "From list audit to automated revenue.",
        "g3_intro": "We set up the foundations properly before sending a single campaign.",
        "g3_cards": [
            ("List &amp; Platform Audit", "We review your current list, tools and sending reputation before building anything new."),
            ("Flow &amp; Campaign Design", "We design the automated flows and campaign calendar around your sales cycle."),
            ("Build &amp; Test", "Emails are built, tested and proofed before anything goes to your full list."),
            ("Send, Track &amp; Improve", "We monitor opens, clicks and sales, and refine the plan every month."),
        ],
        "g4_title": "Email That Earns Its Place in the Inbox", "g4_intro": "People unsubscribe from emails that waste their time. We aim for the opposite.",
        "g4_cards": [
            ("Genuinely Useful", "Every email offers something worth opening, not just a sales pitch."),
            ("Properly Segmented", "The right message reaches the right group, not your whole list every time."),
            ("Mobile-Friendly Design", "Emails that look clean and work properly on a phone, where most people read them."),
            ("Clear Reporting", "You see opens, clicks and sales attributed back to email, in full."),
        ],
        "faq": [
            ("What email platform do you use?", "We work with popular platforms such as Mailchimp, Klaviyo and HubSpot, and recommend the one that fits your budget and CRM."),
            ("Do you write the email content?", "Yes. We plan, write and design campaigns and flows, and you approve everything before it sends."),
            ("How big does my list need to be?", "Any size. Automated welcome and follow-up flows are worth setting up even with a small list, since they keep working as it grows."),
            ("Will this help with GDPR compliance?", "We follow best practice for consent and unsubscribes, though you remain responsible for your own compliance obligations."),
            ("How do you measure success?", "Opens and clicks matter, but we focus on what they lead to &mdash; enquiries and sales &mdash; in your monthly report."),
        ],
        "cta_intro": "tell us about your list and your goals, and we&rsquo;ll reply within one business day with ideas for what to automate first.",
    },
    "lead-generation": {
        "slug": "lead-generation", "nav_label": "Lead Generation", "name": "Lead Generation",
        "eyebrow": "Services · Lead Generation",
        "h1": "Campaigns and landing pages designed to fill your enquiry inbox",
        "lead": "we design campaigns and landing pages that fill your enquiry inbox with people who are genuinely ready to buy.",
        "meta": "Lead generation campaigns and landing pages built to turn traffic into qualified enquiries, not just clicks.",
        "ticks": ["Landing pages built to convert", "Qualified leads, not just clicks", "Tracked from click to enquiry"],
        "badge": ("Focus", "Qualified leads", ""),
        "hero_img": "google-ads-hero.webp", "hero_alt": "Lead generation landing page and enquiry form on screen",
        "split_img": "ppc-digital-advertising-hero.webp", "split_alt": "Lead generation campaign results being reviewed",
        "why_title": "Traffic isn&rsquo;t the goal. Enquiries are.",
        "why_cards": [
            ("Traffic isn&rsquo;t the goal. Enquiries are.", "A page can get plenty of visitors and still generate nothing. We build and measure for enquiries."),
            ("One page, one job.", "Landing pages built for lead generation do one thing well, instead of trying to be a whole website."),
            ("Qualification saves everyone&rsquo;s time.", "The right form and messaging filter out poor-fit enquiries before they reach your inbox."),
            ("We test, not guess.", "Headlines, offers and forms are refined based on real data, not opinion."),
        ],
        "core_title": "What we build.", "core_sub": "The pages and campaigns that turn traffic into leads.",
        "core_intro": "We combine landing page design, clear offers and tracking to fill your pipeline with real opportunities.",
        "core_cards": [
            ("Conversion-focused landing pages", "Pages built around one clear offer and one clear action, with distractions removed."),
            ("Lead magnets &amp; offers", "Guides, quotes or consultations designed to give people a reason to hand over their details."),
            ("Form &amp; funnel optimisation", "Shorter, smarter forms and follow-up sequences that turn more visitors into enquiries."),
            ("Lead tracking &amp; reporting", "Every lead is tracked back to its source, so you know exactly what&rsquo;s working."),
        ],
        "g3_numbered": True, "g3_title": "How We Build Your Lead Generation", "g3_sub": "From offer to full enquiry pipeline.",
        "g3_intro": "A good lead generation system combines the right offer, the right page and the right traffic.",
        "g3_cards": [
            ("Offer &amp; Audience Research", "We identify what will genuinely make your ideal customer get in touch."),
            ("Landing Page Design", "A focused page built around your offer, with a clear, simple next step."),
            ("Traffic &amp; Promotion", "We connect the page to the right channels &mdash; SEO, ads or email &mdash; to drive qualified visitors."),
            ("Track &amp; Optimise", "We monitor conversion rates and refine the page and offer to improve results over time."),
        ],
        "g4_title": "Built to Fill Your Pipeline, Not Just Your Analytics", "g4_intro": "Vanity metrics don&rsquo;t pay the bills. We build around the numbers that do.",
        "g4_cards": [
            ("Clear, Single Offer", "No confusing choices &mdash; just one compelling reason to get in touch."),
            ("Friction Removed", "Short forms and clear next steps make enquiring effortless."),
            ("Qualified Over Quantity", "We&rsquo;d rather send you 20 good leads than 200 poor ones."),
            ("Every Lead Traceable", "You&rsquo;ll always know which channel and campaign a lead came from."),
        ],
        "faq": [
            ("What counts as a &ldquo;lead&rdquo;?", "We agree this upfront &mdash; usually a form submission, call or booking &mdash; so success is measured on something real, not just clicks."),
            ("Do you handle the traffic too?", "Yes, we can combine lead generation pages with SEO, PPC or email to drive the traffic that fills them."),
            ("How quickly will we see leads?", "Landing pages can start converting as soon as they&rsquo;re live and receiving traffic; volume builds as we optimise."),
            ("Can you integrate with our CRM?", "Yes, we connect lead forms to most common CRMs so new enquiries land exactly where your team already works."),
            ("How do you improve results over time?", "We test headlines, offers and forms against real conversion data, and keep what performs best."),
        ],
        "cta_intro": "tell us what a great lead looks like for your business, and we&rsquo;ll reply within one business day with ideas to generate more of them.",
    },
    "branding": {
        "slug": "branding", "nav_label": "Branding & Identity", "name": "Branding & Identity",
        "eyebrow": "Services · Branding & Identity",
        "h1": "A brand that makes your business feel established and trustworthy",
        "lead": "we create a logo and visual identity that make your business feel established and trustworthy from the very first impression.",
        "meta": "Branding and visual identity design - logo, colours and guidelines that make your business feel established and trustworthy.",
        "ticks": ["Logo &amp; visual identity", "Brand guidelines included", "Consistent across every touchpoint"],
        "badge": ("Delivered", "Logo + guidelines", ""),
        "hero_img": "about-pinky-brain-digital-team.webp", "hero_alt": "Brand identity moodboard and logo concepts on a desk",
        "split_img": "luxury-property-marketing.webp", "split_alt": "Branded materials shown in a real environment",
        "why_title": "People judge a business before they read a word.",
        "why_cards": [
            ("People judge a business before they read a word.", "Your logo, colours and design set an impression in seconds &mdash; before anyone reads what you actually do."),
            ("Consistency builds trust.", "A brand that looks the same everywhere feels reliable. A brand that looks different everywhere feels risky."),
            ("Your brand should reflect where you&rsquo;re going.", "We design for the business you&rsquo;re growing into, not just where you are today."),
            ("Guidelines save you money later.", "A proper brand kit means every future designer or supplier gets it right first time."),
        ],
        "core_title": "What&rsquo;s included.", "core_sub": "Everything needed to look consistent everywhere.",
        "core_intro": "We build a complete, practical identity your team can actually use.",
        "core_cards": [
            ("Logo design", "A distinctive mark that works at any size, from a favicon to a shopfront sign."),
            ("Colour &amp; typography system", "A defined palette and type system that keeps every touchpoint feeling consistent."),
            ("Brand guidelines", "A clear reference document so anyone working on your brand gets it right."),
            ("Templates &amp; assets", "Ready-to-use templates for social, documents and marketing materials."),
        ],
        "g3_numbered": True, "g3_title": "How We Build Your Brand", "g3_sub": "From first conversation to a brand you&rsquo;re proud of.",
        "g3_intro": "Good branding starts with understanding the business, not picking colours.",
        "g3_cards": [
            ("Discovery", "We learn about your business, customers and competitors before any design work starts."),
            ("Concept Development", "We design distinct directions for you to react to, then refine the one that fits best."),
            ("Refinement", "The chosen direction is refined across logo, colour and typography until it&rsquo;s ready."),
            ("Delivery &amp; Guidelines", "You receive final files, templates and a guidelines document covering everything."),
        ],
        "g4_title": "A Brand Built to Last", "g4_intro": "Trends fade. We design identities that still feel right in five years.",
        "g4_cards": [
            ("Distinctive, Not Generic", "A mark that stands out from competitors, not a template with your name swapped in."),
            ("Works Everywhere", "Designed to work as well on a website as it does on a van or a business card."),
            ("Easy to Apply", "Clear guidelines mean your team can use the brand confidently without you."),
            ("Room to Evolve", "A flexible system that can extend to new products or services later."),
        ],
        "faq": [
            ("Do you design logos only, or full brand identities?", "We can do either, but recommend a full identity &mdash; logo, colours, type and guidelines &mdash; so everything works together from day one."),
            ("How long does a branding project take?", "Typically 3&ndash;5 weeks depending on the number of concepts and rounds of feedback."),
            ("Can you rebrand an existing business?", "Yes. We can refresh or fully rebrand an existing identity, and advise on how to transition without confusing existing customers."),
            ("What files will I receive?", "Logo files in every format you need, your colour and font specifications, and a guidelines document."),
            ("Can you also design my website around the new brand?", "Yes, branding and website design work well together, and we can scope both as one project."),
        ],
        "cta_intro": "tell us about your business, and we&rsquo;ll reply within one business day with honest thoughts on what your brand needs.",
    },
    "graphic-design": {
        "slug": "graphic-design", "nav_label": "Graphic Design", "name": "Graphic Design",
        "eyebrow": "Services · Graphic Design",
        "h1": "Brochures, packs and social graphics that all look properly on brand",
        "lead": "we design brochures, property packs and social graphics that stay consistently on brand, wherever they appear.",
        "meta": "Graphic design for brochures, property packs, social graphics and marketing materials, kept consistently on brand.",
        "ticks": ["Print &amp; digital design", "Kept consistently on brand", "Fast turnaround available"],
        "badge": ("Design for", "Print &amp; Digital", ""),
        "hero_img": "ecommerce-store-design-detail.webp", "hero_alt": "Graphic design layouts being reviewed on screen",
        "split_img": "luxury-property-marketing.webp", "split_alt": "Printed brochure and property pack design",
        "why_title": "Off-brand design quietly costs you trust.",
        "why_cards": [
            ("Off-brand design quietly costs you trust.", "A brochure or post that doesn&rsquo;t match your brand makes a business look inconsistent, even if the work behind it is great."),
            ("Design should support a goal.", "Every piece is designed to do something &mdash; inform, sell or reassure &mdash; not just to look nice."),
            ("Templates keep you moving fast.", "We build reusable templates so your team can produce on-brand materials without waiting on us for everything."),
            ("Small details, done properly.", "Print-ready files, correct sizing and proper file handling save you costly reprints."),
        ],
        "core_title": "What we design.", "core_sub": "Every touchpoint, kept consistently on brand.",
        "core_intro": "From brochures to social graphics, we design materials that look like they belong to the same business.",
        "core_cards": [
            ("Brochures &amp; property packs", "Polished, print-ready materials that represent your business properly."),
            ("Social media graphics", "On-brand templates for posts, stories and ads that keep your feed consistent."),
            ("Presentations &amp; documents", "Proposals, pitch decks and reports that look as professional as your work."),
            ("Signage &amp; print materials", "Business cards, signage and other print, prepared correctly for the printer."),
        ],
        "g3_numbered": True, "g3_title": "How We Work", "g3_sub": "From brief to finished, print-ready files.",
        "g3_intro": "A clear process keeps design projects on time and on brand.",
        "g3_cards": [
            ("Brief &amp; Brand Review", "We understand what the piece needs to achieve and review your existing brand assets."),
            ("Concepts", "We design initial layouts for you to react to before refining further."),
            ("Refinement", "We revise based on your feedback until the design is exactly right."),
            ("Final Files", "You receive print-ready and digital files, correctly formatted and sized."),
        ],
        "g4_title": "Design That Looks Like One Business", "g4_intro": "Consistency is what makes a growing business feel established.",
        "g4_cards": [
            ("On-Brand, Every Time", "Colours, fonts and style stay consistent across every piece we design."),
            ("Built for Purpose", "Print materials are print-ready; digital materials are optimised for screens."),
            ("Fast Turnaround Available", "We can accommodate quick-turnaround requests for time-sensitive materials."),
            ("Reusable Templates", "Where useful, we build templates so your team can self-serve future materials."),
        ],
        "faq": [
            ("Do you need our brand guidelines to start?", "It helps, but if you don&rsquo;t have any, we can work from your existing website and materials, or build guidelines as part of a branding project."),
            ("Can you design for both print and digital?", "Yes, we design and correctly prepare files for both, including print-ready specifications."),
            ("How quickly can you turn around a design?", "It depends on complexity, but we can accommodate urgent requests &mdash; just let us know your deadline upfront."),
            ("Do you offer ongoing design support?", "Yes, many clients keep us on for regular design needs rather than booking one-off projects each time."),
            ("Can you match an existing brand exactly?", "Yes, we can work precisely within an existing brand&rsquo;s colours, fonts and style."),
        ],
        "cta_intro": "tell us what you need designed, and we&rsquo;ll reply within one business day with a clear quote and timeline.",
    },
    "video-photography": {
        "slug": "video-photography", "nav_label": "Video & Photography", "name": "Video & Photography",
        "eyebrow": "Services · Video & Photography",
        "h1": "Photos and video that show your property, product or team at its best",
        "lead": "we produce photos and video that show your property, product or team at its best, the kind of content that makes people stop scrolling.",
        "meta": "Professional photography and video production for property, product and brand marketing.",
        "ticks": ["Property, product &amp; brand shoots", "Edited &amp; ready to publish", "Licensed for your marketing"],
        "badge": ("Delivered", "Edited &amp; ready to use", ""),
        "hero_img": "luxury-property-marketing.webp", "hero_alt": "Professional property photography at dusk",
        "split_img": "about-pinky-brain-digital-team.webp", "split_alt": "Video production team filming on location",
        "why_title": "People decide in seconds, and images do the deciding.",
        "why_cards": [
            ("People decide in seconds, and images do the deciding.", "Before anyone reads your copy, they&rsquo;ve already judged you on your photos and video."),
            ("Phone photos cost you credibility.", "Professional imagery signals a professional business, especially for premium products and property."),
            ("Video earns attention that photos can&rsquo;t.", "Short-form video consistently gets more reach and engagement across social platforms."),
            ("One shoot, many uses.", "We plan shoots to deliver content for your website, social and ads all at once."),
        ],
        "core_title": "What we shoot.", "core_sub": "Imagery built for how it will actually be used.",
        "core_intro": "We plan every shoot around where the content will appear, so nothing gets wasted.",
        "core_cards": [
            ("Property &amp; interior photography", "Bright, professional photography that presents property at its absolute best."),
            ("Product photography", "Clean, consistent product shots ready for your website and online store."),
            ("Brand &amp; team photography", "Authentic photography that puts a real face to your business."),
            ("Short-form video", "Video content edited for your website, social channels and ads."),
        ],
        "g3_numbered": True, "g3_title": "How a Shoot Works", "g3_sub": "From brief to finished, edited content.",
        "g3_intro": "A clear plan means the shoot day runs smoothly and delivers exactly what you need.",
        "g3_cards": [
            ("Planning", "We agree locations, shot list and style before the shoot day."),
            ("The Shoot", "Our photographer or videographer captures everything on the agreed list, plus extras."),
            ("Editing", "Images and video are professionally edited and colour-graded."),
            ("Delivery", "You receive final files, formatted and sized for every platform you need."),
        ],
        "g4_title": "Content That Actually Gets Used", "g4_intro": "The best photography is the kind that ends up everywhere &mdash; website, social and ads.",
        "g4_cards": [
            ("Shot for Multiple Uses", "One shoot delivers content for your website, social and print at once."),
            ("Consistent Style", "Imagery that matches your brand&rsquo;s tone, every time."),
            ("Fast Editing Turnaround", "Edited files delivered quickly, so content doesn&rsquo;t go stale."),
            ("Rights Included", "You get full usage rights for your own marketing."),
        ],
        "faq": [
            ("Do you shoot on location or in a studio?", "Both &mdash; property and brand shoots are usually on location; product photography can be studio or on-site, depending on what suits the product."),
            ("How long does a shoot take?", "It depends on the brief, but most property or brand shoots take half a day to a full day."),
            ("Do we get the raw files?", "We deliver final, edited files. Raw files can be included by request, agreed before the shoot."),
            ("Can you handle video and photography in one shoot?", "Yes, we often combine both in a single session to save time and cost."),
            ("How quickly will we get the final content?", "Typical turnaround is 5&ndash;10 working days, though we can prioritise urgent deadlines."),
        ],
        "cta_intro": "tell us what you need shot, and we&rsquo;ll reply within one business day with availability and a clear quote.",
    },
    "copywriting": {
        "slug": "copywriting", "nav_label": "Copywriting", "name": "Copywriting",
        "eyebrow": "Services · Copywriting",
        "h1": "Clear words that explain what you do and persuade people to get in touch",
        "lead": "we write clear copy that explains what you do and persuades people to get in touch, without sounding like everyone else.",
        "meta": "Copywriting for websites, brochures and marketing that explains what you do clearly and persuades people to act.",
        "ticks": ["Written for your customers", "Clear, jargon-free English", "SEO-aware from the start"],
        "badge": ("Written for", "Clarity &amp; conversion", ""),
        "hero_img": "aeo-ai-search-detail.webp", "hero_alt": "Website copy being written and edited on screen",
        "split_img": "social-media-marketing-detail.webp", "split_alt": "Marketing copy being reviewed and refined",
        "why_title": "Confusing copy costs you customers.",
        "why_cards": [
            ("Confusing copy costs you customers.", "If visitors can&rsquo;t quickly understand what you offer, most simply leave rather than work it out."),
            ("Clever isn&rsquo;t the goal. Clear is.", "We write to be understood in seconds, not to sound impressive."),
            ("Every page has a job.", "We write with a clear purpose for each page &mdash; inform, reassure or persuade &mdash; not just fill space."),
            ("Your voice, not a template.", "We learn how your business actually talks and write to match, not a generic corporate tone."),
        ],
        "core_title": "What we write.", "core_sub": "Words for every part of your business.",
        "core_intro": "From your homepage to your email sequences, we write copy that does a job.",
        "core_cards": [
            ("Website copy", "Homepage, service and about pages written to explain and convert."),
            ("Brochures &amp; sales materials", "Persuasive copy for the materials your sales team actually hands over."),
            ("SEO-aware content", "Copy written for people first, but structured to support your search visibility too."),
            ("Taglines &amp; messaging", "Sharp, memorable lines that sum up what your business stands for."),
        ],
        "g3_numbered": True, "g3_title": "How We Write Your Copy", "g3_sub": "From brief to words you&rsquo;re proud to publish.",
        "g3_intro": "Good copy starts with understanding the business and the customer, not a blank page.",
        "g3_cards": [
            ("Brief &amp; Research", "We learn about your business, customers and competitors before writing a word."),
            ("First Draft", "We write a full draft built around a clear structure and purpose for each page."),
            ("Review &amp; Refine", "You give feedback and we refine until the tone and message feel exactly right."),
            ("Final Delivery", "You receive final copy, ready to drop straight into your website or materials."),
        ],
        "g4_title": "Copy That Does a Job", "g4_intro": "Good copywriting doesn&rsquo;t just read well &mdash; it moves people to act.",
        "g4_cards": [
            ("Clear in Seconds", "Visitors understand what you offer without having to work for it."),
            ("Built to Persuade", "Every page guides the reader toward a clear next step."),
            ("Consistent Tone", "Your business sounds like the same business, everywhere."),
            ("SEO-Friendly Structure", "Written to read naturally while still supporting search visibility."),
        ],
        "faq": [
            ("Do you write in our existing tone of voice?", "Yes. We learn how your business communicates and match it, or help define a tone if you don&rsquo;t have one yet."),
            ("Can you write and optimise for SEO at the same time?", "Yes, we write for people first but structure content to support your target keywords and search visibility."),
            ("How many revisions are included?", "We include revision rounds as standard so the final copy feels exactly right before delivery."),
            ("Can you write for a technical or niche industry?", "Yes, we research thoroughly and can work with your team&rsquo;s input to get technical details right."),
            ("Do you write blog content too?", "Yes, ongoing blog and content writing is covered under our content marketing service, which pairs well with copywriting."),
        ],
        "cta_intro": "tell us what needs writing, and we&rsquo;ll reply within one business day with a clear quote and timeline.",
    },
    "ai-automation": {
        "slug": "ai-automation", "nav_label": "AI Automation & Chatbots", "name": "AI Automation & Chatbots",
        "eyebrow": "Services · AI Automation & Chatbots",
        "h1": "Let AI answer common questions and follow up leads while you sleep",
        "lead": "we set up AI to answer common questions and follow up leads while you sleep, so no enquiry waits until Monday morning.",
        "meta": "AI automation and chatbots that answer common questions and follow up leads automatically, day or night.",
        "ticks": ["Answers common questions instantly", "Follows up leads automatically", "Handed over when it&rsquo;s complex"],
        "badge": ("Always on", "24/7 response", ""),
        "hero_img": "aeo-ai-search-hero.webp", "hero_alt": "AI chatbot conversation shown on a website",
        "split_img": "website-design-development-process.webp", "split_alt": "AI automation workflow being configured",
        "why_title": "The first reply often wins the customer.",
        "why_cards": [
            ("The first reply often wins the customer.", "Whoever responds first is often who gets the enquiry. AI means you never lose that race to a competitor."),
            ("Automation should feel helpful, not robotic.", "We build flows that genuinely answer questions, and hand over to a real person the moment it gets complex."),
            ("Your team&rsquo;s time goes further.", "Repetitive questions get handled automatically, freeing your team for the enquiries that need a human."),
            ("We&rsquo;re realistic about what AI can do.", "We won&rsquo;t oversell it. AI handles the predictable; people handle the rest."),
        ],
        "core_title": "What we build.", "core_sub": "Automation that saves time without losing the personal touch.",
        "core_intro": "We combine chatbots, automated follow-up and workflow automation around your actual enquiries.",
        "core_cards": [
            ("Website chatbots", "AI chat that answers common questions instantly, day or night."),
            ("Automated lead follow-up", "New enquiries get an immediate, helpful response while you&rsquo;re unavailable."),
            ("Booking &amp; workflow automation", "Automated booking confirmations, reminders and internal handoffs."),
            ("CRM &amp; tool integration", "AI automation connected to the tools you already use, not a separate silo."),
        ],
        "g3_numbered": True, "g3_title": "How We Build Your Automation", "g3_sub": "From common questions to a working system.",
        "g3_intro": "We start with what&rsquo;s actually repetitive, not with the flashiest AI feature.",
        "g3_cards": [
            ("Process Review", "We find the repetitive questions and tasks worth automating."),
            ("Flow Design", "We design conversation flows and automations around real customer journeys."),
            ("Build &amp; Train", "The chatbot or automation is built and trained on your business&rsquo; actual information."),
            ("Launch &amp; Refine", "We monitor real conversations and refine the flows based on what people actually ask."),
        ],
        "g4_title": "AI That Knows When to Step Back", "g4_intro": "The goal isn&rsquo;t to replace your team &mdash; it&rsquo;s to remove the repetitive parts of their day.",
        "g4_cards": [
            ("Answers Instantly", "Common questions get a helpful answer the moment they&rsquo;re asked."),
            ("Hands Over Cleanly", "Complex queries are passed to your team with full context, not lost."),
            ("Works Around the Clock", "Enquiries outside business hours still get an immediate response."),
            ("Keeps Improving", "We refine the automation as we see what customers actually ask."),
        ],
        "faq": [
            ("Will a chatbot feel impersonal to customers?", "Not if it&rsquo;s built well. We design flows that are genuinely helpful and hand over to a real person as soon as a query needs one."),
            ("What can AI automation actually handle?", "Common questions, booking confirmations, lead follow-up and repetitive admin. Anything nuanced is routed to your team."),
            ("Do you build on our existing website and tools?", "Yes, we integrate with your existing website, CRM and booking tools rather than replacing them."),
            ("How long does it take to set up?", "Simple chatbots can launch within a couple of weeks; more complex automations take longer depending on integrations."),
            ("Will it keep working as our business changes?", "We can update the automation&rsquo;s knowledge and flows as your services, pricing or processes change."),
        ],
        "cta_intro": "tell us what&rsquo;s eating up your team&rsquo;s time, and we&rsquo;ll reply within one business day with realistic ideas for what to automate.",
    },
    "crm": {
        "slug": "crm", "nav_label": "CRM Setup & Integration", "name": "CRM Setup & Integration",
        "eyebrow": "Services · CRM Setup & Integration",
        "h1": "One place to track every enquiry, so no customer slips through the cracks",
        "lead": "we set up one place to track every enquiry, so no customer slips through the cracks between email, phone and forms.",
        "meta": "CRM setup and integration to track every enquiry in one place, connected to your website and marketing tools.",
        "ticks": ["One system for every enquiry", "Connected to your website &amp; ads", "Set up around your sales process"],
        "badge": ("One inbox", "For every enquiry", ""),
        "hero_img": "website-design-development-process.webp", "hero_alt": "CRM dashboard showing customer enquiries",
        "split_img": "homepage-hero-digital-agency-team.webp", "split_alt": "Sales pipeline being reviewed by the team",
        "why_title": "Scattered enquiries mean lost customers.",
        "why_cards": [
            ("Scattered enquiries mean lost customers.", "When leads live across email, spreadsheets and sticky notes, some inevitably get missed."),
            ("A CRM should fit your process, not fight it.", "We configure the system around how your team actually sells, not a generic default setup."),
            ("Adoption matters more than features.", "The best CRM is the one your team actually uses. We keep setups simple and practical."),
            ("Connected beats isolated.", "A CRM disconnected from your website and ads is just another spreadsheet. We integrate it properly."),
        ],
        "core_title": "What we set up.", "core_sub": "A CRM that actually gets used.",
        "core_intro": "We configure, connect and train your team on a system built around your real sales process.",
        "core_cards": [
            ("CRM selection &amp; setup", "We recommend and configure the right CRM for your size, budget and sales process."),
            ("Website &amp; form integration", "Enquiries from your website land directly in the CRM, automatically."),
            ("Pipeline &amp; automation setup", "Deal stages, reminders and follow-up tasks configured around how you actually sell."),
            ("Team training", "We train your team so the system gets used properly from day one."),
        ],
        "g3_numbered": True, "g3_title": "How We Set Up Your CRM", "g3_sub": "From process mapping to a system your team trusts.",
        "g3_intro": "We build around your existing sales process rather than forcing you into someone else&rsquo;s.",
        "g3_cards": [
            ("Process Mapping", "We learn how enquiries currently move from first contact to sale."),
            ("CRM Configuration", "The CRM is set up to match that process, not a generic default."),
            ("Integration", "Your website, forms and other tools are connected so data flows automatically."),
            ("Training &amp; Handover", "Your team is trained and supported until the system is second nature."),
        ],
        "g4_title": "A CRM Your Team Actually Uses", "g4_intro": "A powerful CRM nobody logs into is worse than no CRM at all.",
        "g4_cards": [
            ("Simple by Design", "We configure only what your team needs, not every possible feature."),
            ("Nothing Falls Through", "Every enquiry is captured and tracked automatically."),
            ("Clear Reporting", "See exactly where enquiries come from and how many convert."),
            ("Grows With You", "The setup can expand as your team and process mature."),
        ],
        "faq": [
            ("Which CRM platforms do you work with?", "We work with popular platforms such as HubSpot, Pipedrive and Zoho, and recommend the one that fits your budget and needs."),
            ("Can you migrate our existing data?", "Yes, we can import existing contacts and deal history from spreadsheets or another CRM."),
            ("Will our website enquiries feed in automatically?", "Yes, we connect your website forms so new enquiries land directly in the CRM without manual entry."),
            ("Do you provide training for our team?", "Yes, training is included so your team is confident using the system from launch."),
            ("How long does a CRM setup take?", "Simple setups can take 1&ndash;2 weeks; more complex integrations take longer depending on your existing tools."),
        ],
        "cta_intro": "tell us how enquiries reach you today, and we&rsquo;ll reply within one business day with a clear plan to bring it all together.",
    },
    "cyber-security": {
        "slug": "cyber-security", "nav_label": "Cyber Security", "name": "Cyber Security",
        "eyebrow": "Services · Cyber Security",
        "h1": "Protect your website and customer data from hackers and downtime",
        "lead": "we protect your website and customer data from hackers and downtime, with expert advice rather than scare tactics.",
        "meta": "Cyber security for websites and customer data - monitoring, hardening and expert advice, not scare tactics.",
        "ticks": ["Security monitoring &amp; hardening", "Backups &amp; recovery plans", "Expert advice"],
        "badge": ("Monitored", "Around the clock", ""),
        "hero_img": "website-design-service-hero.webp", "hero_alt": "Website security dashboard shown on a laptop",
        "split_img": "aeo-ai-search-detail.webp", "split_alt": "Security review being carried out on a website",
        "why_title": "Most attacks target easy targets, not big ones.",
        "why_cards": [
            ("Most attacks target easy targets, not big ones.", "Automated attacks scan for unpatched, poorly configured websites &mdash; size rarely matters."),
            ("Downtime costs more than the fix.", "Lost trading time and reputation damage usually outweigh the cost of proper prevention."),
            ("We explain risk clearly.", "No scare tactics or jargon &mdash; just a clear view of your actual risk and what to do about it."),
            ("Prevention is cheaper than recovery.", "Ongoing monitoring and backups cost far less than recovering from a serious breach."),
        ],
        "core_title": "What we cover.", "core_sub": "The essentials that keep your website and data safe.",
        "core_intro": "We combine monitoring, hardening and backups so problems get caught before they become disasters.",
        "core_cards": [
            ("Security audits", "A clear review of your current risks, in full, with a prioritised action plan."),
            ("Website hardening", "Firewalls, malware scanning and configuration fixes that close common attack routes."),
            ("Backups &amp; recovery", "Regular, tested backups so you can recover quickly if the worst happens."),
            ("Ongoing monitoring", "Continuous monitoring that flags issues before they become serious problems."),
        ],
        "g3_numbered": True, "g3_title": "How We Secure Your Website", "g3_sub": "From audit to ongoing protection.",
        "g3_intro": "We fix what&rsquo;s urgent first, then keep watching.",
        "g3_cards": [
            ("Security Audit", "We review your website, hosting and plugins for known vulnerabilities."),
            ("Hardening", "We fix priority issues &mdash; outdated software, weak configurations and access controls."),
            ("Backup Setup", "Regular, tested backups are put in place, stored securely off-site."),
            ("Ongoing Monitoring", "We monitor continuously and respond quickly if anything looks wrong."),
        ],
        "g4_title": "Security That Doesn&rsquo;t Get in Your Way", "g4_intro": "Good security should be invisible day-to-day, and obvious the moment it&rsquo;s needed.",
        "g4_cards": [
            ("Comprehensive Reporting", "You understand your risk without needing a technical background."),
            ("Proactive, Not Reactive", "We aim to catch issues before they become incidents."),
            ("Tested Backups", "Backups are actually tested, not just taken and forgotten."),
            ("Fast Response", "If something does happen, we respond quickly to limit the damage."),
        ],
        "faq": [
            ("Is my website really a target?", "Yes &mdash; most attacks are automated and scan the whole internet for weak configurations, regardless of business size."),
            ("What happens if my site does get hacked?", "We isolate the issue, restore from a clean backup and identify how it happened, so it doesn&rsquo;t happen again."),
            ("Do you offer ongoing monitoring, or one-off audits?", "Both. Many clients start with an audit, then move to ongoing monitoring and maintenance."),
            ("Will security measures slow my website down?", "No, done properly, security measures have minimal impact on site speed."),
            ("Can you secure any type of website?", "We primarily work with WordPress and WooCommerce sites, but can advise on other platforms too."),
        ],
        "cta_intro": "tell us about your current setup, and we&rsquo;ll reply within one business day with an honest view of your risk.",
    },
    "website-maintenance": {
        "slug": "website-maintenance", "nav_label": "Website Care & Hosting", "name": "Website Care & Hosting",
        "eyebrow": "Services · Website Care & Hosting",
        "h1": "We keep your site fast, updated and online, so you don&rsquo;t have to",
        "lead": "we keep your site fast, updated, backed up and online, so you don’t have to think about it.",
        "meta": "Website care plans and hosting - updates, backups, speed and uptime monitoring, so your site is always looked after.",
        "ticks": ["Managed hosting", "Updates &amp; backups handled", "Fast, responsive support"],
        "badge": ("Uptime", "Monitored 24/7", ""),
        "hero_img": "website-design-development-process.webp", "hero_alt": "Website hosting and maintenance dashboard",
        "split_img": "homepage-hero-digital-agency-team.webp", "split_alt": "Support team monitoring website performance",
        "why_title": "Websites don&rsquo;t stay finished.",
        "why_cards": [
            ("Websites don&rsquo;t stay finished.", "Plugins, themes and platforms all need regular updates, or your site quietly becomes a security risk."),
            ("Small issues become big ones if ignored.", "A slow site or broken plugin left unchecked can eventually mean lost sales or downtime."),
            ("You shouldn&rsquo;t need to be technical.", "We handle the technical side so you can focus on running your business."),
            ("Fast support, real people.", "When something needs fixing, you get a real response, not a ticket number and a wait."),
        ],
        "core_title": "What&rsquo;s included.", "core_sub": "Everything that keeps a website healthy.",
        "core_intro": "We handle the ongoing technical care that most businesses don&rsquo;t have time for.",
        "core_cards": [
            ("Managed hosting", "Fast, secure hosting set up and managed on your behalf."),
            ("Updates &amp; patches", "Themes, plugins and core software kept up to date and compatible."),
            ("Backups &amp; monitoring", "Regular backups and uptime monitoring, so problems are caught early."),
            ("Ongoing support", "Small edits, fixes and questions handled by a real person."),
        ],
        "g3_numbered": True, "g3_title": "How Care Plans Work", "g3_sub": "From handover to ongoing peace of mind.",
        "g3_intro": "We look after the technical details in the background, month after month.",
        "g3_cards": [
            ("Handover &amp; Audit", "We review your current site and set up monitoring, backups and hosting."),
            ("Regular Updates", "Software and plugins are kept updated on a regular schedule."),
            ("Monitoring", "Uptime and performance are monitored continuously."),
            ("Support &amp; Reporting", "You get ongoing support and a simple monthly summary of what&rsquo;s been done."),
        ],
        "g4_title": "One Less Thing to Worry About", "g4_intro": "A well cared-for website quietly keeps working, month after month, without you thinking about it.",
        "g4_cards": [
            ("Always Up to Date", "Software stays current, reducing security risk and compatibility issues."),
            ("Backed Up Properly", "Regular backups mean you can always recover quickly if needed."),
            ("Fast When It Matters", "Ongoing performance checks keep your site loading quickly."),
            ("Real Support", "A real person to call when something needs fixing."),
        ],
        "faq": [
            ("Do I need a care plan if my site is new?", "Yes &mdash; even new sites need ongoing updates and backups. It&rsquo;s far cheaper than fixing a neglected site later."),
            ("What&rsquo;s included in monthly support?", "Updates, backups, monitoring and a set amount of small edits or fixes each month, detailed in your plan."),
            ("Can you take over a site built by someone else?", "Yes, we regularly take over care of existing sites, starting with a full audit to understand what&rsquo;s there."),
            ("What happens if my site goes down?", "Our monitoring flags downtime immediately, and we act quickly to get it back online."),
            ("Can I cancel a care plan any time?", "Yes, our plans are flexible with no long lock-in contracts."),
        ],
        "cta_intro": "tell us about your current website, and we&rsquo;ll reply within one business day with a care plan that fits.",
    },
    "digital-consulting": {
        "slug": "digital-consulting", "nav_label": "Digital Consulting", "name": "Digital Consulting",
        "eyebrow": "Services · Digital Consulting",
        "h1": "Not sure what you actually need? Let&rsquo;s find out, honestly",
        "lead": "not sure what you actually need? We look at your website and marketing, then tell you plainly where your money is best spent and what can wait.",
        "meta": "Digital consulting - a comprehensive review of your website and marketing, with a prioritised, honest plan.",
        "ticks": ["Comprehensive review", "Prioritised plan with costs", "No jargon, no obligation"],
        "badge": ("Delivered", "A clear, honest plan", ""),
        "hero_img": "homepage-hero-digital-agency-team.webp", "hero_alt": "Digital strategy consultation in progress",
        "split_img": "about-pinky-brain-digital-team.webp", "split_alt": "Consultant reviewing a website and marketing plan",
        "why_title": "Most businesses don&rsquo;t need everything at once.",
        "why_cards": [
            ("Most businesses don&rsquo;t need everything at once.", "We tell you what genuinely matters now, and what can reasonably wait, instead of selling you everything."),
            ("We look at the whole picture.", "Website, SEO, ads and social are reviewed together, not as separate boxes to tick."),
            ("You&rsquo;ll get a plan, not just opinions.", "Every recommendation comes with a rough cost and priority, so you can actually act on it."),
            ("No obligation to hire us afterwards.", "Some clients take the plan and run with their own team. That&rsquo;s absolutely fine."),
        ],
        "core_title": "What&rsquo;s included.", "core_sub": "A clear-eyed look at where your money is best spent.",
        "core_intro": "We review what you have, benchmark it against competitors, and tell you honestly what to do next.",
        "core_cards": [
            ("Website &amp; SEO review", "An honest assessment of your current site&rsquo;s performance, structure and search visibility."),
            ("Marketing audit", "A look at your current social, ads and content, and what&rsquo;s actually working."),
            ("Competitor benchmarking", "We show you where you stand against the businesses you&rsquo;re actually competing with."),
            ("Prioritised action plan", "A clear, costed list of what to do first, next and later."),
        ],
        "g3_numbered": True, "g3_title": "How a Consultation Works", "g3_sub": "From first look to a plan you can act on.",
        "g3_intro": "A structured review keeps the process quick and the advice genuinely useful.",
        "g3_cards": [
            ("Discovery Call", "We learn about your business, goals and current frustrations."),
            ("Full Review", "We audit your website, marketing and competitors in detail."),
            ("Findings &amp; Plan", "We present clear findings and a prioritised, costed plan."),
            ("Next Steps", "You decide what to act on &mdash; with us, your own team, or elsewhere."),
        ],
        "g4_title": "Advice You Can Actually Use", "g4_intro": "A good consultation leaves you clearer, not more confused.",
        "g4_cards": [
            ("Clear Guidance, Always", "No jargon &mdash; just a clear explanation of what matters and why."),
            ("Honest Prioritisation", "We tell you what to do first, and what genuinely can wait."),
            ("Costed Recommendations", "Every suggestion comes with a realistic sense of cost and effort."),
            ("No Pressure", "You&rsquo;re free to use the plan however, and with whoever, you choose."),
        ],
        "faq": [
            ("Is this just a sales pitch for your services?", "No. We&rsquo;re paid for the consultation itself, and the plan is yours to use however you like, with us or otherwise."),
            ("How long does a consultation take?", "Typically a discovery call plus a review, with findings delivered within a week or two."),
            ("What will I actually receive?", "A written, prioritised plan covering website, SEO and marketing, with rough costs and timings for each recommendation."),
            ("Is this suitable for a business with no website yet?", "Yes, it&rsquo;s just as useful for planning a first website and marketing approach as it is for improving an existing one."),
            ("Do you offer this as an ongoing service?", "Most clients start with a one-off consultation, then decide whether ongoing advisory support makes sense."),
        ],
        "cta_intro": "tell us where you&rsquo;re stuck, and we&rsquo;ll reply within one business day to arrange a straight-talking consultation.",
    },
}
EXTRA_SERVICE_ORDER = ["app-development", "custom-software", "local-seo", "content-marketing", "email-marketing",
                        "lead-generation", "branding", "graphic-design", "video-photography", "copywriting",
                        "ai-automation", "crm", "cyber-security", "website-maintenance", "digital-consulting"]
SERVICES.update(EXTRA_SERVICES)

SERVICE_ORDER = ["seo-services", "website-design", "e-commerce-websites-design", "aeo-ai-search",
                  "ppc-digital-advertising", "social-media", "google-ads"]
ALL_SERVICE_SLUGS = SERVICE_ORDER + EXTRA_SERVICE_ORDER

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

# Which services get location (city) landing pages
LOCATION_SERVICE_KEY = {
    "Website Design": "website-design",
    "SEO Services": "seo-services",
}
REGION_FULL = {"USA": "the United States", "Canada": "Canada", "UK": "the United Kingdom", "Europe": "Europe"}

WHY_INTRO = "Honest advice, a flexible approach and clear communication, from the first conversation to long after launch."
OUTCOME_ICONS = ['growth', 'users', 'check', 'chart']

# Fill these in when the details exist; the footer / contact form pick them up automatically.
SOCIAL_LINKS = {}      # e.g. {"LinkedIn": "https://www.linkedin.com/company/..."}
FORM_ENDPOINT = ""     # e.g. a Formspree / Web3Forms URL. Empty = the form opens the visitor's email app instead.

# ---------------------------------------------------------------------------
# SHARED HELPERS
# ---------------------------------------------------------------------------
def cap_first(s):
    return s[0].upper() + s[1:] if s and s[0].isalpha() else s

def lc_first(s):
    return s[0].lower() + s[1:] if s else s

def join_list(items):
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]

def esc_amp(s):
    return re.sub(r"&(?!#?\w+;)", "&amp;", s)

def finalize_html(doc):
    """Escape bare ampersands in markup, leaving <script> and <style> untouched."""
    parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>)", doc, flags=re.S | re.I)
    return "".join(p if i % 2 else esc_amp(p) for i, p in enumerate(parts))

def write_page(filename, doc):
    path = os.path.join(ROOT, filename)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(finalize_html(doc))
    return path

class Alt:
    """Alternates section backgrounds white / tinted."""
    def __init__(self, start=False):
        self.v = start
    def next(self):
        v = self.v
        self.v = not self.v
        return v

def page_url(filename):
    return SITE_URL + ("/" if filename == "index.html" else "/" + filename)

# ---------------------------------------------------------------------------
# HEAD / HEADER / FOOTER
# ---------------------------------------------------------------------------
def head_html(root, title, description, filename, noindex=False, extra_head=""):
    canon = page_url(filename)
    t_text = html.escape(html.unescape(title), quote=False)
    t_attr = html.escape(html.unescape(title), quote=True)
    d_attr = html.escape(html.unescape(description), quote=True)
    robots = '<meta name="robots" content="noindex, follow">\n' if noindex else ""
    return """<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(t_text)s</title>
<meta name="description" content="%(d)s">
%(extra_head)s%(robots)s<link rel="canonical" href="%(canon)s">
<meta name="theme-color" content="#01265A">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pinky Brain Digital">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="%(t_attr)s">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="%(canon)s">
<link rel="icon" href="%(root)sfavicon.ico" sizes="any">
<link rel="icon" type="image/png" href="%(root)simages/favicon-32.png" sizes="32x32">
<link rel="icon" type="image/png" href="%(root)simages/favicon-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="%(root)simages/favicon-180.png">
<link rel="preload" href="%(root)sassets/fonts/general-sans-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="%(root)sassets/fonts/general-sans-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sassets/css/site.css">
</head>
<body>
<a class="pb-skip" href="#main">Skip to main content</a>
""" % {"t_text": t_text, "t_attr": t_attr, "d": d_attr, "robots": robots, "canon": canon, "root": root, "extra_head": extra_head}

def _mega_html(root):
    groups = []
    for gname, slugs in SERVICE_GROUPS:
        links = "".join('<li><a href="%s%s.html">%s</a></li>' % (root, sl, SERVICES[sl]["nav_label"]) for sl in slugs)
        groups.append('<div class="pb-mega__group"><p class="pb-mega__title">%s</p><ul>%s</ul></div>' % (gname, links))
    return "".join(groups)

def _mobile_groups_html(root):
    out = ['<a class="pb-mobile-all" href="%sservices.html">All services</a>' % root]
    for gname, slugs in SERVICE_GROUPS:
        links = "".join('<li><a href="%s%s.html">%s</a></li>' % (root, sl, SERVICES[sl]["nav_label"]) for sl in slugs)
        out.append('<p class="pb-mobile-grouptitle">%s</p><ul>%s</ul>' % (gname, links))
    return "".join(out)

def header_html(root, current=None):
    def cur(name):
        return ' aria-current="page"' if current == name else ""
    chevron = '<svg class="pb-i" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
    return """
<header class="pb-header">
  <div class="pb-wrap pb-header__bar">
    <a class="pb-header__logo" href="%(root)sindex.html" aria-label="Pinky Brain Digital, home">
      <img src="%(root)simages/logo.png" alt="Pinky Brain Digital" width="192" height="64">
    </a>
    <nav class="pb-nav" aria-label="Main">
      <ul class="pb-nav__list">
        <li class="pb-has-mega">
          <a href="%(root)sservices.html"%(c_services)s>Services</a>
          <button type="button" class="pb-nav__toggle" aria-expanded="false" aria-controls="pb-mega" aria-label="Show the services menu">%(chevron)s</button>
          <div class="pb-mega" id="pb-mega">
            <div class="pb-mega__panel">
              <div class="pb-mega__grid">%(mega)s</div>
              <div class="pb-mega__foot"><span>Not sure what you need? We&rsquo;ll point you in the right direction.</span><a class="pb-link" href="%(root)sservices.html">%(secondary)s %(arrow)s</a></div>
            </div>
          </div>
        </li>
        <li><a href="%(root)slocations.html"%(c_locations)s>Locations</a></li>
        <li><a href="%(root)sabout-us.html"%(c_about)s>About Us</a></li>
        <li><a href="%(root)sblog.html"%(c_insights)s>Insights</a></li>
      </ul>
      <a class="pb-btn pb-btn--dark pb-nav__cta" href="%(root)scontact-us.html">%(primary)s</a>
      <button type="button" class="pb-burger" aria-label="Open the menu" aria-expanded="false" aria-controls="pb-mobile-nav"><svg class="pb-i" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </nav>
  </div>
</header>
<div class="pb-mobile-nav" id="pb-mobile-nav" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="pb-mobile-nav__top">
    <a href="%(root)sindex.html" aria-label="Pinky Brain Digital, home"><img src="%(root)simages/logo.png" alt="Pinky Brain Digital" width="138" height="46"></a>
    <button type="button" class="pb-mobile-nav__close" aria-label="Close the menu"><svg class="pb-i" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
  </div>
  <ul>
    <li><a href="%(root)sindex.html">Home</a></li>
    <li><details><summary>Services</summary><div class="pb-mobile-groups">%(mobile_groups)s</div></details></li>
    <li><a href="%(root)slocations.html">Locations</a></li>
    <li><a href="%(root)sabout-us.html">About Us</a></li>
    <li><a href="%(root)sblog.html">Insights</a></li>
  </ul>
  <a class="pb-btn pb-btn--dark" href="%(root)scontact-us.html">%(primary)s</a>
</div>
<main id="main">
""" % {"root": root, "chevron": chevron, "mega": _mega_html(root), "mobile_groups": _mobile_groups_html(root),
       "primary": CTA_PRIMARY, "secondary": CTA_SECONDARY, "arrow": icon("arrow"),
       "c_services": cur("services"), "c_locations": cur("locations"), "c_about": cur("about"), "c_insights": cur("insights")}

def footer_html(root, scripts=""):
    services_links = "".join('<li><a href="%s%s.html">%s</a></li>' % (root, s, SERVICES[s]["nav_label"]) for s in SERVICE_ORDER)
    services_links += '<li><a href="%sservices.html">All services</a></li>' % root
    social = ""
    if SOCIAL_LINKS:
        social = '<ul class="pb-footer__social">%s</ul>' % "".join(
            '<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, n) for n, u in SOCIAL_LINKS.items())
    return """
</main>
<footer class="pb-footer">
  <div class="pb-wrap pb-footer__top">
    <div class="pb-footer__brand">
      <img src="%(root)simages/logo.png" alt="Pinky Brain Digital" width="174" height="58" style="filter:brightness(0) invert(1)">
      <p>One trusted digital team for your website, search, advertising, social media and AI, built around your business and your goals.</p>
      %(social)s
    </div>
    <nav aria-label="Services">
      <p class="pb-footer__h">Services</p>
      <ul>%(services_links)s</ul>
    </nav>
    <nav aria-label="Company">
      <p class="pb-footer__h">Company</p>
      <ul>
        <li><a href="%(root)sabout-us.html">About Us</a></li>
        <li><a href="%(root)sindustries.html">Industries</a></li>
        <li><a href="%(root)slocations.html">Locations</a></li>
        <li><a href="%(root)sblog.html">Insights</a></li>
        <li><a href="%(root)sindex.html#pbs-faq">FAQs</a></li>
        <li><a href="%(root)scontact-us.html">Contact Us</a></li>
      </ul>
    </nav>
    <div>
      <p class="pb-footer__h">Get in touch</p>
      <address>%(address)s<br><a href="mailto:%(email)s">%(email)s</a></address>
    </div>
  </div>
  <div class="pb-wrap pb-footer__bottom">
    <span>&copy; 2026 Pinky Brain Digital. All rights reserved.</span>
    <ul>
      <li><a href="%(root)sprivacy-policy.html">Privacy Policy</a></li>
      <li><a href="%(root)ssitemap.html">Sitemap</a></li>
    </ul>
  </div>
</footer>
<a class="pb-whatsapp" href="https://wa.me/447436236290?text=Hi%%20Pinky%%20Brain%%20Digital%%2C%%20I%%27d%%20like%%20to%%20talk%%20about%%20my%%20business." target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp">
  <svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><path fill="#fff" d="M16.04 3C9.4 3 4 8.38 4 15.01c0 2.12.56 4.19 1.61 6.01L4 29l8.17-1.57a12.03 12.03 0 0 0 3.87.64C22.68 28.07 28 22.69 28 16.06 28 9.4 22.7 3 16.04 3Zm0 22.03c-1.2 0-2.38-.27-3.45-.78l-.5-.24-4.85.93.95-4.72-.27-.52a9.1 9.1 0 0 1-1.35-4.7c0-5.04 4.1-9.14 9.15-9.14 5.04 0 9.14 4.1 9.14 9.14 0 5.05-4.1 9.03-8.82 9.03Zm5.02-6.85c-.28-.14-1.63-.8-1.88-.9-.25-.09-.44-.14-.62.14-.18.27-.71.9-.87 1.08-.16.18-.32.2-.6.07-.27-.14-1.16-.43-2.2-1.36-.81-.72-1.36-1.62-1.52-1.89-.16-.27-.02-.42.12-.56.12-.12.27-.32.4-.48.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.48-.07-.14-.62-1.5-.85-2.05-.22-.54-.45-.46-.62-.47h-.53c-.18 0-.48.07-.73.34-.25.27-.96.94-.96 2.29s.98 2.66 1.12 2.84c.14.18 1.93 2.95 4.68 4.13.65.28 1.16.45 1.56.58.66.21 1.25.18 1.72.11.52-.08 1.63-.67 1.86-1.31.23-.64.23-1.19.16-1.31-.07-.11-.25-.18-.53-.32Z"/></svg>
</a>
<script src="%(root)sassets/js/site.js" defer></script>
%(scripts)s
""" % {"root": root, "services_links": services_links, "social": social, "address": SITE_ADDRESS,
       "email": SITE_EMAIL, "scripts": scripts}

# ---------------------------------------------------------------------------
# COMPONENT RENDERERS
# ---------------------------------------------------------------------------
def render_hero(root, eyebrow, h1, lead, ticks, hero_img, hero_alt, badge=None, secondary=None):
    secondary = secondary or (root + "services.html", CTA_SECONDARY)
    ticks_html = "".join("<li>%s</li>" % t for t in ticks)
    badge_html = ""
    if badge:
        b0, b1, b2 = badge
        badge_html = '<div class="pb-hero__badge"><div><b>%s</b><span>%s</span>%s</div></div>' % (
            b1, b0, ("<div style='margin-top:4px;font-size:.72rem;color:#5B6472'>%s</div>" % b2) if b2 else "")
    return """
<section class="pb-hero">
  <div class="pb-wrap pb-hero__grid">
    <div>
      <p class="pb-eyebrow">%(eyebrow)s</p>
      <h1>%(h1)s</h1>
      <p class="pb-lead">%(lead)s</p>
      <div class="pb-hero__actions">
        <a class="pb-btn pb-btn--dark" href="%(root)scontact-us.html">%(primary)s %(arrow)s</a>
        <a class="pb-btn pb-btn--line" href="%(sec_href)s">%(sec_label)s</a>
      </div>
      <ul class="pb-hero__ticks">%(ticks)s</ul>
    </div>
    <div class="pb-hero__media">
      <img class="pb-hero__img" src="%(root)simages/%(img)s" alt="%(alt)s" width="900" height="792" fetchpriority="high" decoding="async">
      %(badge)s
    </div>
  </div>
</section>
""" % {"eyebrow": eyebrow, "h1": h1, "lead": cap_first(lead), "ticks": ticks_html, "root": root,
       "img": hero_img, "alt": hero_alt, "badge": badge_html, "primary": CTA_PRIMARY, "arrow": icon("arrow"),
       "sec_href": secondary[0], "sec_label": secondary[1]}

def render_cards(cards, icons_cycle):
    out = []
    for i, (title, text) in enumerate(cards):
        ic = icons_cycle[i % len(icons_cycle)]
        out.append('<div class="pb-card"><span class="pb-card__ic">%s</span><h3>%s</h3><p>%s</p></div>' % (icon(ic), title, text))
    return "".join(out)

def render_section(eyebrow, title, intro, cards, icons_cycle, tint=False, numbered=False):
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

def render_outcomes(key, tint=False, city=None):
    intro, items = OUTCOMES[key]
    title = "The results we work towards" if not city else "What %s businesses can expect" % city
    return render_section("Results that matter", title, intro + " " + CASE_BY_CASE, items, OUTCOME_ICONS, tint=tint)

def render_split(root, img, alt, title, intro, reasons, tint=False, eyebrow="Why it matters"):
    items = "".join("<li>%s</li>" % r for r in reasons)
    return """
<section class="pb-section%(tint)s">
  <div class="pb-wrap pb-split">
    <img class="pb-split__img" src="%(root)simages/%(img)s" alt="%(alt)s" width="760" height="644" loading="lazy" decoding="async">
    <div>
      <p class="pb-eyebrow">%(eyebrow)s</p>
      <h2>%(title)s</h2>
      <p>%(intro)s</p>
      <ul class="pb-mini-list">%(items)s</ul>
    </div>
  </div>
</section>
""" % {"root": root, "img": img, "alt": alt, "title": title, "intro": intro, "items": items,
       "tint": " pb-section--tint" if tint else "", "eyebrow": eyebrow}

def render_faq(faq_items, tint=True, faq_id="pb-faq"):
    items = []
    for i, (q, a) in enumerate(faq_items):
        items.append('<details%s><summary><h3>%s</h3></summary><p>%s</p></details>' % (" open" if i == 0 else "", q, a))
    return """
<section id="%(id)s" class="pb-section%(tint)s pb-faq">
  <div class="pb-wrap">
    <div class="pb-section__head">
      <div><p class="pb-eyebrow">FAQs</p><h2>Frequently asked questions</h2></div>
      <p>Straight answers to the questions businesses ask us most.</p>
    </div>
    <div class="pb-faq__list">%(items)s</div>
  </div>
</section>
""" % {"id": faq_id, "items": "".join(items), "tint": " pb-section--tint" if tint else ""}

def faq_jsonld(faq_items):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": html.unescape(q),
             "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}}
            for q, a in faq_items
        ],
    }
    return '<script type="application/ld+json">\n%s\n</script>\n' % json.dumps(data, ensure_ascii=False, indent=1)

def offer_by_key(key):
    for o in FREE_OFFERS:
        if o[0] == key:
            return o
    return None

def render_cta(intro, root="", offer_key=None):
    offer_html = ""
    o = offer_by_key(offer_key) if offer_key else None
    if o:
        offer_html = '<p class="pb-cta__offer">Prefer to start small? Ask about our <a href="%scontact-us.html?interest=%s">%s</a>.</p>' % (root, o[0], o[1])
    return """
<section class="pb-section">
  <div class="pb-wrap">
    <div class="pb-cta">
      <div class="pb-cta__solo">
        <h2>Tell us what you want to achieve.</h2>
        <p>%(intro)s</p>
        <div class="pb-cta__actions">
          <a class="pb-btn pb-btn--pink" href="%(root)scontact-us.html">%(primary)s %(arrow)s</a>
          <a class="pb-btn pb-btn--ghost" href="%(root)sservices.html">%(secondary)s</a>
        </div>
        %(offer)s
        <p class="pb-cta__small">Prefer email? <a href="mailto:%(email)s">%(email)s</a></p>
      </div>
    </div>
  </div>
</section>
""" % {"intro": cap_first(intro), "email": SITE_EMAIL, "arrow": icon("arrow"), "root": root,
       "primary": CTA_PRIMARY, "secondary": CTA_SECONDARY, "offer": offer_html}

def render_free_offers(root="", eyebrow="Start with something free", title="Not sure where to start? Ask for a free review.",
                       intro="Pick the one that fits and we’ll tell you honestly what we find, with no pressure to buy anything.", tint=True):
    cards = "".join(
        '<a class="pb-offer" href="%scontact-us.html?interest=%s"><span class="pb-card__ic">%s</span><h3>%s</h3><p>%s</p>'
        '<span class="pb-link"><span>Ask about this</span> %s</span></a>' % (root, k, icon(ic), t, d, icon("arrow"))
        for k, t, ic, d in FREE_OFFERS)
    return """
<section class="pb-section%(tint)s" id="free-reviews">
  <div class="pb-wrap">
    <div class="pb-section__head">
      <div><p class="pb-eyebrow">%(eyebrow)s</p><h2>%(title)s</h2></div>
      <p>%(intro)s</p>
    </div>
    <div class="pb-offers">%(cards)s</div>
  </div>
</section>
""" % {"tint": " pb-section--tint" if tint else "", "eyebrow": eyebrow, "title": title, "intro": intro, "cards": cards}

def render_breadcrumb(trail):
    parts = []
    for i, (label, href) in enumerate(trail):
        if href:
            parts.append('<a href="%s">%s</a>' % (href, label))
        else:
            parts.append('<span aria-current="page">%s</span>' % label)
    return ('<nav class="pb-wrap pb-crumb" aria-label="Breadcrumb">'
            + '<span class="pb-crumb__sep" aria-hidden="true">/</span>'.join(parts) + '</nav>')

def render_jsonld(data):
    return '<script type="application/ld+json">\n%s\n</script>\n' % json.dumps(data, ensure_ascii=False, indent=1)

ORG_JSONLD = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Pinky Brain Digital",
    "url": SITE_URL + "/",
    "logo": SITE_URL + "/images/logo.png",
    "email": SITE_EMAIL,
    "address": {"@type": "PostalAddress", "streetAddress": "International House, 109–111 Fulham Palace Road",
                "addressLocality": "London", "postalCode": "W6 8JA", "addressCountry": "GB"},
}

# ---------------------------------------------------------------------------
# BUILD: SERVICE PAGES
# ---------------------------------------------------------------------------
def build_service_page(key):
    s = SERVICES[key]
    root = ""
    alt = Alt(False)
    fname = s["slug"] + ".html"
    out = [
        head_html(root, "%s | Pinky Brain Digital" % s["name"], s["meta"], fname),
        header_html(root, current="services"),
        render_breadcrumb([("Home", "index.html"), ("Services", "services.html"), (s["nav_label"], None)]),
        render_hero(root, s["eyebrow"], s["h1"], s["lead"], s["ticks"], s["hero_img"], s["hero_alt"], s["badge"]),
        render_section("Why choose us", "Why businesses choose us for %s" % s["name"], WHY_INTRO, s["why_cards"], WHY_ICONS, tint=alt.next()),
        render_outcomes(key, tint=alt.next()),
        render_section("What we do", s["core_title"], s["core_intro"], s["core_cards"], CORE_ICONS, tint=alt.next()),
        render_section("How we help" if s["g3_numbered"] else "Our approach", s["g3_title"], s["g3_intro"], s["g3_cards"],
                       STEP_ICONS, tint=alt.next(), numbered=s["g3_numbered"]),
    ]
    if key in PROCESS_CONTENT:
        pt, _sub, pintro, psteps = get_process_content(key)
        out.append(render_section("How we work", pt, pintro, psteps, STEP_ICONS, tint=alt.next(), numbered=True))
    out.append(render_split(root, s["split_img"], s["split_alt"], s["g4_title"], s["g4_intro"],
                            [c[0] + ": " + c[1] for c in s["g4_cards"]], tint=alt.next()))
    out.append(render_faq(s["faq"], tint=alt.next()))
    out.append(render_cta(s["cta_intro"], root=root, offer_key=SERVICE_OFFER.get(key)))
    out.append(footer_html(root))
    out.append(faq_jsonld(s["faq"]))
    out.append("</body></html>")
    return write_page(fname, "".join(out))

# ---------------------------------------------------------------------------
# BUILD: LOCATION PAGES
# ---------------------------------------------------------------------------
def read_locations():
    path = os.path.join(ROOT, "Pinky Brain Digital - Location.csv")
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            url = (row.get("URL") or "").strip()
            city = (row.get("City") or "").strip()
            service = (row.get("Service") or "").strip()
            if not url or not city or service not in LOCATION_SERVICE_KEY:
                continue
            rows.append({
                "no": row.get("No", "").strip(),
                "region": (row.get("Region") or "").strip(),
                "city": city,
                "service": service,
                "service_key": LOCATION_SERVICE_KEY[service],
                "title": (row.get("Page title") or "").strip(),
                "url": url,
                "folder": url.strip("/"),
            })
    return rows

WEB_LEADS = [
    "Fast, modern websites for {city} businesses, built around your customers and designed to turn visitors into enquiries.",
    "A professional website that earns trust, works beautifully on mobile and gives {city} customers a clear reason to get in touch.",
    "Websites for {city} businesses that look credible, load quickly and convert more of the people who visit.",
]
SEO_LEADS = [
    "Get found by the right customers in {city}, with better rankings, more visibility and more enquiries.",
    "Search visibility for {city} businesses: more of the right visitors, more enquiries and steady, measurable growth.",
    "Rank higher, be seen more often and turn local searches in {city} into real customers.",
]
WEB_H2 = [
    "Website design for {city} businesses",
    "A website that works as hard as your {city} business",
    "Websites built for the way {city} customers search",
]
SEO_H2 = [
    "SEO that gets {city} businesses found",
    "Be the business {city} customers find first",
    "Search visibility built around {city}",
]

SECTOR_INTROS = [
    "Every project starts with your goals rather than a template. These are some of the sectors we most often support in {city}.",
    "We don’t work from a fixed package. Here are a few of the {city} sectors where we regularly help businesses {goal}.",
    "From {s1} to {s2}, {city} businesses have different customers and different priorities, so we shape the work around each one.",
]
PROCESS_INTROS = {
    "website-design": [
        "Every website follows the same clear process, so you always know what happens next and when.",
        "However big or small the project, you will always know what is happening, what comes next and who to ask.",
        "A simple, staged process keeps your {city} project on time, on budget and free of surprises.",
    ],
    "seo-services": [
        "Good SEO is a long-term asset, so we follow a clear process that builds search performance month after month.",
        "SEO works best when it is steady and measured, so every client gets the same clear, staged process.",
        "We keep SEO simple and transparent, with clear steps and a clear update after each one.",
    ],
}

def build_location_page(loc, idx):
    key = loc["service_key"]
    s = SERVICES[key]
    root = ""
    city, region = loc["city"], loc["region"]
    prof = CITY_PROFILES[city]
    web = key == "website-design"
    areas = prof["areas"]
    sectors = prof["sectors"]
    v = idx % 3
    alt = Alt(False)

    lead = (WEB_LEADS if web else SEO_LEADS)[v].format(city=city)
    h2 = (WEB_H2 if web else SEO_H2)[v].format(city=city)
    local_note = prof["web" if web else "seo"]
    ticks = (["Mobile-first design", "Built around your customers", "Serving %s and nearby" % city] if web else
             ["Better rankings and visibility", "Local and technical SEO", "Serving %s and nearby" % city])

    sector_cards = []
    for i, sec in enumerate(sectors):
        note = SECTOR_NOTES[sec][0 if web else 1]
        verb = "We build " if web else "We focus on "
        sector_cards.append((sec, verb + note))

    london_regions = ("Central, North, South, East, West and South West London, as well as Surrey and Hertfordshire (within 25 miles) "
                      "and the Kent and Essex borders")
    local_faq = [
        ("Do you only work with businesses in Central London?", "No. We work with businesses across %s. We usually work remotely by video call and email, and can arrange to meet where it makes sense." % london_regions)
        if city == "London" else
        ("Do you only work with businesses in central %s?" % city,
         "No. We work with businesses across %s and the surrounding area, including %s. We usually work remotely by video call and email, and can arrange to meet where it makes sense." % (city, join_list(areas[:4]))),
        ("What kinds of businesses do you work with in %s?" % city,
         "A broad mix. In %s that often includes %s businesses, but every project starts with your goals rather than a template." % (city, join_list([lc_first(x) for x in sectors[:3]]))),
    ]
    if web and city == "Berlin":
        local_faq.append(("Can you help with German legal requirements such as the Impressum?",
                          "We build the pages and structure a German website needs, including an Impressum, privacy policy and cookie consent. You should always have the final wording checked by a legal adviser."))
    elif not web:
        local_faq.append(("How do you help a %s business show up in local searches?" % city,
                          "We optimise your Google Business Profile, build pages around the services and areas you cover, and strengthen your reviews and listings. That helps you appear for searches that combine your service with %s or a neighbourhood such as %s or %s." % (city, areas[0], areas[1])))
    shared = s["faq"]
    faq = local_faq + [shared[idx % len(shared)]]

    meta = None
    for n_sectors in (2, 1):
        meta_sectors = join_list([lc_first(x) for x in sectors[:n_sectors]])
        if web:
            meta = "Website design in %s: fast, mobile-first websites for %s and other local businesses, built to win enquiries." % (city, meta_sectors)
        else:
            meta = "SEO services in %s: better rankings, more visibility and more enquiries for %s and other local businesses." % (city, meta_sectors)
        if len(meta) <= 158:
            break

    pt, _sub, _pintro, psteps = get_process_content(key)
    pintro = PROCESS_INTROS[key][v].format(city=city)
    process_title = pt if city in pt else "%s in %s" % (pt, city)
    sector_intro = SECTOR_INTROS[v].format(
        city=city, goal="get more from their website" if web else "be found online",
        s1=lc_first(sectors[0]), s2=lc_first(sectors[1]))

    out = [
        head_html(root, "%s | Pinky Brain Digital" % loc["title"], meta, loc["folder"] + ".html"),
        header_html(root, current="locations"),
        render_breadcrumb([("Home", "index.html"), ("Locations", "locations.html"), (loc["title"], None)]),
        render_hero(root, "%s &middot; %s" % (region, city), loc["title"], lead, ticks, s["hero_img"], s["hero_alt"]),
        """
<section class="pb-section%(tint)s">
  <div class="pb-wrap">
    <div class="pb-section__head">
      <div><p class="pb-eyebrow">%(city)s</p><h2>%(h2)s</h2></div>
      <div><p>%(intro)s</p><p>%(note)s</p><p>%(more)s</p></div>
    </div>
  </div>
</section>
""" % {"tint": " pb-section--tint" if alt.next() else "", "city": city, "h2": h2, "intro": prof["intro"], "note": local_note, "more": prof["more"]},
        render_section("Who we help in %s" % city, "Businesses we work with in %s" % city,
                       sector_intro, sector_cards, CORE_ICONS, tint=alt.next()),
        render_section("Our process", process_title, pintro, psteps, STEP_ICONS, tint=alt.next(), numbered=True),
        render_faq(faq, tint=alt.next()),
        render_cta("Tell us about your %s business and what you want to achieve, and we’ll reply within one business day with honest, practical next steps." % city,
                   root=root, offer_key=SERVICE_OFFER.get(key)),
        footer_html(root),
        faq_jsonld(faq),
        "</body></html>",
    ]
    return write_page(loc["folder"] + ".html", "".join(out))

# ---------------------------------------------------------------------------
# BUILD: HOMEPAGE (wrap the hand-written fragment)
# ---------------------------------------------------------------------------
IMG_REMAP = {
    "2149273705.webp": "homepage-hero-digital-agency-team.webp",
    "10539.webp": "about-pinky-brain-digital-team.webp",
    "2149241210.jpg": "luxury-real-estate-interior.webp",
    "favii.png": "pinky-brain-digital-badge-icon.png",
    "photo-1600585154526-990dced4db0d.webp": "luxury-property-marketing.webp",
    "Modern-dental-clinic-treatment-room.avif": "dental-clinic-marketing.avif",
    "plumber.avif": "plumbers-electricians-marketing.avif",
    "cafe.avif": "restaurant-cafe-marketing.avif",
    "shop.avif": "retail-shop-marketing.avif",
    "online.avif": "ecommerce-online-business-marketing.avif",
    "service.avif": "professional-services-marketing.avif",
}

INDUSTRY_ANCHORS = {
    "/industries/real-estate-marketing/": "real-estate",
    "/industries/property-developers/": "property-developers",
    "/industries/luxury-brands/": "luxury-brands",
    "/industries/dental-marketing/": "dental-clinics",
    "/industries/trades-marketing/": "trades",
    "/industries/restaurant-marketing/": "restaurants",
    "/industries/retail-marketing/": "retail",
    "/industries/ecommerce-marketing/": "online-businesses",
    "/industries/professional-services-marketing/": "professional-services",
}

def _fix_text_nodes(frag):
    """Typographic apostrophes in visible text only (never inside tags, <style> or <script>)."""
    parts = re.split(r"(<style\b.*?</style>|<script\b.*?</script>|<[^>]+>)", frag, flags=re.S | re.I)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", "&rsquo;", parts[i])
    return "".join(parts)

def build_homepage():
    frag_source = os.path.join(ROOT, "_ref", "index.homepage-fragment.html")
    with open(frag_source, encoding="utf-8") as f:
        frag = f.read()
    for old, new in IMG_REMAP.items():
        frag = frag.replace("https://pinkybraindigital.com/wp-content/uploads/2026/09/%s" % old, "images/%s" % new)

    link_fix = {"/services/%s/" % sl: "%s.html" % sl for sl in ALL_SERVICE_SLUGS}
    link_fix.update({
        "/services/ecommerce/": "e-commerce-websites-design.html",
        "/services/seo/": "seo-services.html",
        "/services/aeo/": "aeo-ai-search.html",
        "/services/ppc-management/": "ppc-digital-advertising.html",
        "/services/social-media-marketing/": "social-media.html",
        "/services/": "services.html",
        "/industries/": "industries.html",
        "/about/": "about-us.html",
        "/case-studies/": "industries.html",
        "/contact/": "contact-us.html",
    })
    for old, anchor in INDUSTRY_ANCHORS.items():
        link_fix[old] = "industries.html#%s" % anchor
    for old, new in link_fix.items():
        frag = frag.replace('href="%s"' % old, 'href="%s"' % new)

    # new sections, placed after the testimonials: free reviews, then insights, then the FAQ
    faq_marker = "<!--\n  SECTION 13"
    assert faq_marker in frag, "faq marker missing"
    frag = frag.replace(faq_marker, render_free_offers("") + render_blog_teaser() + faq_marker, 1)


    frag = re.sub(r"<!--.*?-->", "", frag, flags=re.S)
    frag = _fix_text_nodes(frag)

    title = "Pinky Brain Digital | Your Digital Partner, Built for Growth"
    desc = ("Full-service digital agency for websites, SEO, advertising, social media and AI. "
            "One trusted team for businesses in the UK, Europe, USA and Canada.")
    out = [head_html("", title, desc, "index.html"), header_html("", current="home"), frag,
           footer_html(""), render_jsonld(ORG_JSONLD), "</body></html>"]
    return write_page("index.html", "".join(out))

# ---------------------------------------------------------------------------
# BUILD: SERVICES HUB
# ---------------------------------------------------------------------------
GROUP_INTROS = {
    "Search & Advertising": "Be found by the right people on Google, in Maps and in AI answers, and pay to reach them when it makes sense.",
    "Websites & Apps": "Websites, shops and software that look credible, work smoothly and turn visitors into customers.",
    "Marketing": "Social, content, email and lead generation that build visibility, engagement and a steady flow of enquiries.",
    "Branding & Creative": "Identity, design, photography and writing that make your business look and sound established.",
    "Automation & Security": "Smart tools, tidy systems and solid protection that save time and keep your business safe.",
    "Digital Consulting": "Not sure where to start? Honest, expert advice on where your money is best spent.",
}
GROUP_ICONS = {"Search & Advertising": "search", "Websites & Apps": "doc", "Marketing": "growth",
               "Branding & Creative": "target", "Automation & Security": "shield", "Digital Consulting": "users"}

def build_services_page():
    root = ""
    alt = Alt(False)
    sections = []
    for gname, slugs in SERVICE_GROUPS:
        cards = "".join(
            '<a class="pb-card pb-card--link" href="%s.html"><span class="pb-card__ic">%s</span><h3>%s</h3><p>%s</p>'
            '<span class="pb-link">Find out more %s</span></a>'
            % (sl, icon(GROUP_ICONS[gname]), SERVICES[sl]["nav_label"], SERVICE_BLURB[sl], icon("arrow"))
            for sl in slugs)
        sections.append("""
<section class="pb-section%s">
  <div class="pb-wrap">
    <div class="pb-section__head">
      <div><p class="pb-eyebrow">%s</p><h2>%s</h2></div>
      <p>%s</p>
    </div>
    <div class="pb-grid-4">%s</div>
  </div>
</section>""" % (" pb-section--tint" if alt.next() else "", gname, gname, GROUP_INTROS[gname], cards))
    out = [
        head_html(root, "Our Services | Pinky Brain Digital",
                  "SEO, websites, advertising, social media, branding, AI automation and more. Every service explained in full, with the results it should deliver.",
                  "services.html"),
        header_html(root, current="services"),
        render_breadcrumb([("Home", "index.html"), ("Services", None)]),
        """
<section class="pb-hero" style="padding-bottom:clamp(40px,5vw,64px)">
  <div class="pb-wrap pb-narrow">
    <p class="pb-eyebrow">Our services</p>
    <h1>Everything your business needs digitally, from one trusted team.</h1>
    <p class="pb-lead">%s</p>
  </div>
</section>""" % CASE_BY_CASE,
        "".join(sections),
        render_free_offers(root, tint=alt.next()),
        render_cta("Tell us what you want to achieve, and we’ll recommend the right place to start.", root=root),
        footer_html(root),
        "</body></html>",
    ]
    return write_page("services.html", "".join(out))

# ---------------------------------------------------------------------------
# BUILD: INDUSTRIES HUB
# ---------------------------------------------------------------------------
def build_industries_page():
    root = ""
    blocks = []
    for anchor, name, lead, body, slugs in INDUSTRIES:
        links = "".join('<li><a class="pb-link" href="%s.html">%s %s</a></li>' % (sl, SERVICES[sl]["nav_label"], icon("arrow")) for sl in slugs)
        blocks.append("""
<div class="pb-industry" id="%s">
  <div><h2>%s</h2><p class="pb-industry__lead">%s</p><p>%s</p></div>
  <div><h3>Services we often recommend</h3><ul class="pb-chips" style="flex-direction:column;align-items:flex-start;gap:12px">%s</ul></div>
</div>""" % (anchor, name, lead, body, links))
    out = [
        head_html(root, "Industries We Serve | Pinky Brain Digital",
                  "Digital marketing for estate agents, developers, luxury brands, clinics, trades, restaurants, retailers, online businesses and professional services.",
                  "industries.html"),
        header_html(root),
        render_breadcrumb([("Home", "index.html"), ("Industries", None)]),
        """
<section class="pb-hero" style="padding-bottom:clamp(40px,5vw,64px)">
  <div class="pb-wrap pb-narrow">
    <p class="pb-eyebrow">Industries we serve</p>
    <h1>Specialists in luxury real estate. Trusted by local businesses.</h1>
    <p class="pb-lead">We understand the difference between selling a £5 million penthouse and filling a dentist’s diary. Every sector needs a different approach, so we start with your business and your goals.</p>
  </div>
</section>
<section class="pb-section"><div class="pb-wrap">%s</div></section>""" % "".join(blocks),
        render_cta("Tell us about your sector and what you want to achieve, and we’ll reply within one business day.", root=root),
        footer_html(root),
        "</body></html>",
    ]
    return write_page("industries.html", "".join(out))

# ---------------------------------------------------------------------------
# BUILD: CONTACT US PAGE
# ---------------------------------------------------------------------------
def build_contact_page():
    root = ""
    offer_opts = "".join('<option value="%s">%s</option>' % (k, t) for k, t, _i, _d in FREE_OFFERS)
    service_opts = "".join('<option value="%s">%s</option>' % (sl, SERVICES[sl]["name"]) for sl in ALL_SERVICE_SLUGS)
    out = [
        head_html(root, "Contact Us | Pinky Brain Digital",
                  "Tell us what you want to achieve. Send a message or ask for a free review, and we’ll reply within one business day.",
                  "contact-us.html"),
        header_html(root),
        render_breadcrumb([("Home", "index.html"), ("Contact", None)]),
        """
<section class="pb-hero">
  <div class="pb-wrap pb-hero__grid">
    <div>
      <p class="pb-eyebrow">Get in touch</p>
      <h1>Let&rsquo;s talk about your business.</h1>
      <p class="pb-lead">Tell us what you want to achieve and we&rsquo;ll reply within one business day with real next steps, not a scripted sales call.</p>
      <ul class="pb-hero__ticks">
        <li>Real replies, no chatbots</li>
        <li>Free 20-minute consultation</li>
        <li>No obligation</li>
      </ul>
    </div>
    <div class="pb-card" style="padding:32px">
      <h2 style="margin-bottom:16px;font-size:1.25rem">Head office</h2>
      <address style="font-style:normal;font-size:.98rem;color:var(--pb-body)">%(address)s</address>
      <p style="margin-top:20px"><a class="pb-link" href="mailto:%(email)s">%(email)s</a></p>
    </div>
  </div>
</section>
<section class="pb-section">
  <div class="pb-wrap pb-narrow">
    <div class="pb-section__head" style="display:block">
      <p class="pb-eyebrow">Send a message</p>
      <h2>Tell us about your project</h2>
    </div>
    <form class="pb-form" id="pb-contact-form" data-endpoint="%(endpoint)s" data-email="%(email)s">
      <div>
        <label for="pb-name">Your name*</label>
        <input id="pb-name" name="name" type="text" autocomplete="name" required>
      </div>
      <div>
        <label for="pb-email">Email address*</label>
        <input id="pb-email" name="email" type="email" autocomplete="email" required>
      </div>
      <div>
        <label for="pb-phone">Phone number</label>
        <input id="pb-phone" name="phone" type="tel" autocomplete="tel">
      </div>
      <div>
        <label for="pb-interest">What would you like help with?</label>
        <select id="pb-interest" name="interest">
          <option value="">Not sure yet</option>
          <optgroup label="Free reviews and audits">%(offers)s</optgroup>
          <optgroup label="Services">%(services)s</optgroup>
        </select>
      </div>
      <div class="pb-field--full">
        <label for="pb-message">Your message*</label>
        <textarea id="pb-message" name="message" required></textarea>
      </div>
      <div class="pb-form__hp" aria-hidden="true"><label for="pb-website">Leave this field empty</label><input id="pb-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
      <p class="pb-form__note">By sending this message you agree to us using your details to reply, as described in our <a class="pb-link" href="privacy-policy.html">Privacy Policy</a>.</p>
      <div class="pb-form__actions">
        <button type="submit" class="pb-btn pb-btn--dark">Send message %(arrow)s</button>
        <span class="pb-form__note" style="margin:0">We reply within one business day.</span>
      </div>
      <p class="pb-form__status" id="pb-form-status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
""" % {"address": SITE_ADDRESS, "email": SITE_EMAIL, "endpoint": FORM_ENDPOINT, "offers": offer_opts,
       "services": service_opts, "arrow": icon("arrow")},
        footer_html(root, scripts='<script src="assets/js/contact.js" defer></script>'),
        render_jsonld(ORG_JSONLD),
        "</body></html>",
    ]
    return write_page("contact-us.html", "".join(out))

# ---------------------------------------------------------------------------
# BUILD: ABOUT US PAGE
# ---------------------------------------------------------------------------
APPROACH_SECTIONS = [
    ("Your needs come before our services",
     "We don&rsquo;t start with what we can sell you. We start with what you&rsquo;re trying to achieve. We look at what&rsquo;s important now, what can wait, what you can already manage and where you genuinely need help.",
     "Sometimes that means working alongside your existing team. Sometimes we&rsquo;ll bring in expertise from our wider network. And sometimes we&rsquo;ll tell you that you don&rsquo;t need to spend money on something yet. If we&rsquo;re not the right people for something, we&rsquo;ll be honest about that too. We&rsquo;d rather give you the right advice than sell you the wrong service.",
     "users", "website-design-development-process.webp", "Team reviewing a client's project requirements together"),
    ("Built around your business",
     "Every business is different. We stay flexible and adapt our approach around what you actually need, rather than trying to fit you into a standard package.",
     "As your business grows and changes, we want to grow and adapt with you.",
     "target", "ppc-digital-advertising-detail.webp", "A plan being built and tailored around one specific business"),
    ("Keeping you ahead",
     "Digital never stands still, and neither do we. We keep up with new technologies, platforms, tools and changes in the digital world so you don&rsquo;t have to.",
     "It&rsquo;s not about following every trend. It&rsquo;s about understanding what&rsquo;s changing, what matters to your business, and helping you take advantage of the right opportunities at the right time.",
     "growth", "aeo-ai-search-hero.webp", "AI search interface representing new digital technology"),
    ("Transparency from the start",
     "You should know what we&rsquo;re doing, why we&rsquo;re doing it, what it costs and how things are progressing.",
     "We&rsquo;ll keep you updated, be open about what&rsquo;s working, and equally open when something needs to change.",
     "doc", "google-ads-detail.webp", "Performance data and reporting being reviewed openly"),
    ("Here for the long term",
     "We don&rsquo;t expect trust because we have a website or make promises. We have to earn it through our work, communication, transparency and the way we treat people.",
     "We&rsquo;re not looking for a quick transaction. We want to become the digital team you trust and still want to call years from now.",
     "shield", "ecommerce-store-design-detail.webp", "Ongoing work being reviewed together over time"),
]
APPROACH_VALUES = ["Good work", "Fair advice", "Clear communication", "Always evolving", "Long-term relationships"]


def build_about_page():
    root = ""
    title = "About Us | Pinky Brain Digital"
    desc = "Digital is complicated. Trust shouldn’t be. Meet Pinky Brain Digital and the honest, flexible, long-term approach behind every project."
    alt = Alt(False)

    rows_html = "".join("""
<section class="pb-approach-row%(tint)s" id="approach-%(idx)s">
  <div class="pb-wrap pb-split%(rev)s">
    <img class="pb-split__img" src="images/%(img)s" alt="%(alt)s" width="760" height="644" loading="lazy" decoding="async">
    <div>
      <p class="pb-approach-row__num">%(num)s of %(count)s</p>
      <h2>%(title)s</h2>
      <p style="margin-top:16px">%(p1)s</p>
      <p style="margin-top:16px">%(p2)s</p>
    </div>
  </div>
</section>""" % {
        "tint": " pb-section--tint" if i % 2 else "",
        "rev": " pb-split--rev" if i % 2 else "",
        "idx": i + 1, "img": img, "alt": ialt,
        "num": "%02d" % (i + 1), "count": "%02d" % len(APPROACH_SECTIONS),
        "title": t, "p1": p1, "p2": p2,
    } for i, (t, p1, p2, ic, img, ialt) in enumerate(APPROACH_SECTIONS))

    values_html = "".join("<li>%s %s</li>" % (icon("check"), v) for v in APPROACH_VALUES)

    heritage_html = render_section(
        "Our heritage", "14 years of experience in digital.",
        "Pinky Brain Digital is built on more than 14 years of hands-on experience in the industry. We have worked through every major shift in search, advertising and web design, and we bring that depth to every project.",
        [("14+ years in the industry", "Over a decade of practical experience across websites, SEO, advertising and social media."),
         ("Experience that adapts", "From early search engines to AI-driven discovery, we have kept pace with every change and know what lasts."),
         ("Proven across sectors", "From luxury property to local trades, we understand what different businesses need to grow."),
         ("A partner for the long term", "Experience means we give honest advice, set realistic expectations and stay with you as you grow.")],
        ['growth', 'users', 'check', 'chart'], tint=True)

    out = [
        head_html(root, title, desc, "about-us.html"),
        header_html(root, current="about"),
        render_breadcrumb([("Home", "index.html"), ("About Us", None)]),
        """
<section class="pb-hero">
  <div class="pb-wrap pb-hero__grid">
    <div>
      <p class="pb-eyebrow">Our approach</p>
      <h1>Digital is complicated. Trust shouldn&rsquo;t be.</h1>
      <p class="pb-lead">Just as you have a trusted accountant, mechanic or doctor, we believe every business needs a reliable digital partner: someone who understands the landscape, explains things clearly and has your best interests at heart. That&rsquo;s what we want Pinky Brain Digital to be.</p>
      <div class="pb-hero__actions">
        <a class="pb-btn pb-btn--dark" href="contact-us.html">%(primary)s %(arrow)s</a>
        <a class="pb-btn pb-btn--line" href="services.html">%(secondary)s</a>
      </div>
      <ul class="pb-hero__ticks">
        <li>Honest, expert advice</li>
        <li>Flexible, not one-size-fits-all</li>
        <li>A long-term digital partner</li>
      </ul>
    </div>
    <div class="pb-hero__media">
      <img class="pb-hero__img" src="images/about-pinky-brain-digital-team.webp" alt="The Pinky Brain Digital team working together on a client project" width="900" height="792" fetchpriority="high" decoding="async">
      <div class="pb-hero__badge"><div><b>Trust, always</b><span>Our promise</span></div></div>
    </div>
  </div>
</section>
<section class="pb-quote-band">
  <div class="pb-wrap">
    <span class="pb-mark" aria-hidden="true">&ldquo;</span>
    <p>Good work. Fair advice. Clear communication. Always evolving. Long-term relationships.</p>
    <span>That&rsquo;s the Pinky Brain approach</span>
  </div>
</section>
%(heritage)s
%(rows)s
<section class="pb-section">
  <div class="pb-wrap">
    <div class="pb-section__head" style="display:block">
      <p class="pb-eyebrow">What we stand for</p>
      <h2>The Pinky Brain approach, in five phrases</h2>
    </div>
    <ul class="pb-values-row">%(values)s</ul>
  </div>
</section>
""" % {"rows": rows_html, "values": values_html, "heritage": heritage_html, "primary": CTA_PRIMARY, "secondary": CTA_SECONDARY, "arrow": icon("arrow")},
        render_cta("Tell us about your business and what you want to achieve, and we’ll reply within one business day with honest, straight-talking advice, not a sales pitch.", root=root),
        footer_html(root),
        render_jsonld(ORG_JSONLD),
        "</body></html>",
    ]
    return write_page("about-us.html", "".join(out))

# ---------------------------------------------------------------------------
# BUILD: LOCATIONS PAGE
# ---------------------------------------------------------------------------
LOCATIONS_REGIONS = [
    ("UK", "United Kingdom", "Our home market, with local pages for the major cities across England."),
    ("Europe", "Europe", "Websites and search visibility for the European market, with local and legal requirements in mind."),
    ("USA", "United States", "Local expertise across the US’s biggest business hubs, from the East Coast to the West."),
    ("Canada", "Canada", "Support for businesses across Canada’s largest cities."),
]

def build_locations_page(locations):
    root = ""
    by_region = {}
    for l in locations:
        by_region.setdefault(l["region"], {}).setdefault(l["city"], []).append(l)
    alt = Alt(False)
    blocks = []
    for region, label, blurb in LOCATIONS_REGIONS:
        cities = by_region.get(region)
        if not cities:
            continue
        cards = []
        for city in sorted(cities):
            links = "".join('<li><a class="pb-link" href="%s.html">%s %s</a></li>' % (e["folder"], SERVICES[e["service_key"]]["nav_label"], icon("arrow")) for e in cities[city])
            cards.append('<div class="pb-card"><h3>%s</h3><ul style="margin-top:14px;display:flex;flex-direction:column;align-items:flex-start;gap:10px">%s</ul></div>' % (city, links))
        blocks.append("""
<section class="pb-section%s">
  <div class="pb-wrap">
    <div class="pb-section__head">
      <div><p class="pb-eyebrow">%d %s</p><h2>%s</h2></div>
      <p>%s</p>
    </div>
    <div class="pb-grid-4">%s</div>
  </div>
</section>""" % (" pb-section--tint" if alt.next() else "", len(cities), "city" if len(cities) == 1 else "cities", label, blurb, "".join(cards)))
    out = [
        head_html(root, "Locations We Cover | Pinky Brain Digital",
                  "Website design and SEO for businesses across the UK, Europe, the United States and Canada, plus international clients. Find your city.",
                  "locations.html"),
        header_html(root, current="locations"),
        render_breadcrumb([("Home", "index.html"), ("Locations", None)]),
        """
<section class="pb-hero" style="padding-bottom:clamp(40px,5vw,64px)">
  <div class="pb-wrap pb-narrow">
    <p class="pb-eyebrow">Where we work</p>
    <h1>Locations we cover</h1>
    <p class="pb-lead">We work with businesses across the UK, Europe, the United States and Canada, and with international clients remotely. Choose your city to see how we help businesses like yours locally.</p>
  </div>
</section>""",
        "".join(blocks),
        """
<section class="pb-section%s">
  <div class="pb-wrap">
    <div class="pb-section__head">
      <div><p class="pb-eyebrow">International</p><h2>Based somewhere else?</h2></div>
      <p>Most of our work is done remotely, so location is rarely a barrier. If you operate in another country or sell internationally, tell us where your customers are and we&rsquo;ll plan around them.</p>
    </div>
    <a class="pb-btn pb-btn--dark" href="contact-us.html">%s %s</a>
  </div>
</section>""" % (" pb-section--tint" if alt.next() else "", CTA_PRIMARY, icon("arrow")),
        footer_html(root),
        "</body></html>",
    ]
    return write_page("locations.html", "".join(out))

# ---------------------------------------------------------------------------
# BLOG (shown to visitors as "Insights")
# Post bodies are lists of (kind, content) blocks: "p", "h2", "ul", "callout".
# ---------------------------------------------------------------------------
BLOG_POSTS = [
    {
        "slug": "do-you-need-a-new-website",
        "title_tag": "Do You Need a New Website? 7 Questions",
        "meta": "A rebuild is a big investment and not always the answer. Seven honest questions to help you decide whether you need a new website or a few targeted fixes.",
        "title": "Do You Really Need a New Website? 7 Honest Questions to Ask First",
        "date": "2026-09-29",
        "category": "Website Design",
        "read": "5 min read",
        "image": "website-design-service-hero.webp",
        "image_alt": "Business owner reviewing their current website on a laptop",
        "excerpt": "A rebuild is a big investment, and it isn&rsquo;t always the answer. These seven questions help you work out whether you need a new website &mdash; or just a few targeted fixes.",
        "service": "website-design",
        "body": [
            ("callout", "a new website isn&rsquo;t always the answer. Sometimes a few targeted fixes will do more for your enquiries &mdash; for a fraction of the cost. These questions help you work out which is which."),
            ("p", "We get asked this a lot, and our answer surprises people: often, no. A rebuild is a big investment, and if the real problem is something smaller, a shiny new design won&rsquo;t fix it. Before you spend, ask yourself these seven questions."),
            ("h2", "1. What problem are you actually trying to solve?"),
            ("p", "&ldquo;The website looks dated&rdquo; and &ldquo;the website doesn&rsquo;t bring in enquiries&rdquo; are very different problems. The first might need a redesign. The second might need better content, clearer calls to action or SEO work &mdash; none of which require starting over."),
            ("h2", "2. Is it slow, especially on a phone?"),
            ("p", "Most visitors will find you on their phone. If pages take more than a few seconds to load, people leave before they&rsquo;ve read a word. Speed problems can often be fixed &mdash; image optimisation, better hosting, removing heavy plugins &mdash; without a rebuild. But if the site sits on an outdated platform that simply can&rsquo;t be sped up, that&rsquo;s a genuine reason to start fresh."),
            ("h2", "3. Can you update it yourself?"),
            ("p", "If changing a price or adding a photo means emailing a developer and waiting a week, your website is costing you time and money every month. A modern, easy-to-edit site is one of the strongest arguments for a rebuild."),
            ("h2", "4. Does it still describe what you do?"),
            ("p", "Businesses evolve. If your services, pricing or customers have changed and the website hasn&rsquo;t kept up, you may only need new content and a few new pages &mdash; not a new site."),
            ("h2", "5. Is it secure and still supported?"),
            ("p", "An unsupported theme, outdated plugins or a missing SSL certificate are real risks &mdash; to your customers&rsquo; data and to your Google rankings. If the platform itself is no longer maintained, rebuilding is usually the safer long-term choice."),
            ("h2", "6. Do people who visit actually get in touch?"),
            ("p", "Look at the numbers if you have them. Plenty of visitors but few enquiries usually points to messaging, trust signals or the contact process &mdash; all fixable. Very few visitors is a visibility problem, and SEO will do more for you than design."),
            ("h2", "7. Does it reflect the quality of your work?"),
            ("p", "This one matters, especially for premium and luxury businesses. If your website feels cheaper than what you actually deliver, it quietly undermines every enquiry. That&rsquo;s a legitimate reason to invest in a proper redesign."),
            ("h2", "So &mdash; fix or rebuild?"),
            ("ul", [
                "<b>Mostly fix</b> if the site is modern, secure and easy to edit, but underperforming. Improve the content, speed and calls to action.",
                "<b>Mostly rebuild</b> if the platform is outdated, you can&rsquo;t edit it, it&rsquo;s slow at its core, or it no longer reflects your business.",
            ]),
            ("p", "If you&rsquo;re not sure which side you fall on, that&rsquo;s exactly the kind of question we&rsquo;re happy to answer honestly &mdash; even when the answer is &ldquo;you don&rsquo;t need us yet.&rdquo;"),
        ],
    },
    {
        "slug": "seo-vs-aeo-what-your-business-needs",
        "title_tag": "SEO vs AEO: What’s the Difference?",
        "meta": "More customers now ask ChatGPT and Google’s AI for recommendations. Here is how SEO and AEO differ, and whether your business needs both.",
        "title": "SEO vs AEO: What&rsquo;s the Difference, and Does Your Business Need Both?",
        "date": "2026-09-22",
        "category": "SEO &amp; AEO",
        "read": "6 min read",
        "image": "aeo-ai-search-hero.webp",
        "image_alt": "AI search interface answering a customer's question",
        "excerpt": "More customers now ask ChatGPT and Google&rsquo;s AI for recommendations instead of scrolling through results. Here&rsquo;s what that means for your search visibility, explained in full.",
        "service": "seo-services",
        "body": [
            ("callout", "SEO helps you rank in Google&rsquo;s list of results. AEO helps AI tools like ChatGPT and Google&rsquo;s AI Overviews understand and recommend you. They share the same foundations, so most businesses should treat them as one strategy, not two."),
            ("h2", "Search has changed &mdash; but not completely"),
            ("p", "For twenty years, getting found online meant one thing: ranking on page one of Google. That still matters. But more of your customers now ask questions a different way &mdash; they type a full question into ChatGPT, read an AI Overview at the top of Google, or ask a voice assistant for a recommendation. Instead of a list of ten links, they get a single answer."),
            ("p", "That shift is why you&rsquo;re hearing a new term: AEO, or Answer Engine Optimisation."),
            ("h2", "What SEO actually does"),
            ("p", "Search Engine Optimisation is the work of helping search engines find, understand and rank your website. Done properly, it covers four areas:"),
            ("ul", [
                "<b>Technical health</b> &mdash; speed, mobile usability and a structure search engines can crawl.",
                "<b>Content</b> &mdash; pages built around what your customers actually search for.",
                "<b>Local presence</b> &mdash; your Google Business Profile, directory listings and location pages.",
                "<b>Authority</b> &mdash; relevant links and mentions that show your business is trusted.",
            ]),
            ("p", "The goal of SEO is a click: someone sees your listing, visits your site and gets in touch."),
            ("h2", "What AEO does differently"),
            ("p", "AEO is about being the answer rather than one of the results. AI tools read the web, decide which sources they trust, and summarise. If your business is described clearly and consistently, you&rsquo;re more likely to be mentioned. If it isn&rsquo;t, the AI simply recommends someone else."),
            ("ul", [
                "<b>Answer-ready content</b> &mdash; clear, direct answers to the questions customers really ask.",
                "<b>Structured data</b> &mdash; schema markup that tells machines who you are, what you offer and where.",
                "<b>Consistency</b> &mdash; the same name, services and contact details everywhere you appear.",
                "<b>Trust signals</b> &mdash; reviews, credentials and clear authorship.",
            ]),
            ("h2", "The overlap is bigger than the difference"),
            ("p", "Here&rsquo;s the honest part: good AEO is mostly good SEO, done thoroughly. Both reward fast, well-structured websites, genuinely useful content and a trustworthy reputation. An agency that sells AEO as a completely separate, expensive product is usually overcomplicating it."),
            ("p", "Where they differ is emphasis. SEO leans on keywords and rankings. AEO leans on clarity, structure and being quotable &mdash; writing a direct two-sentence answer to &ldquo;how much does a website cost in Manchester?&rdquo; rather than burying it in paragraph six."),
            ("h2", "So which does your business need?"),
            ("ul", [
                "<b>Starting from scratch?</b> Fix the SEO foundations first. AEO won&rsquo;t help a slow site that search engines can&rsquo;t crawl.",
                "<b>Already ranking reasonably well?</b> Adding answer-style content and schema is often a quick, low-cost win.",
                "<b>Rely on local customers?</b> Both matter. Google Maps, AI Overviews and voice assistants all draw on the same local signals.",
            ]),
            ("h2", "Three things you can do this week"),
            ("ul", [
                "Add an FAQ section to your key service pages, answering the questions customers ask you on the phone.",
                "Check that your business name, address and phone number match exactly across your website, Google Business Profile and directories.",
                "Search for your own services in ChatGPT and Google &mdash; note who gets recommended, and why.",
            ]),
            ("p", "If you&rsquo;d like a comprehensive view of where you stand on both, we&rsquo;re happy to take a look &mdash; no jargon, no obligation."),
        ],
    },
]


def _fmt_date(iso):
    y, m, d = iso.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    return "%d %s %s" % (int(d), months[int(m) - 1], y)

def _plain(s):
    return html.unescape(s)

def render_post_card(post, root=""):
    return """<a class="pb-post-card" href="%(root)s%(slug)s.html">
  <img src="%(root)simages/%(img)s" alt="%(alt)s" width="640" height="400" loading="lazy" decoding="async">
  <div class="pb-post-card__body">
    <p class="pb-post-meta"><span class="pb-post-tag">%(cat)s</span> %(date)s &middot; %(read)s</p>
    <h3>%(title)s</h3>
    <p>%(excerpt)s</p>
    <span class="pb-link">Read article %(arrow)s</span>
  </div>
</a>""" % {"root": root, "slug": post["slug"], "img": post["image"], "alt": post["image_alt"],
           "cat": post["category"], "date": _fmt_date(post["date"]), "read": post["read"],
           "title": post["title"], "excerpt": post["excerpt"], "arrow": icon("arrow")}

def render_blog_teaser(root=""):
    cards = "".join(render_post_card(p, root) for p in BLOG_POSTS[:3])
    return """
<section class="pb-section">
  <div class="pb-wrap">
    <div class="pb-section__head">
      <div><p class="pb-eyebrow">Insights</p><h2>Expert advice for growing businesses</h2></div>
      <div>
        <p>Guides on websites, search and marketing, written to help you decide, not to sell.</p>
        <a class="pb-link" href="%(root)sblog.html" style="margin-top:14px">Read all insights %(arrow)s</a>
      </div>
    </div>
    <div class="pb-blog-grid">%(cards)s</div>
  </div>
</section>
""" % {"root": root, "cards": cards, "arrow": icon("arrow")}

def _render_post_body(blocks):
    out = []
    for kind, content in blocks:
        if kind == "p":
            out.append("<p>%s</p>" % content)
        elif kind == "h2":
            out.append("<h2>%s</h2>" % content)
        elif kind == "ul":
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % li for li in content))
        elif kind == "callout":
            out.append('<div class="pb-callout"><p><b>In a nutshell:</b> %s</p></div>' % content)
    return "".join(out)

def build_blog_post(post):
    root = ""
    s = SERVICES[post["service"]]
    others = [p for p in BLOG_POSTS if p["slug"] != post["slug"]]
    jsonld = render_jsonld({
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": _plain(post["title"]), "datePublished": post["date"],
        "image": SITE_URL + "/images/" + post["image"],
        "author": {"@type": "Organization", "name": "Pinky Brain Digital"},
        "publisher": {"@type": "Organization", "name": "Pinky Brain Digital", "logo": {"@type": "ImageObject", "url": SITE_URL + "/images/logo.png"}},
        "description": _plain(post["excerpt"]), "mainEntityOfPage": page_url(post["slug"] + ".html"),
    })
    out = [
        head_html(root, "%s | Pinky Brain Digital" % post.get("title_tag", _plain(post["title"])), post.get("meta", _plain(post["excerpt"])), post["slug"] + ".html"),
        header_html(root, current="insights"),
        render_breadcrumb([("Home", "index.html"), ("Insights", "blog.html"), (post["category"], None)]),
        """
<article>
  <header class="pb-article-head">
    <div class="pb-wrap">
      <p class="pb-eyebrow">%(cat)s</p>
      <h1>%(title)s</h1>
      <p class="pb-post-meta">By the Pinky Brain Digital team &middot; %(date)s &middot; %(read)s</p>
      <img class="pb-article-head__img" src="images/%(img)s" alt="%(alt)s" width="900" height="450" fetchpriority="high" decoding="async">
    </div>
  </header>
  <div class="pb-section" style="padding-top:clamp(40px,5vw,64px)">
    <div class="pb-wrap pb-article">
      %(body)s
      <div class="pb-article__service">
        <div>
          <p class="pb-eyebrow" style="margin-bottom:8px">Related service</p>
          <h2 style="margin:0;font-size:1.2rem">%(sname)s</h2>
          <p>%(slead)s</p>
        </div>
        <a class="pb-btn pb-btn--dark" href="%(sslug)s.html">Explore %(slabel)s %(arrow)s</a>
      </div>
    </div>
  </div>
</article>
<section class="pb-section pb-section--tint">
  <div class="pb-wrap">
    <div class="pb-section__head" style="display:block">
      <p class="pb-eyebrow">Keep reading</p>
      <h2>More insights</h2>
    </div>
    <div class="pb-blog-grid">%(more)s</div>
  </div>
</section>
""" % {"cat": post["category"], "title": post["title"], "date": _fmt_date(post["date"]), "read": post["read"],
       "img": post["image"], "alt": post["image_alt"], "body": _render_post_body(post["body"]),
       "sname": s["name"], "slead": cap_first(s["lead"]), "sslug": s["slug"], "slabel": s["nav_label"],
       "arrow": icon("arrow"), "more": "".join(render_post_card(p) for p in others)},
        render_cta("Tell us what you’re working on, and we’ll reply within one business day with honest, expert advice.", root=root,
                   offer_key=SERVICE_OFFER.get(post["service"])),
        footer_html(root),
        jsonld,
        "</body></html>",
    ]
    return write_page(post["slug"] + ".html", "".join(out))

def build_blog_index():
    root = ""
    featured, rest = BLOG_POSTS[0], BLOG_POSTS[1:]
    out = [
        head_html(root, "Insights | Pinky Brain Digital",
                  "Practical guides on websites, SEO, AI search and digital marketing from the Pinky Brain Digital team.", "blog.html"),
        header_html(root, current="insights"),
        render_breadcrumb([("Home", "index.html"), ("Insights", None)]),
        """
<section class="pb-hero" style="padding-bottom:clamp(40px,5vw,64px)">
  <div class="pb-wrap pb-narrow">
    <p class="pb-eyebrow">Insights &amp; advice</p>
    <h1>Insights</h1>
    <p class="pb-lead">Honest, practical guides on websites, search and marketing, written to help you make better decisions, not to sell you something.</p>
  </div>
</section>
<section class="pb-section" style="padding-top:clamp(40px,5vw,64px)">
  <div class="pb-wrap">
    <a class="pb-post-feature" href="%(fslug)s.html">
      <img src="images/%(fimg)s" alt="%(falt)s" width="900" height="620" fetchpriority="high" decoding="async">
      <div>
        <p class="pb-post-meta"><span class="pb-post-tag">Latest</span> %(fcat)s &middot; %(fdate)s &middot; %(fread)s</p>
        <h2>%(ftitle)s</h2>
        <p>%(fexcerpt)s</p>
        <span class="pb-btn pb-btn--dark" style="margin-top:24px">Read article %(arrow)s</span>
      </div>
    </a>
    %(rest)s
  </div>
</section>
""" % {"fslug": featured["slug"], "fimg": featured["image"], "falt": featured["image_alt"],
       "fcat": featured["category"], "fdate": _fmt_date(featured["date"]), "fread": featured["read"],
       "ftitle": featured["title"], "fexcerpt": featured["excerpt"], "arrow": icon("arrow"),
       "rest": ('<h2 class="pb-blog-subhead">More articles</h2><div class="pb-blog-grid">%s</div>'
                % "".join(render_post_card(p) for p in rest)) if rest else ""},
        render_cta("Have a question we haven’t answered here? Ask us, and we’ll reply within one business day.", root=root),
        footer_html(root),
        "</body></html>",
    ]
    return write_page("blog.html", "".join(out))

# ---------------------------------------------------------------------------
# BUILD: PRIVACY POLICY, 404, SITEMAP, ROBOTS
# ---------------------------------------------------------------------------
def build_privacy_page():
    root = ""
    body = """
<h2>Who we are</h2>
<p>Pinky Brain Digital (&ldquo;we&rdquo;, &ldquo;us&rdquo;) is a digital agency based at %(address)s. We are the controller of the personal information described in this policy. You can contact us at <a href="mailto:%(email)s">%(email)s</a>.</p>
<h2>What information we collect</h2>
<ul>
<li><b>Enquiries.</b> If you use our contact form or email us, we collect your name, email address, phone number (if you give it), the service you are interested in and the message you send.</li>
<li><b>Technical information.</b> Like most websites, our hosting provider may record technical details such as your IP address, browser type and the pages you request, for security and to keep the site running.</li>
</ul>
<h2>How we use it</h2>
<ul>
<li>To reply to your enquiry and, if you ask us to, prepare a quote, audit or proposal.</li>
<li>To keep the website secure and working properly.</li>
<li>To meet our legal and accounting obligations if you become a client.</li>
</ul>
<p>We do not sell your information, and we do not use it for automated decision-making.</p>
<h2>Our lawful basis</h2>
<p>We use your details to respond to your enquiry and take steps at your request before a contract (UK GDPR Article 6(1)(b)), and for our legitimate interests in running and securing our business (Article 6(1)(f)). Where we ask for consent, for example for marketing emails, you can withdraw it at any time.</p>
<h2>Who we share it with</h2>
<p>We only share personal information with trusted service providers who help us run the business, such as website hosting and email providers, and only as far as needed for them to do so. We may also share information where the law requires it.</p>
<h2>How long we keep it</h2>
<p>We keep enquiry details for as long as is needed to deal with your request and any follow-up, and for as long as the law or our legitimate business needs require. We review and delete information we no longer need.</p>
<h2>Cookies and tracking</h2>
<p>This website does not currently use analytics, advertising or other non-essential cookies, and our fonts are hosted on our own server. If we add tools that set non-essential cookies in future, we will ask for your consent first and update this policy.</p>
<h2>Your rights</h2>
<p>Under UK data protection law you have the right to ask for a copy of your information, to have inaccurate information corrected, to ask us to delete or restrict our use of it, to object to our use of it and to ask for it in a portable format. To use any of these rights, email <a href="mailto:%(email)s">%(email)s</a>.</p>
<p>If you are unhappy with how we handle your information, you can complain to the Information Commissioner&rsquo;s Office at <a href="https://ico.org.uk" rel="noopener">ico.org.uk</a> or on 0303 123 1113. We would appreciate the chance to put things right first.</p>
<h2>International transfers</h2>
<p>Some of our service providers may process information outside the UK. Where they do, we make sure appropriate safeguards are in place.</p>
<h2>Changes to this policy</h2>
<p>We may update this policy from time to time. The latest version will always be on this page.</p>
""" % {"address": SITE_ADDRESS, "email": SITE_EMAIL}
    out = [
        head_html(root, "Privacy Policy | Pinky Brain Digital",
                  "How Pinky Brain Digital collects, uses and protects your personal information, and your rights under UK data protection law.",
                  "privacy-policy.html"),
        header_html(root),
        render_breadcrumb([("Home", "index.html"), ("Privacy Policy", None)]),
        """
<section class="pb-section">
  <div class="pb-wrap"><div class="pb-prose">
    <p class="pb-eyebrow">Legal</p>
    <h1 style="font-family:var(--pb-font-head);font-size:clamp(2rem,4vw,3rem);line-height:1.1;letter-spacing:-.03em">Privacy Policy</h1>
    <p class="pb-updated">Last updated: 5 October 2026</p>
    %s
  </div></div>
</section>""" % body,
        footer_html(root),
        "</body></html>",
    ]
    return write_page("privacy-policy.html", "".join(out))

# The 404 page is served from whatever URL was mistyped, so relative links need a base:
# "/<repo>/" on a github.io project site, "/" on a normal domain.
BASE_FIX = (
    "<script>document.write('<base href=\"' + (location.hostname.slice(-10) === '.github.io' ? "
    "'/' + location.pathname.split('/')[1] + '/' : '/') + '\">');</script>\n")

def build_404_page():
    root = ""
    out = [
        head_html(root, "Page Not Found | Pinky Brain Digital", "Sorry, we couldn’t find that page. Try our services, locations or contact page.", "404.html", noindex=True,
                  extra_head=BASE_FIX),
        header_html(root),
        """
<section class="pb-404">
  <div class="pb-wrap" style="max-width:640px">
    <p class="pb-404__code" aria-hidden="true">404</p>
    <h1 style="font-family:var(--pb-font-head);font-size:clamp(1.8rem,3.5vw,2.6rem);line-height:1.15;margin-top:12px">We can&rsquo;t find that page.</h1>
    <p class="pb-lead" style="margin:16px auto 0">The link may be out of date, or the page may have moved. Try one of these instead.</p>
    <div class="pb-hero__actions">
      <a class="pb-btn pb-btn--dark" href="index.html">Back to the homepage</a>
      <a class="pb-btn pb-btn--line" href="services.html">%s</a>
    </div>
    <p style="margin-top:28px;font-size:.95rem"><a class="pb-link" href="contact-us.html">%s</a></p>
  </div>
</section>""" % (CTA_SECONDARY, CTA_PRIMARY),
        footer_html(root),
        "</body></html>",
    ]
    return write_page("404.html", "".join(out))

def build_sitemap_page(locations):
    root = ""

    def col(heading, links, anchor_id=""):
        items = "".join('<li><a href="%s">%s</a></li>' % (href, label) for label, href in links)
        anchor = ' id="%s"' % anchor_id if anchor_id else ""
        return '<div%s><h2>%s</h2><ul>%s</ul></div>' % (anchor, heading, items)

    company = [("Home", "index.html"), ("About Us", "about-us.html"), ("Services", "services.html"),
               ("Industries", "industries.html"), ("Locations", "locations.html"), ("Insights", "blog.html"),
               ("Contact Us", "contact-us.html"), ("Privacy Policy", "privacy-policy.html"), ("Sitemap", "sitemap.html")]
    services = [(SERVICES[k]["name"], "%s.html" % k) for k in ALL_SERVICE_SLUGS]
    posts = [(_plain(p["title"]), "%s.html" % p["slug"]) for p in BLOG_POSTS]
    wd = [(l["city"], "%s.html" % l["folder"]) for l in locations if l["service_key"] == "website-design"]
    seo = [(l["city"], "%s.html" % l["folder"]) for l in locations if l["service_key"] == "seo-services"]
    cols = (col("Company", company) + col("Services", services) + col("Insights", posts)
            + col("Website design locations", wd, "website-design") + col("SEO locations", seo, "seo-services"))
    out = [
        head_html(root, "Sitemap | Pinky Brain Digital", "A complete list of every page on the Pinky Brain Digital website: services, locations, industries, insights and company pages.", "sitemap.html"),
        header_html(root),
        render_breadcrumb([("Home", "index.html"), ("Sitemap", None)]),
        """
<section class="pb-section">
  <div class="pb-wrap">
    <div class="pb-section__head" style="display:block">
      <p class="pb-eyebrow">Every page</p>
      <h1 style="font-family:var(--pb-font-head);font-size:clamp(2rem,4vw,3rem);line-height:1.1;letter-spacing:-.03em">Sitemap</h1>
    </div>
    <div class="pb-sitemap-grid">%s</div>
  </div>
</section>""" % cols,
        footer_html(root),
        "</body></html>",
    ]
    return write_page("sitemap.html", "".join(out))

def build_sitemap_xml(locations):
    files = (["index.html", "about-us.html", "services.html", "industries.html", "locations.html", "blog.html",
              "contact-us.html", "privacy-policy.html"]
             + ["%s.html" % k for k in ALL_SERVICE_SLUGS]
             + ["%s.html" % p["slug"] for p in BLOG_POSTS]
             + ["%s.html" % l["folder"] for l in locations])
    body = "".join("  <url><loc>%s</loc></url>\n" % page_url(f) for f in files)
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % body
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE_URL)
    return os.path.join(ROOT, "sitemap.xml")

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    locations = read_locations()
    missing = sorted({l["city"] for l in locations} - set(CITY_PROFILES))
    assert not missing, "no city profile for: %s" % missing

    built = [build_homepage()]
    built += [build_service_page(k) for k in ALL_SERVICE_SLUGS]
    built += [build_location_page(loc, i) for i, loc in enumerate(locations)]
    built += [build_services_page(), build_industries_page(), build_contact_page(), build_about_page(),
              build_locations_page(locations), build_blog_index()]
    built += [build_blog_post(p) for p in BLOG_POSTS]
    built += [build_privacy_page(), build_404_page(), build_sitemap_page(locations), build_sitemap_xml(locations)]
    print("Built %d files (%d services, %d locations, %d posts)" % (len(built), len(ALL_SERVICE_SLUGS), len(locations), len(BLOG_POSTS)))

if __name__ == "__main__":
    main()
