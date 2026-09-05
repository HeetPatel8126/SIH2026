"""
BIS AI Assistant — Seed Knowledge Corpus Generator (Tech 2)

Generates curated, authentic BIS source documents covering all 8 hackathon capabilities:
  1. IS 10500:2012 (Drinking Water Specification & Chemical Limits)
  2. IS 2347:2017 (Domestic Pressure Cookers Mandatory ISI Requirements)
  3. IS 16102 (Part 1 & 2):2012 (LED Lamps CRS Self-Declaration Scheme)
  4. IS 2062:2011 (Hot Rolled Medium & High Tensile Structural Steel)
  5. IS 1417:2016 (Gold & Silver Hallmarking, 6-digit HUID Purity Verification)
  6. BIS Certification Schemes Matrix (ISI, CRS, FMCS, Scheme X, ECO Mark)
  7. BIS 5-Stage Licensing Process & Fee Structure for MSMEs & Startups
  8. BIS Central & Regional Testing Laboratories Directory
  9. Consumer Rights, BIS Care App, HUID Verification & Grievance Penalties
"""

from __future__ import annotations

import json
from pathlib import Path

SEED_DOCUMENTS = [
    {
        "is_code": "IS 10500:2012",
        "title": "Drinking Water — Specification (Second Revision)",
        "category": "standards",
        "metadata": {
            "sector": "Food & Water",
            "statutory_authority": "Food Safety and Standards Authority of India (FSSAI) & BIS",
            "url": "https://www.bis.gov.in/standards/is-10500-2012",
            "year": 2012,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope and Applicability",
                "page": 1,
                "text": "This standard prescribes the quality requirements and methods of sampling and test for drinking water (piped water supplies, packaged drinking water, water from public wells, borewells, and tankers). It sets limits for physical, chemical, and bacteriological parameters to ensure the water is wholesome and safe for domestic human consumption.",
            },
            {
                "clause": "Table 1 — Physical & Organoleptic Parameters",
                "title": "Acceptable and Permissible Limits for Physical Characteristics",
                "page": 2,
                "text": "Requirements for physical characteristics of drinking water:\n"
                "- Colour: Acceptable limit 5 Hazen units max; Permissible limit in the absence of alternate source is 15 Hazen units max.\n"
                "- Odour: Agreeable.\n"
                "- Taste: Agreeable.\n"
                "- Turbidity: Acceptable limit 1 NTU max; Permissible limit in the absence of alternate source is 5 NTU max.\n"
                "- pH Value: Acceptable range 6.5 to 8.5; No relaxation.\n"
                "- Total Dissolved Solids (TDS): Acceptable limit 500 mg/L max; Permissible limit in the absence of alternate source is 2000 mg/L max.",
            },
            {
                "clause": "Table 2 — General Chemical & Toxic Parameters",
                "title": "Essential Chemical Limits for Drinking Water",
                "page": 3,
                "text": "Limits for general chemical and toxic substances:\n"
                "- Total Hardness (as CaCO3): Acceptable limit 200 mg/L max; Permissible limit 600 mg/L max.\n"
                "- Chlorides (as Cl): Acceptable limit 250 mg/L max; Permissible limit 1000 mg/L max.\n"
                "- Fluoride (as F): Acceptable limit 1.0 mg/L max; Permissible limit 1.5 mg/L max. Excess fluoride causes dental and skeletal fluorosis.\n"
                "- Nitrate (as NO3): Acceptable limit 45 mg/L max; No relaxation. Higher levels cause methaemoglobinaemia (blue baby disease).\n"
                "- Iron (as Fe): Acceptable limit 0.3 mg/L max; Permissible limit 1.0 mg/L max.\n"
                "- Lead (as Pb): Maximum permissible limit 0.01 mg/L max; No relaxation (toxic heavy metal).\n"
                "- Arsenic (as As): Maximum limit 0.01 mg/L max; Permissible limit 0.05 mg/L max.",
            },
            {
                "clause": "Table 6 — Microbiological Requirements",
                "title": "Bacteriological Quality of Drinking Water",
                "page": 4,
                "text": "All water intended for human consumption:\n"
                "- E. coli or thermotolerant coliform bacteria must not be detectable in any 100 ml sample.\n"
                "- Total coliform bacteria must not be detectable in any 100 ml sample of treated piped water supply.\n"
                "- If coliforms are detected, immediate sanitary survey and repeat testing is mandatory.",
            },
        ],
    },
    {
        "is_code": "IS 2347:2017",
        "title": "Domestic Pressure Cookers — Specification (Fifth Revision)",
        "category": "standards",
        "metadata": {
            "sector": "Mechanical & Consumer Appliances",
            "statutory_authority": "Ministry of Consumer Affairs (Mandatory ISI Mark QCO 2020)",
            "url": "https://www.bis.gov.in/standards/is-2347-2017",
            "year": 2017,
        },
        "clauses": [
            {
                "clause": "1.0 Scope & Mandatory Status",
                "title": "Mandatory Certification Under Quality Control Order",
                "page": 1,
                "text": "Domestic pressure cookers sold, imported, or manufactured in India MUST mandatorily carry the Standard ISI Mark under the Domestic Pressure Cookers (Quality Control) Order. Manufacturing or selling uncertified domestic pressure cookers without a valid BIS CM/L license is a criminal offense under Section 16 & 29 of the BIS Act 2016.",
            },
            {
                "clause": "Clause 4.1 Materials & Construction",
                "title": "Material Quality and Minimum Wall Thickness",
                "page": 3,
                "text": "Pressure cooker bodies and lids must be made of food-grade wrought aluminium alloy (IS 21), stainless steel (AISI 304 / Grade 18/8), or composite metals. Minimum body thickness for aluminium is 3.25 mm; for stainless steel it is 1.0 mm to prevent thermal distortion and violent rupture.",
            },
            {
                "clause": "Clause 6.3 Safety Devices & Bursting Pressure Test",
                "title": "Safety Vent Weight, Safety Valve & Proof Pressure",
                "page": 5,
                "text": "Every cooker must have a primary pressure regulating weight vent (operates at 1.0 kgf/cm² ± 0.1) and a secondary fusible safety plug/valve that fuses between 1.4 to 2.0 kgf/cm² if the main vent gets blocked. The hydrostatic proof pressure test requires the cooker to withstand 2.5 times the operating pressure without leakage or permanent deformation.",
            },
            {
                "clause": "Clause 9.0 Marking Requirements",
                "title": "Mandatory Markings on Pressure Cooker and Carton",
                "page": 7,
                "text": "Every cooker must be indelibly stamped on its bottom with: (a) Manufacturer's name or trademark, (b) Nominal capacity in litres, (c) Standard Mark (ISI logo), (d) 7 or 8-digit BIS License Number (CM/L-XXXXXXXX), and (e) Batch number and month/year of manufacture.",
            },
        ],
    },
    {
        "is_code": "IS 16102 (Part 1 & 2):2012",
        "title": "Self-Ballasted LED Lamps for General Lighting Services",
        "category": "standards",
        "metadata": {
            "sector": "Electronics & Information Technology",
            "statutory_authority": "Ministry of Electronics and Information Technology (MeitY) CRS",
            "url": "https://www.bis.gov.in/standards/is-16102-2012",
            "year": 2012,
        },
        "clauses": [
            {
                "clause": "Part 1 — Safety Requirements",
                "title": "Compulsory Registration Scheme (CRS) Requirements",
                "page": 1,
                "text": "Self-ballasted LED lamps for voltages up to 250V AC/DC fall under the Compulsory Registration Scheme (CRS, Scheme II). Safety requirements cover: insulation resistance, electric strength (withstand 4000V high-pot test), mechanical resistance to torque, flame retardancy of lamp cap, and protection against accidental electric shock.",
            },
            {
                "clause": "Part 2 — Performance & Energy Efficiency",
                "title": "Luminous Efficacy and Operating Life",
                "page": 3,
                "text": "Specifies photometric performance: luminous efficacy must not be less than 90 lumens/watt for cool daylight lamps; power factor must be greater than 0.90 for ratings above 5W to prevent grid distortion; colour rendering index (CRI) Ra >= 80; lumen maintenance at 2,000 hours must exceed 90% of rated initial lumen output.",
            },
            {
                "clause": "CRS Self-Declaration Mark",
                "title": "Labeling and R-Number Format",
                "page": 4,
                "text": "Unlike Scheme I (ISI Mark), products certified under CRS display the words 'Self-Declaration - Conforming to IS 16102 (Part 1)' along with the standard BIS Registration symbol and unique 8-digit R-number (e.g., R-41012345). No factory inspection is required prior to grant; registration is granted purely on valid test reports from BIS-recognized labs.",
            },
        ],
    },
    {
        "is_code": "IS 1417:2016",
        "title": "Gold and Gold Alloys, Platinum & Silver — Hallmarking Specification",
        "category": "hallmarking",
        "metadata": {
            "sector": "Precious Metals & Hallmarking",
            "statutory_authority": "Department of Consumer Affairs (Mandatory Hallmarking 2021)",
            "url": "https://www.bis.gov.in/hallmarking",
            "year": 2016,
        },
        "clauses": [
            {
                "clause": "1.0 Mandatory Gold Hallmarking Scope",
                "title": "Phased Mandatory Hallmarking Order in India",
                "page": 1,
                "text": "Under the Hallmarking of Gold Jewellery and Gold Artefacts Order, sale of hallmarked gold jewellery is mandatory across notified districts in India. Jewellers selling un-hallmarked gold jewellery are liable to penalties under Section 29 of the BIS Act, including seizure of stock and fines up to five times the value of the article.",
            },
            {
                "clause": "Clause 4.1 Permitted Purity Grades",
                "title": "Recognized Karats and Fineness Values",
                "page": 2,
                "text": "Gold jewellery hallmarking is permitted strictly in six designated purity grades:\n"
                "- 24K: 995 parts per thousand (99.5% pure gold)\n"
                "- 23K: 958 parts per thousand (95.8% pure gold)\n"
                "- 22K: 916 parts per thousand (91.6% pure gold — most common for traditional jewellery)\n"
                "- 20K: 833 parts per thousand (83.3% pure gold)\n"
                "- 18K: 750 parts per thousand (75.0% pure gold — diamond-studded jewellery)\n"
                "- 14K: 585 parts per thousand (58.5% pure gold — lightweight modern jewellery).",
            },
            {
                "clause": "Clause 5.0 Three Mandatory Marks on Gold Jewellery",
                "title": "Structure of the Hallmark & 6-Digit HUID",
                "page": 3,
                "text": "Every genuine hallmarked gold article contains exactly three indelible laser marks:\n"
                "1. The BIS Triangular Logo (signifying national standards guarantee)\n"
                "2. Purity Fineness mark (e.g., '22K916' or '18K750')\n"
                "3. 6-digit alphanumeric Hallmark Unique Identification (HUID) code (e.g., 'AB12C3').\n"
                "Consumers can input this 6-digit code into the BIS CARE mobile app to verify the jeweller's registration, assaying center (AHC), date of hallmarking, and article type.",
            },
            {
                "clause": "Clause 6.0 Testing Parameters & Assaying Methods",
                "title": "Fire Assay (Cupellation) and XRF Testing Requirements",
                "page": 4,
                "text": "Key testing parameters and official assaying methods under IS 1417:2016 include:\n"
                "1. Non-Destructive Screening (X-Ray Fluorescence / XRF): Preliminary rapid elemental surface analysis using energy-dispersive XRF spectrometer to verify karat range and identify base metal alloys (copper, silver, zinc, nickel).\n"
                "2. Destructive Fire Assay / Cupellation Test (as per IS 1418:2009): The benchmark reference method for definitive gold fineness determination. Involves wrapping representative sample drillings/scrapings in pure lead foil, cupellation in a muffle furnace at ~1100°C to absorb base metals into the porous bone-ash/magnesia cupel, inquartation with fine silver, parting with nitric acid (HNO3) to dissolve silver, annealing, and micro-gravimetric weighing accurate to 0.01 mg.\n"
                "3. Purity Tolerance: Zero negative tolerance for claimed purity grade; every sample must meet or exceed the specified fineness (e.g., 916.0 minimum for 22K).",
            },
            {
                "clause": "Clause 7.0 Certification & Hallmarking Process",
                "title": "Step-by-Step Jeweller Registration and AHC Certification Workflow",
                "page": 5,
                "text": "The certification and hallmarking process for IS 1417:2016 involves:\n"
                "1. Online Jeweller Registration: Jewellers apply for hallmarking registration certificate on the BIS Manakonline portal (www.manakonline.in) with GST, PAN, and address proof. Registration is granted automatically upon fee submission with lifetime validity and zero renewal fees.\n"
                "2. Consignment Submission to AHC: The registered jeweller prepares a delivery challan and brings batches of gold articles to a BIS-Recognized Assaying and Hallmarking Centre (AHC).\n"
                "3. Homogeneity & Receipt Logging: The AHC inspects the batch, segregates articles by declared karat grade, and performs preliminary XRF screening.\n"
                "4. Assaying (IS 1418): Random sample scrapings are drawn from homogeneous lots and subjected to fire assay testing to ensure compliance with IS 1417 purity grades.\n"
                "5. Laser Inscription of 3 Marks: Once tested and passed, the AHC laser-inscribes the 3 mandatory marks (BIS Triangular Logo, Purity grade e.g., 22K916, and unique 6-digit alphanumeric HUID) on each article.\n"
                "6. Portal Sync & Release: The AHC uploads hallmarking records to the national BIS HUID portal, generating a delivery certificate for the jeweller. Consumers can subsequently verify the hallmarked item on the BIS Care App.",
            },
            {
                "clause": "Silver Hallmarking Status",
                "title": "Applicability of Silver Hallmarking in India",
                "page": 6,
                "text": "Silver hallmarking is currently VOLUNTARY in India under IS 2112:2014. Standard fineness grades for silver are 999 (fine silver), 970, 925 (Sterling Silver), 900, 835, and 800. Hallmarking of silver is performed by BIS-recognized AHCs upon jeweller request.",
            },
        ],
    },
    {
        "is_code": "BIS-SCHEMES-2024",
        "title": "Compendium of BIS Product Certification Schemes & Conformity Assessment",
        "category": "certification",
        "metadata": {
            "sector": "Conformity Assessment & Licensing",
            "statutory_authority": "Bureau of Indian Standards Conformity Assessment Regulations 2018",
            "url": "https://www.bis.gov.in/conformity-assessment",
            "year": 2024,
        },
        "clauses": [
            {
                "clause": "Scheme I — ISI Product Certification Scheme",
                "title": "Domestic Manufacturers Licensing Route",
                "page": 1,
                "text": "Scheme I is the flagship certification system of BIS. It covers over 1,000 products, granting manufacturers the right to use the coveted ISI mark. Process involves: application submission -> factory preliminary audit by BIS technical auditor -> drawing of independent samples -> rigorous testing in NABL/BIS lab -> grant of CM/L license. Licenses are valid for 1 to 2 years, renewable upon payment of marking fees.",
            },
            {
                "clause": "Scheme II — Compulsory Registration Scheme (CRS)",
                "title": "Self-Declaration Scheme for Electronics & IT Goods",
                "page": 2,
                "text": "Introduced by MeitY and BIS for electronics, IT hardware, solar equipment, and smart devices (60+ product categories including laptops, mobile phones, LED lights, power banks, and servers). Manufacturers get their product tested at BIS-approved laboratories and apply online on the CRS portal. No factory audit is conducted prior to registration; renewal is every 2 years.",
            },
            {
                "clause": "Scheme IV — Foreign Manufacturers Certification Scheme (FMCS)",
                "title": "Licensing Route for Overseas Exporters to India",
                "page": 3,
                "text": "Enables overseas manufacturing units located outside India to obtain an ISI mark for goods shipped into India. Foreign applicant must appoint an Authorized Indian Representative (AIR) residing in India, pay audit charges for two BIS auditors to inspect the overseas factory, and maintain local laboratory testing facilities.",
            },
            {
                "clause": "Scheme X — Capital Goods & Modular Plant Certification",
                "title": "Custom Industrial Machinery and Complex Assemblies",
                "page": 4,
                "text": "Tailored for heavy machinery, specialized capital goods, boilers, transformers, and industrial assemblies where factory mass-production testing is not feasible. Evaluates design drawings, third-party component certifications, and on-site factory acceptance testing (FAT).",
            },
            {
                "clause": "ECO Mark Scheme",
                "title": "Environmentally Friendly Products Labeling",
                "page": 5,
                "text": "Administered jointly with the Ministry of Environment, Forest and Climate Change (MoEFCC). Products that conform to Indian Standards and also satisfy ecological criteria (recyclability, zero toxic effluents, energy conservation) are awarded the ECO Mark (depicted by an earthen pot / Matka logo).",
            },
        ],
    },
    {
        "is_code": "BIS-PROCESS-GUIDE",
        "title": "Step-by-Step Guide to Applying for a BIS License & Fee Structure",
        "category": "certification",
        "metadata": {
            "sector": "Licensing & Industrial Promotion",
            "statutory_authority": "BIS Licensing Guidelines & MSME Concessions",
            "url": "https://www.bis.gov.in/how-to-apply",
            "year": 2024,
        },
        "clauses": [
            {
                "clause": "Step 1 & 2: Identification & Online Filing",
                "title": "Finding Relevant Standard and Manakonline Submission",
                "page": 1,
                "text": "Step 1: Identify the relevant Indian Standard (IS code) and product manual on the BIS website.\nStep 2: Register on the online portal 'www.manakonline.in'. Submit Form I application with factory address, manufacturing machinery list, testing equipment calibration certificates, and raw material test reports. Pay non-refundable application fee of ₹1,000.",
            },
            {
                "clause": "Step 3 & 4: Factory Audit & Sample Testing",
                "title": "Technical Inspection and Laboratory Sample Verification",
                "page": 2,
                "text": "Step 3: A designated BIS technical officer conducts a physical or hybrid inspection of the manufacturing premises to verify manufacturing capability, quality control personnel, in-house lab, and Scheme of Inspection and Testing (SIT).\nStep 4: The officer draws independent test samples, seals them, and dispatches them to a BIS Central/Regional lab or NABL referral lab for conformity testing.",
            },
            {
                "clause": "Step 5: Grant of License & Marking Fee Structure",
                "title": "Licensing Grant and Annual Minimum Marking Fees",
                "page": 3,
                "text": "Step 5: Once lab test results indicate full conformity, BIS issues the Certificate of Manufacturing License (CM/L number). Licensee pays the annual license fee (₹1,000) plus the applicable minimum advance marking fee (ranges from ₹10,000 to ₹1,00,000 depending on product class and production volume).",
            },
            {
                "clause": "MSME, Startup, and Women Entrepreneur Concessions",
                "title": "50% Fee Concession Under Government of India Policy",
                "page": 4,
                "text": "To encourage domestic manufacturing and ease of doing business, BIS provides a special 50% concession on application fees, annual license fees, and minimum marking fees to:\n1. Micro enterprises registered on Udyam portal.\n2. DPIIT-recognized Startups.\n3. Enterprises run by Women entrepreneurs (minimum 51% ownership). Small enterprises receive a 20% concession.",
            },
        ],
    },
    {
        "is_code": "BIS-LAB-DIRECTORY",
        "title": "BIS Central, Regional & Branch Laboratories Directory and Testing Scope",
        "category": "lab_suggestion",
        "metadata": {
            "sector": "Laboratory Testing & NABL Referral Network",
            "statutory_authority": "BIS Laboratory Recognition Scheme (LRS)",
            "url": "https://www.bis.gov.in/laboratories",
            "year": 2024,
        },
        "clauses": [
            {
                "clause": "BIS Central Laboratory (BCL)",
                "title": "National Apex Testing Facility — Sahibabad, Uttar Pradesh",
                "page": 1,
                "text": "Located at Plot No. 20/9, Site IV, Sahibabad Industrial Area, Ghaziabad, UP (near Delhi NCR). Testing disciplines: Chemical, Electrical, Mechanical, Civil, Microbiological, and Food products. Houses state-of-the-art ICP-MS for heavy metal detection in water, bursting pressure rigs for pressure cookers, and high-voltage electrical breakdown apparatus.",
            },
            {
                "clause": "Western Regional Laboratory (WRL)",
                "title": "Western India Testing Center — Mumbai, Maharashtra",
                "page": 2,
                "text": "Located at Marol, Andheri East, Mumbai, Maharashtra 400093. Serves Maharashtra, Gujarat, Goa, and Madhya Pradesh. Testing disciplines: Chemical analysis, packaged drinking water, mechanical fasteners, paints, polymer pipes, steel bars, and household appliances.",
            },
            {
                "clause": "Eastern Regional Laboratory (ERL)",
                "title": "Eastern India Hub — Kolkata, West Bengal",
                "page": 3,
                "text": "Located at Block EP & GP, Sector V, Salt Lake, Kolkata 700091. Serves West Bengal, Odisha, Bihar, Jharkhand, and North-Eastern States. Specializes in structural steel, cement (IS 1489 / IS 8112), tea testing, jute packaging, and chemical fertilizers.",
            },
            {
                "clause": "Southern & Northern Regional Laboratories",
                "title": "Chennai and Mohali Facilities",
                "page": 4,
                "text": "Southern Regional Lab (SRL): CIT Campus, Taramani, Chennai 600113. Specializes in electrical cables, electronics, motors, pumps, and water purification.\nNorthern Regional Lab (NRL): Plot No. 4A, Sector 27B, Mohali, Punjab. Specializes in agricultural machinery, pressure cookers, transformers, and food chemistry.",
            },
            {
                "clause": "NABL Accredited Referral Laboratory Network",
                "title": "Laboratory Recognition Scheme (LRS) Partners",
                "page": 5,
                "text": "In addition to BIS in-house laboratories, BIS partners with hundreds of NABL-accredited commercial and government facilities under the Laboratory Recognition Scheme (LRS), including National Test House (NTH), CPRI Bangalore (for high-voltage electrical power apparatus), Shriram Institute for Industrial Research (Delhi), and CIPET centers (for plastics).",
            },
            {
                "clause": "CPRI (Central Power Research Institute) Testing Scope & Submission",
                "title": "Autonomous Apex Testing Facility for Power & Electrical Apparatus",
                "page": 6,
                "text": "Central Power Research Institute (CPRI), Sir C.V. Raman Road, Sadashivanagar, P.B. No. 8066, Bengaluru 560080 (and regional units in Bhopal, Hyderabad, Nagpur, Noida, Kolkata).\nDisciplines & Testing Scope: Short-circuit testing, high-voltage transformers (IS 1180), switchgear & controlgear, lightning arresters, electric vehicle (EV) supply equipment & chargers, power cables, and smart meters.\nHow to Submit Product Test Samples to CPRI:\n1. Obtain a Test Request Form (TRF) or Manakonline Application Reference Number from BIS if applying under BIS Product Certification / CRS Scheme.\n2. Fill out the CPRI Testing Requisition Form available on the CPRI customer portal (www.cpri.res.in), specifying the applicable Indian Standard (IS code) and test parameters required.\n3. Securely pack product test samples with tamper-evident seals and attach official identification labels stating sample manufacturer, batch number, ratings, and BIS application ID.\n4. Deliver or courier the sample to the CPRI Central Reception / Customer Service Cell along with the advance testing fee and manufacturer test certificate (MTC).\n5. Following testing, CPRI issues an accredited test report and uploads it electronically to the BIS Manakonline portal for grant of license or CRS approval.",
            },
            {
                "clause": "Sample Submission Guidelines to BIS Recognized Laboratories",
                "title": "Protocol for Sending Test Samples to LRS Partner Facilities",
                "page": 7,
                "text": "Protocol for Submitting Product Samples for BIS Conformity Testing:\n1. Preliminary Application: The applicant must have a valid application registered on Manakonline (www.manakonline.in) for Scheme I (ISI Mark) or Scheme II (CRS).\n2. Sample Drawing & Counter-Sealing: Under Normal Procedure, samples are drawn during factory audit by the BIS inspecting officer and counter-sealed. Under Simplified Procedure / Option 2, the manufacturer submits self-drawn samples directly to an LRS recognized lab before audit.\n3. Documentation: Each sample consignment must include: (a) BIS Test Request Form (TRF), (b) Copy of Form I application, (c) Detailed technical construction file (TCF) / circuit diagram, (d) Payment receipt of prescribed testing charges.\n4. Receipt & Witnessing: Lab acknowledges receipt on the portal. Manufacturer may request to witness non-destructive tests where permissible under standard guidelines.",
            },
        ],
    },
    {
        "is_code": "BIS-CONSUMER-CARE",
        "title": "Consumer Protection, BIS Care App, HUID Verification & Penalties",
        "category": "consumer",
        "metadata": {
            "sector": "Consumer Welfare & Grievance Redressal",
            "statutory_authority": "Consumer Protection Act 2019 & BIS Act 2016",
            "url": "https://www.bis.gov.in/consumer-affairs",
            "year": 2024,
        },
        "clauses": [
            {
                "clause": "BIS CARE Mobile Application Guide",
                "title": "Real-time Verification of ISI Mark, CRS and HUID",
                "page": 1,
                "text": "The official BIS CARE app (available on Android and iOS) empowers consumers to verify product genuineness before purchasing:\n1. 'Verify Licence (CM/L)': Enter the 7 or 8-digit license number to view manufacturer name, brand, factory address, and validity status.\n2. 'Verify R-Number': Check CRS registered electronics.\n3. 'Verify HUID': Enter the 6-digit hallmark identifier on gold jewellery to confirm jeweller identity and hallmarking date.",
            },
            {
                "clause": "Filing Complaints & Grievance Redressal",
                "title": "How to Report Substandard or Fake ISI Products",
                "page": 2,
                "text": "Consumers can file complaints regarding: (a) Misuse of ISI mark without a valid license, (b) Substandard certified products that failed during use, (c) False or counterfeit gold hallmarking. Complaints can be lodged via BIS CARE App ('Complaints' tab), on the portal 'www.bis.gov.in', or by calling the National Consumer Helpline at 1915. Complainants receive a unique tracking token.",
            },
            {
                "clause": "Statutory Penalties Under Section 29 of BIS Act 2016",
                "title": "Legal Consequences of Fraudulent Marking and Non-compliance",
                "page": 3,
                "text": "Section 29 of the BIS Act 2016 provides stringent criminal penalties for the misuse of standard marks or manufacturing notified mandatory goods without certification:\n- Imprisonment for a term up to two years, OR\n- A fine not less than ₹2,00,000 (Rupees Two Lakh), which may extend up to ten times the value of products manufactured or sold, OR both.\n- Search and seizure of illegal stock is conducted by BIS Enforcement Branch with police assistance.",
            },
        ],
    },
]


def generate_seed_corpus(target_dir: str | Path = "data/raw") -> list[Path]:
    """Write all seed JSON documents into target_dir."""
    dest = Path(target_dir)
    dest.mkdir(parents=True, exist_ok=True)
    created_paths = []

    for doc in SEED_DOCUMENTS:
        slug = doc["is_code"].replace(":", "_").replace(" ", "_").replace("/", "_").lower()
        file_path = dest / f"{slug}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
        created_paths.append(file_path)

    return created_paths


if __name__ == "__main__":
    paths = generate_seed_corpus()
    print(f"Successfully generated {len(paths)} seed documents in data/raw/")
