from core.features.feature_builder import build_features
from core.scoring.scoring_engine import calculate_score
from core.decision.decision_engine import make_decision
from core.context.market_context import get_market_context

from risk.tp_sl_engine import build_trade_levels
from risk.risk_manager import validate_trade


def run_pipeline(symbol, market_data):
    # ❗ ФИЛЬТР: слишком маленький ATR
    if market_data["atr"] < market_data["price"] * 0.002:
        return make_decision(symbol, 0, "range")

    features = build_features(market_data)

    score = calculate_score(features)

    context = get_market_context(features)

    signal = make_decision(symbol, score, context)

    if signal.side == "NONE":
        return signal

    levels = build_trade_levels(signal, market_data)

    if not levels:
        return signal

    if not validate_trade(levels):
        signal.side = "NONE"
        return signal

    signal.levels = levels

    return signal