from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post, ContactMessage
from .forms import PostForm

# Saare blogs dikhane aur Contact Form handle karne ke liye
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        if name and email and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message_text
            )
            messages.success(request, 'Shukriya! Aapka message successfully bhej diya gaya hai.')
            return redirect('home')

    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})

# Ek single blog poora padhne ke liye
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# Naya blog create karne ke liye
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = User.objects.first()
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Naya Blog Likhein'})

# Blog edit karne ke liye
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

# Blog delete karne ke liye
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

# Har Service ka alag dedicated page dikhane ke liye
SERVICES_DATA = {
    'digital-marketing': {
        'title': 'Digital Marketing',
        'badge': 'Full-Stack Growth',
        'tagline': 'Data-driven online marketing strategies to grow your brand, traffic, and revenue.',
        'description': 'Hum aapke business ke liye complete digital marketing roadmap banate hain—social media presence se lekar brand awareness aur lead generation tak, taaki aapke competitors se aap hamesha aage rahein.',
        'features': [
            'Complete Brand Strategy & Online Positioning',
            'Content Marketing & Audience Engagement',
            'Conversion Rate Optimization (CRO)',
            'Monthly Performance & ROI Analytics Report'
        ]
    },
    'seo': {
        'title': 'SEO (Search Engine Optimization)',
        'badge': 'Organic Traffic',
        'tagline': 'Rank higher on Google search results and get consistent, high-intent organic leads.',
        'description': 'Search Engine Optimization se aapki website Google ke top results mein rank karti hai bina har click ke paise diye. Hum technical SEO, on-page optimization, aur high-authority backlinks par kaam karte hain.',
        'features': [
            'In-Depth Keyword Research & Competitor Audit',
            'On-Page & Technical SEO Fixes (Speed, Schema, Mobile)',
            'High-Quality Backlink Building & Local SEO',
            'Monthly Ranking & Organic Traffic Tracking'
        ]
    },
    'ppc': {
        'title': 'PPC Advertising',
        'badge': 'Instant Leads',
        'tagline': 'Maximize your return on ad spend with precision-targeted Pay-Per-Click campaigns.',
        'description': 'PPC campaigns aapko turant targeted customers tak pahunchate hain. Hum har click ki cost ko optimize karte hain taaki aapke budget ka maximum hissa real sales aur inquiries mein badle.',
        'features': [
            'High-Converting Ad Copy & Landing Page Strategy',
            'Smart Bid Management & Budget Optimization',
            'A/B Testing for Maximum Click-Through Rate (CTR)',
            'Detailed Conversion & ROAS Tracking'
        ]
    },
    'google-ads': {
        'title': 'Google Ads',
        'badge': 'Search & Display',
        'tagline': 'Capture customers actively searching for your products and services on Google.',
        'description': 'Google Search, Display, Shopping, aur YouTube Ads ke zariye hum aapke business ko un logon ke samne laate hain jo abhi kharidne ke liye search kar rahe hain.',
        'features': [
            'Search, Display & Performance Max Campaigns',
            'Negative Keyword Filtering to Stop Wasted Spend',
            'Conversion Tracking & Google Tag Manager Setup',
            'Weekly Campaign Optimization & Scaling'
        ]
    },
    'meta-ads': {
        'title': 'Meta Ads (Facebook & Instagram)',
        'badge': 'Social Scaling',
        'tagline': 'Reach your ideal audience on Facebook & Instagram with scroll-stopping ad campaigns.',
        'description': 'Meta Ads ke advanced audience targeting aur retargeting funnels se hum aapke brand ko sahi age, location, aur interest wale customers tak pahunchate hain.',
        'features': [
            'Custom & Lookalike Audience Targeting',
            'Engaging Ad Creatives & High-Impact Copywriting',
            'Meta Pixel Setup & Retargeting Funnels',
            'Lead Generation & E-commerce Sales Campaigns'
        ]
    },
    'web-development': {
        'title': 'Web Development',
        'badge': 'Modern & Fast',
        'tagline': 'Custom, fast, and mobile-responsive websites built with Python, Django & modern UI.',
        'description': 'Hum aapke business ke liye fast-loading, secure, aur SEO-friendly websites aur web applications banate hain—clean UI design aur strong backend ke saath.',
        'features': [
            'Custom Business Websites & Full-Stack Web Apps',
            'Python / Django Backend & Admin Dashboard',
            'Mobile-First Responsive & Modern Glass UI',
            'Speed Optimization, SSL Security & Deployment'
        ]
    }
}

def service_detail(request, slug):
    service = get_object_or_404(
        type('ServiceObj', (), {}) if slug not in SERVICES_DATA else [SERVICES_DATA[slug]][0]
    ) if slug not in SERVICES_DATA else SERVICES_DATA[slug]

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')
        if name and email and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=f"[{service['title']} Inquiry] {message_text}"
            )
            messages.success(request, f"Shukriya! {service['title']} ke liye aapki inquiry bhej di gayi hai.")
            return redirect('service_detail', slug=slug)

    return render(request, 'blog/service_detail.html', {
        'service': service,
        'slug': slug,
        'all_services': SERVICES_DATA
    })    