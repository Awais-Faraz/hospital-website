#!/usr/bin/env python3
"""
Hospital website generator.
1. Edit config.json (name, city, phone, domain ...).
2. Run:  python build.py
All HTML pages, sitemap.xml, robots.txt, manifest and logo files are regenerated.
"""
import json, os, datetime, html

ROOT = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
TODAY = datetime.date.today().isoformat()
E = html.escape
NAME, CITY, DOMAIN = C["name"], C["city"], C["domain"].rstrip("/")

# ---------------------------------------------------------------- data
ICONS = {
    "cardiology": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    "orthopedics": '<path d="M6 4a2 2 0 1 1 3 2l9 9a2 2 0 1 1-2 3L7 9a2 2 0 0 1-1-5z"/>',
    "pediatrics": '<circle cx="12" cy="8" r="4"/><path d="M5 21c0-4 3-6 7-6s7 2 7 6"/>',
    "gynecology": '<circle cx="12" cy="9" r="5"/><path d="M12 14v7M9 18h6"/>',
    "neurology": '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 4 3 3 0 0 0 2 4 3 3 0 0 0 4 3V4zM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 4 3 3 0 0 1-2 4 3 3 0 0 1-4 3V4z"/>',
    "emergency-care": '<path d="M12 4v16M4 12h16"/><circle cx="12" cy="12" r="9"/>',
}

DEPTS = [
    dict(slug="cardiology", name="Cardiology (Heart Care)", short="Heart care",
         blurb="Diagnosis and treatment of heart and blood-pressure problems, from ECG and echo to long-term follow-up.",
         intro="Our cardiology team looks after adults with chest pain, high blood pressure, heart failure, rhythm problems and coronary artery disease. Tests are done in-house so you do not have to run between labs.",
         treats=["Chest pain and angina", "High blood pressure", "Heart failure", "Irregular heartbeat (arrhythmia)", "Coronary artery disease", "Post heart-attack follow-up"],
         tests=["ECG and exercise stress test", "Echocardiography", "Holter (24-hour) monitoring", "Cardiac blood tests"],
         see="Chest pressure or pain, breathlessness on mild effort, fainting, a racing or very slow heartbeat, or swelling in both legs.",
         faq=[("Can I get an ECG without an appointment?", "Yes. ECG is available during OPD hours and 24/7 in the emergency department."),
              ("Do I need a referral to see a cardiologist?", "No referral is needed. Bring any previous reports and a list of your medicines.")]),
    dict(slug="orthopedics", name="Orthopedics (Bones & Joints)", short="Bones and joints",
         blurb="Fractures, joint pain, sports injuries and joint replacement, with in-house X-ray and physiotherapy.",
         intro="Orthopedic surgeons and physiotherapists work together so that treatment does not stop at the operating table. We treat injuries, arthritis, spine and joint problems for all ages.",
         treats=["Fractures and dislocations", "Knee and hip pain", "Arthritis", "Back and neck pain", "Sports injuries", "Joint replacement surgery"],
         tests=["Digital X-ray", "Ultrasound", "MRI referral", "Physiotherapy assessment"],
         see="Pain that lasts more than two weeks, a joint that swells or locks, a limb you cannot put weight on, or visible deformity after an injury.",
         faq=[("Is physiotherapy available at the hospital?", "Yes. A physiotherapist can start your rehabilitation plan before and after surgery."),
              ("When is surgery really needed?", "Many problems improve with medicines, exercise and physiotherapy. Your surgeon will explain all options before recommending surgery.")]),
    dict(slug="pediatrics", name="Pediatrics (Child Care)", short="Child care",
         blurb="Newborn care, vaccinations, fever, infections and growth checks for children from birth to 16 years.",
         intro="Children are not small adults, and our pediatricians treat them that way. A child-friendly OPD, a neonatal unit and a full vaccination service are available under one roof.",
         treats=["Fever, cough and infections", "Newborn and premature baby care", "Vaccination (EPI and optional)", "Growth and nutrition problems", "Asthma and allergies", "Diarrhea and dehydration"],
         tests=["Newborn screening", "Blood and urine tests", "Chest X-ray", "Oxygen and nebulizer therapy"],
         see="Fever in a baby under 3 months, fast or difficult breathing, repeated vomiting, a rash that does not fade, or a child who is unusually sleepy.",
         faq=[("Which vaccines are available?", "All routine childhood vaccines as per the national schedule, plus optional vaccines. Ask our pediatric desk for the current list."),
              ("Can parents stay with the child?", "Yes. One parent can stay with the child in the ward.")]),
    dict(slug="gynecology", name="Gynecology & Obstetrics", short="Women's health and maternity",
         blurb="Pregnancy care, safe delivery, and women's health from adolescence to menopause.",
         intro="From your first antenatal visit to delivery and postnatal care, our gynecologists and midwives follow your pregnancy closely. We also treat period problems, fertility concerns and menopause symptoms.",
         treats=["Antenatal and postnatal care", "Normal and C-section delivery", "Irregular or painful periods", "Fertility assessment", "PCOS", "Menopause care"],
         tests=["Pregnancy ultrasound", "Fetal monitoring", "Pap smear", "Hormone profile"],
         see="Missed period with pain, bleeding during pregnancy, reduced baby movements, very heavy periods, or pelvic pain.",
         faq=[("Do you have female doctors?", "Yes. Female gynecologists and midwives are available during OPD and for deliveries."),
              ("Should I register early in pregnancy?", "Yes. Early registration lets us plan scans and tests at the right time.")]),
    dict(slug="neurology", name="Neurology (Brain & Nerves)", short="Brain and nerves",
         blurb="Headache, stroke, epilepsy, nerve problems and memory concerns, assessed by specialist neurologists.",
         intro="Neurological symptoms can be frightening. Our neurologists take time to listen, examine and explain, and arrange the right scans and nerve tests without delay.",
         treats=["Migraine and chronic headache", "Stroke and stroke recovery", "Epilepsy and seizures", "Numbness and nerve pain", "Parkinson's disease", "Memory problems"],
         tests=["EEG", "Nerve conduction study (NCS/EMG)", "CT scan", "MRI referral"],
         see="Sudden weakness on one side, face drooping, speech difficulty, a seizure, or the worst headache of your life. These need emergency care now.",
         faq=[("What are the signs of stroke?", "Face drooping, arm weakness, speech difficulty. Go to the emergency department immediately, time matters."),
              ("Is EEG available?", "Yes, EEG is available by appointment during OPD hours.")]),
    dict(slug="emergency-care", name="Emergency & Trauma Care", short="Open 24/7",
         blurb="Doctors, nurses, ambulance and lab on duty around the clock, every day of the year.",
         intro="Our emergency department never closes. Patients are triaged on arrival so the most serious cases are seen first, and a senior doctor is on call at all times.",
         treats=["Heart attack and stroke", "Road traffic injuries", "Burns and fractures", "Severe breathing difficulty", "Poisoning", "High fever and dehydration"],
         tests=["24/7 laboratory", "24/7 X-ray and ultrasound", "CT scan", "ECG and oxygen support"],
         see="Chest pain, trouble breathing, heavy bleeding, loss of consciousness, severe injury or any condition you believe is life-threatening.",
         faq=[("Do you have an ambulance?", "Yes. Call the emergency number shown on this page and tell us your location."),
              ("Do I need an appointment for emergency?", "No. Come straight to the emergency entrance at any hour.")]),
]

