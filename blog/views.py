from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import Http404, JsonResponse
from .models import Post, ContactMessage
from .forms import PostForm

# Helper function jo Gmail par notification bhejega
def notify_admin_email(subject, body):
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['yadavhimanshu11358@gmail.com'],
            fail_silently=True,
        )
    except Exception:
        pass

# 1. Home Page: Sirf Home, About, Services aur Contact (AJAX support ke saath)
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message_text = request.POST.get('message', '').strip()

        if name and email and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message_text
            )
            notify_admin_email(
                f"New Portfolio Inquiry from {name}",
                f"Name: {name}\nEmail/Phone: {email}\n\nMessage:\n{message_text}"
            )
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Shukriya! Aapka message successfully bhej diya gaya hai.'})
            messages.success(request, 'Shukriya! Aapka message successfully bhej diya gaya hai.')
            return redirect('home')
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Kripya saari fields bharein.'}, status=400)

    return render(request, 'blog/home.html', {
        'services': SERVICES_DATA
    })


# 2. Dedicated Blog Page (/blog/) + Admin-Protected Publish Form
def blog_list(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Sirf Admin hi naya blog publish kar sakta hai.')
            return redirect('blog_list')

        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        if title and content:
            Post.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            messages.success(request, 'Naya blog post successfully publish ho gaya hai!')
            return redirect('blog_list')

    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/blog_list.html', {'posts': posts})


# 3. Single Blog Detail + Related Articles
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    related_posts = Post.objects.exclude(pk=pk).order_by('-created_at')[:3]
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'related_posts': related_posts
    })
# 3. Single Blog Detail
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# 4. Create, Edit & Delete Blog
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = User.objects.first()
            post.save()
            return redirect('blog_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Naya Blog Likhein'})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Blog Edit Karein'})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


