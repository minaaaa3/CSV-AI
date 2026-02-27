from pydantic import BaseModel, Field
from typing import List

class SalesInsight(BaseModel):
    metric_name: str = Field(..., description="KPIの名称（例：客単価）")
    current_value: float
    previous_value: float
    change_rate: float = Field(..., description="前月比などの変化率（0.1 = 10%増）")

class BusinessBottleneck(BaseModel):
    issue: str = Field(..., description="特定された課題")
    evidence_value: str = Field(..., description="根拠となる数値データ")
    severity: str = Field(..., description="重要度（High/Med/Low）")

class StructuredReport(BaseModel):
    kpis: List[SalesInsight] = Field(..., description="主要なKPIのリスト")
    bottlenecks: List[BusinessBottleneck] = Field(..., description="特定された課題のリスト")
    proposed_focus_segment: str = Field(..., description="最も注力すべき顧客層とその理由")