DOCTORS = [
    ("Dr. Ahmed Raza", "Consultant Cardiologist", "MBBS, FCPS (Cardiology)", "cardiology", "15 years"),
    ("Dr. Sana Malik", "Consultant Gynecologist", "MBBS, FCPS (Gynecology)", "gynecology", "12 years"),
    ("Dr. Usman Tariq", "Orthopedic Surgeon", "MBBS, FCPS (Orthopedics)", "orthopedics", "14 years"),
    ("Dr. Hina Farooq", "Consultant Pediatrician", "MBBS, FCPS (Pediatrics)", "pediatrics", "10 years"),
    ("Dr. Bilal Hussain", "Consultant Neurologist", "MBBS, FCPS (Neurology)", "neurology", "11 years"),
    ("Dr. Ayesha Khan", "Emergency Physician", "MBBS, MRCEM", "emergency-care", "9 years"),
]

POSTS = [
    dict(slug="heart-attack-warning-signs", title="Heart attack warning signs and when to go to the ER",
         desc="Learn the common and less obvious signs of a heart attack, and what to do in the first minutes.",
         dept="cardiology", date="2026-10-05",
         body="""<p>A heart attack happens when blood flow to part of the heart is blocked. Treatment works best when it starts early, so knowing the signs can save a life.</p>
<h2>Common warning signs</h2>
<ul class="ticks"><li>Pressure, tightness or heaviness in the centre of the chest</li><li>Pain spreading to the left arm, jaw, neck or back</li><li>Shortness of breath</li><li>Cold sweat, nausea or light-headedness</li></ul>
<h2>Signs that are easy to miss</h2>
<p>Women, older adults and people with diabetes may have less typical symptoms, such as unusual tiredness, indigestion-like discomfort, or pain in the back or jaw without chest pain.</p>
<h2>What to do</h2>
<ul class="ticks"><li>Call the emergency number or an ambulance straight away.</li><li>Do not drive yourself. Sit down and stay calm.</li><li>Take aspirin only if a doctor has told you it is safe for you.</li><li>Tell the team when symptoms started.</li></ul>
<h2>Lower your risk</h2>
<p>Control blood pressure and sugar, stop smoking, stay active, eat less salt and fried food, and have regular check-ups after the age of 40.</p>"""),
    dict(slug="fever-in-children-when-to-see-a-doctor", title="Fever in children: when to see a doctor",
         desc="A simple guide for parents: which fevers can be managed at home and which need a doctor the same day.",
         dept="pediatrics", date="2026-10-18",
         body="""<p>Fever is the body's way of fighting infection. The number on the thermometer matters less than how your child looks and behaves.</p>
<h2>See a doctor immediately if</h2>
<ul class="ticks"><li>Your baby is under 3 months and has a temperature of 38°C (100.4°F) or higher</li><li>Your child is breathing fast or with difficulty</li><li>There is a stiff neck, a seizure, or a rash that does not fade when pressed</li><li>Your child is very sleepy, hard to wake, or not drinking</li></ul>
<h2>Book a visit if</h2>
<ul class="ticks"><li>Fever lasts more than 3 days</li><li>There are signs of dehydration: dry mouth, no tears, fewer wet nappies</li><li>Your child has an ear, throat or urine complaint</li></ul>
<h2>Care at home</h2>
<p>Offer plenty of fluids, dress your child in light clothes and let them rest. Use fever medicine only in the dose advised by your doctor or pharmacist for your child's weight. Do not give aspirin to children.</p>"""),
    dict(slug="knee-pain-causes-and-treatment", title="Knee pain: causes and when to see a doctor",
         desc="Understand the most common causes of knee pain, simple self-care steps, and warning signs that need a specialist.",
         dept="orthopedics", date="2026-11-02",
         body="""<p>Knee pain affects people of all ages. It can come from an injury, overuse or long-term wear of the joint.</p>
<h2>Common causes</h2>
<ul class="ticks"><li>Osteoarthritis (wear of the joint cartilage)</li><li>Ligament injuries, such as an ACL tear</li><li>Meniscus tears</li><li>Tendon problems and bursitis</li></ul>
<h2>Simple self-care for mild pain</h2>
<p>Rest the knee, apply a cold pack for 15 minutes at a time, use a supportive bandage, and raise the leg when sitting. Gentle strengthening exercises often help once the pain settles.</p>
<h2>See an orthopedic doctor if</h2>
<ul class="ticks"><li>You cannot put weight on the leg</li><li>The knee looks deformed, is locked, or gives way</li><li>Swelling comes with fever or redness</li><li>Pain continues for more than two weeks</li></ul>"""),
]

