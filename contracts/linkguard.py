# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json

class LinkGuard(gl.Contract):
    """
    LinkGuard — Decentralized trust signal protocol on GenLayer.
    AI validators analyze wallet addresses, usernames, and domains
    and reach consensus on their trust level before storing on-chain.
    """

    trust_registry: DynArray[str]

    def __init__(self):
        pass

    @gl.public.view
    def get_trust_registry(self) -> list:
        return list(self.trust_registry)

    @gl.public.write
    def analyze_target(
        self,
        target_type: str,
        target_value: str,
        context: str
    ) -> None:
        """
        Submit a wallet address, username, or domain for AI trust analysis.

        Parameters
        ----------
        target_type  : "wallet" | "username" | "domain"
        target_value : The actual address, username, or domain to analyze
        context      : Optional context about why this target is being checked
        """

        t_type  = target_type
        t_value = target_value
        t_ctx   = context

        def get_trust_signal() -> str:
            task = f"""You are a blockchain security analyst for the LinkGuard protocol.
Your role is to analyze the trustworthiness of a submitted target and return a structured trust signal.

Submitted target:
Type: {t_type}
Value: {t_value}
Context: {t_ctx}

Apply these analysis rules in order:

RULE 1 - VALID INPUT:
If the target_type is not one of: wallet, username, domain
Return:
{{"trust_level": "UNKNOWN", "risk_score": 10, "signal": "REJECTED", "reasoning": "Invalid target type. Must be wallet, username, or domain."}}

RULE 2 - EMPTY VALUE:
If the target_value is empty or too short to analyze
Return:
{{"trust_level": "UNKNOWN", "risk_score": 10, "signal": "REJECTED", "reasoning": "Target value is empty or invalid."}}

RULE 3 - KNOWN SCAM PATTERNS:
Check if the target shows common scam or phishing patterns:
- For domains: typosquatting, fake protocol names, suspicious TLDs
- For usernames: impersonation of known projects or people
- For wallets: known mixer patterns or suspicious formatting
If clearly malicious return:
{{"trust_level": "UNTRUSTED", "risk_score": 9, "signal": "FLAGGED", "reasoning": "Target shows patterns consistent with known scam or phishing activity."}}

RULE 4 - TRUST ANALYSIS:
Based on your knowledge, analyze the target and return one of:
- TRUSTED: Well-known legitimate entity, verified project, or reputable address
- NEUTRAL: No strong signals either way, proceed with caution
- UNTRUSTED: Shows red flags, suspicious patterns, or known bad actor signals

Return ONLY this JSON format:
{{
    "trust_level": "TRUSTED" | "NEUTRAL" | "UNTRUSTED" | "UNKNOWN",
    "risk_score": <integer 1-10, where 1=very safe, 10=very dangerous>,
    "signal": "VERIFIED" | "NEUTRAL" | "FLAGGED" | "REJECTED",
    "reasoning": <one or two sentences explaining the trust signal>
}}

Nothing else. No extra words. No markdown. Pure JSON only."""

            result = (
                gl.nondet.exec_prompt(task)
                .replace("```json", "")
                .replace("```", "")
            )
            print(result)
            return result

        result = gl.eq_principle.prompt_comparative(
            get_trust_signal,
            "The values of trust_level and signal must match"
        )

        parsed = json.loads(result)

        entry = (
            f"{str(gl.message.sender_address)}"
            f"|{t_type}"
            f"|{t_value}"
            f"|{parsed['trust_level']}"
            f"|{parsed['signal']}"
            f"|{parsed['risk_score']}"
            f"|{parsed['reasoning']}"
        )

        self.trust_registry.append(entry)
