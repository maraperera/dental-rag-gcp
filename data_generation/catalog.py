# Standard procedures and AUD fees
TREATMENTS_CATALOG = [
    (1, "Comprehensive Oral Examination", "Full diagnostic visual exam, charting, and periodontal screening (Item 011)", 95.00),
    (2, "Periodic Oral Examination", "Routine 6-month recall visual checkup (Item 012)", 75.00),
    (3, "Dental Prophylaxis & Scaling", "Removal of plaque, calculus, and stains (Item 114)", 140.00),
    (4, "Topical Fluoride Application", "High-potency remineralization therapy (Item 121)", 45.00),
    (5, "Bitewing Radiographs (Pair)", "Two posterior horizontal bitewing radiographs (Item 022)", 65.00),
    (6, "Panoramic Radiograph (OPG)", "Full jaw extraoral rotational radiograph (Item 037)", 125.00),
    (7, "Composite Resin Restoration - 1 Surface", "Anterior or posterior tooth-colored filling (Item 521)", 170.00),
    (8, "Composite Resin Restoration - 2 Surfaces", "Multi-surface posterior restoration (Item 522)", 235.00),
    (9, "Root Canal Therapy - Single Canal", "Endodontic extirpation, cleaning, and obturation (Item 417)", 780.00),
    (10, "Root Canal Therapy - Molar (Multi-canal)", "Complete molar endodontic treatment (Item 418)", 1250.00),
    (11, "Porcelain / Ceramic Crown", "Lab-fabricated full contour crown (Item 615)", 1450.00),
    (12, "Surgical Tooth Extraction", "Surgical removal of impacted tooth or retained root (Item 322)", 350.00),
    (13, "Simple Tooth Extraction", "Non-surgical extraction of erupted tooth (Item 311)", 190.00),
    (14, "Titanium Dental Implant Placement", "Surgical fixture placement stage 1 (Item 688)", 2400.00),
    (15, "Custom Occlusal Splint / Night Guard", "Lab-fabricated acrylic occlusal splint for bruxism (Item 965)", 550.00),
]

DENTAL_CONDITIONS = [
    ("Class II Carious Lesion", "Interproximal radiolucency extending into dentin. Recommended composite restoration."),
    ("Recurrent Microleakage", "Marginal breakdown along lingual border with localized discoloration. Refilling suggested."),
    ("Symptomatic Irreversible Pulpitis", "Exaggerated lingering thermal sensitivity (>10 sec) with sharp spontaneous pain. RCT recommended."),
    ("Chronic Periodontitis Stage II", "Localized 4-5mm probing depths, subgingival calculus, moderate bleeding on probing (BOP)."),
    ("Gingival Recession Grade 1", "2mm buccal marginal tissue recession without interproximal bone loss. Monitored for root sensitivity."),
    ("Cracked Tooth Syndrome", "Pain on mastication, positive tooth slooth bite test on distobuccal cusp. Recommended cuspal coverage crown."),
    ("Impacted Wisdom Tooth (Mesioangular)", "Partially erupted lower third molar with mild recurrent pericoronitis. Surgical extraction indicated."),
    ("Healthy Clinical Presentation", "Normal periodontal architecture, probing depths <= 2mm, sound restorations, no active decay.")
]

MEDICAL_HISTORY_CONDITIONS = [
    ("Type 2 Diabetes Mellitus", "HbA1c 7.1%. Increased susceptibility to periodontal disease and slow postoperative healing."),
    ("Essential Hypertension", "Well managed on Perindopril 5mg daily. Pre-op blood pressure monitoring protocol active."),
    ("Severe Penicillin Allergy", "True anaphylaxis with hives and wheezing. Contraindication to all beta-lactams; use Clindamycin."),
    ("Ischemic Heart Disease", "Drug-eluting stent placed 2022. Patient on low-dose Aspirin. Advised not to cease antiplatelets."),
    ("Asthma", "Triggered by cold air/stress. Patient instructed to carry Salbutamol inhaler to all appointments."),
    ("Mild Latex Sensitivity", "Contact erythematous rash. Non-latex nitriles and dental dams must be used."),
    ("Osteopenia", "T-score -1.8. Regular intake of vitamin D and calcium; no bisphosphonates prescribed.")
]

PRESCRIPTION_MEDICATIONS = [
    ("Amoxicillin", "500 mg", "Take 1 capsule orally every 8 hours for 5 days. Complete full course."),
    ("Clindamycin", "300 mg", "Take 1 capsule orally every 6 hours with a full glass of water for 5 days."),
    ("Ibuprofen", "400 mg", "Take 1-2 tablets every 6-8 hours with food as needed for inflammatory pain."),
    ("Paracetamol / Codeine (30mg)", "500/30 mg", "Take 1 tablet every 4 to 6 hours as needed for severe postoperative pain (max 4/day)."),
    ("Chlorhexidine Gluconate 0.2%", "15 ml rinse", "Rinse twice daily for 30 seconds after brushing, then spit. Do not swallow.")
]

APPOINTMENT_REASONS = [
    "Severe toothache in lower right quadrant",
    "Scheduled 6-month routine cleaning and checkup",
    "Chipped molar while eating",
    "Persistent jaw pain and morning tightness",
    "Crown came off while chewing",
    "Bleeding gums when flossing",
    "Wisdom tooth tenderness and swelling",
    "Cold sensitivity around upper front teeth",
    "Follow-up suture check"
]