FAQS = [
    ("What are your emergency and OPD timings?", f"{C['hours']}. {C['opd_hours']}."),
    ("How can I book an appointment?", "Use the booking form on this website, call us, or send a WhatsApp message. We will confirm your slot by phone."),
    ("Do you accept insurance and panel cards?", "Yes. We work with several insurance companies and corporate panels. Please call our reception desk to confirm yours."),
    ("Can I get my lab reports online?", "Yes. Reports can be collected from the lab or sent to you by WhatsApp or email."),
    ("Is parking available?", "Yes. Free parking is available for patients and visitors."),
    ("What should I bring to my first visit?", "Your CNIC, previous reports, a list of current medicines, and your insurance card if you have one."),
]

NAV = [("index.html", "Home"), ("about.html", "About"), ("departments.html", "Departments"),
       ("doctors.html", "Doctors"), ("blog/index.html", "Health Blog"), ("contact.html", "Contact")]

# ---------------------------------------------------------------- helpers
def esc(s): return E(s, quote=True)

def jsonld(d): return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"

def logo_svg(size=38):
    return ('<svg viewBox="0 0 48 48" width="%d" height="%d" aria-hidden="true" focusable="false">'
            '<rect width="48" height="48" rx="12" fill="#0f6b73"/><path d="M20 10h8v10h10v8H28v10h-8V28H10v-8h10z" fill="#fff"/></svg>' % (size, size))

def hospital_schema():
    return {
        "@context": "https://schema.org", "@type": ["Hospital", "MedicalOrganization"], "@id": DOMAIN + "/#hospital",
        "name": NAME, "url": DOMAIN + "/", "logo": DOMAIN + "/assets/img/logo.svg", "image": DOMAIN + "/assets/img/og-image.png",
        "telephone": C["phone_raw"], "email": C["email"], "priceRange": "$$", "isAcceptingNewPatients": True,
        "address": {"@type": "PostalAddress", "streetAddress": C["address"], "addressLocality": CITY,
                    "postalCode": C["postcode"], "addressCountry": "PK"},
        "geo": {"@type": "GeoCoordinates", "latitude": C["lat"], "longitude": C["lng"]},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00", "closes": "23:59"}],
        "sameAs": [C["facebook"], C["instagram"], C["youtube"]],
        "availableService": [{"@type": "MedicalProcedure", "name": d["name"]} for d in DEPTS],
        "medicalSpecialty": ["Cardiovascular", "Orthopedic", "Pediatric", "Gynecologic", "Neurologic", "Emergency"],
    }

def breadcrumb(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + "/" + p} for i, (n, p) in enumerate(items)]}

def page(path, title, desc, body, schemas=(), crumbs=None, og_type="website", hero=False):
    depth = path.count("/")
    r = "../" * depth
    nav = "".join('<li><a href="%s%s"%s>%s</a></li>' % (r, h, ' aria-current="page"' if h == path else "", n) for h, n in NAV)
    nav += '<li><a class="cta" href="%sappointment.html">Book appointment</a></li>' % r
    canon = DOMAIN + "/" + ("" if path == "index.html" else path)
    sch = [hospital_schema()] if path == "index.html" else []
    sch += list(schemas)
    if crumbs: sch.append(breadcrumb(crumbs))
    crumb_html = ""
    if crumbs:
        parts = []
        for i, (n, p) in enumerate(crumbs):
            parts.append(esc(n) if i == len(crumbs) - 1 else '<a href="%s%s">%s</a>' % (r, p, esc(n)))
        crumb_html = '<nav class="crumbs wrap" aria-label="Breadcrumb">' + " / ".join(parts) + "</nav>"
    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#0f6b73">