# 5. Services Data (650+ Words per Service)
SERVICES_DATA = {
    'digital-marketing': {
        'title': 'Full-Stack Digital Marketing',
        'short_desc': 'Data-driven multi-channel growth funnels, CRO, and brand scaling strategies.',
        'badge': 'Full-Stack Growth',
        'tagline': 'Data-driven online marketing strategies designed to grow your brand, qualified traffic, and predictable revenue.',
        'overview': (
            'In today’s competitive digital landscape, simply having a website or social media page is no longer enough to stand out. '
            'Businesses need a cohesive, multi-channel digital marketing strategy that attracts high-intent prospects, builds lasting brand authority, '
            'and converts visitors into loyal paying customers. Our Full-Stack Digital Marketing service bridges the gap between long-term organic '
            'brand building and high-velocity paid customer acquisition. Instead of chasing vanity metrics like impressions, likes, or empty clicks, '
            'we focus strictly on measurable business outcomes: lower customer acquisition costs (CAC), higher customer lifetime value (LTV), and '
            'consistent month-over-month sales pipeline growth. Whether you are launching a new startup or scaling an established small business, '
            'we audit your entire digital footprint, uncover high-leverage growth bottlenecks, and execute customized campaigns across search engines, '
            'social media platforms, and high-converting landing pages.'
        ),
        'features': [
            'Complete Brand Strategy & Competitive Market Positioning',
            'Omnichannel Content Marketing & Audience Engagement Funnels',
            'Conversion Rate Optimization (CRO) & Landing Page Testing',
            'Google Analytics 4 (GA4), Tag Manager & Full Attribution Setup',
            'Transparent Weekly & Monthly ROI Performance Reports'
        ],
        'deliverables': [
            ('Comprehensive Market & Competitor Audit', 'Deep-dive analysis of your industry landscape, competitor ad funnels, keyword gaps, pricing positioning, and untapped customer segments.'),
            ('Omnichannel Customer Journey Architecture', 'Designing end-to-end marketing funnels from initial awareness touchpoints to retargeting sequences and high-converting inquiry forms.'),
            ('Content & Brand Authority Production', 'Creating educational blog guides, lead magnets, and social media assets that build trust and answer buyer objections before a sales call.'),
            ('Conversion Rate Optimization (CRO)', 'Continuous A/B testing of headlines, call-to-action buttons, form friction, and page load speeds to maximize leads from existing traffic.'),
            ('Analytics, Tracking & Revenue Attribution', 'Complete configuration of Google Analytics 4, Google Tag Manager, and conversion pixels so every rupee spent is tracked accurately.')
        ],
        'process': [
            ('1. Discovery & Baseline Growth Audit', 'We analyze your historical traffic, current conversion rates, target buyer personas, and revenue goals to build a clear 90-day execution roadmap.'),
            ('2. Tracking & Funnel Foundation', 'Before spending a single rupee on promotion, we fix broken analytics, configure conversion events, and optimize landing pages for mobile and desktop users.'),
            ('3. Coordinated Multi-Channel Launch', 'We deploy synchronized organic and paid campaigns across Google, Meta, and content channels, ensuring consistent brand messaging at every touchpoint.'),
            ('4. Weekly Optimization & Budget Scaling', 'Using real-time conversion data, we cut underperforming campaigns, reallocate budget to winning channels, and deliver clear weekly progress updates.')
        ],
        'why_us': (
            'Many marketing agencies lock clients into rigid, expensive retainers while delegating execution to inexperienced junior managers. '
            'When you work with Himanshu Yadav, you receive direct, hands-on strategy and execution backed by technical Python and Django web development '
            'expertise alongside practical small-business acumen. Because we understand both the underlying code of your website and the psychology behind '
            'buyer decisions, we eliminate technical bottlenecks and build self-sustaining marketing systems that compound over time.'
        ),
        'faqs': [
            ('How long does it take to see measurable results from digital marketing?', 'Paid acquisition channels like Google Ads and Meta Ads generate targeted traffic and inquiries within the first 7 to 14 days, while organic channels like SEO and content marketing build compounding momentum over 3 to 6 months.'),
            ('Do I need a large marketing budget to get started?', 'No. We design lean, high-intent strategies specifically tailored for small and growing businesses—proving positive return on investment before scaling your budget.'),
            ('How will I track the progress and ROI of my campaigns?', 'You receive transparent, jargon-free weekly and monthly reports highlighting total leads generated, cost per acquisition, website traffic growth, and exact next steps.')
        ]
    },
    'seo': {
        'title': 'SEO (Search Engine Optimization)',
        'short_desc': 'Technical SEO, keyword dominance, and white-hat authority building for Google.',
        'badge': 'Organic Traffic',
        'tagline': 'Rank higher on Google search results, capture high-intent organic traffic, and build long-term domain authority.',
        'overview': (
            'Search Engine Optimization (SEO) is one of the highest-ROI investments a business can make because it connects your brand with '
            'customers at the exact moment they are actively searching for your solutions. Unlike paid advertising, where leads stop the second '
            'you pause your budget, a strong organic search presence delivers compounding, 24/7 inbound traffic without paying for every click. '
            'However, modern Google search algorithms demand far more than keyword stuffing or low-quality directory links. Sustainable search '
            'dominance requires clean technical site architecture, fast Core Web Vitals, helpful human-first content, and authoritative backlinks. '
            'Our SEO service takes a holistic, white-hat engineering approach—fixing underlying crawl and speed issues, mapping commercial-intent '
            'keywords to dedicated service pages, and building topical authority so your website outranks competitors consistently.'
        ),
        'features': [
            'In-Depth Commercial Keyword Research & Competitor Gap Audit',
            'Technical SEO Fixes (Page Speed, Schema Markup, Sitemaps & Mobile UX)',
            'On-Page Optimization & High-Converting Content Architecture',
            'White-Hat High-Authority Backlink Building & Local SEO',
            'Monthly Keyword Ranking, CTR & Organic Lead Tracking'
        ],
        'deliverables': [
            ('Technical SEO & Site Health Audit', 'Resolving crawl errors, broken redirects, duplicate content, XML sitemaps, robots.txt rules, structured schema markup, and Core Web Vitals speed bottlenecks.'),
            ('Commercial Keyword Research & Mapping', 'Identifying high-converting buyer keywords, long-tail search opportunities, and local search terms mapped cleanly to individual website pages.'),
            ('On-Page SEO & Semantic Optimization', 'Crafting compelling title tags, meta descriptions, semantic H1–H3 heading structures, strategic internal linking, and descriptive image alt attributes.'),
            ('Authoritative Content Creation', 'Writing in-depth, well-researched service pages and educational blog posts designed to satisfy search intent and earn top organic rankings.'),
            ('Local SEO & Google Business Profile', 'Optimizing local citations, Google Map Pack visibility, and location-specific landing pages so nearby customers discover your business first.')
        ],
        'process': [
            ('1. Technical Crawl & Competitor Gap Analysis', 'We run a complete diagnostic crawl of your website and reverse-engineer the top-ranking competitors in your niche to uncover immediate ranking opportunities.'),
            ('2. On-Page & Technical Foundation Fixes', 'We clean up URL structures, improve mobile responsiveness, implement JSON-LD structured schema data, and optimize existing pages for target keywords.'),
            ('3. Content & Topical Authority Expansion', 'We publish comprehensive service and informational content targeting high-intent search queries across every stage of your buyer’s research journey.'),
            ('4. Authority Building & Rank Monitoring', 'We earn relevant, reputable backlinks and closely monitor keyword movements, organic click-through rates (CTR), and inbound lead conversions every month.')
        ],
        'why_us': (
            'Because we are also full-stack Python and Django web developers, we do not just hand you a generic audit spreadsheet and leave you '
            'to figure out the technical implementation. We understand server response codes, clean HTML semantics, caching, asset minification, and '
            'structured data directly at the code level—allowing us to execute technical SEO upgrades faster and far more accurately than traditional agencies.'
        ),
        'faqs': [
            ('How long does SEO take to show noticeable ranking improvements?', 'Technical and on-page optimizations frequently produce initial ranking lifts within 4 to 8 weeks, while competitive commercial keywords typically reach top positions within 3 to 6 months.'),
            ('Do you follow Google’s safe, white-hat SEO guidelines?', 'Yes, 100%. We strictly follow Google Search Essentials and never use spammy link farms, private blog networks, or automated shortcuts that put your domain at risk.'),
            ('Can you optimize both local businesses and national websites?', 'Yes. Whether you want to dominate local map searches in a specific city or rank nationwide for software and service queries, we tailor the keyword strategy accordingly.')
        ]
    },
    'ppc': {
        'title': 'PPC Advertising',
        'short_desc': 'High-converting Pay-Per-Click campaigns engineered to maximize ROAS and cut waste.',
        'badge': 'Instant Leads',
        'tagline': 'Maximize your return on ad spend (ROAS) with precision-targeted, data-backed Pay-Per-Click campaigns.',
        'overview': (
            'Pay-Per-Click (PPC) advertising is the fastest way to place your business directly in front of ready-to-buy customers across search '
            'engines and high-traffic digital networks. When structured properly, PPC gives you complete control over your daily budget, geographic '
            'reach, audience demographics, and exact messaging—turning ad spend into predictable leads and sales within days of launch. However, '
            'poorly configured PPC accounts silently waste up to 40% of their budget on irrelevant search queries, broad audience leakage, and weak '
            'landing pages. Our PPC Advertising management service focuses on ruthless efficiency, granular campaign segmentation, and continuous '
            'conversion rate optimization. Every click is tracked, every search term is audited, and every rupee is directed toward campaigns that '
            'generate measurable pipeline and profitable customer acquisition.'
        ),
        'features': [
            'Granular Campaign Architecture & Audience Segmentation',
            'High-Converting Ad Copywriting & Dedicated Landing Page Alignment',
            'Smart Bid Management, Dayparting & Budget Optimization',
            'Continuous A/B Split Testing for Maximum Click-Through Rate (CTR)',
            'End-to-End Conversion, Cost-Per-Lead (CPL) & ROAS Tracking'
        ],
        'deliverables': [
            ('PPC Account Audit & Budget Leak Prevention', 'Analyzing historical campaign data to eliminate wasted ad spend, pause low-intent placements, and restructure overlapping ad groups.'),
            ('High-Intent Targeting & Negative Filtering', 'Focusing budget on bottom-of-funnel buyer intent while maintaining aggressive negative keyword and placement exclusion lists.'),
            ('Persuasive Ad Copy & Creative Testing', 'Writing direct-response headlines and descriptions tested systematically to boost Quality Score and lower Cost-Per-Click (CPC).'),
            ('Conversion-Focused Landing Page Optimization', 'Aligning landing page headlines, social proof, and inquiry forms with your ad promise to maximize visitor-to-lead conversion rates.'),
            ('Granular Attribution & ROI Reporting', 'Connecting ad clicks directly to form submissions, phone calls, and CRM sales so you know the exact return on every campaign.')
        ],
        'process': [
            ('1. Unit Economics & Target CPL Calculation', 'We analyze your product margins, average customer value, and target Cost Per Lead so every bidding decision is grounded in real profitability.'),
            ('2. Precision Campaign & Tracking Build', 'We configure clean conversion tracking, UTM parameters, and tightly themed ad groups engineered for high relevance and strong Quality Scores.'),
            ('3. Controlled Launch & Daily Bid Refinement', 'During the critical launch window, we monitor search queries, device performance, and click-through rates daily to trim waste immediately.'),
            ('4. Profitable Scaling & Split Testing', 'Once winning ad sets and keywords prove consistent ROI, we expand high-performing segments and scale budgets systematically.')
        ],
        'why_us': (
            'Many PPC managers set campaigns on automated defaults and only check performance once a month. We treat your advertising budget '
            'like our own capital—combining active search-term mining, technical conversion tracking, and landing page optimization to ensure '
            'your campaigns get leaner, smarter, and more profitable every week.'
        ),
        'faqs': [
            ('How is PPC advertising different from organic SEO?', 'PPC delivers immediate top-of-page visibility and leads within 24 to 72 hours of launch by paying per click, whereas SEO builds long-term organic rankings over several months.'),
            ('What budget do I need to run profitable PPC campaigns?', 'You can start effectively with a focused test budget—typically ₹15,000 to ₹40,000 per month in ad spend—and scale up once positive ROI is proven.'),
            ('Do I retain full ownership of my ad accounts and data?', 'Yes, 100%. All campaigns are built inside your own advertising accounts so you retain permanent ownership of all data, audiences, and assets.')
        ]
    },
    'google-ads': {
        'title': 'Google Ads Management',
        'short_desc': 'Capture ready-to-buy customers on Google Search, Display, and YouTube.',
        'badge': 'Search & Display',
        'tagline': 'Capture high-intent customers actively searching for your products and services on Google Search, Display & YouTube.',
        'overview': (
            'Every second, millions of buyers with urgent problems type high-intent queries directly into Google Search. Google Ads allows your '
            'business to appear at the very top of those search results at the exact moment a prospect is ready to call, book, or buy. '
            'Our Google Ads management service covers Search, Performance Max, Display, and YouTube remarketing campaigns engineered specifically '
            'for maximum Return on Ad Spend (ROAS). Because Google’s automated bidding and broad-match defaults can easily burn through budget on '
            'unrelated searches, we apply strict campaign architecture, exact and phrase-match keyword clustering, negative keyword firewalls, '
            'and enhanced server-side conversion tracking. The result is a high-efficiency acquisition engine that delivers qualified inquiries '
            'and phone calls consistently.'
        ),
        'features': [
            'Search, Display, YouTube & Performance Max Campaign Management',
            'Aggressive Negative Keyword Filtering to Eliminate Wasted Spend',
            'Enhanced Conversion Tracking & Google Tag Manager (GTM) Setup',
            'High-CTR Responsive Search Ads & Full Ad Extensions',
            'Weekly Search Term Mining, Bid Adjustments & Scaling'
        ],
        'deliverables': [
            ('Account Restructuring & Wasted Spend Audit', 'Identifying budget leaks in existing Google Ads accounts, consolidating fragmented campaigns, and eliminating low-intent broad match waste.'),
            ('Buyer-Intent Keyword & Negative Firewall Setup', 'Targeting high-converting commercial keywords while continuously updating negative keyword lists to block job seekers, freebie hunters, and irrelevant clicks.'),
            ('Compelling Ad Copy & SERP Extensions', 'Crafting persuasive Responsive Search Ads paired with sitelinks, callouts, structured snippets, and call extensions to maximize screen real estate.'),
            ('Google Tag Manager & Enhanced Conversions', 'Implementing accurate form submission, phone call, and offline conversion tracking so Google Smart Bidding optimizes for real customers.'),
            ('Landing Page Message-Match Optimization', 'Improving page load speed and headline alignment between your Google ad and landing page to raise Quality Score and reduce CPC.')
        ],
        'process': [
            ('1. Keyword Intent & Competitor Auction Analysis', 'We research commercial search volume, competitor ad copy, and auction dynamics to identify the highest-converting keyword opportunities.'),
            ('2. Tightly Themed Campaign Construction', 'We build structured campaigns segmented by service line and geographic location, ensuring each ad group speaks directly to the user’s query.'),
            ('3. Launch & Intensive Search Term Mining', 'In the first two weeks post-launch, we review actual search term reports daily, adding negative keywords and refining bid modifiers.'),
            ('4. Smart Bidding Transition & Scaling', 'Once sufficient verified conversion data is collected, we leverage data-driven bidding strategies to scale lead volume at your target CPL.')
        ],
        'why_us': (
            'Google Ads rewards technical precision. By combining deep keyword intent modeling, clean Google Tag Manager conversion tracking, '
            'and fast Django/HTML landing pages, we achieve higher Quality Scores—meaning you pay less per click than competitors while securing '
            'higher ad positions.'
        ),
        'faqs': [
            ('How quickly can Google Ads start generating leads for my business?', 'Once your conversion tracking and ad creatives are approved, targeted clicks and customer inquiries typically begin within 24 to 72 hours.'),
            ('Should I run Search Ads or Performance Max campaigns?', 'For most service businesses, high-intent Google Search campaigns deliver the cleanest lead quality first, after which Performance Max can be layered on for broader scale.'),
            ('How do you prevent clicks from irrelevant searches?', 'We use strict phrase and exact match keywords combined with proactive negative keyword lists reviewed every week.')
        ]
    },
    'meta-ads': {
        'title': 'Meta Ads (Facebook & Instagram)',
        'short_desc': 'Scroll-stopping Reels & Feed creatives with precision retargeting funnels.',
        'badge': 'Social Scaling',
        'tagline': 'Scale leads and e-commerce sales on Facebook & Instagram with scroll-stopping creatives and precision retargeting.',
        'overview': (
            'Facebook and Instagram remain two of the most powerful demand-generation platforms available, enabling businesses to reach ideal '
            'prospects based on interests, behaviors, demographics, and real-time purchase signals. Unlike search ads that wait for users to '
            'actively look for you, Meta Ads proactively introduce your brand to high-potential customers while they scroll their feeds, Stories, '
            'and Reels. Success on modern Meta Ads depends heavily on strong creative hooks, clear offer positioning, and accurate Meta Pixel + '
            'Conversions API (CAPI) tracking. Our Meta Ads management service blends persuasive direct-response copywriting, high-impact visual '
            'and video ad concepts, and multi-stage retargeting funnels to convert cold audiences into booked appointments and repeat buyers.'
        ),
        'features': [
            'Custom Audience, Interest & High-Performing Lookalike Targeting',
            'Scroll-Stopping Ad Creative Concepts & Direct-Response Copywriting',
            'Meta Pixel & Conversions API (CAPI) Event Tracking Setup',
            'Full-Funnel Cold Prospecting & Warm Retargeting Sequences',
            'Lead Generation Forms & E-Commerce Sales Scaling Campaigns'
        ],
        'deliverables': [
            ('Meta Pixel & Conversions API (CAPI) Configuration', 'Setting up accurate browser and server-side event tracking for leads, purchases, and custom actions to overcome iOS privacy signal loss.'),
            ('Audience Research & Lookalike Modeling', 'Building warm retargeting pools from website visitors, video viewers, and social engagers alongside high-converting Lookalike audiences.'),
            ('Creative Angle & Ad Copy Production', 'Developing multiple creative hooks, carousel structures, and direct-response ad copy tailored to distinct customer pain points.'),
            ('Full-Funnel Campaign Architecture', 'Separating cold prospecting campaigns from warm retargeting sequences so prospects see relevant testimonials, case studies, and offers.'),
            ('Creative Fatigue Monitoring & Budget Scaling', 'Tracking frequency, thumb-stop rate, and Cost Per Result weekly to refresh creatives before performance declines.')
        ],
        'process': [
            ('1. Offer Positioning & Buyer Persona Mapping', 'We define your strongest value proposition, craft an irresistible lead magnet or front-end offer, and map your core audience segments.'),
            ('2. Pixel Verification & Funnel Integration', 'We verify domain ownership, test conversion events, and connect Meta Instant Forms or high-speed external landing pages.'),
            ('3. Structured Creative Testing Phase', 'We run controlled creative tests comparing multiple headlines, visuals, and calls-to-action to identify low-CPL winning combinations.'),
            ('4. Warm Retargeting & Vertical Scaling', 'We deploy social-proof retargeting ads to warm prospects while systematically scaling daily spend on winning ad sets.')
        ],
        'why_us': (
            'Simply clicking "Boost Post" wastes money without building a repeatable sales system. We build structured Meta acquisition funnels '
            'that pair compelling human storytelling with accurate technical event tracking—giving Meta’s machine learning algorithm the exact '
            'conversion signals required to find your best customers.'
        ),
        'faqs': [
            ('Are Meta Instant Forms or website landing pages better for leads?', 'We test both approaches: Instant Forms generate higher lead volume at a lower cost, while dedicated landing pages often produce higher-intent prospects—we optimize for best overall sales ROI.'),
            ('Do you provide ad copywriting and creative direction?', 'Yes. We write all primary ad copy, headlines, and creative briefs tailored specifically for Instagram Reels, Stories, and Facebook Feeds.'),
            ('How often do you monitor and optimize Meta campaigns?', 'We monitor ad spend, frequency, click-through rates, and lead costs every 48 to 72 hours and provide comprehensive weekly reports.')
        ]
    },
    'web-development': {
        'title': 'Custom Web Development',
        'short_desc': 'Fast, secure, SEO-ready websites & web apps built with Python and Django.',
        'badge': 'Modern & Fast',
        'tagline': 'Fast, secure, and SEO-ready websites and web applications engineered with Python, Django & modern UI.',
        'overview': (
            'Your website is your digital headquarters—and often the very first impression a prospective client forms about your business. '
            'Slow-loading bloated templates, broken mobile layouts, and vulnerable third-party plugins silently cost businesses thousands in '
            'lost credibility and missed inquiries every month. Our Custom Web Development service delivers clean, high-performance websites '
            'and full-stack web applications built with Python, Django, HTML5, CSS3, and modern JavaScript. Whether you need a sleek personal '
            'portfolio and service platform, a custom lead-management portal, or a dynamic content website with an intuitive admin dashboard, '
            'we engineer solutions that load rapidly, look sharp on every screen size, and are structured from day one for technical SEO and security.'
        ),
        'features': [
            'Custom Business Websites, Portfolios & Full-Stack Web Applications',
            'Python & Django Backend Architecture with Custom Admin Dashboards',
            'Mobile-First Responsive UI with Modern Glassmorphism Design',
            'Core Web Vitals Speed Optimization & Clean Semantic HTML',
            'Enterprise-Grade Security Hardening, Git Workflow & Deployment'
        ],
        'deliverables': [
            ('Custom Responsive UI/UX Design', 'Mobile-first, accessible interfaces built with clean typography, modern visual hierarchy, and intuitive navigation that guides visitors to convert.'),
            ('Full-Stack Python & Django Backend', 'Robust, scalable server-side architecture featuring custom database models, authentication, Django Admin panels, and AJAX/API endpoints.'),
            ('Speed & Core Web Vitals Optimization', 'Lightweight assets, clean CSS/JS architecture, and semantic HTML engineered for fast load times and high Google PageSpeed scores.'),
            ('Security Hardening & Best Practices', 'Built-in protection against CSRF, XSS, and SQL injection vulnerabilities, secure environment configuration, and SSL/HTTPS deployment readiness.'),
            ('Technical SEO & Analytics Integration', 'Clean URL routing, dynamic meta titles/descriptions, semantic heading structures, and seamless integration with Google Analytics and contact forms.')
        ],
        'process': [
            ('1. Architecture & Wireframe Planning', 'We map out your page structure, user journeys, database models, and visual direction before writing production code.'),
            ('2. Frontend & Backend Development', 'We craft responsive templates alongside clean, modular Django views and models, sharing interactive progress previews throughout development.'),
            ('3. Cross-Device QA & Security Testing', 'Every form, interactive script, and database query is tested across mobile and desktop browsers for responsiveness, speed, and security.'),
            ('4. Deployment, Handover & Documentation', 'We push your codebase to GitHub, deploy to production hosting with SSL enabled, and provide clear guidance on managing content via the admin panel.')
        ],
        'why_us': (
            'Unlike developers who focus purely on code without understanding customer acquisition, we build websites with conversion rate '
            'optimization, lead capture, and search engine visibility baked directly into the architecture. You get a clean, maintainable '
            'Python/Django codebase that looks exceptional and actively drives business growth.'
        ),
        'faqs': [
            ('Will I be able to publish blog posts and update content myself?', 'Yes. Every Django website includes a secure, user-friendly Admin Panel where you can publish articles, manage inquiries, and update content without touching code.'),
            ('Are your websites mobile-friendly and optimized for Google SEO?', 'Absolutely. Every layout is engineered mobile-first and follows semantic HTML, fast loading, and clean URL best practices required by search engines.'),
            ('Do you provide post-launch support and GitHub version control?', 'Yes. Your entire project is cleanly structured on GitHub, and we provide post-launch support along with optional ongoing maintenance and feature upgrades.')
        ]
    }
}


def service_detail(request, slug):
    service = SERVICES_DATA.get(slug)
    if not service:
        raise Http404("Service not found")

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message_text = request.POST.get('message', '').strip()
        if name and email and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=f"[{service['title']} Inquiry] {message_text}"
            )
            notify_admin_email(
                f"New {service['title']} Inquiry from {name}",
                f"Service: {service['title']}\nName: {name}\nEmail: {email}\n\nMessage:\n{message_text}"
            )
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': f"Shukriya! {service['title']} ke liye aapki inquiry bhej di gayi hai."})
            messages.success(request, f"Shukriya! {service['title']} ke liye aapki inquiry bhej di gayi hai.")
            return redirect('service_detail', slug=slug)

    return render(request, 'blog/service_detail.html', {
        'service': service,
        'slug': slug,
        'all_services': SERVICES_DATA
    })