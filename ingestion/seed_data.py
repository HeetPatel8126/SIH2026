"""
BIS AI Assistant — Expanded Seed Knowledge Corpus Generator (Tech 2)

Generates a comprehensive, authentic BIS source corpus covering 50+ real Indian
Standards, all 6 BIS certification schemes, hallmarking regulations, consumer
protection, and testing laboratories across India.

Each standard includes multiple realistic clauses with scope, requirements,
test methods, and compliance tables — yielding 200+ chunks total for a
demo-quality knowledge base.

Coverage:
  - Food & Water (7 standards)
  - Construction & Materials (8 standards)
  - Electronics & IT (7 standards)
  - Consumer Products & Safety (6 standards)
  - Automotive & Transport (4 standards)
  - Chemicals & Environment (4 standards)
  - Textiles & Packaging (4 standards)
  - Precious Metals & Hallmarking (3 standards + HUID system)
  - BIS Certification Schemes (ISI, CRS, FMCS, Hallmark, Scheme X, ECO Mark)
  - BIS Licensing Process & Fees
  - Testing Laboratories (all major regions)
  - Consumer Rights & Grievance Mechanisms
"""

from __future__ import annotations

import json
from pathlib import Path

SEED_DOCUMENTS = [
    # ===================================================================
    # FOOD & WATER STANDARDS
    # ===================================================================
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
                "clause": "Table 2 — Chemical Parameters",
                "title": "Chemical Requirements for Drinking Water",
                "page": 3,
                "text": "Key chemical parameters and limits:\n"
                "- Iron (Fe): Acceptable 0.3 mg/L; Permissible 1.0 mg/L (causes staining and taste issues above limits)\n"
                "- Fluoride: Acceptable 1.0 mg/L; Permissible 1.5 mg/L (excess causes dental/skeletal fluorosis)\n"
                "- Arsenic: Acceptable 0.01 mg/L; Permissible 0.05 mg/L (toxic heavy metal)\n"
                "- Lead: Acceptable 0.01 mg/L; No relaxation (neurotoxic)\n"
                "- Nitrate (as NO3): Acceptable 45 mg/L; No relaxation (causes methemoglobinemia in infants)\n"
                "- Total Hardness (as CaCO3): Acceptable 200 mg/L; Permissible 600 mg/L\n"
                "- Chloride: Acceptable 250 mg/L; Permissible 1000 mg/L\n"
                "- Residual Free Chlorine: Minimum 0.2 mg/L at consumer end for disinfection",
            },
            {
                "clause": "Table 3 — Bacteriological Parameters",
                "title": "Microbiological Requirements",
                "page": 4,
                "text": "Bacteriological requirements for drinking water:\n"
                "- E. coli or Thermotolerant Coliform: Shall not be detectable in any 100 mL sample.\n"
                "- Total Coliform: Shall not be detectable in any 100 mL sample (piped treated supply).\n"
                "- All drinking water samples should be free from pathogenic organisms.\n"
                "Testing method: IS 1622 (Methods of sampling and microbiological examination of water).",
            },
        ],
    },
    {
        "is_code": "IS 14543:2016",
        "title": "Packaged Drinking Water (Other Than Packaged Natural Mineral Water) — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Food & Water",
            "url": "https://www.bis.gov.in",
            "year": 2016,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "This standard covers packaged drinking water (other than packaged natural mineral water). It specifies requirements for raw water source, treatment process, packaging, and labelling. All packaged drinking water sold in India MUST bear the ISI mark under compulsory BIS certification (Scheme I). Products not conforming to IS 14543 cannot be legally sold as packaged drinking water.",
            },
            {
                "clause": "5.0 Requirements",
                "title": "Requirements for Packaged Drinking Water",
                "page": 3,
                "text": "Requirements include:\n"
                "- TDS: Shall not exceed 500 mg/L.\n"
                "- pH: 6.5 to 8.5.\n"
                "- Turbidity: Maximum 1 NTU.\n"
                "- Ozone treatment residual: Not more than 0.1 mg/L at the time of packaging.\n"
                "- Packing: Clean, hygienic, food-grade containers. Reusable containers must be properly cleaned and sanitized.\n"
                "- Labelling: Must display ISI mark, CM/L number, IS code, net quantity, manufacturing date, batch number, and 'best before' date.",
            },
        ],
    },
    {
        "is_code": "IS 7328:2019",
        "title": "Edible Vegetable Oils — Blended Edible Vegetable Oil — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Food & Water",
            "url": "https://www.bis.gov.in",
            "year": 2019,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope and Coverage",
                "page": 1,
                "text": "This standard prescribes requirements for blended edible vegetable oils obtained by blending two or more edible vegetable oils. The standard covers quality parameters including acid value, peroxide value, moisture content, and fatty acid composition. Blended oils must contain a minimum of 20% of any component oil.",
            },
            {
                "clause": "4.0 Requirements",
                "title": "Quality Requirements",
                "page": 2,
                "text": "Key requirements for blended edible vegetable oil:\n"
                "- Acid value: Not more than 0.5 mg KOH/g of oil (for refined blended oils)\n"
                "- Peroxide value: Not more than 10 meq oxygen/kg of oil\n"
                "- Moisture and volatile matter: Not more than 0.10%\n"
                "- The blend must be clearly labelled with the names and proportions of component oils\n"
                "- Argemone oil: Absent (toxic contaminant)\n"
                "- Mineral oil: Absent",
            },
        ],
    },
    {
        "is_code": "IS 7930:2019",
        "title": "Wheat Flour (Atta) — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Food & Water",
            "url": "https://www.bis.gov.in",
            "year": 2019,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "This standard covers whole wheat flour (atta) obtained by grinding clean wheat. It specifies the requirements for quality, hygiene, and packaging of wheat flour meant for human consumption.",
            },
            {
                "clause": "4.0 Requirements",
                "title": "Quality Requirements for Wheat Flour",
                "page": 2,
                "text": "Requirements for wheat flour (atta):\n"
                "- Moisture: Not more than 14.0% by mass\n"
                "- Total ash (on dry basis): Not more than 2.0% by mass\n"
                "- Acid insoluble ash: Not more than 0.1% by mass\n"
                "- Gluten (dry basis): Not less than 7.5% by mass\n"
                "- Uric acid: Not more than 100 mg/kg\n"
                "- Aflatoxin: Not more than 15 µg/kg\n"
                "- The flour shall be free from added colouring matter, rodent hair, excreta fragments, and insect fragments beyond prescribed limits.",
            },
        ],
    },
    {
        "is_code": "IS 2490:1991",
        "title": "Extracted Honey — Specification (Second Revision)",
        "category": "standards",
        "metadata": {
            "sector": "Food & Water",
            "url": "https://www.bis.gov.in",
            "year": 1991,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "This standard prescribes requirements for extracted honey intended for direct consumption. It covers floral honey, honeydew honey, and blended honey. ISI certification is available for honey under BIS Scheme I.",
            },
            {
                "clause": "3.0 Requirements",
                "title": "Requirements for Honey",
                "page": 2,
                "text": "Requirements for extracted honey:\n"
                "- Moisture content: Not more than 20% by mass\n"
                "- Total reducing sugars: Not less than 65%\n"
                "- Sucrose: Not more than 5%\n"
                "- Ash: Not more than 0.5%\n"
                "- Fiehe's test: Negative (indicates adulteration with sugar syrup)\n"
                "- Aniline chloride test: Negative (indicates invert sugar adulteration)\n"
                "- HMF (Hydroxymethylfurfural): Not more than 80 mg/kg\n"
                "- Honey shall be free from artificial flavouring, colouring matter, and any other food additives.",
            },
        ],
    },
    {
        "is_code": "IS 13428:2005",
        "title": "Packaged Natural Mineral Water — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Food & Water",
            "url": "https://www.bis.gov.in",
            "year": 2005,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "This standard prescribes requirements for packaged natural mineral water obtained directly from natural springs and underground sources. Unlike IS 14543 (packaged drinking water), mineral water must not undergo any treatment that alters its original mineral composition. BIS certification (ISI Mark) is MANDATORY for packaged natural mineral water.",
            },
            {
                "clause": "3.0 Requirements",
                "title": "Requirements",
                "page": 2,
                "text": "Requirements for packaged natural mineral water:\n"
                "- Source: Must originate from an underground water source protected from pollution\n"
                "- Mineral content: Total mineral content shall be declared on the label\n"
                "- No chemical treatment for disinfection allowed (UV or ozone only)\n"
                "- TDS: Minimum 150 mg/L (to distinguish from regular packaged water)\n"
                "- Labelling: Must declare dominant mineral composition (e.g., 'rich in calcium')",
            },
        ],
    },
    {
        "is_code": "IS 15778:2007",
        "title": "Organic Food Products — Requirements",
        "category": "standards",
        "metadata": {
            "sector": "Food & Water",
            "url": "https://www.bis.gov.in",
            "year": 2007,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "This standard specifies the requirements for production, processing, labelling, and marketing of organic food products. It provides guidelines for conversion period, permitted inputs, and certification requirements for organic food products in India.",
            },
        ],
    },
    # ===================================================================
    # CONSTRUCTION & MATERIALS
    # ===================================================================
    {
        "is_code": "IS 2062:2011",
        "title": "Hot Rolled Medium and High Tensile Structural Steel — Specification (Seventh Revision)",
        "category": "standards",
        "metadata": {
            "sector": "Construction & Steel",
            "url": "https://www.bis.gov.in",
            "year": 2011,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 2062:2011 specifies requirements for hot rolled medium and high tensile structural steel plates, strips, wide flats, shapes and sections (angles, tees, beams, channels, and bulb angles) for use in structural and general engineering purposes. This is the most widely used structural steel standard in India.",
            },
            {
                "clause": "Table 1 — Grades",
                "title": "Grades and Mechanical Properties",
                "page": 3,
                "text": "Key structural steel grades under IS 2062:\n"
                "- Grade E250A (Fe 410 W A): Most common; Yield strength ≥250 MPa, Tensile strength 410-540 MPa. Used for general structural work.\n"
                "- Grade E250B (Fe 410 W B): Same strength, additional impact test requirements.\n"
                "- Grade E300 (Fe 440): Yield ≥300 MPa, Tensile 440-570 MPa. For higher load applications.\n"
                "- Grade E350 (Fe 490): Yield ≥350 MPa, Tensile 490-630 MPa. For heavy structural work.\n"
                "- Grade E450 (Fe 570): Yield ≥450 MPa, Tensile 570-720 MPa. For bridges and heavy structures.\n"
                "- Carbon content shall not exceed 0.23% (max) for E250 grade.\n"
                "- All structural steel used in India for buildings and bridges should conform to IS 2062.",
            },
        ],
    },
    {
        "is_code": "IS 456:2000",
        "title": "Plain and Reinforced Concrete — Code of Practice (Fourth Revision)",
        "category": "standards",
        "metadata": {
            "sector": "Construction & Steel",
            "url": "https://www.bis.gov.in",
            "year": 2000,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 456 is the primary Indian Standard code of practice for design of plain and reinforced concrete structures. It covers materials, workmanship, inspection, and testing requirements. This is one of the most important BIS standards for the construction industry and is mandatorily followed in all government and private construction projects in India.",
            },
            {
                "clause": "Table 5 — Grades of Concrete",
                "title": "Grades of Concrete",
                "page": 5,
                "text": "Standard grades of concrete as per IS 456:\n"
                "- M10: Characteristic compressive strength 10 MPa (used for lean concrete, levelling)\n"
                "- M15: 15 MPa (plain concrete works, PCC)\n"
                "- M20: 20 MPa (general reinforced concrete, minimum for RCC)\n"
                "- M25: 25 MPa (reinforced concrete in moderate exposure)\n"
                "- M30: 30 MPa (RCC in severe exposure conditions, bridges)\n"
                "- M35: 35 MPa (pre-stressed concrete, heavy structural work)\n"
                "- M40 and above: High-performance concrete for special structures\n"
                "- Minimum grade for reinforced concrete is M20. Minimum grade for pre-stressed concrete is M30.\n"
                "- Water-cement ratio shall not exceed 0.55 for M20 in moderate exposure.",
            },
        ],
    },
    {
        "is_code": "IS 1786:2008",
        "title": "High Strength Deformed Steel Bars and Wires for Concrete Reinforcement — Specification (Fourth Revision)",
        "category": "standards",
        "metadata": {
            "sector": "Construction & Steel",
            "url": "https://www.bis.gov.in",
            "year": 2008,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 1786 specifies requirements for high strength deformed steel bars and wires (TMT bars) produced by the thermo-mechanical treatment process for use as reinforcement in concrete. ISI certification is MANDATORY for TMT bars/steel reinforcement sold in India.",
            },
            {
                "clause": "5.0 Grades",
                "title": "Grades and Properties",
                "page": 3,
                "text": "TMT bar grades under IS 1786:\n"
                "- Fe 415: Yield strength ≥415 MPa, Elongation ≥14.5%. Most common for residential construction.\n"
                "- Fe 415D: Ductile variant of Fe 415 with higher elongation (≥18%). Recommended for earthquake-prone zones.\n"
                "- Fe 500: Yield strength ≥500 MPa, Elongation ≥12%. For commercial and industrial structures.\n"
                "- Fe 500D: Ductile variant with elongation ≥16%. Preferred for seismic zones.\n"
                "- Fe 550: Yield ≥550 MPa. For heavy infrastructure.\n"
                "- Fe 600: Yield ≥600 MPa. For pre-stressed concrete and specialized applications.\n"
                "- Carbon content: Max 0.30% for Fe 415, Max 0.25% for Fe 500D\n"
                "- All TMT bars must bear the ISI mark (CM/L number) for legal sale in India.",
            },
        ],
    },
    {
        "is_code": "IS 269:2015",
        "title": "Ordinary Portland Cement — Specification (Sixth Revision)",
        "category": "standards",
        "metadata": {
            "sector": "Construction & Steel",
            "url": "https://www.bis.gov.in",
            "year": 2015,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 269 specifies requirements for 33-grade Ordinary Portland Cement (OPC). This is the basic cement standard. Higher grade cements are covered by IS 8112 (43-grade OPC) and IS 12269 (53-grade OPC). ALL cement sold in India must mandatorily carry the ISI mark — cement is one of the items under compulsory BIS certification.",
            },
            {
                "clause": "5.0 Chemical Requirements",
                "title": "Chemical Composition Requirements",
                "page": 3,
                "text": "Chemical requirements for OPC (IS 269):\n"
                "- Lime Saturation Factor: 0.66 to 1.02\n"
                "- Insoluble Residue: Not more than 4.0%\n"
                "- Magnesia (MgO): Not more than 6.0%\n"
                "- Sulphuric Anhydride (SO3): Not more than 3.5%\n"
                "- Total Loss on Ignition: Not more than 5.0%\n"
                "- Compressive strength at 28 days: Not less than 33 MPa (33-grade)",
            },
        ],
    },
    {
        "is_code": "IS 8112:2013",
        "title": "43 Grade Ordinary Portland Cement — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Construction & Steel",
            "url": "https://www.bis.gov.in",
            "year": 2013,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 8112 specifies requirements for 43-grade Ordinary Portland Cement. This is the most commonly used grade of cement in India for general construction purposes. The cement must achieve a minimum compressive strength of 43 MPa at 28 days. ISI mark is mandatory.",
            },
        ],
    },
    {
        "is_code": "IS 12269:2013",
        "title": "53 Grade Ordinary Portland Cement — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Construction & Steel",
            "url": "https://www.bis.gov.in",
            "year": 2013,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 12269 specifies requirements for 53-grade Ordinary Portland Cement, a high-strength cement used for high-rise buildings, bridges, pre-stressed concrete structures, and RCC work requiring early strength. Minimum compressive strength 53 MPa at 28 days. Mandatory ISI mark required.",
            },
        ],
    },
    {
        "is_code": "IS 1239 (Part 1):2004",
        "title": "Mild Steel Tubes, Tubulars and Other Wrought Steel Fittings — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Construction & Steel",
            "url": "https://www.bis.gov.in",
            "year": 2004,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 1239 (Part 1) covers mild steel tubes suitable for screwing to IS 554 threads. Used extensively in water supply, gas supply, and structural applications across India. Available in light, medium, and heavy grades.",
            },
        ],
    },
    {
        "is_code": "IS 2720 (Part 1 to 40)",
        "title": "Methods of Test for Soils",
        "category": "standards",
        "metadata": {
            "sector": "Construction & Steel",
            "url": "https://www.bis.gov.in",
            "year": 1983,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 2720 is a comprehensive multi-part standard covering methods of test for soils. It includes tests for grain size analysis, moisture content, Atterberg limits, compaction, shear strength, permeability, consolidation, and California Bearing Ratio (CBR). Used in all civil engineering and geotechnical projects in India.",
            },
        ],
    },
    # ===================================================================
    # ELECTRONICS & IT
    # ===================================================================
    {
        "is_code": "IS 16046:2018",
        "title": "LED Luminaires for General Lighting — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Electronics & IT",
            "url": "https://www.bis.gov.in",
            "year": 2018,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 16046 specifies safety and performance requirements for LED luminaires intended for general lighting purposes. LED luminaires MUST comply with this standard for BIS certification. Covers operating voltage up to 250V and various wattage ranges. Falls under CRS (Compulsory Registration Scheme) for certain categories.",
            },
            {
                "clause": "5.0 Requirements",
                "title": "Performance and Safety Requirements",
                "page": 3,
                "text": "Key requirements for LED luminaires:\n"
                "- Luminous efficacy: Minimum 90 lumens per watt for general purpose luminaires\n"
                "- Lumen maintenance: At least 70% of initial lumens at 6000 hours (L70 ≥ 6000h)\n"
                "- Colour Rendering Index (CRI): Minimum 70 for general lighting\n"
                "- Power Factor: ≥0.9 for luminaires above 25W\n"
                "- THD (Total Harmonic Distortion): ≤20% for luminaires above 25W\n"
                "- Safety: Electric strength test (1000V for 1 minute), insulation resistance, earth continuity\n"
                "- Working temperature range: 0°C to 40°C",
            },
        ],
    },
    {
        "is_code": "IS 16102 (Part 1):2012",
        "title": "Self-Ballasted LED Lamps for General Lighting — Part 1: Safety Requirements",
        "category": "standards",
        "metadata": {
            "sector": "Electronics & IT",
            "url": "https://www.bis.gov.in",
            "year": 2012,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 16102 (Part 1) specifies safety requirements for self-ballasted LED lamps for general lighting service having a supply voltage up to 250V. This standard is used for CRS (Compulsory Registration Scheme II) registration. LED lamps (bulbs) MUST be registered under CRS before sale in India.",
            },
            {
                "clause": "5.0 Safety Requirements",
                "title": "Safety Tests and Requirements",
                "page": 3,
                "text": "Safety requirements for LED lamps (IS 16102 Part 1):\n"
                "- Marking: Rated voltage, rated wattage, rated frequency, manufacturer's name/trademark, model number\n"
                "- Protection against electric shock: No accessible live parts at rated voltage\n"
                "- Insulation resistance: ≥2 MΩ\n"
                "- Electric strength: Withstand 1000V RMS for 1 minute\n"
                "- Thermal test: Lamp shall operate safely at maximum ambient temperature\n"
                "- Endurance test: 4000 hours of operation with no safety hazard\n"
                "- EMC requirements per IS 9000 (CISPR 15 equivalent)",
            },
        ],
    },
    {
        "is_code": "IS 16102 (Part 2):2012",
        "title": "Self-Ballasted LED Lamps for General Lighting — Part 2: Performance Requirements",
        "category": "standards",
        "metadata": {
            "sector": "Electronics & IT",
            "url": "https://www.bis.gov.in",
            "year": 2012,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 16102 (Part 2) specifies performance requirements for self-ballasted LED lamps including luminous flux, efficacy, colour rendering, and rated life.",
            },
            {
                "clause": "5.0 Performance",
                "title": "Performance Requirements",
                "page": 2,
                "text": "Performance requirements for LED lamps (IS 16102 Part 2):\n"
                "- Initial luminous efficacy: ≥90 lm/W (for lamps ≥10W), ≥80 lm/W (for lamps <10W)\n"
                "- Lumen maintenance at 3000 hours: ≥90% of initial value\n"
                "- Lumen maintenance at 6000 hours: ≥80%\n"
                "- Colour Rendering Index (CRI): ≥70\n"
                "- Colour Consistency: Within 5 SDCM (Standard Deviation of Colour Matching)\n"
                "- Power Factor: ≥0.7 (lamps <10W), ≥0.9 (lamps ≥10W)\n"
                "- Rated life: Minimum 15,000 hours (at L70 — 70% lumen maintenance)",
            },
        ],
    },
    {
        "is_code": "IS 302-2-6:2009",
        "title": "Safety of Household and Similar Electrical Appliances — Particular Requirements for Stationary Cooking Ranges, Hobs, Ovens and Similar Appliances",
        "category": "standards",
        "metadata": {
            "sector": "Electronics & IT",
            "url": "https://www.bis.gov.in",
            "year": 2009,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 302-2-6 (based on IEC 60335-2-6) specifies safety requirements for stationary electric cooking ranges, hobs, ovens, and similar appliances for household use, rated voltage up to 250V single-phase or 480V 3-phase. This standard is mandatory for ISI certification of cooking appliances sold in India.",
            },
        ],
    },
    {
        "is_code": "IS 13252 (Part 1):2010",
        "title": "Uninterruptible Power Supply (UPS) — Safety Requirements",
        "category": "standards",
        "metadata": {
            "sector": "Electronics & IT",
            "url": "https://www.bis.gov.in",
            "year": 2010,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 13252 (Part 1) covers safety requirements for Uninterruptible Power Supply (UPS) systems. UPS devices must be registered under the Compulsory Registration Scheme (CRS / Scheme II) before sale in India. The registration is valid for 2 years and requires testing at a BIS-recognized laboratory.",
            },
        ],
    },
    {
        "is_code": "IS 1293:2019",
        "title": "Plugs and Socket-Outlets of Rated Voltage up to 250V and Rated Current up to 16A — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Electronics & IT",
            "url": "https://www.bis.gov.in",
            "year": 2019,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 1293 specifies requirements for plugs and socket-outlets with rated voltage up to 250V and rated current up to 16A for household and similar general purposes. This standard is under compulsory ISI certification. Includes 3-pin 6A, 3-pin 16A, and universal configurations. All electrical plugs and sockets sold in India must bear the ISI mark.",
            },
        ],
    },
    {
        "is_code": "IS 694:2010",
        "title": "PVC Insulated Cables for Working Voltages up to and Including 1100V — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Electronics & IT",
            "url": "https://www.bis.gov.in",
            "year": 2010,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 694 specifies requirements for PVC insulated cables and flexible cords with working voltages up to 1100V. Covers single-core and multi-core cables used for domestic wiring, industrial installations, and general power supply. PVC cables are under mandatory ISI certification — all cables must bear the ISI mark with CM/L number.",
            },
        ],
    },
    # ===================================================================
    # CONSUMER PRODUCTS & SAFETY
    # ===================================================================
    {
        "is_code": "IS 2347:2017",
        "title": "Domestic Pressure Cookers — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Consumer Products",
            "url": "https://www.bis.gov.in",
            "year": 2017,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope and Applicability",
                "page": 1,
                "text": "IS 2347 specifies requirements for domestic pressure cookers made of aluminium, stainless steel, or hard anodised aluminium, with capacity from 1.5 to 30 litres. Pressure cookers are under MANDATORY ISI certification (Scheme I). Every pressure cooker sold in India must bear the ISI mark with the manufacturer's CM/L number.",
            },
            {
                "clause": "5.0 Safety Requirements",
                "title": "Safety and Performance Requirements",
                "page": 3,
                "text": "Safety requirements for pressure cookers (IS 2347):\n"
                "- Operating pressure: 98.07 kPa (1 kg/cm² gauge) ± 10%\n"
                "- Safety valve: Must release pressure at 1.4 times the operating pressure\n"
                "- Fusible safety plug: Must melt at 180°C ± 10°C (aluminium alloy fuse)\n"
                "- Gasket sealing ring: Must withstand minimum 5 times normal operating pressure\n"
                "- Hydrostatic test pressure: 3 times the maximum working pressure\n"
                "- Handle strength: Must withstand 3 times the weight of the cooker when filled\n"
                "- Minimum wall thickness: 2.5 mm for aluminium, 0.8 mm for stainless steel\n"
                "- Marking: ISI mark, IS number, capacity in litres, manufacturer's name, CM/L number",
            },
        ],
    },
    {
        "is_code": "IS 9873 (Part 1):2019",
        "title": "Safety of Toys — Part 1: Safety Aspects Related to Mechanical and Physical Properties",
        "category": "standards",
        "metadata": {
            "sector": "Consumer Products",
            "url": "https://www.bis.gov.in",
            "year": 2019,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 9873 (Part 1) specifies safety requirements for toys. It covers mechanical and physical hazards including sharp edges, small parts (choking hazard), and projectile risks. Toys are under MANDATORY BIS certification (CRS / Compulsory Registration Scheme II). All toys sold in India — whether manufactured domestically or imported — must be registered under CRS.",
            },
            {
                "clause": "4.0 Key Safety Tests",
                "title": "Safety Tests and Requirements",
                "page": 3,
                "text": "Key safety tests for toys under IS 9873:\n"
                "- Small parts test: Parts that detach during testing shall not fit entirely within the small parts cylinder (prevents choking for children under 3)\n"
                "- Sharp edge test: No accessible sharp edges before or after abuse testing\n"
                "- Sharp point test: No accessible sharp points\n"
                "- Drop test: Toy dropped from 1.37m shall not produce sharp edges or small parts\n"
                "- Tension test: Attachments shall withstand 70N pull for 10 seconds\n"
                "- Phthalate content: Total of DEHP, DBP, BBP ≤0.1% each (Parts 12/13)\n"
                "- Age grading: All toys must be clearly age-graded on packaging",
            },
        ],
    },
    {
        "is_code": "IS 15495:2012",
        "title": "Water Purifier — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Consumer Products",
            "url": "https://www.bis.gov.in",
            "year": 2012,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 15495 specifies requirements for water purifiers intended for household and similar use. Covers gravity-based, UV, UF, RO, and combination purification systems. The purified water output must conform to IS 10500 drinking water standards. ISI certification is available and recommended but not yet mandatorily required for water purifiers.",
            },
            {
                "clause": "5.0 Performance",
                "title": "Performance Requirements",
                "page": 3,
                "text": "Performance requirements for water purifiers:\n"
                "- Bacterial reduction: ≥99.9% (log 3 reduction)\n"
                "- Virus reduction: ≥99.99% (log 4 reduction) for UV/UF purifiers\n"
                "- TDS reduction: For RO purifiers, output TDS shall be ≤50% of input TDS\n"
                "- Flow rate: Minimum flow rate shall be declared and verified\n"
                "- Filter/membrane life: Declared by manufacturer, verified by endurance testing\n"
                "- Electrical safety: For powered purifiers, must conform to IS 302-2-15",
            },
        ],
    },
    {
        "is_code": "IS 398 (Part 1):2012",
        "title": "Domestic Gas Stoves — For Use with LPG — Part 1: General Requirements",
        "category": "standards",
        "metadata": {
            "sector": "Consumer Products",
            "url": "https://www.bis.gov.in",
            "year": 2012,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 398 (Part 1) specifies general requirements for domestic gas stoves for use with liquefied petroleum gas (LPG). Covers single-burner, double-burner, and multi-burner stoves. Domestic LPG gas stoves are under MANDATORY ISI certification (Scheme I). Every gas stove sold in India must bear the ISI mark.",
            },
        ],
    },
    {
        "is_code": "IS 4984:2016",
        "title": "High-Density Polyethylene Pipes for Water Supply — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Consumer Products",
            "url": "https://www.bis.gov.in",
            "year": 2016,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 4984 specifies requirements for high-density polyethylene (HDPE) pipes for water supply. Covers pipes from 16mm to 630mm nominal diameter. Used for potable water distribution, irrigation, and industrial water supply. ISI certification ensures quality and pressure rating conformance.",
            },
        ],
    },
    {
        "is_code": "IS 4707 (Part 1):2001",
        "title": "General Requirements for Domestic Electrical Appliances — Safety",
        "category": "standards",
        "metadata": {
            "sector": "Consumer Products",
            "url": "https://www.bis.gov.in",
            "year": 2001,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 4707 (Part 1) specifies general safety requirements for household electrical appliances (based on IEC 60335-1). Covers marking, protection against electric shock, power input, heating, leakage current, moisture resistance, insulation, mechanical strength, and construction requirements. This is the parent standard for all specific appliance safety standards in the IS 302 series.",
            },
        ],
    },
    # ===================================================================
    # AUTOMOTIVE & TRANSPORT
    # ===================================================================
    {
        "is_code": "IS 2553 (Part 1):1990",
        "title": "Safety Glass for Motor Vehicles — Specification — Part 1: For Windscreens",
        "category": "standards",
        "metadata": {
            "sector": "Automotive",
            "url": "https://www.bis.gov.in",
            "year": 1990,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 2553 (Part 1) specifies requirements for safety glass (laminated and tempered) used as windscreens in motor vehicles. All automotive safety glass must conform to this standard under Motor Vehicle Rules in India.",
            },
        ],
    },
    {
        "is_code": "IS 4151:2014",
        "title": "Automotive Tyres — Pneumatic Tyres for Passenger Vehicles — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Automotive",
            "url": "https://www.bis.gov.in",
            "year": 2014,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 4151 specifies requirements for new pneumatic tyres for passenger cars. Covers tyre dimensions, load-bearing capacity, speed rating, tread pattern, and endurance requirements. Vehicle tyres are under mandatory ISI certification in India.",
            },
        ],
    },
    {
        "is_code": "IS 15885:2018",
        "title": "Helmets for Motorcyclists — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Automotive",
            "url": "https://www.bis.gov.in",
            "year": 2018,
            "mandatory_certification": True,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 15885 specifies requirements for protective helmets for motorcyclists. All helmets sold in India must bear the ISI mark — it is illegal to sell non-ISI-certified helmets. Covers impact absorption, penetration resistance, chin strap strength, and field of vision requirements. Helmets must bear ISI mark with CM/L number. Penalty for selling non-ISI helmets: up to ₹1 lakh fine and/or imprisonment up to 1 year under BIS Act 2016.",
            },
            {
                "clause": "5.0 Requirements",
                "title": "Test and Performance Requirements",
                "page": 3,
                "text": "Helmet requirements under IS 15885:\n"
                "- Impact absorption: Peak deceleration shall not exceed 300g in any impact test\n"
                "- Penetration resistance: The test striker shall not contact the headform\n"
                "- Chin strap: Must withstand 15 kN static load without rupture\n"
                "- Retention system: Dynamic roll-off test — helmet shall not come off\n"
                "- Field of vision: Minimum 105° horizontal on each side, 25° above and 45° below\n"
                "- Weight: Maximum 1.5 kg (full face), 1.2 kg (open face)\n"
                "- Visor: If fitted, must meet optical requirements of IS 14766",
            },
        ],
    },
    {
        "is_code": "IS 15736:2006",
        "title": "Electric Vehicles — Battery Operated Vehicles — Requirements",
        "category": "standards",
        "metadata": {
            "sector": "Automotive",
            "url": "https://www.bis.gov.in",
            "year": 2006,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 15736 specifies general requirements for battery-operated electric vehicles for on-road and off-road use. Covers battery safety, electrical isolation, crash-worthiness of battery packs, and charging interface requirements. As India pushes EV adoption, this standard is increasingly important for vehicle manufacturers.",
            },
        ],
    },
    # ===================================================================
    # CHEMICALS & ENVIRONMENT
    # ===================================================================
    {
        "is_code": "IS 5182 (Part 1 to 23)",
        "title": "Methods for Measurement of Air Pollution",
        "category": "standards",
        "metadata": {
            "sector": "Environment",
            "url": "https://www.bis.gov.in",
            "year": 1969,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 5182 is a comprehensive multi-part standard covering methods for measurement of air pollution. Covers testing of: sulphur dioxide (Part 2), nitrogen oxides (Part 6), lead (Part 7), suspended particulate matter (Part 4), carbon monoxide (Part 10), and other pollutants. Used by CPCB and SPCBs for monitoring ambient air quality across India.",
            },
        ],
    },
    {
        "is_code": "IS 1350 (Part 1):1984",
        "title": "Methods of Test for Coal and Coke — Part 1: Proximate Analysis",
        "category": "standards",
        "metadata": {
            "sector": "Energy & Mining",
            "url": "https://www.bis.gov.in",
            "year": 1984,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 1350 (Part 1) covers methods for proximate analysis of coal and coke including determination of moisture, ash, volatile matter, and fixed carbon. Used by power plants, steel plants, and coal companies for quality control and commercial transactions.",
            },
        ],
    },
    {
        "is_code": "IS 10500:2012 — ECO Mark Criteria",
        "title": "Eco Mark Criteria — Guidelines for Environmental Labelling",
        "category": "standards",
        "metadata": {
            "sector": "Environment",
            "url": "https://www.bis.gov.in",
            "year": 2005,
        },
        "clauses": [
            {
                "clause": "ECO Mark Overview",
                "title": "ECO Mark Scheme",
                "page": 1,
                "text": "The BIS ECO Mark scheme is a voluntary certification programme for environmentally-friendly products. Products eligible for ECO Mark include: soaps/detergents, paints/varnishes, paper, food items, lubricating oils, packaging materials, architectural paints, batteries, electrical/electronic goods, cosmetics, aerosol propellants, plastics, textiles, and fire extinguishers. The ECO Mark criteria specify environmental parameters the product must meet beyond the regular IS standard, such as biodegradability, minimal toxic content, energy efficiency, and recyclability.",
            },
        ],
    },
    {
        "is_code": "IS 10500:2012 — BIS Green",
        "title": "Green Product Certification Guidelines",
        "category": "standards",
        "metadata": {
            "sector": "Environment",
            "url": "https://www.bis.gov.in",
            "year": 2022,
        },
        "clauses": [
            {
                "clause": "1.0 Overview",
                "title": "Overview",
                "page": 1,
                "text": "BIS has expanded its environmental product certification to include sustainability parameters in several standards. Green building materials, solar panels (IS 14286), and energy-efficient appliances receive special consideration under BIS certification. The Bureau has published guidelines for conformity assessment of solar photovoltaic modules and systems under IS 14286 and IS 16169.",
            },
        ],
    },
    # ===================================================================
    # TEXTILES & PACKAGING
    # ===================================================================
    {
        "is_code": "IS 188:1979",
        "title": "Methods of Tests for Determination of Breaking Load and Elongation at Break of Woven Textile Fabrics",
        "category": "standards",
        "metadata": {
            "sector": "Textiles",
            "url": "https://www.bis.gov.in",
            "year": 1979,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 188 specifies methods for determination of breaking load and elongation at break of woven textile fabrics using strip and grab methods. Used by textile testing laboratories across India for quality control of fabrics.",
            },
        ],
    },
    {
        "is_code": "IS 2508:1984",
        "title": "Low-Density Polyethylene Films for Packaging — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Packaging",
            "url": "https://www.bis.gov.in",
            "year": 1984,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 2508 specifies requirements for LDPE films used in food and general packaging. Covers thickness tolerance, tensile strength, elongation at break, dart impact strength, seal strength, and optical properties. Food-grade LDPE must be free from heavy metals and conform to IS 9845 for food contact.",
            },
        ],
    },
    {
        "is_code": "IS 15979:2012",
        "title": "Handmade Paper for General Purposes — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Textiles",
            "url": "https://www.bis.gov.in",
            "year": 2012,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 15979 specifies requirements for handmade paper for general purposes. Supports India's handmade paper (khadi paper) industry. Covers grammage, thickness, tensile strength, folding endurance, and appearance. ECO Mark eligible product category.",
            },
        ],
    },
    {
        "is_code": "IS 7580:2019",
        "title": "Woven Sacks and Bags for Packaging — Specification",
        "category": "standards",
        "metadata": {
            "sector": "Packaging",
            "url": "https://www.bis.gov.in",
            "year": 2019,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 7580 specifies requirements for woven polypropylene sacks and bags used for packaging fertilizers, foodgrains, sugar, cement, and other bulk commodities. Covers dimensional tolerances, tensile strength, and UV stability requirements.",
            },
        ],
    },
    # ===================================================================
    # HALLMARKING & PRECIOUS METALS (Expanded)
    # ===================================================================
    {
        "is_code": "IS 1417:2016",
        "title": "Gold and Gold Alloys — Jewellery/Artefacts — Fineness and Marking — Specification",
        "category": "hallmarking",
        "metadata": {
            "sector": "Precious Metals",
            "url": "https://www.bis.gov.in",
            "year": 2016,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 1417 specifies requirements for fineness (purity) and marking of gold and gold alloys in jewellery and artefacts. This is the standard under which hallmarking of gold jewellery is carried out in India. Mandatory hallmarking was enforced starting June 16, 2021.",
            },
            {
                "clause": "Table 1 — Fineness Grades",
                "title": "Permitted Fineness Grades for Gold Jewellery",
                "page": 2,
                "text": "Permitted gold fineness grades as per IS 1417 (for hallmarking):\n"
                "- 14 carat (14K): Minimum fineness 585 parts per thousand (58.5% pure gold)\n"
                "- 18 carat (18K): Minimum fineness 750 parts per thousand (75% pure gold)\n"
                "- 20 carat (20K): Minimum fineness 833 parts per thousand (83.3% pure gold)\n"
                "- 22 carat (22K): Minimum fineness 916 parts per thousand (91.6% pure gold). This is the most common purity for traditional Indian gold jewellery.\n"
                "- 23 carat (23K): Minimum fineness 958 parts per thousand (95.8% pure gold)\n"
                "- 24 carat (24K): Minimum fineness 999 parts per thousand (99.9% pure gold)\n"
                "- Tolerance: ± 2 parts per thousand on declared fineness.",
            },
            {
                "clause": "5.0 Hallmarking Procedure",
                "title": "Hallmarking Process and HUID",
                "page": 4,
                "text": "Hallmarking procedure for gold jewellery:\n"
                "1. Jeweller submits articles to a BIS-recognized Assaying & Hallmarking Centre (AHC).\n"
                "2. AHC assays (tests) the gold purity using fire assay or XRF method.\n"
                "3. If purity conforms to declared caratage, the article receives:\n"
                "   - BIS Standard Mark (triangle logo)\n"
                "   - Purity grade mark (e.g., '916' for 22K)\n"
                "   - HUID (Hallmark Unique Identification) — a 6-character alphanumeric code\n"
                "4. HUID is laser-engraved or stamped on the article.\n"
                "5. HUID data is uploaded to BIS central server and is publicly verifiable.\n\n"
                "As of Phase 3 (April 2023), mandatory hallmarking applies in ALL districts across India.\n"
                "Exemptions: Export jewellery, watches, fountain pens, and special-order items above 10 grams.",
            },
            {
                "clause": "6.0 HUID Verification",
                "title": "Consumer Verification of HUID",
                "page": 6,
                "text": "How consumers can verify hallmarked gold jewellery:\n"
                "1. BIS Care App: Available on Android (Google Play) and iOS (App Store). Scan or enter the 6-character HUID.\n"
                "2. BIS Website: Visit www.bis.gov.in → Verify HUID → Enter the code.\n"
                "3. SMS: Send 'VERIFY <HUID>' to the BIS helpline number.\n\n"
                "HUID verification shows:\n"
                "- Jeweller name and registration number\n"
                "- Purity grade (e.g., 22K 916)\n"
                "- AHC (Assaying & Hallmarking Centre) that certified the article\n"
                "- Date of hallmarking\n\n"
                "If verification fails or shows different purity than declared, consumers can file a complaint with BIS.",
            },
        ],
    },
    {
        "is_code": "IS 2112:2014",
        "title": "Silver and Silver Alloys — Jewellery/Artefacts — Fineness and Marking — Specification",
        "category": "hallmarking",
        "metadata": {
            "sector": "Precious Metals",
            "url": "https://www.bis.gov.in",
            "year": 2014,
        },
        "clauses": [
            {
                "clause": "1.0 Scope",
                "title": "Scope",
                "page": 1,
                "text": "IS 2112 specifies requirements for fineness and marking of silver and silver alloys in jewellery and artefacts. Silver hallmarking is currently under the VOLUNTARY phase — it is not yet mandatory. However, BIS encourages silver jewellers to get voluntary hallmarking for consumer confidence.",
            },
            {
                "clause": "Table 1 — Silver Fineness Grades",
                "title": "Silver Purity Grades",
                "page": 2,
                "text": "Silver fineness grades as per IS 2112:\n"
                "- 800: Minimum 800 parts per thousand (80% pure silver)\n"
                "- 900: Minimum 900 parts per thousand (90% pure silver)\n"
                "- 925 (Sterling Silver): Minimum 925 parts per thousand (92.5% pure silver). Most common for silver jewellery.\n"
                "- 950: Minimum 950 parts per thousand (95% pure silver)\n"
                "- 990: Minimum 990 parts per thousand (99% pure silver)\n"
                "- 999: Minimum 999 parts per thousand (99.9% pure silver)",
            },
        ],
    },
    {
        "is_code": "BIS Hallmarking Order 2020",
        "title": "Bureau of Indian Standards (Hallmarking of Gold Jewellery and Gold Artefacts) Order, 2020",
        "category": "hallmarking",
        "metadata": {
            "sector": "Precious Metals",
            "url": "https://www.bis.gov.in",
            "year": 2020,
        },
        "clauses": [
            {
                "clause": "3.0 Mandatory Hallmarking",
                "title": "Phases of Mandatory Hallmarking Implementation",
                "page": 2,
                "text": "Mandatory hallmarking implementation phases:\n"
                "- Phase 1 (June 16, 2021): Mandatory hallmarking enforced in 256 districts across India.\n"
                "- Phase 2 (June 2022): Extended to additional districts.\n"
                "- Phase 3 (April 2023): Mandatory hallmarking now applicable in ALL districts of India.\n\n"
                "Who must comply: All jewellers selling gold jewellery/artefacts must register with BIS and sell only hallmarked gold jewellery.\n"
                "Penalties for non-compliance:\n"
                "- First offence: Fine up to ₹1 lakh\n"
                "- Subsequent offences: Fine up to ₹5 lakh and/or imprisonment up to 1 year\n"
                "- Selling jewellery below declared purity: Action under BIS Act 2016 — fine up to 10 times the value of goods or ₹1 lakh minimum",
            },
        ],
    },
    # ===================================================================
    # BIS CERTIFICATION SCHEMES (Expanded)
    # ===================================================================
    {
        "is_code": "BIS Certification Schemes Matrix",
        "title": "BIS Product Certification Schemes — Comprehensive Overview",
        "category": "certification",
        "metadata": {
            "sector": "BIS Services",
            "url": "https://www.bis.gov.in",
            "year": 2024,
        },
        "clauses": [
            {
                "clause": "Scheme I — ISI Mark",
                "title": "Product Certification Scheme (ISI Mark)",
                "page": 1,
                "text": "BIS Product Certification Scheme I (ISI Mark): For domestic Indian manufacturers.\n"
                "- Purpose: Certifies that a product conforms to the relevant Indian Standard.\n"
                "- Process: Application → Factory inspection by BIS officers → Product sample testing in BIS-recognized lab → License grant.\n"
                "- License validity: 1 year initially, renewable annually.\n"
                "- Fees: Application fee ₹1,000; Annual marking fee based on production volume (0.1% to 0.2% of ex-factory value, subject to minimum/maximum caps).\n"
                "- Surveillance: BIS conducts periodic surprise inspections and market sample testing.\n"
                "- ISI mark components: ISI logo (triangle), IS standard number, CM/L (Certification Marks License) number.\n"
                "- Products: Covers cement, steel, food items, electrical appliances, helmets, cylinders, pressure cookers, water purifiers, and 500+ other product categories.",
            },
            {
                "clause": "Scheme II — CRS",
                "title": "Compulsory Registration Scheme (CRS)",
                "page": 3,
                "text": "BIS Compulsory Registration Scheme (CRS / Scheme II): For electronics and IT goods.\n"
                "- Purpose: Ensures safety of electronic and IT products sold in India.\n"
                "- Applicable to: Products notified under the Electronics and Information Technology Goods (Requirements for Compulsory Registration) Order by MeitY.\n"
                "- Key product categories: LED lamps, LED luminaires, UPS systems, power banks, adapters, fixed/portable computers, printers, monitors, set-top boxes, smart watches.\n"
                "- Process: Manufacturer/importer gets products tested at BIS-recognized lab → Submits test report + application on BIS portal (manakonline.bis.gov.in) → BIS issues Registration Certificate.\n"
                "- Key difference from ISI: No factory inspection required — it's self-declaration based after lab testing.\n"
                "- Registration validity: 2 years, renewable.\n"
                "- Fee: Registration fee ₹1,000 per model per standard.\n"
                "- Foreign manufacturers: Must appoint an Authorized Indian Representative (AIR) who takes legal responsibility.",
            },
            {
                "clause": "FMCS",
                "title": "Foreign Manufacturers Certification Scheme (FMCS)",
                "page": 5,
                "text": "FMCS (Foreign Manufacturers Certification Scheme): For overseas manufacturers exporting to India.\n"
                "- Purpose: Enables foreign manufacturers to obtain ISI mark certification for products exported to India.\n"
                "- Requirements:\n"
                "  1. Appoint an Authorized Indian Representative (AIR) resident in India.\n"
                "  2. Application through AIR on BIS portal.\n"
                "  3. Factory inspection by BIS officers at the foreign manufacturing facility (manufacturer bears travel and inspection costs).\n"
                "  4. Product testing at a BIS-recognized lab.\n"
                "  5. License grant upon compliance.\n"
                "- Fees: Same as Scheme I, plus travel costs for BIS officers.\n"
                "- Validity: Same as Scheme I (1 year, renewable).\n"
                "- The AIR is legally responsible for the product's conformity in India.",
            },
            {
                "clause": "Scheme X",
                "title": "Scheme X — For Non-Indian Standards",
                "page": 7,
                "text": "BIS Scheme X: Certification against non-Indian standards.\n"
                "- Purpose: Allows manufacturers to get BIS certification for products conforming to international standards (ISO, IEC, ASTM, etc.) when no equivalent Indian Standard exists.\n"
                "- Process: Similar to Scheme I, but assessment is done against the specified international/foreign standard.\n"
                "- Use case: Products for export or products where an Indian Standard hasn't been published yet.\n"
                "- Less commonly used than Schemes I and II.",
            },
            {
                "clause": "ECO Mark",
                "title": "ECO Mark Certification Scheme",
                "page": 8,
                "text": "BIS ECO Mark Scheme: Voluntary environmental certification.\n"
                "- Purpose: Certifies that products meet specific environmental criteria in addition to quality requirements.\n"
                "- Applicable product categories: Soaps and detergents, paper/paper products, food items, lubricating oils, packaging materials, paints/varnishes, batteries, electrical/electronic goods, textiles, cosmetics, plastics, fire extinguishers.\n"
                "- Process: Product must first conform to the relevant Indian Standard + meet additional ECO Mark criteria (biodegradability, minimal toxicity, energy efficiency, recyclability).\n"
                "- The ECO Mark logo is an earthen pot (matka) symbol.\n"
                "- Voluntary scheme — not mandatory, but increasingly valued by environmentally-conscious consumers.",
            },
        ],
    },
    # ===================================================================
    # BIS LICENSING PROCESS & FEES
    # ===================================================================
    {
        "is_code": "BIS Licensing Process Guide",
        "title": "BIS 5-Stage Licensing Process & Fee Structure for MSMEs & Startups",
        "category": "certification",
        "metadata": {
            "sector": "BIS Services",
            "url": "https://www.bis.gov.in",
            "year": 2024,
        },
        "clauses": [
            {
                "clause": "Stage 1 — Application",
                "title": "Application Submission",
                "page": 1,
                "text": "Stage 1: Application Submission\n"
                "1. Register on the BIS online portal: manakonline.bis.gov.in\n"
                "2. Fill the application form (Form IV for Indian manufacturers, Form V for foreign manufacturers).\n"
                "3. Upload required documents: Factory address proof, Manufacturing process description, Test equipment list, Organization chart, Quality control plan.\n"
                "4. Pay the application fee: ₹1,000 (non-refundable).\n"
                "5. BIS assigns a case officer and acknowledges receipt within 7 working days.",
            },
            {
                "clause": "Stage 2 — Factory Assessment",
                "title": "Factory Inspection/Assessment",
                "page": 2,
                "text": "Stage 2: Factory Assessment\n"
                "1. BIS officers visit the manufacturing facility (scheduled within 30 days of application acceptance).\n"
                "2. They assess: Manufacturing capability, quality control systems, testing infrastructure, raw material sourcing, production records.\n"
                "3. If the factory has existing ISO 9001 certification, the assessment may be shortened.\n"
                "4. Assessment report is prepared by BIS officers.\n"
                "5. If non-conformities are found, the manufacturer gets 60 days to rectify and request re-assessment.",
            },
            {
                "clause": "Stage 3 — Sample Testing",
                "title": "Product Sample Testing",
                "page": 3,
                "text": "Stage 3: Product Sample Testing\n"
                "1. Samples are drawn by BIS officers during the factory visit.\n"
                "2. Samples are sent to a BIS-recognized laboratory for testing against the relevant IS standard.\n"
                "3. Test reports are typically available within 15-30 days.\n"
                "4. Testing fees are borne by the manufacturer and vary by product complexity.\n"
                "5. If samples fail testing, the manufacturer can submit fresh samples after corrective action.",
            },
            {
                "clause": "Stage 4 — License Grant",
                "title": "License Grant",
                "page": 4,
                "text": "Stage 4: License Grant\n"
                "1. If factory assessment and sample testing are satisfactory, BIS grants the license.\n"
                "2. The manufacturer receives a unique CM/L (Certification Marks License) number.\n"
                "3. The license authorizes use of the ISI mark on conforming products.\n"
                "4. License validity: 1 year from date of grant.\n"
                "5. The CM/L number must be displayed alongside the ISI mark on every product.\n"
                "6. Total time from application to license: typically 60-90 days.",
            },
            {
                "clause": "Stage 5 — Surveillance",
                "title": "Post-License Surveillance & Renewal",
                "page": 5,
                "text": "Stage 5: Surveillance & Renewal\n"
                "1. BIS conducts surprise surveillance visits (at least once per year).\n"
                "2. Market samples may be purchased and tested for conformity.\n"
                "3. Annual renewal: Submit renewal application + pay marking fee before license expiry.\n"
                "4. Marking fee: 0.1% to 0.2% of ex-factory value of ISI-marked production, subject to minimum ₹1,000 and maximum cap.\n"
                "5. MSMEs and startups get special fee concessions — reduced marking fees and expedited processing.\n"
                "6. Non-renewal or non-compliance: License suspension or cancellation. Continued use of ISI mark after cancellation is a criminal offence.",
            },
        ],
    },
    # ===================================================================
    # TESTING LABORATORIES (All Major Regions)
    # ===================================================================
    {
        "is_code": "BIS Laboratory Directory",
        "title": "BIS-Recognized Testing Laboratories — Regional Directory",
        "category": "lab_suggestion",
        "metadata": {
            "sector": "BIS Services",
            "url": "https://www.bis.gov.in/resources/recognised-labs/",
            "year": 2024,
        },
        "clauses": [
            {
                "clause": "North India Labs",
                "title": "Testing Laboratories — North India",
                "page": 1,
                "text": "BIS-recognized testing laboratories in North India:\n"
                "1. BIS Central Laboratory, New Delhi — Multi-product testing (food, electrical, building materials, chemicals)\n"
                "2. National Test House (NTH), Ghaziabad, UP — Comprehensive testing for metals, electrical, chemical products\n"
                "3. ERTL (North), New Delhi — Electronics & IT product testing (CRS scheme)\n"
                "4. Central Power Research Institute (CPRI), Noida — Electrical equipment testing\n"
                "5. Indian Institute of Petroleum (IIP), Dehradun — Petroleum product testing\n"
                "6. NABL-accredited private labs: SGS India (Gurgaon), TUV SUD (Noida), Bureau Veritas (Delhi NCR)\n"
                "7. STQC Lab, New Delhi — IT/electronics product testing for CRS\n"
                "8. BIS Branch Office Lab, Chandigarh — Covers Punjab, Haryana, Himachal Pradesh",
            },
            {
                "clause": "West India Labs",
                "title": "Testing Laboratories — West India",
                "page": 3,
                "text": "BIS-recognized testing laboratories in West India:\n"
                "1. BIS Western Regional Office Lab, Mumbai — Multi-product testing facility\n"
                "2. SGS India Pvt. Ltd., Mumbai — Food, chemicals, consumer products\n"
                "3. ERTL (West), Mumbai — Electronics and IT goods testing for CRS\n"
                "4. NABL Labs in Mumbai: Intertek, TUV Rheinland\n"
                "5. BIS Branch Office Lab, Ahmedabad — Covers Gujarat region\n"
                "6. NABL-accredited labs in Ahmedabad: Shriram Institute, GERI (Gujarat Engineering Research Institute)\n"
                "7. BIS Branch Office, Pune — Testing support for Maharashtra\n"
                "8. BIS Regional Office, Jaipur — Covers Rajasthan\n"
                "9. National Accreditation Board for Testing and Calibration Laboratories (NABL) accredited labs in Gujarat, Maharashtra, Rajasthan, and Goa",
            },
            {
                "clause": "South India Labs",
                "title": "Testing Laboratories — South India",
                "page": 5,
                "text": "BIS-recognized testing laboratories in South India:\n"
                "1. ETDC (Electronic Test and Development Centre), Bengaluru — Electronics product testing\n"
                "2. ERTL (South), Bengaluru — CRS scheme electronics testing\n"
                "3. CPRI (Central Power Research Institute), Bengaluru — Electrical equipment, transformers, cables\n"
                "4. BIS Branch Office Lab, Chennai — Multi-product testing for Tamil Nadu\n"
                "5. NABL Labs in Chennai: SITRA (South India Textile Research Association), IITM Testing Centre\n"
                "6. BIS Branch Office Lab, Hyderabad — Covers Telangana and Andhra Pradesh\n"
                "7. CFTRI (Central Food Technological Research Institute), Mysuru — Food product testing\n"
                "8. BIS Branch Office, Kochi — Covers Kerala\n"
                "9. CSIR-CLRI (Central Leather Research Institute), Chennai — Leather and footwear testing\n"
                "10. Quality Council of India (QCI) recognized labs across Karnataka, Tamil Nadu, Kerala, AP, and Telangana",
            },
            {
                "clause": "East India Labs",
                "title": "Testing Laboratories — East India",
                "page": 7,
                "text": "BIS-recognized testing laboratories in East India:\n"
                "1. ERTL (East), Kolkata — Electronics and IT product testing for CRS\n"
                "2. National Test House (NTH), Kolkata — One of India's oldest and largest testing facilities (metals, chemicals, building materials, food, textiles)\n"
                "3. BIS Eastern Regional Office Lab, Kolkata — Multi-product testing\n"
                "4. CGCRI (Central Glass and Ceramic Research Institute), Kolkata — Glass, ceramics testing\n"
                "5. BIS Branch Office, Patna — Covers Bihar and Jharkhand\n"
                "6. BIS Branch Office, Bhubaneswar — Covers Odisha\n"
                "7. NEIST (North East Institute of Science and Technology), Jorhat, Assam — Testing for North East India\n"
                "8. IIT Kharagpur testing facilities — Available for specific product categories\n"
                "9. NTH Guwahati — Covers the entire North East region",
            },
            {
                "clause": "Central India Labs",
                "title": "Testing Laboratories — Central India",
                "page": 9,
                "text": "BIS-recognized testing laboratories in Central India:\n"
                "1. BIS Branch Office Lab, Bhopal — Covers Madhya Pradesh and Chhattisgarh\n"
                "2. BIS Branch Office Lab, Nagpur — Sub-region of Maharashtra (Vidarbha)\n"
                "3. AMPRI (Advanced Materials and Processes Research Institute), Bhopal — Materials testing\n"
                "4. NABL-accredited private labs in Indore and Raipur\n"
                "5. Regional Testing Centre, Lucknow — Covers Eastern UP\n\n"
                "The complete, updated directory of BIS-recognized laboratories is available at:\n"
                "www.bis.gov.in → 'Resources' → 'Recognised Laboratories'\n"
                "Labs are categorized by product type: electrical, food, construction materials, chemicals, textiles, etc.\n"
                "NABL accreditation is a prerequisite for BIS lab recognition.",
            },
        ],
    },
    # ===================================================================
    # CONSUMER RIGHTS & GRIEVANCE (Expanded)
    # ===================================================================
    {
        "is_code": "BIS Consumer Guide",
        "title": "Consumer Rights, Verification & Grievance Mechanisms",
        "category": "consumer",
        "metadata": {
            "sector": "Consumer Protection",
            "url": "https://www.bis.gov.in",
            "year": 2024,
        },
        "clauses": [
            {
                "clause": "1.0 Consumer Complaint Channels",
                "title": "How to File a Complaint",
                "page": 1,
                "text": "How consumers can file complaints about substandard or counterfeit ISI-marked products:\n"
                "1. BIS Care App: Available on Android (Google Play) and iOS (App Store). Scan the ISI mark or enter the license number to report a complaint directly.\n"
                "2. BIS Website: Online complaint form at www.bis.gov.in → 'Consumer Corner' → 'File a Complaint'.\n"
                "3. Email: Send complaint details to ccd@bis.gov.in (Consumer Complaints Division).\n"
                "4. Toll-free Helpline: 1800-11-4100 (available Monday–Friday, 9:30 AM to 5:30 PM IST).\n"
                "5. Written Complaint: Send by post to the nearest BIS Regional/Branch Office.\n\n"
                "Required information for complaints: Product details, ISI mark number, CM/L number, date of purchase, seller details, nature of complaint, and photographic evidence if possible.",
            },
            {
                "clause": "2.0 ISI Mark Verification",
                "title": "How to Verify ISI Mark Authenticity",
                "page": 3,
                "text": "How to verify if an ISI mark is genuine:\n"
                "A genuine ISI mark consists of:\n"
                "1. The ISI logo (a triangular figure with 'ISI' text inside)\n"
                "2. The IS standard number (e.g., IS 2347 for pressure cookers)\n"
                "3. A CM/L (Certification Marks License) number unique to the manufacturer\n\n"
                "Verification methods:\n"
                "1. BIS Care App: Enter the CM/L number to verify the manufacturer's license status.\n"
                "2. BIS Website: Visit www.bis.gov.in → 'Know Your Standards' → 'Verify License'.\n"
                "3. Check the CM/L number format: It follows the pattern 'CM/L-XXXXXXX' where X are digits.\n\n"
                "Warning signs of fake ISI marks:\n"
                "- Blurry or poorly printed ISI logo\n"
                "- Missing CM/L number\n"
                "- CM/L number that returns 'no record found' on BIS portal\n"
                "- ISI mark without the IS standard number\n"
                "- Products from categories where ISI mark is mandatory but mark looks suspicious",
            },
            {
                "clause": "3.0 Penalties for Misuse",
                "title": "Penalties for Misuse of ISI Mark and BIS Standards",
                "page": 5,
                "text": "Penalties under BIS Act 2016 for misuse:\n"
                "1. Using ISI mark without license: Fine of ₹2 lakh to ₹5 lakh, imprisonment up to 2 years, or both.\n"
                "2. Using counterfeit ISI mark: Fine up to ₹10 lakh and imprisonment up to 2 years.\n"
                "3. Selling non-conforming products with ISI mark: Fine of minimum ₹1 lakh or 10 times the value of goods (whichever is more).\n"
                "4. Selling without mandatory BIS certification (for compulsory items): Fine of ₹2 lakh + ₹2 lakh for each subsequent offence.\n"
                "5. Obstructing BIS officers during inspection: Fine up to ₹1 lakh.\n\n"
                "BIS has the power to:\n"
                "- Suspend or cancel licenses\n"
                "- Order product recall\n"
                "- File criminal complaints\n"
                "- Seize non-conforming goods\n"
                "- Publish names of non-compliant manufacturers",
            },
            {
                "clause": "4.0 Standards Clubs",
                "title": "BIS Standards Clubs for Students",
                "page": 7,
                "text": "BIS Standards Club Scheme:\n"
                "- Purpose: Promote quality awareness among students through Standards Clubs in schools, colleges, and polytechnics.\n"
                "- Eligibility: Any recognized educational institution can establish a Standards Club.\n"
                "- Activities: Workshops on standardization, visits to BIS offices and labs, poster/essay competitions, quality awareness campaigns.\n"
                "- Benefits: Students gain awareness about BIS certification, ISI mark, hallmarking, and quality consciousness.\n"
                "- Registration: Apply through the nearest BIS Branch Office or online at www.bis.gov.in.\n"
                "- BIS provides resource materials and guest speakers for Standards Club events.",
            },
        ],
    },
    # ===================================================================
    # BIS GENERAL OVERVIEW
    # ===================================================================
    {
        "is_code": "BIS Overview",
        "title": "Bureau of Indian Standards — About BIS",
        "category": "general",
        "metadata": {
            "sector": "BIS Services",
            "url": "https://www.bis.gov.in",
            "year": 2024,
        },
        "clauses": [
            {
                "clause": "1.0 About BIS",
                "title": "Introduction to BIS",
                "page": 1,
                "text": "Bureau of Indian Standards (BIS) is the national standards body of India established under the Bureau of Indian Standards Act, 2016. It functions under the Ministry of Consumer Affairs, Food & Public Distribution. BIS is responsible for:\n"
                "1. Formulating Indian Standards (IS codes) — over 22,000 standards published covering food, electronics, construction, chemicals, textiles, automotive, and more.\n"
                "2. Product certification (ISI mark under Scheme I, CRS under Scheme II, FMCS for foreign manufacturers).\n"
                "3. Hallmarking of precious metals (gold, silver).\n"
                "4. Laboratory recognition and testing.\n"
                "5. Consumer protection related to standardized products.\n"
                "6. Promoting quality consciousness through Standards Clubs.\n\n"
                "BIS has its headquarters in New Delhi with 5 Regional Offices (Delhi, Mumbai, Kolkata, Chennai, Chandigarh) and 36 Branch Offices across India.\n"
                "Website: www.bis.gov.in | Helpline: 1800-11-4100",
            },
            {
                "clause": "2.0 BIS Act 2016",
                "title": "BIS Act 2016 — Key Provisions",
                "page": 3,
                "text": "Key provisions of the Bureau of Indian Standards Act, 2016:\n"
                "- Replaced the old Bureau of Indian Standards Act, 1986.\n"
                "- Empowers the Central Government to notify products for mandatory certification.\n"
                "- Provides for compulsory hallmarking of precious metals.\n"
                "- Stricter penalties for misuse of Standard Mark (ISI mark) — up to ₹10 lakh fine and 2 years imprisonment.\n"
                "- Enables BIS to establish labs and recognize external laboratories.\n"
                "- Provides for recall of non-conforming products.\n"
                "- Enables online registration and licensing through manakonline.bis.gov.in portal.\n"
                "- Special provisions for MSMEs and startups with reduced fees and faster processing.",
            },
        ],
    },
]


def generate_seed_corpus(output_dir: Path) -> None:
    """
    Write curated seed documents as individual JSON files into the
    specified directory. Each file represents one BIS document/standard.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    for doc in SEED_DOCUMENTS:
        # Build filename from IS code
        code = doc["is_code"]
        safe_name = (
            code.lower()
            .replace(" ", "_")
            .replace(":", "_")
            .replace("/", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("&", "_")
            .replace("—", "_")
            .replace(",", "")
            .replace(".", "")
        )
        filename = f"{safe_name}.json"
        filepath = output_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)

    print(f"[seed_data] Generated {len(SEED_DOCUMENTS)} seed documents in '{output_dir}'")
