import openai
from typing import List, Dict, Any
import json

class LLMInterface:
    """
    ارتباط با مدل زبانی
    """
    def __init__(self, api_key: str = None, use_local: bool = True):
        self.use_local = use_local
        
        if not use_local and api_key:
            openai.api_key = api_key
    
    def analyze_reality(self, user_text: str, prompt_template: str) -> Dict[str, Any]:
        """
        تحلیل متن کاربر برای استخراج "واقعیت"
        """
        # اینجا از یک مدل ساده تقلید می‌کنیم (برای شروع)
        # در نسخه بعدی با LLM واقعی جایگزین می‌شود
        
        # تحلیل بسیار ساده بر اساس کلمات کلیدی
        analysis = {
            "emotional_state": self._detect_emotion(user_text),
            "beliefs": self._detect_beliefs(user_text),
            "cognitive_needs": self._detect_needs(user_text),
            "shift_indicators": self._detect_shift(user_text)
        }
        
        return analysis
    
    def _detect_emotion(self, text: str) -> str:
        """تشخیص ساده وضعیت عاطفی"""
        emotion_keywords = {
            "شاد": ["خوشحال", "عالی", "خوب"],
            "غمگین": ["غمگین", "ناراحت", "افسرده"],
            "سردرگم": ["نمی‌دانم", "مردد", "شک"],
            "مشتاق": ["کنجکاو", "می‌خواهم", "علاقه"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(kw in text for kw in keywords):
                return emotion
        
        return "خنثی"
    
    def _detect_beliefs(self, text: str) -> List[str]:
        """تشخیص ساده باورها"""
        beliefs = []
        belief_keywords = {
            "مادی‌گرایی": ["پول", "ثروت", "مادی"],
            "معنوی": ["روح", "معنا", "هدف"],
            "شک‌گرا": ["چرا", "شک", "مطمئن نیستم"]
        }
        
        for belief, keywords in belief_keywords.items():
            if any(kw in text for kw in keywords):
                beliefs.append(belief)
        
        return beliefs if beliefs else ["نامشخص"]
    
    def _detect_needs(self, text: str) -> str:
        """تشخیص نیاز شناختی"""
        if "چرا" in text:
            return "جستجوی معنا"
        elif "چطور" in text:
            return "راهنمایی عملی"
        elif "احساس" in text:
            return "همدلی و درک"
        else:
            return "اطلاعات عمومی"
    
    def _detect_shift(self, text: str) -> List[str]:
        """تشخیص نشانه‌های تغییر"""
        indicators = []
        shift_keywords = {
            "تغییر نگرش": ["قبلاً فکر می‌کردم", "عوض شده", "دیگر"],
            "بحران": ["بی‌معنا", "پوچ", "چرا"],
            "آغاز": ["تازه فهمیدم", "الان می‌بینم"]
        }
        
        for indicator, keywords in shift_keywords.items():
            if any(kw in text for kw in keywords):
                indicators.append(indicator)
        
        return indicators
    
    def generate_response(self, 
                          user_text: str, 
                          analysis: Dict[str, Any],
                          similar_realities: List[Dict],
                          prompt_template: str) -> str:
        """
        تولید پاسخ بر اساس تحلیل و واقعیت‌های مشابه
        """
        # در این نسخه ساده، پاسخ‌های از پیش تعریف‌شده برمی‌گردانیم
        emotional_state = analysis.get("emotional_state", "")
        
        responses = {
            "غمگین": "به نظر می‌رسد این روزها احساس ناراحتی می‌کنی. اگر دوست داری بیشتر درباره‌اش صحبت کنیم، من اینجام.",
            "سردرگم": "احساس سردرگمی گاهی می‌تونه نشانه رشد باشه. چه چیزی بیشتر از همه تو رو مردد کرده؟",
            "مشتاق": "اشتیاق تو برای کشف رو حس می‌کنم. دقیقاً چه چیزی بیشتر از همه کنجکاوت کرده؟",
            "خنثی": "متوجه شدم. می‌تونی بیشتر توضیح بدی؟"
        }
        
        return responses.get(emotional_state, "متوجه شدم. لطفاً بیشتر توضیح بده.")