<meta name="geo.region" content="PK"><meta name="geo.placename" content="{esc(CITY)}">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{esc(NAME)}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{DOMAIN}/assets/img/og-image.png">
<meta property="og:locale" content="en_PK">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.png">
<link rel="icon" href="{r}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{r}assets/img/apple-touch-icon.png">
<link rel="manifest" href="{r}manifest.webmanifest">
<link rel="preload" href="{r}assets/css/style.css" as="style">
<link rel="stylesheet" href="{r}assets/css/style.css">
{"".join(jsonld(s) for s in sch)}
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<div class="strip"><div class="wrap"><span>Emergency department open 24/7</span><span>Emergency: <a href="tel:{C['emergency_raw']}">{C['emergency']}</a> &nbsp;|&nbsp; Appointments: <a href="tel:{C['phone_raw']}">{C['phone']}</a></span></div></div>
<header class="site-head"><div class="wrap">
<a class="brand" href="{r}index.html" aria-label="{esc(NAME)} home">{logo_svg()}<span>{esc(NAME)}</span></a>
<button class="menu-btn" aria-expanded="false" aria-controls="site-nav">Menu</button>
<nav id="site-nav" aria-label="Main"><ul>{nav}</ul></nav>
</div></header>
<main id="main">
{crumb_html if not hero else ""}
"""
    foot = f"""
</main>
<footer><div class="wrap">
<div class="fgrid">
<div><h3>{esc(NAME)}</h3><p>Trusted multi-specialty hospital in {esc(CITY)}, Pakistan. Specialist doctors, modern diagnostics and emergency care, every day.</p></div>
<div><h3>Departments</h3><ul>{"".join('<li><a href="%sdepartments/%s.html">%s</a></li>' % (r, d["slug"], esc(d["name"])) for d in DEPTS)}</ul></div>
<div><h3>Quick links</h3><ul><li><a href="{r}about.html">About us</a></li><li><a href="{r}doctors.html">Our doctors</a></li><li><a href="{r}appointment.html">Book appointment</a></li><li><a href="{r}faq.html">FAQs</a></li><li><a href="{r}blog/index.html">Health blog</a></li><li><a href="{r}privacy-policy.html">Privacy policy</a></li></ul></div>
<div><h3>Contact</h3>
<address style="font-style:normal"><p>{esc(C['address'])}, {esc(CITY)}<br>{esc(C['country'])}</p>
<p>Phone: <a href="tel:{C['phone_raw']}">{C['phone']}</a><br>Emergency: <a href="tel:{C['emergency_raw']}">{C['emergency']}</a><br>Email: <a href="mailto:{C['email']}">{C['email']}</a></p></address>
<p><a href="{C['facebook']}" rel="noopener me" target="_blank">Facebook</a> &middot; <a href="{C['instagram']}" rel="noopener me" target="_blank">Instagram</a> &middot; <a href="{C['youtube']}" rel="noopener me" target="_blank">YouTube</a></p></div>
</div>
<div class="copy">&copy; <span id="yr">2026</span> {esc(NAME)}. All rights reserved. This website gives general information and does not replace a doctor's advice. In an emergency call {C['emergency']}.</div>
</div></footer>
<a class="wa" href="https://wa.me/{C['whatsapp_raw']}" target="_blank" rel="noopener">WhatsApp us</a>
<script src="{r}assets/js/main.js" defer></script>
</body></html>"""
    full = head + body + foot
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(full)
    return canon

def dept_options():
    return "".join('<option value="%s">%s</option>' % (esc(d["name"]), esc(d["name"])) for d in DEPTS) + '<option value="Not sure">Not sure, please advise</option>'

def booking_form(full=False):
    extra = '<label for="date">Preferred date</label><input id="date" name="date" type="date">'
    if full:
        extra += '<label for="message">Your concern (optional)</label><textarea id="message" name="message" rows="3"></textarea>'
    return f"""<form data-appointment data-wa="{C['whatsapp_raw']}">
<label for="name">Full name</label><input id="name" name="name" required autocomplete="name">
<label for="phone">Mobile number</label><input id="phone" name="phone" type="tel" required autocomplete="tel" placeholder="03XX XXXXXXX">
<label for="department">Department</label><select id="department" name="department">{dept_options()}</select>
{extra}
<button class="btn" type="submit">Send request on WhatsApp</button>
<p style="font-size:.85rem;color:var(--muted);margin:10px 0 0">We will call you to confirm the time. For emergencies call {C['emergency']}.</p>
</form>"""

def ico(slug):
    return '<span class="ico"><svg viewBox="0 0 24 24" aria-hidden="true">%s</svg></span>' % ICONS[slug]

def cta_band():
    return f"""<section class="cta-band"><div class="wrap split" style="align-items:center">
