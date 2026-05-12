"""M3.3 - Company Type Detection.

SG employer database (JSON config)
Known GLCs: DBS, OCBC, UOB, SingTel, etc.
Known Government/Statutory Boards
Known MNCs
Fallback: Claude Haiku classification
Cache per company (TTL 90 days)
"""
import hashlib
import json
import time
from dataclasses import dataclass
from typing import Optional

import structlog

from keystone.core import get_settings
from keystone.services.claude_client import get_claude_client, ClaudeResponse

logger = structlog.get_logger()

# Simple in-memory cache: company_name_lower → (classified_at, company_type)
_COMPANY_TYPE_CACHE: dict[str, tuple[float, str]] = {}
_COMPANY_CACHE_TTL_SECONDS = 90 * 24 * 60 * 60  # 90 days


# Known Singapore employers by type
KNOWN_GLCS = {
    # Banks
    "dbs": "banking_glc",
    "development bank of singapore": "banking_glc",
    "ocbc": "banking_glc",
    "oversea-chinese banking corporation": "banking_glc",
    "uob": "banking_glc",
    "united overseas bank": "banking_glc",
    "citi": "banking_glc",  # Citibank is partly GLC (Temasek stake)
    "standard chartered": "banking_glc",  # partly GLC

    # Telecom
    "singtel": "telecom_glc",
    "singapore telecommunications": "telecom_glc",
    "starhub": "telecom_glc",
    "m1": "telecom_glc",

    # Airlines
    "singapore airlines": "aviation_glc",
    "scoot": "aviation_glc",
    "sIA": "aviation_glc",

    # Utilities / Energy
    "sp group": "utilities_glc",
    "senoko energy": "energy_glc",
    "yondr": "energy_glc",
    "Keppel": "energy_glc",
    "kem Facilities management": "utilities_glc",

    # Transport
    "SMRT": "transport_glc",
    " SBS": "transport_glc",
    "comfortdelgro": "transport_glc",
    "taxi": "transport_glc",

    # Others
    "psa corporation": "port_glc",
    "jurong port": "port_glc",
    "hdb": "housing_glc",
    "housing development board": "housing_glc",
    "JTC": "industrial_glc",
    "EDB": "economic_glc",
    "IE Singapore": "economic_glc",
    "Singapore Economic Development Board": "economic_glc",
    "SGX": "finance_glc",
    "singapore exchange": "finance_glc",
    "MAS": "regulatory_glc",
    "monetary authority of singapore": "regulatory_glc",
    "CPF": "social_glc",
    "central provident fund": "social_glc",
    "board of engineers": "regulatory_glc",
    "PE": "transport_glc",
    "parkway": "healthcare_glc",
    "raffles medical": "healthcare_glc",
    "national university hospital": "healthcare_glc",
    "nuh": "healthcare_glc",
    "alexandra hospital": "healthcare_glc",
    "singhealth": "healthcare_glc",
    "national healthcare group": "healthcare_glc",
}

KNOWN_GOVERNMENT_DEPARTMENTS = {
    "ministry of defence": "government",
    "mindef": "government",
    "ministry of education": "government",
    "moe": "government",
    "ministry of health": "government",
    "moh": "government",
    "ministry of manpower": "government",
    "mom": "government",
    "public service commission": "government",
    "civil service college": "government",
    "ira": "government",
    "smart nation": "government",
    "government technology agency": "government",
    "govtech": "government",
    "infocomm media development authority": "government",
    "imda": "government",
    "economic development board": "government",
    "edb": "government",
    "jtc corporation": "government",
    "housing development board": "government",
    "hdb": "government",
    "urban redevelopment authority": "government",
    "ura": "government",
    "land transport authority": "government",
    "lta": "government",
    "maritime and port authority": "government",
    "mpa": "government",
    "civil aviation authority of singapore": "government",
    "caas": "government",
    "nlb": "government",
    "national library board": "government",
    "national parks board": "government",
    "nparks": "government",
    "public utilities board": "government",
    "pub": "government",
    "energy market authority": "government",
    "ema": "government",
    "accounting and corporate regulatory authority": "government",
    "acra": "government",
    "accounting standards council": "government",
    "agence francaise de developpement": "government",
    "air navigation service authority": "government",
    "central bank": "government",
    "defence science and technology agency": "government",
    "dsta": "government",
    "defence technology exchange": "government",
    "dutw": "government",
    "geodata": "government",
    "immigration and checkpoints authority": "government",
    "ica": "government",
    "international enterprise singapore": "government",
    "jgc": "government",
    "keppel": "government",
    "law society": "government",
    "monetary authority": "government",
    "public sector reform": "government",
    "psd": "government",
    "public sector division": "government",
    "real estate": "government",
    "rose": "government",
    "sec": "government",
    "sec singapore": "government",
    "singapore customs": "government",
    "singapore police force": "government",
    "spf": "government",
    "singapore prison service": "government",
    "sps": "government",
    "statutory boards": "government",
    "strategy group": "government",
    "trade and industry": "government",
    "mti": "government",
}

