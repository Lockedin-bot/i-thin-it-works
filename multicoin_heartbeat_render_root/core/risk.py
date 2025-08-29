def position_size(equity:float, risk_per_trade:float, entry:float, stop:float):
    risk_amt = equity * risk_per_trade
    per_unit_risk = max(entry - stop, 0.0001)
    units = max(int(risk_amt / per_unit_risk), 0)
    return units