<div><h2>Need to see a specialist?</h2><p>Book online in a minute, or call our reception. Emergency care needs no appointment.</p></div>
<div class="btns"><a class="btn alt2" href="appointment.html">Book appointment</a><a class="btn red" href="tel:{C['emergency_raw']}">Call emergency</a></div></div></section>"""

def fix_links(body, depth):
    """body templates use relative links written for root level; prefix for sub folders."""
    if depth == 0: return body
    pre = "../" * depth
    for key in ('href="', 'src="'):
        body = body.replace(key + "appointment.html", key + pre + "appointment.html")
    return body

# ---------------------------------------------------------------- pages
urls = []

# HOME
ecg = '<svg class="ecg" viewBox="0 0 1200 90" preserveAspectRatio="none" aria-hidden="true"><path d="M0 50 H300 L330 50 L350 20 L375 80 L395 8 L420 62 L440 50 H700 L725 50 L745 28 L768 72 L790 50 H1200"/></svg>'
dept_cards = "".join(f'<a class="card" href="departments/{d["slug"]}.html">{ico(d["slug"])}<h3>{esc(d["name"])}</h3><p>{esc(d["blurb"])}</p><span class="more">Learn more</span></a>' for d in DEPTS)
doc_cards = "".join(f'<div class="card doc"><div class="avatar" aria-hidden="true">{"".join(w[0] for w in n.replace("Dr. ","").split()[:2])}</div><h3>{esc(n)}</h3><p><strong>{esc(t)}</strong></p><small>{esc(q)}</small><small>{esc(e)} experience</small></div>' for n, t, q, s, e in DOCTORS[:3])
blog_cards = "".join(f'<a class="card" href="blog/{p["slug"]}.html"><p class="meta">{p["date"]}</p><h3>{esc(p["title"])}</h3><p>{esc(p["desc"])}</p><span class="more">Read article</span></a>' for p in POSTS)
faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in FAQS[:4])

home = f"""
<section class="hero"><div class="wrap">
<div class="hero-grid">
<div>
<h1>Specialist care and 24/7 emergency services in {esc(CITY)}</h1>
<p class="lead">{esc(NAME)} brings experienced doctors, modern diagnostics and caring nurses together, so you get clear answers and fast treatment.</p>
<div class="btns"><a class="btn" href="appointment.html">Book appointment</a><a class="btn red" href="tel:{C['emergency_raw']}">Emergency: {C['emergency']}</a><a class="btn alt2" href="departments.html">Find a department</a></div>
</div>
<div class="book" id="book"><h2>Request an appointment</h2>{booking_form()}</div>
</div>
{ecg}
<div class="facts">
<div><strong>24/7</strong>Emergency and laboratory</div>
<div><strong>{C['doctors_count']}</strong>Consultants and doctors</div>
<div><strong>{C['beds']}</strong>Patient beds</div>
<div><strong>Since {C['founded']}</strong>Serving {esc(CITY)}</div>
</div></div></section>

<section><div class="wrap">
<h2>Our departments</h2>
<p class="lead">Six core specialties under one roof, with in-house lab, imaging and pharmacy.</p>
<div class="grid">{dept_cards}</div>
</div></section>

<section class="alt"><div class="wrap split">
<div><h2>Why patients choose {esc(NAME)}</h2>
<ul class="ticks"><li>Senior consultants see you personally, not only juniors</li><li>Emergency, X-ray, ultrasound and lab open round the clock</li><li>Clear estimates before treatment, with panel and insurance support</li><li>Female doctors and a private, respectful environment</li><li>Free parking and wheelchair access</li></ul>
<a class="btn" href="about.html">About our hospital</a></div>
<div><h2>How your visit works</h2>
<ol class="steps">
<li><strong>Book</strong>Send the form, call us or message on WhatsApp.</li>
<li><strong>Arrive and register</strong>Bring your CNIC and previous reports. Our desk guides you to the doctor.</li>
<li><strong>Consult and test</strong>Your doctor examines you and orders tests, which are done in the same building.</li>
<li><strong>Treatment and follow-up</strong>You receive a clear plan, reports on WhatsApp or email, and a follow-up date.</li>
</ol></div>
</div></section>

<section><div class="wrap"><h2>Meet our doctors</h2><p class="lead">Qualified, experienced and easy to talk to.</p>
<div class="grid">{doc_cards}</div><p style="margin-top:22px"><a class="btn alt2" href="doctors.html">See all doctors</a></p></div></section>

<section class="alt"><div class="wrap"><h2>From our health blog</h2><div class="grid">{blog_cards}</div></div></section>