KNOWN_MNCS = {
    "google": "mnc_tech",
    "alphabet": "mnc_tech",
    "meta": "mnc_tech",
    "facebook": "mnc_tech",
    "amazon": "mnc_tech",
    "apple": "mnc_tech",
    "microsoft": "mnc_tech",
    "ibm": "mnc_tech",
    "intel": "mnc_tech",
    "nvidia": "mnc_tech",
    "oracle": "mnc_tech",
    "salesforce": "mnc_tech",
    "sap": "mnc_tech",
    "adobe": "mnc_tech",
    "paypal": "mnc_tech",
    "stripe": "mnc_tech",
    "shopify": "mnc_tech",
    "atlassian": "mnc_tech",
    "grab": "mnc_fintech",
    "sea group": "mnc_tech",
    "shopee": "mnc_tech",
    "lazada": "mnc_tech",
    "tencent": "mnc_tech",
    "bytedance": "mnc_tech",
    "tiktok": "mnc_tech",
    "字节跳动": "mnc_tech",
    "jpmorgan": "mnc_banking",
    "jpm": "mnc_banking",
    "goldman sachs": "mnc_banking",
    "gs": "mnc_banking",
    "morgan stanley": "mnc_banking",
    "ms": "mnc_banking",
    "bank of america": "mnc_banking",
    "bac": "mnc_banking",
    "merrill lynch": "mnc_banking",
    "wells fargo": "mnc_banking",
    "hsbc": "mnc_banking",
    "barclays": "mnc_banking",
    "credit suisse": "mnc_banking",
    "ubs": "mnc_banking",
    "deutsche bank": "mnc_banking",
    "Société Générale": "mnc_banking",
    "bnp Paribas": "mnc_banking",
    "pwc": "mnc_professional",
    "pricewaterhousecoopers": "mnc_professional",
    "deloitte": "mnc_professional",
    "kpmg": "mnc_professional",
    "ey": "mnc_professional",
    "ernst & young": "mnc_professional",
    "accenture": "mnc_professional",
    "mckinsey": "mnc_professional",
    "bcg": "mnc_professional",
    "bain": "mnc_professional",
    "booz allen": "mnc_professional",
    "nestle": "mnc_fmcg",
    "unilever": "mnc_fmcg",
    "procter & gamble": "mnc_fmcg",
    "pg": "mnc_fmcg",
    "johnson & johnson": "mnc_pharma",
    "jnj": "mnc_pharma",
    "pfizer": "mnc_pharma",
    "novartis": "mnc_pharma",
    "roche": "mnc_pharma",
    "merck": "mnc_pharma",
    "abbott": "mnc_pharma",
    "siemens": "mnc_industrial",
    "schneider electric": "mnc_industrial",
    "honeywell": "mnc_industrial",
    "ge": "mnc_industrial",
    "general electric": "mnc_industrial",
    "bosch": "mnc_industrial",
    "caterpillar": "mnc_industrial",
    "bae systems": "mnc_defense",
    "lockheed martin": "mnc_defense",
    "raytheon": "mnc_defense",
}


@dataclass
class CompanyClassification:
    """Company classification result."""
    company_name: str
    company_type: str  # banking_glc|fintech|startup|mnc|government| sme|other
    confidence: float  # 0.0 to 1.0
    classification_method: str  # "database" | "ai_fallback"


_COMPANY_TYPE_SYSTEM_PROMPT = """You are a company classification specialist for Singapore.

Classify the company type for the company name below.
Return ONLY valid JSON with these exact fields:
- company_type: One of:
  - banking_glc: Singapore government-linked banks (DBS, OCBC, UOB, etc.)
  - telecom_glc: Singapore telco GLCs (SingTel, StarHub, M1)
  - aviation_glc: Singapore aviation GLCs (Singapore Airlines, Scoot)
  - energy_glc: Singapore energy GLCs
  - transport_glc: Singapore transport GLCs (SMRT, SBS, ComfortDelGro)
  - utilities_glc: Singapore utilities GLCs (SP Group, etc.)
  - healthcare_glc: Singapore healthcare GLCs (NUH, SingHealth, etc.)
  - government: Singapore government ministries, departments, statutory boards
  - mnc_tech: Multinational technology company
  - mnc_banking: Multinational bank
  - mnc_professional: Professional services firm (consulting, accounting, legal)
  - mnc_fmcg: Multinational FMCG company
  - mnc_pharma: Multinational pharmaceutical company
  - mnc_industrial: Multinational industrial/manufacturing company
  - mnc_defense: Multinational defense contractor
  - mnc_fintech: Multinational fintech company
  - startup: Startup or venture-funded company
  - fintech: Singapore-based fintech
  - sme: Small or medium enterprise
  - other: Cannot determine

Return ONLY valid JSON, no markdown or explanation."""


