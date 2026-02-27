import os
import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv
from models import StructuredReport

# --- 1. 設定・初期化 ---
def setup_gemini():
    """環境変数からAPIキーを読み込みGeminiを初期化する"""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    # 万が一、標準のload_dotenvが失敗した時のための予備ロジック
    if not api_key:
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(dotenv_path):
            with open(dotenv_path, "r") as f:
                for line in f:
                    if "GEMINI_API_KEY" in line:
                        api_key = line.strip().split("=")[1].strip("'\"")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY が .env に見つかりません。")
        
    genai.configure(api_key=api_key)
    return 'gemini-flash-latest'

MODEL_ID = setup_gemini()
model = genai.GenerativeModel(MODEL_ID)


# --- 2. ビジネスロジック ---
def get_structured_analysis(file_path="data/sample.csv"):
    """CSVを読み込み、Geminiで構造化データに変換する"""
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except:
        df = pd.read_csv(file_path, encoding="shift_jis")
    
    print(f"\nAI ({MODEL_ID}) がCSVデータを解析中...")
    
    prompt = (
        "売上データを分析し、JSON形式でレポートを出してください。\n\n"
        f"【売上データ】\n{df.to_csv(index=False)}"
    )
    
    response = model.generate_content(
        prompt,
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": StructuredReport,
        }
    )
    return StructuredReport.model_validate_json(response.text)


def generate_next_actions(analysis_result):
    """分析結果に基づき施策案を生成する"""
    print("🚀 施策案と実行スケジュールを生成中...")
    
    bottlenecks = "\n".join([f"- {b.issue} ({b.severity})" for b in analysis_result.bottlenecks])
    prompt = f"""
    あなたはAIコンサルタントです。以下の分析結果に基づき、具体的施策案を提案してください。
    【課題】\n{bottlenecks}
    【最優先ターゲット】\n{analysis_result.proposed_focus_segment}
    【出力形式】\n1. 具体的施策（3つ以内） 2. 実行スケジュール（Mermaidのgantt形式）
    """
    return model.generate_content(prompt).text


# --- 3. メイン実行 ---
def main():
    try:
        # ステップ1: 分析
        result = get_structured_analysis()
        
        print("\n" + "="*50)
        print("📊 LayerX Ai Workforce Prototype: 分析結果")
        print("="*50)
        print(f"🎯 推奨ターゲット: {result.proposed_focus_segment}")
        print("\n📈 主要KPI:")
        for kpi in result.kpis:
            print(f"- {kpi.metric_name}: {kpi.current_value} (前月比: {kpi.change_rate*100:+.1f}%)")
        
        # ステップ2: 施策生成
        user_input = input("\n💡 施策案を生成しますか？ (y/n): ").strip().lower()
        if user_input in ['y', '']:
            actions = generate_next_actions(result)
            print("\n" + "="*50 + "\n" + actions + "\n" + "="*50)
            
            with open("final_proposal.md", "w", encoding="utf-8") as f:
                f.write(actions)
            print("✅ 'final_proposal.md' に保存完了！")
                
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    main()