<section><div class="wrap split"><div><h2>Common questions</h2>{faq_html}<p><a href="faq.html">Read all FAQs</a></p></div>
<div><h2>Find us</h2><div class="map-box"><div><p><strong>{esc(NAME)}</strong><br>{esc(C['address'])}, {esc(CITY)}</p><a class="btn" href="{C['google_maps_link']}" target="_blank" rel="noopener">Open in Google Maps</a></div></div></div></div></section>
{cta_band()}
"""
urls.append(page("index.html", f"{NAME} | 24/7 Emergency & Specialists in {CITY}",
                 f"{NAME} in {CITY}: specialist doctors, 24/7 emergency, cardiology, orthopedics, pediatrics, gynecology. Book online.",
                 home, hero=True))

# ABOUT
about = f"""
<div class="pagehead"><div class="wrap"><h1>About {esc(NAME)}</h1><p class="lead">A hospital built around one idea: people should understand their own treatment.</p></div></div>
<section><div class="wrap split"><div>
<h2>Our story</h2>
<p>{esc(NAME)} opened in {C['founded']} with a small outpatient clinic in {esc(CITY)}. Today we are a {C['beds']}-bed multi-specialty hospital with an emergency department, operation theatres, a modern laboratory and imaging services.</p>
<p>We keep the same promise we started with: honest advice, fair pricing and respect for every patient.</p>
<h2>Our mission</h2><p>To provide safe, affordable and compassionate healthcare for families in {esc(CITY)} and the surrounding districts.</p>
</div><div><h2>What we stand for</h2>
<ul class="ticks"><li><strong>Safety first:</strong> infection control, patient identification and checklists in every ward</li><li><strong>Clear communication:</strong> your doctor explains the diagnosis and options in simple language</li><li><strong>Fair cost:</strong> estimates are shared before major procedures</li><li><strong>Privacy:</strong> your records are kept confidential</li></ul>
<h2>Facilities</h2><ul class="ticks"><li>24/7 emergency and ambulance</li><li>ICU, CCU and neonatal unit</li><li>Operation theatres</li><li>Laboratory, X-ray, ultrasound, CT scan</li><li>In-house pharmacy and physiotherapy</li></ul></div></div></section>
{cta_band()}"""
urls.append(page("about.html", f"About {NAME} | Hospital in {CITY}", f"Learn about {NAME}, our mission, facilities and the team behind our multi-specialty hospital in {CITY}.",
                 about, crumbs=[("Home", "index.html"), ("About", "about.html")]))

# DEPARTMENTS LIST
dep_body = f"""<div class="pagehead"><div class="wrap"><h1>Hospital departments in {esc(CITY)}</h1><p class="lead">Choose a specialty to see what we treat, which tests are available and when to book.</p></div></div>
<section><div class="wrap"><div class="grid">{dept_cards}</div></div></section>{cta_band()}"""
urls.append(page("departments.html", f"Departments & Specialties | {NAME}", f"Cardiology, orthopedics, pediatrics, gynecology, neurology and 24/7 emergency care at {NAME}, {CITY}.",
                 dep_body, crumbs=[("Home", "index.html"), ("Departments", "departments.html")]))

# DEPARTMENT PAGES
for d in DEPTS:
    others = "".join(f'<a class="card" href="{o["slug"]}.html">{ico(o["slug"])}<h3>{esc(o["name"])}</h3><p>{esc(o["short"])}</p></a>' for o in DEPTS if o["slug"] != d["slug"])
    body = f"""<div class="pagehead"><div class="wrap"><h1>{esc(d['name'])} in {esc(CITY)}</h1><p class="lead">{esc(d['blurb'])}</p>
