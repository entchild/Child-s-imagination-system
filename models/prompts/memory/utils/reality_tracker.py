from typing import Dict, Any, List, Optional

class RealityTracker:
    """
    تشخیص تغییر واقعیت و مدیریت سفر شناختی کاربر
    """
    def __init__(self, similarity_threshold: float = 0.6):
        self.threshold = similarity_threshold
    
    def is_new_reality(self, 
                       current_analysis: Dict[str, Any], 
                       similar_realities: List[Dict]) -> bool:
        """
        تشخیص اینکه آیا این یک واقعیت جدید است یا ادامه واقعیت قبلی
        """
        # اگر هیچ واقعیت مشابهی نباشد، قطعاً جدید است
        if not similar_realities:
            print("🔍 واقعیت جدید تشخیص داده شد (بدون سابقه)")
            return True
        
        # بررسی فاصله (distance) نزدیکترین واقعیت
        closest_distance = similar_realities[0].get('distance', 1.0)
        
        # در ChromaDB، distance کمتر به معنای شباهت بیشتر است
        # برای cosine similarity، distance=0 یعنی کاملاً مشابه
        if closest_distance > (1 - self.threshold):
            print(f"🔍 واقعیت جدید تشخیص داده شد (فاصله: {closest_distance})")
            return True
        else:
            print(f"🔍 ادامه واقعیت قبلی (فاصله: {closest_distance})")
            return False
    
    def get_reality_shift_description(self, 
                                      current: Dict[str, Any], 
                                      previous: Optional[Dict[str, Any]]) -> str:
        """
        توصیف چگونگی تغییر واقعیت
        """
        if not previous:
            return "اولین تعامل کاربر"
        
        shifts = []
        
        # مقایسه وضعیت عاطفی
        if current.get("emotional_state") != previous.get("emotional_state"):
            shifts.append(f"وضعیت عاطفی از {previous.get('emotional_state')} به {current.get('emotional_state')} تغییر کرد")
        
        # مقایسه باورها
        current_beliefs = set(current.get("beliefs", []))
        prev_beliefs = set(previous.get("beliefs", []))
        
        new_beliefs = current_beliefs - prev_beliefs
        if new_beliefs:
            shifts.append(f"باورهای جدید: {', '.join(new_beliefs)}")
        
        lost_beliefs = prev_beliefs - current_beliefs
        if lost_beliefs:
            shifts.append(f"باورهای کناررفته: {', '.join(lost_beliefs)}")
        
        if shifts:
            return " | ".join(shifts)
        else:
            return "تغییر ظریفی detectable نیست"