def classify_company(company_name: str) -> CompanyClassification:
    """Classify company type using SG employer database.

    Args:
        company_name: Company name to classify

    Returns:
        CompanyClassification with type and confidence
    """
    if not company_name or company_name == "Not Specified":
        return CompanyClassification(
            company_name=company_name,
            company_type="other",
            confidence=0.0,
            classification_method="none",
        )

    company_lower = company_name.lower().strip()
    cache_key = company_lower

    # Check cache
    now = time.time()
    if cache_key in _COMPANY_TYPE_CACHE:
        cached_at, cached_type = _COMPANY_TYPE_CACHE[cache_key]
        if now - cached_at < _COMPANY_CACHE_TTL_SECONDS:
            logger.info("company_classify.cache_hit", company=company_name)
            return CompanyClassification(
                company_name=company_name,
                company_type=cached_type,
                confidence=1.0,
                classification_method="database",
            )

    # Check known databases (in order of specificity)
    if company_lower in KNOWN_GLCS:
        company_type = KNOWN_GLCS[company_lower]
        _COMPANY_TYPE_CACHE[cache_key] = (now, company_type)
        logger.info("company_classify.glc", company=company_name, type=company_type)
        return CompanyClassification(
            company_name=company_name,
            company_type=company_type,
            confidence=1.0,
            classification_method="database",
        )

    if company_lower in KNOWN_GOVERNMENT_DEPARTMENTS:
        company_type = KNOWN_GOVERNMENT_DEPARTMENTS[company_lower]
        _COMPANY_TYPE_CACHE[cache_key] = (now, company_type)
        logger.info("company_classify.gov", company=company_name, type=company_type)
        return CompanyClassification(
            company_name=company_name,
            company_type=company_type,
            confidence=1.0,
            classification_method="database",
        )

    if company_lower in KNOWN_MNCS:
        company_type = KNOWN_MNCS[company_lower]
        _COMPANY_TYPE_CACHE[cache_key] = (now, company_type)
        logger.info("company_classify.mnc", company=company_name, type=company_type)
        return CompanyClassification(
            company_name=company_name,
            company_type=company_type,
            confidence=1.0,
            classification_method="database",
        )

    # Partial match on known names
    for known_name, company_type in KNOWN_GLCS.items():
        if known_name in company_lower or company_lower in known_name:
            _COMPANY_TYPE_CACHE[cache_key] = (now, company_type)
            return CompanyClassification(
                company_name=company_name,
                company_type=company_type,
                confidence=0.8,
                classification_method="database",
            )

    for known_name, company_type in KNOWN_MNCS.items():
        if known_name in company_lower or company_lower in known_name:
            _COMPANY_TYPE_CACHE[cache_key] = (now, company_type)
            return CompanyClassification(
                company_name=company_name,
                company_type=company_type,
                confidence=0.8,
                classification_method="database",
            )

    # Fall back to AI classification
    return _classify_company_with_ai(company_name)


async def _classify_company_with_ai(company_name: str) -> CompanyClassification:
    """Classify company type using Claude Haiku.

    Args:
        company_name: Company name to classify

    Returns:
        CompanyClassification with AI-classified type
    """
    settings = get_settings()
    client = get_claude_client()

    prompt = f"""Classify this company:

{company_name}

Return ONLY valid JSON."""

    try:
        response: ClaudeResponse = await client.generate(
            model=settings.anthropic_model_haiku,
            system_prompt=_COMPANY_TYPE_SYSTEM_PROMPT,
            user_prompt=prompt,
            timeout=10.0,  # Analysis ≤10s per spec
            max_tokens=256,
        )

        content = response.content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])

        result = json.loads(content)
        company_type = result.get("company_type", "other")

        # Cache the result
        cache_key = company_name.lower().strip()
        now = time.time()
        _COMPANY_TYPE_CACHE[cache_key] = (now, company_type)

        logger.info("company_classify.ai", company=company_name, type=company_type)

        return CompanyClassification(
            company_name=company_name,
            company_type=company_type,
            confidence=0.6,  # AI classification is lower confidence
            classification_method="ai_fallback",
        )

    except json.JSONDecodeError:
        logger.warning("company_classify.ai_failed", company=company_name)
        return CompanyClassification(
            company_name=company_name,
            company_type="other",
            confidence=0.0,
            classification_method="ai_failed",
        )
    except Exception as e:
        logger.error("company_classify.error", company=company_name, error=str(e))
        return CompanyClassification(
            company_name=company_name,
            company_type="other",
            confidence=0.0,
            classification_method="error",
        )


def clear_company_cache(company_name: Optional[str] = None) -> None:
    """Clear company classification cache.

    Args:
        company_name: If provided, clear only this company's cache. Otherwise clear all.
    """
    if company_name:
        cache_key = company_name.lower().strip()
        if cache_key in _COMPANY_TYPE_CACHE:
            del _COMPANY_TYPE_CACHE[cache_key]
    else:
        _COMPANY_TYPE_CACHE.clear()