<div class="btns"><a class="btn" href="../appointment.html">Book appointment</a><a class="btn red" href="tel:{C['emergency_raw']}">Emergency: {C['emergency']}</a></div></div></div>
<section><div class="wrap split"><div>
<h2>About this department</h2><p>{esc(d['intro'])}</p>
<h2>Conditions we treat</h2><ul class="ticks">{"".join(f"<li>{esc(t)}</li>" for t in d['treats'])}</ul>
<h2>Tests and services</h2><ul class="ticks">{"".join(f"<li>{esc(t)}</li>" for t in d['tests'])}</ul>
</div><div>
<div class="note"><strong>When to see a doctor:</strong> {esc(d['see'])}</div>
<h2>Frequently asked questions</h2>{"".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in d['faq'])}
<div class="book" style="margin-top:24px"><h2>Book now</h2>{booking_form()}</div>
</div></div></section>
<section class="alt"><div class="wrap"><h2>Other departments</h2><div class="grid">{others}</div></div></section>"""
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]}
    urls.append(page(f"departments/{d['slug']}.html", f"{d['name']} in {CITY} | {NAME}"[:70],
                     f"{d['name']} at {NAME}, {CITY}. Expert specialists and modern tests. Book an appointment today.", body, schemas=[fq],
                     crumbs=[("Home", "index.html"), ("Departments", "departments.html"), (d["name"], f"departments/{d['slug']}.html")]))

# DOCTORS
slug2name = {d["slug"]: d["name"] for d in DEPTS}
doc_all = "".join(f'<div class="card doc"><div class="avatar" aria-hidden="true">{"".join(w[0] for w in n.replace("Dr. ","").split()[:2])}</div><h3>{esc(n)}</h3><p><strong>{esc(t)}</strong></p><small>{esc(q)}</small><small>{esc(e)} experience</small><p style="margin-top:10px"><a href="departments/{s}.html">{esc(slug2name[s])}</a></p></div>' for n, t, q, s, e in DOCTORS)
doc_body = f"""<div class="pagehead"><div class="wrap"><h1>Our doctors</h1><p class="lead">Specialists who listen first and explain clearly.</p></div></div>
<section><div class="wrap"><div class="grid">{doc_all}</div></div></section>{cta_band()}"""
urls.append(page("doctors.html", f"Best Doctors & Consultants in {CITY} | {NAME}", f"Meet the specialist doctors at {NAME}, {CITY}: cardiologist, gynecologist, orthopedic surgeon, pediatrician and neurologist.",
                 doc_body, crumbs=[("Home", "index.html"), ("Doctors", "doctors.html")]))

# APPOINTMENT
app_body = f"""<div class="pagehead"><div class="wrap"><h1>Book an appointment</h1><p class="lead">Fill in the form. We will confirm your time by phone.</p></div></div>
<section><div class="wrap split"><div class="book"><h2>Appointment request</h2>{booking_form(True)}</div>
<div><h2>Prefer to call?</h2><p>Appointments: <a href="tel:{C['phone_raw']}">{C['phone']}</a><br>{esc(C['opd_hours'])}</p>
<div class="note"><strong>Emergency?</strong> Do not wait for an appointment. Call <a href="tel:{C['emergency_raw']}">{C['emergency']}</a> or come to the emergency entrance. We are open 24/7.</div>
<h2>Bring with you</h2><ul class="ticks"><li>CNIC</li><li>Previous reports and prescriptions</li><li>List of medicines you take</li><li>Insurance or panel card</li></ul></div></div></section>"""
urls.append(page("appointment.html", f"Book Doctor Appointment Online | {NAME}, {CITY}"[:70], f"Book a doctor appointment at {NAME} in {CITY}. Send your request online or on WhatsApp and we will confirm by phone.",
                 app_body, crumbs=[("Home", "index.html"), ("Book appointment", "appointment.html")]))

# CONTACT
contact_body = f"""<div class="pagehead"><div class="wrap"><h1>Contact {esc(NAME)}</h1><p class="lead">We are here for you, day and night.</p></div></div>
<section><div class="wrap split"><div>
<h2>Hospital details</h2>
<address style="font-style:normal"><p><strong>Address</strong><br>{esc(C['address'])}, {esc(CITY)}, {esc(C['country'])}</p>
<p><strong>Appointments</strong><br><a href="tel:{C['phone_raw']}">{C['phone']}</a></p>
<p><strong>Emergency (24/7)</strong><br><a href="tel:{C['emergency_raw']}">{C['emergency']}</a></p>
<p><strong>Email</strong><br><a href="mailto:{C['email']}">{C['email']}</a></p>
<p><strong>Hours</strong><br>{esc(C['hours'])}<br>{esc(C['opd_hours'])}</p></address>
<a class="btn" href="{C['google_maps_link']}" target="_blank" rel="noopener">Get directions</a></div>
<div><h2>Send us a message</h2><div class="book">{booking_form(True)}</div></div></div></section>
<section class="alt"><div class="wrap"><h2>Map</h2><div class="map-box"><div><p>Replace this box with your Google Maps embed (see README).</p><a class="btn" href="{C['google_maps_link']}" target="_blank" rel="noopener">Open map</a></div></div></div></section>"""
contact_schema = {"@context": "https://schema.org", "@type": "ContactPage", "name": f"Contact {NAME}", "url": DOMAIN + "/contact.html"}
urls.append(page("contact.html", f"Contact {NAME} | Phone, Address & Emergency Number", f"Contact {NAME} in {CITY}. Emergency {C['emergency']}, appointments {C['phone']}, address, email and directions.",
                 contact_body, schemas=[contact_schema], crumbs=[("Home", "index.html"), ("Contact", "contact.html")]))

# FAQ
faq_all = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in FAQS)
faq_body = f"""<div class="pagehead"><div class="wrap"><h1>Frequently asked questions</h1></div></div><section><div class="wrap">{faq_all}</div></section>{cta_band()}"""
faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
urls.append(page("faq.html", f"Hospital FAQs: Timings, Appointments, Insurance | {NAME}"[:70], f"Answers to common questions about timings, appointments, insurance, reports and parking at {NAME}, {CITY}.",
                 faq_body, schemas=[faq_schema], crumbs=[("Home", "index.html"), ("FAQs", "faq.html")]))

# BLOG INDEX + POSTS
blog_idx = f"""<div class="pagehead"><div class="wrap"><h1>Health blog</h1><p class="lead">Practical health advice from our doctors.</p></div></div><section><div class="wrap"><div class="grid">{"".join(f'<a class="card" href="{p["slug"]}.html"><p class="meta">{p["date"]}</p><h3>{esc(p["title"])}</h3><p>{esc(p["desc"])}</p><span class="more">Read article</span></a>' for p in POSTS)}</div></div></section>"""
urls.append(page("blog/index.html", f"Health Blog & Medical Tips | {NAME}", f"Health articles from the doctors of {NAME}, {CITY}: heart health, child care, bones and joints.",
                 blog_idx, crumbs=[("Home", "index.html"), ("Health blog", "blog/index.html")]))
for p in POSTS:
    art = {"@context": "https://schema.org", "@type": "Article", "headline": p["title"], "description": p["desc"],
           "datePublished": p["date"], "dateModified": TODAY, "image": DOMAIN + "/assets/img/og-image.png",
           "author": {"@type": "Organization", "name": NAME}, "publisher": {"@type": "Organization", "name": NAME,
           "logo": {"@type": "ImageObject", "url": DOMAIN + "/assets/img/logo.svg"}},
           "mainEntityOfPage": DOMAIN + f"/blog/{p['slug']}.html"}
    body = f"""<div class="pagehead"><div class="wrap"><h1>{esc(p['title'])}</h1><p class="meta">Published {p['date']} &middot; {esc(NAME)} medical team</p></div></div>
<section><div class="wrap"><article class="post">{p['body']}
<div class="note">This article is for general information only. It does not replace a medical examination. In an emergency call {C['emergency']}.</div>
<p>Related department: <a href="../departments/{p['dept']}.html">{esc(slug2name[p['dept']])}</a></p>
<p><a class="btn" href="../appointment.html">Book appointment</a></p></article></div></section>"""
    urls.append(page(f"blog/{p['slug']}.html", p["title"] + " | " + C["short"], p["desc"], body, schemas=[art], og_type="article",
                     crumbs=[("Home", "index.html"), ("Health blog", "blog/index.html"), (p["title"], f"blog/{p['slug']}.html")]))

# PRIVACY
priv = f"""<div class="pagehead"><div class="wrap"><h1>Privacy policy</h1></div></div><section><div class="wrap"><article class="post">
<p>{esc(NAME)} respects your privacy. This page explains how information entered on this website is used.</p>
<h2>Information we collect</h2><p>When you send an appointment request we receive your name, phone number, preferred date and message. This information is sent through WhatsApp or the channel you choose.</p>
<h2>How we use it</h2><p>We use it only to contact you about your appointment or enquiry. We do not sell your information.</p>
<h2>Medical records</h2><p>Patient records are kept confidential and shared only with your care team or when required by law.</p>
<h2>Contact</h2><p>Questions about privacy: <a href="mailto:{C['email']}">{C['email']}</a>.</p>
<p class="meta">Last updated: {TODAY}</p></article></div></section>"""
urls.append(page("privacy-policy.html", f"Privacy Policy | {NAME}", f"How {NAME} handles information you share on this website.", priv,
                 crumbs=[("Home", "index.html"), ("Privacy policy", "privacy-policy.html")]))

# 404 (not in sitemap)
page("404.html", f"Page not found | {NAME}", "The page you are looking for could not be found.",
     f"""<section><div class="wrap"><h1>Page not found</h1><p class="lead">This page may have moved. Try one of these instead.</p>
<div class="btns"><a class="btn" href="/index.html">Home</a><a class="btn alt2" href="/departments.html">Departments</a><a class="btn alt2" href="/appointment.html">Book appointment</a></div></div></section>""")
p404 = os.path.join(ROOT, "404.html")
s = open(p404, encoding="utf-8").read().replace('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">', '<meta name="robots" content="noindex, follow">')
open(p404, "w", encoding="utf-8").write(s)

# ---------------------------------------------------------------- sitemap, robots, manifest, htaccess, images
def prio(u):
    if u == DOMAIN + "/": return "1.0"
    if "departments/" in u or "appointment" in u: return "0.9"
    if "blog/" in u: return "0.7"
    return "0.8"
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    sm.append(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{prio(u)}</priority></url>")
sm.append("</urlset>")
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm))
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {DOMAIN}/sitemap.xml\n")
open(os.path.join(ROOT, "manifest.webmanifest"), "w").write(json.dumps({
    "name": NAME, "short_name": C["short"], "start_url": "/index.html", "display": "standalone",
    "background_color": "#ffffff", "theme_color": "#0f6b73",
    "icons": [{"src": "/assets/img/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}]}, indent=2))
open(os.path.join(ROOT, ".htaccess"), "w").write("""# Apache settings for speed + SEO (works on most shared hosting / cPanel)
ErrorDocument 404 /404.html
DirectoryIndex index.html
Options -Indexes

RewriteEngine On
# force HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
# remove www (change if you prefer www)
RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
# /index.html -> /
RewriteCond %{THE_REQUEST} \\s/index\\.html[\\s?] [NC]
RewriteRule ^index\\.html$ / [L,R=301]

<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml application/xml
</IfModule>
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType text/css "access plus 1 year"
ExpiresByType application/javascript "access plus 1 year"
ExpiresByType image/png "access plus 1 year"
ExpiresByType image/svg+xml "access plus 1 year"
ExpiresByType text/html "access plus 1 hour"
</IfModule>
<IfModule mod_headers.c>
Header set X-Content-Type-Options "nosniff"
Header set X-Frame-Options "SAMEORIGIN"
Header set Referrer-Policy "strict-origin-when-cross-origin"
Header set Strict-Transport-Security "max-age=31536000; includeSubDomains" env=HTTPS
</IfModule>
""")
img = os.path.join(ROOT, "assets", "img")
open(os.path.join(img, "logo.svg"), "w").write(logo_svg(128).replace('aria-hidden="true" focusable="false"', 'xmlns="http://www.w3.org/2000/svg"'))
open(os.path.join(img, "favicon.svg"), "w").write(logo_svg(64).replace('aria-hidden="true" focusable="false"', 'xmlns="http://www.w3.org/2000/svg"'))
try:
    from PIL import Image, ImageDraw, ImageFont
    def font(sz, bold=True):
        for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
            if os.path.exists(f): return ImageFont.truetype(f, sz)
        return ImageFont.load_default()
    im = Image.new("RGB", (1200, 630), "#0c3a41"); dr = ImageDraw.Draw(im)
    dr.rounded_rectangle((80, 90, 200, 210), 28, fill="#0f6b73")
    dr.polygon([(120, 110), (160, 110), (160, 130), (180, 130), (180, 170), (160, 170), (160, 190), (120, 190), (120, 170), (100, 170), (100, 130), (120, 130)], fill="white")
    dr.text((80, 270), NAME, font=font(72), fill="white")
    dr.text((80, 380), f"Specialist care & 24/7 emergency in {CITY}", font=font(38), fill="#cfe5df")
    dr.text((80, 520), f"Emergency: {C['emergency']}", font=font(34), fill="#ff8f86")
    im.save(os.path.join(img, "og-image.png"), optimize=True)
    ic = Image.new("RGB", (180, 180), "#0f6b73"); d2 = ImageDraw.Draw(ic)
    d2.polygon([(70, 30), (110, 30), (110, 70), (150, 70), (150, 110), (110, 110), (110, 150), (70, 150), (70, 110), (30, 110), (30, 70), (70, 70)], fill="white")
    ic.save(os.path.join(img, "apple-touch-icon.png"))
except Exception as ex:
    print("PIL not available, create og-image.png (1200x630) and apple-touch-icon.png (180x180) manually:", ex)

print("Built %d pages for %s" % (len(urls) + 1, NAME))
